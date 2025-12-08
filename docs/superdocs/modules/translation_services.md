# translation_services

**File:** `modules/translation_services.py`
**Lines:** 282
**Classes:** 3
**Functions:** 1

---

## Module Description

Translation Services Module
Handles Machine Translation (MT) and Large Language Model (LLM) integration
Keeps main application file clean and manageable

Author: Michael Beijer
License: MIT

---

## Classes

### `TranslationRequest`

**Line:** 16

Request object for translation services

---

### `TranslationResult`

**Line:** 27

Result object from translation services

---

### `TranslationServices`

**Line:** 39

Main class for handling all translation services (MT and LLM)

#### Methods

##### `get_all_translations()`

Get translations from all available services

Args:
    request: TranslationRequest object
    
Returns:
    List of TranslationResult objects

##### `get_mt_translations()`

Get Machine Translation results

Args:
    request: TranslationRequest object
    
Returns:
    List of TranslationResult objects from MT services

##### `get_llm_translations()`

Get Large Language Model translation results

Args:
    request: TranslationRequest object
    
Returns:
    List of TranslationResult objects from LLM services


---

## Functions

### `create_translation_service()`

**Line:** 272

Factory function to create a TranslationServices instance

Args:
    config: Configuration dictionary
    
Returns:
    TranslationServices instance

---

