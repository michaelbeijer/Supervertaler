package com.supervertaler.sidecar;

/**
 * A translated segment sent back during the /merge operation.
 */
public class MergeSegment {
    /** The Okapi text unit ID (from extraction). */
    public String id;

    /** Segment index within the text unit (0-based). */
    public int segmentIndex;

    /** The translated text. */
    public String translation;

    public MergeSegment() {}

    public MergeSegment(String id, int segmentIndex, String translation) {
        this.id = id;
        this.segmentIndex = segmentIndex;
        this.translation = translation;
    }
}
