# Performance Tips

Supervertaler is designed to stay responsive on large projects, but performance can vary with project size and enabled features.

## Tips

- Enable [Pagination](../editor/pagination.md) for very large projects
- Use a smaller **segments per page** setting (for example 50)
- Keep only the needed TMs and glossaries enabled
- If semantic search is enabled, allow indexing to complete

## Quick wins when it feels slow

1. Disable spellcheck temporarily (Settings → View Settings)
2. Disable Supermemory/semantic features if you don’t need them
3. Close other heavy apps (browsers with many tabs, IDE builds, etc.)
4. Restart Supervertaler and reopen the project

## Large projects

Very large files (thousands of segments) can stress any UI grid.

- Prefer pagination.
- Consider splitting source documents or using multi-file projects.

## If it feels slow

Try restarting the app and reopening the project.

If performance is still poor, note:

- Project size (segment count)
- Whether spellcheck is enabled
- Whether Supermemory is enabled
- Which CAT format you imported
