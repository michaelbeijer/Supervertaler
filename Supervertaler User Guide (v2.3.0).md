# Supervertaler User Guide
## Version 2.3.0 - Complete Documentation & Quick Start

---

## 🚀 Quick Navigation
- **[⚡ Quick Start](#-5-minute-quick-start)** - Get up and running fast!
- **[📖 Complete Guide](#complete-user-guide)** - Comprehensive documentation
- **[🆕 What's New in v2.3.0](#whats-new-in-v230)** - Latest features
- **[🎛️ Project Library](#project-library)** - Revolutionary workspace management
- **[📁 Prompt Library](#custom-prompt-library)** - Domain-specific expertise
- **[🆘 Troubleshooting](#troubleshooting)** - Common issues and solutions

---

## What's New in v2.3.0

### 🎯 Revolutionary Project Library
- **Complete Workspace Management**: Save and restore entire application configurations
- **Cross-Platform Support**: Clickable folder paths that work on Windows, macOS, and Linux
- **Instant Project Switching**: Load complete settings with one click
- **Professional Organization**: JSON-based project storage with timestamps

### 🎓 Domain-Specific Prompt Collections
Eight new professionally crafted prompt sets for specialized translation:
- **Patent Translation Specialist**: Technical precision and legal compliance
- **Medical Translation Specialist**: Patient safety and regulatory accuracy
- **Legal Translation Specialist**: Juridical precision and formal register
- **Financial Translation Specialist**: Banking terminology and market conventions
- **Technical Translation Specialist**: Engineering accuracy and safety warnings
- **Marketing & Creative Translation**: Cultural adaptation and brand consistency
- **Cryptocurrency & Blockchain Specialist**: DeFi protocols and Web3 terminology
- **Gaming & Entertainment Specialist**: Cultural localization and user experience

### ✨ Enhanced User Experience
- **Lightning Bolt Indicators**: ⚡ symbols show active prompts clearly
- **Renamed Interface**: "Advanced System Prompts" → "Prompt Library" for clarity
- **Consistent Visual Hierarchy**: Project Library ↔ Custom Prompt Library ↔ Prompt Library
- **Professional Tooltips**: Enhanced guidance throughout the interface

---

## ⚡ 5-Minute Quick Start

### Step 1: Install Dependencies (2 minutes)
```bash
pip install google-generativeai anthropic openai pillow
```
**Note**: Install only what you need based on your AI provider choice.

### Step 2: Get API Keys (2 minutes)
Choose at least one provider and get your API key:

**🤖 Google Gemini** (Recommended for beginners)
- Visit: https://aistudio.google.com/
- Click "Get API Key" → Create new key
- Copy the key

**🧠 Claude (Anthropic)** (Best for creative content)
- Visit: https://console.anthropic.com/
- Create account → API Keys → Generate
- Add billing credits
- Copy the key

**💬 OpenAI** (Most familiar)
- Visit: https://platform.openai.com/
- Account → API Keys → Create new
- Add billing information  
- Copy the key

### Step 3: Configure Supervertaler (1 minute)
1. **Download**: Get `Supervertaler_v2.3.0.py`
2. **First Run**: Execute the file to create `api_keys.txt`
3. **Add Key**: Edit `api_keys.txt`, uncomment and fill your API key:
```
google = your_google_key_here
#claude = your_claude_key_here  
#openai = your_openai_key_here
```
4. **Launch**: Run `python Supervertaler_v2.3.0.py`

---

## 🎯 Your First Translation (5 minutes)

### Prepare Input File
Create a text file `sample.txt` with one sentence per line:
```
Welcome to our new product.
This software will change your workflow.
Please refer to Figure 1 for details.
Contact support if you need assistance.
```

### Run Translation
1. **Launch Supervertaler** - You'll see the professional 3-panel interface
2. **Operation Mode** - Select "Translate" (default)
3. **Input File** - Browse and select your `sample.txt`
4. **Output File** - Choose where to save results
5. **Languages** - Set Source: "English", Target: "Spanish" 
6. **AI Provider** - Select your configured provider
7. **Start Process** - Click the button and watch the progress!

### Check Results
- **Text File**: Tab-separated source and translations
- **TMX File**: Translation memory format for CAT tools
- **Processing Log**: Detailed status in bottom-right panel

---

## 🎨 Explore the New Libraries (10 minutes)

### Understanding the Interface
**Professional 3-Panel Design**:
- **Left Panel**: All controls and settings (resizable)
- **Top Right**: Information and guidance (larger display)
- **Bottom Right**: Real-time processing log

### Access the Prompt Library
1. **Expand Section**: Click "⚙️ Prompt Library (Click to expand/collapse)"
2. **Four Tabs Available**:
   - **Translation Prompt**: Control AI translation behavior
   - **Proofreading Prompt**: Control AI proofreading behavior  
   - **📁 Custom Prompt Library**: Save and manage your custom prompts
   - **📂 Project Library**: NEW! Complete workspace management

### Try Domain-Specific Prompts

#### Load a Professional Prompt Set
1. **Switch to 📁 Custom Prompt Library tab**
2. **Browse Available Sets**: See the 8 new domain-specific collections
3. **Select**: "Medical Translation Specialist" or your preferred domain
4. **Load**: Click "📂 Load Selected"
5. **Active Indicator**: Notice the ⚡ lightning bolt showing it's active

#### Create Your Own Project
1. **Switch to 📂 Project Library tab**
2. **Configure Settings**: Set up your languages, provider, file paths
3. **Save Project**: Enter name like "Medical Documents Project"
4. **Click**: "💾 Save Current Project"
5. **Success**: See your project in the list with timestamp!

---

## 🔄 Your First Proofreading (5 minutes)

### Prepare Proofreading File  
Create `proofread_sample.txt` with tab-separated content:
```
Hello world	Hola mundo
How are you?	Como estas?
Good morning	Buenos dias
The weather is nice	El clima esta bien
```

### Run Proofreading
1. **Change Mode**: Select "Proofread" 
2. **Input File**: Browse and select your proofreading file
3. **Same Settings**: Keep your language and AI provider
4. **Process**: Click "Start Process"

### Review Improvements
The AI will:
- Fix spelling errors (missing accents)
- Improve fluency and naturalness  
- Provide explanations for changes
- Maintain original meaning

---

## Complete User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation & Setup](#installation--setup)
3. [Getting Started](#getting-started)
4. [Prompt Library](#prompt-library)
5. [Custom Prompt Library](#custom-prompt-library)
6. [Project Library](#project-library)
7. [Translation Mode](#translation-mode)
8. [Proofreading Mode](#proofreading-mode)
9. [Context Sources](#context-sources)
10. [Tracked Changes](#tracked-changes)
11. [Document Images](#document-images)
12. [Translation Memory](#translation-memory)
13. [AI Provider Settings](#ai-provider-settings)
14. [Troubleshooting](#troubleshooting)
15. [Advanced Tips](#advanced-tips)

---

## Introduction

Supervertaler is a professional AI-powered translation and proofreading application that leverages multiple Large Language Models (LLMs) and context sources to deliver highly accurate translations. Version 2.3.0 introduces revolutionary **Project Library** functionality and **domain-specific prompt collections** alongside an enhanced user interface.

### Key Features
- **Dual Operation Modes**: Translation and Proofreading with specialized workflows
- **Project Library**: Complete workspace configuration management with cross-platform support
- **Domain-Specific Prompts**: 8 professionally crafted prompt collections for specialized translation
- **Custom Prompt Library**: Create, save, and manage specialized system prompts
- **Advanced System Prompt Editor**: Full control over AI behavior with template variables
- **Multiple AI Providers**: Support for Claude, Gemini, and OpenAI models
- **Rich Context Integration**: Translation Memory, tracked changes, and figure references
- **Multimodal Processing**: Automatic image injection for figure references
- **Professional GUI**: 3-panel resizable interface with intuitive design
- **Multicontextual Approach**: Leverages multiple context sources for superior accuracy

### What Makes Supervertaler Unique
- **Multicontextual Intelligence**: Unlike simple AI translation tools, Supervertaler combines Translation Memory, tracked changes, visual context, and domain expertise
- **Professional Workflow Management**: Complete project management with instant workspace switching
- **Domain Expertise**: Built-in specialized knowledge for medical, legal, technical, financial, and other professional fields
- **Quality-Focused Design**: Every feature designed to maximize translation accuracy and consistency

---

## Installation & Setup

### System Requirements
- **Python**: 3.10 or higher (3.11+ recommended)
- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimum 4GB RAM (8GB+ recommended for large documents)
- **Storage**: 500MB free space for application and dependencies

### Installation Steps

1. **Download Supervertaler**
   - Obtain the latest `Supervertaler_v2.3.0.py` file
   - Place it in your desired working directory

2. **Install Python Dependencies**
   ```bash
   pip install google-generativeai anthropic openai pillow tkinter
   ```
   
   **Note**: Install only the providers you plan to use:
   - `google-generativeai` for Gemini models
   - `anthropic` for Claude models  
   - `openai` for OpenAI/ChatGPT models
   - `pillow` for image processing (optional but recommended)

3. **Configure API Keys**
   - Run Supervertaler once to generate the `api_keys.txt` template
   - Edit `api_keys.txt` with your API keys:
   ```
   #google = YOUR_GOOGLE_API_KEY_HERE
   #claude = YOUR_CLAUDE_API_KEY_HERE  
   #openai = YOUR_OPENAI_API_KEY_HERE
   ```
   - Uncomment and fill the lines for providers you want to use
   - At least one API key is required

4. **Launch Application**
   ```bash
   python Supervertaler_v2.3.0.py
   ```

### API Key Setup Guide

#### Google Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API Key" and create a new key
4. Copy the key to your `api_keys.txt` file

#### Anthropic Claude API Key  
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Create an account and verify your email
3. Navigate to "API Keys" and generate a new key
4. Add credits to your account for usage
5. Copy the key to your `api_keys.txt` file

#### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign in or create an account
3. Go to "API Keys" and create a new secret key
4. Add billing information and credits
5. Copy the key to your `api_keys.txt` file

---

## Getting Started

### First Launch
When you first start Supervertaler v2.3.0, you'll see a professional 3-panel interface:

- **Left Panel**: Main controls and settings
- **Top Right Panel**: Information and guidance  
- **Bottom Right Panel**: Processing log and status

### Basic Workflow

1. **Select Operation Mode**: Choose "Translate" or "Proofread"
2. **Choose Input File**: Browse for your source text file
3. **Set Output Location**: Specify where results should be saved
4. **Configure Languages**: Set source and target languages
5. **Select AI Provider**: Choose from available models
6. **Add Context Sources** (optional): TM files, tracked changes, images
7. **Start Processing**: Click "Start Process" to begin

### File Format Requirements

#### Translation Mode Input
- **Format**: Plain text file (.txt)
- **Structure**: One source sentence per line
```
This is the first sentence to translate.
Here is another sentence.
And a third one.
```

#### Proofreading Mode Input  
- **Format**: Tab-separated text file (.txt)
- **Structure**: Source{TAB}Target{TAB}Optional_Comment
```
Hello world	Hola mundo
How are you?	¿Cómo estás?	Previous comment here
Good morning	Buenos días
```

---

## Prompt Library

### Overview
The Prompt Library gives you complete control over the AI instructions that drive translation and proofreading behavior. This professional-grade feature allows customization for specific domains, styles, or requirements.

### Accessing the Editor
1. Click the **"⚙️ Prompt Library (Click to expand/collapse)"** section
2. The section expands to reveal a tabbed interface
3. Navigate between **Translation Prompt** and **Proofreading Prompt** tabs

### Template Variables
System prompts support dynamic variables that are automatically replaced:
- `{source_lang}`: Replaced with your selected source language
- `{target_lang}`: Replaced with your selected target language

**Example Usage**:
```
You are an expert {source_lang} to {target_lang} translator 
specializing in legal documents...
```

### Prompt Editor Features

#### Translation Prompt Tab
- **Purpose**: Controls AI behavior during translation tasks
- **Default Focus**: Generic professional translation approach
- **Customization**: Modify tone, style, terminology preferences
- **Output Format**: Specifies how translations should be structured

#### Proofreading Prompt Tab  
- **Purpose**: Controls AI behavior during proofreading tasks
- **Default Focus**: Accuracy checking and improvement suggestions
- **Change Detection**: Instructs AI on how to summarize modifications
- **Quality Metrics**: Defines evaluation criteria for revisions

#### Action Buttons
- **Preview Final Prompt**: See how your prompt looks with current language settings
- **Reset to Default**: Instantly restore the original system prompt
- **Template Variables Help**: Guidance on available dynamic variables

### Best Practices

#### Writing Effective Prompts
1. **Be Specific**: Clearly define the task and expectations
2. **Set Context**: Explain the document type and domain
3. **Define Quality**: Specify accuracy and style requirements  
4. **Structure Output**: Describe the exact format needed
5. **Use Examples**: Include sample input/output when helpful

#### Domain Specialization Examples

**Legal Documents**:
```
You are an expert {source_lang} to {target_lang} legal translator. 
Maintain precise legal terminology and formal register. 
Preserve all clause numbering and legal references exactly.
When uncertain about legal terms, indicate with [VERIFY: term].
```

**Medical Texts**:
```  
You are a specialized medical {source_lang} to {target_lang} translator.
Use established medical terminology from authoritative sources.
Preserve dosages, measurements, and medical codes exactly.
Maintain clinical precision while ensuring readability.
```

**Marketing Content**:
```
You are a creative {source_lang} to {target_lang} translator for marketing.
Adapt cultural references and idioms for the target market.
Maintain persuasive tone and emotional impact.
Ensure brand consistency and market-appropriate messaging.
```

---

## Custom Prompt Library

### Overview
The Custom Prompt Library allows you to create, save, and manage collections of specialized system prompts. This enables rapid switching between different translation approaches for various document types or clients.

### Accessing the Library
1. Open **Prompt Library** section
2. Click the **"📁 Custom Prompt Library"** tab
3. The library interface displays with management controls and saved prompt list

### Domain-Specific Prompt Collections (New in v2.3.0)

#### Available Collections
Supervertaler v2.3.0 comes with 8 professionally crafted domain-specific prompt sets:

1. **Patent Translation Specialist**
   - Technical precision and legal compliance
   - Proper handling of claims, figures, and technical drawings
   - Regulatory terminology and formal patent language

2. **Medical Translation Specialist**
   - Patient safety focus and regulatory compliance
   - Accurate medical terminology and dosage preservation
   - Clinical precision with readability balance

3. **Legal Translation Specialist**
   - Juridical precision and formal legal register
   - Proper handling of legal systems and terminology
   - Clause numbering and reference preservation

4. **Financial Translation Specialist**
   - Banking terminology and market conventions
   - Regulatory compliance and precision
   - Financial instrument and market-specific language

5. **Technical Translation Specialist**
   - Engineering precision and safety warnings
   - Technical specification accuracy
   - Proper handling of measurements and standards

6. **Marketing & Creative Translation**
   - Cultural adaptation and brand consistency
   - Creative localization and market appropriateness
   - Emotional impact and persuasive messaging

7. **Cryptocurrency & Blockchain Specialist**
   - DeFi protocols and Web3 terminology
   - Technical accuracy for blockchain concepts
   - Current crypto market language and conventions

8. **Gaming & Entertainment Specialist**
   - Cultural localization and user experience optimization
   - Gaming terminology and interface elements
   - Entertainment industry conventions

#### Lightning Bolt Indicators ⚡
Active prompts are clearly marked with lightning bolt symbols (⚡) throughout the interface, making it easy to see which specialized prompt set is currently loaded.

### Creating Custom Prompt Sets

#### Step-by-Step Process
1. **Design Your Prompts**:
   - Switch to "Translation Prompt" tab
   - Modify the prompt for your specific use case
   - Switch to "Proofreading Prompt" tab  
   - Customize the proofreading instructions
   - Test with preview functionality

2. **Save the Prompt Set**:
   - Return to "📁 Custom Prompt Library" tab
   - Enter a descriptive name in "Prompt Set Name" field
   - Click "💾 Save Current Prompts" button
   - Confirm success message

3. **Verify Storage**:
   - Check that your prompt set appears in the list
   - Note the automatic file creation in `custom_prompts/` folder

#### Naming Conventions
- **Be Descriptive**: Use clear, meaningful names
- **Include Context**: Mention document type or domain
- **Version Control**: Consider adding version indicators
- **Examples**: 
  - "Legal Contracts v1.2"
  - "Medical Research Papers"
  - "Marketing Materials - EU"
  - "Technical Documentation"

### Managing Prompt Sets

#### Loading Saved Prompts
1. **Browse Available Sets**: View all saved prompts in the list
2. **Select Target Set**: Click on the desired prompt name
3. **Load Prompts**: Click "📂 Load Selected" button
4. **Confirm Loading**: Check success message and verify prompt content
5. **Active Indicator**: Notice the ⚡ symbol indicating the active set

#### Deleting Prompt Sets
1. **Select Unwanted Set**: Click on the prompt to delete
2. **Delete Action**: Click "🗑️ Delete Selected" button  
3. **Confirm Deletion**: Respond "Yes" to confirmation dialog
4. **Verify Removal**: Check that set no longer appears in list

#### Default Prompts Option
- **"[Default System Prompts]"** always appears first in the list
- Loading this option restores original factory prompts
- Cannot be deleted (protected system option)
- Useful for reverting customizations

### File Organization

#### Storage Location
- **Directory**: `custom_prompts/` (created automatically)
- **Location**: Same folder as main application
- **Format**: JSON files with `.json` extension
- **Naming**: Matches your prompt set name

#### File Structure
Each saved prompt set creates a JSON file containing:
```json
{
  "name": "Your Prompt Set Name",
  "created": "2025-09-08 14:30:25", 
  "translate_prompt": "Your custom translation prompt...",
  "proofread_prompt": "Your custom proofreading prompt...",
  "version": "2.3.0"
}
```

#### Backup and Sharing
- **Backup**: Copy entire `custom_prompts/` folder
- **Share**: Send individual `.json` files to colleagues
- **Import**: Place `.json` files in `custom_prompts/` folder
- **Sync**: Use cloud storage for multi-device access

---

## Project Library

### Overview
The Project Library is a revolutionary new feature in v2.3.0 that provides complete workspace configuration management. Save and restore entire application states including languages, AI providers, file paths, prompt settings, and all context sources.

### Accessing the Project Library
1. Open **Prompt Library** section
2. Click the **"📂 Project Library"** tab
3. The project management interface displays with comprehensive controls

### Key Features

#### Complete State Serialization
- **Language Settings**: Source and target languages, chunk sizes
- **AI Provider Configuration**: Selected provider and model
- **File Paths**: Input files, output locations, all context sources
- **Prompt Settings**: Currently loaded custom prompts
- **Context Sources**: Translation Memory files, tracked changes, image folders
- **Custom Instructions**: Any additional guidance provided

#### Cross-Platform Support
- **Clickable Folder Paths**: Direct access to project directories
- **Windows**: Opens in File Explorer
- **macOS**: Opens in Finder  
- **Linux**: Opens in default file manager
- **Error Handling**: Graceful fallback if folder access fails

#### Professional Organization
- **JSON Storage**: Structured, readable project files
- **Timestamp Tracking**: Creation and modification dates
- **Version Compatibility**: Forward and backward compatibility
- **Intuitive Interface**: Clear visual hierarchy and controls

### Creating Projects

#### Step-by-Step Process
1. **Configure Your Workspace**:
   - Set up all your preferred settings (languages, AI provider, etc.)
   - Select input and output files
   - Load your preferred custom prompts
   - Add any context sources (TM files, images, etc.)
   - Add custom instructions if needed

2. **Save the Project**:
   - Switch to "📂 Project Library" tab
   - Enter a descriptive name in "Project Name" field
   - Click "💾 Save Current Project" button
   - Confirm success message

3. **Verify Creation**:
   - Check that your project appears in the list with timestamp
   - Note the automatic file creation in `projects/` folder
   - Test folder access by clicking the project name

#### Project Naming Best Practices
- **Client-Based**: "Acme Corp Legal Documents"
- **Domain-Based**: "Medical Research Translation"
- **Time-Based**: "Q4 2025 Marketing Campaign"
- **Content-Based**: "Patent Application Series"

### Managing Projects

#### Loading Projects
1. **Browse Available Projects**: View all saved projects in the list
2. **Preview Details**: See creation dates and quick info
3. **Select Project**: Click on the desired project name
4. **Load Configuration**: Click "📂 Load Selected Project" button
5. **Instant Restoration**: All settings are immediately applied

#### Deleting Projects
1. **Select Project**: Click on the project to remove
2. **Delete Action**: Click "🗑️ Delete Selected Project" button
3. **Confirm Deletion**: Respond "Yes" to confirmation dialog
4. **File Cleanup**: Both list entry and file are removed

#### Folder Access
- **Click Project Names**: Direct access to project directories
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Organized Structure**: Projects stored in dedicated `projects/` folder

### File Organization

#### Storage Structure
```
Supervertaler/
├── Supervertaler_v2.3.0.py
├── projects/
│   ├── Acme Corp Legal Documents.json
│   ├── Medical Research Translation.json
│   └── Patent Application Series.json
└── custom_prompts/
    ├── Legal Translation Specialist.json
    └── Medical Translation Specialist.json
```

#### Project File Format
```json
{
  "name": "Acme Corp Legal Documents",
  "created": "2025-09-08 14:30:25",
  "version": "2.3.0",
  "source_lang": "English",
  "target_lang": "Spanish", 
  "chunk_size": "100",
  "ai_provider": "claude",
  "ai_model": "claude-3.5-sonnet",
  "input_file": "/path/to/input.txt",
  "output_file": "/path/to/output.txt",
  "tm_file": "/path/to/memory.tmx",
  "tracked_changes_file": "/path/to/changes.docx",
  "images_folder": "/path/to/images/",
  "custom_instructions": "Use formal legal register...",
  "current_prompt_set": "Legal Translation Specialist"
}
```

### Professional Use Cases

#### Translation Agency Workflow
1. **Client Projects**: Separate configurations for each client
2. **Recurring Work**: Instant setup for regular translation projects
3. **Team Coordination**: Shared project configurations across translators
4. **Quality Consistency**: Standardized settings for similar document types

#### Corporate Translation Department
1. **Product Lines**: Dedicated projects for different product categories
2. **Compliance Projects**: Regulatory translation with specific requirements
3. **Multilingual Campaigns**: Coordinated approach across language pairs
4. **Brand Management**: Consistent voice and terminology across projects

#### Freelance Translator Efficiency
1. **Client Specialization**: Quick switching between different clients
2. **Domain Expertise**: Rapid access to specialized configurations
3. **Project Tracking**: Organized approach to ongoing work
4. **Quality Standards**: Consistent setup for professional deliverables

### Advanced Project Management

#### Version Control Integration
- **Git-Friendly**: JSON format works well with version control
- **Change Tracking**: Monitor project configuration evolution
- **Backup Strategy**: Regular commits of project configurations
- **Team Collaboration**: Shared repositories for project templates

#### Automation Possibilities
- **Batch Processing**: Load project, process files, save results
- **Quality Assurance**: Consistent settings reduce configuration errors
- **Workflow Integration**: Connect with existing business processes
- **Reporting**: Track project usage and translation volumes

---

## Translation Mode

### Purpose and Workflow
Translation Mode is designed for converting source language text into target language text with maximum accuracy and context awareness. It integrates multiple context sources and produces both text and TMX output files.

### Input Requirements

#### File Format
- **Extension**: `.txt` (plain text)
- **Encoding**: UTF-8 recommended
- **Structure**: One sentence or segment per line

#### Sample Input File
```
The new product features advanced technology.
Users can access the system through multiple interfaces. 
Data security remains our top priority.
Please refer to Figure 1A for the technical specifications.
```

### Processing Flow

1. **Text Ingestion**: Supervertaler reads your input file line by line
2. **TM Matching**: Exact matches from Translation Memory are applied first
3. **Context Assembly**: Relevant context from all sources is gathered
4. **Chunking**: Text is divided into optimal batch sizes for AI processing
5. **AI Translation**: Each chunk is sent to your selected AI provider
6. **Output Generation**: Results are compiled into text and TMX formats

### Context Integration

#### Translation Memory Priority
- **Exact Matches**: Applied immediately without AI processing
- **Fuzzy Matches**: Provided to AI as reference context
- **New Segments**: Translated by AI with TM context

#### Tracked Changes Context
- **Relevant Extraction**: Changes matching current content are identified
- **Context Injection**: Relevant changes are provided as translation examples
- **Terminology Consistency**: Helps maintain consistent term translation

#### Figure Reference Processing
- **Automatic Detection**: Lines referencing figures (e.g., "Figure 1A", "Fig. 2B")
- **Image Injection**: Corresponding images inserted before referenced lines
- **Multimodal Translation**: AI receives both text and visual context

### Output Files

#### Text Output (.txt)
**Format**: Source{TAB}Translation
```
The new product features advanced technology.	El nuevo producto cuenta con tecnología avanzada.
Users can access the system through multiple interfaces.	Los usuarios pueden acceder al sistema a través de múltiples interfaces.
Data security remains our top priority.	La seguridad de los datos sigue siendo nuestra máxima prioridad.
```

#### TMX Output (.tmx)  
**Purpose**: Translation Memory exchange format
**Content**: All exact matches plus new AI translations
**Exclusions**: Error segments and processing failures
**Usage**: Import into CAT tools or other TM systems

### Quality Optimization

#### Chunk Size Settings
- **Default**: 100 lines per batch
- **Small Documents**: Use smaller chunks (25-50 lines)
- **Large Documents**: Increase chunk size (150-200 lines)
- **Complex Content**: Reduce chunk size for better context

#### AI Provider Selection
- **Claude**: Excellent for creative and nuanced translations
- **Gemini**: Strong performance with technical content
- **OpenAI**: Balanced approach for general content

#### Context Source Optimization
- **High-Quality TM**: Clean, accurate Translation Memory improves results
- **Relevant Tracked Changes**: Include changes from similar document types
- **Appropriate Images**: Ensure figure images match text references

---

## Proofreading Mode

### Purpose and Workflow
Proofreading Mode is designed to review and improve existing translations, focusing on accuracy, fluency, and consistency. It compares source and target text to identify and correct issues.

### Input Requirements

#### File Format
- **Extension**: `.txt` (tab-separated text)
- **Structure**: Source{TAB}Target{TAB}Optional_Comment
- **Encoding**: UTF-8 recommended

#### Sample Input File
```
Hello world	Hola mundo	
How are you today?	¿Como estas hoy?	Missing accent on "Cómo"
The weather is nice.	El clima está bueno.	Check formality level
Please see Figure 2.	Consulte la Figura 2.	
```

### Processing Components

#### Source-Target Analysis
- **Accuracy Check**: Verification of meaning preservation
- **Completeness Review**: Ensuring no content is omitted
- **Terminology Consistency**: Checking term usage across document
- **Style Alignment**: Matching register and tone

#### Context Utilization
- **Previous Comments**: Integration of existing feedback
- **Tracked Changes**: Learning from revision patterns
- **Translation Memory**: Reference for consistent terminology
- **Domain Knowledge**: Application of specialized expertise

### AI Instructions

#### Standard Proofreading Tasks
1. **Accuracy Assessment**: Does the target convey the source meaning?
2. **Fluency Improvement**: Is the target natural in the target language?
3. **Terminology Validation**: Are technical terms correctly translated?
4. **Style Consistency**: Does the translation match the required register?
5. **Completeness Check**: Are all source elements present in the target?

#### Change Documentation
The AI is instructed to:
- **Identify Issues**: Specifically describe problems found
- **Explain Changes**: Provide rationale for modifications
- **Suggest Alternatives**: Offer multiple options when appropriate
- **Maintain Traceability**: Link changes to specific quality criteria

### Output Format

#### Revised Translation File
**Structure**: Source{TAB}Revised_Target{TAB}Combined_Comments

#### Comment Merging
- **Original Comments**: Preserved from input file
- **AI Comments**: Added explanations of changes made
- **Change Summary**: Consolidated view of all modifications

#### Sample Output
```
Hello world	Hola mundo	
How are you today?	¿Cómo estás hoy?	Missing accent on "Cómo" | PROOFREADER COMMENT: Added missing accent on "Cómo" and tilde on "estás" for correct Spanish spelling.
The weather is nice.	El tiempo está agradable.	Check formality level | PROOFREADER COMMENT: Changed "clima está bueno" to "tiempo está agradable" for more natural and formal register.
```

### Quality Metrics

#### Evaluation Criteria
- **Linguistic Accuracy**: Correct grammar, syntax, and spelling
- **Terminology Consistency**: Uniform translation of technical terms
- **Cultural Appropriateness**: Suitable for target language culture
- **Readability**: Natural flow and comprehension
- **Completeness**: All source information preserved

#### Change Classification
- **Critical**: Accuracy issues that change meaning
- **Important**: Fluency improvements for naturalness
- **Minor**: Style adjustments and preference changes
- **Optional**: Alternative expressions or variations

---

## Context Sources

### Overview
Context Sources are additional information that Supervertaler uses to improve translation and proofreading quality. These sources provide terminology, examples, and domain-specific knowledge that enhance AI performance.

### Translation Memory (TM)

#### Supported Formats
- **TMX Files**: Industry-standard Translation Memory eXchange format
- **TXT Files**: Tab-separated source{TAB}target format

#### TM Processing
1. **Exact Match Detection**: Identical source segments are replaced immediately
2. **Fuzzy Match Context**: Similar segments provided as reference
3. **Terminology Extraction**: Key terms identified for consistency
4. **Quality Filtering**: Only high-confidence matches are used

#### TM File Requirements
**TMX Format**: Standard XML structure with translation units
**TXT Format**: 
```
Source segment 1	Target segment 1
Source segment 2	Target segment 2
```

#### Best Practices
- **Clean Data**: Ensure TM contains accurate, reviewed translations
- **Domain Relevance**: Use TM from similar document types
- **Size Optimization**: Larger TM files provide better coverage
- **Regular Updates**: Keep TM current with latest terminology

### Tracked Changes

#### Purpose
Tracked Changes provide examples of how previous translations have been revised, helping the AI understand common improvement patterns and terminology preferences.

#### Supported Sources

**DOCX Files with Track Changes**:
- Microsoft Word documents with revision tracking enabled
- Automatically extracts insertions and deletions
- Provides before/after examples for learning

**TSV Files**:
- Tab-separated format: Original{TAB}Revised
- Manual compilation of revision examples
- Custom change documentation

#### Change Processing
1. **Extraction**: Changes are identified and catalogued
2. **Relevance Filtering**: Only changes matching current content are selected
3. **Context Injection**: Relevant changes are provided to AI as examples
4. **Pattern Learning**: AI learns from revision patterns

#### Sample Tracked Changes
```
Original Text: The system is very good.
Final Text: The system performs exceptionally well.

Original Text: Please see the attached file.  
Final Text: Please refer to the attached document.
```

### Document Images

#### Multimodal Processing
Supervertaler supports automatic image injection when text references figures, diagrams, or illustrations. This provides crucial visual context for accurate translation of technical content.

#### Image Requirements
- **Formats**: PNG, JPG, JPEG, WebP, GIF
- **Naming**: Must match figure references in text
- **Location**: All images in single "Document Images Folder"

#### Reference Matching
The system automatically normalizes and matches:
- "Figure 1A" ↔ "fig1a.png"
- "Fig. 2-B" ↔ "Figure_2B.jpg"  
- "Figuur 3" ↔ "figuur_3.webp"

#### Processing Workflow
1. **Text Scanning**: System identifies figure references in source text
2. **Image Location**: Corresponding images are found in specified folder
3. **Context Injection**: Images are inserted before relevant text lines
4. **Multimodal Translation**: AI receives both text and visual information

#### AI Provider Support
- **Gemini**: Native PIL image processing
- **Claude**: Base64 image encoding
- **OpenAI**: Data URL image_url format

### Custom Instructions

#### Purpose
Custom Instructions allow you to provide additional guidance specific to your translation project, client requirements, or domain expertise.

#### Usage Examples
- **Terminology Preferences**: "Use 'software' instead of 'programme'"
- **Style Guidelines**: "Maintain formal register throughout"
- **Cultural Adaptations**: "Adapt currency references to target market"
- **Technical Requirements**: "Preserve all code snippets unchanged"

#### Integration
Custom Instructions are automatically appended to the AI system prompt, ensuring they influence all translation decisions while maintaining the core prompt structure.

---

## AI Provider Settings

### Supported Providers

#### Claude (Anthropic)
- **Models**: Claude-3.5-Sonnet, Claude-3-Haiku, Claude-3-Opus
- **Strengths**: Creative translations, nuanced understanding
- **Best For**: Literary texts, marketing content, cultural adaptation
- **Token Limits**: Up to 200K tokens context window
- **Multimodal**: Full image support via base64 encoding

#### Gemini (Google)
- **Models**: Gemini-1.5-Pro, Gemini-1.5-Flash, Gemini-1.0-Pro
- **Strengths**: Technical accuracy, structured output
- **Best For**: Technical documentation, scientific texts
- **Token Limits**: Up to 2M tokens context window  
- **Multimodal**: Native PIL image processing

#### OpenAI
- **Models**: GPT-4, GPT-4-Turbo, GPT-3.5-Turbo
- **Strengths**: Balanced performance, reliability
- **Best For**: General content, business documents
- **Token Limits**: Varies by model (4K-128K tokens)
- **Multimodal**: Image support via data URLs

### Model Selection

#### Performance Considerations
- **Quality vs Speed**: Higher-end models provide better quality but slower processing
- **Context Window**: Larger windows allow more context but cost more
- **Multimodal Needs**: Choose models supporting image processing when needed
- **Budget Constraints**: Balance quality requirements with API costs

#### Recommended Configurations

**High-Quality Translation**:
- Claude-3.5-Sonnet for creative content
- Gemini-1.5-Pro for technical content
- GPT-4-Turbo for balanced needs

**Fast Processing**:  
- Claude-3-Haiku for quick turnaround
- Gemini-1.5-Flash for speed with quality
- GPT-3.5-Turbo for basic needs

**Multimodal Requirements**:
- All current models support image processing
- Gemini offers best image understanding
- Claude provides excellent text-image integration

### API Configuration

#### Rate Limiting
- Supervertaler automatically handles API rate limits
- Processing pauses and resumes as needed
- Error recovery and retry mechanisms built-in

#### Cost Optimization
- **Chunk Size**: Larger chunks reduce API calls but may exceed token limits
- **Context Filtering**: Only relevant context is included to minimize tokens
- **Model Selection**: Choose appropriate model for quality/cost balance

#### Error Handling
- **Network Issues**: Automatic retry with exponential backoff
- **Token Limits**: Graceful degradation with context trimming
- **API Errors**: Clear error messages and recovery suggestions

---

## Troubleshooting

### Common Issues and Solutions

#### Application Won't Start
**Problem**: Error messages on launch or missing dependencies

**Solutions**:
1. **Check Python Version**: Ensure Python 3.10+ is installed
2. **Install Dependencies**: Run `pip install` commands for missing packages
3. **Verify API Keys**: Ensure at least one valid API key is configured
4. **Check File Permissions**: Ensure write access to application directory

#### No AI Providers Available
**Problem**: "No working AI providers available!" message

**Solutions**:
1. **Verify API Keys**: Check `api_keys.txt` for correct format and valid keys
2. **Test API Access**: Use provider's official tools to verify key functionality  
3. **Check Network**: Ensure internet connection and firewall settings
4. **Install Libraries**: Confirm provider-specific Python packages are installed

#### Translation Quality Issues
**Problem**: Poor translation results or inappropriate output

**Solutions**:
1. **Use Domain-Specific Prompts**: Load appropriate prompt set from Custom Prompt Library
2. **Review System Prompts**: Customize prompts for your domain and requirements
3. **Optimize Context**: Ensure TM and tracked changes are high quality and relevant
4. **Adjust Chunk Size**: Smaller chunks for complex content, larger for simple text
5. **Try Different Models**: Some models perform better for specific content types

#### Project Library Issues
**Problem**: Projects not saving or loading correctly

**Solutions**:
1. **Check Permissions**: Ensure write access to `projects/` folder
2. **Verify File Paths**: Ensure all referenced files still exist
3. **Review JSON Format**: Check project files for corruption
4. **Folder Access**: Verify cross-platform folder opening works

#### File Processing Errors
**Problem**: Input files not processing correctly

**Solutions**:
1. **Check File Format**: Ensure UTF-8 encoding and correct structure
2. **Verify File Paths**: Ensure no special characters in file names or paths
3. **Review File Size**: Very large files may need smaller chunk sizes
4. **Validate Content**: Check for unusual characters or formatting issues

#### Memory or Performance Issues
**Problem**: Application runs slowly or crashes with large files

**Solutions**:
1. **Reduce Chunk Size**: Process smaller batches to reduce memory usage
2. **Close Other Applications**: Free up system memory for processing
3. **Check Available Storage**: Ensure sufficient disk space for output files
4. **Monitor API Limits**: Some providers have rate limits that slow processing

### Advanced Troubleshooting

#### Log Analysis
- **Processing Log**: Check the bottom-right panel for detailed status messages
- **Error Patterns**: Look for recurring error types or specific content issues
- **Context Clues**: Error messages often indicate the specific problem area

#### Debug Mode
1. **Enable Detailed Logging**: Monitor console output for technical details
2. **Test with Small Files**: Isolate issues using minimal test cases
3. **Check Individual Components**: Test TM, tracked changes, and images separately

#### Network and API Issues
- **Firewall Configuration**: Ensure AI provider APIs are not blocked
- **Proxy Settings**: Configure proxy if required for internet access
- **API Status**: Check provider status pages for service interruptions

---

## Advanced Tips

### Optimization Strategies

#### Prompt Engineering
- **Use Domain Prompts**: Start with provided domain-specific prompts as templates
- **Iterative Refinement**: Test and improve prompts based on results
- **A/B Testing**: Compare different prompt versions for quality
- **Template Variables**: Use `{source_lang}` and `{target_lang}` for flexibility

#### Context Management
- **TM Quality**: Invest time in cleaning and organizing Translation Memory
- **Relevant Changes**: Include only tracked changes from similar document types  
- **Image Organization**: Use consistent naming for reliable figure matching
- **Custom Instructions**: Provide specific, actionable guidance for AI

#### Workflow Efficiency
- **Project Library**: Use projects for consistent workflow setup
- **Batch Processing**: Process similar documents together for consistency
- **Prompt Libraries**: Create and maintain prompt sets for different use cases
- **Quality Checkpoints**: Review sample outputs before processing large batches
- **Backup Strategies**: Maintain copies of custom prompts and project configurations

### Professional Workflows

#### Translation Agency Setup
1. **Client-Specific Projects**: Create project configurations for each major client
2. **Domain-Specific Prompts**: Use appropriate prompt sets for different content types
3. **Quality Tiers**: Different configurations for draft, standard, and premium services
4. **Team Coordination**: Share project libraries and best practices across translators

#### Large Document Processing
1. **Pre-Processing**: Clean and structure input files for optimal processing
2. **Staged Approach**: Process documents in logical sections or chapters
3. **Quality Control**: Regular spot-checks during long processing runs
4. **Post-Processing**: Review and refine outputs before final delivery

#### Multilingual Projects
1. **Consistent Projects**: Use similar project structures across language pairs
2. **Cultural Adaptation**: Adjust prompts for different target cultures
3. **Terminology Management**: Maintain consistent term translation across languages
4. **Quality Standards**: Apply uniform quality criteria regardless of language pair

### Integration Possibilities

#### CAT Tool Integration
- **TMX Export**: Import Supervertaler TMX output into CAT tools
- **Terminology Extraction**: Use outputs to build glossaries and termbases
- **Quality Metrics**: Combine AI translation with human post-editing workflows

#### Custom Automation
- **Project-Based Scripts**: Automate file processing using saved project configurations
- **API Integration**: Potential for custom integrations with existing systems
- **Output Processing**: Automatically format or convert output files as needed

#### Quality Assurance
- **Comparison Tools**: Use diff tools to compare versions and track changes
- **Metrics Collection**: Track translation quality and consistency over time
- **Feedback Loops**: Incorporate client feedback into prompt improvement cycles

### Cross-Platform Considerations

#### Windows Optimization
- **PowerShell Integration**: Use Windows PowerShell for advanced automation
- **File Association**: Set up file associations for quick project access
- **Network Drives**: Consider network storage for team collaboration

#### macOS Features
- **Finder Integration**: Take advantage of macOS folder organization
- **Spotlight Search**: Use macOS search to find project files quickly
- **Services Menu**: Potential for macOS Services integration

#### Linux Compatibility
- **File Manager Integration**: Works with various Linux desktop environments
- **Shell Scripting**: Advanced automation possibilities with bash/zsh
- **Package Management**: Easy installation via pip and system package managers

---

## 🎉 Congratulations!

You're now ready to use Supervertaler v2.3.0 effectively! The combination of powerful AI translation, domain-specific expertise, complete project management, and professional interface design provides a comprehensive solution for modern translation needs.

### Key Success Factors
- **Experiment and Iterate**: Try different prompts, test various settings, and build a library of specialized configurations
- **Leverage Domain Expertise**: Use the built-in domain-specific prompts as starting points for your specialized needs
- **Organize with Projects**: Take advantage of the Project Library for consistent, professional workflow management
- **Quality Focus**: Every feature is designed to maximize translation accuracy and consistency

### Next Steps
1. **Start with Domain Prompts**: Load an appropriate domain-specific prompt set
2. **Create Your First Project**: Save your workspace configuration for future use
3. **Build Custom Prompts**: Develop specialized prompts for your unique requirements
4. **Establish Workflows**: Use projects and prompts to create consistent professional processes

**Happy Translating!** 🌍✨

---

*Supervertaler v2.3.0 - Professional AI Translation with Revolutionary Project Management and Domain Expertise*

**Contact**: For support, feedback, or suggestions, email [info@michaelbeijer.co.uk](mailto:info@michaelbeijer.co.uk)
