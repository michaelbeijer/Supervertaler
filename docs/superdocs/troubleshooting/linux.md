# Linux-Specific Issues

Supervertaler is Linux compatible, but Windows is the primary development platform.

## Spellcheck dictionaries

If spellcheck isn’t working, you may need to install Hunspell dictionaries for your language:

```bash
sudo apt install hunspell-en-us
```

If the dictionary package for your language exists, install it using the language code you need (for example `hunspell-de-de`, `hunspell-nl`, etc.).

## Stability tips

If you encounter instability:

- Disable spellcheck temporarily
- Disable semantic memory features temporarily
- Use a smaller project to isolate the issue

## Crashes / memory access violations

Some native dependencies (spellcheck backends, vector search, tokenization libraries) can crash the Python process on certain Linux setups.

If you see random crashes (segfaults) when interacting with the grid:

1. Disable spellcheck and restart
2. Disable Supermemory and restart
3. Retry on a smaller project

If that stabilizes the app, re-enable features one by one.
