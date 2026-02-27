package com.supervertaler.sidecar;

import io.javalin.Javalin;
import io.javalin.config.SizeUnit;
import io.javalin.http.Context;
import io.javalin.http.UploadedFile;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.nio.file.*;
import java.util.*;

/**
 * Supervertaler Okapi Sidecar — lightweight REST service that wraps
 * Okapi Framework filters for document extraction and merge.
 *
 * Endpoints:
 *   GET  /health           → liveness check
 *   GET  /filters          → list supported file formats
 *   POST /extract          → upload file, get segments as JSON
 *   POST /merge            → upload original + translations, get translated file
 *   POST /tmx/read         → upload TMX, get TUs as JSON
 *   POST /tmx/validate     → upload TMX, get validation report
 *   POST /segment          → send text + SRX rules, get segmented result
 */
public class App {

    private static final Logger log = LoggerFactory.getLogger(App.class);
    private static final ObjectMapper mapper = new ObjectMapper()
            .enable(SerializationFeature.INDENT_OUTPUT);

    private static FilterService filterService;

    public static void main(String[] args) {
        int port = 8090;

        // Parse command-line args
        for (String arg : args) {
            if (arg.startsWith("--port=")) {
                port = Integer.parseInt(arg.substring(7));
            }
        }

        filterService = new FilterService();

        Javalin app = Javalin.create(config -> {
            // Allow large file uploads (100 MB)
            config.jetty.multipartConfig.maxFileSize(100, SizeUnit.MB);
            config.jetty.multipartConfig.maxTotalRequestSize(100, SizeUnit.MB);

            // CORS for local development — only localhost origins
            config.bundledPlugins.enableCors(cors -> {
                cors.addRule(rule -> {
                    rule.allowHost("http://localhost", "http://127.0.0.1");
                });
            });
        });

        // ── Health check ─────────────────────────────────────────
        app.get("/health", ctx -> {
            Map<String, Object> health = new LinkedHashMap<>();
            health.put("status", "ok");
            health.put("service", "supervertaler-okapi-sidecar");
            health.put("version", "0.1.0");
            health.put("okapi_version", filterService.getOkapiVersion());
            ctx.json(health);
        });

        // ── List supported filters ───────────────────────────────
        app.get("/filters", ctx -> {
            ctx.json(filterService.getSupportedFilters());
        });

        // ── Extract segments from a document ─────────────────────
        app.post("/extract", App::handleExtract);

        // ── Merge translations back into original document ───────
        app.post("/merge", App::handleMerge);

        // ── Read TMX file ────────────────────────────────────────
        app.post("/tmx/read", App::handleTmxRead);

        // ── Validate TMX file ────────────────────────────────────
        app.post("/tmx/validate", App::handleTmxValidate);

        // ── Segment text using SRX rules ─────────────────────────
        app.post("/segment", App::handleSegment);

        // ── Error handling ───────────────────────────────────────
        app.exception(Exception.class, (e, ctx) -> {
            log.error("Request failed: {}", e.getMessage(), e);
            Map<String, Object> error = new LinkedHashMap<>();
            error.put("error", true);
            error.put("message", e.getMessage());
            error.put("type", e.getClass().getSimpleName());
            ctx.status(500).json(error);
        });

        app.start(port);
        log.info("Supervertaler Okapi Sidecar started on port {}", port);
    }

    // ═══════════════════════════════════════════════════════════════
    //  /extract — Upload a file, get segments as JSON
    // ═══════════════════════════════════════════════════════════════
    private static void handleExtract(Context ctx) throws Exception {
        UploadedFile file = ctx.uploadedFile("file");
        if (file == null) {
            ctx.status(400).json(Map.of("error", true,
                    "message", "Missing 'file' in multipart upload"));
            return;
        }

        String sourceLang = ctx.formParam("source_lang");
        String targetLang = ctx.formParam("target_lang");
        boolean doSegmentation = !"false".equals(ctx.formParam("segment"));

        if (sourceLang == null || sourceLang.isBlank()) {
            sourceLang = "en";
        }
        if (targetLang == null || targetLang.isBlank()) {
            targetLang = "fr";
        }

        // Save uploaded file to temp directory
        Path tempDir = Files.createTempDirectory("okapi-extract-");
        Path tempFile = tempDir.resolve(file.filename());
        try (InputStream is = file.content()) {
            Files.copy(is, tempFile, StandardCopyOption.REPLACE_EXISTING);
        }

        try {
            ExtractResult result = filterService.extract(
                    tempFile, file.filename(), sourceLang, targetLang, doSegmentation);
            ctx.json(result);
        } finally {
            // Clean up temp files
            deleteRecursive(tempDir);
        }
    }

    // ═══════════════════════════════════════════════════════════════
    //  /merge — Upload original + translations, get translated file
    // ═══════════════════════════════════════════════════════════════
    private static void handleMerge(Context ctx) throws Exception {
        UploadedFile originalFile = ctx.uploadedFile("original");
        if (originalFile == null) {
            ctx.status(400).json(Map.of("error", true,
                    "message", "Missing 'original' file in multipart upload"));
            return;
        }

        String translationsJson = ctx.formParam("translations");
        if (translationsJson == null || translationsJson.isBlank()) {
            ctx.status(400).json(Map.of("error", true,
                    "message", "Missing 'translations' JSON parameter"));
            return;
        }

        String sourceLang = ctx.formParam("source_lang");
        String targetLang = ctx.formParam("target_lang");
        if (sourceLang == null) sourceLang = "en";
        if (targetLang == null) targetLang = "fr";

        // Parse translations JSON
        @SuppressWarnings("unchecked")
        List<MergeSegment> segments = Arrays.asList(
                mapper.readValue(translationsJson, MergeSegment[].class));

        // Save original to temp
        Path tempDir = Files.createTempDirectory("okapi-merge-");
        Path tempFile = tempDir.resolve(originalFile.filename());
        try (InputStream is = originalFile.content()) {
            Files.copy(is, tempFile, StandardCopyOption.REPLACE_EXISTING);
        }

        try {
            byte[] merged = filterService.merge(
                    tempFile, originalFile.filename(),
                    sourceLang, targetLang, segments);

            // Determine output filename
            String outName = originalFile.filename();
            int dot = outName.lastIndexOf('.');
            if (dot > 0) {
                outName = outName.substring(0, dot) + "_" + targetLang + outName.substring(dot);
            }

            ctx.header("Content-Disposition", "attachment; filename=\"" + outName + "\"");
            ctx.header("Content-Type", "application/octet-stream");
            ctx.result(merged);
        } finally {
            deleteRecursive(tempDir);
        }
    }

    // ═══════════════════════════════════════════════════════════════
    //  /tmx/read — Parse a TMX file and return TUs as JSON
    // ═══════════════════════════════════════════════════════════════
    private static void handleTmxRead(Context ctx) throws Exception {
        UploadedFile file = ctx.uploadedFile("file");
        if (file == null) {
            ctx.status(400).json(Map.of("error", true,
                    "message", "Missing 'file' in multipart upload"));
            return;
        }

        Path tempDir = Files.createTempDirectory("okapi-tmx-");
        Path tempFile = tempDir.resolve(file.filename());
        try (InputStream is = file.content()) {
            Files.copy(is, tempFile, StandardCopyOption.REPLACE_EXISTING);
        }

        try {
            TmxReadResult result = filterService.readTmx(tempFile);
            ctx.json(result);
        } finally {
            deleteRecursive(tempDir);
        }
    }

    // ═══════════════════════════════════════════════════════════════
    //  /tmx/validate — Check a TMX file for errors
    // ═══════════════════════════════════════════════════════════════
    private static void handleTmxValidate(Context ctx) throws Exception {
        UploadedFile file = ctx.uploadedFile("file");
        if (file == null) {
            ctx.status(400).json(Map.of("error", true,
                    "message", "Missing 'file' in multipart upload"));
            return;
        }

        Path tempDir = Files.createTempDirectory("okapi-tmx-val-");
        Path tempFile = tempDir.resolve(file.filename());
        try (InputStream is = file.content()) {
            Files.copy(is, tempFile, StandardCopyOption.REPLACE_EXISTING);
        }

        try {
            TmxValidationResult result = filterService.validateTmx(tempFile);
            ctx.json(result);
        } finally {
            deleteRecursive(tempDir);
        }
    }

    // ═══════════════════════════════════════════════════════════════
    //  /segment — Segment text using SRX rules
    // ═══════════════════════════════════════════════════════════════
    private static void handleSegment(Context ctx) throws Exception {
        SegmentRequest req = ctx.bodyAsClass(SegmentRequest.class);

        if (req.text == null || req.text.isBlank()) {
            ctx.status(400).json(Map.of("error", true,
                    "message", "Missing 'text' in request body"));
            return;
        }
        if (req.language == null) req.language = "en";

        List<String> segments = filterService.segment(req.text, req.language);
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("language", req.language);
        result.put("segment_count", segments.size());
        result.put("segments", segments);
        ctx.json(result);
    }

    // ── Utility ──────────────────────────────────────────────────

    private static void deleteRecursive(Path path) {
        try {
            if (Files.isDirectory(path)) {
                try (var entries = Files.list(path)) {
                    entries.forEach(App::deleteRecursive);
                }
            }
            Files.deleteIfExists(path);
        } catch (IOException e) {
            log.warn("Failed to delete temp file: {}", path, e);
        }
    }

    // ── Request/response DTOs used by /segment ──────────────────

    public static class SegmentRequest {
        public String text;
        public String language;
    }
}
