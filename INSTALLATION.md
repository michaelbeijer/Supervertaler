==========================================================================
  SUPERVERTALER v2.4.1-CLASSIC - Installation & Quick Start Guide
==========================================================================

NOTE: As of October 10, 2025, v2.4.1 has been renamed to v2.4.1-CLASSIC
to distinguish it from the v3.0.0-beta CAT editor. The functionality is
identical - only the version naming has changed for clarity.

Thank you for downloading Supervertaler! This guide will help you get 
started with AI-powered translation.

--------------------------------------------------------------------------
SYSTEM REQUIREMENTS
--------------------------------------------------------------------------

- Windows 10 or Windows 11 (64-bit)
- Internet connection (for AI API calls)
- At least 100 MB free disk space
- Visual C++ Redistributable 2015-2022 (usually pre-installed)

--------------------------------------------------------------------------
INSTALLATION INSTRUCTIONS
--------------------------------------------------------------------------

1. EXTRACT THE ZIP FILE
   - Right-click on Supervertaler_v2.4.1_Windows.zip
   - Select "Extract All..."
   - Choose a permanent location (e.g., C:\Program Files\Supervertaler)
   - Click "Extract"

2. VERIFY FILE STRUCTURE
   After extraction, your folder should contain:
   
   Supervertaler_v2.4.1/
   ├── Supervertaler.exe          (Main application)
   ├── user data/                  (User data folder)
   │   ├── Custom_prompts/      (AI prompt templates)
   │   ├── Projects/            (Your projects folder)
   │   └── Projects_private/    (Private projects)
   ├── docs/                      (Documentation)
   ├── _internal/                 (Application files - DO NOT MODIFY)
   ├── api_keys.example.txt       (API key template)
   ├── README.md                  (Full documentation)
   └── CHANGELOG.md               (Version history)

3. FIRST RUN
   - Double-click Supervertaler.exe
   - Windows Defender may show a warning:
     → Click "More info"
     → Click "Run anyway"
   - This is normal for new executables without a code signature

--------------------------------------------------------------------------
API KEY SETUP (REQUIRED)
--------------------------------------------------------------------------

Supervertaler requires at least ONE of the following AI service API keys:

OPTION 1: Anthropic Claude (Recommended)
  - Sign up at: https://console.anthropic.com/
  - Get API key from: Settings → API Keys
  - Best models: Claude 3.5 Sonnet, Claude 3 Opus

OPTION 2: OpenAI GPT
  - Sign up at: https://platform.openai.com/
  - Get API key from: API Keys section
  - Best models: GPT-4o, GPT-4 Turbo

OPTION 3: Google Gemini
  - Sign up at: https://aistudio.google.com/
  - Get API key from: Get API Key
  - Best models: Gemini 2.0 Flash, Gemini 1.5 Pro

HOW TO ENTER API KEYS:
  1. Launch Supervertaler.exe
  2. Go to Settings tab
  3. Paste your API key(s) in the respective field(s)
  4. Click "Save API Keys"
  
  NOTE: Keys are stored locally in api_keys.txt (never shared)

--------------------------------------------------------------------------
QUICK START - BASIC TRANSLATION
--------------------------------------------------------------------------

1. SELECT AI MODEL
   - In the "Translation" tab, choose your AI model from the dropdown
   - Recommended: Claude 3.5 Sonnet (best quality/speed balance)

2. SET LANGUAGES
   - Source Language: Language you're translating FROM
   - Target Language: Language you're translating TO

3. ENTER SOURCE TEXT
   - Type or paste text in the "Source Text" box
   - Or: File → Import → [choose format]

4. TRANSLATE
   - Click the "Translate" button
   - Wait for AI to process (a few seconds)
   - Translation appears in the "Translation" box

5. SAVE YOUR WORK
   - File → Save Session (saves project state)
   - File → Export → [choose format]

--------------------------------------------------------------------------
QUICK START - CAFETRAN WORKFLOW
--------------------------------------------------------------------------

For CafeTran bilingual DOCX translation with formatting preservation:

1. EXPORT FROM CAFETRAN
   - In CafeTran: File → Export → Bilingual DOCX

2. IMPORT TO SUPERVERTALER
   - File → Import → CafeTran Bilingual DOCX
   - Select your exported file
   - Segments load automatically

3. TRANSLATE
   - Segments appear in the translation area
   - Click "Translate" to process with AI
   - Formatting markers (|pipes|) preserved automatically

4. EXPORT BACK TO CAFETRAN
   - File → Export → CafeTran Bilingual DOCX
   - Save the file
   - Import back into CafeTran - formatting intact!

See docs/features/CAFETRAN_SUPPORT.md for detailed guide

--------------------------------------------------------------------------
QUICK START - MEMOQ WORKFLOW
--------------------------------------------------------------------------

For memoQ bilingual DOCX translation with formatting preservation:

1. EXPORT FROM MEMOQ
   - In memoQ: File → Export → Bilingual DOCX

2. IMPORT TO SUPERVERTALER
   - File → Import → memoQ Bilingual DOCX
   - Select your exported file
   - Segments with formatting detected automatically

3. TRANSLATE
   - Click "Translate" to process with AI
   - Formatting applied programmatically (60% threshold rule)

4. EXPORT BACK TO MEMOQ
   - File → Export → memoQ Bilingual DOCX
   - Save the file
   - Import back into memoQ - formatting preserved!

See docs/features/MEMOQ_SUPPORT.md for detailed guide

--------------------------------------------------------------------------
SUPPORTED FILE FORMATS
--------------------------------------------------------------------------

IMPORT:
  ✓ Plain text (.txt)
  ✓ DOCX documents (.docx)
  ✓ XLIFF 1.2/2.0 (.xlf, .xliff)
  ✓ TMX translation memory (.tmx)
  ✓ TSV spreadsheet (.tsv)
  ✓ CafeTran bilingual DOCX (.docx)
  ✓ memoQ bilingual DOCX (.docx)

EXPORT:
  ✓ Plain text (.txt)
  ✓ DOCX documents (.docx)
  ✓ XLIFF 1.2/2.0 (.xlf, .xliff)
  ✓ TMX translation memory (.tmx)
  ✓ TSV spreadsheet (.tsv)
  ✓ Bilingual text (.txt)
  ✓ CafeTran bilingual DOCX (.docx)
  ✓ memoQ bilingual DOCX (.docx)

--------------------------------------------------------------------------
CUSTOM PROMPTS
--------------------------------------------------------------------------

Supervertaler includes specialized translation prompts for:

- Legal Translation
- Medical Translation
- Financial Translation
- Marketing & Creative
- Patent Translation
- Gaming & Entertainment
- Cryptocurrency & Blockchain

TO USE CUSTOM PROMPTS:
  1. Go to "Custom Prompts" tab
  2. Select a prompt from the dropdown
  3. Click "Load Selected Prompt"
  4. Translate as normal - specialized instructions applied!

TO CREATE YOUR OWN:
  1. Click "Save Current Prompt" in Custom Prompts tab
  2. Edit the JSON file in user data/Custom_prompts/ folder
  3. Reload in Supervertaler

--------------------------------------------------------------------------
PROJECT ORGANIZATION
--------------------------------------------------------------------------

FOLDERS:
  - user data/Projects/          Use for general translation projects
  - user data/Projects_private/  Use for confidential/NDA projects

SAVING SESSIONS:
  - File → Save Session → Choose location
  - Saves: source text, translation, settings, custom instructions
  - File → Load Session → Resume where you left off

--------------------------------------------------------------------------
TROUBLESHOOTING
--------------------------------------------------------------------------

PROBLEM: "API key not found" error
SOLUTION: Go to Settings tab and enter your API key, then click Save

PROBLEM: "Rate limit exceeded" error
SOLUTION: You've hit API usage limits - wait a few minutes or upgrade plan

PROBLEM: Formatting not preserved in CAT tool export
SOLUTION: Ensure you're using the correct import/export format:
          - CafeTran Bilingual DOCX for CafeTran
          - memoQ Bilingual DOCX for memoQ

PROBLEM: Application won't start
SOLUTION: 
  1. Check Windows Defender isn't blocking it
  2. Right-click Supervertaler.exe → Properties → Unblock
  3. Install Visual C++ Redistributable 2015-2022

PROBLEM: Slow translation speed
SOLUTION:
  1. Try a faster model (Claude 3.5 Haiku, Gemini 2.0 Flash)
  2. Reduce source text length
  3. Check your internet connection

--------------------------------------------------------------------------
DOCUMENTATION
--------------------------------------------------------------------------

Full documentation available in the docs/ folder:

- README.md                     - Complete user manual
- CHANGELOG.md                  - Version history
- docs/features/                - Feature-specific guides
  - CAFETRAN_SUPPORT.md         - CafeTran workflow guide
  - MEMOQ_SUPPORT.md            - memoQ workflow guide
- docs/user_guides/             - Tutorial guides

--------------------------------------------------------------------------
PRIVACY & SECURITY
--------------------------------------------------------------------------

- API keys stored locally (never transmitted except to AI services)
- No telemetry or usage tracking
- Source text sent only to your chosen AI provider
- Private projects folder for confidential work
- All data stays on your computer

--------------------------------------------------------------------------
GETTING HELP
--------------------------------------------------------------------------

GitHub Issues: https://github.com/michaelbeijer/Supervertaler/issues
Documentation: https://github.com/michaelbeijer/Supervertaler

Found a bug? Have a feature request? Please open a GitHub issue!

--------------------------------------------------------------------------
LICENSE & CREDITS
--------------------------------------------------------------------------

Supervertaler v2.4.1
Released: October 9, 2025

Developed by: Michael Beijer
GitHub: https://github.com/michaelbeijer/Supervertaler

Thank you for using Supervertaler!

==========================================================================
