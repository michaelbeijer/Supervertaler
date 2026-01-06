# Unified Prompt Library - User Guide

## 🎉 What's New

Supervertaler's prompt system has been simplified from a confusing 4-layer architecture to an intuitive 2-layer system:

### Old System (Confusing!)
- ❌ System Prompts tab
- ❌ Domain Prompts tab  
- ❌ Project Prompts tab
- ❌ Style Guides tab
- 🤯 Too many layers, hard to understand

### New System (Simple!)
- ✅ **System Prompts** (in Settings - you rarely touch these)
- ✅ **Prompt Library** (your main workspace - one unified view)

---

## 📚 The Prompt Library

### What Is It?

Your unified workspace for managing all translation prompts, style guides, and instructions. Think of it like CoTranslatorAI's prompt library, but better organized.

### Main Features

#### 1. **Folder Organization**
- Create unlimited nested folders
- Organize prompts however you want
- Built-in folders: Style Guides, Domain Expertise, Project Prompts
- Create your own: Active Projects, Clients, Languages, etc.

#### 2. **Favorites ⭐**
- Mark frequently-used prompts as favorites
- Quick access from the Favorites section at the top

#### 3. **Quick Run Menu 🚀**
- Add prompts to your Quick Run menu
- Perfect for one-click operations

#### 4. **Multi-Attach 📎**
- Set ONE primary prompt (your main instructions)
- Attach multiple additional prompts (style guides, formatting rules, etc.)
- System automatically combines them

---

## 🔧 System Prompts (Advanced)

### What Are They?

Technical prompts that handle CAT tool tag preservation and basic translation setup. They're automatically selected based on what you're doing:

- **Single Segment** - When translating selected text
- **Batch DOCX** - When processing Word documents
- **Batch Bilingual** - When importing CAT tool bilingual files

### Where Are They?

Settings > Translation > System Prompts

⚠️ **Warning:** Only modify these if you understand CAT tool formats. These handle the technical stuff (memoQ tags, Trados tags, etc.).

---

## 💡 How to Use

### Basic Workflow

1. **Open Prompt Library** (tab in main interface)

2. **Find or create your prompt:**
   - Browse folders
   - Right-click to create new prompts/folders

3. **Set as active:**
   - Double-click a prompt to set as Primary
   - OR right-click → "Set as Primary Prompt"

4. **Add style guides/extras:**
   - Right-click another prompt → "Attach to Active"
   - Add as many as you need

5. **Translate!**
   - System automatically combines:
     - System Prompt (auto-selected)
     - Your Primary Prompt
     - Your Attached Prompts

### Example: Medical Device Translation

```
Primary Prompt:
📄 Medical Translation Specialist
   (Domain expertise, terminology)

Attached:
📎 Dutch Style Guide
   (Number formatting, units)
📎 Professional Tone & Style
   (Formal register, no contractions)

System auto-selects:
🔧 Batch Bilingual Template
   (Tag preservation, formatting)

= Final combined prompt sent to LLM
```

---

## 🎯 Right-Click Menu

Right-click any prompt to:

- **⭐ Set as Primary Prompt** - Make it your main instruction
- **📎 Attach to Active** - Add to current configuration
- **☆ Add to Favorites** - Quick access
- **Add to Quick Run** - One-click execution
- **✏️ Edit** - Modify content
- **📋 Duplicate** - Create copy
- **🗑️ Delete** - Remove

Right-click folders to:

- **+ New Prompt in Folder** - Create prompt here
- **📁 New Subfolder** - Create subfolder

---

## 📂 Folder Structure

After migration, your prompts are organized like this:

```
Prompt Library/
├── ⭐ Favorites
│   └── (Your favorite prompts)
├── 🚀 Quick Run Menu
│   └── (Your quick-run prompts)
├── 📁 Style Guides
│   ├── Dutch.md
│   ├── English.md
│   └── ...
├── 📁 Domain Expertise
│   ├── Medical Translation Specialist.md
│   ├── Legal Translation Specialist.md
│   └── ...
├── 📁 Project Prompts
│   ├── Professional Tone & Style.md
│   └── ...
└── 📁 Active Projects
    └── (Create your own subfolders)
```

---

## 🔄 Migration

### What Happened?

When you first opened the new version:

1. ✅ Old folders backed up with `.old` extension
2. ✅ All prompts migrated to new Library/ folder
3. ✅ Metadata added (favorites, quick-run, etc.)
4. ✅ JSON prompts converted to Markdown
5. ✅ System Prompts moved to Settings

### Your Old Files

- **Backed up** in same location with `.old` extension
- **Not deleted** - safe to remove once you verify everything works
- Located in: `user_data/Prompt_Library/*.old`

### Rollback

If something went wrong (unlikely), you can manually:

1. Delete `user_data/Prompt_Library/Library/`
2. Rename `.old` folders back to original names
3. Restart application

---

## 🆕 Creating Prompts

### Option 1: In the UI

1. Click "**+ New Prompt**" button
2. Enter name and content
3. Save

### Option 2: Create Markdown File

Create a new `.md` file in any Library subfolder:

```markdown
---
name: "My Custom Prompt"
description: "What this prompt does"
favorite: false
quick_run: false
tags: ["medical", "dutch"]
---

# Your prompt content here

You are a specialist in...
```

Refresh the library to see it.

---

## 🤔 FAQ

### Q: Where did my prompts go?

**A:** They're in `Prompt Library/Library/`. The tree view shows them organized by folder.

### Q: Can I still use my old prompts?

**A:** Yes! They were automatically migrated. Check the new folder structure.

### Q: What if I liked the old 4-layer system?

**A:** The new system does the same thing, just more intuitively. Your primary prompt replaces "Domain Prompt," attached prompts replace "Project Prompts" and "Style Guides."

### Q: How do I edit System Prompts?

**A:** Settings > Translation > System Prompts. But be careful - these handle CAT tool tags.

### Q: Can I organize prompts differently?

**A:** Absolutely! Create any folder structure you want. The built-in folders are just suggestions.

### Q: What's the difference between Primary and Attached?

**A:** 
- **Primary** = Your main translation instructions (domain expertise, task type)
- **Attached** = Additional rules that modify the primary (style guides, formatting, tone)

---

## 🐛 Troubleshooting

### Prompts not showing up

1. Click "🔄 Refresh" button
2. Check they're `.md` or `.txt` files
3. Check file permissions

### Migration failed

- Check logs in terminal
- Backup files should exist as `.old`
- Contact support with error message

### Can't find old prompts

- Look in `user_data/Prompt_Library/*.old` folders
- These are your backups
- Copy any missing files to `Library/` manually

---

## 💡 Tips & Best Practices

### Organization

- **Style Guides folder:** Language-specific formatting rules
- **Domain Expertise folder:** Industry/domain knowledge
- **Active Projects folder:** Client-specific instructions
- Create project subfolders: `Active Projects/ClientName/ProjectCode/`

### Favorites

- Mark 3-5 most-used prompts as favorites
- Faster than browsing folders
- Perfect for your "go-to" domain prompts

### Multi-Attach Strategy

```
Primary: Domain expertise (Medical, Legal, etc.)
Attach: Language style guide (Dutch, English UK, etc.)
Attach: Project-specific rules (if any)
Attach: Tone/formatting preferences

= Comprehensive combined prompt
```

### Naming

- Use descriptive names: "Medical Device IFU Translation"
- Not: "Prompt 1", "Test", "New"
- Include language if relevant: "Dutch Style Guide"

---

## 🚀 Advanced

### Prompt Variables

Use these placeholders in your prompts:

- `{{SOURCE_LANGUAGE}}` - Auto-replaced with source language
- `{{TARGET_LANGUAGE}}` - Auto-replaced with target language
- `{{SOURCE_TEXT}}` - Auto-replaced with text to translate

### Tags

Add tags to prompts for better organization:

```yaml
tags: ["medical", "regulatory", "dutch", "high-priority"]
```

(Future: Search/filter by tags)

### Quick Run

- Add prompts for instant execution
- Perfect for utilities like "Count words", "Explain", "Proofread"
- One-click access from Quick Run menu

---

## 📞 Support

Questions? Issues?

- Check this guide first
- Check logs in terminal
- Report issues with:
  - What you were trying to do
  - Error message
  - Which prompt/folder

---

**Enjoy the simplified prompt system! 🎉**
