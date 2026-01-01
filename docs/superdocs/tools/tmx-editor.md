# TMX Editor

Supervertaler includes a built-in TMX editor for inspecting and editing TMX translation memories.

## Where to find it

- Go to the **Tools** tab → **✏️ TMX Editor**.

## What you can do

- Open, edit, and save TMX files.
- Search and filter by source/target text.
- Edit TMX header metadata.
- Run basic validation and view statistics.
- Perform bulk operations (for example: delete entries, copy source → target).

## Common workflows

### Clean up a TMX before importing

1. Open the TMX in **✏️ TMX Editor**.
2. Fix any obvious formatting issues (wrong language, empty segments, etc.).
3. Save the TMX.
4. Import it into your project via [Importing TMX files](../translation-memory/importing-tmx.md).

### Remove unwanted tags

If you’re trying to simplify a TMX that contains formatting or CAT-tool tags, you can remove them before importing.

{% hint style="info" %}
TMX is just XML — some tags are real inline markup (TMX/XLIFF-style), others are literal text like `&lt;b&gt;...&lt;/b&gt;`.
Cleaning tags can improve matching, but it can also remove important formatting. If you’re unsure, test on a copy first.
{% endhint %}

## Related

- [Importing TMX files](../translation-memory/importing-tmx.md)
- [Translation memory](../translation-memory/README.md)
