package com.supervertaler.sidecar;

/**
 * A single extracted segment from a document.
 */
public class ExtractedSegment {
    /** The Okapi text unit ID — used to map translations back during merge. */
    public String id;

    /** Segment index within the text unit (0-based). */
    public int segmentIndex;

    /** The source text (plain text, with inline codes removed). */
    public String source;

    /**
     * The source text with formatting preserved as HTML-like tags.
     * E.g., "<b>bold</b> and <i>italic</i>".
     * Null/empty if no formatting codes were found.
     */
    public String sourceWithTags;

    /** The text unit type (e.g., "paragraph", "header"). */
    public String type;

    /** Whether this text unit is a referent (referenced by another element). */
    public boolean isReferent;

    /** The Okapi text unit name (may contain style/context info). */
    public String name;

    /**
     * The sub-document this segment came from.
     * "body" for main document body, or e.g. "header1.xml", "footer1.xml"
     * for headers/footers.
     */
    public String subDocument;

    public ExtractedSegment() {}

    public ExtractedSegment(String id, int segmentIndex, String source,
                            String sourceWithTags, String type,
                            boolean isReferent, String name,
                            String subDocument) {
        this.id = id;
        this.segmentIndex = segmentIndex;
        this.source = source;
        this.sourceWithTags = sourceWithTags;
        this.type = type;
        this.isReferent = isReferent;
        this.name = name;
        this.subDocument = subDocument;
    }
}
