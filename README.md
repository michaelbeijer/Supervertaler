# Supervertaler v3.7.1

🎯 **Context-aware, LLM-powered CAT editor for professional translators** — Revolutionary segment-based translation tool with AI-enhanced prompts, PDF Rescue OCR, and seamless CAT tool integration.

**Latest Version**: v3.7.1 (October 20, 2025)

---

## ✨ What is Supervertaler?

Supervertaler is a **professional Computer-Aided Translation (CAT) editor** designed by a 30-year veteran translator for translators. It combines:

- 🤖 **Multiple AI providers** - OpenAI GPT-4, Anthropic Claude, Google Gemini
- 🎯 **Context-aware translation** - Full document understanding, figure context, translation memory
- 📚 **Unified Prompt Library** - System Prompts (AI role) + Custom Instructions (user preferences)
- 🆘 **PDF Rescue** - AI-powered OCR for badly-formatted PDFs
- ✅ **Professional CAT features** - Segment editing, grid pagination, dual selection (memoQ-style)
- 🔗 **CAT tool integration** - memoQ, CafeTran, Trados Studio support
- 📊 **Smart auto-export** - Session reports, TMX, TSV, XLIFF, Excel
- 💾 **Translation Memory** - Fuzzy matching with segment context

---

## 🚀 Current Version: v3.7.1

**File**: `Supervertaler_v3.7.1.py`

### 📌 What's New in v3.7.1

🔒 **Security & Configuration Updates** (v3.7.1 - October 20, 2025):
- 🛡️ **Data Folder Security** - Reorganised user data handling to separate dev and user environments
- 🔐 **API Keys Protection** - Moved `api_keys.txt` to user data folder (never committed to git)
- 📁 **Configurable Data Folders** - Users can now choose where to store projects and resources on first launch
- ⚙️ **Settings Menu** - Added "Change Data Folder" option to Settings tab
- 🐛 **Bug Fixes** - Fixed Tkinter error in Prompt Library tab switching

### 📌 What's New in v3.7.1

✨ **Product Unification**:
- Unified product focus on v3.x CAT Edition
- Single clear product line for users and LSPs
- Simplified repository and documentation

📁 **Folder Structure Reorganization** (v3.7.1):
- `Prompt_Library/System_prompts/` - Domain-specific prompts (19 files)
- `Prompt_Library/Custom_instructions/` - User preferences (8 files)
- `Translation_Resources/Glossaries/` - Terminology databases
- `Translation_Resources/TMs/` - Translation Memory files
- `Translation_Resources/Non-translatables/` - Non-translatable lists
- `Translation_Resources/Segmentation_rules/` - Segmentation rules

📝 **Markdown Prompt Format** (v3.7.1):
- All prompts now in Markdown with YAML frontmatter
- Human-readable format (no escaped JSON)
- Beautiful Markdown tables for glossaries
- Mixed format support (loads both `.json` and `.md`)

### 🎯 Core Features

**Translation Engine**:
- ✅ Multiple AI providers with model selection
- ✅ Custom prompts with variable substitution (`{source_lang}`, `{target_lang}`, `{domain}`, etc.)
- ✅ Translation Memory with fuzzy matching
- ✅ Full document context for better accuracy
- ✅ Tracked changes learning (learns from your edits)

**Professional CAT Editor**:
- ✅ **Grid View** - 50 segments per page (10x faster loading!)
- ✅ **List View** - Simple inline editing
- ✅ **Document View** - Full document layout
- ✅ **Dual Selection** - memoQ-style multi-segment selection
- ✅ **Smart Pagination** - Instant navigation between pages
- ✅ **Figure Context** - Multimodal AI with image understanding

**Prompt Management**:
- 🎯 **System Prompts** - Define AI behavior (specialist roles)
- 📝 **Custom Instructions** - User preferences & guidelines
- 🤖 **Prompt Assistant** - AI-powered document analysis and prompt generation
- 🔍 **Prompt Library** - Browse, edit, create, filter prompts

**PDF Rescue - AI-Powered OCR** (v3.5+):
- 📄 One-click PDF import with automatic page extraction
- 🧠 GPT-4 Vision for badly-formatted PDFs
- 🎨 Optional formatting preservation (markdown-based)
- 🔍 Smart redaction/stamp handling with language-aware placeholders
- 📊 Professional session reports with branding

**CAT Tool Integration**:
- ☕ **CafeTran Bilingual DOCX** - AI-based pipe symbol preservation
- 📊 **memoQ Bilingual DOCX** - Programmatic formatting preservation
- 🏢 **Trados Studio** - XLIFF import/export with tag preservation
- 💾 **Export Formats** - DOCX, TSV, JSON, XLIFF, TMX, Excel, HTML, Markdown

**Data Management**:
- 💾 Project save/load with full context preservation
- 📁 Organised folder structure (Prompt_Library, Translation_Resources, Projects)
- 🔄 Automatic backup capability
- 👥 Dev mode with parallel folder structure (`user data/` vs `user data_private/`)

---

## 🔧 Getting Started

### Installation - Choose Your Method

Supervertaler v3.7.1 is available in **three ways**:

#### **1️⃣ Windows Executable (Easiest - Recommended for Most Users)**

No Python installation required!

1. **Download**: Get the latest release from [GitHub Releases](https://github.com/michaelbeijer/Supervertaler/releases)
2. **Extract**: Unzip `Supervertaler-v3.7.1.zip` to any folder
3. **Run**: Double-click `Supervertaler/Supervertaler.exe`
4. **Configure**: Add your API keys and start translating!

**Advantages**:
- ✅ No Python needed
- ✅ Works on any Windows system
- ✅ All documentation and templates included
- ✅ Portable - run from USB stick
- ✅ Fastest startup

#### **2️⃣ Python Package (pip - For Python Developers)**

For those with Python 3.12+ installed:

```bash
pip install supervertaler
```

Then run:
```bash
python -m Supervertaler_v3.7.1
```

> **Note**: v3.7.1 has been yanked from PyPI due to security updates. v3.7.1 includes critical data folder security improvements.

**Advantages**:
- ✅ Easy updates: `pip install --upgrade supervertaler`
- ✅ Integrates with Python projects
- ✅ Full source code visible
- ✅ Can customise and extend

#### **3️⃣ From Source (For Contributors and Developers)**

```bash
# Clone repository
git clone https://github.com/michaelbeijer/Supervertaler.git
cd Supervertaler

# Install dependencies
pip install -r requirements.txt

# Run application
python Supervertaler_v3.7.1.py
```

**Advantages**:
- ✅ Latest development version
- ✅ Full access to source code
- ✅ Can contribute improvements
- ✅ Perfect for customization

---

### Quick Comparison Table

| Method | Setup Time | Python Required | Updates | Best For |
|--------|-----------|-----------------|---------|----------|
| **Windows Exe** | 30 seconds | ❌ No | Manual | Most users |
| **pip** | 1 minute | ✅ Yes (3.12+) | `pip upgrade` | Developers |
| **From Source** | 2 minutes | ✅ Yes (3.12+) | `git pull` | Contributors |

---

### First Steps

1. **Configure API Keys**: Set up OpenAI, Claude, or Gemini credentials
2. **Explore System Prompts** (Ctrl+P) - Browse domain-specific specialist prompts
3. **Create Custom Instructions** - Define your translation preferences
4. **Open a Document** - Import DOCX, create segments
5. **Start Translating** - Use System Prompts or custom instructions
6. **Export Results** - Session reports, TMX, auto-export to CAT tools

---

## 📖 Documentation

- **User Guide**: [USER_GUIDE.md](USER_GUIDE.md)
- **CAT Tool Integration**:
  - [CafeTran Integration](.dev/docs/features/CAFETRAN_SUPPORT.md)
  - [memoQ Integration](.dev/docs/features/MEMOQ_SUPPORT.md)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **Website**: [supervertaler.com](https://supervertaler.com)

---

## 🎯 Why Supervertaler?

### For Professional Translators
- ✅ Built by a professional translator (30 years experience)
- ✅ Designed for real translation workflows, not generic AI
- ✅ Integrates with your existing CAT tools
- ✅ Context-aware for better accuracy
- ✅ Fully open source - no vendor lock-in

### For Translation Agencies (LSPs)
- ✅ Improve translator productivity (20-40% gains documented)
- ✅ Consistent quality across your translator pool
- ✅ Works with your existing CAT tool infrastructure
- ✅ Open source means you own your workflow
- ✅ Custom training and consulting available

### Why Open Source?
- 🔓 **Full transparency** - See exactly what the AI is doing
- 🔓 **No vendor lock-in** - Own your translation workflow
- 🔓 **Community-driven** - Contribute features, report bugs
- 🔓 **Sustainable** - Supported through consulting and training

---

## 🚀 Features Overview

### AI Translation Engine
- **Multiple providers** - OpenAI, Anthropic, Google Gemini
- **Multimodal support** - GPT-4 Vision for figures and context
- **Batch processing** - Translate entire documents at once
- **Context preservation** - Full document analysis before translation

### Professional Prompts
- **19 System Prompts** - Domain specialists (Legal, Medical, Patent, Tech, etc.)
- **8 Custom Instructions** - User-defined preferences
- **Prompt Assistant** - Generate custom prompts from document analysis
- **Markdown format** - Human-readable, easy to edit

### Translation Memory
- **Fuzzy matching** - Find similar segments
- **Context display** - See source alongside match
- **Segment history** - Learn from previous translations
- **TMX export** - Industry-standard format

### Professional Export
- **Auto-reports** - Session reports in HTML and Markdown
- **CAT tool export** - Direct memoQ and CafeTran DOCX
- **Format preservation** - Bold, italic, formatting maintained
- **Tag safety** - XLIFF tags completely preserved

---

## 📊 Performance

- ⚡ **Grid pagination** - 10x faster loading (50 segments/page)
- ⚡ **Smart caching** - Reduce API calls with TM fuzzy matching
- ⚡ **Batch translation** - Process 100+ segments simultaneously
- ⚡ **Responsive UI** - Stays responsive during large operations

---

## 🤝 Community & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/michaelbeijer/Supervertaler/issues)
- **GitHub Discussions**: [Community chat and questions](https://github.com/michaelbeijer/Supervertaler/discussions)
- **Website**: [supervertaler.com](https://supervertaler.com)
- **Professional Website**: [michaelbeijer.co.uk](https://michaelbeijer.co.uk)

---

## 💡 Use Cases

### Individual Translators
- Enhance personal productivity with AI
- Maintain consistent terminology
- Work faster without sacrificing quality
- Leverage domain-specific prompts

### Translation Agencies
- Train all translators with same prompts
- Maintain company-wide consistency
- Increase productivity across the team
- Reduce review/QA time
- Custom LSP consulting available

### Translation Students
- Learn professional translation workflows
- Understand CAT tool integration
- Practice with real-world tools
- Open source to study and modify

---

## 🔐 Privacy & Security

- **No data collection** - Your translations stay on your computer
- **Local processing** - Translations processed locally by default
- **API keys encrypted** - Credentials stored securely
- **Open source** - Full audit trail, no hidden code
- **GDPR compliant** - User data never leaves your system

---

## 📄 License

**MIT License** - Fully open source and free

This software is provided as-is for both personal and commercial use.

---

## 👤 About

**Supervertaler** is maintained by Michael Beijer, a professional translator with 30 years of experience in technical and patent translation. The project represents a personal passion for building tools that make translators' lives easier.

- 🌐 **Website**: [michaelbeijer.co.uk](https://michaelbeijer.co.uk)
- 💼 **Professional**: [ProZ Profile](https://www.proz.com/profile/652138)
- 🔗 **LinkedIn**: [linkedin.com/in/michaelbeijer](https://www.linkedin.com/in/michaelbeijer/)

---

## 🎯 Roadmap

### Planned Features (v3.8+)
- Enhanced Prompt Assistant with auto-refinement
- Glossary management UI improvements
- Advanced TM features (penalty weights, leverage scoring)
- Integration marketplace (partner CAT tools)
- Professional cloud hosting option (optional)

### Community Contributions Welcome
We're looking for:
- 🐛 Bug reports and feature requests
- 💡 Prompt contributions (System Prompts, Custom Instructions)
- 📖 Documentation improvements
- 🌍 Translations and localization
- 🤝 Code contributions

---

## 📞 Questions?

Check out:
1. **README.md** (this file) - Overview
2. **[CHANGELOG.md](CHANGELOG.md)** - What's new
3. **[USER_GUIDE.md](USER_GUIDE.md)** - Detailed usage instructions
4. **GitHub Issues** - Common questions
5. **Website Documentation** - tutorials and guides

---

**Last Updated**: October 20, 2025  
**Version**: v3.7.1  
**Status**: Active Development  
**License**: MIT (Open Source)  
**Security Status**: Current - Security patches applied in v3.7.1

---

> 🎯 **Supervertaler**: Empowering professional translators with intelligent, context-aware AI tools. Built by translators, for translators.
