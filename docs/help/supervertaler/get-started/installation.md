# Installation

## Windows (Recommended)

### Option 1: Download Release (Easiest)

1. Go to [GitHub Releases](https://github.com/michaelbeijer/Supervertaler/releases)
2. Download the latest `.zip` file
3. Extract to a folder of your choice
4. Run `Supervertaler.exe`

### Option 2: Run from Source

If you want the latest development version or want to contribute:

```bash
# Clone the repository
git clone https://github.com/michaelbeijer/Supervertaler.git
cd Supervertaler

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python Supervertaler.py
```

## Linux

Supervertaler is compatible with Linux, though Windows is the primary development platform.

```bash
# Clone the repository
git clone https://github.com/michaelbeijer/Supervertaler.git
cd Supervertaler

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Hunspell dictionaries (for spellcheck)
sudo apt install hunspell-en-us hunspell-nl  # Add your languages

# Run the application
python Supervertaler.py
```

{% hint style="info" %}
**Linux Users:** If you experience crashes related to spellcheck or ChromaDB, see [Linux-Specific Issues](../troubleshooting/linux.md).
{% endhint %}

## Dependencies

The main dependencies are automatically installed via `requirements.txt`:

| Package | Purpose |
|---------|---------|
| PyQt6 | User interface |
| openai | OpenAI GPT integration |
| anthropic | Anthropic Claude integration |
| google-generativeai | Google Gemini integration |
| python-docx | DOCX file handling |
| chromadb | Supermemory vector search |
| sentence-transformers | Semantic embeddings |
| pyspellchecker | Spellcheck |

## Next Steps

After installation:

1. [Set up your API keys](api-keys.md) for AI translation
2. Follow the [Quick Start Guide](quick-start.md)
3. Create your [first translation project](first-project.md)
