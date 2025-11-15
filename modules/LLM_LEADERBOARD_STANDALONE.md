# LLM Leaderboard - Standalone Usage Guide

The LLM Leaderboard can be run independently outside of Supervertaler for benchmarking LLM translation quality.

## Quick Start

### 1. Install Dependencies

```bash
pip install PyQt6 openpyxl sacrebleu anthropic openai google-generativeai
```

### 2. Create API Keys File

Create a file named `api_keys.txt` in **one of these locations**:

**Option A** (Recommended): In the project root folder:
```
C:\Dev\Supervertaler\api_keys.txt
```

**Option B**: In the user_data_private folder (if using dev mode):
```
C:\Dev\Supervertaler\user_data_private\api_keys.txt
```

### 3. API Keys File Format

The `api_keys.txt` file should contain your API keys in this format:

```
# LLM API Keys for Translation Benchmarking
# Lines starting with # are comments and will be ignored

openai=sk-proj-YOUR_OPENAI_KEY_HERE
claude=sk-ant-YOUR_ANTHROPIC_KEY_HERE
google=YOUR_GOOGLE_GEMINI_KEY_HERE

# Optional keys (not needed for LLM Leaderboard)
deepl=
mymemory=
google_translate=
```

**Important Notes:**
- Replace `YOUR_OPENAI_KEY_HERE`, `YOUR_ANTHROPIC_KEY_HERE`, and `YOUR_GOOGLE_GEMINI_KEY_HERE` with your actual API keys
- For **Gemini**, use the key name `google` (not `gemini`)
- You can leave unused keys blank or comment them out
- Don't add spaces around the `=` sign
- Don't use quotes around the keys

### 4. Get API Keys

**OpenAI (GPT-4o, GPT-5):**
- Visit: https://platform.openai.com/api-keys
- Create a new API key
- Add it as: `openai=sk-proj-...`

**Anthropic (Claude):**
- Visit: https://console.anthropic.com/settings/keys
- Create a new API key
- Add it as: `claude=sk-ant-...`

**Google (Gemini):**
- Visit: https://aistudio.google.com/app/apikey
- Create a new API key
- Add it as: `google=AIza...`

### 5. Run the Leaderboard

**From within Supervertaler:**
```bash
python Supervertaler_Qt.py
```
Then navigate to: **Modules** → **🏆 LLM Leaderboard**

**Standalone UI (if implemented):**
```bash
python modules/llm_leaderboard_ui.py
```

## Usage

1. **Select Test Dataset**: Choose from pre-loaded datasets (Business, Technical, Legal)
2. **Select Models**: Check which models you want to test (OpenAI, Claude, Gemini)
3. **Choose Model Variants**: Use dropdowns to select specific models (e.g., GPT-5, Claude Opus 4.1, Gemini 2.5 Pro)
4. **Run Benchmark**: Click "Run Benchmark" and wait for results
5. **Export Results**: Click "Export Results" to save as Excel or JSON

## Understanding Results

### Quality Score (chrF++)
- **Range**: 0-100 (higher is better)
- **80-100**: Excellent quality
- **60-79**: Good quality
- **40-59**: Fair quality
- **Below 40**: Poor quality

### Speed (ms)
- **Under 2000ms**: Very fast
- **2000-5000ms**: Normal (typical)
- **Over 5000ms**: Slow

### Color Coding in Excel Export
- **Green**: Best performer in that category
- **Red**: Failed translation (error occurred)

## Test Datasets

The leaderboard includes 3 pre-loaded test datasets:

1. **Business EN→NL** (5 segments)
   - Formal business correspondence
   - Corporate communication

2. **Technical EN→NL** (5 segments)
   - User manuals
   - System requirements
   - Installation guides

3. **Legal NL→EN** (5 segments)
   - Contract clauses
   - Legal declarations
   - Governing law statements

## Troubleshooting

### "No API key configured for [provider]"
**Solution**: Check that your `api_keys.txt` file exists and contains the correct key names:
- OpenAI: `openai=...`
- Claude: `claude=...`
- Gemini: `google=...` (note: use `google`, not `gemini`)

### "sacrebleu not installed"
**Solution**: Install sacrebleu for quality scoring:
```bash
pip install sacrebleu
```

### Import Errors
**Solution**: Make sure you're in the project root directory when running:
```bash
cd C:\Dev\Supervertaler
python modules/llm_leaderboard_ui.py
```

### Model 404 Errors
**Solution**: Check that you're using current model IDs:
- ✅ `claude-sonnet-4-5-20250929` (correct)
- ❌ `claude-3-5-sonnet-20241022` (outdated)

## File Locations

```
C:\Dev\Supervertaler\
├── api_keys.txt                    # Your API keys (create this!)
├── modules/
│   ├── llm_leaderboard.py         # Core benchmarking engine
│   ├── superbench_ui.py           # Qt user interface
│   └── llm_clients.py             # LLM API client
└── user_data_private/             # Alternative location
    └── api_keys.txt               # API keys (dev mode)
```

## Security Notes

⚠️ **Important Security Reminders:**
- **Never commit** `api_keys.txt` to version control
- Keep your API keys private and secure
- Each API key should be kept secret
- Consider using environment variables for production deployments
- Monitor your API usage to detect unauthorized access

## Example api_keys.txt

```
# My API Keys for LLM Leaderboard
# Updated: 2025-01-09

openai=sk-proj-abcd1234567890EXAMPLE_KEY_DO_NOT_SHARE
claude=sk-ant-xyz9876543210EXAMPLE_KEY_DO_NOT_SHARE
google=AIzaSyEXAMPLE_KEY_12345_DO_NOT_SHARE

# Not needed for leaderboard
deepl=
mymemory=
```

## Advanced: Custom Test Datasets

You can create custom test datasets by editing `modules/llm_leaderboard.py` and adding to the `create_sample_datasets()` function. Each test segment needs:

- `id`: Unique segment number
- `source`: Source text to translate
- `reference`: High-quality reference translation (for quality scoring)
- `domain`: Domain category (e.g., "medical", "legal", "technical")
- `direction`: Language pair (e.g., "EN→NL", "NL→EN")
- `context`: Optional context information

## Support

For issues or questions:
- GitHub: https://github.com/mbeijer/supervertaler
- Website: https://supervertaler.com/
- Email: support@supervertaler.com

---

**LLM Leaderboard** is part of **Supervertaler**, a professional CAT tool.
Learn more at https://supervertaler.com/
