# API Connection Problems

If AI translation isn’t working, this page helps you diagnose provider/API issues.

## Common causes

- Missing or invalid API key
- No internet connection
- Provider rate limits or quota limits
- Wrong model selected

## Quick checks

1. Verify your API key in [Setting Up API Keys](../get-started/api-keys.md)
2. Confirm you selected a **provider** and **model** in Settings (LLM/AI settings)
3. Try translating a single short segment (`Ctrl+T`)
4. Check whether your account has credits/quota

## Common errors and fixes

| Symptom / message | Likely cause | What to do |
|---|---|---|
| “Invalid API key” / authentication failed | Key is wrong or has extra whitespace | Re-paste the key; make sure there are no leading/trailing spaces; Save and restart if needed |
| “Rate limit exceeded” | Provider is throttling requests | Wait 1–2 minutes; reduce batch size; try a different model |
| “Quota/credits exceeded” | Account has no credits or billing disabled | Check provider dashboard; add credits/enable billing |
| “Model not found” | Selected model name not available | Pick a supported model in Settings; update if the provider changed model names |
| “No response” / empty translation | Transient provider failure, network issue, or timeout | Try single-segment translation; retry the segment; try a different model/provider |
| Connection errors / timeouts | Network/VPN/firewall/proxy issues | Try another network; disable VPN; allow Python/Supervertaler through firewall |

## Tips for reliable translation

- Start with **single-segment** translation to verify your setup before running batch.
- If batch translation returns empty segments, enable the retry option in the batch dialog.
- If your segments contain tags/placeholders, add a prompt rule to preserve them exactly.

## Error messages

If you see an error dialog, copy the message and include it when asking for help.

Include:

- Provider + model
- Whether single-segment translation works
- The exact error text
