# OPUS API Integration - Feature Investigation

> **Date:** January 6, 2026  
> **Status:** ✅ Implemented (Phase 1)  
> **Priority:** Medium  
> **Component:** Superlookup

---

## 📚 What is OPUS?

[OPUS](https://opus.nlpl.eu/) (Open Parallel Corpus) is the largest free collection of parallel corpora in the world:

| Metric | Value |
|--------|-------|
| Total Sentence Pairs | 58.8 billion |
| Languages | 1,005 |
| Corpora | 1,213 |
| Top Corpora | OpenSubtitles (20B), NLLB (13B), CCMatrix (11B) |

OPUS is maintained by the University of Helsinki and provides essential training data for machine translation systems worldwide.

---

## 🔍 What Can OPUS API Do?

### Current API Capabilities (https://opus.nlpl.eu/opusapi/)

The OPUS API is primarily designed for **corpus metadata and download URLs**, NOT for live concordance search:

```bash
# List available languages
GET https://opus.nlpl.eu/opusapi/?languages=True

# List available corpora
GET https://opus.nlpl.eu/opusapi/?corpora=True

# Get download links for a specific corpus/language pair
GET https://opus.nlpl.eu/opusapi/?corpus=OpenSubtitles&source=en&target=nl&preprocessing=xml&version=latest
```

**Response example:**
```json
{
  "corpora": [
    {
      "corpus": "OpenSubtitles",
      "version": "v2018",
      "source": "en",
      "target": "nl",
      "preprocessing": "xml",
      "url": "https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/xml/en-nl.xml.gz",
      "size": 123456789,
      "documents": 45678,
      "alignment_pairs": 9876543
    }
  ]
}
```

### OPUS Query Tool (CQP - Corpus Query Processor)

OPUS also provides a **web-based concordance search** at:
- https://opus.nlpl.eu/bin/opuscqp.pl

This uses CWB (Corpus Workbench) with CQP query syntax for advanced concordance searches across multiple corpora.

**Example query URL:**
```
https://opus.nlpl.eu/bin/opuscqp.pl?query=machine&corpus=Europarl&lang1=en&lang2=nl
```

⚠️ **Important Limitation:** The CQP interface is a web form, NOT a REST API. It returns HTML, not JSON.

---

## 🎯 Integration Options for Superlookup

### Option A: Web Resource (Simplest - Recommended First)

Add OPUS Query as a **web resource** in Superlookup's existing Web Resources tab:

```python
{
    'id': 'opus_query',
    'name': 'OPUS Corpus Search',
    'icon': '📚',
    'description': 'Search parallel corpora (OpenSubtitles, Europarl, etc.)',
    'url_template': 'https://opus.nlpl.eu/bin/opuscqp.pl?query={query}&lang1={sl}&lang2={tl}&corpus=OpenSubtitles',
    'lang_format': 'iso2',  # en, nl, de
    'bidirectional': False,
}
```

**Pros:**
- ✅ 30 minutes implementation time
- ✅ No new dependencies
- ✅ Uses existing embedded browser
- ✅ Full CQP query power available

**Cons:**
- ❌ Results shown in browser, not integrated into TM-style table
- ❌ User must manually copy translations
- ❌ No programmatic access to results

### Option B: Scrape CQP Results (Medium Effort)

Parse the HTML response from the CQP query tool:

```python
import requests
from bs4 import BeautifulSoup

def search_opus(query: str, source_lang: str, target_lang: str, corpus: str = "OpenSubtitles"):
    url = f"https://opus.nlpl.eu/bin/opuscqp.pl"
    params = {
        'query': query,
        'lang1': source_lang,
        'lang2': target_lang,
        'corpus': corpus
    }
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Parse table rows for source/target pairs
    results = []
    # ... parsing logic
    return results
```

**Pros:**
- ✅ Results in Superlookup's table format
- ✅ Copy/insert functionality
- ✅ Searchable across multiple corpora

**Cons:**
- ❌ Fragile (HTML structure may change)
- ❌ Scraping may be against ToS
- ❌ Slower than direct API
- ❌ CQP interface sometimes returns errors

### Option C: Local OPUS Data (Most Powerful, Most Complex)

Download OPUS corpora locally and build a searchable index:

```python
# Download corpus
import opustools
opus = opustools.OpusRead(
    directory='OpenSubtitles',
    source='en',
    target='nl',
    preprocess='raw'
)

# Index with SQLite FTS5 or ChromaDB
# ... indexing logic
```

**Pros:**
- ✅ Blazing fast searches
- ✅ No network dependency
- ✅ Full control over results
- ✅ Can integrate with Supermemory

**Cons:**
- ❌ Storage: 1-50+ GB per language pair
- ❌ Setup complexity
- ❌ opustools dependency
- ❌ Maintenance burden (corpus updates)

### Option D: OPUS-MT Translation (Alternative)

Instead of concordance search, use OPUS-MT models for translation:

OPUS provides pre-trained MT models via Hugging Face:
- https://github.com/Helsinki-NLP/OPUS-MT
- https://huggingface.co/Helsinki-NLP

```python
from transformers import MarianMTModel, MarianTokenizer

model_name = 'Helsinki-NLP/opus-mt-nl-en'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def translate(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
```

**Pros:**
- ✅ Proper API-based integration
- ✅ 1000+ language pairs available
- ✅ Works offline once downloaded

**Cons:**
- ❌ Different use case (MT not concordance)
- ❌ Models are 300MB+ each
- ❌ GPU recommended for speed

---

## 📊 Recommended Implementation Path

### Phase 1: Web Resource (Now)
1. Add OPUS Query to Web Resources tab
2. Pre-select relevant corpora (OpenSubtitles, Europarl, DGT, EMEA)
3. Add corpus selector dropdown in settings

**Implementation time:** ~30 minutes

### Phase 2: Native Results Tab (Future)
1. Add "OPUS" tab to Superlookup
2. Parse CQP HTML results
3. Display in standard source/target table format
4. Add corpus multi-select

**Implementation time:** ~4-8 hours

### Phase 3: Local OPUS Integration (Optional)
1. Add OPUS corpus download/import feature
2. Index with Supermemory (ChromaDB)
3. Unified search across local TMs + OPUS

**Implementation time:** ~16-40 hours

---

## 🗂️ Relevant Corpora for Translators

| Corpus | Content | Size | Best For |
|--------|---------|------|----------|
| **OpenSubtitles** | Movie/TV subtitles | 20B pairs | Conversational, informal |
| **Europarl** | EU Parliament proceedings | 186M pairs | Legal, political |
| **DGT** | EU Translation Memory | 1.1B pairs | Legal, official |
| **EMEA** | European Medicines Agency | 243M pairs | Medical, pharmaceutical |
| **EUbookshop** | EU publications | 279M pairs | Technical, policy |
| **JRC-Acquis** | EU legislation | 147M pairs | Legal |
| **ECB** | European Central Bank | 15M pairs | Finance, economics |
| **TED2020** | TED talks | 143M pairs | General, presentations |
| **WikiMatrix** | Wikipedia | 127M pairs | General knowledge |
| **GlobalVoices** | News articles | 7.3M pairs | News, current events |

---

## 🔗 References

- **OPUS Website:** https://opus.nlpl.eu/
- **OPUS API:** https://opus.nlpl.eu/opusapi/
- **OPUS Query (CQP):** https://opus.nlpl.eu/bin/opuscqp.pl
- **OpusTools (Python):** https://github.com/Helsinki-NLP/OpusTools
- **OPUS-MT Models:** https://github.com/Helsinki-NLP/OPUS-MT

---

## 📝 Decision

**Recommended:** Start with **Option A (Web Resource)** for immediate value, then evaluate user feedback before investing in Option B or C.

---

*Investigation by: GitHub Copilot*  
*Date: January 6, 2026*
