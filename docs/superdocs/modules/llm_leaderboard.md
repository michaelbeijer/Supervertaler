# llm_leaderboard

**File:** `modules/llm_leaderboard.py`
**Lines:** 737
**Classes:** 5
**Functions:** 3

---

## Module Description

LLM Leaderboard - Core Benchmarking Module
===========================================

Comprehensive LLM translation benchmarking system for Supervertaler.
Compare translation quality, speed, and cost across multiple providers.

Features:
- Multi-provider comparison (OpenAI, Claude, Gemini)
- Quality scoring (chrF++ metric)
- Speed measurement (latency per segment)
- Cost estimation (token-based)
- Test dataset management
- Results export (Excel/CSV)

Author: Michael Beijer
License: MIT

---

## Classes

### `TestSegment`

**Line:** 38

Single test segment with source and reference translation

---

### `BenchmarkResult`

**Line:** 49

Result of translating a single segment with one model

---

### `ModelConfig`

**Line:** 65

Configuration for a single model to test

---

### `TestDataset`

**Line:** 73

Manages test datasets for benchmarking

#### Methods

##### `add_segment()`

Add a test segment to the dataset

##### `to_dict()`

Convert dataset to dictionary for JSON export

##### `from_dict()`

Load dataset from dictionary

##### `from_json_file()`

Load dataset from JSON file

##### `save_to_json()`

Save dataset to JSON file


---

### `LLMLeaderboard`

**Line:** 114

Main benchmarking engine for LLM translation comparison

#### Methods

##### `build_translation_prompt()`

Build translation prompt for a test segment

##### `run_benchmark()`

Run benchmark comparing multiple models on a test dataset

Args:
    dataset: TestDataset to run
    models: List of ModelConfig to test
    progress_callback: Optional callback(current, total, message)

Returns:
    List of BenchmarkResult objects

##### `cancel_benchmark()`

Request cancellation of running benchmark

##### `get_summary_stats()`

Calculate summary statistics from benchmark results

Returns:
    Dict with stats per model:
    {
        "model_name": {
            "avg_latency_ms": float,
            "avg_quality_score": float,
            "success_count": int,
            "error_count": int,
            "total_cost": float
        }
    }

##### `export_to_dict()`

Export results to dictionary for JSON/Excel export


---

## Functions

### `create_sample_datasets()`

**Line:** 481

Create sample test datasets for quick testing

---

### `create_dataset_from_project()`

**Line:** 568

Create test dataset from current Supervertaler project

Supports two scenarios:
- Translated projects: Uses existing targets as reference for quality scoring
- Untranslated projects: No references, compare speed/cost/outputs only

Args:
    project: Supervertaler project object with segments
    sample_size: Number of segments to include (default 10)
    sampling_method: "random", "evenly_spaced", or "smart" (default)
    require_targets: If True, only include segments with targets

Returns:
    Tuple of (TestDataset, metadata_dict)
    metadata_dict contains info about reference availability

---

