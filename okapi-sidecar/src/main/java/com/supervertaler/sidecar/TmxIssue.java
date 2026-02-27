package com.supervertaler.sidecar;

/**
 * A single issue found during TMX validation.
 */
public class TmxIssue {
    /** "error", "warning", or "info" */
    public String level;
    public String message;
    public int tuIndex;

    public TmxIssue() {}

    public TmxIssue(String level, String message, int tuIndex) {
        this.level = level;
        this.message = message;
        this.tuIndex = tuIndex;
    }
}
