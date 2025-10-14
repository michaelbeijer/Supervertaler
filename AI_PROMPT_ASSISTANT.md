# AI-Powered Prompt Editor with Edit-Based Learning

## Overview

A unique feature that would set Supervertaler apart from all other CAT tools: an **integrated AI assistant** that helps users refine their translation prompts through natural conversation and learns from their actual translation edits to suggest improvements automatically.

## Vision

Transform the Prompt Library from a simple prompt selector into an **intelligent, interactive workspace** where users can:

1. **Chat with an AI** about their prompts
2. **Request modifications** in natural language
3. **See AI-suggested improvements** based on their actual translation work
4. **Review changes** with visual diffs before applying
5. **Evolve prompts** over time based on real usage patterns

## Core Concept

```
┌─────────────────────────────────────────────────────────────────────┐
│ 🎯 Prompt Library                                                   │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─────────────────┐  ┌──────────────────────────────────────────┐  │
│ │ Prompt List     │  │ Prompt Editor + AI Assistant             │  │
│ │                 │  │ ┌──────────────────────────────────────┐ │  │
│ │ ✓ Patent Trans  │  │ │ Patent Translation Specialist        │ │  │
│ │   Medical Trans │  │ │ [Prompt content...]                  │ │  │
│ │   Legal Trans   │  │ │                                      │ │  │
│ │   Localization  │  │ └──────────────────────────────────────┘ │  │
│ │   ...           │  │                                          │  │
│ │                 │  │ 💬 AI Prompt Assistant                   │  │
│ │ [Task Type]     │  │ ┌──────────────────────────────────────┐ │  │
│ │ [Domain]        │  │ │ 👤 User: Add emphasis on chemical    │ │  │
│ │ [Apply] [New]   │  │ │     nomenclature precision           │ │  │
│ └─────────────────┘  │ │                                      │ │  │
│                      │ │ 🤖 AI: I'll modify the Patent prompt │ │  │
│                      │ │     to include specific guidance on  │ │  │
│                      │ │     IUPAC naming conventions...      │ │  │
│                      │ │                                      │ │  │
│                      │ │     [📊 Show Diff] [✓ Apply] [✗ Discard] │ │  │
│                      │ └──────────────────────────────────────┘ │  │
│                      └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## User Scenarios

### Scenario 1: Manual Prompt Refinement
**User:** "Please modify the 'Patent Translation Specialist' prompt to add more emphasis on chemical nomenclature precision"

**AI:** 
1. Analyzes current prompt structure
2. Identifies relevant sections (technical terminology, special attention)
3. Generates specific additions about IUPAC naming, molecular formulas, CAS numbers
4. Shows visual diff with additions highlighted
5. Explains rationale for changes
6. User reviews and applies or discards

### Scenario 2: Edit-Based Learning (The Game Changer!)
**System:** Tracks user's edits during translation project:
- Changed "organization" → "organisation" (UK spelling) 52 times
- Changed "analyze" → "analyse" 34 times
- Changed "license" → "licence" (noun form) 18 times
- Consistently used sentence case for headings

**AI:** "I've noticed you consistently prefer UK English spelling in this project. Would you like me to:
1. Update the active prompt to explicitly specify UK English preferences?
2. Create a new 'UK English Localization' custom instruction?
3. Show me the patterns you detected first?"

**User:** "Yes, update the prompt and show me what you learned"

**AI:**
1. Shows aggregated patterns with frequency counts
2. Proposes specific prompt modifications
3. Displays before/after diff
4. User approves → Prompt updated with learned preferences

### Scenario 3: Project-Specific Adaptation
After completing a medical translation project, user asks:

**User:** "What did you learn from my edits in this project that could improve the Medical Translation prompt?"

**AI:** Analyzes 500+ edits and identifies:
- User prefers "patient" over "individual" (87% of time)
- Consistently adds "clinical" before "guidelines"
- Prefers passive voice for procedures
- Uses specific UK medical terminology

Suggests creating a specialized "UK Medical Translation" prompt variant incorporating these preferences.

## Development Phases

### Phase 1: Foundation - Single Prompt Library Tab ✅ (CURRENT)
**Timeline:** This session
**Effort:** 2-3 hours

**Goals:**
- ✅ Consolidate System Prompts and Custom Instructions into one unified tab
- ✅ Integrate existing Task Type and Type filters
- ✅ Show active prompt prominently
- ✅ Streamline UI - one location for all prompt operations

**Deliverables:**
- Single "Prompt Library" tab in assistant panel
- Type filter (System prompts / Custom instructions / All)
- Task Type filter (Translation / Localization / Transcreation / etc.)
- Quick actions: Apply, Edit, New, Import, Export
- Active prompt indicator

---

### Phase 2: AI Prompt Assistant - Basic Chat Interface 🎯 (MEDIUM TERM)
**Timeline:** 2-4 weeks
**Effort:** 15-20 hours

**Goals:**
- Add chat interface to Prompt Library tab
- Implement conversational prompt modification
- Visual diff display for proposed changes
- Apply/discard workflow

**Technical Components:**
1. **Chat UI** (3-4 hours)
   - Scrollable message history
   - User input field
   - Message bubbles (user/AI)
   - Markdown rendering for AI responses

2. **AI Modification Engine** (6-8 hours)
   - Prompt analysis system
   - LLM-based modification generator
   - Context-aware suggestions
   - Structured prompt understanding

3. **Diff Visualization** (4-6 hours)
   - Side-by-side or inline diff view
   - Syntax highlighting for prompt sections
   - Selective change application
   - Revert capability

4. **Integration** (2-3 hours)
   - Connect to existing LLM clients
   - File I/O for prompt updates
   - State management
   - Error handling

**Example Interactions:**
```
User: "Add examples for financial terminology to the Financial Translation prompt"
AI: [Analyzes prompt] "I'll add examples in the 'Special attention to' section..."
     [Shows diff with 5 new examples about IFRS, Basel III, derivatives]
     [Apply] [Modify] [Discard]

User: "Make this prompt more concise"
AI: [Analyzes verbosity] "I can reduce by ~30% while maintaining key guidance..."
     [Shows trimmed version with redundancies removed]

User: "Explain this section to me"
AI: "The 'Technical Precision' section ensures that numerical values, chemical 
     formulas, and measurements are preserved exactly..."
```

**Deliverables:**
- Chat interface in Prompt Library
- AI-powered prompt modification
- Diff viewer with apply/discard
- Conversation history per prompt
- Help/examples for common commands

---

### Phase 3: Edit-Based Learning System 🚀 (LONG TERM)
**Timeline:** 2-3 months (iterative development)
**Effort:** 30-40 hours

**Goals:**
- Track all user edits during translation
- Identify patterns and preferences
- Suggest prompt improvements automatically
- Create "learned" prompt variants

**Technical Components:**

1. **Edit Tracking Infrastructure** (8-10 hours)
   ```python
   class EditTracker:
       """Track every edit in real-time"""
       
       def track_edit(self, segment_id, original_text, edited_text, context):
           """Record edit with metadata"""
           
       def categorize_edit(self, original, edited):
           """Classify: terminology, style, formatting, correction, etc."""
           
       def calculate_edit_distance(self, original, edited):
           """Measure magnitude of change"""
   ```

2. **Pattern Analysis Engine** (10-12 hours)
   ```python
   class PatternAnalyzer:
       """Find meaningful patterns in edit history"""
       
       def analyze_terminology_changes(self, edits):
           """Detect consistent word replacements"""
           # Example: "color" → "colour" (52 occurrences)
           
       def detect_style_preferences(self, edits):
           """Identify stylistic patterns"""
           # Example: Always adds "please" to imperatives
           
       def find_formatting_rules(self, edits):
           """Discover formatting preferences"""
           # Example: Sentence case for headings
           
       def identify_domain_terminology(self, edits):
           """Build domain-specific vocabulary from actual usage"""
   ```

3. **Learning Integration** (8-10 hours)
   - Statistical significance testing (avoid over-fitting to noise)
   - Confidence scoring for patterns
   - Minimum threshold for pattern recognition (e.g., 5+ occurrences)
   - Pattern aggregation across projects
   - User preference persistence

4. **AI Suggestion Generator** (6-8 hours)
   ```python
   class PromptLearner:
       """Generate prompt improvements from patterns"""
       
       def suggest_improvements(self, patterns, current_prompt):
           """Use LLM to craft appropriate prompt modifications"""
           
       def create_custom_variant(self, base_prompt, learned_patterns):
           """Generate specialized prompt version"""
           
       def explain_learnings(self, patterns):
           """Provide human-readable explanation of discoveries"""
   ```

**Example Learning Scenarios:**

**Scenario A: UK English Preference Detection**
```
Detected patterns (confidence: 95%):
- "organize" → "organise" (34 times)
- "color" → "colour" (28 times)  
- "analyze" → "analyse" (22 times)
- "license" → "licence" (15 times, noun context)

AI Suggestion:
"I've detected consistent UK English spelling preferences. 
 Shall I update your Medical Translation prompt to specify:
 - Use -ise endings (not -ize)
 - Use -our endings (not -or)
 - Distinguish licence (noun) vs license (verb)
 
 [View Full Changes] [Apply] [Create New Variant] [Ignore]"
```

**Scenario B: Domain Terminology Learning**
```
Detected specialized terms (Financial domain):
- Consistently changed "stock" → "equity" in security contexts
- Preferred "counterparty" over "other party" (12 times)
- Used "netting agreement" consistently (8 occurrences)
- Added "regulatory" before "compliance" (15 times)

AI Suggestion:
"I've learned domain-specific terminology from your edits.
 Create a 'Financial Services - Advanced' prompt variant with:
 - Preferred terminology glossary
 - Context-specific word choices
 - Regulatory language emphasis
 
 [Review Glossary] [Create Variant] [Add to Current]"
```

**Scenario C: Style Pattern Recognition**
```
Detected style preferences:
- Passive voice for procedures: 78% of procedural sentences
- "The patient should..." → "Patients should..." (plural, no article)
- Sentence case for all headings (42 heading edits)
- Consistent use of Oxford comma (94% of lists)

AI Suggestion:
"Your editing style shows clear preferences. Update prompt to include:
 - Style guide: Passive voice for medical procedures
 - Heading format: Sentence case preferred
 - Punctuation: Oxford comma standard
 
 [Preview Changes] [Apply] [Customize]"
```

**Deliverables:**
- Real-time edit tracking system
- Pattern analysis dashboard
- AI-generated improvement suggestions
- Automated prompt variant creation
- Learning statistics and confidence metrics
- Export learned patterns to share/backup

---

## Unique Value Proposition

### Why This Makes Supervertaler Special

**No other CAT tool offers:**

1. **Conversational Prompt Editing**
   - Most tools: Static prompt fields, manual editing only
   - Supervertaler: Natural language requests, AI assistance

2. **Learning from Actual Work**
   - Most tools: Prompts never evolve from usage
   - Supervertaler: Automatic discovery of user preferences

3. **Intelligent Adaptation**
   - Most tools: One-size-fits-all prompts
   - Supervertaler: Personalized, project-specific refinement

4. **Transparency & Control**
   - Most tools: Black box AI behavior
   - Supervertaler: See what AI learned, approve changes, understand rationale

### Competitive Analysis

**Current Translation AI Tools:**
- **DeepL Write**: Fixed suggestions, no customization
- **ChatGPT/Claude**: General purpose, no CAT integration
- **memoQ Language Weaver**: Fixed MT engines, no prompt control
- **Trados AI**: Limited customization, no learning
- **SmartCAT**: Basic AI, no prompt engineering

**None offer:**
- Interactive prompt development
- Edit-based learning
- Conversational AI assistance for prompt refinement
- Automated pattern recognition from translator behavior

---

## Technical Architecture

### High-Level System Design

```
┌─────────────────────────────────────────────────────────────┐
│                    Supervertaler Core                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Prompt Library Tab (UI Layer)              │    │
│  │  - Prompt list (filtered by type/task)             │    │
│  │  - Prompt editor pane                              │    │
│  │  - AI chat interface                               │    │
│  └──────────────┬─────────────────────────────────────┘    │
│                 │                                            │
│  ┌──────────────▼─────────────────────────────────────┐    │
│  │      AI Prompt Assistant (Business Logic)          │    │
│  │  - Conversation manager                            │    │
│  │  - Prompt analysis engine                          │    │
│  │  - Modification generator                          │    │
│  │  - Diff generator                                  │    │
│  └──────────────┬─────────────────────────────────────┘    │
│                 │                                            │
│  ┌──────────────▼─────────────────────────────────────┐    │
│  │      Edit Tracking System (Data Layer)             │    │
│  │  - EditTracker: Records all edits                  │    │
│  │  - PatternAnalyzer: Finds patterns                 │    │
│  │  - PromptLearner: Generates suggestions            │    │
│  └──────────────┬─────────────────────────────────────┘    │
│                 │                                            │
│  ┌──────────────▼─────────────────────────────────────┐    │
│  │           LLM Integration Layer                     │    │
│  │  - OpenAI API (GPT-4, GPT-4o)                      │    │
│  │  - Anthropic API (Claude 3.5 Sonnet)               │    │
│  │  - Google API (Gemini 1.5 Pro)                     │    │
│  └──────────────┬─────────────────────────────────────┘    │
│                 │                                            │
│  ┌──────────────▼─────────────────────────────────────┐    │
│  │         Persistent Storage                          │    │
│  │  - Prompts (JSON files)                            │    │
│  │  - Edit history (SQLite or JSON)                   │    │
│  │  - Learned patterns (JSON)                         │    │
│  │  - Conversation logs (optional)                    │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Data Models

**Edit Record:**
```python
{
    "id": "edit_20251014_001",
    "segment_id": 42,
    "project_id": "patent_chem_2024",
    "timestamp": "2025-10-14T22:30:15",
    "original_text": "The organization uses specialized equipment",
    "edited_text": "The organisation uses specialised equipment",
    "edit_type": "terminology",  # terminology | style | formatting | correction
    "edit_distance": 4,  # Levenshtein distance
    "context": {
        "active_prompt": "Patent Translation Specialist",
        "source_lang": "en-US",
        "target_lang": "en-GB"
    }
}
```

**Learned Pattern:**
```python
{
    "pattern_id": "pat_uk_spelling_001",
    "type": "terminology",
    "source_term": "organization",
    "target_term": "organisation",
    "frequency": 52,
    "confidence": 0.98,
    "first_seen": "2025-10-14T20:15:00",
    "last_seen": "2025-10-14T22:30:15",
    "projects": ["patent_chem_2024", "medical_uk_2024"],
    "contexts": ["UK English", "British medical terminology"]
}
```

**Prompt Modification Suggestion:**
```python
{
    "suggestion_id": "sug_20251014_001",
    "prompt_name": "Medical Translation Specialist",
    "modification_type": "enhancement",  # enhancement | correction | specialization
    "confidence": 0.85,
    "based_on_patterns": ["pat_uk_spelling_001", "pat_uk_spelling_002"],
    "proposed_changes": {
        "section": "SPELLING CHANGES",
        "operation": "add",
        "content": "- Use UK English spelling: -ise (not -ize), -our (not -or)"
    },
    "explanation": "Detected consistent UK spelling preference across 150+ edits",
    "status": "pending"  # pending | applied | rejected
}
```

---

## Implementation Roadmap

### Phase 1: Foundation (CURRENT SESSION)
- [x] Task Type system implementation
- [ ] Remove DEBUG logging
- [ ] Single Prompt Library tab
- [ ] Commit and document changes

### Phase 2: AI Chat Interface (Weeks 1-3)
- Week 1: Chat UI components
- Week 2: AI modification engine
- Week 3: Diff visualization and integration

### Phase 3: Edit Tracking (Month 2)
- Week 1: Edit recording infrastructure
- Week 2: Pattern analysis algorithms
- Week 3: Initial learning suggestions
- Week 4: Testing and refinement

### Phase 4: Polish & Launch (Month 3)
- Week 1: UI/UX improvements
- Week 2: Performance optimization
- Week 3: Documentation and examples
- Week 4: Beta testing with real users

---

## Success Metrics

**Phase 2 Success:**
- Users can modify prompts via chat in <30 seconds
- 80%+ of requested modifications work on first try
- Diff visualization is clear and actionable

**Phase 3 Success:**
- System detects 5+ meaningful patterns per 100 edits
- 70%+ of AI suggestions are accepted by users
- Users report prompts "get smarter" over time
- Reduced need for manual prompt tweaking

**Overall Success:**
- Supervertaler becomes known for "AI that learns from you"
- Feature drives user adoption and retention
- Community shares learned prompts/patterns
- Professional translators use it as competitive advantage

---

## Future Enhancements

**Beyond Phase 3:**

1. **Collaborative Learning**
   - Share learned patterns across team
   - Agency-wide prompt libraries
   - Community prompt marketplace

2. **Multi-Project Analysis**
   - Learn across all user's projects
   - Domain-specific pattern libraries
   - Client-specific prompt variants

3. **Predictive Suggestions**
   - "Users with similar edit patterns also improved prompts by..."
   - Proactive suggestions before starting new projects
   - Smart prompt recommendations based on file type/content

4. **Integration with TM Systems**
   - Learn from Translation Memory edits
   - Suggest prompt updates when TM patterns emerge
   - Bi-directional learning (TM ↔ Prompts)

5. **Voice/Multimodal Input**
   - "Hey Supervertaler, make this prompt focus more on legal precision"
   - Image-based examples in prompts
   - Audio notes for context

---

## Conclusion

The AI-Powered Prompt Editor with Edit-Based Learning represents a **paradigm shift** in how translators interact with AI assistance. Instead of static, one-size-fits-all prompts, Supervertaler would offer:

- **Personalized** prompts that adapt to each translator's style
- **Intelligent** assistance that learns from actual work
- **Transparent** AI that explains its suggestions
- **Collaborative** workflows that combine human expertise with AI power

This feature alone could establish Supervertaler as the **most intelligent and adaptive CAT tool** on the market.

---

**Document Status:** Vision & Implementation Plan  
**Created:** October 14, 2025  
**Author:** Michael Beijer  
**Next Review:** After Phase 1 completion
