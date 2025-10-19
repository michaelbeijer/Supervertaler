# Quick Release Checklist - v3.7.0

## ✅ Pre-Release (DO THIS FIRST)

- [ ] Zip file created: `dist/Supervertaler-v3.7.0.zip` (108 MB)
- [ ] Test exe works: `dist/Supervertaler/Supervertaler.exe` ✓ Double-click works
- [ ] All folders present in zip:
  - [ ] docs/
  - [ ] user data/
  - [ ] modules/
  - [ ] assets/
- [ ] All files present in zip:
  - [ ] Supervertaler.exe
  - [ ] README.md
  - [ ] CHANGELOG.md
  - [ ] FAQ.md
  - [ ] api_keys.example.txt
- [ ] Documentation ready:
  - [ ] RELEASE_NOTES_v3.7.0.md
  - [ ] README.md updated
  - [ ] CHANGELOG.md updated
- [ ] Git commits pushed: `git push origin main`

---

## 🚀 Create GitHub Release (5 minutes)

### Web Interface (Easiest):

1. Go to: https://github.com/michaelbeijer/Supervertaler/releases

2. Click: "Create a new release"

3. Fill in:
   - Tag: `v3.7.0`
   - Title: `Supervertaler v3.7.0 - Stable Release`
   - Description: Copy from RELEASE_NOTES_v3.7.0.md

4. Attach file:
   - Drag/drop or click "Attach"
   - Select: `Supervertaler-v3.7.0.zip` (108 MB)
   - Wait for upload

5. Publish:
   - ❌ Uncheck "Pre-release" 
   - Click "Publish release"

6. Done! ✅

### Command Line (Alternative):

```powershell
cd C:\Dev\Supervertaler

# Install if needed
# choco install gh

# Login (first time only)
# gh auth login

# Create release
gh release create v3.7.0 `
  --title "Supervertaler v3.7.0 - Stable Release" `
  --notes-file RELEASE_NOTES_v3.7.0.md `
  dist/Supervertaler-v3.7.0.zip
```

---

## ✨ Post-Release (Optional)

- [ ] Test download from release page
- [ ] Announce on Twitter/social media
- [ ] Update website/documentation
- [ ] Monitor for issues
- [ ] Celebrate! 🎉

---

## 📊 What Users Get

**File size**: 108 MB  
**Extract to**: Any folder  
**Run**: `Supervertaler/Supervertaler.exe`  
**Requirements**: Windows, nothing else!

---

## 🎯 Release Info

- **Version**: 3.7.0
- **Status**: Stable
- **Release Type**: Full release (not beta/pre-release)
- **File**: Supervertaler-v3.7.0.zip
- **Size**: 108 MB (compressed)
- **Includes**: Exe + all documentation + templates

---

## ❓ Quick FAQ

**Q: Is the exe tested?**  
A: Not yet - test it first by double-clicking `dist/Supervertaler/Supervertaler.exe`

**Q: What if I need to change something?**  
A: Edit, rebuild with `python build_distribution.py`, and create a new release (v3.7.1)

**Q: Do users need Python?**  
A: No! The exe is standalone.

**Q: How do I delete a release if something's wrong?**  
A: GitHub > Releases > v3.7.0 > Delete (before many downloads)

**Q: Can I edit after publishing?**  
A: Yes - just re-upload if file was bad. But release date will stay the same.

---

## 📞 Support

**Need help?** See:
- RELEASE_DISTRIBUTION_GUIDE.md (detailed steps)
- GITHUB_RELEASE_GUIDE.md (original guide)
- RELEASE_NOTES_v3.7.0.md (what to copy)

---

**Ready? Let's release! 🚀**
