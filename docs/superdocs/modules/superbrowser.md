# superbrowser

**File:** `modules/superbrowser.py`
**Lines:** 303
**Classes:** 2
**Functions:** 0

---

## Module Description

=============================================================================
MODULE: Superbrowser - Multi-Chat AI Browser
=============================================================================
Display multiple AI chat pages side by side in a single interface.
Supports ChatGPT, Claude, and Gemini in a three-column resizable layout.

Author: Michael Beijer
Date: November 18, 2025
Version: 1.0.0
=============================================================================

---

## Classes

### `ChatColumn`

**Line:** 27

A column containing a chat interface with web browser

#### Methods

##### `init_ui()`

Initialize the chat column UI

##### `load_url()`

Load URL from input field

##### `reload_page()`

Reload the current page

##### `go_home()`

Go back to the home URL

##### `update_url_bar()`

Update URL bar when page changes


---

### `SuperbrowserWidget`

**Line:** 139

Superbrowser - Multi-Chat AI Browser Widget

Displays multiple AI chat interfaces side by side for easy comparison
and concurrent interaction with different AI models.

#### Methods

##### `init_ui()`

Initialize the Superbrowser UI

##### `toggle_configuration()`

Toggle visibility of configuration section

##### `update_urls()`

Update the URLs for all chat columns


---

