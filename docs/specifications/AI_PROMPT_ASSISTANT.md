# AI Prompt Assistant Specification

## 🎯 Vision

An interactive AI-powered chat interface that helps users create, refine, and optimize translation prompts through natural conversation and automated learning from user edits.

## 🚀 Unique Value Proposition

**No other CAT tool or translation software offers:**
- ✅ AI-assisted prompt refinement through conversational chat
- ✅ Automated learning from user edits to improve prompts
- ✅ Interactive prompt development integrated into translation workflow
- ✅ Context-aware prompt generation based on document analysis

## 📊 Implementation Phases

### Phase 1: Basic AI Prompt Editor (MEDIUM - 15-20 hours)

**Goal:** Interactive chat interface for prompt modification

**Features:**
1. **Chat Interface**
   - Embedded chat panel in Prompt Library
   - User can request prompt modifications in natural language
   - AI analyzes current prompt and suggests specific changes
   - Visual diff showing before/after
   - Apply/Discard buttons for each suggestion

2. **Example Interactions:**
   ```
   User: "Add emphasis on chemical nomenclature to Patent prompt"
   AI: Analyzes prompt → Suggests additions → Shows diff → User approves
   
   User: "Make this prompt more formal"
   AI: Modifies tone throughout → Shows changes → User applies
   
   User: "Add a rule about preserving measurement units"
   AI: Adds specific instruction → Shows where inserted → User accepts
   ```

3. **Technical Components:**
   - Chat UI with scrollable history
   - LLM integration (reuse existing OpenAI/Anthropic/Google connections)
   - Diff visualization using `difflib`
   - Prompt versioning system

**UI Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ 🎯 Prompt Library                                           │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────┐  ┌────────────────────────────────────┐│
│ │ Prompt List     │  │ Prompt Editor + AI Assistant       ││
│ │                 │  │ ┌────────────────────────────────┐ ││
│ │ ✓ Patent Trans  │  │ │ Patent Translation Specialist  │ ││
│ │   Medical Trans │  │ │ [Prompt content here...]       │ ││
│ │   Legal Trans   │  │ │                                │ ││
│ │   Localization  │  │ └────────────────────────────────┘ ││
│ │                 │  │                                    ││
│ │                 │  │ 💬 AI Prompt Assistant             ││
│ │                 │  │ ┌────────────────────────────────┐ ││
│ │                 │  │ │ User: Add emphasis on chemical │ ││
│ │                 │  │ │ nomenclature precision         │ ││
│ │                 │  │ │                                │ ││
│ │                 │  │ │ AI: I'll modify the Patent     │ ││
│ │                 │  │ │ prompt to add...               │ ││
│ │                 │  │ │                                │ ││
│ │                 │  │ │ [Show Diff] [Apply] [Discard]  │ ││
│ │                 │  │ └────────────────────────────────┘ ││
│ └─────────────────┘  └────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### Phase 2: Document-Aware Prompt Generation (MEDIUM - 10-15 hours)

**Goal:** AI analyzes current document to suggest optimal prompts

**Features:**
1. **Analyze Document** button
   - AI examines source text segments
   - Detects domain (legal, medical, technical, etc.)
   - Identifies terminology patterns
   - Suggests appropriate base prompt
   - Offers customizations based on content

2. **Example Interaction:**
   ```
   User: Loads pharmaceutical patent document
   User: "Create a prompt for this document"
   AI: "I've analyzed your document. It appears to be a pharmaceutical 
        patent with chemical nomenclature and regulatory language. 
        I recommend starting with the Patent Translation prompt with 
        these modifications:
        - Emphasis on IUPAC chemical naming
        - Preservation of regulatory references
        - Formal technical tone
        Would you like me to create this prompt?"
   User: "Yes, but also add attention to measurement units"
   AI: Creates customized prompt → Shows content → User applies
   ```

3. **Document Analysis:**
   - Extract terminology frequency
   - Detect formatting patterns (lists, tables, headings)
   - Identify special elements (figures, equations, references)
   - Assess tone and formality level
   - Recognise domain-specific patterns

### Phase 3: Edit-Based Learning (HARD - 30-40 hours)

**Goal:** System learns from user edits to suggest prompt improvements

**Features:**
1. **Edit Tracking System**
   - Monitors every translation edit during work session
   - Categorizes edits: terminology, style, formatting, corrections
   - Aggregates patterns across segments
   - Stores edit history per project/domain

2. **Pattern Analysis:**
   ```python
   Detected Patterns:
   - Terminology: "color" → "colour" (50 instances) → UK English preference
   - Style: User adds "please" to imperatives (12 instances) → Polite tone
   - Formatting: Removes extra spaces (35 instances) → Strict formatting
   - Corrections: "program" → "programme" (18 instances) → UK spelling
   ```

3. **AI-Generated Suggestions:**
   ```
   AI: "I've noticed patterns in your edits:
       
       1. You consistently use UK English spelling
          → Update Patent prompt to specify 'en-GB'?
          
       2. You prefer formal medical terminology over common terms
          → Add instruction: 'Use formal medical terminology'?
          
       3. You remove 'respectively' when translating lists
          → Add rule: 'Avoid redundant 'respectively' in lists'?
       
       Apply these improvements? [Select All] [Review Each] [Dismiss]"
   ```

4. **Learning Categories:**
   - **Terminology Preferences:** Consistent word choice changes
   - **Style Rules:** Tone, formality, voice patterns
   - **Formatting Fixes:** Spacing, punctuation, structure
   - **Domain Patterns:** Subject-specific conventions

## 🛠️ Technical Architecture

### Core Components

#### 1. PromptAssistant Class
```python
class PromptAssistant:
    """AI-powered prompt modification and learning system"""
    
    def __init__(self, llm_client):
        self.llm = llm_client
        self.edit_history = []
        self.chat_history = []
        
    def suggest_modification(self, prompt_name, user_request):
        """AI suggests changes based on user request"""
        current_prompt = self.load_prompt(prompt_name)
        
        # Use LLM to modify prompt
        response = self.llm.chat([
            {"role": "system", "content": PROMPT_ENGINEER_SYSTEM},
            {"role": "user", "content": f"Modify this prompt: {current_prompt}\n\nUser wants: {user_request}"}
        ])
        
        # Parse response, generate diff
        new_prompt = self.extract_modified_prompt(response)
        diff = self.generate_diff(current_prompt, new_prompt)
        
        return {
            "new_prompt": new_prompt,
            "diff": diff,
            "explanation": response
        }
    
    def analyze_document(self, segments):
        """Analyze loaded document to suggest optimal prompt"""
        document_context = {
            'domain': self.detect_domain(segments),
            'terminology': self.extract_key_terms(segments),
            'tone': self.assess_tone(segments),
            'special_elements': self.identify_elements(segments)
        }
        
        suggestion = self.llm.generate_prompt_suggestion(document_context)
        return suggestion
    
    def learn_from_edits(self, project_edits):
        """Analyze translation edits to suggest prompt improvements"""
        patterns = self.analyze_edit_patterns(project_edits)
        suggestions = self.llm.generate_prompt_improvements(patterns)
        return suggestions
```

#### 2. EditTracker Class
```python
class EditTracker:
    """Track and analyze user edits during translation"""
    
    def __init__(self):
        self.edits = []
        
    def track_edit(self, segment_id, original, edited, context):
        """Record each edit with context"""
        self.edits.append({
            'segment_id': segment_id,
            'original': original,
            'edited': edited,
            'type': self.classify_edit(original, edited),
            'timestamp': datetime.now(),
            'edit_distance': self.calculate_distance(original, edited),
            'context': context  # Surrounding segments, document metadata
        })
    
    def analyze_patterns(self):
        """Find patterns in edits"""
        patterns = {
            'terminology': defaultdict(int),  # "color" → "colour": 50
            'style_rules': [],
            'common_fixes': [],
            'formatting_preferences': []
        }
        
        for edit in self.edits:
            # Detect terminology changes
            if self.is_terminology_change(edit):
                change = f"{edit['original']} → {edit['edited']}"
                patterns['terminology'][change] += 1
            
            # Detect style patterns
            style = self.extract_style_pattern(edit)
            if style:
                patterns['style_rules'].append(style)
            
            # Common correction patterns
            if self.is_common_error(edit):
                patterns['common_fixes'].append(edit)
        
        return self.aggregate_patterns(patterns)
    
    def classify_edit(self, original, edited):
        """Classify type of edit"""
        # Terminology: Single word/phrase substitution
        # Style: Tone, voice, formality changes
        # Formatting: Spacing, punctuation, capitalization
        # Correction: Grammar, accuracy fixes
        # Structure: Sentence reordering, restructuring
        pass
```

#### 3. DiffVisualizer Class
```python
class DiffVisualizer:
    """Generate visual diffs for prompt changes"""
    
    def generate_diff(self, old_prompt, new_prompt):
        """Create side-by-side or inline diff"""
        import difflib
        
        diff = difflib.unified_diff(
            old_prompt.splitlines(),
            new_prompt.splitlines(),
            lineterm=''
        )
        
        return self.format_diff_for_display(diff)
    
    def format_diff_for_display(self, diff):
        """Convert diff to rich text with colors"""
        # Green for additions
        # Red for deletions
        # Yellow for modifications
        pass
```

### System Prompts

#### Prompt Engineer System Prompt
```
You are an expert prompt engineer specializing in translation and localization.
Your role is to help users refine and optimize their translation prompts.

When modifying prompts:
1. Maintain the original structure and intent
2. Add specific, actionable instructions
3. Use clear, unambiguous language
4. Consider context and domain requirements
5. Preserve existing rules unless explicitly changing them

When analyzing documents:
1. Identify the domain and subject matter
2. Detect terminology patterns and technical language
3. Assess tone, formality, and audience
4. Note special formatting or structural elements
5. Suggest appropriate prompt customizations

When learning from edits:
1. Look for consistent patterns (5+ occurrences)
2. Categorize changes: terminology, style, formatting
3. Propose specific, testable prompt improvements
4. Explain why each suggestion would help
5. Allow selective application of suggestions
```

## 📋 User Stories

### Story 1: Refine Existing Prompt
**As a** medical translator  
**I want to** chat with AI to refine my Medical Translation prompt  
**So that** I can add specific terminology preferences without manual editing

**Acceptance Criteria:**
- [ ] User can open chat in Prompt Library
- [ ] User can request modifications in natural language
- [ ] AI understands context and suggests specific changes
- [ ] User sees visual diff before applying
- [ ] Changes are applied with single click
- [ ] Original prompt is preserved (versioning)

### Story 2: Generate Prompt from Document
**As a** patent translator  
**I want** AI to analyze my document and suggest an optimized prompt  
**So that** I don't have to manually configure every setting

**Acceptance Criteria:**
- [ ] User clicks "Analyze Document" button
- [ ] AI examines loaded segments
- [ ] AI identifies domain, terminology, and special requirements
- [ ] AI suggests base prompt with customizations
- [ ] User can request additional modifications
- [ ] Generated prompt can be saved to library

### Story 3: Learn from Translation Edits
**As a** professional translator  
**I want** the system to learn from my correction patterns  
**So that** future translations better match my style automatically

**Acceptance Criteria:**
- [ ] System tracks all edits during translation
- [ ] After session, AI analyzes edit patterns
- [ ] AI suggests specific prompt improvements
- [ ] User reviews suggestions individually
- [ ] User can apply selected improvements
- [ ] System remembers accepted patterns for future suggestions

## 🎨 UI Components

### Chat Interface
- **Input Field:** Multi-line text area with Send button
- **Message Bubbles:** Distinct styling for user vs AI messages
- **Diff Viewer:** Side-by-side or inline comparison with syntax highlighting
- **Action Buttons:** Apply, Discard, Show More, Modify Further
- **History:** Scrollable conversation history (session-persistent)

### Prompt Editor Integration
- **Split View:** Prompt content on left, chat on right (or bottom)
- **Quick Actions:** "Ask AI to improve this", "Analyze current document"
- **Status Indicator:** Shows when AI is processing
- **Version History:** Dropdown showing prompt versions with revert option

## 🔧 Technical Requirements

### Dependencies
- `difflib` - Built-in Python, for diff generation
- Existing LLM clients (OpenAI, Anthropic, Google)
- `tkinter` widgets for chat UI
- JSON storage for edit history and chat logs

### Performance Considerations
- Chat responses should be async (non-blocking UI)
- Edit analysis can run in background
- Limit stored edit history to recent 1000 edits or 30 days
- Cache common diff patterns

### Data Storage
```
user data/
  Edit_History/
    [project_name]_edits.json
  Chat_Logs/
    prompt_assistant_[date].json
  Prompt_Versions/
    [prompt_name]_v1.json
    [prompt_name]_v2.json
```

## 📊 Success Metrics

### Phase 1
- [ ] 80% of users try the AI assistant within first week
- [ ] Average 3+ prompt modifications per user per session
- [ ] 90% satisfaction rate with AI suggestions

### Phase 2
- [ ] 60% of new projects use document-based prompt generation
- [ ] Generated prompts achieve 85%+ user satisfaction
- [ ] Average 2 minutes saved per prompt creation

### Phase 3
- [ ] System detects actionable patterns in 70% of sessions
- [ ] 50% of suggestions are accepted by users
- [ ] Translation quality improves 15% (measured by edit rate)

## 🚦 Implementation Roadmap

### Milestone 1: Basic Chat Interface (Week 1-2)
- [ ] Design and implement chat UI
- [ ] Integrate with existing LLM clients
- [ ] Basic prompt modification workflow
- [ ] Diff visualization
- [ ] Apply/Discard functionality

### Milestone 2: Document Analysis (Week 3-4)
- [ ] Domain detection algorithm
- [ ] Terminology extraction
- [ ] Tone assessment
- [ ] Prompt generation from analysis
- [ ] Template system for common patterns

### Milestone 3: Edit Tracking (Week 5-6)
- [ ] Hook into translation grid edit events
- [ ] Edit classification system
- [ ] Pattern detection algorithms
- [ ] Storage and retrieval of edit history

### Milestone 4: Learning System (Week 7-8)
- [ ] Pattern aggregation
- [ ] AI-powered suggestion generation
- [ ] User review interface
- [ ] Prompt update workflow
- [ ] Feedback loop integration

## 💡 Future Enhancements

### Advanced Features
1. **Collaborative Learning:** Share anonymized patterns across users (opt-in)
2. **Prompt Templates Marketplace:** Community-contributed prompts
3. **A/B Testing:** Test prompt variations, track which performs better
4. **Voice Input:** Speak modifications instead of typing
5. **Multi-lingual Prompts:** AI adapts instructions for target language
6. **Integration with TM:** Learn from translation memory matches
7. **Quality Scoring:** AI scores translation quality, suggests improvements

### AI Capabilities
1. **Context Awareness:** Remember project context across sessions
2. **Proactive Suggestions:** "Your translations seem inconsistent, want help?"
3. **Batch Optimization:** Analyze multiple projects, suggest universal improvements
4. **Custom AI Models:** Fine-tune models on user's specific domain

## 🔐 Privacy & Ethics

### Data Handling
- Edit patterns stored locally by default
- Optional cloud sync (encrypted)
- User controls what data AI can access
- Clear consent for learning features
- Ability to disable tracking entirely

### Transparency
- Show user what patterns AI detected
- Explain why each suggestion was made
- Allow user to reject patterns permanently
- Audit log of all AI-suggested changes

## 📚 Documentation Needs

1. **User Guide:** "Using the AI Prompt Assistant"
2. **Tutorial Video:** "Creating Your First AI-Assisted Prompt"
3. **Best Practices:** "Getting the Most from Edit-Based Learning"
4. **FAQ:** Common questions and troubleshooting
5. **API Reference:** For developers extending the system

---

**Status:** Specification Draft  
**Target Version:** v4.0.0-beta  
**Last Updated:** January 16, 2025  
**Author:** Based on concept discussion
