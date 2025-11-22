==========================================================================
  SUPERVERTALER v1.7.8 - Installation Guide
==========================================================================

**Current Version:** v1.7.8 (November 22, 2025)  
**Framework:** PyQt6  
**Last Updated:** November 22, 2025

Welcome to Supervertaler! This guide will help you install and run the 
ultimate AI-powered companion tool for professional translators.

**What is Supervertaler?**
A professional CAT tool companion that works alongside memoQ, Trados, 
and CafeTran, featuring AI Assistant, project termbases, translation 
memory, voice dictation, and powerful prompt management.

--------------------------------------------------------------------------
SYSTEM REQUIREMENTS
--------------------------------------------------------------------------

**Operating System:**
- Windows 10/11 (64-bit) - Primary platform
- macOS 10.13+ - Compatible
- Linux (any recent distribution) - Compatible

**Software:**
- Python 3.8+ (Python 3.12 recommended)
- Internet connection (for AI API calls)

**Hardware:**
- RAM: 4GB minimum, 8GB recommended
- Disk: ~500 MB (application + dependencies)
- Optional: Microphone (for Supervoice voice dictation feature)

**API Keys Required:**
At least ONE of: OpenAI (GPT-4), Anthropic (Claude), or Google (Gemini)

--------------------------------------------------------------------------
INSTALLATION METHOD 1: RUN FROM SOURCE (RECOMMENDED)
--------------------------------------------------------------------------

This is the primary method for v1.7.8. No executable build required.

**Step 1: Install Python**
- Download Python 3.12 from python.org
- During installation, CHECK "Add Python to PATH"
- Verify: Open terminal and run `python --version`

**Step 2: Download Supervertaler**
- Visit: https://github.com/michaelbeijer/Supervertaler
- Click green "Code" button → "Download ZIP"
- Extract to your preferred location (e.g., C:\Dev\Supervertaler)

**Step 3: Install Dependencies**
Open terminal in Supervertaler folder and run:
```bash
pip install -r requirements.txt
```

This installs:
- PyQt6 (GUI framework)
- openai, anthropic, google-generativeai (AI providers)
- python-docx (DOCX support)
- openai-whisper (voice dictation)
- Additional dependencies

**Step 4: Setup API Keys**
1. Copy `api_keys.example.txt` → `api_keys.txt`
2. Edit `api_keys.txt` and add your keys:
   ```
   OPENAI_API_KEY=sk-...your-key-here...
   ANTHROPIC_API_KEY=sk-ant-...your-key-here...
   GOOGLE_API_KEY=AI...your-key-here...
   ```
3. Save the file

**Step 5: Launch Supervertaler**
```bash
python Supervertaler.py
```

Or on Windows, double-click `run.bat`

**Project Structure:**
After installation, your folder structure:
```
Supervertaler/
├── Supervertaler.py           (Main application - 21,600+ lines)
├── requirements.txt           (Python dependencies)
├── run.bat                    (Windows launcher)
├── api_keys.txt              (Your API keys - keep private!)
├── api_keys.example.txt      (Template)
├── modules/                  (Core modules)
│   ├── ai_assistant.py
│   ├── database_manager.py
│   ├── prompt_manager_qt.py
│   ├── termbase_manager.py
│   └── ... (50+ modules)
├── user_data/               (User data - auto-created)
│   ├── Prompt_Library/      (Your prompts)
│   ├── projects/            (Translation projects)
│   ├── termbases/          (Terminology databases)
│   └── translation_memories/ (TM databases)
├── docs/                    (Documentation)
├── legacy_versions/         (Historical versions)
└── tests/                   (Unit tests)
```

--------------------------------------------------------------------------
API KEY SETUP (REQUIRED FOR AI FEATURES)
--------------------------------------------------------------------------

Supervertaler requires at least ONE AI service API key:

**OPTION 1: Anthropic Claude (Highly Recommended)**
- Sign up: https://console.anthropic.com/
- Navigate to: Settings → API Keys → Create Key
- Best models: Claude 3.5 Sonnet (best quality), Claude 3.5 Haiku (fastest)
- Pricing: Pay-as-you-go, very affordable
- Key format: `sk-ant-api03-...`

**OPTION 2: OpenAI GPT**
- Sign up: https://platform.openai.com/
- Navigate to: API Keys section → Create new secret key
- Best models: GPT-4o (recommended), GPT-4 Turbo, o1-preview
- Pricing: Pay-as-you-go
- Key format: `sk-proj-...` or `sk-...`

**OPTION 3: Google Gemini**
- Sign up: https://aistudio.google.com/
- Click: "Get API Key"
- Best models: Gemini 2.0 Flash (fast & free), Gemini 1.5 Pro
- Pricing: Generous free tier!
- Key format: `AIza...`

**TWO WAYS TO ENTER API KEYS:**

**Method A: api_keys.txt file (Recommended)**
1. Edit `api_keys.txt` in Supervertaler folder
2. Add your keys (one per line):
   ```
   OPENAI_API_KEY=sk-proj-your-key-here
   ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
   GOOGLE_API_KEY=AIza-your-key-here
   ```
3. Save file and launch Supervertaler

**Method B: In-App Settings**
1. Launch Supervertaler: `python Supervertaler.py`
2. Go to: Settings → AI Providers
3. Paste your key(s) in the respective field(s)
4. Click "Save Settings"

**SECURITY:**
- Keys stored locally in `api_keys.txt` (never transmitted except to AI services)
- Add `api_keys.txt` to `.gitignore` if using version control
- Never share your API keys publicly

--------------------------------------------------------------------------
QUICK START - YOUR FIRST PROJECT
--------------------------------------------------------------------------

**1. Launch Supervertaler**
```bash
python Supervertaler.py
```

**2. Create New Project**
- Click: File → New Project
- Enter project name (e.g., "My First Translation")
- Set source language (e.g., English)
- Set target language (e.g., Dutch)
- Click "Create"

**3. Import Document**
Choose your format:
- **Monolingual DOCX:** File → Import DOCX (for plain Word documents)
- **memoQ Bilingual:** File → Import memoQ bilingual document
- **Manual Entry:** Type directly in the grid

**4. Translate with AI**
- Select a segment (row) in the grid
- View AI suggestions in the Translation Results panel (right side)
- Press Ctrl+1 to insert first match
- Or type/edit translation manually
- Press Ctrl+Enter to confirm segment

**5. Review & Edit**
- Use Grid View (default) for segment-by-segment editing
- Use Document View for natural reading flow
- Use List View for overview with filters

**6. Export**
- File → Save Project (saves .json project file)
- File → Export → Choose format:
  - Monolingual DOCX
  - memoQ bilingual DOCX
  - TMX (translation memory)
  - Plain text

--------------------------------------------------------------------------
CAT TOOL INTEGRATION
--------------------------------------------------------------------------

**memoQ Round-Trip Workflow:**
1. Export from memoQ: File → Export → Bilingual DOCX
2. Import to Supervertaler: File → Import memoQ bilingual document
3. Translate segments with AI assistance
4. Export: File → Export memoQ bilingual document
5. Import back to memoQ - formatting preserved!

**CafeTran Integration:**
Via DOCX bilingual table format (experimental support)

**Trados Studio:**
Via XLIFF 1.2/2.0 files (bilingual format)

**Key Benefits:**
- Use AI translation while preserving CAT tool formatting
- Access termbase and TM matches alongside AI suggestions
- Benefit from Supervertaler's prompt management
- Return to your CAT tool with translations intact

--------------------------------------------------------------------------
KEY FEATURES (v1.7.8)
--------------------------------------------------------------------------

**🔍 Filter Highlighting (NEW in v1.7.8)**
- Search terms in source/target filters highlighted in yellow
- Case-insensitive matching
- Multiple matches per cell

**🎯 Termbase Display Customization (v1.7.7)**
- Sort termbase matches: appearance order, alphabetical, or by length
- Hide shorter matches contained in longer terms
- Configurable in Settings

**📚 Project Termbases (v1.7.0)**
- Dedicated project-specific termbase per project
- Automatic term extraction from source segments
- Pink highlighting for project terms vs blue for background termbases

**💾 Auto-Backup System (v1.7.6)**
- Automatic project.json backups at configurable intervals
- Prevents data loss during translation work

**🤖 AI Assistant**
- Conversational interface for prompt generation
- Analyze documents and generate custom translation prompts
- File attachments (PDF, DOCX, TXT, MD)

**🎤 Supervoice Voice Dictation**
- AI-powered speech recognition via OpenAI Whisper
- 100+ language support
- F9 global hotkey (press-to-start/stop)
- 5 model sizes (tiny to large)

**💾 Translation Memory**
- SQLite-based TM with FTS5 full-text search
- Fuzzy matching with visual diff
- TMX import/export
- Auto-propagation of exact matches

**📊 Superbench**
- Benchmark LLM translation quality on YOUR projects
- chrF++ scoring with adaptive segment sampling
- Compare GPT-4o, Claude, Gemini side-by-side

**🔍 Universal Lookup**
- System-wide TM search with Ctrl+Alt+L hotkey
- Works in any application
- Instant terminology lookup

**📝 TMX Editor**
- Professional database-backed TMX editor
- Handle massive 1GB+ files
- Filter, search, edit entries

--------------------------------------------------------------------------
UNIFIED PROMPT LIBRARY (v1.3.0+)
--------------------------------------------------------------------------

Supervertaler features a powerful 2-layer prompt architecture:

**Layer 1: System Templates**
- Core translation philosophy and infrastructure
- CAT tag handling, formatting rules
- Accessed via Settings → System Templates

**Layer 2: Custom Prompts (Unified Library)**
- Domain expertise (Legal, Medical, Financial, Technical, etc.)
- Project-specific instructions
- Style guides
- **38+ built-in prompts** in organized folders

**Using Prompts:**
1. Go to: Prompt Manager tab
2. Browse folders in left panel
3. Select prompt → Right-click → "Set as Primary" or "Attach"
4. Multi-attach: Combine multiple prompts (e.g., Legal + Client style)
5. Translate normally - prompts automatically applied

**Creating Custom Prompts:**
1. Prompt Manager → "New Prompt" button
2. Enter name, select folder
3. Write prompt content (markdown supported)
4. Save → Available immediately in library

**Favorites:**
- Star frequently-used prompts
- Access via Favorites filter

**AI Assistant Integration:**
- Ask AI to analyze your document
- Generates custom prompts automatically
- One-click save to library

--------------------------------------------------------------------------
TROUBLESHOOTING
--------------------------------------------------------------------------

**PROBLEM: "ModuleNotFoundError" when launching**
SOLUTION: 
```bash
pip install -r requirements.txt
```
Ensures all dependencies are installed.

**PROBLEM: "API key not found" error**
SOLUTION: 
1. Check `api_keys.txt` exists in Supervertaler folder
2. Verify key format: `OPENAI_API_KEY=sk-...` (no spaces, no quotes)
3. Or enter keys via Settings → AI Providers

**PROBLEM: "Rate limit exceeded" error**
SOLUTION: 
- You've hit API usage limits
- Wait a few minutes or upgrade your plan
- Switch to a different provider temporarily

**PROBLEM: PyQt6 installation fails**
SOLUTION:
```bash
pip install --upgrade pip
pip install PyQt6
```
On Linux, may need: `sudo apt-get install python3-pyqt6`

**PROBLEM: Whisper (voice dictation) not working**
SOLUTION:
1. Ensure FFmpeg is installed: `ffmpeg -version`
2. Install Whisper: `pip install openai-whisper`
3. Check microphone permissions in OS settings

**PROBLEM: Application crashes on startup**
SOLUTION:
1. Delete `user_data/ui_preferences.json` (resets UI settings)
2. Check Python version: `python --version` (need 3.8+)
3. Update PyQt6: `pip install --upgrade PyQt6`

**PROBLEM: Translation results not showing**
SOLUTION:
1. Verify API key is correct
2. Check internet connection
3. Try different AI provider
4. Check Settings → TM/Termbase Options → "Enable matching" is checked

**PROBLEM: Filter highlighting not visible**
SOLUTION:
1. Ensure you're on v1.7.8+
2. Type search term in "Filter Source" or "Filter Target" box
3. Press Enter to apply filter
4. Matching terms highlighted in yellow in visible segments

--------------------------------------------------------------------------
KEYBOARD SHORTCUTS
--------------------------------------------------------------------------

**General:**
- Ctrl+S - Save project
- Ctrl+N - New project
- Ctrl+O - Open project
- Ctrl+Q - Quit application
- Ctrl++ - Increase font size
- Ctrl+- - Decrease font size

**Grid Navigation:**
- Tab - Move from source to target cell
- Enter - Confirm segment and move to next
- Ctrl+Enter - Confirm segment (stay on current row)
- Ctrl+Up/Down - Navigate between segments
- Ctrl+A - Select all segments

**Translation Results:**
- Ctrl+1-9 - Insert match #1-9
- Ctrl+Space - Insert selected match
- Ctrl+Up/Down - Navigate between matches

**Voice Dictation:**
- F9 - Start/stop recording (global hotkey)

**Universal Lookup:**
- Ctrl+Alt+L - Open lookup window (works in any app)

**Segment Status:**
- Ctrl+T - Mark as Translated
- Ctrl+K - Mark as Confirmed
- Ctrl+R - Reset status to Not Started

--------------------------------------------------------------------------
DOCUMENTATION & RESOURCES
--------------------------------------------------------------------------

**Essential Reading:**
- [README.md](../../README.md) - Project overview
- [CHANGELOG.md](../../CHANGELOG.md) - Complete version history
- [PROJECT_CONTEXT.md](../PROJECT_CONTEXT.md) - Technical reference

**Feature Guides:**
- [AI_ASSISTANT_GUIDE.md](../AI_ASSISTANT_GUIDE.md) - AI Assistant usage
- [UNIFIED_PROMPT_LIBRARY_GUIDE.md](../UNIFIED_PROMPT_LIBRARY_GUIDE.md) - Prompt management
- [VOICE_DICTATION_GUIDE.md](../VOICE_DICTATION_GUIDE.md) - Supervoice setup
- [SUPERBROWSER_GUIDE.md](../SUPERBROWSER_GUIDE.md) - Multi-chat browser

**Online Resources:**
- Website: https://supervertaler.com
- GitHub: https://github.com/michaelbeijer/Supervertaler
- Discussions: https://github.com/michaelbeijer/Supervertaler/discussions
- Issues: https://github.com/michaelbeijer/Supervertaler/issues

--------------------------------------------------------------------------
PRIVACY & SECURITY
--------------------------------------------------------------------------

**Local-First Design:**
- All data stored locally on your computer
- No telemetry or usage tracking
- No account registration required

**API Key Security:**
- Keys stored in local `api_keys.txt` file
- Never transmitted except to your chosen AI provider
- Excluded from git via .gitignore

**Data Privacy:**
- Source text sent only to AI provider you select
- Projects stored in `user_data/projects/` folder
- Use `user_data_private/` for confidential/NDA projects
- All TMs and termbases local SQLite databases

**Open Source:**
- Full source code available on GitHub
- Audit the code yourself
- MIT License - free for commercial use

--------------------------------------------------------------------------
GETTING HELP
--------------------------------------------------------------------------

**Community Support:**
- GitHub Discussions: Ask questions, share workflows
  https://github.com/michaelbeijer/Supervertaler/discussions

**Bug Reports:**
- GitHub Issues: Report bugs or request features
  https://github.com/michaelbeijer/Supervertaler/issues

**Documentation:**
- Website: https://supervertaler.com
- GitHub: Full docs in docs/ folder

--------------------------------------------------------------------------
WHAT'S NEXT?
--------------------------------------------------------------------------

Now that you're installed:

1. **Create your first project** - File → New Project
2. **Import a document** - Try with a small DOCX or bilingual file
3. **Explore the Prompt Library** - See 38+ built-in prompts
4. **Try AI Assistant** - Let it analyze your document
5. **Setup voice dictation** - Configure Supervoice (Settings → Supervoice)
6. **Create a termbase** - Add terminology in Termbases tab
7. **Join GitHub Discussions** - Share your experience!

--------------------------------------------------------------------------
LICENSE & CREDITS
--------------------------------------------------------------------------

**Supervertaler v1.7.8**
Released: November 22, 2025
Framework: PyQt6
License: MIT

Created by: Michael Beijer
Website: https://michaelbeijer.co.uk
GitHub: https://github.com/michaelbeijer

With assistance from: Claude AI (Anthropic)

**Thank you for using Supervertaler!**

Developed by: Michael Beijer
GitHub: https://github.com/michaelbeijer/Supervertaler

Thank you for using Supervertaler!

==========================================================================
