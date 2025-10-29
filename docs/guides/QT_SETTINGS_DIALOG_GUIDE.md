# Supervertaler Qt v1.0.0 - Settings Dialog Guide

## Accessing Settings

**Menu Path**: `Tools → Options`

## Settings Dialog Layout

```
┌─────────────────────────────────────────────────────────────┐
│ Settings                                                [X] │
├─────────────────────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────────────────┐   │
│ │ [🤖 LLM Settings] [⚙️ General]                       │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                             │
│ ╔═══════════════════════════════════════════════════════╗ │
│ ║ LLM Provider                                          ║ │
│ ║                                                       ║ │
│ ║ Select your preferred translation provider:          ║ │
│ ║                                                       ║ │
│ ║ ○ OpenAI (GPT-4o, GPT-5, o1, o3)                    ║ │
│ ║ ○ Anthropic Claude (Claude 3.5 Sonnet)              ║ │
│ ║ ○ Google Gemini (Gemini 2.0 Flash)                  ║ │
│ ╚═══════════════════════════════════════════════════════╝ │
│                                                             │
│ ╔═══════════════════════════════════════════════════════╗ │
│ ║ Model Selection                                       ║ │
│ ║                                                       ║ │
│ ║ Choose the specific model to use:                    ║ │
│ ║                                                       ║ │
│ ║ OpenAI Models:                                       ║ │
│ ║ ┌─────────────────────────────────────────────┐     ║ │
│ ║ │ gpt-4o (Recommended)                    ▼ │     ║ │
│ ║ └─────────────────────────────────────────────┘     ║ │
│ ║   • gpt-4o (Recommended)                           ║ │
│ ║   • gpt-4o-mini (Fast & Economical)                ║ │
│ ║   • gpt-5 (Reasoning, Temperature 1.0)             ║ │
│ ║   • o3-mini (Reasoning, Temperature 1.0)           ║ │
│ ║   • o1 (Reasoning, Temperature 1.0)                ║ │
│ ║   • gpt-4-turbo                                    ║ │
│ ║                                                       ║ │
│ ║ Claude Models:                                       ║ │
│ ║ ┌─────────────────────────────────────────────┐     ║ │
│ ║ │ claude-3-5-sonnet-20241022 (Recommended) ▼│     ║ │
│ ║ └─────────────────────────────────────────────┘     ║ │
│ ║   • claude-3-5-sonnet-20241022 (Recommended)       ║ │
│ ║   • claude-3-5-haiku-20241022 (Fast)               ║ │
│ ║   • claude-3-opus-20240229 (Powerful)              ║ │
│ ║                                                       ║ │
│ ║ Gemini Models:                                       ║ │
│ ║ ┌─────────────────────────────────────────────┐     ║ │
│ ║ │ gemini-2.0-flash-exp (Recommended)      ▼ │     ║ │
│ ║ └─────────────────────────────────────────────┘     ║ │
│ ║   • gemini-2.0-flash-exp (Recommended)             ║ │
│ ║   • gemini-1.5-pro                                 ║ │
│ ║   • gemini-1.5-flash                               ║ │
│ ╚═══════════════════════════════════════════════════════╝ │
│                                                             │
│ ╔═══════════════════════════════════════════════════════╗ │
│ ║ API Keys                                              ║ │
│ ║                                                       ║ │
│ ║ Configure your API keys in:                          ║ │
│ ║ user data_private/api_keys.txt                       ║ │
│ ║                                                       ║ │
│ ║ See example file for format:                         ║ │
│ ║ user data_private/api_keys.example.txt               ║ │
│ ║                                                       ║ │
│ ║ ┌───────────────────────────────────────────┐        ║ │
│ ║ │  📝 Open API Keys File                   │        ║ │
│ ║ └───────────────────────────────────────────┘        ║ │
│ ╚═══════════════════════════════════════════════════════╝ │
│                                                             │
│                                    ┌────┐  ┌────────┐     │
│                                    │ OK │  │ Cancel │     │
│                                    └────┘  └────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## General Tab Layout

```
┌─────────────────────────────────────────────────────────────┐
│ Settings                                                [X] │
├─────────────────────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────────────────┐   │
│ │ [🤖 LLM Settings] [⚙️ General]                       │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                             │
│ ╔═══════════════════════════════════════════════════════╗ │
│ ║ Find & Replace Settings                               ║ │
│ ║                                                       ║ │
│ ║ ☐ Allow Replace in Source Text                      ║ │
│ ║                                                       ║ │
│ ║ ┌─────────────────────────────────────────────────┐ ║ │
│ ║ │ ⚠️ Warning: Replacing in source text modifies  │ ║ │
│ ║ │ your original content. This feature is disabled│ ║ │
│ ║ │ by default for safety.                         │ ║ │
│ ║ └─────────────────────────────────────────────────┘ ║ │
│ ╚═══════════════════════════════════════════════════════╝ │
│                                                             │
│                                    ┌────┐  ┌────────┐     │
│                                    │ OK │  │ Cancel │     │
│                                    └────┘  └────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Usage Flow

### Step 1: Open Settings
1. Click `Tools` in menu bar
2. Click `Options`
3. Settings dialog appears

### Step 2: Select Provider
1. Stay on "🤖 LLM Settings" tab
2. Click radio button for your provider:
   - **OpenAI** - Best overall, GPT-5 available
   - **Claude** - Excellent for complex text
   - **Gemini** - Fast and economical

### Step 3: Choose Model
1. The corresponding dropdown becomes active
2. Select your preferred model
3. Notes:
   - **(Recommended)** = Best balance of quality/speed/cost
   - **(Fast)** = Optimized for speed
   - **(Reasoning, Temperature 1.0)** = For complex logic/analysis

### Step 4: Configure API Key
1. Click "📝 Open API Keys File"
2. File opens in your default text editor
3. Add your key in format: `provider=key`
   - Example: `openai=sk-proj-abc123...`
   - Example: `claude=sk-ant-xyz789...`
   - Example: `gemini=AIza123456...`
4. Save and close the file

### Step 5: Save Settings
1. Click "OK" button
2. Settings are saved automatically
3. Ready to translate!

## Translation Workflow

### With Settings Configured
1. **Select segment** in grid
2. **Press Ctrl+T** (or click 🤖 Translate button)
3. **Translation happens** using your chosen provider/model
4. **Status shows**: "✓ Segment #1 translated with openai/gpt-4o"

### First Translation (No Settings)
1. **Press Ctrl+T**
2. **Dialog appears**: "Would you like to configure API keys now?"
3. **Click Yes**
4. **Settings dialog opens** automatically
5. **Follow steps above** to configure
6. **Try again** - translation works!

## Dynamic UI Behavior

### Provider Selection Changes
When you click a different provider radio button:
- ✅ That provider's model dropdown **enables**
- ❌ Other providers' dropdowns **disable** (grayed out)
- ℹ️ Your previous selections are **remembered** for each provider

### Model Dropdown States

**OpenAI Selected:**
```
OpenAI Models:    [ENABLED]
Claude Models:    [DISABLED]
Gemini Models:    [DISABLED]
```

**Claude Selected:**
```
OpenAI Models:    [DISABLED]
Claude Models:    [ENABLED]
Gemini Models:    [DISABLED]
```

**Gemini Selected:**
```
OpenAI Models:    [DISABLED]
Claude Models:    [DISABLED]
Gemini Models:    [ENABLED]
```

## Settings Persistence

### Where Settings Are Stored
- **File**: `user data_private/ui_preferences.json`
- **Format**: JSON
- **Git**: Ignored (in private folder)

### Example Settings File
```json
{
  "llm_settings": {
    "provider": "openai",
    "openai_model": "gpt-4o",
    "claude_model": "claude-3-5-sonnet-20241022",
    "gemini_model": "gemini-2.0-flash-exp"
  }
}
```

### What Gets Saved
- ✅ **Current provider** (last selected radio button)
- ✅ **Model for each provider** (all dropdowns)
- ✅ **General settings** (replace in source, etc.)

### What Happens on Restart
1. App loads `ui_preferences.json`
2. Settings dialog shows your previous choices
3. Translation uses your saved provider/model
4. No need to reconfigure!

## Model Selection Guide

### OpenAI Models

| Model | Best For | Speed | Cost | Notes |
|-------|----------|-------|------|-------|
| **gpt-4o** | General translation | Fast | $$ | **Recommended** |
| gpt-4o-mini | Simple text | Very Fast | $ | Economical |
| **gpt-5** | Complex reasoning | Slow | $$$ | Temp=1.0 |
| o3-mini | Logic & analysis | Slow | $$ | Temp=1.0 |
| o1 | Deep reasoning | Very Slow | $$$$ | Temp=1.0 |
| gpt-4-turbo | Long documents | Medium | $$$ | Legacy |

### Claude Models

| Model | Best For | Speed | Cost | Notes |
|-------|----------|-------|------|-------|
| **claude-3-5-sonnet-20241022** | General translation | Fast | $$ | **Recommended** |
| claude-3-5-haiku-20241022 | Quick drafts | Very Fast | $ | Good quality |
| claude-3-opus-20240229 | Highest quality | Slow | $$$$ | Premium |

### Gemini Models

| Model | Best For | Speed | Cost | Notes |
|-------|----------|-------|------|-------|
| **gemini-2.0-flash-exp** | Fast translation | Very Fast | $ | **Recommended** |
| gemini-1.5-pro | Quality work | Medium | $$ | Balanced |
| gemini-1.5-flash | Bulk translation | Very Fast | $ | Economical |

### Temperature Settings (Automatic)

The system **automatically** sets temperature based on model:

- **Reasoning Models** (GPT-5, o1, o3): `temperature = 1.0`
  - These models need higher temperature for proper reasoning
  - Set automatically by `modules/llm_clients.py`
  
- **Standard Models** (GPT-4o, Claude, Gemini): `temperature = 0.3`
  - Lower temperature for consistent, focused translation
  - No user configuration needed

## Troubleshooting

### "API Key Missing" Error
**Solution**:
1. Click "Yes" when prompted to configure
2. Settings dialog opens
3. Click "📝 Open API Keys File"
4. Add your key in format: `provider=key`
5. Save file
6. Click OK in settings
7. Try translating again

### Model Dropdown Grayed Out
**Solution**:
- Click the **radio button** for that provider first
- The dropdown will automatically enable

### Settings Not Saving
**Check**:
- File permissions on `user data_private/` folder
- Disk space available
- Check console log for error messages

### Translation Uses Wrong Provider
**Solution**:
1. Open Settings (Tools → Options)
2. Verify the **radio button** shows your intended provider
3. Click OK to save again
4. Try translating

## Keyboard Shortcuts

- **Translate Segment**: `Ctrl+T`
- **Open Settings**: Click `Tools → Options` (no shortcut yet)
- **Save Settings**: `Enter` (when in dialog)
- **Cancel Settings**: `Esc` (when in dialog)

---

**Phase**: 2 - Provider & Model Selection  
**Status**: ✅ Complete  
**Version**: Qt v1.0.0
