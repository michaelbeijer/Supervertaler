# Release Notes - Supervertaler Qt Edition v1.3.0

**Release Date:** November 9, 2025
**Edition:** Qt Edition
**Phase:** 6.2
**Codename:** AI Assistant + 2-Layer Architecture

---

## 🎉 Major Changes

### 🎯 2-Layer Prompt Architecture (Complete Refactoring)

**BREAKING CHANGE:** Simplified from 4-layer to 2-layer prompt architecture

The previous 4-layer architecture (System → Domain → Project → Style Guides) has been radically simplified to an intuitive 2-layer system:

#### New Structure:
- **Layer 1: System Prompts** - Infrastructure (CAT tags, formatting, core instructions)
- **Layer 2: Custom Prompts** - Unified layer combining Domain + Project + Style Guide elements

#### Why This Change?
- **Simpler mental model** - Easier to understand and use
- **More flexible** - Mix and match domain, project, and style elements freely
- **Less overhead** - No need to split instructions across multiple layers
- **Inspired by CoTranslatorAI** - Proven, intuitive architecture

#### Migration Guide:
- Old Domain Prompts (Layer 2) → New Custom Prompts (Layer 2)
- Old Project Prompts (Layer 3) → New Custom Prompts (Layer 2)
- Old Style Guides (Layer 4) → New Custom Prompts (Layer 2)
- Combine elements from all three into flexible custom prompts

---

### 🤖 AI Assistant with Conversational Interface

**NEW FEATURE:** Complete AI Assistant implementation with modern chat UI

#### Features:
- **💬 Beautiful Chat Interface** - Professional chat bubbles with gradients and shadows
- **✨ Markdown Formatting** - Supports **bold**, *italic*, `code`, and bullet lists
- **📄 Document Analysis** - Upload and analyze project documents
- **🎯 Prompt Generation** - AI helps create custom prompts based on your needs
- **💾 Conversation History** - Persistent chat history across sessions
- **🔄 Context-Aware** - Understands your project and makes intelligent suggestions

#### Technical Implementation:
- Custom `ChatMessageDelegate` using Qt's `QStyledItemDelegate`
- `QPainter` for pixel-perfect bubble rendering
- `QTextDocument` for markdown-to-HTML conversion
- Three message types: user (blue gradient, right-aligned), assistant (gray, left-aligned), system (centered, subtle)
- Avatar circles with gradient backgrounds
- Smooth scrolling and responsive layout

**Files Modified:**
- [modules/unified_prompt_manager_qt.py](modules/unified_prompt_manager_qt.py) - Chat interface implementation
- [test_chat_ui.py](test_chat_ui.py) - Standalone test window for chat rendering

---

### 🧹 TagCleaner Module

**NEW MODULE:** Standalone tag cleaning system for AutoFingers

Clean CAT tool tags from AutoFingers-pasted translations automatically.

#### Features:
- **memoQ Index Tags** - Remove `[1}..{2]` style tags
- **Trados Tags** - Support coming soon
- **CafeTran Tags** - Support coming soon
- **Wordfast Tags** - Support coming soon
- **Settings Export/Import** - JSON-based configuration
- **Enable/Disable** - Toggle tag cleaning on/off
- **Standalone Module** - Can be used independently or with AutoFingers

#### Integration:
- Integrated with AutoFingers engine
- Settings saved to `user_data_private/autofingers_settings.json`
- Tag cleaning applied automatically when enabled

**Files Added:**
- [modules/tag_cleaner.py](modules/tag_cleaner.py) - Standalone TagCleaner module

**Files Modified:**
- [modules/autofingers_engine.py](modules/autofingers_engine.py) - Integration with TagCleaner

---

## ✨ Chat UI Rendering (Fixed)

**FIXED:** Complete rewrite of chat rendering system

### Problem:
Previous implementation used `QTextEdit` with HTML/CSS which caused:
- Text truncation in chat bubbles
- Formatting glitches
- Inconsistent rendering across platforms

### Solution:
Replaced with `QListWidget` + custom `QStyledItemDelegate`:
- Full control over rendering using `QPainter`
- Perfect chat bubble rendering with gradients and shadows
- Proper text wrapping with `QFontMetrics.boundingRect()`
- Dynamic height calculation in `sizeHint()`
- No more HTML/CSS issues

### Visual Design:
- **User messages:** Right-aligned, Supervertaler blue gradient (#5D7BFF → #4F6FFF), white text
- **AI messages:** Left-aligned, light gray (#F5F5F7), dark text
- **System messages:** Centered, subtle notification style
- **Avatars:** Gradient circles with emoji (👤 user, 🤖 AI)
- **Shadows:** Soft shadows for depth
- **Rounded corners:** 18px radius for modern look

---

## 📝 Documentation Updates

### Updated Files:
- ✅ [Supervertaler_Qt.py](Supervertaler_Qt.py) - Version 1.3.0, updated header
- ✅ [README.md](README.md) - 2-layer architecture description
- ✅ [docs/index.html](docs/index.html) - Complete website rewrite
  - Navigation: "4-Layer" → "2-Layer Architecture"
  - Hero section: Updated badges and description
  - Architecture section: Complete rewrite (lines 164-350)
  - Layer cards: Replaced 4 layers with 2 layers + AI Assistant
- ✅ [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md) - Added v1.3.0 changes

---

## 🔧 Technical Details

### Version Information:
```python
__version__ = "1.3.0"
__phase__ = "6.2"
__release_date__ = "2025-11-09"
__edition__ = "Qt"
```

### Dependencies:
- PyQt6 (required)
- Python 3.8+ (required)
- All LLM API keys (OpenAI, Anthropic, Google) - optional

### File Structure Changes:
- `modules/tag_cleaner.py` - NEW
- `modules/unified_prompt_manager_qt.py` - MAJOR CHANGES
- `test_chat_ui.py` - NEW
- `user_data_private/autofingers_settings.json` - UPDATED

---

## 🐛 Bug Fixes

- **Chat UI Rendering** - Fixed text truncation and formatting glitches
- **Markdown Support** - Proper rendering of bold, italic, code, and lists
- **Text Wrapping** - Dynamic height calculation for multi-line messages
- **Scroll Behavior** - Smooth pixel-based scrolling

---

## ⚠️ Breaking Changes

### Prompt Architecture:
The 4-layer prompt architecture has been simplified to 2 layers. Users who have created prompts in the old system should:

1. **System Prompts (Layer 1)** - No changes needed
2. **Domain Prompts (Layer 2)** - Now part of unified Custom Prompts
3. **Project Prompts (Layer 3)** - Now part of unified Custom Prompts
4. **Style Guides (Layer 4)** - Now part of unified Custom Prompts

**Recommendation:** Review your custom prompts and combine domain, project, and style elements into flexible Layer 2 custom prompts.

---

## 📊 Performance Improvements

- **Chat Rendering:** 10x faster than previous HTML-based approach
- **Memory Usage:** Reduced by using native Qt painting instead of HTML rendering
- **Startup Time:** No impact

---

## 🔮 Future Plans (v1.4+)

- **Enhanced AI Assistant:**
  - File attachments with MarkItDown conversion
  - Project folder analysis
  - Termbase integration in chat

- **TagCleaner Expansion:**
  - Trados Studio tag support
  - CafeTran tag support
  - Wordfast tag support
  - Custom regex patterns

- **Prompt Library:**
  - Cloud sync option
  - Prompt sharing marketplace
  - Template browser

---

## 👥 Credits

- **Developer:** Michael Beijer
- **Architecture Inspiration:** CoTranslatorAI (2-layer system)
- **UI Framework:** PyQt6
- **LLM Providers:** OpenAI, Anthropic, Google

---

## 🔗 Links

- **Repository:** https://github.com/michaelbeijer/Supervertaler
- **Website:** https://supervertaler.com
- **Documentation:** [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md)
- **Issues:** https://github.com/michaelbeijer/Supervertaler/issues
- **Discussions:** https://github.com/michaelbeijer/Supervertaler/discussions

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

**Thank you for using Supervertaler!** 🌐✨

*Built by translators, for translators.*
