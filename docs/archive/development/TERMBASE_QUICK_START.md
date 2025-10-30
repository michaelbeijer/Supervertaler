# Quick Start: Using Term Bases in Supervertaler

## What Are Term Bases?

**Term Bases** (also called "Termbases") are specialized databases of terminology used in professional translation. Unlike Translation Memories (TM) which store complete translations, term bases store individual terms with:
- Source term (e.g., "totale lichaamscan")
- Target term (e.g., "total body scan")
- Priority/ranking (determines importance)
- Domain (e.g., "Medical Imaging")
- Definition and context

---

## Quick Start (5 minutes)

### 1. Open Term Bases Tab
When you launch Supervertaler:
1. Go to **Home** tab
2. Click **"📚 Term Bases"** tab
3. You'll see 3 sample termbases already loaded:
   - **Medical-NL-EN** (27 medical terms, Dutch → English)
   - **Legal-NL-EN** (10 legal terms, Dutch → English)  
   - **Technical-NL-EN** (10 IT terms, Dutch → English)

### 2. Activate Term Bases for Your Project
1. Select your translation project
2. In the Term Bases tab, **check the box** next to each termbase you want to use
3. Active termbases become **bold** in the list

### 3. Start Translating
1. Go to **Translation Grid**
2. Select a segment with Dutch source text
3. The **Assistance Panel** (right side) automatically shows:
   - TM matches (red section)
   - **Termbase matches** (blue section) ← This is new!

### 4. Insert Termbase Matches
When you see a termbase match you want to use:

**Option A:** Click the match in the Assistance Panel, then press **Ctrl+1**
- Or Ctrl+2, Ctrl+3, etc. if multiple matches

**Option B:** Double-click the match in the panel
- (Auto-inserts into translation)

---

## Example

### Scenario: Medical Document Translation

**You're translating a Dutch medical report. A segment contains:**
```
Source: "De patiënt ondergaat een totale lichaamscan."
```

**What happens:**
1. You click this segment
2. Supervertaler searches Translation Memory → finds 0 matches
3. Supervertaler searches Term Bases → finds:
   - "totale lichaamscan" → "total body scan" (Medical-NL-EN, Priority 1)

**You press Ctrl+1 to insert:**
```
Target: "The patient undergoes a total body scan."
```

---

## Managing Term Bases

### Create Your Own Termbase
1. In **Term Bases** tab, click **"+ Create New"**
2. Fill in:
   - **Name:** e.g., "My Company Terminology"
   - **Source Language:** e.g., "nl"
   - **Target Language:** e.g., "en"
   - **Scope:** 
     - "Global" = available to all projects
     - "Project-specific" = only for current project
3. Click **"Create"**

### Add Terms to Your Termbase
1. Click **"✏️ Edit Terms"**
2. Select your termbase
3. In the editor:
   - **Source term:** Dutch word/phrase
   - **Target term:** English translation
   - **Priority:** 1-99 (1 = highest priority)
   - Click **"+ Add"** to add the term

### Edit Existing Terms
1. Click **"✏️ Edit Terms"**
2. Select your termbase
3. All terms are listed in the table
4. Click on a term to select it and modify

### Delete Termbase
1. Click the termbase in the list
2. Click **"🗑️ Delete"**
3. Confirm deletion (also deletes all terms)

---

## Understanding Priority

**Priority determines the order of matches (1 = shown first):**

| Priority | Meaning | Example |
|----------|---------|---------|
| 1-10 | Critical terms | Company brand name, standard medical term |
| 20-50 | Important terms | Common technical terms, domain-specific |
| 60-90 | General terms | Less critical, alternative translations |
| 99 | Default | New terms get this by default |

**Lower priority number = higher importance = shown first in results**

---

## Sample Termbases Included

### Medical-NL-EN (27 terms)
Medical and healthcare terminology - Dutch to English

**Sample terms:**
- totale lichaamscan → total body scan
- myocardinfarct → myocardial infarction
- CT-getal → Hounsfield unit
- dynamische scan → dynamic scan

### Legal-NL-EN (10 terms)
Legal and contract terminology - Dutch to English

**Sample terms:**
- geldende overeenkomst → binding agreement
- voorwaarden → terms and conditions
- handtekening → signature

### Technical-NL-EN (10 terms)
IT and software terminology - Dutch to English

**Sample terms:**
- software → software
- firewall → firewall
- database → database
- netwerk → network

---

## Tips & Tricks

### Tip 1: Multiple Termbases
You can activate multiple termbases for one project. All their terms will show in the Assistance Panel.

### Tip 2: Priority Organization
Create high-priority (1-10) entries for:
- Company/client-specific terms
- Mandatory terminology
- Brand names

Use standard priority (50-60) for general terms.

### Tip 3: Search by Domain
When creating terms, use the "Domain" field (e.g., "Medical Imaging", "Law", "Finance") to organize terms by subject.

### Tip 4: Forbidden Terms
Mark terms as "forbidden" if you want to flag them as NOT recommended. These will show with special styling (future version).

### Tip 5: Re-use Termbases
Once created, termbases are global. You can activate the same termbase for multiple projects.

---

## Keyboard Shortcuts

When a termbase match is selected in the Assistance Panel:

| Shortcut | Action |
|----------|--------|
| **Ctrl+1** | Insert 1st match |
| **Ctrl+2** | Insert 2nd match |
| **Ctrl+3** | Insert 3rd match |
| **Ctrl+4** | Insert 4th match |
| **Ctrl+5** | Insert 5th match |
| ... | ... |
| **Ctrl+9** | Insert 9th match |

---

## Troubleshooting

### Problem: "No termbase matches showing"
**Solution:**
1. Check that the termbase is activated (checkbox checked, text is bold)
2. Check that source and target languages match your project
3. Verify the term actually exists (use "✏️ Edit Terms" to check)

### Problem: "Created term but can't find it"
**Solution:**
1. Make sure termbase is activated for your project
2. The search looks for partial matches - exact spelling matters
3. Language codes must match (e.g., "nl" for Dutch, "en" for English)

### Problem: "Wrong match appearing"
**Solution:**
- This might be the highest priority match in your termbase
- Edit the term priority to change the order
- Or create a higher priority term that matches better

---

## Coming Soon

**Future features in development:**
- 📥 Import termbases from CSV/Excel
- 📤 Export termbases to TMX format
- 🔍 Dedicated Terminology Search dialog (like memoQ Ctrl+P)
- 🔄 Concordance search (search translation memories)
- 🎨 Color-coding by priority
- ⚠️ Forbidden term highlighting

---

## Need Help?

For detailed technical information, see: `docs/TERMBASE_IMPLEMENTATION.md`

For general questions about term bases in translation:
- See your CAT tool documentation (memoQ, SDL Trados, etc.)
- Research terminology management best practices
- Consult industry glossaries for your domain

---

**Happy translating with Term Bases!** 🎉
