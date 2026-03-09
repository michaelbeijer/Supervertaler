# AI Settings

{% hint style="info" %}
This page is about **Supervertaler for Trados** — the Trados Studio plugin.
{% endhint %}

Configure the AI provider, model, and context options used by the Supervertaler for Trados plugin.

## Accessing AI settings

Open the plugin **Settings** dialog and switch to the **AI** tab.

## Provider selection

Choose one of the supported AI providers:

| Provider | Description |
|----------|-------------|
| **OpenAI** | GPT models (GPT-4o, GPT-4, etc.) |
| **Anthropic** | Claude models |
| **Google** | Gemini models |
| **Ollama** | Run models locally, no API key required |
| **Custom OpenAI-compatible** | Any provider with an OpenAI-compatible API |

{% hint style="info" %}
You only need one provider to get started. See [Setting Up API Keys](../../get-started/api-keys.md) for instructions on obtaining a key.
{% endhint %}

## API key

Enter the API key for your selected provider. The key is stored locally and never sent anywhere except to the provider's API endpoint.

## Model selection

A dropdown showing available models for the selected provider. The list is fetched automatically when a valid API key is entered.

## Ollama endpoint

When using Ollama as the provider, this field sets the local endpoint URL. Defaults to:

```
http://localhost:11434
```

Change this only if you are running Ollama on a different port or a remote machine.

## Custom OpenAI-compatible provider

For providers that expose an OpenAI-compatible API (e.g., Azure OpenAI, together.ai, local inference servers), configure these fields:

| Field | Description |
|-------|-------------|
| **Display name** | A label for this provider (shown in the provider dropdown) |
| **Endpoint URL** | The base URL for the API (e.g., `https://your-server.com/v1`) |
| **API key** | The authentication key for this endpoint |
| **Model name** | The model identifier to use (e.g., `llama-3-70b`) |

## AI context options

These options control what additional context is included when the AI translates a segment.

### Include termbases in AI prompt

When enabled, all terminology matches from active termbases for the current segment are injected into the translation prompt. This helps the AI use the correct, approved terminology.

### Include TM matches

When enabled, translation memory matches for the current segment are included in the prompt. This gives the AI context from previous translations, improving consistency.

{% hint style="success" %}
**Tip:** Enabling both options gives the AI the most context for accurate, consistent translations. Disable them if you want the AI to translate without any reference material.
{% endhint %}

## Batch settings

Configure the **batch size** for the [Batch Translate](../../ai-translation/batch-translation.md) feature. This determines how many segments are sent to the AI provider in a single request.

- A larger batch size is faster but uses more tokens per request
- A smaller batch size is more granular and easier to review

---

## See Also

- [Prompts](prompts.md)
- [TermLens Settings](termlens.md)
- [Supported LLM Providers (standalone)](../../ai-translation/providers.md)
