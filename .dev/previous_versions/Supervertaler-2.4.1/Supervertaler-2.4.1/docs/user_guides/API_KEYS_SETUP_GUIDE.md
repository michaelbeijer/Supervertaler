# API Keys Setup Guide - Supervertaler v2.5.0

## 🔒 Security First

**CRITICAL**: Your API keys are like passwords - they give access to your paid AI services. Supervertaler is designed to keep your keys 100% secure and local to your computer.

### What's Protected

✅ **api_keys.txt** - Your actual API keys (NEVER uploaded to GitHub)  
✅ **custom_prompts_private/** - Your private custom prompts  
✅ **projects_private/** - Your private translation projects  

These are all listed in `.gitignore` and will never be synced to version control.

### What's Shared

✅ **api_keys.example.txt** - Template file with instructions (safe to share)  
✅ **custom_prompts/** - Public example prompts  
✅ **projects/** - Public example projects  

---

## 📋 Quick Setup (3 Steps)

### Step 1: Copy the Example File

**Windows**:
```powershell
Copy-Item "api_keys.example.txt" -Destination "api_keys.txt"
```

**macOS/Linux**:
```bash
cp api_keys.example.txt api_keys.txt
```

**Manual**: Right-click `api_keys.example.txt` → Copy → Paste → Rename to `api_keys.txt`

### Step 2: Get Your API Keys

You only need keys for the AI providers you want to use. You don't need all three.

#### OpenAI (GPT-4, GPT-4o)
1. Go to: https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Name it (e.g., "Supervertaler")
5. Copy the key (starts with `sk-proj-` or `sk-`)
6. **Save it immediately** - you can't see it again!

**Pricing**: Pay-per-use, ~$0.01-0.15 per 1000 words depending on model

#### Anthropic Claude (Claude 3.5 Sonnet, Claude 3 Opus)
1. Go to: https://console.anthropic.com/settings/keys
2. Sign in or create account
3. Click "Create Key"
4. Name it (e.g., "Supervertaler")
5. Copy the key (starts with `sk-ant-`)
6. **Save it immediately** - you can't see it again!

**Pricing**: Pay-per-use, ~$0.015-0.075 per 1000 words depending on model

#### Google Gemini (Gemini 2.5 Pro, Gemini 1.5 Flash)
1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API key"
4. Select or create a Google Cloud project
5. Copy the key (starts with `AIzaSy`)
6. **Save it immediately**

**Pricing**: Free tier available (60 requests/minute), then pay-per-use

### Step 3: Edit api_keys.txt

Open `api_keys.txt` in a text editor (Notepad, VS Code, etc.) and:

1. **Remove the `#` symbol** from the lines you want to use
2. **Replace the placeholder** with your actual key
3. **Save the file**

**Before**:
```
#openai = YOUR_OPENAI_KEY_HERE
#claude = YOUR_CLAUDE_KEY_HERE
#google = YOUR_GOOGLE_KEY_HERE
```

**After** (example with OpenAI key):
```
openai = sk-proj-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
#claude = YOUR_CLAUDE_KEY_HERE
#google = YOUR_GOOGLE_KEY_HERE
```

**Important**: 
- No spaces around the `=` sign (or one space on each side is fine)
- No quotes around the key
- One key per line
- Lines starting with `#` are ignored (comments)

---

## ✅ Verify It Worked

### Method 1: Check Settings Tab
1. Launch Supervertaler
2. Click the **⚙️ Settings** tab in Translation Workspace
3. Look at "LLM Provider" section
4. You should see your configured provider and model

### Method 2: Check API Settings Dialog
1. Click **Translate** menu → **API Settings**
2. Look for green checkmarks ✓:
   - ✓ OpenAI (✓ Installed) - if openai library is installed
   - ✓ Claude (✓ Installed) - if anthropic library is installed
   - ✓ Gemini (✓ Installed) - if google-generativeai is installed
3. Your API key should show as `***` (masked for security)

### Method 3: Try a Translation
1. Import a DOCX file
2. Select a segment
3. Press **Ctrl+T** to translate
4. If it works, your API key is correctly configured! 🎉

---

## 🚨 Troubleshooting

### "API Key Missing" Error

**Possible causes**:
1. ❌ File is still named `api_keys.example.txt` instead of `api_keys.txt`
2. ❌ The `#` symbol is still at the beginning of the line
3. ❌ Extra spaces or characters in the key
4. ❌ Key is in quotes (remove them)
5. ❌ File is in the wrong folder

**Solution**:
```
# Wrong:
#openai = sk-proj-...         ← Still has #
openai = "sk-proj-..."        ← Has quotes
openai= sk-proj-...           ← Missing space (still works but inconsistent)

# Correct:
openai = sk-proj-...          ← Perfect!
```

### "Library Missing" Error

**Error**: `OpenAI library not installed. Run: pip install openai`

**Solution**:
```powershell
# Install required libraries
pip install openai
pip install anthropic
pip install google-generativeai
```

Or install all at once:
```powershell
pip install openai anthropic google-generativeai
```

### "Invalid API Key" Error

**Possible causes**:
1. ❌ Key was copied incorrectly (missing characters)
2. ❌ Key has expired or been revoked
3. ❌ Billing not set up for your provider account
4. ❌ Wrong key type (e.g., using a different service's key)

**Solution**:
1. Go back to the provider's website
2. Generate a new API key
3. Copy it carefully (no extra spaces or line breaks)
4. Replace in `api_keys.txt`
5. Save and restart Supervertaler

### Keys Not Loading

**Check these**:
1. ✓ File location: Same folder as `Supervertaler_v2.5.0.py`
2. ✓ File name: Exactly `api_keys.txt` (case-sensitive on some systems)
3. ✓ File format: Plain text (not .docx or .rtf)
4. ✓ Encoding: UTF-8 (default for most text editors)

**Test manually**:
1. Open `Supervertaler_v2.5.0.py` location in File Explorer
2. Check if `api_keys.txt` exists
3. Open it and verify your keys are there without `#`
4. Close Supervertaler completely
5. Restart it

---

## 🔐 Security Best Practices

### DO ✅

- ✅ Keep `api_keys.txt` in your local Supervertaler folder only
- ✅ Use different API keys for different projects/applications
- ✅ Set up billing alerts at your AI provider (to avoid surprise charges)
- ✅ Revoke and regenerate keys if you suspect they've been compromised
- ✅ Regularly check `.gitignore` to ensure `api_keys.txt` is listed

### DON'T ❌

- ❌ Email your `api_keys.txt` file to anyone
- ❌ Upload `api_keys.txt` to cloud storage (Dropbox, Google Drive, OneDrive)
- ❌ Commit `api_keys.txt` to Git (it's in `.gitignore` - don't remove it!)
- ❌ Share screenshots showing your full API keys
- ❌ Store keys in your code files or project JSON files
- ❌ Use the same key across multiple users (each person should have their own)

### If You Accidentally Expose a Key

**IMMEDIATELY**:
1. Go to your AI provider's website
2. Revoke/delete the exposed key
3. Generate a new key
4. Update your `api_keys.txt`
5. Monitor your usage for any unauthorized activity

---

## 💰 Cost Management

### Understanding Costs

AI translation is **pay-per-use**. Costs depend on:
- **Model**: GPT-4o-mini is cheaper than GPT-4o
- **Input length**: Longer source text = higher cost
- **Context**: Including surrounding segments increases tokens
- **Frequency**: More translations = more cost

### Typical Costs (approximate)

**For a 10,000-word document**:
- GPT-4o-mini: ~$0.50 - $1.00
- GPT-4o: ~$5.00 - $10.00
- Claude 3.5 Haiku: ~$0.50 - $1.50
- Claude 3.5 Sonnet: ~$3.00 - $6.00
- Gemini 1.5 Flash: ~$0.15 - $0.50 (or free tier)
- Gemini 2.5 Pro: ~$2.00 - $5.00

### Saving Money with TM

**Translation Memory reduces costs**:
- Exact matches (100%): FREE (no API call)
- Fuzzy matches (75%+): Show preview, you decide whether to use AI

**Example**: 1000-segment project with 30% exact TM matches
- Without TM: 1000 API calls = ~$5.00
- With TM: 700 API calls = ~$3.50
- **Savings**: $1.50 (30%)

Plus, TM gets better over time - future projects cost even less!

### Set Up Billing Alerts

**OpenAI**:
1. Go to https://platform.openai.com/settings/organization/billing/limits
2. Set "Soft limit" (warning) and "Hard limit" (stop)
3. Example: Soft limit $10, Hard limit $20

**Anthropic**:
1. Go to https://console.anthropic.com/settings/billing
2. Monitor "Current usage"
3. Set up email notifications

**Google**:
1. Go to https://console.cloud.google.com/billing
2. Set budget alerts
3. Configure quota limits

---

## 📁 File Structure Reference

```
Supervertaler/
├── Supervertaler_v2.5.0.py          ← Main application
├── api_keys.txt                     ← YOUR KEYS (not in Git) ✓
├── api_keys.example.txt             ← Template (in Git) ✓
├── .gitignore                       ← Security config ✓
├── custom_prompts/                  ← Public prompts ✓
├── custom_prompts_private/          ← Private prompts (not in Git) ✓
├── projects/                        ← Public projects ✓
└── projects_private/                ← Private projects (not in Git) ✓
```

**Legend**:
- ✓ = Protected by `.gitignore`
- Items marked "not in Git" will never be uploaded to GitHub

---

## 🆘 Getting Help

### Check Log Panel
Supervertaler shows detailed error messages in the log panel at the bottom:
- Look for "✗" (error) messages in red
- Check for "API Key Missing" or "Library Missing" messages
- Log shows exactly what went wrong

### Common Log Messages

```
✗ API Key Missing: Please configure your OPENAI API key
→ Solution: Add openai = your_key to api_keys.txt

✗ Library Missing: OpenAI library not installed
→ Solution: pip install openai

✓ Loaded 0 TM entries
→ Normal if you haven't loaded a TM file yet

✓ OpenAI API key loaded
→ Success! Your key is configured
```

### Still Stuck?

1. **Read the log carefully** - it usually tells you exactly what's wrong
2. **Check this guide again** - follow each step precisely
3. **Verify .gitignore** - confirm api_keys.txt is listed (line 5)
4. **Test the key directly** - try using it at the provider's playground
5. **Create an issue** - on GitHub with the error message (never include your actual key!)

---

## ✅ Security Checklist

Before you start using Supervertaler, verify:

- [ ] `api_keys.txt` exists in the Supervertaler folder
- [ ] `api_keys.txt` contains my actual API keys (not placeholders)
- [ ] `api_keys.txt` is listed in `.gitignore` (line 5)
- [ ] `.gitignore` file exists and is properly configured
- [ ] I have NOT committed `api_keys.txt` to Git
- [ ] I have NOT shared my `api_keys.txt` file with anyone
- [ ] I have set up billing alerts at my AI provider(s)
- [ ] I understand that API usage costs money (except Gemini free tier)
- [ ] I know how to revoke/regenerate keys if needed

---

## 📚 Additional Resources

### Official Documentation
- **OpenAI API**: https://platform.openai.com/docs/api-reference
- **Anthropic Claude**: https://docs.anthropic.com/en/api
- **Google Gemini**: https://ai.google.dev/gemini-api/docs

### Pricing Information
- **OpenAI Pricing**: https://openai.com/api/pricing/
- **Anthropic Pricing**: https://www.anthropic.com/pricing
- **Google Gemini Pricing**: https://ai.google.dev/pricing

### Community
- **Supervertaler GitHub**: https://github.com/michaelbeijer/Supervertaler
- **Issues/Questions**: Use GitHub Issues (never post your API keys!)

---

**Last Updated**: October 5, 2025  
**Supervertaler Version**: 2.5.0  
**Security Level**: Maximum 🔒
