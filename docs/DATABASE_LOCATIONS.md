# Database File Locations

## Current Setup (as of v1.0.1)

### Production Mode
When `.supervertaler.local` file is **NOT** present in root:
- Database location: `user data/supervertaler.db`
- Synced to GitHub: ✅ YES

### Development Mode  
When `.supervertaler.local` file **IS** present in root:
- Database location: `user data_private/supervertaler.db`
- Synced to GitHub: ❌ NO (privacy/gitignored)

## Important Notes

1. **Folder naming**: Use `user data` and `user data_private` (WITH SPACES)
   - ❌ NOT `user_data` or `user_data_private` (underscores)
   
2. **Current database**: `supervertaler.db` (180KB, Oct 29 2025)
   - Contains: 3 termbases, 48 terms
   - Tables: translation_units, termbases, termbase_terms, projects, etc.

3. **Backup strategy**:
   - `user data/` → Synced to GitHub (public data)
   - `user data_private/` → Local only (private data, use Macrium backup)

## Recovery Notes (Oct 30, 2025)

- Accidentally deleted `user_data` and `user_data_private` (underscore versions)
- Recovered `user data` from git history ✅
- Recovered `user data_private` from Macrium backup ✅
- Database file copied to both locations for safety
