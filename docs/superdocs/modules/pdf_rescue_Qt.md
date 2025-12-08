# pdf_rescue_Qt

**File:** `modules/pdf_rescue_Qt.py`
**Lines:** 1,822
**Classes:** 3
**Functions:** 0

---

## Module Description

PDF Rescue Module - Qt Edition
Embeddable version of the AI-powered OCR tool for extracting text from poorly formatted PDFs
Supports multiple AI providers: OpenAI GPT-4 Vision, Anthropic Claude Vision, Google Gemini Vision

This module can be embedded in the main Supervertaler Qt application as a tab.
Can also be run independently as a standalone application.

---

## Classes

### `CheckmarkCheckBox`

**Line:** 27

Custom checkbox with green background and white checkmark when checked - matches Supervertaler Qt style

#### Methods

##### `paintEvent()`

Override paint event to draw white checkmark when checked


---

### `PDFRescueQt`

**Line:** 110

PDF Rescue feature - extract text from images using AI OCR
Can be embedded in any PyQt6 application as a tab or panel

#### Methods

##### `log_message()`

Log a message to the parent app's log if available

##### `create_tab()`

Create the PDF Rescue tab UI

Args:
    parent: The parent widget (QWidget)


---

### `StandaloneApp`

**Line:** 1741

Minimal parent app for standalone mode

#### Methods

##### `log()`

Add message to log

##### `load_api_keys()`

Load API keys for compatibility


---

