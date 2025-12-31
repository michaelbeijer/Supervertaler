# FAQ

Frequently asked questions about Supervertaler.

## General

### What is Supervertaler?

Supervertaler is a professional desktop translation application that integrates AI-powered translation with traditional CAT tool workflows. It's designed as a companion tool for translators.

### Is Supervertaler free?

Yes! Supervertaler is open source and free to use. You only pay for API calls if you use cloud-based LLMs (OpenAI, Anthropic, Google). Using Ollama for local models is completely free.

### What platforms does it support?

- **Windows 10/11** (primary platform)
- **Linux** (compatible, may require additional setup)
- macOS support is not officially tested

### What languages can I translate?

Supervertaler supports any language pair. The AI providers (GPT, Claude, Gemini) can translate between most world languages.

---

## AI Translation

### Which AI provider is best?

It depends on your needs:
- **GPT-4o** - Fast, reliable, good for most translations
- **Claude 3.5 Sonnet** - Excellent for nuanced, creative text
- **Gemini Pro** - Good value, strong multilingual support
- **Ollama** - Free, private, runs locally

### How much does AI translation cost?

Cloud providers charge per token:
- **GPT-4o**: ~$5-15 per million tokens
- **Claude**: ~$3-15 per million tokens
- **Gemini**: ~$0.50-1.50 per million tokens
- **Ollama**: **Free** (runs on your computer)

A typical document with 1,000 segments might cost $0.10-$1.00 depending on the provider and length.

### Can I use AI without an internet connection?

Yes! Use [Ollama](ai-translation/ollama.md) to run models locally on your computer.

---

## CAT Tool Integration

### Which CAT tools are supported?

- **memoQ** - Bilingual DOCX and XLIFF
- **Trados Studio** - SDLPPX/SDLRPX packages
- **Phrase (Memsource)** - Bilingual DOCX
- **CafeTran Espresso** - External View DOCX

### Will translations round-trip correctly?

Yes, when you follow the documented workflows. Supervertaler preserves:
- Segment structure
- Inline formatting tags
- Status information

### Can I use Supervertaler instead of my CAT tool?

Supervertaler is a **companion tool**, not a replacement. Use it for AI translation power, then return to your CAT tool for QA and delivery.

---

## Translation Memory

### Can I import my existing TMs?

Yes! Import TMX files from any CAT tool:
- **File → Import → TMX**
- Your TM entries become searchable

### What is Supermemory?

Supermemory is a semantic search feature that finds conceptually similar translations, even if the exact words don't match. It uses AI embeddings to understand meaning.

### How does fuzzy matching work?

Supervertaler compares source text to TM entries and shows:
- **100%** - Exact match
- **75-99%** - High fuzzy match (minor differences)
- **50-74%** - Medium fuzzy match
- **<50%** - Not shown by default

---

## Files & Projects

### What file formats are supported?

**Import:**
- DOCX (Word documents)
- TXT (plain text)
- TMX (Translation Memory)
- SDLPPX (Trados packages)
- memoQ bilingual DOCX/XLIFF
- Phrase bilingual DOCX
- CafeTran bilingual DOCX

**Export:**
- Translated DOCX
- Bilingual tables
- SDLRPX (Trados return)
- TMX

### Where are my projects saved?

Projects are saved as `.svproj` files wherever you choose. User data (TMs, glossaries, settings) is stored in the `user_data` folder.

### Can I work on the same project from multiple computers?

The `.svproj` file is portable. Copy it along with any referenced TMs/glossaries to work on another computer.

---

## Troubleshooting

### AI translation isn't working

1. Check your API key is entered correctly
2. Verify you have credits/balance with the provider
3. Test your internet connection
4. Check the Settings → LLM Settings for the correct model

### Spellcheck shows wrong language

1. Go to **Settings → View Settings**
2. Find Spellcheck Language dropdown
3. Select the correct target language

### Application crashes on startup

Try:
1. Delete `user_data/ui_preferences.json` (resets window state)
2. Run from source to see error messages
3. Check if required dependencies are installed

### Import fails with an error

- Ensure the file isn't open in another program
- Check the file isn't corrupted
- Try a different export format from your CAT tool

---

## Getting Help

### Where can I report bugs?

Open an issue on [GitHub Issues](https://github.com/michaelbeijer/Supervertaler/issues).

### Is there a user community?

Join the discussions on [GitHub Discussions](https://github.com/michaelbeijer/Supervertaler/discussions).

### How can I contribute?

Supervertaler is open source! See [Contributing](contributing.md) for how to help.
