# Supervertaler v3.7.0 - Release Notes

## 🎯 Stable Production Release

**Release Date**: October 19, 2025  
**Version**: 3.7.0 (STABLE)  
**Python Requirement**: 3.12+  
**Status**: ✅ Production Ready

---

## 📦 What's Included

### Download Options

1. **Windows Executable** (Recommended for non-programmers)
   - `Supervertaler.exe` - Standalone Windows application
   - No Python installation required
   - Download, extract, and run
   - File size: ~150-180 MB

2. **Python Package** (Recommended for developers)
   - Install via pip: `pip install Supervertaler`
   - Requires Python 3.12+
   - Full source code included
   - Perfect for integration and customization

3. **Source Code**
   - Full repository with all features
   - Clone from: https://github.com/michaelbeijer/Supervertaler
   - For developers who want to modify or contribute

---

## ✨ Major Features (v3.7.0)

### Segment-Based CAT Editor
- **Grid View**: Professional spreadsheet-like editing
- **List View**: Vertical reading and reviewing
- **Document View**: Natural document flow for proofreading
- **Grid Pagination**: 10x faster loading for large documents (50 segments per page)

### Multi-Selection System (memoQ-style)
- Ctrl+Click to toggle individual segments
- Shift+Click to select ranges
- Ctrl+A to select all on current page
- Bulk operations on multiple segments
- Visual status indicators

### AI-Powered Translation
- **Multiple AI Providers**: OpenAI (GPT-4, GPT-4o), Claude (Sonnet, Opus), Google Gemini
- **Context-Aware**: Full document context + TM + custom instructions + system prompts
- **Professional Control**: Inline editing, status tracking, project management
- **Advanced Features**:
  - Translation Memory (TMX) integration with fuzzy matching
  - Custom Instructions for project-specific guidelines
  - System Prompts for domain specialists (Medical, Legal, Patent, Financial, etc.)
  - Tracked changes analysis for editing style learning

### Professional CAT Tool Integration
- **CafeTran Bilingual DOCX**: AI-based pipe symbol preservation
- **memoQ Bilingual DOCX**: Programmatic formatting preservation (bold/italic/underline)
- **Complete Round-Trip**: Import → Translate → Export → Reimport with formatting intact
- **100% Accuracy** verified on real-world translation projects

### Auto-Export Features
- **Session Reports** (MD/HTML): Statistics, timing, cost estimates
- **Translation Memory** (TMX): Export for reuse and consistency
- **Spreadsheets** (TSV, XLSX): Data analysis and client delivery
- **XLIFF Format**: Standard localization exchange format
- Automatic export after each translation

### PDF Rescue - AI-Powered OCR
- One-click PDF import for badly formatted documents
- GPT-4 Vision OCR with smart redaction handling
- Language-aware placeholder insertion
- Stamp and signature detection
- Professional DOCX export
- Session reports with full transparency

### Status Tracking & Quality Assurance
- **5-Level Status System**: Untranslated → Draft → Translated → Approved → Locked
- **Visual Indicators**: Color-coded status icons
- **Bulk Operations**: Change status for multiple segments
- **Find & Replace**: With regex support and scope filtering

### Figure Context (Visual Context)
- Load technical drawings and diagrams
- AI receives both text AND images for translation
- Essential for patents, technical manuals, scientific papers
- Automatic figure reference detection

---

## 🐛 Bug Fixes (v3.7.0)

All issues discovered during real-world testing have been fixed:

- ✅ **Filter mode save error** - Fixed initialization
- ✅ **Prompt save paths** - Corrected forward/backslashes and directories
- ✅ **Path display** - Normalized with proper OS separators
- ✅ **Folder links** - Now open correct System_prompts/Custom_instructions folders
- ✅ **Generated prompts** - Now saved to project file for persistence
- ✅ **Session reports** - Complete logs, branding, HTML links working

---

## 🎨 Professional Defaults

### New Project Settings (Production-Optimized)
- ✅ Auto-export Session Reports (MD & HTML)
- ✅ Auto-export Translation Memory (TMX)
- ✅ Auto-export Excel bilingual (XLSX)
- ✅ Include full document context by default
- ✅ Auto-propagate 100% TM matches
- ✅ Auto-activate generated prompts

### Quality-First Configuration
All new projects now follow professional translation practices out of the box.

---

## 📋 Installation & Setup

### Option 1: Windows Executable (Easiest)
```
1. Download Supervertaler.exe
2. Extract to desired location
3. Run Supervertaler.exe
4. Configure API keys (OpenAI, Claude, or Gemini)
5. Start translating!
```

### Option 2: Python Package Installation
```bash
# Install
pip install Supervertaler

# Run
python -m Supervertaler

# Or directly
supervertaler
```

### Option 3: From Source
```bash
# Clone repository
git clone https://github.com/michaelbeijer/Supervertaler.git
cd Supervertaler

# Install dependencies
pip install -r requirements.txt

# Run
python Supervertaler_v3.7.0.py
```

---

## 🔑 Getting API Keys

**OpenAI (GPT-4, GPT-4o)**  
https://platform.openai.com → API Keys → Create new secret key

**Anthropic (Claude)**  
https://console.anthropic.com → API Keys → Generate new key

**Google (Gemini)**  
https://aistudio.google.com → Get API key → Generate

---

## 📚 Documentation

- **README.md**: Feature overview and quick start
- **FAQ.md**: Comprehensive Q&A (in root directory)
- **USER_GUIDE.md**: Step-by-step workflows
- **INSTALLATION.md**: Detailed setup guide
- **CHANGELOG.md**: Complete version history
- **docs/guides/PDF_RESCUE.md**: AI-powered OCR guide

---

## 💼 Use Cases

### For Professional Translators
- AI-powered translation with professional CAT tool integration
- Context-aware output (full document, TM, custom instructions, domain expertise)
- Seamless workflow with memoQ, CafeTran, Trados
- Session reports for client delivery

### For Translation Agencies
- Multiple translator support (all local, no cloud sync - privacy first)
- Professional project management and status tracking
- Auto-export in multiple formats for client delivery
- Quality assurance tools (find/replace, status tracking)

### For Technical Translators
- Patent, medical, and legal domain specialists
- Figure context support for technical drawings
- Terminology consistency through TM and custom instructions
- PDF rescue for badly formatted source documents

### For Language Service Providers
- Commercial use permitted (respect open source license)
- No subscription required (pay only for API usage)
- Open source allows customization
- Professional, production-ready tool

---

## 🚀 Performance & Scalability

- **Large Documents**: Grid pagination handles 1000+ segments efficiently
- **Memory Usage**: Only current page in memory (configurable)
- **API Optimization**: Configurable chunk sizes for API calls
- **Batch Processing**: Process entire projects overnight if needed

**Tested Successfully On**:
- Documents with 1000+ segments
- memoQ bilingual DOCX with complex formatting
- CafeTran bilingual DOCX with pipe formatting
- Technical PDFs (20+ pages) with figure context
- All major AI providers (OpenAI, Claude, Gemini)

---

## 📊 Comparison: v2.5.0-CLASSIC vs v3.7.0

| Feature | v2.5.0-CLASSIC | v3.7.0 |
|---------|-----------------|--------|
| **Architecture** | Document-based workflow | Segment-based CAT editor |
| **UI Views** | Single view | Grid, List, Document views |
| **Pagination** | All segments at once | 50 per page (10x faster) |
| **Multi-Selection** | No | Yes (memoQ-style) |
| **Status Tracking** | Manual | 5-level system with icons |
| **Auto-Export** | Limited | 5+ formats |
| **Bilingual Support** | CafeTran (v2.4.3+) | CafeTran + memoQ |
| **Image Context** | Yes | Yes |
| **Production Status** | Stable | Stable (Latest) |

**Recommendation**: Use v3.7.0 for new projects. v2.5.0-CLASSIC still available for legacy workflows.

---

## 🔐 Security & Privacy

- **No telemetry**: Supervertaler does not collect usage data
- **Local storage**: All projects, TMs, and translations stored on your computer
- **Open source**: Code is public and inspectable
- **API-only**: Text only sent to chosen AI provider, not to Supervertaler
- **Private folders**: `user data_private` never synced to repository

**Data Flow**:
1. You load source document locally
2. Supervertaler sends text to your chosen AI provider
3. AI provider returns translation
4. Translation saved locally on your computer
5. No data sent to Supervertaler developers or third parties

---

## 🎓 Learning Resources

**Getting Started**:
- Download and run the application
- Create sample project with bilingual DOCX
- Try different AI models (GPT-4, Claude, Gemini)
- Experiment with custom instructions

**Advanced Usage**:
- Load Translation Memory (TMX) files
- Create domain-specific System Prompts
- Use tracked changes for style learning
- Configure auto-export for workflows
- Build custom prompts for specialized domains

**Community**:
- GitHub Issues: Bug reports, feature requests
- GitHub Discussions: Questions, tips, workflows
- Developer Website: https://michaelbeijer.co.uk

---

## 🤝 Contributing

**How to Help**:
- Test the application and report bugs
- Suggest improvements and new features
- Contribute code fixes (Python/tkinter)
- Improve documentation
- Share your workflows and best practices
- Translate UI to other languages

**GitHub**: https://github.com/michaelbeijer/Supervertaler

---

## 📝 License

Supervertaler is released under the MIT License.  
See LICENSE file in repository for details.

**Summary**: Free for personal and commercial use, must retain copyright notice, no warranty provided.

---

## 🙏 Acknowledgments

**Creator & Development**: Michael Beijer  
**AI-Assisted Development**: Claude Sonnet (Anthropic)  
**Testing & Feedback**: Real translation projects with memoQ and CafeTran

This project demonstrates the potential of human-AI collaboration in software development.

---

## 🔄 Upgrade Path

### From v2.5.0-CLASSIC
- Both versions can run on same computer
- Projects are separate (no automatic migration)
- Recommend trying v3.7.0 on test projects first
- Keep v2.5.0-CLASSIC for legacy workflows if needed

### Future Updates
- v3.8.0+: Additional features and refinements
- v4.0+: Potential architecture improvements
- Always: Community feedback drives development

---

## 📞 Support

**Quick Help**:
- Check FAQ.md for common questions
- Review README.md for feature overview
- Search GitHub Issues for similar problems

**Report Issues**:
- https://github.com/michaelbeijer/Supervertaler/issues
- Include version, Python version, OS, error message

**Feature Requests**:
- https://github.com/michaelbeijer/Supervertaler/issues
- Describe use case and desired behavior

---

## 🌟 What's Next

Supervertaler v3.7.0 is production-ready and recommended for professional use.

### Immediate (Weeks):
- User feedback collection
- Performance optimization
- Community contributions

### Short-term (Months):
- v3.8.0: Additional features based on feedback
- Quality assurance tools enhancements
- More CAT tool integrations

### Long-term (Quarters):
- v4.0: Major features (if needed based on usage)
- Cloud sync (optional)
- Plugin system
- Additional language support

---

## 💡 Pro Tips

1. **Cost Optimization**: Start with Gemini Flash (cheapest), upgrade to Claude Sonnet for quality
2. **Speed**: Reduce chunk size for faster processing (more API calls but lower cost)
3. **Quality**: Use Claude Sonnet or GPT-4o with full document context for best results
4. **TM Leverage**: Always load relevant TMX files for consistency and cost reduction
5. **Batch Processing**: Process large documents overnight to distribute costs
6. **Project Backups**: Supervertaler auto-saves projects - backup `user data/` regularly

---

## ✅ Quality Assurance

- ✅ Tested on real translation projects
- ✅ Bilingual DOCX round-trip verified (memoQ + CafeTran)
- ✅ 1000+ segment documents tested and optimized
- ✅ All major AI providers tested
- ✅ Security review: No data collection, no cloud upload
- ✅ Production-ready: Used by professional translator

---

## 🎉 Release Summary

**Supervertaler v3.7.0** represents a complete, production-ready AI-powered CAT editor for professional translators.

- ✅ Stable, tested, and reliable
- ✅ Professional features (multi-selection, status tracking, auto-export)
- ✅ Real-world tested workflows (memoQ, CafeTran bilingual DOCX)
- ✅ Multiple distribution methods (exe, pip, source)
- ✅ Comprehensive documentation
- ✅ Free and open source
- ✅ Ready for professional commercial use

**Download now and start translating smarter!**

---

*Made with ❤️ by Michael Beijer*  
*AI-Assisted development showcase* 

GitHub: https://github.com/michaelbeijer/Supervertaler  
Website: https://michaelbeijer.co.uk  
Email: info@michaelbeijer.co.uk
