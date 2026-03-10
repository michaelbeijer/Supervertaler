# MultiTerm Support

TermLens automatically detects MultiTerm termbases (`.sdltb` files) attached to your active Trados project and displays their terms alongside your Supervertaler terms.

## How It Works

When you open a project in Trados Studio that has MultiTerm termbases attached, TermLens reads those `.sdltb` files and loads all term pairs into its matching engine. MultiTerm terms appear as **green chips** in the TermLens panel, right next to the blue, pink, and yellow chips from your Supervertaler termbases.

There is nothing to configure. If your Trados project has MultiTerm termbases attached (via **Project Settings > Language Pairs > Termbases**), TermLens picks them up automatically.

### Color coding

| Color | Meaning |
|-------|---------|
| **Blue** | Regular Supervertaler termbase match |
| **Pink** | Project termbase match (higher priority) |
| **Yellow** | Non-translatable term (source = target) |
| **Green** | MultiTerm termbase match (`.sdltb`) |

Green chips behave like any other TermLens chip — click to insert, or use **Alt+1** through **Alt+9** to insert by number.

## Read-Only

MultiTerm termbases are **read-only** in TermLens. You cannot add, edit, or delete terms in a MultiTerm termbase from the TermLens panel. To manage MultiTerm terms, use Trados Studio's built-in MultiTerm interface.

When you right-click a green MultiTerm chip, the Edit, Delete, and "Mark as Non-Translatable" options are not shown.

## Auto-Refresh

When you add or edit terms in a MultiTerm termbase using Trados's native interface, TermLens detects the file change automatically. The next time you navigate to a different segment, the updated terms appear in the panel — no manual refresh needed.

## MultiTerm Termbases in Settings

MultiTerm termbases appear at the bottom of the termbase list in the **Supervertaler Settings** dialog (gear icon > TermLens tab). Each one is labeled with **[MultiTerm]** and has a light green background to distinguish it from Supervertaler termbases.

| Toggle | Behavior |
|--------|----------|
| **Read** | Controls whether this termbase's terms appear in TermLens. Uncheck to hide it. |
| **Write** | Always disabled — MultiTerm termbases are read-only in TermLens |
| **Project** | Always disabled — only Supervertaler termbases can be the project termbase |

To add or remove MultiTerm termbases from your project, use Trados Studio's **Project Settings > Language Pairs > Termbases**.

## Technical Details

TermLens reads `.sdltb` files directly using the JET 4.0 database driver built into Windows. This is the same driver that MultiTerm itself uses. If the JET driver is not available (uncommon on modern Windows), TermLens falls back to Trados's terminology provider API for per-segment lookups.

Because the access is read-only, there is no risk of data corruption. TermLens opens the `.sdltb` file in shared read mode, so MultiTerm and Trados can continue to use it simultaneously.

## Troubleshooting

### MultiTerm terms not appearing

1. **Check your Trados project** — verify that MultiTerm termbases are attached via **Project Settings > Language Pairs > Termbases**
2. **Check the Read toggle** — open Supervertaler Settings and make sure the MultiTerm termbase's Read checkbox is enabled
3. **Check languages** — the termbase's source and target languages must match the current project's language pair

### Terms added in MultiTerm not updating

- Navigate to a different segment — this triggers the auto-refresh check
- If terms still do not appear, press **F5** in the TermLens panel to force a full reload

---

## See Also

- [TermLens](termlens.md)
- [Termbase Management](termbase-management.md)
- [TermLens Settings](settings/termlens.md)
- [Troubleshooting](troubleshooting.md)
