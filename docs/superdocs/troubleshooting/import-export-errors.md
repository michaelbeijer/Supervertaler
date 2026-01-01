# Import/Export Errors

This page covers common problems when importing or exporting files.

## Segments don’t match on reimport

**Cause:** Segment structure changed.

**Fix:**

- Don’t merge or split segments in Supervertaler
- Export using the matching CAT format
- Avoid deleting placeholder/tag-only segments

## Formatting lost on reimport

**Cause:** Tags not preserved.

**Fix:**

- Verify tags are balanced (for example `<b>text</b>`)
- Don’t delete CAT placeholder tags
- Re-export using the correct CAT workflow
