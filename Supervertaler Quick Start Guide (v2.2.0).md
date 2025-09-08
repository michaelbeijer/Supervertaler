# Supervertaler Quick Start Guide
## Version 2.2.0 - Get Up and Running Fast!

---

## Welcome to Supervertaler! 🚀

This quick start guide will have you translating and proofreading documents with AI assistance in just a few minutes. Supervertaler v2.2.0 introduces the revolutionary **Custom Prompt Library** and enhanced user interface.

---

## 📋 Quick Checklist

### Before You Start
- [ ] Python 3.10+ installed
- [ ] At least one AI provider API key
- [ ] Input files prepared in correct format
- [ ] 15 minutes to complete setup

### What You'll Achieve
- [ ] Install and configure Supervertaler
- [ ] Complete your first translation or proofreading task
- [ ] Create and save your first custom prompt set
- [ ] Understand the new 3-panel interface

---

## ⚡ 5-Minute Setup

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
1. **Download**: Get `Supervertaler_v2.1.1.py`
2. **First Run**: Execute the file to create `api_keys.txt`
3. **Add Key**: Edit `api_keys.txt`, uncomment and fill your API key:
```
google = your_google_key_here
#claude = your_claude_key_here  
#openai = your_openai_key_here
```
4. **Launch**: Run `python Supervertaler_v2.1.1.py`

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
1. **Launch Supervertaler** - You'll see the new 3-panel interface
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

## 🎨 Explore Custom Prompt Library (10 minutes)

### Understanding the Interface
**New 3-Panel Design**:
- **Left Panel**: All controls and settings (resizable)
- **Top Right**: Information and guidance (larger in v2.2.0)
- **Bottom Right**: Real-time processing log

### Access Advanced Prompts
1. **Expand Section**: Click "⚙️ Advanced System Prompts (Click to expand/collapse)"
2. **Three Tabs Available**:
   - **Translation Prompt**: Control AI translation behavior
   - **Proofreading Prompt**: Control AI proofreading behavior  
   - **📁 Prompt Library**: NEW! Save and manage custom prompts

### Create Your First Custom Prompt Set

#### Customize Translation Prompt
1. **Switch to Translation Prompt tab**
2. **Edit the prompt** for your specific needs:
```
You are an expert {source_lang} to {target_lang} translator 
specializing in business communication. 
Use professional but friendly tone.
Ensure cultural appropriateness for business contexts.
Maintain brand consistency and clarity.
```

#### Save Custom Set
1. **Switch to 📁 Prompt Library tab**
2. **Enter Name**: "Business Communication"  
3. **Click**: "💾 Save Current Prompts"
4. **Success**: See your prompt set in the list!

#### Load Custom Set Later
1. **Select**: Your saved prompt from the list
2. **Click**: "📂 Load Selected"
3. **Instant Loading**: Prompts are immediately applied

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

## 🎛️ Interface Tour: What's New in v2.2.0

### Left Panel - Main Controls
- **Program Title**: Supervertaler v2.2.0 (larger, sharper font)
- **Operation Mode**: Translate/Proofread selection
- **File Selection**: Input and output file browsing
- **Context Sources**: TM files, tracked changes, images
- **Advanced System Prompts**: NEW expandable section
- **AI Provider Settings**: Model selection and configuration
- **Language Settings**: Source, target, and chunk size
- **Action Buttons**: Start process, list models, refresh

### Top Right Panel - Information Hub  
- **Larger Display**: 700px height for better visibility
- **Feature Overview**: Complete functionality description
- **Mode-Specific Help**: Changes based on Translate/Proofread mode
- **Context Examples**: Sample input/output formats

### Bottom Right Panel - Processing Log
- **Compact Design**: 200px height for efficient space usage
- **Real-Time Updates**: Live status messages during processing
- **Error Reporting**: Clear problem identification and solutions
- **Progress Tracking**: Step-by-step processing information

### Advanced System Prompts Section
- **Collapsible Design**: Click header to expand/collapse
- **Tabbed Interface**: Translation, Proofreading, Library tabs
- **Template Variables**: `{source_lang}` and `{target_lang}` support
- **Preview Function**: See final prompts with current settings
- **Reset Options**: Restore defaults with one click

### Custom Prompt Library (NEW!)
- **Save/Load Interface**: Intuitive prompt management
- **File Organization**: Automatic storage in `custom_prompts/` folder
- **Selection Memory**: Auto-fills names when browsing
- **Protected Defaults**: "[Default System Prompts]" always available

---

## 🚀 Pro Tips for Success

### Optimization Strategies
1. **Start Small**: Test with small files before processing large documents
2. **Review Prompts**: Customize system prompts for your specific domain
3. **Use Context**: Add TM files and tracked changes for better results
4. **Monitor Quality**: Check sample outputs before processing full batches

### Custom Prompt Best Practices
1. **Be Specific**: Include domain, tone, and style requirements
2. **Use Templates**: Leverage `{source_lang}` and `{target_lang}` variables
3. **Test Variants**: Create multiple prompt sets for different use cases
4. **Document Changes**: Keep notes on what works best for different content

### Workflow Efficiency  
1. **Organize Files**: Keep input, output, and context files well organized
2. **Backup Prompts**: Export your `custom_prompts/` folder regularly
3. **Monitor Logs**: Check processing log for issues and improvements
4. **Iterate Quickly**: Use preview functions to test before full processing

### Common Use Cases
- **Business Documents**: Professional, clear, culturally appropriate
- **Technical Manuals**: Precise terminology, structured format
- **Marketing Content**: Creative, engaging, target market adaptation
- **Legal Texts**: Formal register, accurate terminology, careful structure

---

## 🆘 Quick Troubleshooting

### App Won't Start
- **Check Python**: Ensure version 3.10+
- **Install Dependencies**: Run pip install commands
- **Verify API Keys**: At least one valid key required

### Poor Translation Quality
- **Customize Prompts**: Use Advanced System Prompts for your domain
- **Add Context**: Include TM files and relevant tracked changes
- **Try Different Models**: Some work better for specific content types

### Processing Errors
- **Check File Format**: UTF-8 encoding, correct structure
- **Reduce Chunk Size**: For large or complex documents
- **Monitor API Limits**: Some providers have rate restrictions

### Performance Issues
- **Smaller Chunks**: Reduce memory usage
- **Close Programs**: Free up system resources
- **Check Internet**: Stable connection required for API calls

---

## 🎯 Next Steps

### Immediate Actions (Today)
1. **Complete First Translation**: Follow the 5-minute guide above
2. **Create Custom Prompt**: Save your first specialized prompt set
3. **Test Proofreading**: Try the proofreading workflow
4. **Explore Interface**: Get familiar with the new 3-panel design

### Short Term (This Week)
1. **Process Real Documents**: Use your actual translation projects
2. **Build Prompt Library**: Create prompt sets for different document types
3. **Add Context Sources**: Set up TM files and tracked changes
4. **Optimize Workflow**: Find the best settings for your use cases

### Long Term (This Month)
1. **Quality Assessment**: Compare results with previous translation methods
2. **Team Integration**: Share prompt libraries with colleagues
3. **Advanced Features**: Explore multimodal processing with document images
4. **Workflow Automation**: Develop consistent processes for regular work

### Professional Development
1. **Prompt Engineering**: Learn to write effective AI instructions
2. **Quality Control**: Develop systematic review processes
3. **Technology Integration**: Connect with existing translation workflows
4. **Continuous Improvement**: Regular refinement of prompts and processes

---

## 📞 Support and Resources

### Documentation
- **Full User Guide**: Complete feature documentation
- **README.md**: Technical setup and configuration details
- **CHANGELOG.md**: Version history and feature updates

### Getting Help
- Check the processing log for specific error messages
- Review file formats and ensure proper encoding
- Test with smaller files to isolate issues
- Verify API keys and network connectivity

### Community and Updates
- Watch for new versions with additional features
- Share prompt sets and best practices with colleagues
- Provide feedback for future improvements
- Monitor AI provider updates and new model releases

---

## 🎉 Congratulations!

You're now ready to use Supervertaler v2.2.0 effectively! The combination of powerful AI translation, custom prompt management, and professional interface design provides a comprehensive solution for modern translation needs.

**Remember**: The key to success with Supervertaler is experimentation and iteration. Try different prompts, test various settings, and build a library of specialized configurations for your specific translation requirements.

**Happy Translating!** 🌍✨

---

*For detailed information on advanced features, see the complete User Guide. This Quick Start Guide covers the essentials to get you productive immediately.*
