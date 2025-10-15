"""
Verify that both v2.5.0 and v3.2.0 have the Tracked Changes feature correctly integrated
"""

import os
import re

print("=" * 70)
print("TRACKED CHANGES FEATURE VERIFICATION")
print("=" * 70)

# Files to check
files_to_verify = {
    'v2.5.0': 'Supervertaler_v2.5.0-CLASSIC.py',
    'v3.2.0': 'Supervertaler_v3.2.0-beta_CAT.py'
}

results = {}

for version, filename in files_to_verify.items():
    print(f"\n{'='*70}")
    print(f"Checking {version}: {filename}")
    print('='*70)
    
    if not os.path.exists(filename):
        print(f"❌ ERROR: File not found!")
        results[version] = False
        continue
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check 1: Version number
    if version == 'v2.5.0':
        version_check = 'v2.5.0-CLASSIC' in content
    else:
        version_check = 'v3.2.0-beta' in content
    
    print(f"✅ Version string present" if version_check else "❌ Version string missing")
    
    # Check 2: TrackedChangesBrowser class
    browser_class = 'class TrackedChangesBrowser:' in content
    print(f"✅ TrackedChangesBrowser class present" if browser_class else "❌ TrackedChangesBrowser class missing")
    
    # Check 3: export_to_md_report method
    md_export = 'def export_to_md_report(self):' in content
    print(f"✅ export_to_md_report method present" if md_export else "❌ export_to_md_report method missing")
    
    # Check 4: Batch size slider
    batch_slider = 'batch_dialog = tk.Toplevel' in content and 'Batch Size Configuration' in content
    print(f"✅ Batch size slider present" if batch_slider else "❌ Batch size slider missing")
    
    # Check 5: AI precision prompts
    precision_prompts = 'PAY SPECIAL ATTENTION to quote marks' in content
    print(f"✅ Precision AI prompts present" if precision_prompts else "❌ Precision AI prompts missing")
    
    # Check 6: Batch processing method
    batch_method = 'def get_ai_change_summaries_batch' in content
    print(f"✅ Batch processing method present" if batch_method else "❌ Batch processing method missing")
    
    # Check 7: Browse method integration
    if version == 'v2.5.0':
        # v2 should have button in Post-Translation Analysis section
        browse_integration = 'Post-Translation Analysis' in content or 'browse_tracked_changes' in content
    else:
        # v3 should use TrackedChangesBrowser class
        browse_integration = 'self.tracked_changes_browser = TrackedChangesBrowser' in content
    
    print(f"✅ Browse method integrated" if browse_integration else "❌ Browse method not properly integrated")
    
    # Check 8: Markdown report header explanation
    report_explanation = 'What is this report?' in content
    print(f"✅ Report explanation present" if report_explanation else "❌ Report explanation missing")
    
    # Check 9: Queue import (v3 only)
    if version == 'v3.2.0':
        queue_import = 'import queue' in content
        print(f"✅ queue module imported" if queue_import else "❌ queue module not imported")
    
    # Overall result
    if version == 'v2.5.0':
        all_checks = all([
            version_check, browser_class, md_export, batch_slider, 
            precision_prompts, batch_method, browse_integration, report_explanation
        ])
    else:
        all_checks = all([
            version_check, browser_class, md_export, batch_slider,
            precision_prompts, batch_method, browse_integration, report_explanation,
            queue_import
        ])
    
    results[version] = all_checks
    
    if all_checks:
        print(f"\n✅ {version} VERIFICATION PASSED - All checks successful!")
    else:
        print(f"\n❌ {version} VERIFICATION FAILED - Some checks failed")

# Final summary
print("\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)

if all(results.values()):
    print("\n🎉 SUCCESS! Both versions verified successfully!")
    print("\n✅ v2.5.0-CLASSIC: Feature complete")
    print("✅ v3.2.0-beta: Feature ported successfully")
    print("\nBoth versions ready for testing!")
else:
    print("\n⚠️ ISSUES DETECTED!")
    for version, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {version}: {status}")

print("\n" + "=" * 70)
print("DOCUMENTATION STATUS")
print("=" * 70)

# Check documentation files
docs = {
    'CHANGELOG-CLASSIC.md': 'v2.5.0',
    'CHANGELOG-CAT.md': 'v3.2.0',
    'CHANGELOG.md': 'both versions',
    'README.md': 'both versions',
    'TRACKED_CHANGES_FEATURE_SUMMARY.md': 'feature summary'
}

for doc, description in docs.items():
    if os.path.exists(doc):
        with open(doc, 'r', encoding='utf-8') as f:
            doc_content = f.read()
        
        # Check for relevant version mentions
        if 'CLASSIC' in doc:
            has_content = '2.5.0' in doc_content
        elif 'CAT' in doc:
            has_content = '3.2.0' in doc_content
        else:
            has_content = '2.5.0' in doc_content or '3.2.0' in doc_content
        
        status = "✅" if has_content else "⚠️ "
        print(f"{status} {doc}: {description}")
    else:
        print(f"❌ {doc}: NOT FOUND")

print("\n" + "=" * 70)
print("READY TO TEST!")
print("=" * 70)
print("""
Next steps:
1. Run Supervertaler_v2.5.0-CLASSIC.py
2. Run Supervertaler_v3.2.0-beta_CAT.py
3. Test Tracked Changes feature in both
4. Export MD reports with AI analysis
5. Verify quote/dash detection works
6. Commit to Git if all tests pass

See TRACKED_CHANGES_FEATURE_SUMMARY.md for detailed testing checklist.
""")
