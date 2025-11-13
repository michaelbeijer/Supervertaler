# LLM Leaderboard - Design Specification

## Overview

**LLM Leaderboard** is an integrated LLM benchmarking module for Supervertaler that allows users to compare translation quality, speed, and cost across multiple LLM providers and models.

## Name Rationale

**LLM Leaderboard** - Perfect name because:
- ✅ Instantly understandable (everyone knows what a leaderboard is)
- ✅ Implies competitive comparison and rankings
- ✅ Short, catchy, memorable
- ✅ Modern (matches industry terminology like LMSys Leaderboard)
- ✅ Visual concept (users expect scores, rankings, winners)

## Architecture

### Module Structure
```
modules/
  llm_leaderboard.py          # Core benchmarking logic
  superbench_ui.py             # Qt UI components
  llm_leaderboard_data.py      # Test dataset management

data/
  llm_leaderboard/
    test_sets/
      business_en_nl.json        # Business EN→NL tests
      legal_nl_en.json           # Legal NL→EN tests
      technical_en_nl.json       # Technical EN→NL tests
      custom/                    # User-added test sets
```

### Dual-Mode Operation

1. **Integrated Mode** (Tab in Supervertaler_Qt)
   - Accessible via "🏆 LLM Leaderboard" tab in main window
   - Uses existing API keys from Settings
   - Results saved to project database

2. **Standalone Mode** (Independent launcher)
   - `python -m modules.superbench_ui`
   - Can be used independently of main app
   - Own configuration management

## Features

### Phase 1: Core Functionality ⭐ (MVP)

**Test Dataset Management:**
- Pre-loaded test sets (business, legal, technical, marketing)
- CSV import for custom test sets
- Test set builder (add individual source/reference pairs)
- Format: source text, reference translation, domain, direction (EN→NL or NL→EN)

**Model Selection:**
- Checkboxes for each provider (OpenAI, Claude, Gemini)
- Dropdown for specific model per provider
- Enable/disable individual models
- Uses API keys from main Settings

**Benchmark Execution:**
- "Run Benchmark" button
- Progress bar with segment count
- Real-time updates as translations complete
- Cancel button for long-running tests

**Results Display:**
- **Comparison Table** with columns:
  - Source text (truncated to 100 chars)
  - Reference translation
  - Model 1 output
  - Model 2 output
  - Model 3 output
  - Speed (ms per segment)
  - Quality score (chrF++)
- **Summary Panel**:
  - Average speed per model
  - Average quality score per model
  - Total cost estimate (based on token usage)
  - Winner badges (🥇🥈🥉) for best speed, quality, value

**Export:**
- Export to Excel (detailed results + summary)
- Export to CSV
- Copy results to clipboard

### Phase 2: Advanced Features 🚀

**Quality Metrics:**
- chrF++ score (character-level F-score)
- BLEU score (optional)
- Human evaluation integration (thumbs up/down per translation)

**Cost Analysis:**
- Token counting per translation
- Cost calculation per model
- Total cost projection for large projects
- Cost per segment comparison

**Visualization:**
- Speed vs Quality scatter plot
- Cost vs Quality comparison chart
- Bar charts for average metrics

**Test Set Management:**
- Create custom test sets from current project segments
- "Add to Arena" button in main segment view
- Tag-based test set organization
- Domain-specific test sets

### Phase 3: Pro Features 💎

**Historical Tracking:**
- Save benchmark results to database
- Compare model performance over time
- Track API cost trends
- Model performance regression alerts

**Batch Testing:**
- Run multiple test sets at once
- Schedule regular benchmarks
- Email reports

**Collaborative Features:**
- Share test sets with team
- Compare results across different users
- Team leaderboards

## UI Layout

### Tab Structure in Main Window

```
┌─────────────────────────────────────────────────────────────┐
│ [Project] [Segments] [Resources] [🏆 LLM Leaderboard] [Help] │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐  ┌────────────────────────────────┐   │
│  │ Test Set        │  │ Model Selection                 │   │
│  │ ▼ Business EN→NL│  │ ☑ OpenAI: [gpt-4o ▼]          │   │
│  │                 │  │ ☑ Claude: [Sonnet 4.5 ▼]      │   │
│  │ Load: 30 tests  │  │ ☑ Gemini: [2.5 Flash ▼]       │   │
│  │                 │  │                                 │   │
│  │ [Import CSV]    │  │ [Run Benchmark]                 │   │
│  │ [Create Custom] │  │                                 │   │
│  └─────────────────┘  └────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Results                                    [Export ▼]    │ │
│  ├─────────────────────────────────────────────────────────┤ │
│  │ Source          │ GPT-4o    │ Sonnet 4.5│ Gemini 2.5   │ │
│  │─────────────────┼───────────┼───────────┼──────────────│ │
│  │ The contract... │ Het contr.│ Het contr.│ Het contract.│ │
│  │ Speed:          │ 850ms     │ 920ms     │ 780ms        │ │
│  │ Quality:        │ 89.5      │ 91.2 🥇   │ 88.7         │ │
│  │─────────────────┼───────────┼───────────┼──────────────│ │
│  │ Please note...  │ Let op... │ Graag no..│ Noteer...    │ │
│  │ Speed:          │ 720ms 🥇  │ 890ms     │ 810ms        │ │
│  │ Quality:        │ 85.3      │ 87.9      │ 86.1         │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Summary                                                  │ │
│  ├─────────────────────────────────────────────────────────┤ │
│  │ Model          │ Avg Speed │ Avg Quality │ Est. Cost   │ │
│  │────────────────┼───────────┼─────────────┼─────────────│ │
│  │ GPT-4o         │ 785ms 🥇  │ 87.4        │ $0.023      │ │
│  │ Sonnet 4.5     │ 905ms     │ 89.6 🥇     │ $0.031      │ │
│  │ Gemini 2.5     │ 795ms     │ 87.4        │ $0.015 🥇   │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Integration Points

### With Existing Supervertaler Components

1. **API Keys**: Uses keys from main Settings (no separate config)
2. **LLM Clients**: Leverages existing `modules/llm_clients.py`
3. **Database**: Stores benchmark history in main SQLite database
4. **Projects**: Can create test sets from current project segments
5. **Segments**: "Test in Arena" button in segment context menu

### Data Flow

```
User selects test set
    ↓
User selects models (checkboxes)
    ↓
Click "Run Benchmark"
    ↓
For each test in test set:
    For each enabled model:
        - Send translation request
        - Measure response time
        - Calculate quality score (chrF++)
        - Estimate cost (token count × pricing)
    ↓
Display results in table
    ↓
Generate summary statistics
    ↓
Optional: Export to Excel/CSV
```

## Implementation Plan

### Phase 1: MVP (Immediate)
1. Create `modules/translation_arena.py` with core logic
2. Create simple Qt UI with basic comparison table
3. Add 3-5 pre-loaded test sets (10 segments each)
4. Implement chrF++ quality scoring
5. Add "TranslationArena" tab to main window
6. Basic Excel export

**Timeline**: 2-3 hours

### Phase 2: Polish (Soon)
1. Enhanced UI with summary panel
2. Speed/Quality/Cost visualization
3. CSV import for custom test sets
4. Historical tracking in database
5. Cost estimation per model

**Timeline**: 3-4 hours

### Phase 3: Advanced (Future)
1. Create test sets from project segments
2. Scheduled benchmarking
3. Advanced visualizations
4. Team collaboration features

**Timeline**: Future releases

## Test Set Format

### JSON Structure
```json
{
  "name": "Business EN→NL",
  "description": "Business correspondence and documents",
  "direction": "EN→NL",
  "domain": "business",
  "tests": [
    {
      "id": 1,
      "source": "We are pleased to inform you that your order has been processed.",
      "reference": "Wij zijn verheugd u te kunnen mededelen dat uw bestelling is verwerkt.",
      "context": "formal business email"
    },
    {
      "id": 2,
      "source": "Please find attached the invoice for your recent purchase.",
      "reference": "In de bijlage treft u de factuur aan voor uw recente aankoop.",
      "context": "business correspondence"
    }
  ]
}
```

### CSV Format
```csv
id,source,reference,domain,direction,context
1,"We are pleased...","Wij zijn verheugd...","business","EN→NL","formal email"
2,"Please find attached...","In de bijlage...","business","EN→NL","correspondence"
```

## Pre-loaded Test Sets

### 1. Business EN→NL (15 segments)
- Formal business correspondence
- Emails, reports, presentations
- Mix of short and long segments

### 2. Legal NL→EN (15 segments)
- Contracts, terms & conditions
- Legal terminology
- Complex sentence structures

### 3. Technical EN→NL (15 segments)
- User manuals, technical specs
- IT/software documentation
- Specialized terminology

### 4. Marketing NL→EN (15 segments)
- Creative copy, taglines
- Product descriptions
- Persuasive language

### 5. General Mixed (20 segments)
- Various domains and directions
- Diverse text types
- Good for general comparison

## Quality Metrics

### chrF++ (Primary Metric)
- Character-level F-score
- Better for morphologically rich languages (like Dutch)
- Range: 0-100 (higher is better)
- Correlates well with human judgment
- Library: `sacrebleu`

### Speed Metric
- Time from API request to response
- Measured in milliseconds
- Average across all segments
- Excludes network latency where possible

### Cost Metric
- Estimated based on token count × published pricing
- Input tokens + output tokens
- Pricing data from `CLAUDE_MODELS` dict and similar

## User Workflows

### Workflow 1: Quick Model Comparison
1. User opens TranslationArena tab
2. Selects "Business EN→NL" test set (pre-loaded)
3. Checks all three providers (GPT-4o, Sonnet 4.5, Gemini 2.5)
4. Clicks "Run Benchmark"
5. Waits 30-60 seconds for completion
6. Reviews comparison table
7. Sees winner: Sonnet 4.5 (best quality), GPT-4o (fastest), Gemini (cheapest)
8. Decides to use Sonnet 4.5 for important project

### Workflow 2: Custom Test Set
1. User working on legal translation project
2. Selects 10 challenging segments from current project
3. Right-click → "Add to TranslationArena Test Set"
4. Names it "Legal NL→EN - Contract Terms"
5. Adds reference translations manually
6. Runs benchmark with Claude Opus 4.1 vs Sonnet 4.5
7. Discovers Opus 4.1 handles complex legal terminology better
8. Switches to Opus for this project

### Workflow 3: Historical Tracking
1. User runs monthly benchmark with same test set
2. Tracks quality improvement as models update
3. Notices GPT-4o improved from 85 → 89 chrF++ over 3 months
4. Exports trend chart for team report

## Benefits

### For Translators:
- ✅ Choose best model for specific project types
- ✅ Justify model selection to clients
- ✅ Optimize cost vs quality tradeoff
- ✅ Discover which models handle domain-specific terminology best

### For Agencies:
- ✅ Benchmark models before committing to large projects
- ✅ Track model performance over time
- ✅ Cost analysis for budget planning
- ✅ Quality assurance for LLM-assisted translation

### For Supervertaler:
- ✅ Professional feature that sets it apart
- ✅ Data-driven model selection
- ✅ Builds trust in LLM translation quality
- ✅ Educational tool for understanding model differences

## Technical Considerations

### Performance:
- Run translations in parallel where possible (ThreadPoolExecutor)
- Batch API requests to reduce overhead
- Cache results to avoid re-running identical tests
- Progress bar with real-time updates

### Error Handling:
- Handle API rate limits gracefully
- Retry failed requests (with backoff)
- Continue benchmark even if one model fails
- Display error messages in results table

### Storage:
- SQLite table: `llm_leaderboard_results`
- Columns: test_set_name, model, segment_id, source, output, speed_ms, quality_score, cost_estimate, timestamp
- Index on timestamp for historical queries

## Future Enhancements

1. **Live Arena Mode**: Real-time translation comparison as you type
2. **Human Evaluation**: Add thumbs up/down to each translation
3. **Model Voting**: Community-driven quality rankings
4. **A/B Testing**: Present translations blind, user picks winner
5. **Multi-Language**: Support language pairs beyond EN↔NL
6. **Terminology Consistency**: Track term translation across segments
7. **API Integration**: Export results to Google Sheets/Excel Online
8. **Team Dashboard**: Centralized benchmark results for translation teams

---

## Next Steps

1. ✅ Review design document
2. Implement Phase 1 MVP
3. Create pre-loaded test sets
4. Integrate into main Supervertaler_Qt window
5. User testing and feedback
6. Iterate on Phase 2 features

**Goal**: Professional, data-driven LLM benchmarking tool integrated seamlessly into Supervertaler workflow.
