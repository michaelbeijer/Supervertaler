# AI Assistant Guide

## Overview

The AI Assistant is an integrated conversational AI tool within Supervertaler's Prompt Manager that helps you:
- Analyze translation projects
- Generate domain and project-specific prompts
- Get prompt improvement suggestions
- Discuss attached documents
- Access all Supervertaler resources (prompts, TMs, termbases)

## Features

### 🔍 Project Analysis
Click "Analyze Project & Generate Prompts" to get AI-powered analysis of your current project, including:
- Domain identification
- Recommended existing prompts from your library
- Suggestions for new custom prompts
- Complete prompt text ready to save

### 💬 Conversational Interface
Chat naturally with the AI about:
- Your translation project requirements
- Prompt optimization and improvements
- Document analysis and context
- Translation memory and termbase usage

### 📎 File Attachments
Attach documents to the conversation:
- **Supported formats**: PDF, DOCX, TXT, MD
- **Auto-conversion**: Documents are converted to markdown for AI processing
- **Multiple files**: Attach reference materials, source documents, style guides
- **Persistent**: Attached files remain available throughout the conversation

### 📋 Context Awareness
The AI Assistant has access to:
- **Current Document**: Automatically includes your active project document
- **Prompt Library**: All 38+ prompts from your unified library
- **Translation Memories**: Can query and reference TM data
- **Termbases**: Access to terminology databases
- **Chat History**: Maintains conversation context

## Usage

### Quick Start
1. Open **Prompt Manager** tab
2. Switch to **✨ AI Assistant** sub-tab
3. Click "🔍 Analyze Project & Generate Prompts" for automated analysis
4. Or start chatting: "Help me create a prompt for legal translations"

### Attaching Files
1. Click "📎 Attached Files" in the context sidebar
2. Select PDF, DOCX, or text files
3. Ask questions about the attached content

### Example Conversations

**Generate a prompt:**
```
User: Create a prompt for medical device translations from English to German
AI: [Analyzes requirements and generates complete prompt text]
```

**Improve existing prompt:**
```
User: My legal prompt is too generic. Make it more specific for contracts.
AI: [Reviews current prompt and suggests targeted improvements]
```

**Analyze document:**
```
User: I attached a style guide PDF. What are the key requirements?
AI: [Extracts and summarizes style guide requirements]
```

### Selecting Resources
Click on context sidebar items to include specific resources:
- **💡 Prompt Library**: Select which prompts to reference
- **💾 Translation Memories**: Include relevant TM entries
- **📚 Termbases**: Add terminology context

## LLM Configuration

The AI Assistant uses your configured LLM provider from Settings:
- **OpenAI**: GPT-4, GPT-4o, GPT-5
- **Anthropic**: Claude 3.5 Sonnet
- **Google**: Gemini 2.0 Flash

Configure API keys in Settings → API Configuration.

## Conversation Persistence

All conversations are automatically saved to:
```
user_data/ai_assistant/conversation.json
```

This includes:
- Full chat history
- Attached file metadata
- Timestamps for all interactions

## Tips & Best Practices

### For Best Results
1. **Be specific**: "Create a legal contract prompt for EN→DE" beats "make a legal prompt"
2. **Provide context**: Attach style guides, reference documents, or examples
3. **Iterative refinement**: Start broad, then ask for specific improvements
4. **Use analysis**: Let the AI analyze your project first for tailored suggestions

### Workflow Integration
1. Start new project → Analyze with AI Assistant
2. Review suggested prompts → Save to library
3. Attach project-specific documents → Generate custom prompt
4. Test translations → Ask AI for prompt refinements

### Resource Management
- Keep attached files relevant to current project
- Clear conversation history when starting new projects
- Save generated prompts immediately to library

## Keyboard Shortcuts

- **Shift+Enter**: New line in message input
- **Enter**: Send message

## Troubleshooting

**"AI Assistant not available"**
- Check API keys in Settings
- Ensure you have an active API key for OpenAI, Claude, or Gemini

**Slow responses**
- Large attached files increase processing time
- Consider summarizing lengthy documents first

**Context too large**
- Detach old files not needed for current task
- Clear conversation history (File → New Conversation)

## Coming Soon

- ✨ Direct prompt creation and saving from chat
- ✨ Advanced markdown conversion for PDF/DOCX (via markitdown)
- ✨ Translation memory search integration
- ✨ Termbase query interface
- ✨ Export conversation as documentation
- ✨ Prompt comparison and A/B testing

## Technical Details

**Architecture:**
- Built on `llm_clients.py` for provider-agnostic AI calls
- Uses same LLM configuration as main translation engine
- Conversation stored in JSON format
- File attachments cached for session duration

**Privacy:**
- All data stored locally
- API calls go directly to your configured provider
- No third-party intermediaries

---

Last updated: November 8, 2025
Version: 4.0.0-beta (Unified Prompt System)
