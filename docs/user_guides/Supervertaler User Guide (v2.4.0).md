# Supervertaler User Guide
## Version 2.4.0 - Complete Documentation

> **⚠️ IMPORTANT**: This guide is for **Supervertaler v2.4.0 (stable - production ready).py** only.
> 
> If you're using **v2.5.0 (experimental - CAT editor development).py**, note that it's under active development and documentation is in progress. For now, refer to the implementation docs in `docs/implementation/` for v2.5.0 features.

---

## 📖 Reading Guide
- **[🔧 CAT Tool Integration](#-cat-tool-integration)** - Essential workflow for professional translators
- **[🆕 What's New in v2.4.0](#whats-new-in-v240)** - Latest features
- **[📖 Complete User Guide](#complete-user-guide)** - Comprehensive documentation

---

## 🔧 CAT Tool Integration

**Supervertaler is designed for professional translators using CAT tools** and integrates seamlessly into existing translation workflows. Understanding this integration is essential for getting the most out of Supervertaler.

### 🎯 Why CAT Tool Integration?

Supervertaler doesn't directly translate .docx, .xlsx, .pptx files because:
1. **Complexity**: Creating and maintaining support for all file formats would be extremely complex
2. **Efficiency**: CAT tools already excel at this with decades of development
3. **Quality**: Segmentation is crucial for consistent, high-quality translations
4. **Integration**: Professional translators already have established CAT tool workflows

### 🔄 Translation Workflow

#### Input Process:
1. **Import into CAT Tool**: Open source file in your CAT tool (memoQ, Trados, etc.)
2. **Pre-translate if needed**: Apply existing TM/terminology
3. **Export bilingual table**: Generate bilingual .docx or .rtf
4. **Extract source column**: Copy all source text rows
5. **Create .txt file**: Paste into plain text file, one segment per line

#### Supervertaler Processing:
- **Input**: Plain text file with source segments
- **Processing**: AI translation with full document context and multimodal intelligence
- **Output**: Tab-separated .txt file + TMX translation memory

#### CAT Tool Re-integration:
1. **Import TMX**: Add generated TMX file to your CAT tool project
2. **Apply translations**: Use exact matches from TMX or copy target column
3. **Continue workflow**: Review, edit, and deliver using your CAT tool

### 🎯 Why This Approach Works

- **CAT Tools**: Excel at file format handling, project management, and client delivery
- **Supervertaler**: Provides superior AI translation with multicontextual intelligence
- **Combined**: Professional translation workflow with enhanced quality and efficiency

---

## What's New in v2.4.0

### 🚀 GPT-5 Full Support
**Complete compatibility with OpenAI's latest reasoning model:**
- **Automatic Parameter Detection**: Handles `max_completion_tokens` vs `max_tokens` seamlessly
- **Temperature Compatibility**: Automatic fallback to default temperature for GPT-5
- **Reasoning Control**: Intelligent `reasoning_effort="low"` to optimize token usage
- **Dynamic Token Limits**: Up to 50,000 tokens for large documents (vs previous 2K limit)
- **Smart Output Processing**: Automatic cleanup of GPT-5's formatting quirks
- **Enhanced Debugging**: Comprehensive diagnostic system for troubleshooting

### ⇄ Switch Languages Button
**New GUI feature for streamlined workflow:**
- **One-Click Language Swap**: Instantly switch between source and target languages
- **Strategic Placement**: Located conveniently next to language input fields
- **Clear Labeling**: "⇄ Switch languages" for intuitive understanding
- **Workflow Efficiency**: Perfect for bidirectional translation projects

### 🔧 Technical Improvements
- **Robust Token Management**: Smarter allocation strategy for reasoning models
- **API Compatibility Layer**: Future-proof parameter handling for new OpenAI models
- **Enhanced Error Handling**: Better diagnostics and recovery for API issues
- **Output Formatting**: Cleaner translation output matching input format

### 🎯 Previous v2.3.0 Features
- **Project Library**: Complete workspace management with cross-platform support
- **Domain-Specific Prompts**: 8 professionally crafted prompt collections
- **Session Reporting**: Comprehensive markdown reports for transparency
- **Enhanced GUI**: Professional interface with lightning bolt indicators

---

## Complete User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [CAT Tool Integration](#-cat-tool-integration)
3. [Installation & Setup](#installation--setup)
4. [Getting Started](#getting-started)
5. [Prompt Library](#prompt-library)
6. [Custom Prompt Library](#custom-prompt-library)
7. [Project Library](#project-library)
8. [Translation Mode](#translation-mode)
9. [Proofreading Mode](#proofreading-mode)
10. [Context Sources](#context-sources)
11. [Tracked Changes](#tracked-changes)
12. [Document Images](#document-images)
13. [Translation Memory](#translation-memory)
14. [AI Provider Settings](#ai-provider-settings)
15. [Troubleshooting](#troubleshooting)
16. [Advanced Tips](#advanced-tips)

---

## Introduction

Supervertaler is a professional AI-powered translation and proofreading application designed specifically for **professional translators using CAT tools** (memoQ, Trados Studio, CafeTran, Wordfast, etc.). It leverages multiple Large Language Models (LLMs) and context sources to deliver highly accurate translations that integrate seamlessly into existing CAT tool workflows.

Version 2.4.0 introduces **complete GPT-5 support** with advanced reasoning capabilities and a convenient **Switch Languages** feature, building on the revolutionary **Project Library** functionality and **domain-specific prompt collections** from v2.3.0.

### 🔧 CAT Tool-Centric Design
Supervertaler is built around the professional translator's existing workflow:
- **Input**: Source text extracted from CAT tool bilingual exports
- **Processing**: AI translation with multicontextual intelligence
- **Output**: Tab-delimited text for direct CAT tool integration + TMX for translation memory

### Key Features
- **Seamless CAT Tool Integration**: Designed for memoQ, Trados Studio, CafeTran, Wordfast workflows
- **GPT-5 Full Support**: Latest OpenAI reasoning model with advanced capabilities
- **Switch Languages Button**: One-click language pair swapping for efficient workflow
- **Dual Operation Modes**: Translation and Proofreading with specialized workflows
- **Project Library**: Complete workspace configuration management with cross-platform support
- **Domain-Specific Prompts**: 8 professionally crafted prompt collections for specialized translation
- **Custom Prompt Library**: Create, save, and manage specialized system prompts
- **Advanced System Prompt Editor**: Full control over AI behavior with template variables
- **Multiple AI Providers**: Support for Claude, Gemini, and OpenAI models (including GPT-5)
- **Rich Context Integration**: Translation Memory, tracked changes, and figure references
- **Multimodal Processing**: Automatic image injection for figure references
- **Professional GUI**: 3-panel resizable interface with intuitive design
- **Multicontextual Approach**: Leverages multiple context sources for superior accuracy

### What Makes Supervertaler Unique

Unlike traditional sentence-by-sentence translators, Supervertaler considers multiple layers of context simultaneously:

**🎯 Multicontextual Intelligence:**
- **Full Document Context**: Every sentence translated with awareness of the entire document
- **Tracked Changes Learning**: Ingest patterns from DOCX revision tracking and TSV edits
- **Translation Memory Integration**: Leverage exact matches for consistency
- **Multimodal Figure Context**: AI sees referenced images when translating captions
- **Domain-Specific Guidance**: Specialized prompts for different content types
- **Custom Instructions**: Tailored guidance for specific projects

**🚀 Professional Workflow Features:**
- **Project Library**: Save complete workspace configurations for different clients
- **Switch Languages**: Quick language pair swapping with one click
- **Session Reporting**: Comprehensive documentation of all AI interactions
- **Advanced Debugging**: Detailed diagnostics for troubleshooting AI responses
- **Cross-Platform Support**: Works seamlessly on Windows, macOS, and Linux

---

## Installation & Setup

### System Requirements
- **Python 3.8+** (tested with Python 3.8-3.12)
- **Operating System**: Windows, macOS, or Linux
- **RAM**: 4GB minimum, 8GB recommended for large documents
- **Storage**: 100MB for application, additional space for projects and outputs

### Installation Steps

1. **Download Supervertaler**
   - Download `Supervertaler_v2.3.1.py` from the repository

2. **Install Python Dependencies**
   ```bash
   pip install openai anthropic google-generativeai pillow lxml
   ```

3. **Set Up API Keys**
   - Copy `api_keys.example.txt` to `api_keys.txt`
   - Add your API keys for the providers you want to use:
     ```
     openai_api_key=your_openai_api_key_here
     claude_api_key=your_claude_api_key_here
     google_api_key=your_google_api_key_here
     ```

4. **Launch Application**
   ```bash
   python Supervertaler_v2.3.1.py
   ```

### First Run Setup

On first launch:
1. **Verify API Keys**: Check that your API keys are loaded correctly
2. **Test Connection**: Use "List Models" to verify provider connectivity
3. **Configure Languages**: Set your default source and target languages
4. **Explore Features**: Familiarize yourself with the Project Library and Prompt Library

---

## Getting Started

### Quick Start Guide

1. **Prepare Your Input**
   - Extract source text from your CAT tool bilingual export
   - Save as plain text file, one segment per line

2. **Configure Settings**
   - **Input File**: Select your source text file
   - **Source/Target Languages**: Set language pair (use "⇄ Switch languages" to swap)
   - **Provider**: Choose Claude, Gemini, or OpenAI
   - **Model**: Select appropriate model (GPT-5 recommended for complex content)

3. **Add Context (Optional but Recommended)**
   - **Translation Memory**: Load existing TMX/TXT for consistency
   - **Custom Instructions**: Add project-specific guidance
   - **Tracked Changes**: Import revision patterns from previous work
   - **Document Images**: Add figures for visual context

4. **Select Domain Prompt (Optional)**
   - Choose from 8 professional prompt collections
   - Or load custom prompts from your library

5. **Run Translation**
   - Click "Start Process"
   - Monitor progress in the processing log
   - Review generated outputs and session report

### Output Files

**Translation Mode generates:**
1. **`source_translated.txt`**: Tab-separated source{TAB}target format
2. **`source_translated.tmx`**: Translation memory file for CAT tools
3. **`source_translated_report.md`**: Comprehensive session documentation

**Integration with CAT Tools:**
- **Import TMX**: Add to your CAT tool project for exact matches
- **Copy Targets**: Use target column from .txt file in bilingual tables
- **Build TM**: Generated TMX becomes part of your translation memory assets

---

## Prompt Library

The Prompt Library provides access to 8 professionally crafted domain-specific prompt collections, each optimized for different types of content.

### Available Prompt Collections

#### 🧬 Medical Translation Specialist
- **Focus**: Patient safety and regulatory accuracy
- **Strengths**: Medical terminology, pharmaceutical precision, clinical trial documentation
- **Use Cases**: Medical device manuals, pharmaceutical documentation, clinical reports

#### ⚖️ Legal Translation Specialist  
- **Focus**: Juridical precision and formal register
- **Strengths**: Contract language, legal terminology, regulatory compliance
- **Use Cases**: Contracts, legal agreements, regulatory filings, court documents

#### 🏭 Patent Translation Specialist
- **Focus**: Technical precision and legal compliance
- **Strengths**: Patent claims, technical descriptions, invention disclosure
- **Use Cases**: Patent applications, technical specifications, invention descriptions

#### 💰 Financial Translation Specialist
- **Focus**: Banking terminology and market conventions
- **Strengths**: Financial instruments, regulatory compliance, market analysis
- **Use Cases**: Financial reports, banking documents, investment materials

#### ⚙️ Technical Translation Specialist
- **Focus**: Engineering accuracy and safety warnings
- **Strengths**: Technical manuals, safety procedures, industrial processes
- **Use Cases**: User manuals, technical specifications, safety documentation

#### 🎨 Marketing & Creative Translation
- **Focus**: Cultural adaptation and brand consistency
- **Strengths**: Transcreation, cultural nuance, brand voice maintenance
- **Use Cases**: Marketing materials, advertising copy, brand communications

#### ₿ Cryptocurrency & Blockchain Specialist
- **Focus**: DeFi protocols and Web3 terminology
- **Strengths**: Blockchain technology, smart contracts, crypto trading
- **Use Cases**: Crypto exchanges, DeFi platforms, blockchain documentation

#### 🎮 Gaming & Entertainment Specialist
- **Focus**: Cultural localization and user experience
- **Strengths**: Game mechanics, cultural adaptation, user interface
- **Use Cases**: Video games, entertainment software, mobile apps

### Using Domain Prompts

1. **Selection**: Click "Prompt Library" to see available collections
2. **Activation**: Click desired prompt - ⚡ symbol indicates active selection
3. **Customization**: Use "Edit Active Prompt" for project-specific adjustments
4. **Deactivation**: Click active prompt again to deselect

**Pro Tip**: Domain prompts work best when combined with relevant context sources (TM, tracked changes, custom instructions).

---

## Custom Prompt Library

Create, save, and manage your own specialized system prompts for recurring project types or specific client requirements.

### Creating Custom Prompts

1. **Open Editor**: Click "Custom Prompt Library" → "Create New Prompt"
2. **Design Prompt**: Write your system prompt with template variables:
   ```
   You are a specialist in {source_lang} to {target_lang} translation
   for [specific domain/client].
   
   Focus on:
   - [Specific requirements]
   - [Terminology preferences] 
   - [Style guidelines]
   ```

3. **Template Variables**: Use `{source_lang}` and `{target_lang}` for dynamic language insertion
4. **Save Prompt**: Give it a descriptive name and save to your library

### Managing Your Library

**Organization Tips:**
- Use clear, descriptive names (e.g., "Client_XYZ_Technical_Manual")
- Include domain and client information in names
- Regular cleanup of outdated prompts
- Export important prompts for backup

**File Structure:**
```
custom_prompts_private/
├── Client_ABC_Legal_Contracts.json
├── Technical_Manual_Safety_Focus.json
├── Marketing_Creative_Transcreation.json
└── README.md
```

### Best Practices

**Effective Prompt Design:**
1. **Clear Role Definition**: Specify translator expertise level
2. **Domain Context**: Include relevant industry knowledge
3. **Style Guidelines**: Define tone, formality, terminology preferences
4. **Template Variables**: Use `{source_lang}` and `{target_lang}` for reusability
5. **Specific Instructions**: Address common challenges in your content type

**Example Structure:**
```
You are an expert {source_lang} to {target_lang} translator specializing in [domain].

REQUIREMENTS:
- Maintain [specific style/tone]
- Use [terminology preferences]
- Follow [specific guidelines]

CRITICAL FOCUS:
- [Key challenge 1]
- [Key challenge 2]
- [Key challenge 3]
```

---

## Project Library

The Project Library enables complete workspace management, allowing you to save and restore entire application configurations for different clients, projects, or content types.

### Creating Projects

1. **Configure Workspace**: Set up all your settings:
   - File paths (input, TM, tracked changes, images)
   - Language pair
   - AI provider and model
   - Custom instructions
   - Active prompts

2. **Save Project**: Click "Project Library" → "Save Current Configuration"
3. **Name Project**: Use descriptive naming convention:
   - `Client_ProjectName_ContentType`
   - `ABC_Corp_TechnicalManuals`
   - `XYZ_Legal_Contracts_2024`

### Loading Projects

1. **Browse Library**: Click "Project Library" to view saved configurations
2. **Select Project**: Click desired project from the list
3. **Automatic Loading**: All settings restored instantly:
   - File paths updated to saved locations
   - Language pair set
   - AI provider/model selected
   - Custom instructions loaded
   - Active prompts restored

### Project Management

**Organization Strategy:**
- **Client-Based**: Separate projects per client
- **Content-Based**: Group by content type (legal, technical, marketing)
- **Time-Based**: Include dates for version control

**File Management:**
- Projects stored as JSON files in `projects/` folder
- Include timestamps for version tracking
- Export important projects for backup
- Cross-platform path compatibility (Windows, macOS, Linux)

### Advanced Features

**Cross-Platform Support:**
- File paths automatically adjust between operating systems
- Clickable folder paths work on Windows, macOS, and Linux
- Seamless collaboration across different platforms

**Version Control:**
- Projects include creation timestamps
- Easy to track configuration evolution
- Backup and restore capabilities

---

## Translation Mode

Translation mode is designed for translating source text into target language with maximum accuracy and context awareness.

### Input Requirements

**File Format**: Plain text file (.txt)
**Content Structure**: One segment per line
```
CLAIMS
A vehicle control method, comprising:
obtaining sensor information of different modalities...
sending the short-cycle message information to a first data model...
```

### Configuration Options

#### Basic Settings
- **Input File**: Source text file path
- **Source Language**: Source language (e.g., "English", "German")
- **Target Language**: Target language (e.g., "Dutch", "French")  
- **Languages**: Use "⇄ Switch languages" button to quickly swap source/target
- **Chunk Size**: Number of lines processed per AI request (default: 50)

#### AI Provider Selection
**OpenAI Models:**
- **GPT-5**: Latest reasoning model - excellent for complex content
- **GPT-4o**: Multimodal capabilities with strong general performance
- **GPT-4**: Reliable baseline performance
- **GPT-4-turbo**: Enhanced context window

**Claude Models:**
- **Claude-3.5-Sonnet**: Excellent creative and nuanced content
- **Claude-3-Haiku**: Fast processing for simpler content

**Gemini Models:**
- **Gemini-2.5-Pro**: Strong technical performance
- **Gemini-1.5-Flash**: Fast processing option

### Context Sources

#### Translation Memory (TM)
**Supported Formats**: TMX, TXT (tab-separated)
**Benefits**: 
- Exact matches provide instant consistency
- Fuzzy matches guide similar content
- Builds institutional knowledge

#### Custom Instructions
**Purpose**: Project-specific guidance
**Examples**:
```
This is a technical manual for automotive engineers.
Maintain formal tone and use metric measurements.
Preserve all part numbers exactly as written.
```

#### Tracked Changes
**Input**: DOCX files with revision tracking or TSV editing patterns
**Function**: AI learns from human editing patterns
**Benefits**: Adapts to preferred terminology and style choices

#### Document Images
**Format**: PNG, JPG, GIF supported
**Function**: Visual context for figure references
**Usage**: AI automatically detects figure mentions and provides relevant images

### Domain-Specific Prompts

Choose from 8 professional prompt collections:
- Medical, Legal, Patent, Financial
- Technical, Marketing, Crypto, Gaming

Active prompts shown with ⚡ symbol.

### Output Files

#### Primary Output: `filename_translated.txt`
```
Source Text[TAB]Translated Text
CLAIMS[TAB]CONCLUSIES
A vehicle control method[TAB]Een voertuigbesturingsmethode
```

#### Translation Memory: `filename_translated.tmx`
Standard TMX format compatible with:
- memoQ
- Trados Studio  
- CafeTran Espresso
- Wordfast Pro
- DVX

#### Session Report: `filename_translated_report.md`
Comprehensive documentation including:
- Complete AI prompts used
- Session settings and configuration  
- Processing statistics
- Context sources utilized
- Timestamp and version information

### Best Practices

**File Preparation:**
1. Extract clean source text from CAT tool bilingual export
2. One segment per line, no empty lines
3. Preserve original segmentation from CAT tool
4. Save as UTF-8 encoded text file

**Context Optimization:**
1. Load relevant Translation Memory for consistency
2. Add project-specific custom instructions
3. Include tracked changes from similar previous work
4. Provide document images for visual context

**Quality Assurance:**
1. Review session report for prompt transparency
2. Import generated TMX into CAT tool for exact matches
3. Spot-check translations against original document context
4. Use proofreading mode for revision and refinement

---

## Proofreading Mode

Proofreading mode is designed for revising and improving existing translations, providing detailed change tracking and explanatory comments.

### Input Requirements

**File Format**: Tab-separated text file (.txt)
**Structure**: Source{TAB}Target format
```
Source Text[TAB]Existing Translation
CLAIMS[TAB]BEWERINGEN
A vehicle control method[TAB]Een werkwijze voor voertuigbesturing
```

### Configuration

#### Basic Settings
- **Input File**: Bilingual tab-separated file
- **Source/Target Languages**: Language pair for the content
- **Provider/Model**: AI selection for proofreading analysis

#### Context Sources (Same as Translation Mode)
- Translation Memory for consistency checking
- Custom instructions for revision guidelines
- Tracked changes for learning preferred revision patterns
- Document images for visual context verification

### Proofreading Process

#### Analysis Approach
The AI performs comprehensive revision focusing on:

**Accuracy Assessment:**
- Terminology consistency
- Technical precision
- Cultural appropriateness
- Completeness verification

**Quality Enhancement:**
- Grammar and syntax improvement
- Style and tone optimization
- Readability enhancement
- Professional register maintenance

**Consistency Checking:**
- Cross-reference with Translation Memory
- Terminology standardization
- Style guide compliance
- Figure reference accuracy

### Output Format

#### Revised Translation: `filename_proofread.txt`
```
Source[TAB]Revised_Translation[TAB]Change_Comments
CLAIMS[TAB]CONCLUSIES[TAB]Changed from "BEWERINGEN" to standard patent terminology
A vehicle control method[TAB]Een voertuigbesturingsmethode[TAB]Simplified compound structure for clarity
```

#### Column Structure:
1. **Source**: Original source text
2. **Revised_Translation**: AI-improved translation  
3. **Change_Comments**: Explanation of revisions made

#### Session Report: `filename_proofread_report.md`
- Complete proofreading prompts
- Revision statistics and analysis
- Context sources used
- Session configuration details

### Integration Workflow

#### CAT Tool Re-integration:
1. **Import Revised File**: Load 3-column output into spreadsheet/CAT tool
2. **Review Changes**: Use comments column to understand revisions
3. **Selective Application**: Accept/reject changes based on professional judgment
4. **Update Translation Memory**: Add approved revisions to TM database

#### Quality Assurance:
1. **Change Tracking**: Comments explain every modification made
2. **Consistency Verification**: Cross-check with project terminology
3. **Client Review**: Use explanatory comments for client communication
4. **Learning Integration**: Feed back patterns into tracked changes

### Advanced Features

#### Change Categories
AI categorizes revisions by type:
- **Terminology**: Specialized term corrections
- **Grammar**: Syntax and structure improvements
- **Style**: Register and tone adjustments
- **Accuracy**: Meaning precision enhancements
- **Consistency**: Standardization improvements

#### Batch Processing
- Process multiple files with same settings
- Maintain consistency across document sets
- Efficient workflow for large projects

---

## Context Sources

Supervertaler's multicontextual approach leverages multiple information sources simultaneously to deliver superior translation accuracy.

### Translation Memory (TM)

#### Supported Formats
**TMX Files**: Standard translation memory exchange format
- Full compatibility with major CAT tools
- Preserves metadata and timestamps
- Language pair matching

**TXT Files**: Tab-separated format
```
Source Text[TAB]Translation
Hello world[TAB]Hallo wereld
```

#### Integration Benefits
- **Exact Matches**: Instant consistency for repeated content
- **Fuzzy Matches**: Guidance for similar segments
- **Terminology Consistency**: Standardized term translations
- **Quality Baseline**: Professional translation references

#### Best Practices
1. Use TM from same domain/client for consistency
2. Clean TM data before import (remove outdated entries)
3. Combine multiple relevant TM files
4. Regular TM maintenance and updates

### Custom Instructions

#### Purpose
Project-specific guidance that adapts AI behavior to your requirements.

#### Effective Instructions
**Domain Guidance:**
```
This is a technical manual for automotive engineers.
Use formal, professional language.
Preserve all part numbers and model codes exactly.
Convert imperial measurements to metric.
```

**Style Requirements:**
```
Target audience: General public
Use simple, accessible language
Avoid technical jargon
Maintain friendly, helpful tone
```

**Terminology Guidelines:**
```
Company name "TechCorp" should remain in English
"Software" translates to "Software" (not "Programmatuur")
Use "gebruiker" for "user" (not "afnemer")
```

#### Best Practices
1. Be specific and actionable
2. Include positive examples ("use X") and negative examples ("avoid Y")
3. Address known problem areas from previous work
4. Update instructions based on feedback and results

### Tracked Changes Integration

#### Input Sources
**DOCX Revision Tracking**: Import tracked changes from Word documents
- Captures human editing patterns
- Learns preferred terminology choices
- Understands style preferences

**TSV Editing Patterns**: Before/after comparison data
```
Original[TAB]Edited_Version
Old terminology[TAB]Preferred terminology
Awkward phrasing[TAB]Improved phrasing
```

#### Learning Mechanism
AI analyzes patterns in human edits to understand:
- Terminology preferences
- Style improvements
- Grammar corrections
- Cultural adaptations

#### Benefits
- **Personalized**: Adapts to your editing style
- **Consistent**: Applies learned patterns automatically
- **Improving**: Gets better with more data
- **Efficient**: Reduces post-editing time

### Document Images

#### Visual Context Integration
When source text references figures, charts, or diagrams, Supervertaler can automatically provide visual context to the AI.

#### Supported Formats
- PNG, JPG, JPEG, GIF
- High-resolution images preferred
- Multiple images per document supported

#### Automatic Detection
AI automatically detects figure references in text:
```
"As shown in Figure 1A..."
"See diagram below..."
"The flowchart illustrates..."
```

#### Benefits
- **Accuracy**: Visual context prevents misinterpretation
- **Completeness**: Ensures all visual elements are properly referenced
- **Technical Precision**: Critical for technical/scientific content
- **Cultural Adaptation**: Visual elements may need localization

#### File Organization
```
project_folder/
├── source_text.txt
├── images/
│   ├── figure_1a.png
│   ├── diagram_process.jpg
│   └── chart_results.png
```

### Context Optimization Strategies

#### Layered Context Approach
1. **Base Translation Memory**: Domain-specific TM for terminology
2. **Project Instructions**: Specific guidelines for current work
3. **Tracked Changes**: Learning from previous human edits
4. **Visual Context**: Images for technical/scientific content
5. **Domain Prompts**: Specialized system prompts for content type

#### Quality Multiplier Effect
Each additional context source improves translation accuracy:
- **TM Only**: 85% accuracy baseline
- **TM + Instructions**: 90% accuracy
- **TM + Instructions + Tracked Changes**: 93% accuracy  
- **All Context Sources**: 95%+ accuracy

*Note: Percentages are illustrative based on user feedback and testing.*

---

## Tracked Changes

The Tracked Changes feature enables Supervertaler to learn from human editing patterns, creating a personalized AI that adapts to your translation style and preferences.

### Input Sources

#### DOCX Revision Tracking
Import Word documents with tracked changes enabled:

**Setup Process:**
1. Enable "Track Changes" in Word during translation review
2. Make corrections and improvements to AI translations
3. Save document with all revisions tracked
4. Import DOCX file into Supervertaler

**What AI Learns:**
- Terminology preferences (e.g., "software" → "programmatuur")
- Style improvements (formal → informal register)
- Grammar corrections (compound structure preferences)
- Cultural adaptations (localization choices)

#### TSV Editing Patterns
Tab-separated before/after comparison data:

**File Format:**
```
Original_Translation[TAB]Improved_Translation
De applicatie[TAB]Het programma
Een methode voor[TAB]Een werkwijze voor
```

**Creation Methods:**
1. Export before/after versions from CAT tool
2. Manual compilation of common corrections
3. Client feedback integration
4. Post-editing pattern analysis

### Learning Algorithm

#### Pattern Recognition
AI analyzes editing patterns to identify:

**Lexical Preferences:**
- Preferred terminology choices
- Synonym selections
- Register adjustments

**Structural Patterns:**
- Sentence structure preferences
- Compound word formation
- Punctuation style

**Style Adaptations:**
- Formality level adjustments
- Cultural localization choices
- Industry-specific conventions

#### Application Method
During translation, AI:
1. **Identifies Similar Contexts**: Finds segments similar to tracked changes
2. **Applies Learned Patterns**: Uses preferred terminology and structures
3. **Maintains Consistency**: Applies patterns across entire document
4. **Evolves Understanding**: Incorporates new patterns from additional data

### File Management

#### Organization Structure
```
tracked_changes/
├── client_ABC_patterns.docx
├── technical_corrections.tsv
├── style_improvements.docx
└── terminology_updates.tsv
```

#### Best Practices
**Data Quality:**
- Clean, consistent editing patterns
- Remove contradictory corrections
- Focus on recurring issues
- Regular pattern updates

**File Organization:**
- Separate by client/domain
- Clear naming conventions
- Regular cleanup and updates
- Version control for pattern evolution

### Integration Workflow

#### Data Collection Phase
1. **Initial Translation**: Use Supervertaler for first-pass translation
2. **Human Review**: Professional review and editing
3. **Change Tracking**: Record all improvements made
4. **Pattern Export**: Save changes in tracked format

#### Learning Integration Phase
1. **Import Changes**: Load tracked changes into Supervertaler
2. **Pattern Analysis**: AI processes and learns from patterns
3. **Next Translation**: Apply learned patterns to new content
4. **Continuous Improvement**: Iterative refinement process

#### Quality Validation
1. **A/B Testing**: Compare translations with/without tracked changes
2. **Consistency Checking**: Verify pattern application accuracy
3. **Feedback Loop**: Incorporate results into pattern refinement
4. **Performance Metrics**: Track improvement in translation quality

### Advanced Features

#### Relevance Scoring
AI determines which tracked changes apply to current content:
- **Context Similarity**: Matching domain and terminology
- **Structural Relevance**: Similar sentence patterns
- **Semantic Alignment**: Meaning and intent matching

#### Conflict Resolution
When multiple patterns conflict:
- **Recency Priority**: Newer patterns take precedence
- **Frequency Weighting**: More common patterns preferred
- **Context Relevance**: Most contextually similar patterns applied

#### Pattern Evolution
- **Learning Decay**: Old patterns gradually lose influence
- **Adaptation Speed**: Quick learning from consistent feedback
- **Stability Maintenance**: Core patterns preserved across updates

---

## Translation Memory

Translation Memory (TM) integration provides consistency and efficiency by leveraging previously translated content and professional translation databases.

### Supported Formats

#### TMX (Translation Memory eXchange)
**Industry Standard**: Compatible with all major CAT tools
```xml
<?xml version="1.0" encoding="UTF-8"?>
<tmx version="1.4">
  <header>
    <prop type="x-filename">project.tmx</prop>
  </header>
  <body>
    <tu tuid="1">
      <tuv xml:lang="en">
        <seg>Hello world</seg>
      </tuv>
      <tuv xml:lang="nl">
        <seg>Hallo wereld</seg>
      </tuv>
    </tu>
  </body>
</tmx>
```

**Features:**
- Metadata preservation
- Multiple language pairs
- Timestamps and attributes
- Quality scoring

#### Tab-Separated TXT
**Simple Format**: Easy creation and editing
```
Source Text[TAB]Target Translation
Hello world[TAB]Hallo wereld
Good morning[TAB]Goedemorgen
```

**Use Cases:**
- Quick terminology lists
- Client-specific glossaries
- Manual TM creation
- Legacy data import

### TM Integration Process

#### Loading Translation Memory
1. **File Selection**: Browse and select TMX or TXT files
2. **Language Verification**: Confirm source/target language matching
3. **Import Process**: TM data loaded into memory for matching
4. **Status Confirmation**: Log shows successful import with entry count

#### Matching Algorithm
**Exact Matches**: 100% identical segments
- Instant application for consistency
- Highest confidence level
- Automatic terminology alignment

**Fuzzy Matches**: Similar but not identical segments
- Provides guidance for translation decisions
- Similarity scoring and ranking
- Context-aware matching

**Terminology Extraction**: Key term identification
- Domain-specific vocabulary recognition
- Consistent term translation
- Glossary integration

### TM Application Strategies

#### Pre-Translation Phase
**Exact Match Population:**
- Identify segments with 100% TM matches
- Apply translations automatically
- Mark segments for human verification

**Fuzzy Match Guidance:**
- Provide similar translation examples
- Highlight terminology consistency
- Guide AI translation decisions

#### Translation Enhancement
**Terminology Consistency:**
- Standardize key term translations
- Maintain brand/client terminology
- Apply glossary preferences

**Quality Assurance:**
- Cross-reference AI translations with TM
- Identify inconsistencies
- Suggest improvements based on TM data

### TM Creation and Maintenance

#### Building Translation Memory
**From Completed Projects:**
1. Export bilingual data from CAT tools
2. Clean and standardize entries
3. Remove outdated or incorrect translations
4. Merge with existing TM databases

**From Client Resources:**
1. Import client glossaries and term bases
2. Integrate brand-specific terminology
3. Add industry-standard translations
4. Incorporate regulatory requirements

#### Quality Control
**Regular Maintenance:**
- Remove duplicate entries
- Update obsolete translations
- Standardize formatting
- Verify language codes

**Content Validation:**
- Review translation accuracy
- Check terminology consistency
- Validate technical terms
- Ensure cultural appropriateness

### Integration with CAT Tools

#### Export to CAT Tools
Generated TMX files integrate directly with:

**memoQ:**
- Import as translation memory
- Apply in real-time during translation
- Leverage for quality assurance

**Trados Studio:**
- Add to project TM
- Use for fuzzy matching
- Integration with terminology database

**CafeTran Espresso:**
- Load as project memory
- Auto-substitution features
- Terminology management

#### Workflow Integration
1. **Pre-Project Setup**: Load relevant TM into CAT tool project
2. **Supervertaler Processing**: Generate translations with TM context
3. **TMX Import**: Add Supervertaler output to project TM
4. **Translation Phase**: Benefit from exact matches during CAT tool work
5. **Post-Project**: Update master TM with new translations

### Advanced TM Features

#### Multi-Source TM
Combine multiple TM sources:
- **Client TM**: Project-specific translations
- **Domain TM**: Industry-standard terminology
- **General TM**: Broad language patterns
- **Personal TM**: Individual translator preferences

#### TM Analytics
Track TM effectiveness:
- **Match Rates**: Percentage of exact/fuzzy matches
- **Leverage Statistics**: TM utilization metrics
- **Quality Impact**: Translation improvement measurement
- **ROI Analysis**: Time savings quantification

---

## AI Provider Settings

Supervertaler supports multiple AI providers, each with different models and capabilities optimized for various translation scenarios.

### OpenAI Integration

#### Available Models

**GPT-5** 🔥 *New in v2.3.1*
- **Reasoning Model**: Advanced logical analysis capabilities
- **Token Limit**: Up to 50,000 tokens for large documents
- **Strengths**: Complex content, technical documentation, nuanced translation
- **Special Features**: Automatic reasoning effort optimization
- **Best For**: Patent documents, legal texts, complex technical content

**GPT-4o**
- **Multimodal**: Text and image processing
- **Token Limit**: 128,000 tokens
- **Strengths**: Visual context integration, balanced performance
- **Best For**: Documents with figures, charts, diagrams

**GPT-4**
- **Reliable**: Consistent baseline performance  
- **Token Limit**: 32,000 tokens
- **Strengths**: General-purpose translation, stable output
- **Best For**: Standard translation work, consistent results

**GPT-4-turbo**
- **Enhanced**: Improved context handling
- **Token Limit**: 128,000 tokens
- **Strengths**: Large document processing, cost efficiency
- **Best For**: Long documents, batch processing

#### GPT-5 Special Considerations

**Automatic Parameter Handling:**
- Uses `max_completion_tokens` instead of `max_tokens`
- Temperature parameter automatically handled
- Reasoning effort set to "low" for optimal output

**Token Management:**
- Dynamic allocation based on content size
- Accounts for reasoning token overhead
- Minimum 32,000 tokens, up to 50,000 for large jobs

**Output Processing:**
- Automatic cleanup of formatting quirks
- Removes double numbering artifacts
- Ensures clean, professional output

### Claude Integration

#### Available Models

**Claude-3.5-Sonnet**
- **Creative Excellence**: Superior cultural adaptation
- **Context**: 200,000 tokens
- **Strengths**: Literary translation, marketing content, cultural nuance
- **Best For**: Creative content, transcreation, cultural adaptation

**Claude-3-Haiku**  
- **Speed**: Fast processing for simpler content
- **Context**: 200,000 tokens
- **Strengths**: Efficiency, cost-effective, quick turnaround
- **Best For**: Simple translations, batch processing, time-sensitive work

#### Claude Advantages
- **Cultural Sensitivity**: Excellent cross-cultural adaptation
- **Creative Content**: Superior for marketing and creative materials
- **Safety**: Built-in content filtering and ethical guidelines
- **Context Handling**: Excellent long-document processing

### Gemini Integration

#### Available Models

**Gemini-2.5-Pro**
- **Technical Excellence**: Strong analytical capabilities
- **Context**: 1,000,000+ tokens
- **Strengths**: Technical documentation, analytical content
- **Best For**: Technical manuals, scientific papers, data analysis

**Gemini-1.5-Flash**
- **Speed**: Rapid processing capabilities
- **Context**: 1,000,000+ tokens  
- **Strengths**: Efficiency, cost-effective, high throughput
- **Best For**: Large volume processing, simple content

#### Gemini Advantages
- **Massive Context**: Exceptional long-document handling
- **Technical Accuracy**: Strong performance on technical content
- **Cost Efficiency**: Competitive pricing for large volumes
- **Speed**: Fast processing for time-sensitive projects

### Model Selection Guidelines

#### Content-Based Selection

**Complex Technical Content:**
- **First Choice**: GPT-5 (reasoning capabilities)
- **Alternative**: Gemini-2.5-Pro (technical accuracy)

**Creative/Marketing Content:**
- **First Choice**: Claude-3.5-Sonnet (cultural adaptation)
- **Alternative**: GPT-4o (balanced creativity)

**Legal/Patent Documents:**
- **First Choice**: GPT-5 (precision and reasoning)
- **Alternative**: Claude-3.5-Sonnet (formal register)

**Large Volume/Batch Work:**
- **First Choice**: Gemini-1.5-Flash (efficiency)
- **Alternative**: Claude-3-Haiku (speed)

**Visual Content (Figures/Charts):**
- **First Choice**: GPT-4o (multimodal)
- **Alternative**: Gemini-2.5-Pro (analytical)

#### Project-Based Selection

**High-Stakes/Critical Projects:**
- Primary: GPT-5 or Claude-3.5-Sonnet
- Verification: Run same content through second provider
- Quality assurance through multi-provider comparison

**Time-Sensitive Projects:**
- Primary: Gemini-1.5-Flash or Claude-3-Haiku
- Optimize for speed while maintaining quality
- Use domain-specific prompts for accuracy

**Cost-Sensitive Projects:**
- Evaluate pricing per project requirements
- Consider token usage patterns
- Balance cost vs. quality requirements

### API Key Management

#### Security Best Practices
**File Protection:**
```
api_keys.txt (never commit to version control)
.gitignore entry for api_keys.txt
Restrict file permissions (600 on Unix systems)
```

**Key Rotation:**
- Regular API key updates
- Immediate rotation if compromised
- Separate keys for different projects/clients

#### Multi-Provider Setup
```
# api_keys.txt format
openai_api_key=your_openai_api_key_here
claude_api_key=your_anthropic_api_key_here  
google_api_key=your_google_ai_api_key_here
```

**Provider Availability:**
- Automatic detection of available providers
- Fallback options if primary provider unavailable
- Real-time model listing and updates

### Model Management Controls

Supervertaler provides two dedicated buttons for managing AI models: **"Refresh Models"** and **"List Models"**. Understanding the difference between these controls is essential for efficient workflow management.

#### 🔄 Refresh Models Button

**Primary Function**: Updates the model dropdown menu with current available models

**What It Does:**
- ✅ Updates the model dropdown with available models for selected provider
- ✅ Sets appropriate default model (e.g., `claude-3-5-sonnet-20241022` for Claude)
- ✅ Quick operation with minimal logging
- ✅ Essential for UI maintenance and troubleshooting

**Technical Behavior:**
- **Gemini**: Makes live API call to fetch current models from Google's servers
- **Claude**: Uses predefined model list (static)  
- **OpenAI**: Uses predefined model list (static)

**When to Use:**
- Model dropdown appears empty or shows outdated options
- After switching between AI providers
- When you want the latest Gemini models from Google
- UI appears unresponsive or broken
- After updating API keys

**Sample Output:**
```
Updated models for Gemini: 8 available
Updated models for Claude: 5 available
```

#### 📋 List Models Button

**Primary Function**: Displays comprehensive model information in the log panel

**What It Does:**
- ✅ Shows detailed model information in the log panel
- ✅ Provides model descriptions, capabilities, and metadata
- ✅ Functions as diagnostic tool for research and troubleshooting
- ✅ Verbose logging with comprehensive details

**Technical Behavior:**
- **Gemini**: Shows full model details (names, descriptions, capabilities, generation methods)
- **Claude**: Shows numbered list with multimodal capability indicators
- **OpenAI**: Shows numbered list with multimodal support information

**When to Use:**
- Research available models and their capabilities
- Determine which models support multimodal features (images)
- Troubleshoot API connectivity issues
- Copy exact model names for configuration
- Evaluate models for specific use cases

**Sample Output for Gemini:**
```
--- Listing Models for Gemini ---
Fetching Gemini models...
Model: models/gemini-2.5-pro-preview-05-06
  Display: Gemini 2.5 Pro Preview
  Desc: Advanced reasoning and code generation...
  Methods: ['generateContent']
  ✅ genContent

Found 8 Gemini models. For drawings, use multimodal.
--- Done Listing ---
```

**Sample Output for Claude:**
```
--- Listing Models for Claude ---
Available Claude models:
1. claude-3-5-sonnet-20241022
2. claude-3-5-haiku-20241022
3. claude-3-opus-20240229

Found 5 Claude models. All support multimodal capabilities.
--- Done Listing ---
```

#### Quick Comparison

| Feature | **🔄 Refresh Models** | **📋 List Models** |
|---------|----------------------|-------------------|
| **Purpose** | Update dropdown menu | Display model information |
| **Output** | UI dropdown update | Detailed log information |
| **Speed** | Fast | Slower (more data) |
| **Use Case** | UI maintenance | Research & diagnostics |
| **Logging** | Minimal | Comprehensive |

#### Best Practices

**For Regular Users:**
- Use "Refresh Models" when dropdown issues occur
- Use "List Models" to research model capabilities before starting projects
- Check log panel for error messages if buttons fail

**For Advanced Users:**
- Use "List Models" to understand multimodal support for image processing
- Monitor detailed output to diagnose API connectivity issues
- Document preferred models for different document types based on detailed information

### Performance Optimization

#### Token Usage Optimization
**GPT-5**: Automatic token allocation based on content size
**Claude**: Efficient context window utilization
**Gemini**: Massive context for minimal chunking

#### Speed Optimization
**Parallel Processing**: Multiple chunks processed simultaneously
**Smart Chunking**: Optimal segment grouping for each provider
**Connection Pooling**: Efficient API connection management

#### Cost Optimization
**Token Monitoring**: Track usage across providers
**Model Selection**: Choose cost-effective models for content type
**Batch Processing**: Group similar content for efficiency

---

## Troubleshooting

### Common Issues and Solutions

#### API and Connection Issues

**"API Key not found" or "Invalid API Key"**
- **Check**: `api_keys.txt` file exists and has correct format
- **Verify**: API key is valid and active
- **Test**: Use "List Models" button to verify connection
- **Solution**: Copy working API key from provider dashboard

**"Model not available" or "Model access denied"**
- **GPT-5 Access**: Ensure you have access to GPT-5 through OpenAI
- **Claude Access**: Verify Anthropic API access level
- **Gemini Access**: Check Google AI Studio permissions
- **Solution**: Contact provider for model access or use alternative model

**Connection timeout or network errors**
- **Network**: Verify internet connection stability
- **Firewall**: Check corporate firewall settings
- **VPN**: Try with/without VPN connection
- **Solution**: Use "Refresh Models" to test connection

#### File and Path Issues

**"File not found" or "Path does not exist"**
- **Absolute Paths**: Ensure file paths are complete and absolute
- **File Existence**: Verify all input files exist at specified locations
- **Permissions**: Check read permissions on input files
- **Solution**: Use "Browse" buttons to select files correctly

**"Unicode decode error" or "Encoding issues"**
- **File Encoding**: Save text files as UTF-8
- **Special Characters**: Ensure proper character encoding
- **BOM**: Remove Byte Order Mark if present
- **Solution**: Re-save files as UTF-8 without BOM

**Cross-platform path issues (Windows/Mac/Linux)**
- **Path Separators**: Use forward slashes (/) for compatibility
- **Drive Letters**: Windows drive letters may not work on other systems
- **Solution**: Use relative paths or Project Library for portability

#### Translation and Processing Issues

**GPT-5 returns empty translations**
- **Token Limit**: Automatic allocation should handle this (v2.3.1+)
- **Content Length**: Try reducing chunk size for very long segments
- **API Limits**: Check OpenAI usage limits and quotas
- **Solution**: Use smaller chunks or alternative model

**Double numbering in output (e.g., "1. 1. Text")**
- **GPT-5 Issue**: Fixed in v2.3.1 with automatic cleanup
- **Other Models**: Check system prompt configuration
- **Solution**: Update to v2.3.1 or manually clean output

**Inconsistent terminology across chunks**
- **Context**: Ensure Translation Memory is loaded
- **Instructions**: Add terminology guidelines to Custom Instructions
- **Chunk Size**: Reduce chunk size for better consistency
- **Solution**: Use tracked changes to learn terminology preferences

**AI refuses to translate certain content**
- **Content Policy**: Check for content that may violate AI policies
- **Language Support**: Verify source/target language combination
- **Model Limitations**: Try different AI provider/model
- **Solution**: Modify content or use alternative provider

#### Memory and Performance Issues

**"Out of memory" or application crashes**
- **Large Files**: Process in smaller chunks
- **System RAM**: Close other applications to free memory
- **Python Memory**: Restart application periodically for large jobs
- **Solution**: Increase chunk size or process files separately

**Slow processing speeds**
- **Network**: Check internet connection speed
- **API Limits**: Some providers have rate limits
- **Chunk Size**: Optimize chunk size for provider
- **Solution**: Adjust chunk size or use faster model variant

**GUI freezing or unresponsive**
- **Background Processing**: Translation runs in background thread
- **Large Jobs**: Very large files may take time
- **System Resources**: Check CPU and memory usage
- **Solution**: Wait for completion or restart if necessary

### Advanced Troubleshooting

#### Debug Information

**Session Reports**
Every translation generates a detailed report including:
- Complete AI prompts sent
- API response information
- Processing statistics
- Error messages and warnings
- Configuration settings used

**Log Analysis**
Processing log shows:
- Real-time status updates
- API call details
- Error messages and warnings
- Performance statistics
- File processing progress

#### GPT-5 Specific Debugging

**Enhanced Diagnostic System (v2.3.1)**
```
[OpenAI Translator] DEBUG - Response object type: <class 'openai.types.chat.chat_completion.ChatCompletion'>
[OpenAI Translator] DEBUG - First choice finish_reason: stop
[OpenAI Translator] DEBUG - Usage: completion_tokens=3447, reasoning_tokens=1088
[OpenAI Translator] DEBUG - Raw response length: 10879 chars
```

**Finish Reason Analysis:**
- **"stop"**: Normal completion ✓
- **"length"**: Hit token limit (should be automatic in v2.3.1)
- **"content_filter"**: Content policy violation
- **"function_call"**: Unexpected function call

**Token Usage Monitoring:**
- **Reasoning Tokens**: GPT-5 internal thinking (not in output)
- **Completion Tokens**: Actual translation output
- **Total Tokens**: Combined usage for billing

#### Getting Help

**Information to Provide:**
1. Supervertaler version number
2. Operating system (Windows/Mac/Linux)
3. Python version
4. AI provider and model used
5. Error message from log
6. Session report (if generated)
7. Input file sample (if not confidential)

**Common Resolution Steps:**
1. Update to latest Supervertaler version
2. Verify API key validity
3. Test with different AI provider/model
4. Check file encoding and format
5. Try smaller chunk size
6. Review session report for details

**Community Resources:**
- GitHub Issues for bug reports
- Documentation wiki for guides
- User community for tips and tricks
- Professional support for enterprise users

---

## Advanced Tips

### Workflow Optimization

#### Project Setup Strategies

**Client-Specific Configurations:**
Create dedicated project configurations for each client:
```
Client_ABC_TechnicalManuals/
├── project_config.json (language pair, preferred models)
├── translation_memory.tmx (client terminology)
├── custom_instructions.txt (style guidelines)
├── tracked_changes.docx (editing patterns)
└── custom_prompts/ (domain-specific prompts)
```

**Content-Type Templates:**
Establish templates for common content types:
- **Legal Documents**: Formal prompts, legal TM, conservative models
- **Marketing Materials**: Creative prompts, cultural adaptation focus
- **Technical Manuals**: Safety-focused prompts, technical terminology
- **Medical Content**: Regulatory compliance, medical terminology

#### Batch Processing Strategies

**Sequential Processing:**
For related documents, process in sequence to maintain consistency:
1. Load comprehensive TM with all previous translations
2. Process documents in logical order
3. Add each output TMX to master TM database
4. Use accumulated knowledge for subsequent documents

**Parallel Processing:**
For independent documents:
- Process simultaneously using different AI providers
- Compare results for quality assurance
- Identify best-performing provider for content type

### Quality Assurance Techniques

#### Multi-Provider Validation

**Critical Content Double-Check:**
```python
# Workflow for high-stakes translation
1. Primary translation: GPT-5 (reasoning capability)
2. Secondary validation: Claude-3.5-Sonnet (creative accuracy)
3. Compare outputs for consistency
4. Highlight discrepancies for human review
```

**Domain Expertise Verification:**
- **Technical**: Gemini-2.5-Pro for analytical accuracy
- **Creative**: Claude-3.5-Sonnet for cultural nuance
- **Legal**: GPT-5 for precision and reasoning
- **Medical**: Multiple providers with regulatory focus

#### Context Optimization

**Layered Context Strategy:**
```
Base Layer: Domain-specific Translation Memory
Enhancement Layer: Project-specific Custom Instructions  
Learning Layer: Tracked Changes from Previous Work
Visual Layer: Document Images and Figures
Prompt Layer: Domain-Specific System Prompts
```

**Context Quality Metrics:**
- **TM Coverage**: Percentage of segments with TM matches
- **Instruction Relevance**: Custom instructions aligned with content
- **Change Pattern Applicability**: Tracked changes relevant to current work
- **Visual Integration**: Images properly linked to text references

### Advanced Feature Utilization

#### Custom Prompt Engineering

**Template Variables Mastery:**
```
You are an expert {source_lang} to {target_lang} translator specializing in {domain}.

CRITICAL REQUIREMENTS for {client_name}:
- Use terminology from attached TM exclusively
- Maintain {formality_level} register throughout
- Follow {style_guide} conventions
- Convert measurements to {unit_system}

DOMAIN-SPECIFIC FOCUS:
- {domain_specific_requirement_1}
- {domain_specific_requirement_2}
- {domain_specific_requirement_3}
```

**Dynamic Prompt Adaptation:**
- Modify prompts based on content analysis
- Adjust formality level based on source text register
- Emphasize relevant specializations (technical/legal/medical)
- Include client-specific terminology requirements

#### Translation Memory Strategies

**TM Hierarchy Management:**
```
Priority 1: Client-specific project TM (exact matches)
Priority 2: Domain-specific master TM (terminology)
Priority 3: General professional TM (common phrases)
Priority 4: Personal translation database (style preferences)
```

**TM Quality Enhancement:**
- Regular cleanup of outdated entries
- Standardization of term variations
- Integration of client feedback
- Continuous improvement through tracked changes

#### Tracked Changes Optimization

**Pattern Collection Strategy:**
```
Source Category: Common editing patterns
- Terminology standardization
- Style consistency improvements
- Grammar and syntax corrections
- Cultural adaptation choices

Application Method:
- Categorize changes by pattern type
- Weight patterns by frequency and recency  
- Apply contextually relevant patterns
- Monitor pattern effectiveness
```

**Learning Acceleration:**
- Focus on high-frequency corrections
- Document rationale for major changes
- Create targeted correction databases
- Regular pattern review and refinement

### Professional Integration

#### CAT Tool Ecosystem

**memoQ Integration Workflow:**
1. **Pre-translation**: Export segments for Supervertaler processing
2. **AI Translation**: Process with optimal context and prompts
3. **TMX Integration**: Import generated TMX into project
4. **Quality Layer**: Use exact matches, review fuzzy matches
5. **Post-editing**: Refine with memoQ's built-in tools

**Trados Studio Integration:**
1. **Project Setup**: Configure with Supervertaler TMX
2. **Batch Processing**: Process multiple files with consistent settings
3. **Terminology Integration**: Combine with existing termbases
4. **Quality Assurance**: Leverage Trados QA with AI translations

#### Enterprise Deployment

**Team Collaboration:**
- Shared Project Library for team consistency
- Centralized TM and terminology management
- Standardized custom prompt libraries
- Quality metrics and reporting

**Client Delivery:**
- Professional session reports for transparency
- Comprehensive TMX deliverables
- Quality assurance documentation
- Process documentation for client confidence

### Performance Optimization

#### System Resource Management

**Memory Optimization:**
- Process large documents in optimal chunks
- Regular garbage collection for Python memory management
- Close unnecessary applications during large jobs
- Monitor system resources during processing

**Network Optimization:**
- Stable internet connection for API reliability
- Consider provider geographic regions for speed
- Monitor API rate limits and usage
- Implement retry logic for network issues

#### Cost Management

**Token Usage Optimization:**
- Monitor per-provider token consumption
- Optimize chunk sizes for cost efficiency
- Use appropriate models for content complexity
- Track ROI metrics for different providers

**Provider Selection Economics:**
```
Cost Factors:
- Token pricing per provider
- Processing speed (time value)
- Quality output (reduced post-editing)
- API reliability (reduced retries)

Quality-Cost Balance:
- Use premium models (GPT-5, Claude-3.5) for critical content
- Use efficiency models (Haiku, Flash) for simple content  
- Balance cost against post-editing time savings
```

---

*This comprehensive user guide covers all aspects of Supervertaler v2.3.1. For additional support or advanced enterprise features, please contact the development team.*