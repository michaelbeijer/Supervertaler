# 🎯 CAT EDITOR - QUICK REFERENCE CARD

## 🚀 START THE APP
```powershell
cd "c:\Users\pc\My Drive\Software\Python\Supervertaler\cat_tool_prototype"
python cat_editor_prototype.py
```

## ⌨️ KEYBOARD SHORTCUTS
| Key | Action |
|-----|--------|
| **Ctrl+O** | Import DOCX |
| **Ctrl+S** | Save Project |
| **Ctrl+L** | Load Project |
| **Ctrl+F** | Find/Replace |
| **Ctrl+D** | Copy Source → Target |
| **Ctrl+Enter** | Save & Next |
| **Enter** | Edit Segment |
| **↑↓** | Navigate |

## 🎨 STATUS COLORS
- 🔴 **Red** = Untranslated
- 🟡 **Yellow** = Draft
- 🟢 **Green** = Translated
- 🔵 **Blue** = Approved

## 📤 EXPORT OPTIONS
1. **DOCX** - Translated document (formatting preserved)
2. **Bilingual DOCX** - Source | Target table (for review)
3. **TSV** - Tab-separated (opens in Excel)

## 🔄 TYPICAL WORKFLOW
1. Import DOCX (`Ctrl+O`)
2. Translate each segment
3. Mark status as you go
4. Save project (`Ctrl+S`)
5. Export DOCX when done

## 💡 PRO TIPS
- **Ctrl+D** for identical text (e.g., figure numbers)
- **Ctrl+F** for terminology consistency
- **Ctrl+Enter** for speed
- Save often with **Ctrl+S**

## 📁 FILES
- **cat_editor_prototype.py** - Main app
- **simple_segmenter.py** - Segmentation
- **docx_handler.py** - DOCX handler
- **README.md** - Full docs
- **QUICK_START.md** - Tutorial

## 🆘 TROUBLESHOOTING
**No segments after import?**
→ Check DOCX has text

**Export fails?**
→ Original DOCX must exist

**Crashes?**
→ Check python-docx installed

## 📞 GET HELP
1. Read `README.md`
2. Read `QUICK_START.md`
3. Check `COMPLETION_REPORT.md`

---
**🎉 Ready to translate! 🌍✨**
