package com.supervertaler.sidecar;

import java.util.List;

/**
 * JSON response model for the /tmx/validate endpoint.
 */
public class TmxValidationResult {
    public String filename;
    public boolean valid;
    public int tuCount;
    public List<String> languages;
    public int emptySourceCount;
    public int emptyTargetCount;
    public List<TmxIssue> issues;
}
