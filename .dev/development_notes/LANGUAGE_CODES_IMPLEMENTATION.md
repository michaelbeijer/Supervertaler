# Language Codes and Variants - Implementation Summary

## ✅ What Was Fixed

### 1. **ISO Language Code Support**
- TMX now correctly uses **ISO 639-1** codes (e.g., `en`, `nl`, `de`, `fr`)
- Language names like "English" and "Dutch" are automatically converted to ISO codes
- Full support for language variants (e.g., `en-US`, `nl-BE`, `fr-CA`)

### 2. **Enhanced Language Conversion Function**

The `get_simple_lang_code()` function now handles:

**Language Names → ISO Codes:**
- "English" → `en`
- "Dutch" → `nl`
- "German" → `de`
- "French" → `fr`
- etc. (60+ languages supported)

**ISO Codes Preserved:**
- `en` → `en`
- `nl-NL` → `nl-NL`
- `en-US` → `en-US`

**Variants Properly Formatted:**
- `nl_BE` → `nl-BE`
- `EN-us` → `en-US`

### 3. **Language Variants in UI**

Expanded language list with regional variants:

```
English, en-US, en-GB, en-CA, en-AU
Dutch, nl-NL, nl-BE
German, de-DE, de-AT, de-CH
French, fr-FR, fr-CA, fr-BE, fr-CH
Spanish, es-ES, es-MX, es-AR
Portuguese, pt-PT, pt-BR
Italian, it-IT, it-CH
Chinese (Simplified), zh-CN
Chinese (Traditional), zh-TW, zh-HK
```

### 4. **Automatic TM Language Metadata**

Translation Memory now automatically stores correct ISO codes:

```python
# When you set languages in UI:
Source: "English"    → Stored as: "en"
Target: "Dutch"      → Stored as: "nl"

# With variants:
Source: "en-US"      → Stored as: "en-US"
Target: "nl-BE"      → Stored as: "nl-BE"
```

### 5. **TMX Export Improvements**

TMX files now have proper language codes:

**Before (incorrect):**
```xml
<tuv xml:lang="English">
  <seg>stabilization rib</seg>
</tuv>
<tuv xml:lang="Dutch">
  <seg>stabilisatierib</seg>
</tuv>
```

**After (correct):**
```xml
<tuv xml:lang="en">
  <seg>stabilization rib</seg>
</tuv>
<tuv xml:lang="nl">
  <seg>stabilisatierib</seg>
</tuv>
```

**With variants:**
```xml
<tuv xml:lang="en-US">
  <seg>stabilization rib</seg>
</tuv>
<tuv xml:lang="nl-BE">
  <seg>stabilisatierib</seg>
</tuv>
```

## 🎯 How to Use

### Setting Language Variants

1. **Menu: Project → Language Settings...**
2. Select language with variant from dropdown:
   - English → `en` (generic)
   - en-US → `en-US` (American English)
   - en-GB → `en-GB` (British English)
3. Click **Save**
4. TM metadata automatically updated with ISO codes

### Verifying Language Codes

1. **Open TM Manager**: Resources → Translation Memory...
2. **View Languages column**: Shows ISO code pairs
3. **Export TM**: File will have correct `xml:lang` attributes

### Example Workflow

```
1. Set languages:
   Source: en-US
   Target: nl-NL

2. Add term:
   "stabilization rib" → "stabilisatierib"

3. Export TM:
   Result: TMX with xml:lang="en-US" and xml:lang="nl-NL"

4. Import in other CAT tool:
   ✓ Correctly recognized as US English → Netherlands Dutch
```

## 📋 Supported Language Variants

### Dutch
- `nl` - Dutch (generic)
- `nl-NL` - Netherlands Dutch
- `nl-BE` - Belgian Dutch (Flemish)

### English
- `en` - English (generic)
- `en-US` - American English
- `en-GB` - British English
- `en-CA` - Canadian English
- `en-AU` - Australian English

### German
- `de` - German (generic)
- `de-DE` - German (Germany)
- `de-AT` - Austrian German
- `de-CH` - Swiss German

### French
- `fr` - French (generic)
- `fr-FR` - French (France)
- `fr-CA` - Canadian French
- `fr-BE` - Belgian French
- `fr-CH` - Swiss French

### Spanish
- `es` - Spanish (generic)
- `es-ES` - European Spanish
- `es-MX` - Mexican Spanish
- `es-AR` - Argentinian Spanish

### Portuguese
- `pt` - Portuguese (generic)
- `pt-PT` - European Portuguese
- `pt-BR` - Brazilian Portuguese

### Italian
- `it` - Italian (generic)
- `it-IT` - Italian (Italy)
- `it-CH` - Swiss Italian

### Chinese
- `zh-CN` - Simplified Chinese
- `zh-TW` - Traditional Chinese (Taiwan)
- `zh-HK` - Traditional Chinese (Hong Kong)

## 🔧 Technical Details

### Language Storage

**In Memory:**
- UI shows: "English" or "en-US"
- TM stores: `"en"` or `"en-US"`

**In TMX Files:**
- Always uses ISO codes
- Variants preserved exactly: `en-US`, `nl-BE`, etc.

### Conversion Logic

```python
# Language name
"English" → get_simple_lang_code() → "en"

# ISO code (preserved)
"nl-NL" → get_simple_lang_code() → "nl-NL"

# Invalid format (normalized)
"nl_be" → get_simple_lang_code() → "nl-BE"
"EN-us" → get_simple_lang_code() → "en-US"
```

### Backward Compatibility

- Existing TMs without language metadata get fallback values
- Generic language names still work: "English" automatically converts to "en"
- TMX files created with old version can still be imported

## ✨ Benefits

1. **CAT Tool Compatibility**: TMX files work correctly in memoQ, Trados, CafeTran, etc.
2. **Proper Variant Support**: Can distinguish US vs UK English, Belgian vs Netherlands Dutch
3. **Standards Compliant**: Follows ISO 639-1 and TMX 1.4 standards
4. **Future-Proof**: Ready for database implementation with proper language tagging

---

**Everything is now compliant with TMX standards and supports regional variants!** 🎉
