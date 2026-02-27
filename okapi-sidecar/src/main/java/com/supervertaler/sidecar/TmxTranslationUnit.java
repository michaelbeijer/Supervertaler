package com.supervertaler.sidecar;

import java.util.Map;

/**
 * A single TU from a TMX file.
 */
public class TmxTranslationUnit {
    public String id;
    public String source;

    /** Language code → translated text */
    public Map<String, String> targets;

    /** TMX properties/metadata (changedate, creationid, etc.) */
    public Map<String, String> properties;
}
