package com.supervertaler.sidecar;

import java.util.List;

/**
 * JSON response model for the /extract endpoint.
 */
public class ExtractResult {
    public String filename;
    public String sourceLang;
    public String targetLang;
    public String filterUsed;
    public int textUnitCount;
    public int segmentCount;
    public List<ExtractedSegment> segments;
}
