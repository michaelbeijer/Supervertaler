# Prompts

{% hint style="info" %}
This page is about **Supervertaler for Trados** — the Trados Studio plugin. For prompts in Supervertaler Workbench, see [Creating Prompts (Workbench)](../../ai-translation/prompts.md).
{% endhint %}

Prompts control how the AI translates your content. The Prompt Manager lets you browse built-in domain prompts and create your own custom prompts.

## Accessing the Prompt Manager

Open the plugin **Settings** dialog and switch to the **Prompts** tab.

## Built-in domain prompts

The plugin ships with 14 domain-specific prompts, ready to use out of the box:

| Category | Prompts |
|----------|---------|
| **Domain** | Medical, Legal, Patent, Financial, Technical, Marketing, IT |
| **Style guides** | Dutch Style Guide, English Style Guide, French Style Guide, German Style Guide, Spanish Style Guide |
| **General** | General Translation, Creative / Transcreation |

Each prompt is tuned for its domain, including instructions for tone, terminology handling, and formatting conventions.

{% hint style="info" %}
Built-in prompts are **read-only**. If you want to customise one, create a new prompt and copy the content as a starting point.
{% endhint %}

## Creating custom prompts

1. Click **New**
2. Fill in the fields:

| Field | Description |
|-------|-------------|
| **Name** | A short label for this prompt (shown in the selection list) |
| **Description** | Optional summary of what this prompt is for |
| **Category** | Group the prompt under a category for easier browsing |
| **Content** | The full prompt text sent to the AI model |

3. Click **Save**

## Prompt variables

You can use the following variables in your prompt content. They are replaced automatically at translation time:

| Variable | Replaced with |
|----------|---------------|
| `{{SOURCE_LANGUAGE}}` | The source language of the current project |
| `{{TARGET_LANGUAGE}}` | The target language of the current project |

**Example prompt content:**

```
You are a professional medical translator. Translate the following text
from {{SOURCE_LANGUAGE}} to {{TARGET_LANGUAGE}}. Use formal, clinical
language. Preserve all formatting tags exactly as they appear.
```

## Editing prompts

1. Select a prompt in the list
2. Click **Edit**
3. Modify the fields as needed
4. Click **Save**

{% hint style="warning" %}
Built-in prompts cannot be edited. To modify a built-in prompt, create a new custom prompt based on it.
{% endhint %}

## Deleting custom prompts

1. Select a custom prompt in the list
2. Click **Delete**
3. Confirm the deletion

Built-in prompts cannot be deleted.

## Using prompts for Batch Translate

The currently selected prompt is used when running **Batch Translate**. Before starting a batch, make sure you have the correct prompt selected for the domain and style you need.

---

## See Also

- [AI Settings](ai-settings.md)
- [Batch Translation (standalone)](../../ai-translation/batch-translation.md)
- [Creating Prompts (standalone)](../../ai-translation/prompts.md)
