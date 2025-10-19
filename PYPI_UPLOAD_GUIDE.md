# PyPI Upload Guide - Supervertaler v3.7.0

**Goal**: Make Supervertaler installable via `pip install Supervertaler`

**Timeline**: 5-10 minutes setup + 2-3 minutes for first upload

---

## 📋 Checklist

- ✅ setup.py created
- ✅ pyproject.toml created
- ✅ MANIFEST.in created
- ✅ Version: 3.7.0
- ✅ Email: info@michaelbeijer.co.uk
- ✅ Git commits pushed
- ⏳ PyPI account setup (ONE-TIME)
- ⏳ Build and upload

---

## 🔑 Step 1: Create PyPI Account (One-time)

### A. Create Account
1. Go to: https://pypi.org/account/register/
2. Fill in:
   - **Username**: `michaelbeijer` (or choose yours)
   - **Email**: `info@michaelbeijer.co.uk`
   - **Password**: Strong password (save it!)
3. Verify email
4. Create account

### B. Set Up API Token (Recommended - More Secure)
1. Log in to https://pypi.org/
2. Go to: Account settings > API tokens
3. Click: "Add API token"
4. Name: `Supervertaler-token`
5. Scope: "Entire account"
6. Create and **save the token** (you won't see it again!)
   - Looks like: `pypi-AgEI...` (long string)

### C. Store Token Locally
Create file: `~/.pypirc` (in your home directory)

**Windows**: `C:\Users\[YourUsername]\.pypirc`

Content:
```ini
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-AgEI... [paste your token here]
```

Or use keyring (more secure):
```powershell
pip install keyring
keyring set https://upload.pypi.org/legacy/ __token__
# Paste token when prompted
```

---

## 🔧 Step 2: Install Build Tools

Run in PowerShell:

```powershell
pip install --upgrade build twine
```

This installs:
- **build**: Creates distribution packages
- **twine**: Uploads to PyPI securely

---

## 📦 Step 3: Build Distribution Packages

In your project root (`C:\Dev\Supervertaler`):

```powershell
cd C:\Dev\Supervertaler

# Clean previous builds
rm -Recurse dist, build, *.egg-info -Force -ErrorAction SilentlyContinue

# Build distribution
python -m build
```

**Output should show**:
```
Successfully built Supervertaler-3.7.0-py3-none-any.whl
Successfully built Supervertaler-3.7.0.tar.gz
```

**This creates in `dist/` folder**:
- `Supervertaler-3.7.0.tar.gz` (source distribution)
- `Supervertaler-3.7.0-py3-none-any.whl` (wheel distribution)

---

## ✅ Step 4: Test Upload to TestPyPI (Optional but Recommended)

Before uploading to real PyPI, test with TestPyPI (sandbox):

```powershell
# Test upload
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# When prompted:
# Username: __token__
# Password: [paste your TestPyPI token or use keyring]
```

**If successful**, you'll see:
```
Uploading Supervertaler-3.7.0.tar.gz
Uploading Supervertaler-3.7.0-py3-none-any.whl
Successfully uploaded
```

**Then test install from TestPyPI**:
```powershell
pip install --index-url https://test.pypi.org/simple/ Supervertaler
```

---

## 🚀 Step 5: Upload to Real PyPI

Once you're confident, upload to the real PyPI:

```powershell
twine upload dist/*
```

**When prompted**:
- Username: `__token__`
- Password: `pypi-AgEI...` (your token, or use keyring)

**Success output**:
```
Uploading Supervertaler-3.7.0-py3-none-any.whl
Uploading Supervertaler-3.7.0.tar.gz
Successfully uploaded
```

---

## 🎉 Step 6: Verify on PyPI

After upload (usually appears in 1-2 minutes):

1. Go to: https://pypi.org/project/Supervertaler/
2. You should see:
   - Version 3.7.0
   - Your description
   - Installation instructions

---

## 📥 Step 7: Users Can Now Install

After upload, anyone can install with:

```powershell
pip install Supervertaler
```

Or specific version:
```powershell
pip install Supervertaler==3.7.0
```

Or upgrade existing:
```powershell
pip install --upgrade Supervertaler
```

---

## 🔄 Future Updates

When you release v3.7.1, v3.8.0, etc.:

1. Update version in `Supervertaler_v3.7.0.py` (or version file)
2. Update `setup.py` if needed
3. Run:
   ```powershell
   python -m build
   twine upload dist/*
   ```
4. Done! Users get `pip install --upgrade Supervertaler`

---

## ❓ Troubleshooting

### "HTTPError 403: Forbidden"
- Token expired or wrong scope
- Solution: Generate new token from PyPI account page

### "Already exists"
- Version 3.7.0 already uploaded
- Solution: Use new version number (3.7.1) or delete old release on PyPI

### "Package not found on PyPI"
- Wait 1-2 minutes, PyPI indexing
- Solution: Refresh or check spelling

### "Installation fails"
- Dependencies missing or outdated
- Check: `setup.py` has all required packages in `install_requires`

### "Wrong Python version"
- PyPI may not support Python 3.12 fully yet
- Solution: Test with Python 3.11 or add version classifiers

---

## 📊 What Users Get

When they run `pip install Supervertaler`:

1. **Downloads**: Latest version
2. **Installs**: Python dependencies:
   - python-docx
   - openpyxl
   - Pillow
   - openai
   - anthropic
   - google-generativeai
   - etc.
3. **Runs**: `python Supervertaler_v3.7.0.py`
4. **Ready**: Full application

---

## 🔐 Security Notes

1. **Never commit `.pypirc`** to git (add to `.gitignore`)
2. **Use API tokens**, not passwords
3. **Rotate tokens** periodically
4. **Keep token private** - treat like password

---

## 📝 Complete Command Reference

```powershell
# One-time setup
pip install --upgrade build twine

# Build packages
python -m build

# Test upload (optional)
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Real upload
twine upload dist/*

# Users install
pip install Supervertaler

# Users upgrade
pip install --upgrade Supervertaler

# Check version installed
pip show Supervertaler
```

---

## ✨ That's It!

Your package is now on PyPI! 🎉

**Share with users**:
- Simple: `pip install Supervertaler`
- Professional: Post URL to PyPI package page
- Documentation: Link to GitHub repo

---

## 🎯 Next Steps

After first upload:
1. ✅ Test local installation: `pip install Supervertaler`
2. ✅ Verify on PyPI: https://pypi.org/project/Supervertaler/
3. ✅ Update documentation
4. ✅ Announce to users
5. ✅ Monitor for issues

---

**Congratulations! Your package is live on PyPI! 🚀**
