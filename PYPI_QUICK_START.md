# PyPI Upload - Quick Start Guide

**Status**: ✅ Distribution packages built and ready!

**Files created**:
- `supervertaler-3.7.0.tar.gz` (2.51 MB)
- `supervertaler-3.7.0-py3-none-any.whl` (0.07 MB)

**Location**: `C:\Dev\Supervertaler\dist\`

---

## 🚀 Upload to PyPI (3 Simple Steps)

### Prerequisites
✅ PyPI account: https://pypi.org/account/register/  
✅ API token: Generated from PyPI account settings  
✅ Build tools: Already installed (build, twine)

---

### Step 1: Create/Get Your PyPI API Token

1. **Log in to PyPI**: https://pypi.org/account/login/

2. **Go to API tokens**:
   - Click your username (top right)
   - Select "Account settings"
   - Scroll to "API tokens"
   - Click "Add API token"

3. **Create token**:
   - **Name**: `Supervertaler-release`
   - **Scope**: Entire account
   - Click "Create"
   - **Save the token** (you won't see it again!)
   - Copy to clipboard

---

### Step 2: Upload to PyPI

Open PowerShell in project folder and run:

```powershell
cd C:\Dev\Supervertaler
twine upload dist/*
```

**When prompted**:
- **Username**: `__token__`
- **Password**: `pypi-AgEI...` (paste your token from Step 1)

**Success looks like**:
```
Uploading supervertaler-3.7.0-py3-none-any.whl
Uploading supervertaler-3.7.0.tar.gz
✓ Uploaded files successfully
```

---

### Step 3: Verify on PyPI

1. Go to: https://pypi.org/project/supervertaler/
2. You should see version 3.7.0 listed
3. Done! 🎉

---

## 📥 Users Can Now Install

After upload (PyPI may take 1-2 minutes to index):

```bash
pip install supervertaler
```

Or specific version:
```bash
pip install supervertaler==3.7.0
```

Or upgrade existing:
```bash
pip install --upgrade supervertaler
```

---

## ⚡ Alternative: Save Token Locally (Optional)

To avoid pasting token every time:

### Create `~\.pypirc` file

**Windows**: `C:\Users\[YourUsername]\.pypirc`

Content:
```ini
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-AgEI... [paste your full token here]
```

Then just run:
```powershell
twine upload dist/*
# No prompt needed!
```

---

## 🧪 Test Upload First (Recommended)

Before uploading to real PyPI, test with TestPyPI:

```powershell
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ supervertaler
```

If that works, do real upload (Step 2 above).

---

## 🎯 What Users Get

When they install:

```powershell
pip install supervertaler
```

They get:
- ✅ All Python dependencies installed automatically
- ✅ Full Supervertaler application
- ✅ Ready to run with: `python -m Supervertaler_v3.7.0`
- ✅ Or: `python -c "import Supervertaler_v3.7.0; Supervertaler_v3.7.0.main()"`

---

## 📊 Verify Installation Works Locally

Before releasing, test locally:

```powershell
# Uninstall any local version
pip uninstall supervertaler -y

# Install from local dist folder
pip install C:\Dev\Supervertaler\dist\supervertaler-3.7.0-py3-none-any.whl

# Test import
python -c "import Supervertaler_v3.7.0; print('✅ Works!')"

# Or run application
python -m Supervertaler_v3.7.0
```

---

## 🔐 Security Tips

1. **Never commit** `.pypirc` file to git
2. **Add to `.gitignore`**:
   ```
   .pypirc
   dist/
   build/
   *.egg-info/
   ```
3. **Rotate tokens** periodically on PyPI
4. **Treat token like password** - keep it secret!

---

## ❓ Troubleshooting

### "HTTPError 403: Forbidden"
- Wrong token or expired
- Solution: Generate new token from PyPI

### "File already exists"  
- Version 3.7.0 already uploaded
- Solution: Use new version (3.7.1) or delete old on PyPI

### "Package not found"
- Wait 1-2 minutes for PyPI indexing
- Or check spelling: `supervertaler` (lowercase!)

### "Import fails when installed"
- Make sure `Supervertaler_v3.7.0.py` is in right location
- Check setup.py `packages=find_packages()`
- Verify entry point configuration

---

## 🎊 Success Indicators

✅ Distribution files built (check ✓)  
✅ Packages uploaded to PyPI  
✅ Package visible at https://pypi.org/project/supervertaler/  
✅ Users can `pip install supervertaler`  
✅ Application runs after install

---

## 📝 Full Commands Reference

```powershell
# Build (already done)
python -m build

# Check quality
twine check dist/*

# Test upload
twine upload --repository testpypi dist/*

# Real upload
twine upload dist/*

# Users install
pip install supervertaler

# Users upgrade
pip install --upgrade supervertaler

# Check what's installed
pip show supervertaler
```

---

## 🚀 Ready?

```powershell
# Navigate to project
cd C:\Dev\Supervertaler

# Upload to PyPI
twine upload dist/*

# Done! 🎉
```

---

## 📚 Additional Resources

- PyPI Documentation: https://pypi.org/help/
- Twine Docs: https://twine.readthedocs.io/
- Python Packaging: https://packaging.python.org/
- setuptools: https://setuptools.pypa.io/

---

**Your Supervertaler v3.7.0 is ready for PyPI distribution! 🚀**

**Next: Commit changes and push to GitHub, then announce the release!**
