# Tag Validation

When working with formatted documents or CAT tool files, **tags must be preserved**.

## Why tags matter

Tags represent formatting or placeholders. If tags are missing or unbalanced, reimporting into your CAT tool can fail or formatting may be lost.

## Tag display modes

Supervertaler supports two ways of viewing formatting:

- **WYSIWYG mode**: shows *bold/italic/underline* as formatting
- **Tag view**: shows the raw markup (for example `<b>...</b>`)

Use **Tag view** when you are preparing to export/reimport and you want to verify the raw tags.

## Supported formatting tags

These tags are commonly used in Supervertaler projects:

| Tag | Meaning |
|-----|---------|
| `<b>...</b>` | Bold |
| `<i>...</i>` | Italic |
| `<u>...</u>` | Underline |
| `<bi>...</bi>` | Bold + Italic |
| `<sub>...</sub>` | Subscript |
| `<sup>...</sup>` | Superscript |

## CAT tool placeholder tags

CAT tools use placeholders/tags that must be preserved exactly:

| CAT tool | Examples |
|----------|----------|
| memoQ | `{1}`, `[2}...{2]`, `{MQ}`, `{tspan}` |
| Trados Studio | `<1>`, `</1>`, `<2/>` |
| Phrase (Memsource) | `{1}`, `{2}` |

## Tips

- Keep tags balanced (for example `<b>text</b>`, not `<b>text`).
- If you’re unsure, switch to Tag View and verify the raw tags.
- Don’t change tag numbers or names (for example `{1}` → `{2}`), even if the translation “looks fine”.
- If you insert a TM match, double-check that tags/placeholders still match the source.

{% hint style="warning" %}
For CAT tool workflows, don’t delete or edit placeholder tags unless you know exactly what they represent.
{% endhint %}
