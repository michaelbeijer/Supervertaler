# Apps Similar to Supervertaler

A curated list of translation tools and AI-powered assistants that offer similar functionality to Supervertaler.

---

## 🤖 AI-Powered Translation Tools

### TransAIde (Plugin for Trados Studio)
- **Website:** [posteditacat.xyz/transaide-plugin-for-trados-studio](https://posteditacat.xyz/transaide-plugin-for-trados-studio/)
- **Type:** Trados Studio plugin
- **Description:** Context-aware AI translation plugin that exports entire documents from Trados Studio, allowing translation with any AI model (Claude, Gemini, ChatGPT, etc.) or NMT system while preserving full context.
- **Key Features:**
  - Export/import full documents with context (text or JSON format)
  - Works with any AI model via chat, API, or agent systems
  - Termbase integration (exports required/forbidden terms)
  - Dedicated window showing AI translations segment-by-segment
  - Supports grammar checking (LanguageTool, Grammarly)
  - Compatible with Trados Studio 2021, 2022, 2024
- **Pricing:** Free up to 500 words, subscription for unlimited (39 EUR/year freelancer, 69 EUR/year agency)
- **Open Source:** ❌

### OpenAI Provider for Trados Studio
- **Website:** [appstore.rws.com/plugin/249](https://appstore.rws.com/plugin/249?lang=fr&tab=documentation)
- **Type:** Trados Studio plugin (Translation Provider)
- **Description:** Official free plugin from RWS that integrates OpenAI's language models as a translation provider within Trados Studio.
- **Key Features:**
  - Direct OpenAI API integration
  - Works as a standard translation provider in Trados
  - Segment-by-segment translation workflow
  - Requires OpenAI API key
- **Pricing:** Free (pay-per-use OpenAI API costs)
- **Open Source:** ❌
- **Note:** RWS also offers "AI Professional" plugin with more features (Azure OpenAI support, custom prompts, AI companion, terminology-aware suggestions)

### CotranslatorAI
- **Website:** [cotranslator.ai](https://cotranslatorai.com/)
- **Type:** Web-based AI translation assistant
- **Description:** AI-powered translation tool that helps professional translators work more efficiently with machine translation post-editing and terminology management.
- **Key Features:**
  - AI-assisted translation
  - Terminology management
  - CAT tool integration
- **Open Source:** ❌

### TWAS Suite / TWAS Assistant
- **Website:** [twas.info](https://twas-all-apps.netlify.app/) 
- **Type:** Desktop application
- **Description:** Translation Workflow Automation Suite - a comprehensive set of tools for translators working with various CAT tools and file formats.
- **Key Features:**
  - Workflow automation
  - File format conversion
  - Batch processing
- **Open Source:** ❌

---

## 📊 How They Compare

| Feature | Supervertaler | TransAIde | OpenAI Provider | CotranslatorAI | TWAS Suite |
|---------|---------------|-----------|-----------------|----------------|------------|
| Multi-LLM Support | ✅ GPT, Claude, Gemini, Ollama | ✅ Any AI model | ❌ (OpenAI only) | ❌ (only GPT) | ❓ |
| Standalone App | ✅ | ❌ (Trados plugin only) | ❌ (Trados plugin only) | ✅ Web | ✅ Desktop |
| Local/Offline Mode | ✅ Ollama | ✅ (via any local model) | ❌ | ❌ | ✅ |
| Trados Integration | ✅ SDLPPX/SDLRPX | ✅ Native plugin | ✅ Native plugin | ✅ | ✅ |
| memoQ Integration | ✅ | ❌ | ❌ | ✅ | ✅ |
| CafeTran Integration | ✅ | ❌ | ❌ | ❓ | ✅ |
| Full Context Translation | ✅ | ✅ (entire documents) | ❌ (segment-by-segment) | ❓ | ❓ |
| Translation Memory | ✅ SQLite + TMX | ➖ (uses Trados TM) | ➖ (uses Trados TM) | ✅ | ✅ |
| Terminology Management | ✅ | ➖ (exports from Trados) | ➖ (uses Trados TB) | ✅ | ✅ |
| Voice Dictation | ✅ Whisper | ❌ | ❌ | ❌ | ❌ |
| Open Source | ✅ MIT License | ❌ | ❌ | ❌ | ❌ |
| Free | ✅ | Freemium (500 words) | ✅ (API costs) | Freemium | Paid |

---

## 💡 Why Choose Supervertaler?

Supervertaler stands out by being:

1. **Completely Free & Open Source** - No subscription, no hidden costs
2. **Privacy-Focused** - Run locally with Ollama, your data stays on your machine
3. **Multi-LLM Flexible** - Use any AI provider, switch between them freely
4. **Translator-Built** - Created by a working translator who understands real workflows
5. **CAT Tool Agnostic** - Works alongside memoQ, Trados, CafeTran, and others
6. **Standalone Application** - No need to buy or use specific CAT tools

---

*Know of another similar app that should be listed here? Open an issue or discussion on GitHub!*
