# 🏷️ INLINE TAGS - QUICK REFERENCE CARD

## Tag Types
```
<b>text</b>   = Bold
<i>text</i>   = Italic  
<u>text</u>   = Underline
<bi>text</bi> = Bold + Italic
```

## Validation Status
```
✓ Tags: 1 b, 2 i    = Valid (1 bold, 2 italic)
⚠️ Unclosed tags: b  = Error: Missing </b>
⚠️ Mismatched tags   = Error: Wrong closing tag
```

## Button Actions
```
[<b>Bold</b>]           = Wrap selection in <b> tags
[<i>Italic</i>]         = Wrap selection in <i> tags  
[<u>Underline</u>]      = Wrap selection in <u> tags
[Strip Tags]            = Remove all tags
[Copy Source Tags]      = Copy source formatting
```

## Workflow
```
1. Import DOCX          → Tags extracted automatically
2. Select segment       → Source shows: "The <b>API</b> is..."
3. Translate            → Target: "La <b>API</b> es..."
4. Insert tags          → Select word → Click button
5. Validate             → Look for green ✓
6. Export DOCX          → Formatting restored
```

## Keyboard Tips
```
Select text             = Shift + Arrow keys
Insert tag              = Click button (or use mouse)
Next segment            = Ctrl + Enter
Undo                    = Ctrl + Z
```

## Examples

### Simple Bold
```
Source: The <b>API key</b> is required.
Target: La <b>clé API</b> est requise.
```

### Multiple Formats
```
Source: See <i>Section 3</i> for <b>details</b>.
Target: Ver <i>Sección 3</i> para <b>detalles</b>.
```

### Bold + Italic
```
Source: This is <bi>very important</bi>.
Target: Ceci est <bi>très important</bi>.
```

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Tags not showing | Check validation (green ✓) |
| "Unclosed tags" | Count: `<b>` must match `</b>` |
| Wrong formatting | Verify tag names: `<b>` not `<bold>` |
| Tags in export | Shouldn't happen - check console |

## ✅ DO
- Match source tags in target
- Use buttons (not manual typing)
- Check for green ✓ before saving
- Keep tags together

## ❌ DON'T  
- Forget closing tags
- Nest incorrectly: `<b><i>text</b></i>`
- Use unsupported tags: `<bold>`
- Split tags across segments

---

**Print this card for quick reference while translating!**
