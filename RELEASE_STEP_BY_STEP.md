# Creating GitHub Release - Step-by-Step Screenshots

## 🎯 Your Release Files

**Location**: `C:\Dev\Supervertaler\dist\`

- ✅ **Supervertaler-v3.7.0.zip** (108 MB) - Ready to upload
- ✅ **Supervertaler/** (folder) - Uncompressed version for testing

---

## Step 1: Open GitHub Releases Page

1. Open browser: https://github.com/michaelbeijer/Supervertaler/releases

2. You should see:
   - List of previous releases
   - "Create a new release" button (top right)

```
┌─────────────────────────────────────────────────────┐
│ GitHub.com > michaelbeijer/Supervertaler > Releases│
├─────────────────────────────────────────────────────┤
│ [Create a new release] ← CLICK THIS                │
├─────────────────────────────────────────────────────┤
│ v3.6.5  │ Release title...  │ Published Oct 1      │
│ v3.6.0  │ Release title...  │ Published Sep 15     │
│ v3.5.0  │ Release title...  │ Published Aug 10     │
└─────────────────────────────────────────────────────┘
```

---

## Step 2: Fill in Release Details

Click "Create a new release" and you'll see this form:

```
┌─────────────────────────────────────────────────────┐
│ Release title:                                      │
│ ┌───────────────────────────────────────────────┐  │
│ │ Supervertaler v3.7.0 - Stable Release         │  │
│ └───────────────────────────────────────────────┘  │
│                                                     │
│ Tag version:                                        │
│ ┌───────────────────────────────────────────────┐  │
│ │ v3.7.0                                        │  │
│ └───────────────────────────────────────────────┘  │
│                                                     │
│ Target: main                                        │
│                                                     │
│ Release notes (Describe the release):               │
│ ┌───────────────────────────────────────────────┐  │
│ │ # Supervertaler v3.7.0 - Stable Release      │  │
│ │                                               │  │
│ │ Professional AI-powered CAT editor...        │  │
│ │ [Copy from RELEASE_NOTES_v3.7.0.md]          │  │
│ │                                               │  │
│ │                                               │  │
│ └───────────────────────────────────────────────┘  │
│                                                     │
│ ☐ This is a pre-release                            │
│ ☐ Create a discussion for this release             │
│                                                     │
│ [Save as draft] [Preview] [Publish release]        │
└─────────────────────────────────────────────────────┘
```

### What to Enter:

**Release title:**
```
Supervertaler v3.7.0 - Stable Release
```

**Tag version:**
```
v3.7.0
```

**Release notes:**  
Copy everything from your `RELEASE_NOTES_v3.7.0.md` file

---

## Step 3: Attach the Zip File

Scroll down in the release form. You'll see:

```
┌─────────────────────────────────────────────────────┐
│ Attachments                                         │
│ ┌───────────────────────────────────────────────┐  │
│ │ Attach binaries by dropping them here or      │  │
│ │ [selecting them]                              │  │
│ └───────────────────────────────────────────────┘  │
│                                                     │
│ Click or drag-drop: Supervertaler-v3.7.0.zip      │
│                                                     │
│ Upload progress: [████████████░░░░] 75%            │
│                                                     │
│ ✓ Supervertaler-v3.7.0.zip (108 MB)               │
└─────────────────────────────────────────────────────┘
```

**Options:**
- **Option A (Easiest)**: Drag and drop the zip file onto the attachment area
- **Option B**: Click "selecting them" and browse to `C:\Dev\Supervertaler\dist\Supervertaler-v3.7.0.zip`

Wait for the upload to complete (may take 1-2 minutes for 108 MB)

---

## Step 4: Configure Release Settings

Make sure these are correct:

```
☐ This is a pre-release     ← UNCHECK THIS! (This IS a stable release)
☐ Create a discussion...     ← Optional (check if you want)

Target: main                 ← Should be "main" branch
```

---

## Step 5: Publish Release

At the bottom of the form, click:

```
┌─────────────────────────────────────┐
│  [Save as draft] [Preview]          │
│  [Publish release] ← CLICK THIS!   │
└─────────────────────────────────────┘
```

---

## ✅ Success!

After clicking "Publish release", you should see:

```
┌─────────────────────────────────────────────────────┐
│ ✓ Release published!                                │
│                                                     │
│ v3.7.0 - Supervertaler v3.7.0 - Stable Release    │
│ Released Oct 19, 2025 by [you]                     │
│                                                     │
│ [Edit release] [Delete release]                    │
│                                                     │
│ ### Assets                                         │
│ Supervertaler-v3.7.0.zip (108 MB)                 │
│ Downloads: 0 ↓ | Latest ★                         │
│                                                     │
│ [Source code (zip)]                               │
│ [Source code (tar.gz)]                            │
└─────────────────────────────────────────────────────┘
```

---

## 🧪 Test Before Sharing

### Windows Users Can Now:

1. **Download** the zip from the release page
2. **Extract** it anywhere
3. **Run** `Supervertaler/Supervertaler.exe`
4. **It just works!** ✅

### You Should Test:

```powershell
# Test the exe locally first
C:\Dev\Supervertaler\dist\Supervertaler\Supervertaler.exe

# Make sure it starts without errors
```

---

## 🔄 URL Pattern

After publishing, your release will be at:

```
https://github.com/michaelbeijer/Supervertaler/releases/tag/v3.7.0
```

You can:
- Share this link
- Download from this link
- Edit the release from this link
- Delete the release from this link

---

## 📋 Release Page Shows:

```
┌──────────────────────────────────────┐
│ 📦 Supervertaler v3.7.0              │
│ Stable Release                       │
│ Released Oct 19, 2025                │
├──────────────────────────────────────┤
│ [Full release notes content here]    │
├──────────────────────────────────────┤
│ ASSETS                               │
│ ✓ Supervertaler-v3.7.0.zip (108 MB) │
│   Downloads: 0 ↓                     │
│ ✓ Source code (zip)                 │
│ ✓ Source code (tar.gz)              │
└──────────────────────────────────────┘
```

Users click the zip to download!

---

## ❓ Common Issues

### "File is still uploading"?
- Wait a bit longer (large file)
- Refresh the page

### "Can't find the Publish button"?
- Scroll down in the form
- Make sure you filled in title and tag

### "Release shows as draft"?
- Click "Publish release" again
- Or edit and check "pre-release" status

### "Want to change something?"
- Click "Edit release"
- Update and save
- Or delete and create new release

---

## 🎉 You're Done!

Your release is now live at:  
https://github.com/michaelbeijer/Supervertaler/releases/tag/v3.7.0

**Next steps** (optional):
- 📢 Announce on social media
- 📖 Update your website
- 💬 Post in relevant communities
- 📊 Monitor download numbers

---

**Congratulations! Supervertaler v3.7.0 is officially released! 🚀**
