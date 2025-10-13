# Testing Guide: Figure Context Feature

## Overview
This guide helps you test the Figure Context feature in Supervertaler v3.4.0-beta.

## Test Materials Provided

### Test Images (in `test_figures/` folder)
1. **Figure 1.png** - Blue rectangular diagram
2. **Figure 2A.jpg** - Yellow circle with red outline
3. **fig3b.png** - Orange triangle

### Test Document
- **test_document.txt** - Contains figure references in various formats

## Testing Steps

### 1. Load Test Images
1. Run Supervertaler v3.4.0-beta
2. Go to **Resources > 🖼️ Load figure context...**
3. Select the `test_figures` folder
4. **Expected Result**:
   - Dialog: "Figure Context Loaded - Loaded 3 figure images as visual context"
   - Log: Shows loaded images (Figure 1.png → '1', Figure 2A.jpg → '2a', fig3b.png → '3b')

### 2. Check Images Tab
1. Click on **Images** tab in assistant panel
2. **Expected Result**:
   - Status shows: "✓ 3 images loaded from: test_figures"
   - Three thumbnails visible with:
     * Figure names (FIGURE 1, FIGURE 2A, FIGURE 3B)
     * Preview images
     * Dimensions (400 × 300 px)

### 3. Import Test Document
1. Go to **File > Import > TXT (Mono/Bilingual)...**
2. Select `test_figures/test_document.txt`
3. When prompted for format, choose **Source only (monolingual)**
4. **Expected Result**:
   - Document loaded with 7-8 segments
   - Segments visible in grid

### 4. Test Figure Detection (Segment with "Figure 1")
1. Select segment containing "As shown in Figure 1"
2. Click **Translate current** (or press Ctrl+T)
3. **Check Log Panel** - Should show:
   ```
   [Figure Context] Detected references: Figure 1
   [Figure Context] Found 1 matching images - using multimodal API
   ```
4. **Expected Result**:
   - Segment translated using multimodal API
   - Translation considers the blue rectangular diagram

### 5. Test Multiple Figures (Segment with "Figure 2A")
1. Select segment mentioning "Figure 2A"
2. Translate
3. **Check Log** - Should show:
   ```
   [Figure Context] Detected references: Figure 2A
   [Figure Context] Found 1 matching images - using multimodal API
   ```

### 6. Test Alternative Notation (Segment with "fig. 3b" or "fig3b")
1. Select segment with "fig. 3b" or "fig3b"
2. Translate
3. **Check Log** - Should detect and match figure 3b

### 7. Test Context Status
1. Look at bottom status bar
2. **Expected**: Shows "Context: ... | 🖼️ 3 figures"

### 8. Test Project Persistence
1. Go to **Project > Save project**
2. Save as "test_figure_context.json"
3. Go to **Project > Close project**
4. Go to **Project > Open project...**
5. Load "test_figure_context.json"
6. **Expected Result**:
   - Log: "✓ Loaded figure context: 3 images from test_figures"
   - Images tab shows thumbnails again
   - Status bar shows figure count

### 9. Test Clear Function
1. Go to **Resources > 🗑️ Clear figure context**
2. **Expected Result**:
   - Dialog: "Figure Context Cleared"
   - Images tab shows "No figure context loaded"
   - Status bar no longer shows figure count

### 10. Test Without Figures (Control Test)
1. Make sure figures are cleared
2. Translate a segment
3. **Expected**: Uses text-only API (no multimodal messages in log)

## Success Criteria

✅ **All tests pass if**:
1. Images load successfully from folder
2. Thumbnails display correctly in Images tab
3. Figure references are detected in text
4. Multimodal API is used when figures detected
5. Text-only API used when no figures detected
6. Figure context persists with project save/load
7. Clear function removes all images
8. Status indicators update correctly

## Troubleshooting

### Images not showing thumbnails
- **Error**: "name 'ImageTk' is not defined"
- **Fix**: Already fixed in latest version - restart Supervertaler

### Figures not detected
- Check log for "[Figure Context] Detected references: ..."
- Verify text contains "Figure X", "fig X", or "Figuur X"
- Check figure naming matches pattern (Figure 1.png, Figure 2A.jpg, etc.)

### Multimodal API not being used
- Verify you have API keys configured
- Check that detected figures match loaded image names
- Look for log message: "[Figure Context] Found X matching images"

## Test Results Template

Copy and fill out after testing:

```
Date: _______________
Version: v3.4.0-beta

Test 1 - Load Images: [ ] Pass [ ] Fail
Test 2 - Images Tab: [ ] Pass [ ] Fail
Test 3 - Import Document: [ ] Pass [ ] Fail
Test 4 - Detect Figure 1: [ ] Pass [ ] Fail
Test 5 - Detect Figure 2A: [ ] Pass [ ] Fail
Test 6 - Detect fig3b: [ ] Pass [ ] Fail
Test 7 - Status Indicator: [ ] Pass [ ] Fail
Test 8 - Project Persistence: [ ] Pass [ ] Fail
Test 9 - Clear Function: [ ] Pass [ ] Fail
Test 10 - Without Figures: [ ] Pass [ ] Fail

Notes:
__________________________________________
__________________________________________
__________________________________________
```

## Next Steps

After successful testing:
1. Try with your own technical documents
2. Test with real figure images from your projects
3. Test with all three providers (OpenAI, Claude, Gemini)
4. Report any issues or suggestions
