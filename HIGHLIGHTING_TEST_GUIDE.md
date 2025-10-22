# Text Highlighting Feature - Test Guide

## Quick Test Instructions

### Step 1: Upload Sample Document
A sample document has been created at `/tmp/sample_document.txt`. This document contains content about **AI Ethics and Ethical Frameworks**.

**To upload:**
1. Go to http://127.0.0.1:5001 in your browser
2. Click "Choose File" or drag-and-drop
3. Select `/tmp/sample_document.txt`
4. Click upload

### Step 2: Paste Comparison Text
Copy and paste **one of these examples** into the "Paste comparison text" field:

#### Example 1: High Match (75-84% - Medium/Yellow)
```
A conceptual framework that interpretively develops ethical implications of AI robot applications, 
drawing on descriptive and normative ethical theory. The new framework elaborates on how the locus 
of morality and moral intensity combine within context-specific AI robot applications.
```

**Expected Result:** 2-3 sentences highlighted in **YELLOW** (Medium match ~78-80%)

---

#### Example 2: Critical Match (95%+ - Red)
```
A conceptual framework that interpretively develops the ethical implications of AI robot applications, 
drawing on descriptive and normative ethical theory, is essential for understanding the complexities of 
modern automation. The framework elaborates on how the locus of morality (human to AI agency) and moral 
intensity combine within context-specific AI robot applications.
```

**Expected Result:** 2 sentences highlighted in **RED** (Critical match ~95%+)

---

#### Example 3: Mixed Matches (Multiple colors)
```
Research indicates that in situations of escalating AI agency and situational moral intensity, accountability 
is widely dispersed between actors and institutions. This creates significant challenges for establishing clear 
responsibility and ethical oversight.

A conceptual framework that interpretively develops ethical implications of AI robot applications, drawing on 
descriptive and normative ethical theory.
```

**Expected Result:** 
- First 2 sentences highlighted in **ORANGE/YELLOW** (High match ~85-90%)
- Last sentence highlighted in **YELLOW** (Medium match ~78%)

---

#### Example 4: Low Match (60-74% - Light Yellow)
```
The framework examines artificial intelligence development and ethical considerations for robotic systems, 
incorporating moral principles and theory.
```

**Expected Result:** 1-2 sentences highlighted in **LIGHT YELLOW** (Low match ~65-70%)

---

### Step 3: Click "Highlight Suspicious Text"
1. After uploading document and pasting comparison text
2. Click the **"✨ Highlight Suspicious Text"** button
3. Switch to the **"Highlights"** tab
4. See color-coded results!

---

## Color Legend 🎨

| Color | Similarity | Meaning |
|-------|-----------|---------|
| 🔴 **Red** | 95%+ | **CRITICAL** - Exact match or nearly identical |
| 🟠 **Orange** | 85-94% | **HIGH** - Very similar, likely plagiarism |
| 🟡 **Yellow** | 75-84% | **MEDIUM** - Substantially similar |
| 🟨 **Light Yellow** | 60-74% | **LOW** - Somewhat similar |

---

## What's Being Compared?

✅ **Uploaded Document:** `/tmp/sample_document.txt` (AI Ethics content)
✅ **Pasted Text:** Whatever you paste in the comparison field
✅ **Algorithm:** Sentence-level similarity using SequenceMatcher
✅ **Threshold:** 0.60 (matches 60% and above)

---

## Debugging Tips

If highlighting shows **"0 out of X sentences"**:

1. **Check that a document is uploaded**
   - Look for "File Info" section showing filename and text length
   
2. **Ensure pasted text is substantial**
   - At least 1-2 full sentences for best results
   
3. **Use the sample text above**
   - It's guaranteed to match with the uploaded document

4. **Open Browser Console** (F12) and check for errors:
   - Look for failed fetch requests
   - Check the file_id being used

---

## Test Results Expected

| Test | Upload | Paste | Expected Highlighting |
|------|--------|-------|----------------------|
| 1 | sample_document.txt | Example 1 | 2-3 Yellow sentences |
| 2 | sample_document.txt | Example 2 | 2 Red sentences |
| 3 | sample_document.txt | Example 3 | 4-5 mixed colors |
| 4 | sample_document.txt | Example 4 | 1-2 Light Yellow |

---

## Troubleshooting

**Problem:** Button says "Highlights" tab doesn't appear
- **Solution:** Click refresh (⟳) after highlighting completes

**Problem:** 0% matches shown
- **Solution:** Make sure your pasted text actually relates to the uploaded document

**Problem:** Similarity shows 0 for everything
- **Solution:** Open browser console (F12), check error messages in "Network" tab

**Problem:** Colors not showing
- **Solution:** Hard refresh browser (Cmd+Shift+R on Mac)

---

## Need More Help?

1. Share a screenshot showing:
   - What filename was uploaded
   - What text you pasted
   - What results you got

2. Use the debug endpoint (if needed):
   ```bash
   curl -X POST http://localhost:5001/api/debug/highlight-test \
     -H "Content-Type: application/json" \
     -d '{"file_id": "YOUR_FILE_ID", "comparison_text": "your pasted text"}'
   ```

---

**Happy Testing! 🚀**
