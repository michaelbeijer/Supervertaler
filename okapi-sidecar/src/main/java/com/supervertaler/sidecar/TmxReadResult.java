package com.supervertaler.sidecar;

import java.util.List;

/**
 * JSON response model for the /tmx/read endpoint.
 */
public class TmxReadResult {
    public String filename;
    public int tuCount;
    public List<TmxTranslationUnit> translationUnits;
}
