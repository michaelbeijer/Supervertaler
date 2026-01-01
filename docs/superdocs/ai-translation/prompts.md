# Creating Prompts

Prompts control how the AI translates (tone, domain, rules, formatting).

## What makes a good translation prompt

- Target audience and tone (formal/informal)
- Domain constraints (legal, medical, technical)
- Rules for numbers, punctuation, terminology
- Instructions to preserve tags and placeholders

{% hint style="warning" %}
If your text contains formatting or CAT tool tags, instruct the model to preserve them exactly.
{% endhint %}

## Quick checklist

- Specify the language direction (source → target)
- Specify style and audience (formal/informal, US/UK spelling, etc.)
- Tell the model what to do with **tags/placeholders** (keep, don’t reorder, don’t delete)
- Tell the model what to do with terminology (use glossary terms when provided)

## Next

- [Prompt Library](prompt-library.md)
