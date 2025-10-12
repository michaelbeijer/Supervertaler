# Supervertaler CLASSIC Edition - Changelog

**Version Line**: v2.x.x-CLASSIC (DOCX-based Workflow Architecture)

---

## [2.5.0-CLASSIC] - 2025-10-12 🎯 POST-TRANSLATION ANALYSIS

> **📊 Major Feature**: AI-powered Tracked Changes Analysis with configurable batch processing

### ✨ NEW FEATURES

**Tracked Changes Analysis Report** - Export AI-powered markdown reports

- **AI-Powered Change Summaries**:
  - Analyze differences between AI baseline and final edited translations
  - Batch processing (configurable 1-100 segments per API call)
  - Supports all AI providers (Claude, Gemini, OpenAI)
  - Default batch size: 25 segments (optimal speed/cost balance)
  
- **Interactive Batch Size Slider**:
  - Choose batch size from 1-100 via slider dialog
  - Real-time estimate of API calls needed
  - Example: 33 changes → 2 batches at size 25
  
- **Precision AI Prompts** (4 iterations of refinement):
  - Detects subtle changes: curly vs straight quotes (" vs ")
  - Apostrophe detection: ' vs '
  - Dash detection: - vs – vs —
  - Explicit character examples in prompts
  - "DO NOT say 'No change' unless 100% identical"
  - Quotes exact changed text: "X" → "Y"
  
- **Markdown Report Format**:
  - Clear explanation of report purpose
  - Paragraph format (not wide tables)
  - One segment per section with Source/Target/Summary
  - Includes AI configuration and full prompt template
  - Multi-line formatting for multiple changes per segment

### 🔧 GUI REORGANIZATION

**Moved Tracked Changes to New Section**:
- **Removed** from "Context Sources" section
- **Created** new "📊 Post-Translation Analysis" section
- **Clarified** purpose: post-translation review tool, NOT translation context
- **Added** explanatory label: "Load bilingual exports from CAT tools..."

**Purpose**:
- Used AFTER completing translation in CAT tools (memoQ, CafeTran)
- Analyzes how much you edited the AI-generated baseline
- Review tool for tracking translation workflow improvements

### 📊 EXPORT CAPABILITIES

**Markdown Report Includes**:
```markdown
# Tracked Changes Analysis Report

## What is this report?
[Clear explanation of purpose and use case]

**Generated:** [timestamp]
**Total Changes:** [count]
**AI Analysis:** Enabled/Disabled

### AI Analysis Configuration
**Provider:** Claude/Gemini/OpenAI
**Model:** [model-name]
**Prompt Template Used:** [full prompt shown]

---

### Segment 1
**Target (Original):** [AI-generated text]
**Target (Revised):** [Your edited text]
**Change Summary:** [AI-powered precise analysis]
```

### ⚡ PERFORMANCE

**Batch Processing**:
- **90% faster** than sequential processing
- 33 changes: ~10 seconds (batch) vs ~90 seconds (sequential)
- Configurable batch size balances speed vs token usage

### 🎯 USE CASE

1. Complete translation project in CAT tool (with tracked changes enabled)
2. Export bilingual document from memoQ/CafeTran
3. Load into Supervertaler Tracked Changes feature
4. Export markdown report with AI analysis
5. Review all your editing decisions in one comprehensive document

---

