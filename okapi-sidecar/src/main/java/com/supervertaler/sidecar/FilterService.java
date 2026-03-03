package com.supervertaler.sidecar;

import net.sf.okapi.common.*;
import net.sf.okapi.common.encoder.EncoderManager;
import net.sf.okapi.common.filters.IFilter;
import net.sf.okapi.common.filters.IFilterConfigurationMapper;
import net.sf.okapi.common.filters.FilterConfigurationMapper;
import net.sf.okapi.common.filterwriter.IFilterWriter;
import net.sf.okapi.common.resource.*;
import net.sf.okapi.common.LocaleId;
import net.sf.okapi.lib.segmentation.SRXDocument;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.net.URI;
import java.nio.file.*;
import java.util.*;
import java.util.regex.*;
import java.util.stream.Collectors;

/**
 * Core service that wraps Okapi Framework filters for extraction, merge,
 * TMX reading/validation, and SRX segmentation.
 */
public class FilterService {

    private static final Logger log = LoggerFactory.getLogger(FilterService.class);

    /** Maps file extensions to Okapi filter configuration IDs. */
    private final IFilterConfigurationMapper fcMapper;

    /** Default SRX document for segmentation. */
    private SRXDocument defaultSrx;

    /** Supported formats: extension → description */
    private static final Map<String, String> SUPPORTED_FORMATS;

    static {
        Map<String, String> m = new LinkedHashMap<>();
        m.put(".docx",  "Microsoft Word 2007+ (OpenXML)");
        m.put(".xlsx",  "Microsoft Excel 2007+ (OpenXML)");
        m.put(".pptx",  "Microsoft PowerPoint 2007+ (OpenXML)");
        m.put(".html",  "HTML");
        m.put(".htm",   "HTML");
        m.put(".xliff", "XLIFF 1.2");
        m.put(".xlf",   "XLIFF 1.2");
        m.put(".tmx",   "TMX (Translation Memory eXchange)");
        m.put(".po",    "PO (Gettext)");
        m.put(".idml",  "Adobe InDesign Markup (IDML)");
        SUPPORTED_FORMATS = Collections.unmodifiableMap(m);
    }

    public FilterService() {
        // Set up the filter configuration mapper with all bundled filters
        fcMapper = new FilterConfigurationMapper();
        fcMapper.addConfigurations("net.sf.okapi.filters.openxml.OpenXMLFilter");
        fcMapper.addConfigurations("net.sf.okapi.filters.tmx.TmxFilter");
        fcMapper.addConfigurations("net.sf.okapi.filters.html.HtmlFilter");
        fcMapper.addConfigurations("net.sf.okapi.filters.xliff.XLIFFFilter");
        fcMapper.addConfigurations("net.sf.okapi.filters.po.POFilter");
        fcMapper.addConfigurations("net.sf.okapi.filters.idml.IDMLFilter");

        // Load the default SRX rules bundled with Okapi
        loadDefaultSrx();

        log.info("FilterService initialised — {} filters available", SUPPORTED_FORMATS.size());
    }

    public String getOkapiVersion() {
        // Okapi doesn't have a simple version API, so we read from the JAR manifest
        try {
            Package pkg = IFilter.class.getPackage();
            String v = pkg != null ? pkg.getImplementationVersion() : null;
            return v != null ? v : "unknown";
        } catch (Exception e) {
            return "unknown";
        }
    }

    public List<Map<String, String>> getSupportedFilters() {
        List<Map<String, String>> result = new ArrayList<>();
        for (var entry : SUPPORTED_FORMATS.entrySet()) {
            Map<String, String> item = new LinkedHashMap<>();
            item.put("extension", entry.getKey());
            item.put("description", entry.getValue());
            result.add(item);
        }
        return result;
    }

    // ═══════════════════════════════════════════════════════════════
    //  EXTRACT — Parse a document and return source segments
    // ═══════════════════════════════════════════════════════════════

    public ExtractResult extract(Path filePath, String filename,
                                 String srcLang, String trgLang,
                                 boolean doSegmentation) {

        String configId = getConfigIdForFile(filename);
        LocaleId sourceLocale = LocaleId.fromString(srcLang);
        LocaleId targetLocale = LocaleId.fromString(trgLang);

        List<ExtractedSegment> segments = new ArrayList<>();
        int textUnitCount = 0;

        // Track the current sub-document context (body, header, footer, etc.)
        String currentSubDoc = "body";

        IFilter filter = fcMapper.createFilter(configId);
        if (filter == null) {
            throw new IllegalArgumentException(
                    "No Okapi filter found for configuration: " + configId);
        }

        try {
            RawDocument rawDoc = new RawDocument(filePath.toUri(), "UTF-8", sourceLocale, targetLocale);
            filter.open(rawDoc);

            while (filter.hasNext()) {
                Event event = filter.next();

                // Track sub-document boundaries (headers, footers, etc.)
                EventType etype = event.getEventType();
                if (etype == EventType.START_SUBDOCUMENT) {
                    IResource res = event.getResource();
                    if (res instanceof StartSubDocument) {
                        StartSubDocument ssd = (StartSubDocument) res;
                        currentSubDoc = ssd.getName() != null
                                ? ssd.getName() : "subdocument";
                        log.debug("Entering sub-document: {}", currentSubDoc);
                    }
                } else if (etype == EventType.END_SUBDOCUMENT) {
                    log.debug("Leaving sub-document: {}", currentSubDoc);
                    currentSubDoc = "body";
                }

                if (event.isTextUnit()) {
                    ITextUnit tu = event.getTextUnit();
                    if (!tu.isTranslatable()) continue;

                    textUnitCount++;
                    String tuId = tu.getId();
                    String tuName = tu.getName() != null ? tu.getName() : "";

                    if (doSegmentation && defaultSrx != null) {
                        // Segment the source content using SRX rules
                        // Returns [plainText, taggedText] pairs
                        List<String[]> segs = segmentTextContentWithTags(
                                tu.getSource(), srcLang);
                        for (int i = 0; i < segs.size(); i++) {
                            String[] pair = segs.get(i);
                            segments.add(new ExtractedSegment(
                                    tuId, i, pair[0], pair[1],
                                    tu.getType(), tu.isReferent(),
                                    tuName, currentSubDoc));
                        }
                    } else {
                        // Return the full text unit as a single segment
                        TextFragment tf = tu.getSource().getFirstContent();
                        String plain = tf.toText();
                        String tagged = convertCodesToTags(tf);
                        // Only include tagged version if different from plain
                        String taggedResult = tagged.equals(plain) ? null : tagged;
                        segments.add(new ExtractedSegment(
                                tuId, 0, plain, taggedResult,
                                tu.getType(), tu.isReferent(),
                                tuName, currentSubDoc));
                    }
                }
            }
        } finally {
            filter.close();
        }

        ExtractResult result = new ExtractResult();
        result.filename = filename;
        result.sourceLang = srcLang;
        result.targetLang = trgLang;
        result.filterUsed = configId;
        result.textUnitCount = textUnitCount;
        result.segmentCount = segments.size();
        result.segments = segments;
        return result;
    }

    // ═══════════════════════════════════════════════════════════════
    //  MERGE — Re-create the original document with translations
    // ═══════════════════════════════════════════════════════════════

    public byte[] merge(Path originalPath, String filename,
                        String srcLang, String trgLang,
                        List<MergeSegment> translations) {

        String configId = getConfigIdForFile(filename);
        LocaleId sourceLocale = LocaleId.fromString(srcLang);
        LocaleId targetLocale = LocaleId.fromString(trgLang);

        // Build a lookup: textUnitId → list of translated segments (ordered)
        Map<String, List<MergeSegment>> txMap = new LinkedHashMap<>();
        for (MergeSegment seg : translations) {
            txMap.computeIfAbsent(seg.id, k -> new ArrayList<>()).add(seg);
        }

        IFilter filter = fcMapper.createFilter(configId);
        if (filter == null) {
            throw new IllegalArgumentException(
                    "No Okapi filter found for configuration: " + configId);
        }

        // Prepare output
        Path outputPath;
        try {
            outputPath = Files.createTempFile("okapi-merge-out-", getSuffix(filename));
        } catch (IOException e) {
            throw new RuntimeException("Failed to create temp output file", e);
        }

        try {
            RawDocument rawDoc = new RawDocument(originalPath.toUri(), "UTF-8",
                    sourceLocale, targetLocale);
            filter.open(rawDoc);

            IFilterWriter writer = filter.createFilterWriter();
            writer.setOptions(targetLocale, "UTF-8");
            writer.setOutput(outputPath.toString());

            while (filter.hasNext()) {
                Event event = filter.next();

                if (event.isTextUnit()) {
                    ITextUnit tu = event.getTextUnit();

                    List<MergeSegment> segs = txMap.get(tu.getId());
                    if (segs != null && !segs.isEmpty()) {
                        // Concatenate all segment translations for this TU
                        StringBuilder combined = new StringBuilder();
                        for (MergeSegment seg : segs) {
                            if (seg.translation != null) {
                                if (combined.length() > 0) combined.append(" ");
                                combined.append(seg.translation);
                            }
                        }
                        // Set translation as the target, preserving inline codes
                        TextContainer target = tu.createTarget(
                                targetLocale, false, IResource.COPY_ALL);
                        TextFragment sourceContent = tu.getSource().getFirstContent();
                        target.setContent(
                            buildTargetFragment(combined.toString(), sourceContent));
                    }
                }

                writer.handleEvent(event);
            }

            writer.close();
            filter.close();

            return Files.readAllBytes(outputPath);
        } catch (IOException e) {
            throw new RuntimeException("Merge failed: " + e.getMessage(), e);
        } finally {
            try { Files.deleteIfExists(outputPath); } catch (IOException ignored) {}
        }
    }

    // ═══════════════════════════════════════════════════════════════
    //  TMX READ — Parse a TMX file and return translation units
    // ═══════════════════════════════════════════════════════════════

    public TmxReadResult readTmx(Path tmxPath) {
        LocaleId sourceLocale = LocaleId.fromString("en");
        // TMX files define their own languages internally; we supply a
        // dummy target locale so the RawDocument constructor is satisfied.
        LocaleId targetLocale = LocaleId.fromString("fr");

        IFilter filter = fcMapper.createFilter("okf_tmx");
        if (filter == null) {
            throw new IllegalStateException("TMX filter not available");
        }

        TmxReadResult result = new TmxReadResult();
        result.translationUnits = new ArrayList<>();

        try {
            RawDocument rawDoc = new RawDocument(tmxPath.toUri(), "UTF-8",
                    sourceLocale, targetLocale);
            filter.open(rawDoc);

            while (filter.hasNext()) {
                Event event = filter.next();

                if (event.isTextUnit()) {
                    ITextUnit tu = event.getTextUnit();
                    TmxTranslationUnit tmxTu = new TmxTranslationUnit();
                    tmxTu.id = tu.getId();

                    // Source
                    if (tu.getSource() != null) {
                        tmxTu.source = TextFragment.getText(
                                tu.getSource().getCodedText());
                    }

                    // All target languages
                    tmxTu.targets = new LinkedHashMap<>();
                    for (LocaleId loc : tu.getTargetLocales()) {
                        TextContainer tc = tu.getTarget(loc);
                        if (tc != null) {
                            tmxTu.targets.put(loc.toString(),
                                    TextFragment.getText(tc.getCodedText()));
                        }
                    }

                    // Properties (metadata)
                    tmxTu.properties = new LinkedHashMap<>();
                    for (String propName : tu.getPropertyNames()) {
                        Property prop = tu.getProperty(propName);
                        if (prop != null) {
                            tmxTu.properties.put(propName, prop.getValue());
                        }
                    }

                    result.translationUnits.add(tmxTu);
                }
            }
        } finally {
            filter.close();
        }

        result.tuCount = result.translationUnits.size();
        result.filename = tmxPath.getFileName().toString();
        return result;
    }

    // ═══════════════════════════════════════════════════════════════
    //  TMX VALIDATE — Check a TMX file for structural issues
    // ═══════════════════════════════════════════════════════════════

    public TmxValidationResult validateTmx(Path tmxPath) {
        TmxValidationResult result = new TmxValidationResult();
        result.filename = tmxPath.getFileName().toString();
        result.issues = new ArrayList<>();

        LocaleId sourceLocale = LocaleId.fromString("en");
        LocaleId targetLocale = LocaleId.fromString("fr");

        IFilter filter = fcMapper.createFilter("okf_tmx");
        if (filter == null) {
            result.valid = false;
            result.issues.add(new TmxIssue("error",
                    "TMX filter not available", 0));
            return result;
        }

        int tuCount = 0;
        int emptySource = 0;
        int emptyTarget = 0;
        Set<String> languages = new LinkedHashSet<>();

        try {
            RawDocument rawDoc = new RawDocument(tmxPath.toUri(), "UTF-8",
                    sourceLocale, targetLocale);
            filter.open(rawDoc);

            while (filter.hasNext()) {
                Event event = filter.next();

                if (event.isTextUnit()) {
                    ITextUnit tu = event.getTextUnit();
                    tuCount++;

                    // Check for empty source
                    if (tu.getSource() == null ||
                        tu.getSource().getCodedText().isBlank()) {
                        emptySource++;
                        result.issues.add(new TmxIssue("warning",
                                "Empty source in TU " + tu.getId(), tuCount));
                    }

                    // Check targets
                    for (LocaleId loc : tu.getTargetLocales()) {
                        languages.add(loc.toString());
                        TextContainer tc = tu.getTarget(loc);
                        if (tc == null || tc.getCodedText().isBlank()) {
                            emptyTarget++;
                            result.issues.add(new TmxIssue("warning",
                                    "Empty target (" + loc + ") in TU " + tu.getId(),
                                    tuCount));
                        }
                    }
                }
            }

            result.valid = result.issues.stream()
                    .noneMatch(i -> "error".equals(i.level));
            result.tuCount = tuCount;
            result.languages = new ArrayList<>(languages);
            result.emptySourceCount = emptySource;
            result.emptyTargetCount = emptyTarget;

        } catch (Exception e) {
            result.valid = false;
            result.issues.add(new TmxIssue("error",
                    "Parse error: " + e.getMessage(), tuCount));
        } finally {
            filter.close();
        }

        return result;
    }

    // ═══════════════════════════════════════════════════════════════
    //  SEGMENT — Segment text using Okapi's SRX engine
    // ═══════════════════════════════════════════════════════════════

    public List<String> segment(String text, String language) {
        if (defaultSrx == null) {
            // Fallback: return as single segment
            return List.of(text);
        }

        ISegmenter segmenter = defaultSrx.compileLanguageRules(
                LocaleId.fromString(language), null);

        TextContainer tc = new TextContainer(text);
        segmenter.computeSegments(tc);
        tc.getSegments().create(segmenter.getRanges());

        List<String> result = new ArrayList<>();
        for (Segment seg : tc.getSegments()) {
            String segText = seg.getContent().toText();
            if (!segText.isBlank()) {
                result.add(segText);
            }
        }
        return result;
    }

    // ── Internal helpers ─────────────────────────────────────────

    /**
     * Segment the text content of a TextContainer using SRX rules.
     * Returns a list of [plainText, taggedText] pairs.
     * taggedText includes HTML-like formatting tags; null if no formatting.
     */
    private List<String[]> segmentTextContentWithTags(TextContainer source, String lang) {
        if (defaultSrx == null || source == null) {
            String text = source != null
                    ? TextFragment.getText(source.getCodedText())
                    : "";
            String tagged = source != null
                    ? convertCodesToTags(source.getFirstContent())
                    : "";
            if (text.isBlank()) return new ArrayList<>();
            String taggedResult = tagged.equals(text) ? null : tagged;
            List<String[]> fallback = new ArrayList<>();
            fallback.add(new String[]{text, taggedResult});
            return fallback;
        }

        ISegmenter segmenter = defaultSrx.compileLanguageRules(
                LocaleId.fromString(lang), null);
        segmenter.computeSegments(source);
        source.getSegments().create(segmenter.getRanges());

        List<String[]> result = new ArrayList<>();
        for (Segment seg : source.getSegments()) {
            TextFragment tf = seg.getContent();
            String plain = TextFragment.getText(tf.getCodedText());
            if (!plain.isBlank()) {
                String tagged = convertCodesToTags(tf);
                String taggedResult = tagged.equals(plain) ? null : tagged;
                result.add(new String[]{plain, taggedResult});
            }
        }
        return result;
    }

    /**
     * Load the default SRX segmentation rules that ship with Okapi.
     */
    private void loadDefaultSrx() {
        try {
            // Try loading the default SRX from Okapi's bundled resources
            InputStream is = getClass().getResourceAsStream(
                    "/net/sf/okapi/lib/segmentation/defaultSegmentation.srx");
            if (is == null) {
                // Alternative path
                is = SRXDocument.class.getResourceAsStream("defaultSegmentation.srx");
            }
            if (is != null) {
                defaultSrx = new SRXDocument();
                defaultSrx.loadRules(is);
                is.close();
                log.info("Default SRX segmentation rules loaded");
            } else {
                log.warn("Default SRX rules not found — segmentation disabled");
            }
        } catch (Exception e) {
            log.warn("Failed to load SRX rules: {}", e.getMessage());
            defaultSrx = null;
        }
    }

    // ═══════════════════════════════════════════════════════════════
    //  Inline code → HTML tag conversion
    // ═══════════════════════════════════════════════════════════════

    /**
     * Convert inline codes in a TextFragment to HTML-like tags.
     * Maps OOXML run properties (bold, italic, underline, etc.) to
     * simple HTML tags like {@code <b>}, {@code <i>}, {@code <u>}.
     *
     * @param fragment the TextFragment containing coded text
     * @return text with HTML formatting tags, or plain text if no
     *         recognisable formatting was found
     */
    private String convertCodesToTags(TextFragment fragment) {
        if (fragment == null) return "";

        List<Code> codes = fragment.getCodes();
        if (codes == null || codes.isEmpty()) {
            return fragment.toText();
        }

        String codedText = fragment.getCodedText();

        // Pre-analyse opening codes to determine formatting
        // Map: code ID → [openingTags, closingTags]
        Map<Integer, String[]> codeIdTags = new HashMap<>();

        for (Code code : codes) {
            if (code.getTagType() == TextFragment.TagType.OPENING) {
                // Try raw XML data first (works for filters that embed OOXML)
                String[] tags = analyzeFormatting(code.getData());
                // Fall back to Okapi's type descriptor (e.g. "x-bold;fonts:Arial;")
                if (tags[0].isEmpty()) {
                    tags = analyzeCodeType(code.getType());
                }
                if (!tags[0].isEmpty()) {
                    codeIdTags.put(code.getId(), tags);
                }
            }
        }

        if (codeIdTags.isEmpty()) {
            return fragment.toText(); // No recognisable formatting
        }

        // Build the tagged text
        StringBuilder result = new StringBuilder();
        ArrayDeque<String> openTagStack = new ArrayDeque<>();

        int i = 0;
        while (i < codedText.length()) {
            char ch = codedText.charAt(i);
            if (TextFragment.isMarker(ch) && i + 1 < codedText.length()) {
                int codeIndex = TextFragment.toIndex(codedText.charAt(i + 1));
                if (codeIndex >= 0 && codeIndex < codes.size()) {
                    Code code = codes.get(codeIndex);
                    String[] tags = codeIdTags.get(code.getId());
                    if (tags != null) {
                        if (code.getTagType() == TextFragment.TagType.OPENING) {
                            result.append(tags[0]);
                            openTagStack.push(tags[1]);
                        } else if (code.getTagType() == TextFragment.TagType.CLOSING) {
                            result.append(tags[1]);
                            if (!openTagStack.isEmpty()) openTagStack.pop();
                        }
                    }
                    // PLACEHOLDER codes (images, breaks, etc.) — skip
                }
                i += 2;
            } else {
                result.append(ch);
                i++;
            }
        }

        // Auto-close any unclosed tags (can happen at segment boundaries)
        while (!openTagStack.isEmpty()) {
            result.append(openTagStack.pop());
        }

        return result.toString().trim();
    }

    /**
     * Analyse an Okapi code's data (raw XML) to determine formatting.
     *
     * @param data the raw XML data from the Code
     * @return String[2]: [0] = opening HTML tags, [1] = closing HTML tags
     */
    private String[] analyzeFormatting(String data) {
        if (data == null || data.isEmpty()) return new String[]{"", ""};

        String d = data.toLowerCase();
        StringBuilder open = new StringBuilder();
        StringBuilder close = new StringBuilder();

        // OOXML run properties
        if (hasOoxmlFormat(d, "b"))  { open.append("<b>");   close.insert(0, "</b>");   }
        if (hasOoxmlFormat(d, "i"))  { open.append("<i>");   close.insert(0, "</i>");   }
        if (d.contains("<w:u ") && !d.contains("w:val=\"none\"")) {
            open.append("<u>"); close.insert(0, "</u>");
        }
        if (d.contains("\"superscript\"")) {
            open.append("<sup>"); close.insert(0, "</sup>");
        }
        if (d.contains("\"subscript\"")) {
            open.append("<sub>"); close.insert(0, "</sub>");
        }
        // Strikethrough
        if (hasOoxmlFormat(d, "strike")) {
            open.append("<s>"); close.insert(0, "</s>");
        }

        // HTML-based formats (for HTML filter)
        if (d.contains("<b>") || d.contains("<strong>")) {
            if (open.indexOf("<b>") < 0) { // avoid duplicates
                open.append("<b>"); close.insert(0, "</b>");
            }
        }
        if (d.contains("<i>") || d.contains("<em>")) {
            if (open.indexOf("<i>") < 0) {
                open.append("<i>"); close.insert(0, "</i>");
            }
        }

        return new String[]{open.toString(), close.toString()};
    }

    /**
     * Analyse an Okapi Code's type descriptor for formatting information.
     * The OpenXML filter sets type strings like "x-bold;fonts:Arial;" or
     * "x-bold;x-italic;color:FF0000;fonts:Calibri;".
     *
     * @param codeType the Code.getType() value
     * @return String[2]: [0] = opening tags, [1] = closing tags
     */
    private String[] analyzeCodeType(String codeType) {
        if (codeType == null || codeType.isEmpty()) return new String[]{"", ""};

        String t = codeType.toLowerCase();
        // Split on semicolons to get individual properties
        String[] parts = t.split(";");

        StringBuilder open = new StringBuilder();
        StringBuilder close = new StringBuilder();

        String fontName = null;
        String colorHex = null;

        for (String part : parts) {
            String p = part.trim();
            if (p.isEmpty()) continue;

            switch (p) {
                case "x-bold":
                    open.append("<b>"); close.insert(0, "</b>");
                    break;
                case "x-italic":
                    open.append("<i>"); close.insert(0, "</i>");
                    break;
                case "x-underlined":
                    open.append("<u>"); close.insert(0, "</u>");
                    break;
                case "x-strikethrough":
                    open.append("<s>"); close.insert(0, "</s>");
                    break;
                case "x-superscript":
                    open.append("<sup>"); close.insert(0, "</sup>");
                    break;
                case "x-subscript":
                    open.append("<sub>"); close.insert(0, "</sub>");
                    break;
                default:
                    if (p.startsWith("color:")) {
                        colorHex = p.substring(6).trim();
                    } else if (p.startsWith("fonts:")) {
                        fontName = p.substring(6).trim();
                    }
                    break;
            }
        }

        // Only wrap with <cf> when there is meaningful visual info like
        // color.  Font name alone is usually the paragraph default and just
        // adds noise.  When there IS a color, include the font for context.
        if (colorHex != null && !colorHex.isEmpty()) {
            StringBuilder cfOpen = new StringBuilder("<cf color=\"#");
            cfOpen.append(colorHex).append("\"");
            if (fontName != null && !fontName.isEmpty()) {
                cfOpen.append(" font=\"").append(fontName).append("\"");
            }
            cfOpen.append(">");
            open.insert(0, cfOpen);
            close.append("</cf>");
        }

        return new String[]{open.toString(), close.toString()};
    }

    // ═══════════════════════════════════════════════════════════════
    //  MERGE — reconstruct inline codes from display tags
    // ═══════════════════════════════════════════════════════════════

    /** Regex that matches our display tags: {@code <b>}, {@code </b>},
     *  {@code <cf color="#FF0000">}, {@code </cf>}, etc. */
    private static final Pattern TAG_RE = Pattern.compile(
            "<(/?)([a-z]+)(\\s[^>]*)?>", Pattern.CASE_INSENSITIVE);

    /**
     * Determine the primary HTML-like tag name for a source Code, based
     * on Okapi's type descriptor (e.g. "x-bold;fonts:Arial;" → "b").
     * Returns {@code null} if no recognisable formatting is found.
     */
    private String getTagNameForCode(Code code) {
        String type = code.getType();
        if (type == null) return null;
        String t = type.toLowerCase();
        if (t.contains("x-bold"))          return "b";
        if (t.contains("x-italic"))        return "i";
        if (t.contains("x-underlined"))    return "u";
        if (t.contains("x-strikethrough")) return "s";
        if (t.contains("x-superscript"))   return "sup";
        if (t.contains("x-subscript"))     return "sub";
        // Colour/font only (no primary formatting) → <cf>
        if (t.contains("color:"))          return "cf";
        return null;
    }

    /**
     * Build a target {@link TextFragment} from a translation string that
     * may contain HTML display tags ({@code <b>}, {@code <i>}, etc.),
     * mapping them back to the original Okapi inline codes from the source.
     *
     * <p>Positional matching is used: the first {@code <b>} in the
     * translation maps to the first bold code in the source, and so on.</p>
     *
     * @param taggedTranslation translation text with display tags
     * @param sourceContent     the source TextFragment (with inline codes)
     * @return a TextFragment with the translation text and proper codes
     */
    private TextFragment buildTargetFragment(String taggedTranslation,
                                             TextFragment sourceContent) {
        List<Code> srcCodes = (sourceContent != null) ? sourceContent.getCodes() : null;

        if (srcCodes == null || srcCodes.isEmpty()) {
            // No codes in source — strip any tags and return plain text
            return new TextFragment(TAG_RE.matcher(taggedTranslation).replaceAll(""));
        }

        // ── Step 1: classify source codes by tag name ──────────────
        // tag name → FIFO queue of code IDs
        Map<String, Queue<Integer>> tagQueues = new LinkedHashMap<>();
        Map<Integer, Code> openingById = new LinkedHashMap<>();
        Map<Integer, Code> closingById = new LinkedHashMap<>();

        for (Code c : srcCodes) {
            if (c.getTagType() == TextFragment.TagType.OPENING) {
                openingById.put(c.getId(), c);
                String tag = getTagNameForCode(c);
                if (tag != null) {
                    tagQueues.computeIfAbsent(tag, k -> new LinkedList<>()).add(c.getId());
                }
            } else if (c.getTagType() == TextFragment.TagType.CLOSING) {
                closingById.put(c.getId(), c);
            }
        }

        // ── Step 2: walk through the translation, replacing tags ───
        TextFragment result = new TextFragment();
        Deque<Integer> openStack = new ArrayDeque<>();   // stack of open code IDs
        Matcher m = TAG_RE.matcher(taggedTranslation);
        int lastEnd = 0;

        while (m.find()) {
            // Append plain text before this tag
            if (m.start() > lastEnd) {
                result.append(taggedTranslation.substring(lastEnd, m.start()));
            }

            boolean isClosing = "/".equals(m.group(1));
            String tagName = m.group(2).toLowerCase();

            if (!isClosing) {
                // ── OPENING tag ─────────────────────────────────
                Queue<Integer> queue = tagQueues.get(tagName);
                if (queue != null && !queue.isEmpty()) {
                    int codeId = queue.poll();
                    Code src = openingById.get(codeId);
                    if (src != null) {
                        Code c = new Code(TextFragment.TagType.OPENING,
                                          src.getType(), src.getData());
                        c.setId(codeId);
                        result.append(c);
                        openStack.push(codeId);
                    }
                }
                // else: tag not in source → silently drop it
            } else {
                // ── CLOSING tag ─────────────────────────────────
                // Find the most-recently-opened code that matches this
                // tag name. For properly nested tags this is the top.
                Integer matchedId = null;
                Iterator<Integer> it = openStack.iterator();
                while (it.hasNext()) {
                    int id = it.next();
                    Code src = openingById.get(id);
                    if (src != null) {
                        String srcTag = getTagNameForCode(src);
                        if (tagName.equals(srcTag)) {
                            matchedId = id;
                            it.remove();
                            break;
                        }
                    }
                }
                if (matchedId != null) {
                    Code src = closingById.get(matchedId);
                    if (src != null) {
                        Code c = new Code(TextFragment.TagType.CLOSING,
                                          src.getType(), src.getData());
                        c.setId(matchedId);
                        result.append(c);
                    }
                }
                // else: unmatched closing tag → silently drop it
            }

            lastEnd = m.end();
        }

        // Append any remaining text after the last tag
        if (lastEnd < taggedTranslation.length()) {
            result.append(taggedTranslation.substring(lastEnd));
        }

        return result;
    }

    /**
     * Check for an OOXML formatting element like {@code <w:b/>}.
     * Handles val="false"/val="0" negation and avoids matching
     * longer tag names (e.g. "b" must not match "bCs").
     */
    private boolean hasOoxmlFormat(String dataLower, String tag) {
        String[] patterns = {
                "<w:" + tag + "/>",   // self-closing
                "<w:" + tag + " ",    // with attributes
                "<w:" + tag + ">"     // opening
        };

        boolean found = false;
        for (String p : patterns) {
            if (dataLower.contains(p)) {
                found = true;
                break;
            }
        }
        if (!found) return false;

        // Check for explicit "false" values
        if (dataLower.contains("<w:" + tag + " w:val=\"false\"") ||
            dataLower.contains("<w:" + tag + " w:val=\"0\"")) {
            return false;
        }

        return true;
    }

    /**
     * Map a filename to an Okapi filter configuration ID.
     */
    private String getConfigIdForFile(String filename) {
        String lower = filename.toLowerCase();
        if (lower.endsWith(".docx"))  return "okf_openxml";
        if (lower.endsWith(".xlsx"))  return "okf_openxml";
        if (lower.endsWith(".pptx"))  return "okf_openxml";
        if (lower.endsWith(".html") || lower.endsWith(".htm"))
                                      return "okf_html";
        if (lower.endsWith(".xliff") || lower.endsWith(".xlf"))
                                      return "okf_xliff";
        if (lower.endsWith(".tmx"))   return "okf_tmx";
        if (lower.endsWith(".po"))    return "okf_po";
        if (lower.endsWith(".idml"))  return "okf_idml";

        throw new IllegalArgumentException(
                "Unsupported file format: " + filename +
                ". Supported: " + String.join(", ", SUPPORTED_FORMATS.keySet()));
    }

    private static String getSuffix(String filename) {
        int dot = filename.lastIndexOf('.');
        return dot > 0 ? filename.substring(dot) : "";
    }
}
