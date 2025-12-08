# pdf_rescue_tkinter

**File:** `modules/pdf_rescue_tkinter.py`
**Lines:** 909
**Classes:** 2
**Functions:** 0

---

## Module Description

PDF Rescue Module
Embeddable version of the AI-powered OCR tool for extracting text from poorly formatted PDFs
Uses OpenAI's GPT-4 Vision API

This module can be embedded in the main Supervertaler application as a tab.

---

## Classes

### `PDFRescue`

**Line:** 21

PDF Rescue feature - extract text from images using AI OCR
Can be embedded in any tkinter application as a tab or panel

#### Methods

##### `log_message()`

Log a message to the parent app's log if available

##### `create_tab()`

Create the PDF Rescue tab UI

Args:
    parent: The parent widget (notebook tab or frame)


---

### `StandaloneApp`

**Line:** 841

Minimal parent app for standalone mode

#### Methods

##### `log()`

Add message to log

##### `run()`

Start the application


---

