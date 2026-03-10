# Spellcheck

Supervertaler includes a powerful spellcheck system that highlights misspellings while you translate, with support for regional language variants.

## How It Works

Supervertaler uses a **three-tier spellcheck system** that automatically selects the best available backend:

| Backend | Description | Languages |
|---------|-------------|-----------|
| **Hunspell (cyhunspell)** | Native C library, best accuracy | Any language with .dic/.aff files |
| **Spylls** | Pure Python Hunspell (recommended for Windows) | Bundled: EN, RU, SV + any .dic/.aff files you add |
| **pyspellchecker** | Built-in fallback | EN, NL, DE, FR, ES, PT, IT, RU |

The system automatically falls back through backends: Hunspell → Spylls → pyspellchecker.

{% hint style="info" %}
**Windows Users:** Spylls is automatically used since cyhunspell doesn't compile on Python 3.12+. This works great and supports regional variants!
{% endhint %}

## Features

- **Red wavy underlines** for misspelled words in the translation grid
- **Right-click context menu** with spelling suggestions
- **Add to Dictionary** — Save a word permanently
- **Ignore** — Skip a word for the current session only
- **Regional variants** — Distinguish between en_US "color" and en_GB "colour"

## Language Variants

Supervertaler supports regional language variants. The spellcheck dropdown shows variants like:

- English (US), English (GB), English (AU), English (CA), English (ZA)
- Portuguese (PT), Portuguese (BR)
- Spanish (ES), Spanish (MX), Spanish (AR)
- French (FR), French (CA), French (BE)
- German (DE), German (AT), German (CH)
- Dutch (NL), Dutch (BE)

{% hint style="success" %}
**Regional spelling works correctly!**
- With **English (GB)**: "colour" ✅ correct, "color" ❌ incorrect
- With **English (US)**: "colour" ❌ incorrect, "color" ✅ correct
{% endhint %}

## Spellcheck Info Dialog

Access detailed information about your spellcheck setup:

1. Click the **🔤 Spellcheck** button in the grid toolbar
2. Or go to **View → Spellcheck Info**

The dialog shows:
- Current language and backend
- Available languages
- Diagnostic information (which backends are available/initialized)
- Links to download additional dictionaries
- Custom dictionary word count

## Adding More Dictionaries

To add spellcheck support for additional languages or variants:

1. **Download Hunspell dictionaries** (.dic and .aff files) from:
   - [hunspell.memoq.com](https://hunspell.memoq.com/) — 70+ languages
   - [GitHub: wooorm/dictionaries](https://github.com/wooorm/dictionaries/tree/main/dictionaries) — 92+ languages
   - [LibreOffice Extensions](https://extensions.libreoffice.org/?Tags%5B%5D=50) — Rename .oxt to .zip

2. **Extract the files** — You need both `.dic` and `.aff` files (e.g., `nl_NL.dic` and `nl_NL.aff`)

3. **Place them in the dictionaries folder:**
   - Open Supervertaler
   - Go to Spellcheck Info dialog
   - Click "📁 Open Dictionaries Folder"
   - Copy your .dic and .aff files there
   - You can also organize in subfolders (e.g., `dictionaries/en/en_GB.dic`)

4. **Restart Supervertaler** — The new language will appear in the dropdown

{% hint style="info" %}
**Spylls bundled dictionaries** (EN, RU, SV) are stored inside the spylls pip package, not in your dictionaries folder. Add your own .dic/.aff files to the dictionaries folder to extend available languages.
{% endhint %}

## Custom Dictionary

You can add words that Supervertaler should always accept:

- **Right-click a "misspelled" word** → **Add to Dictionary**
- Or manually edit `user_data/dictionaries/custom_words.txt`

Custom words are stored permanently and apply to all languages.

## Troubleshooting

### Spellcheck not working?

1. **Check the language** — Make sure the correct language variant is selected
2. **Check the backend** — Open Spellcheck Info to see which backend is active
3. **Missing dictionaries** — Some languages require manual dictionary installation

### Wrong language variant?

If you need British English but only have US English:
1. Download `en_GB.dic` and `en_GB.aff` from one of the dictionary sources
2. Place them in your dictionaries folder
3. Select "English (GB)" from the dropdown

### Linux crashes?

On Linux, some Hunspell configurations can cause crashes. Try:
- Installing proper Hunspell dictionaries: `sudo apt install hunspell-<lang>` (e.g., `hunspell-pl` for Polish)
- Temporarily disabling spellcheck in Settings → View Settings
- See [Linux-Specific Issues](../troubleshooting/linux.md) for more details

## Technical Details

For developers and advanced users:

| Project | Description |
|---------|-------------|
| [pyspellchecker](https://github.com/barrust/pyspellchecker) | Built-in word frequency spellcheck |
| [spylls](https://github.com/zverok/spylls) | Pure Python Hunspell implementation |
| [Hunspell](http://hunspell.github.io/) | Original C/C++ spellcheck library |

The spellcheck manager is located in `modules/spellcheck_manager.py` and provides:
- Automatic backend selection
- Dictionary file detection (including subdirectories)
- Word caching for performance
- Custom dictionary management
