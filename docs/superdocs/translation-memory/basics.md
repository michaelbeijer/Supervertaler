# Translation Memory Basics

Translation Memory (TM) helps you reuse previous translations.

## What is Translation Memory?

A Translation Memory stores pairs of source and target text:

| Source | Target | Match % |
|--------|--------|---------|
| "Save the file" | "Sla het bestand op" | 100% |
| "Save the document" | "Sla het document op" | 85% |

When you translate new text, the TM finds similar segments.

## How TM Works

1. **You translate** a segment
2. **TM stores** the source + target pair
3. **Later**, when similar text appears:
   - TM finds matches
   - Shows them in the Translation Results panel
   - You can insert or adapt them

## Match Types

| Type | Match % | Description |
|------|---------|-------------|
| **Exact** | 100% | Identical source text |
| **High Fuzzy** | 90-99% | Minor differences (numbers, capitalization) |
| **Medium Fuzzy** | 75-89% | Some words different |
| **Low Fuzzy** | 50-74% | Significant differences |

## Benefits

### Save Time

Don't translate the same sentence twice. TM automatically suggests previous translations.

### Consistency

Same source = same translation. Important for technical documentation, UI strings, and legal text.

### Cost Savings

Clients often pay less for TM matches:
- 100% match: Lowest rate
- Fuzzy match: Reduced rate
- New text: Full rate

## TM in Supervertaler

### Translation Results Panel

When you select a segment:
1. TM searches for matches
2. Results appear in the panel on the right
3. Shows match percentage, source, and target
4. Double-click to insert

### Using Matches

| Action | How |
|--------|-----|
| Insert match | Double-click or press `Ctrl+1-9` for first 9 matches |
| Copy match | Right-click → Copy |
| View in context | Right-click → View in TM |

### Building TM

Your TM grows as you translate:
1. Translate a segment
2. Confirm with `Ctrl+Enter`
3. The pair is saved to active TM

## Multiple TMs

You can have multiple TMs:
- **Project TM**: For the current project
- **Client TMs**: One per client
- **Master TM**: All your translations

### TM Priority

When multiple TMs match:
- Higher priority TMs shown first
- Can reorder in Project resources

---

## See Also

- [Creating & Managing TMs](managing-tms.md)
- [Importing TMX Files](importing-tmx.md)
- [Fuzzy Matching](fuzzy-matching.md)
- [Supermemory (Semantic Search)](supermemory.md)
