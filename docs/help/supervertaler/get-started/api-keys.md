# Setting Up API Keys

To use AI translation, you need API keys from one or more LLM providers.

## Supported Providers

| Provider | Models | Best For |
|----------|--------|----------|
| **OpenAI** | GPT-4o, GPT-4-turbo, GPT-3.5 | General translation, fast responses |
| **Anthropic** | Claude 3.5 Sonnet, Claude 3 Opus | Complex texts, nuanced writing |
| **Google** | Gemini Pro, Gemini Ultra | Multilingual content |
| **Ollama** | Llama, Mistral, etc. | Free, offline, privacy |

## Getting API Keys

### OpenAI

1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Navigate to **API Keys** in the sidebar
4. Click **Create new secret key**
5. Copy the key (it won't be shown again!)

{% hint style="warning" %}
OpenAI requires a paid account with credits. New accounts may get free trial credits.
{% endhint %}

### Anthropic

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Navigate to **API Keys**
4. Click **Create Key**
5. Copy the key

### Google (Gemini)

1. Go to [makersuite.google.com](https://makersuite.google.com)
2. Sign in with your Google account
3. Click **Get API key**
4. Create a key for a new or existing project
5. Copy the key

### Ollama (Free, Local)

Ollama runs models locally - no API key needed!

1. Download from [ollama.ai](https://ollama.ai)
2. Install and run Ollama
3. Download a model: `ollama pull llama2`
4. Supervertaler will detect it automatically

## Adding Keys to Supervertaler

### Method 1: Settings Dialog (Recommended)

1. Go to **Settings** tab
2. Find the **LLM Settings** section
3. Enter your API keys in the appropriate fields
4. Click **Save**

### Method 2: api_keys.txt File

Create or edit `api_keys.txt` in the Supervertaler folder:

```
openai_api_key=sk-your-key-here
anthropic_api_key=sk-ant-your-key-here
google_api_key=AIza-your-key-here
```

{% hint style="info" %}
**Security:** The `api_keys.txt` file is gitignored and never uploaded to GitHub.
{% endhint %}

## Testing Your Setup

1. Import a document or create a new project
2. Select a segment
3. Press `Ctrl+T` to translate
4. If successful, you'll see the translation appear

### Troubleshooting

| Problem | Solution |
|---------|----------|
| "Invalid API key" | Double-check the key, ensure no extra spaces |
| "Rate limit exceeded" | Wait a minute, or upgrade your API plan |
| "Model not found" | Check if the model name is correct in settings |
| No response | Check your internet connection |

## Choosing a Provider

**For beginners:** Start with OpenAI GPT-4o - it's fast, reliable, and has good translation quality.

**For cost-conscious users:** Use Ollama with a local model like Llama 3 - completely free!

**For sensitive content:** Use Ollama (data stays on your machine) or Anthropic Claude.

---

## Next Steps

- [Create your first translation project](first-project.md)
- [Learn about AI translation options](../ai-translation/overview.md)
- [Set up custom prompts](../ai-translation/prompts.md)
