"""
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
"""

import time
import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import threading

try:
    from sacrebleu.metrics import CHRF
    CHRF_AVAILABLE = True
except ImportError:
    CHRF_AVAILABLE = False
    print("Warning: sacrebleu not installed. Quality scoring will be disabled.")
    print("Install with: pip install sacrebleu")


@dataclass
class TestSegment:
    """Single test segment with source and reference translation"""
    id: int
    source: str
    reference: str
    domain: str = "general"
    direction: str = "EN→NL"
    context: str = ""


@dataclass
class BenchmarkResult:
    """Result of translating a single segment with one model"""
    segment_id: int
    model_name: str
    provider: str
    model_id: str
    output: str
    latency_ms: float
    quality_score: Optional[float] = None
    error: Optional[str] = None
    tokens_input: Optional[int] = None
    tokens_output: Optional[int] = None
    cost_estimate: Optional[float] = None


@dataclass
class ModelConfig:
    """Configuration for a single model to test"""
    name: str  # Display name (e.g., "GPT-4o")
    provider: str  # "openai", "claude", "gemini"
    model_id: str  # Actual model ID for API
    enabled: bool = True


class TestDataset:
    """Manages test datasets for benchmarking"""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.segments: List[TestSegment] = []

    def add_segment(self, segment: TestSegment):
        """Add a test segment to the dataset"""
        self.segments.append(segment)

    def to_dict(self) -> Dict:
        """Convert dataset to dictionary for JSON export"""
        return {
            "name": self.name,
            "description": self.description,
            "segments": [asdict(seg) for seg in self.segments]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'TestDataset':
        """Load dataset from dictionary"""
        dataset = cls(data["name"], data.get("description", ""))
        for seg_data in data.get("segments", []):
            dataset.add_segment(TestSegment(**seg_data))
        return dataset

    @classmethod
    def from_json_file(cls, filepath: Path) -> 'TestDataset':
        """Load dataset from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)

    def save_to_json(self, filepath: Path):
        """Save dataset to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)


class LLMLeaderboard:
    """Main benchmarking engine for LLM translation comparison"""

    def __init__(self, llm_client_factory, log_callback=None):
        """
        Initialize LLM Leaderboard

        Args:
            llm_client_factory: Function that creates LLMClient instances
                                Signature: (provider: str, model: str) -> LLMClient
            log_callback: Optional callback for logging messages
        """
        self.llm_client_factory = llm_client_factory
        self.log = log_callback if log_callback else print
        self.chrf_metric = CHRF(word_order=2) if CHRF_AVAILABLE else None
        self.results: List[BenchmarkResult] = []
        self.is_running = False
        self.cancel_requested = False

    def _lang_code_to_name(self, code: str) -> str:
        """Convert language code to full language name for LLM prompts"""
        # Common language codes to names mapping
        lang_map = {
            "en": "English", "en-us": "English", "en-gb": "English",
            "nl": "Dutch", "nl-nl": "Dutch", "nl-be": "Dutch (Belgian)",
            "de": "German", "de-de": "German", "de-at": "German (Austrian)",
            "fr": "French", "fr-fr": "French", "fr-be": "French (Belgian)",
            "es": "Spanish", "es-es": "Spanish", "es-mx": "Spanish (Mexican)",
            "it": "Italian", "it-it": "Italian",
            "pt": "Portuguese", "pt-pt": "Portuguese", "pt-br": "Portuguese (Brazilian)",
            "ru": "Russian", "ru-ru": "Russian",
            "zh": "Chinese", "zh-cn": "Chinese (Simplified)", "zh-tw": "Chinese (Traditional)",
            "ja": "Japanese", "ja-jp": "Japanese",
            "ko": "Korean", "ko-kr": "Korean",
            "ar": "Arabic", "ar-sa": "Arabic",
            "pl": "Polish", "pl-pl": "Polish",
            "sv": "Swedish", "sv-se": "Swedish",
            "da": "Danish", "da-dk": "Danish",
            "no": "Norwegian", "nb-no": "Norwegian",
            "fi": "Finnish", "fi-fi": "Finnish",
            "cs": "Czech", "cs-cz": "Czech",
            "tr": "Turkish", "tr-tr": "Turkish",
            "el": "Greek", "el-gr": "Greek",
            "he": "Hebrew", "he-il": "Hebrew",
            "hi": "Hindi", "hi-in": "Hindi",
            "th": "Thai", "th-th": "Thai",
            "vi": "Vietnamese", "vi-vn": "Vietnamese",
            "id": "Indonesian", "id-id": "Indonesian",
            "ms": "Malay", "ms-my": "Malay",
            "uk": "Ukrainian", "uk-ua": "Ukrainian",
            "ro": "Romanian", "ro-ro": "Romanian",
            "hu": "Hungarian", "hu-hu": "Hungarian",
            "bg": "Bulgarian", "bg-bg": "Bulgarian",
            "hr": "Croatian", "hr-hr": "Croatian",
            "sr": "Serbian", "sr-rs": "Serbian",
            "sk": "Slovak", "sk-sk": "Slovak",
            "sl": "Slovenian", "sl-si": "Slovenian",
            "lt": "Lithuanian", "lt-lt": "Lithuanian",
            "lv": "Latvian", "lv-lv": "Latvian",
            "et": "Estonian", "et-ee": "Estonian",
        }

        # Normalize code to lowercase
        code_lower = code.lower().strip()

        # Return mapped name or capitalize the code as fallback
        return lang_map.get(code_lower, code.upper())

    def build_translation_prompt(self, segment: TestSegment) -> str:
        """Build translation prompt for a test segment"""
        # Extract language codes from direction (e.g., "EN→NL" or "en→nl")
        parts = segment.direction.split("→")
        source_code = parts[0].strip() if len(parts) > 0 else "source language"
        target_code = parts[1].strip() if len(parts) > 1 else "target language"

        # Convert codes to full language names
        source_lang = self._lang_code_to_name(source_code)
        target_lang = self._lang_code_to_name(target_code)
        direction_hint = f"from {source_lang} to {target_lang}"

        prompt = f"""You are a professional translator. Translate the following text {direction_hint}.

Domain: {segment.domain}
Target language: {target_lang}
Requirements: Be faithful to meaning, natural, and correct. Preserve units, numbers, and formatting. Keep terminology consistent.

Text to translate:
{segment.source}

Return ONLY the translation, no explanations or additional text."""

        if segment.context:
            prompt = f"Context: {segment.context}\n\n{prompt}"

        return prompt

    def run_benchmark(
        self,
        dataset: TestDataset,
        models: List[ModelConfig],
        progress_callback=None
    ) -> List[BenchmarkResult]:
        """
        Run benchmark comparing multiple models on a test dataset

        Args:
            dataset: TestDataset to run
            models: List of ModelConfig to test
            progress_callback: Optional callback(current, total, message)

        Returns:
            List of BenchmarkResult objects
        """
        self.is_running = True
        self.cancel_requested = False
        self.results = []

        enabled_models = [m for m in models if m.enabled]
        total_tests = len(dataset.segments) * len(enabled_models)
        current_test = 0

        self.log(f"Starting benchmark: {dataset.name}")
        self.log(f"   Models: {', '.join(m.name for m in enabled_models)}")
        self.log(f"   Segments: {len(dataset.segments)}")
        self.log(f"   Total translations: {total_tests}")

        for segment in dataset.segments:
            if self.cancel_requested:
                self.log("Warning: Benchmark cancelled by user")
                break

            prompt = self.build_translation_prompt(segment)

            for model_config in enabled_models:
                if self.cancel_requested:
                    break

                current_test += 1

                # Progress update
                if progress_callback:
                    progress_callback(
                        current_test,
                        total_tests,
                        f"Testing {model_config.name} on segment {segment.id}"
                    )

                # Run translation and measure time
                result = self._translate_segment(
                    segment,
                    model_config,
                    prompt
                )

                self.results.append(result)

                # Log result
                if result.error:
                    self.log(f"   ERROR {model_config.name} seg {segment.id}: {result.error}")
                else:
                    quality_str = f", chrF++: {result.quality_score:.1f}" if result.quality_score else ""
                    self.log(f"   OK {model_config.name} seg {segment.id}: {result.latency_ms:.0f}ms{quality_str}")

        self.is_running = False
        self.log(f"Benchmark complete: {len(self.results)} results")

        return self.results

    def _translate_segment(
        self,
        segment: TestSegment,
        model_config: ModelConfig,
        prompt: str
    ) -> BenchmarkResult:
        """Translate a single segment with one model and measure performance"""

        result = BenchmarkResult(
            segment_id=segment.id,
            model_name=model_config.name,
            provider=model_config.provider,
            model_id=model_config.model_id,
            output="",
            latency_ms=0.0
        )

        try:
            self.log(f"   DEBUG: Starting translation for segment {segment.id} with {model_config.name}")

            # Validate segment data first
            if not segment:
                result.error = "Null segment"
                self.log(f"   ERROR: Null segment received")
                return result

            if not hasattr(segment, 'id') or segment.id is None:
                result.error = "Segment missing ID"
                self.log(f"   ERROR: Segment missing ID")
                return result

            if not hasattr(segment, 'source'):
                result.error = f"Segment {segment.id} missing source attribute"
                self.log(f"   ERROR: {result.error}")
                return result

            # Validate segment source text
            if not segment.source or not segment.source.strip():
                result.error = "Empty source text"
                self.log(f"   ERROR: Segment {segment.id} has empty source text")
                return result

            # Parse language codes from direction
            if not hasattr(segment, 'direction') or not segment.direction:
                result.error = f"Segment {segment.id} missing direction"
                self.log(f"   ERROR: {result.error}")
                return result

            try:
                direction_parts = segment.direction.split("→")
                if len(direction_parts) != 2:
                    raise ValueError(f"Invalid direction format: {segment.direction}")
                source_lang = direction_parts[0].strip().lower()
                target_lang = direction_parts[1].strip().lower()

                if not source_lang or not target_lang:
                    raise ValueError(f"Empty language codes in direction: {segment.direction}")
            except Exception as lang_err:
                result.error = f"Invalid language direction: {segment.direction} - {str(lang_err)}"
                self.log(f"   ERROR: {result.error}")
                return result

            # Create LLM client with error handling
            try:
                self.log(f"   DEBUG: Creating client for {model_config.provider} with model {model_config.model_id}")
                client = self.llm_client_factory(model_config.provider, model_config.model_id)
                if not client:
                    result.error = f"Failed to create {model_config.provider} client"
                    self.log(f"   ERROR: {result.error}")
                    return result
                self.log(f"   DEBUG: Client created successfully")
            except Exception as client_err:
                result.error = f"Client creation failed: {str(client_err)}"
                self.log(f"   ERROR: {result.error}")
                return result

            # Measure translation time with comprehensive error handling
            try:
                start_time = time.perf_counter()
                source_preview = segment.source[:50] + "..." if len(segment.source) > 50 else segment.source
                self.log(f"   DEBUG: Calling translate with text='{source_preview}', source={source_lang}, target={target_lang}")

                output = client.translate(
                    text=segment.source,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    custom_prompt=prompt
                )
                elapsed_time = time.perf_counter() - start_time

                # Validate output
                if output is None:
                    result.error = "Translation returned None"
                    self.log(f"   ERROR: {result.error}")
                    return result

                output_preview = output[:50] if output else 'EMPTY'
                self.log(f"   DEBUG: Translation received: '{output_preview}...'")

                result.output = output if isinstance(output, str) else str(output)
                result.latency_ms = elapsed_time * 1000

            except Exception as translate_err:
                result.error = f"Translation failed: {str(translate_err)}"
                self.log(f"   ERROR: {result.error}")
                import traceback
                self.log(f"   TRACEBACK: {traceback.format_exc()}")
                return result

            # Calculate quality score if reference is available
            if self.chrf_metric and segment.reference and segment.reference.strip():
                try:
                    score = self.chrf_metric.corpus_score([output], [[segment.reference]])
                    result.quality_score = score.score
                    self.log(f"   DEBUG: chrF++ score calculated: {result.quality_score:.1f}")
                except Exception as score_err:
                    self.log(f"   WARNING: chrF++ scoring failed for segment {segment.id}: {score_err}")
                    result.quality_score = None

            # TODO: Token counting and cost estimation
            # Would need to access response metadata from LLM client

        except Exception as e:
            import traceback
            result.error = str(e)
            error_details = traceback.format_exc()
            self.log(f"   ERROR: Exception translating segment {segment.id} with {model_config.name}")
            self.log(f"   ERROR: {str(e)}")
            self.log(f"   ERROR: Traceback:\n{error_details}")

        return result

    def cancel_benchmark(self):
        """Request cancellation of running benchmark"""
        self.cancel_requested = True

    def get_summary_stats(self) -> Dict:
        """
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
        """
        stats = {}

        for result in self.results:
            if result.model_name not in stats:
                stats[result.model_name] = {
                    "latencies": [],
                    "quality_scores": [],
                    "success_count": 0,
                    "error_count": 0,
                    "total_cost": 0.0
                }

            model_stats = stats[result.model_name]

            if result.error:
                model_stats["error_count"] += 1
            else:
                model_stats["success_count"] += 1
                model_stats["latencies"].append(result.latency_ms)

                if result.quality_score is not None:
                    model_stats["quality_scores"].append(result.quality_score)

                if result.cost_estimate is not None:
                    model_stats["total_cost"] += result.cost_estimate

        # Calculate averages
        summary = {}
        for model_name, data in stats.items():
            summary[model_name] = {
                "avg_latency_ms": sum(data["latencies"]) / len(data["latencies"]) if data["latencies"] else 0,
                "avg_quality_score": sum(data["quality_scores"]) / len(data["quality_scores"]) if data["quality_scores"] else None,
                "success_count": data["success_count"],
                "error_count": data["error_count"],
                "total_cost": data["total_cost"]
            }

        return summary

    def export_to_dict(self) -> Dict:
        """Export results to dictionary for JSON/Excel export"""
        return {
            "results": [asdict(r) for r in self.results],
            "summary": self.get_summary_stats()
        }


def create_sample_datasets() -> List[TestDataset]:
    """Create sample test datasets for quick testing"""

    # Business EN→NL dataset
    business_en_nl = TestDataset(
        name="Business EN→NL",
        description="Formal business correspondence and documents"
    )

    business_segments = [
        TestSegment(1, "We are pleased to inform you that your order has been processed.",
                   "Wij zijn verheugd u te kunnen mededelen dat uw bestelling is verwerkt.",
                   "business", "EN→NL", "formal business email"),
        TestSegment(2, "Please find attached the invoice for your recent purchase.",
                   "In de bijlage treft u de factuur aan voor uw recente aankoop.",
                   "business", "EN→NL", "business correspondence"),
        TestSegment(3, "We would like to schedule a meeting to discuss the project timeline.",
                   "Wij willen graag een vergadering plannen om de projectplanning te bespreken.",
                   "business", "EN→NL", "project management"),
        TestSegment(4, "The annual report will be published next quarter.",
                   "Het jaarverslag zal volgend kwartaal worden gepubliceerd.",
                   "business", "EN→NL", "corporate communication"),
        TestSegment(5, "Thank you for your prompt response to our inquiry.",
                   "Hartelijk dank voor uw snelle reactie op onze vraag.",
                   "business", "EN→NL", "business email"),
    ]

    for seg in business_segments:
        business_en_nl.add_segment(seg)

    # Technical EN→NL dataset
    technical_en_nl = TestDataset(
        name="Technical EN→NL",
        description="Technical documentation and user manuals"
    )

    technical_segments = [
        TestSegment(1, "Press the power button to turn on the device.",
                   "Druk op de aan/uit-knop om het apparaat in te schakelen.",
                   "technical", "EN→NL", "user manual"),
        TestSegment(2, "The software supports Windows 10 and later versions.",
                   "De software ondersteunt Windows 10 en latere versies.",
                   "technical", "EN→NL", "system requirements"),
        TestSegment(3, "Ensure that all cables are properly connected before starting.",
                   "Zorg ervoor dat alle kabels correct zijn aangesloten voordat u begint.",
                   "technical", "EN→NL", "installation guide"),
        TestSegment(4, "The battery life is approximately 8 hours under normal usage.",
                   "De batterijduur bedraagt ongeveer 8 uur bij normaal gebruik.",
                   "technical", "EN→NL", "product specifications"),
        TestSegment(5, "For technical support, please contact our service department.",
                   "Neem voor technische ondersteuning contact op met onze serviceafdeling.",
                   "technical", "EN→NL", "support information"),
    ]

    for seg in technical_segments:
        technical_en_nl.add_segment(seg)

    # Legal NL→EN dataset
    legal_nl_en = TestDataset(
        name="Legal NL→EN",
        description="Legal contracts and formal documents"
    )

    legal_segments = [
        TestSegment(1, "De partijen zijn overeengekomen als volgt.",
                   "The parties have agreed as follows.",
                   "legal", "NL→EN", "contract clause"),
        TestSegment(2, "Deze overeenkomst treedt in werking op de datum van ondertekening.",
                   "This agreement shall enter into force on the date of signature.",
                   "legal", "NL→EN", "contract terms"),
        TestSegment(3, "Beide partijen verklaren bevoegd te zijn deze overeenkomst aan te gaan.",
                   "Both parties declare to be authorized to enter into this agreement.",
                   "legal", "NL→EN", "legal declaration"),
        TestSegment(4, "In geval van geschillen zal bemiddeling worden gezocht.",
                   "In case of disputes, mediation shall be sought.",
                   "legal", "NL→EN", "dispute resolution"),
        TestSegment(5, "Deze overeenkomst is onderworpen aan Nederlands recht.",
                   "This agreement is governed by Dutch law.",
                   "legal", "NL→EN", "governing law"),
    ]

    for seg in legal_segments:
        legal_nl_en.add_segment(seg)

    return [business_en_nl, technical_en_nl, legal_nl_en]


def create_dataset_from_project(
    project,
    sample_size: int = 10,
    sampling_method: str = "smart",
    require_targets: bool = False
) -> Tuple[TestDataset, Dict]:
    """
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
    """
    # Create dataset with project info
    dataset = TestDataset(
        name=f"Project: {getattr(project, 'name', 'Current')}",
        description=f"Sample from current project ({getattr(project, 'source_lang', '??')}→{getattr(project, 'target_lang', '??')})"
    )

    # Get eligible segments
    eligible_segments = []
    translated_count = 0

    for seg in project.segments:
        has_source = seg.source and seg.source.strip()
        has_target = seg.target and seg.target.strip()

        if has_target:
            translated_count += 1

        if require_targets:
            # Only segments with existing translations
            if has_source and has_target:
                eligible_segments.append(seg)
        else:
            # All segments with source text
            if has_source:
                eligible_segments.append(seg)

    # Check if we have enough segments
    if len(eligible_segments) == 0:
        raise ValueError("No eligible segments found in project")

    # Sample segments
    actual_sample_size = min(sample_size, len(eligible_segments))
    sampled = _sample_segments(eligible_segments, actual_sample_size, sampling_method)

    # Create TestSegments
    reference_count = 0
    for i, seg in enumerate(sampled, 1):
        # Use target as reference if available
        reference = seg.target if (seg.target and seg.target.strip()) else ""
        if reference:
            reference_count += 1

        test_seg = TestSegment(
            id=seg.id,
            source=seg.source,
            reference=reference,
            domain=getattr(project, 'domain', 'general'),
            direction=f"{getattr(project, 'source_lang', 'XX')}→{getattr(project, 'target_lang', 'XX')}",
            context=""
        )
        dataset.add_segment(test_seg)

    # Build metadata
    metadata = {
        "total_segments": len(project.segments),
        "translated_count": translated_count,
        "translation_percentage": (translated_count / len(project.segments) * 100) if project.segments else 0,
        "eligible_segments": len(eligible_segments),
        "sampled_segments": len(sampled),
        "segments_with_references": reference_count,
        "has_references": reference_count > 0,
        "quality_scoring_available": reference_count > 0,
        "sampling_method": sampling_method
    }

    return dataset, metadata


def _sample_segments(segments: List, n: int, method: str) -> List:
    """
    Sample segments from project using specified method

    Args:
        segments: List of segment objects
        n: Number of segments to sample
        method: "random", "evenly_spaced", or "smart"

    Returns:
        List of sampled segments
    """
    if len(segments) <= n:
        return segments

    if method == "random":
        return random.sample(segments, n)

    elif method == "evenly_spaced":
        # Stratified sampling - every Nth segment
        step = len(segments) / n
        return [segments[int(i * step)] for i in range(n)]

    elif method == "smart":
        # Smart sampling: representative coverage across document
        # 30% from beginning, 40% from middle, 30% from end
        # Ensures coverage of introduction, main content, and conclusions

        # Divide into sections
        third = len(segments) // 3
        begin = segments[:third]
        middle = segments[third:2*third]
        end = segments[2*third:]

        # Calculate samples per section
        n_begin = int(n * 0.3)
        n_middle = int(n * 0.4)
        n_end = n - n_begin - n_middle

        # Sample from each section
        sampled = []
        if begin and n_begin > 0:
            sampled.extend(random.sample(begin, min(n_begin, len(begin))))
        if middle and n_middle > 0:
            sampled.extend(random.sample(middle, min(n_middle, len(middle))))
        if end and n_end > 0:
            sampled.extend(random.sample(end, min(n_end, len(end))))

        # If we didn't get enough, fill from remaining
        if len(sampled) < n:
            remaining = [s for s in segments if s not in sampled]
            if remaining:
                needed = n - len(sampled)
                sampled.extend(random.sample(remaining, min(needed, len(remaining))))

        return sampled

    else:
        # Default to random if method not recognized
        return random.sample(segments, n)


# For testing/development
if __name__ == "__main__":
    print("LLM Leaderboard - Core Module")
    print("=" * 50)

    # Create sample datasets
    datasets = create_sample_datasets()

    print(f"\nCreated {len(datasets)} sample datasets:")
    for ds in datasets:
        print(f"  • {ds.name}: {len(ds.segments)} segments")

    # Check if chrF++ is available
    if CHRF_AVAILABLE:
        print("\n✅ chrF++ quality scoring available")
    else:
        print("\nWarning: chrF++ quality scoring not available (sacrebleu not installed)")
