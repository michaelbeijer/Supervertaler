# --- Supervertaler (v10) - Multi-LLM AI-powered Translator & Proofreader ---
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import threading
import queue
import os
import re
import math
import xml.etree.ElementTree as ET 
import io 
import sys

PIL_AVAILABLE = False
try:
    from PIL import Image 
    PIL_AVAILABLE = True
except ImportError:
    print("WARNING: Pillow (PIL) library not found. Drawings Image Folder feature will be disabled.")

# --- Library Import Checks ---
GOOGLE_AI_AVAILABLE = False
GOOGLE_AI_IMPORT_ERROR_MESSAGE = ""
GENAI_VERSION = "unknown"

print("--- Supervertaler Script: Attempting to import google.generativeai ---")
try:
    import google.generativeai as genai
    try:
        from google.generativeai.types import GenerationConfig 
    except ImportError:
        print("Note: Could not import GenerationConfig from google.generativeai.types (may not be needed for this script version).")
    
    GENAI_VERSION = getattr(genai, '__version__', 'unknown')
    print(f"SUCCESS: google.generativeai imported. Version: {GENAI_VERSION}")
    GOOGLE_AI_AVAILABLE = True
except ImportError as e:
    GOOGLE_AI_IMPORT_ERROR_MESSAGE = f"ImportError: {e}\nThe library 'google-generativeai' could not be found by this script."
    print(f"FAIL: {GOOGLE_AI_IMPORT_ERROR_MESSAGE}")
except Exception as e_other:
    GOOGLE_AI_IMPORT_ERROR_MESSAGE = f"An unexpected error occurred during import: {e_other}"
    print(f"FAIL: {GOOGLE_AI_IMPORT_ERROR_MESSAGE}")

CLAUDE_AVAILABLE = False
CLAUDE_IMPORT_ERROR_MESSAGE = ""
ANTHROPIC_VERSION = "unknown"

print("--- Supervertaler Script: Attempting to import anthropic ---")
try:
    import anthropic
    ANTHROPIC_VERSION = getattr(anthropic, '__version__', 'unknown')
    print(f"SUCCESS: anthropic imported. Version: {ANTHROPIC_VERSION}")
    CLAUDE_AVAILABLE = True
except ImportError as e:
    CLAUDE_IMPORT_ERROR_MESSAGE = f"ImportError: {e}\nThe library 'anthropic' could not be found by this script."
    print(f"FAIL: {CLAUDE_IMPORT_ERROR_MESSAGE}")
except Exception as e_other:
    CLAUDE_IMPORT_ERROR_MESSAGE = f"An unexpected error occurred during import: {e_other}"
    print(f"FAIL: {CLAUDE_IMPORT_ERROR_MESSAGE}")

OPENAI_AVAILABLE = False
OPENAI_IMPORT_ERROR_MESSAGE = ""
OPENAI_VERSION = "unknown"

print("--- Supervertaler Script: Attempting to import openai ---")
try:
    import openai
    OPENAI_VERSION = getattr(openai, '__version__', 'unknown')
    print(f"SUCCESS: openai imported. Version: {OPENAI_VERSION}")
    OPENAI_AVAILABLE = True
except ImportError as e:
    OPENAI_IMPORT_ERROR_MESSAGE = f"ImportError: {e}\nThe library 'openai' could not be found by this script."
    print(f"FAIL: {OPENAI_IMPORT_ERROR_MESSAGE}")
except Exception as e_other:
    OPENAI_IMPORT_ERROR_MESSAGE = f"An unexpected error occurred during import: {e_other}"
    print(f"FAIL: {OPENAI_IMPORT_ERROR_MESSAGE}")

# --- API Key Configuration ---
def load_api_keys():
    """Load API keys from api_keys.txt file in the same directory as the script"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    api_keys_file = os.path.join(script_dir, "api_keys.txt")
    
    api_keys = {
        "google": "",
        "claude": "",
        "openai": ""
    }
    
    if os.path.exists(api_keys_file):
        try:
            with open(api_keys_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        if key in ["google", "google_api_key", "gemini"]:
                            api_keys["google"] = value
                        elif key in ["claude", "claude_api_key", "anthropic"]:
                            api_keys["claude"] = value
                        elif key in ["openai", "openai_api_key", "chatgpt"]:
                            api_keys["openai"] = value
        except Exception as e:
            print(f"Error reading api_keys.txt: {e}")
    else:
        # Create template file
        try:
            with open(api_keys_file, 'w', encoding='utf-8') as f:
                f.write("# API Keys Configuration\n")
                f.write("# Format: key_name = your_api_key_here\n")
                f.write("# Remove the # at the beginning of the line to uncomment\n\n")
                f.write("# Google API Key for Gemini models\n")
                f.write("#google = YOUR_GOOGLE_API_KEY_HERE\n\n")
                f.write("# Claude API Key for Anthropic models\n")
                f.write("#claude = YOUR_CLAUDE_API_KEY_HERE\n\n")
                f.write("# OpenAI API Key for ChatGPT models\n")
                f.write("#openai = YOUR_OPENAI_API_KEY_HERE\n")
            print(f"Created template api_keys.txt file at: {api_keys_file}")
        except Exception as e:
            print(f"Could not create api_keys.txt template: {e}")
    
    return api_keys

# Load API keys
API_KEYS = load_api_keys()

# --- Model Definitions ---
GEMINI_MODELS = [
    "gemini-2.5-pro-preview-05-06",
    "gemini-2.5-pro-preview-12-17",
    "gemini-2.5-flash-preview-05-06", 
    "gemini-2.5-flash-preview-12-17",
    "gemini-1.5-pro-latest",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro",
    "gemini-1.5-flash"
]

CLAUDE_MODELS = [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022", 
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307"
]

OPENAI_MODELS = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4-turbo",
    "gpt-4-turbo-preview",
    "gpt-4",
    "gpt-3.5-turbo"
]

# --- Helper Functions ---
def get_simple_lang_code(lang_name_or_code_input):
    if not lang_name_or_code_input: return ""
    lang_lower = lang_name_or_code_input.strip().lower()
    lang_map = {
        "english": "en", "dutch": "nl", "german": "de", "french": "fr",
        "spanish": "es", "italian": "it", "japanese": "ja", "chinese": "zh",
        "russian": "ru", "portuguese": "pt",
    }
    if lang_lower in lang_map: return lang_map[lang_lower]
    base_code = lang_lower.split('-')[0].split('_')[0]
    if len(base_code) == 2: return base_code
    return lang_lower[:2]

def normalize_figure_ref(ref_text):
    if not ref_text: return None
    match = re.search(r"(?:figure|figuur|fig\.?)\s*([\w\d]+(?:[\s\.\-]*[\w\d]+)?)", ref_text, re.IGNORECASE)
    if match:
        identifier = match.group(1); return re.sub(r"[\s\.\-]", "", identifier).lower()
    base_name = os.path.splitext(ref_text)[0]
    cleaned_base = re.sub(r"(?:figure|figuur|fig\.?)\s*", "", base_name, flags=re.IGNORECASE)
    normalized = re.sub(r"[\s\.\-]", "", cleaned_base).lower()
    if normalized: return normalized
    return None

# --- Agent Classes ---
class BilingualFileIngestionAgent:
    def process(self, file_path, log_queue, mode="Translate"):
        log_queue.put(f"[Ingestor] Processing: {file_path} for mode: {mode}")
        data = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f):
                    line = line.rstrip('\n') 
                    if not line.strip(): continue
                    if mode == "Translate":
                        # Simply use the entire line as source text
                        data.append(line.strip())
                    elif mode == "Proofread":
                        parts = line.split('\t', 2) 
                        if len(parts) == 2: data.append({"source": parts[0], "target": parts[1], "comment": None})
                        elif len(parts) == 3: data.append({"source": parts[0], "target": parts[1], "comment": parts[2]})
                        else: log_queue.put(f"[Ingestor] Warn (Proofread): Skip line {line_num+1} (needs 2 or 3 tab-sep cols): {line}")
        except Exception as e: log_queue.put(f"[Ingestor] Err reading {file_path}: {e}"); return []
        log_queue.put(f"[Ingestor] Done. {len(data)} entries/lines loaded.")
        return data

class TMAgent:
    def __init__(self, log_queue):
        self.log_queue = log_queue; self.tm_data = {} 
    def _parse_tmx_lang_xml_code(self, lang_attr_val):
        if lang_attr_val: return lang_attr_val.split('-')[0].split('_')[0].lower()
        return ""
    def load_tm(self, tm_fp, src_lang_gui, tgt_lang_gui):
        self.tm_data = {}; loaded_count = 0
        if not tm_fp: return
        _, ext = os.path.splitext(tm_fp)
        self.log_queue.put(f"[TM Load] Attempting: {tm_fp}")
        gui_src = get_simple_lang_code(src_lang_gui); gui_tgt = get_simple_lang_code(tgt_lang_gui)
        self.log_queue.put(f"[TM Load] GUI Langs for TM: Src='{gui_src}', Tgt='{gui_tgt}'")
        if not gui_src or not gui_tgt: self.log_queue.put("[TM Load] Err: GUI langs for TM not set."); messagebox.showerror("TM Error", "Set GUI Source/Target Langs for TM."); return
        try:
            if ext.lower() == ".tmx":
                tree = ET.parse(tm_fp); root = tree.getroot(); xml_ns = "http://www.w3.org/XML/1998/namespace"
                for tu in root.findall('.//tu'): 
                    src_tuv, tgt_tuv = None, None
                    for tuv_node in tu.findall('tuv'):
                        lang_attr = tuv_node.get(f'{{{xml_ns}}}lang')
                        if not lang_attr: continue
                        tmx_simple_code = self._parse_tmx_lang_xml_code(lang_attr)
                        if tmx_simple_code == gui_src: src_tuv = tuv_node
                        elif tmx_simple_code == gui_tgt: tgt_tuv = tuv_node
                    if src_tuv and tgt_tuv:
                        src_seg_node, tgt_seg_node = src_tuv.find('seg'), tgt_tuv.find('seg')
                        if src_seg_node is not None and tgt_seg_node is not None:
                            try: 
                                src_txt = ET.tostring(src_seg_node, encoding='unicode', method='text').strip()
                                tgt_txt = ET.tostring(tgt_seg_node, encoding='unicode', method='text').strip()
                            except: src_txt = "".join(src_seg_node.itertext()).strip(); tgt_txt = "".join(tgt_seg_node.itertext()).strip()
                            if src_txt: self.tm_data[src_txt] = tgt_txt or ""; loaded_count +=1
                self.log_queue.put(f"[TM Load] Loaded {loaded_count} from TMX.")
            elif ext.lower() == ".txt": 
                with open(tm_fp, 'r', encoding='utf-8') as f:
                    for line in f:
                        parts = line.strip().split('\t', 1)
                        if len(parts) == 2: self.tm_data[parts[0]] = parts[1]; loaded_count += 1
                self.log_queue.put(f"[TM Load] Loaded {loaded_count} from TXT.")
            else: self.log_queue.put(f"[TM Load] Err: Unsupported TM ext: {ext}"); messagebox.showerror("TM Error", f"Unsupported TM type: {ext}.")
        except Exception as e: self.log_queue.put(f"[TM Load] Err: {e}"); messagebox.showerror("TM Load Error", f"TM Load Error: {e}")
    def get_translation(self, src_seg): return self.tm_data.get(src_seg.strip())

# --- Base Agent Classes ---
class BaseTranslationAgent:
    def __init__(self, api_key, log_queue, model_name, provider):
        self.log_queue = log_queue
        self.model = None
        self.model_name = model_name
        self.provider = provider
        self.api_key = api_key

class BaseProofreadingAgent:
    def __init__(self, api_key, log_queue, model_name, provider):
        self.log_queue = log_queue
        self.model = None
        self.model_name = model_name
        self.provider = provider
        self.api_key = api_key

# --- Gemini Agent Classes ---
class GeminiTranslationAgent(BaseTranslationAgent):
    def __init__(self, api_key, log_queue, model_name='gemini-2.5-pro-preview-05-06'): 
        super().__init__(api_key, log_queue, model_name, "Gemini")
        self.model_name = model_name.split('/')[-1] if model_name.startswith("models/") else model_name
        if not GOOGLE_AI_AVAILABLE: self.log_queue.put("[Gemini Translator] ERROR: Google AI library not available."); return
        if not api_key: 
            self.log_queue.put("[Gemini Translator] ERROR: API Key is missing.")
            return
        try:
            genai.configure(api_key=api_key); self.model = genai.GenerativeModel(self.model_name)
            self.log_queue.put(f"[Gemini Translator] Agent with model '{self.model_name}' initialized.")
        except Exception as e: self.log_queue.put(f"[Gemini Translator] ERROR init ('{self.model_name}'): {e}.")

    def translate_specific_lines_with_drawings_context(self, 
                                               lines_map_to_translate, 
                                               full_document_context_text_str,
                                               source_lang, target_lang,
                                               all_source_segments_original_list, 
                                               drawings_images_map, 
                                               user_custom_instructions=""): 
        if not self.model: self.log_queue.put(f"[Gemini Translator] Model ('{self.model_name}') not init."); return {n: f"[Err: Model not init]" for n in lines_map_to_translate.keys()}
        if not lines_map_to_translate: self.log_queue.put(f"[Gemini Translator] No lines for chunk."); return {}
        
        line_nums_being_translated = sorted(list(lines_map_to_translate.keys()))
        self.log_queue.put(f"[Gemini Translator] Translating {len(line_nums_being_translated)} lines: {line_nums_being_translated[:3]}... w/ '{self.model_name}' (drawings if ref)...")

        prompt_parts = [] 
        prompt_parts.append(f"You are an expert {source_lang} to {target_lang} translator specialized in patent documents.")
        if user_custom_instructions: 
            prompt_parts.append(f"\nIMPORTANT USER-PROVIDED INSTRUCTIONS:\n{user_custom_instructions}\n")
        prompt_parts.extend([
            "The full patent text for overall context is in 'FULL PATENT CONTEXT' below. Translate ONLY sentences from 'PATENT SENTENCES TO TRANSLATE' later. These are listed with their original line numbers from the full document.",
            "If a sentence refers to a Figure (e.g., 'Figure 1A', 'Figuur X'), relevant images may be provided just before that sentence. Use these images as crucial context for accurately translating references to parts, features, or relationships shown in those figures.",
            "Present your output ONLY as a numbered list of the translations for the requested sentences, using their original numbering. Maintain accuracy and appropriate patent terminology.\n",
            f"FULL PATENT CONTEXT:\n{full_document_context_text_str}\n",
            "PATENT SENTENCES TO TRANSLATE (translate only these, using preceding images if provided for a figure reference):\n"])
        
        images_added_this_api_call = set()
        for global_ln_num in line_nums_being_translated:
            original_line_text_for_ref_scan = all_source_segments_original_list[global_ln_num - 1] 
            numbered_src_line_to_translate = lines_map_to_translate[global_ln_num]
            found_fig_refs_in_line = re.findall(r"(?:figure|figuur|fig\.?)\s*([\w\d]+(?:[\s\.\-]*[\w\d]+)?)", original_line_text_for_ref_scan, re.IGNORECASE)
            img_added_for_this_line_in_prompt = False
            if PIL_AVAILABLE and found_fig_refs_in_line and drawings_images_map:
                for raw_fig_ref_tuple in found_fig_refs_in_line:
                    raw_fig_ref = raw_fig_ref_tuple if isinstance(raw_fig_ref_tuple, str) else raw_fig_ref_tuple[0]
                    normalized_ref = normalize_figure_ref(f"fig {raw_fig_ref}") 
                    if normalized_ref and normalized_ref in drawings_images_map and normalized_ref not in images_added_this_api_call:
                        pil_image = drawings_images_map[normalized_ref]
                        prompt_parts.append(f"\n--- Context Image: Figure {raw_fig_ref} (Referenced in or near the following text) ---")
                        prompt_parts.append(pil_image) 
                        images_added_this_api_call.add(normalized_ref); img_added_for_this_line_in_prompt = True
                        self.log_queue.put(f"[Gemini Translator] Added Image for Figure Ref '{raw_fig_ref}' (norm: {normalized_ref}) for line {global_ln_num}.")
            prompt_parts.append(numbered_src_line_to_translate) 
            if img_added_for_this_line_in_prompt: prompt_parts.append("\n") 
        
        prompt_parts.append("\nTRANSLATED SENTENCES (numbered list for 'PATENT SENTENCES TO TRANSLATE' only):")

        try:
            response = self.model.generate_content(prompt_parts) 
            raw_text = response.text 
            if not raw_text and hasattr(response, 'prompt_feedback'): self.log_queue.put(f"[Gemini Translator] Warn: Empty response. Feedback: {response.prompt_feedback}")
            elif not raw_text: self.log_queue.put(f"[Gemini Translator] Warn: Empty response for lines {line_nums_being_translated}. Response: {response}")

            translations = {}
            for line in (raw_text or "").splitlines():
                match = re.match(r"^\s*(\d+)\.\s*(.*)", line.strip())
                if match: 
                    num = int(match.group(1))
                    text = match.group(2).strip()
                    if num in line_nums_being_translated: 
                        translations[num] = text
            for num in line_nums_being_translated:
                if num not in translations: 
                    self.log_queue.put(f"[Gemini Translator] Warn: Missing TL line {num}. Placeholder.") 
                    translations[num] = f"[TL Missing line {num}]"
            self.log_queue.put(f"[Gemini Translator] Multimodal TL for chunk done. Got {len(translations)} segs.")
            return translations
        except Exception as e:
            self.log_queue.put(f"[Gemini Translator] Error multimodal TL ('{self.model_name}'): {e}")
            return {n: f"[TL Err line {n} (multimodal): {e}]" for n in line_nums_being_translated}

class GeminiProofreadingAgent(BaseProofreadingAgent):
    def __init__(self, api_key, log_queue, model_name='gemini-2.5-pro-preview-05-06'):
        super().__init__(api_key, log_queue, model_name, "Gemini")
        self.model_name = model_name.split('/')[-1] if model_name.startswith("models/") else model_name
        if not GOOGLE_AI_AVAILABLE: self.log_queue.put("[Gemini Proofreader] ERROR: Google AI library not available."); return
        if not api_key:
            self.log_queue.put("[Gemini Proofreader] ERROR: API Key is missing."); return
        try:
            genai.configure(api_key=api_key); self.model = genai.GenerativeModel(self.model_name)
            self.log_queue.put(f"[Gemini Proofreader] Agent initialized with model '{self.model_name}'.")
        except Exception as e: self.log_queue.put(f"[Gemini Proofreader] ERROR initializing ('{self.model_name}'): {e}.")

    def proofread_specific_lines_with_context(self, lines_to_proofread_map, full_source_doc_str,
                                             full_original_target_doc_str, source_lang, target_lang,
                                             all_source_segments_original_list, drawings_images_map,
                                             user_custom_instructions=""):
        if not self.model: self.log_queue.put(f"[Gemini Proofreader] Model not initialized."); return {n: {"revised_target": lines_to_proofread_map[n]["target_original"], "changes_summary": "[Proofread Err: Model not init]"} for n in lines_to_proofread_map.keys()}
        if not lines_to_proofread_map: self.log_queue.put(f"[Gemini Proofreader] No lines for proofreading chunk."); return {}

        line_nums_being_proofread = sorted(list(lines_to_proofread_map.keys()))
        self.log_queue.put(f"[Gemini Proofreader] Proofreading {len(line_nums_being_proofread)} lines: {line_nums_being_proofread[:3]}... w/ '{self.model_name}'...")

        prompt_parts = [f"You are an expert proofreader and editor for {source_lang} to {target_lang} translations, specializing in patent documents."]
        if user_custom_instructions: prompt_parts.append(f"\nIMPORTANT USER-PROVIDED INSTRUCTIONS:\n{user_custom_instructions}\n")
        prompt_parts.extend([
            "For each segment below, you are given the 'SOURCE SEGMENT' and the 'EXISTING TRANSLATION'. Review the 'EXISTING TRANSLATION' against the 'SOURCE SEGMENT' based on the following criteria, using the 'FULL SOURCE DOCUMENT CONTEXT' and 'FULL ORIGINAL TARGET DOCUMENT CONTEXT' (provided earlier, if any) for reference. If images for Figures are provided with a segment, use them as crucial context.",
            "Checks to perform:\n1. Accuracy: Faithfully convey source meaning. Correct mistranslations.\n2. Terminology: Ensure correct and consistent use of patent-specific terms.\n3. Tone & Style: Ensure formal, objective, and precise tone appropriate for patents.\n4. Grammar, Spelling, Punctuation: Correct all errors in the {target_lang} translation.\n5. Fluency & Naturalness: Ensure smooth, natural {target_lang} reading.\n6. Completeness: No omissions or additions.\n7. Figure Reference Consistency: Align with any provided images for figure refs.",
            f"Your response MUST be structured as follows:\nFirst, provide a numbered list of ONLY the revised and improved {target_lang} translations for each segment. If an existing translation is already perfect and needs NO changes, return the original EXISTING TRANSLATION for that number.\nSecond, after the complete list of revised translations, add a section explicitly titled '---CHANGES SUMMARY START---'. Under this title, for EACH line number that you modified, provide a brief, clear explanation of the key changes you made (e.g., '27. Corrected spelling; rephrased for flow.'). If NO changes were made to ANY segment in this batch, this section should contain only the text 'No changes made to any segment in this batch.'.\nEnd this section with '---CHANGES SUMMARY END---'.\n",
            f"FULL SOURCE DOCUMENT CONTEXT (for your reference):\n{full_source_doc_str}\n",
            f"FULL ORIGINAL TARGET DOCUMENT CONTEXT (for consistency reference):\n{full_original_target_doc_str}\n",
            "SEGMENTS FOR PROOFREADING (review 'EXISTING TRANSLATION' for each, using preceding images if provided for a figure reference in source):\n"])

        images_added_this_api_call = set()
        for global_ln_num in line_nums_being_proofread:
            segment_data = lines_to_proofread_map[global_ln_num]
            original_source_text_for_ref_scan = all_source_segments_original_list[global_ln_num - 1]
            fig_refs = re.findall(r"(?:figure|figuur|fig\.?)\s*([\w\d]+(?:[\s\.\-]*[\w\d]+)?)", original_source_text_for_ref_scan, re.IGNORECASE)
            if PIL_AVAILABLE and fig_refs and drawings_images_map:
                for raw_fig_ref_tuple in fig_refs:
                    raw_fig_ref = raw_fig_ref_tuple if isinstance(raw_fig_ref_tuple, str) else raw_fig_ref_tuple[0]
                    normalized_ref = normalize_figure_ref(f"fig {raw_fig_ref}")
                    if normalized_ref and normalized_ref in drawings_images_map and normalized_ref not in images_added_this_api_call:
                        pil_image = drawings_images_map[normalized_ref]
                        prompt_parts.append(f"\n--- Context Image: Figure {raw_fig_ref} (for segment {global_ln_num}) ---")
                        prompt_parts.append(pil_image)
                        images_added_this_api_call.add(normalized_ref)
            prompt_parts.append(f"{global_ln_num}. SOURCE SEGMENT: {segment_data['source']}")
            prompt_parts.append(f"{global_ln_num}. EXISTING TRANSLATION: {segment_data['target_original']}")
            prompt_parts.append("\n")
        prompt_parts.append(f"\nREVISED AND PROOFREAD {target_lang.upper()} TARGET SENTENCES (numbered list for the segments above only):")

        try:
            response = self.model.generate_content(prompt_parts)
            raw_text_response = response.text 
            
            if not raw_text_response and hasattr(response, 'prompt_feedback'): self.log_queue.put(f"[Gemini Proofreader] Warn: Empty response. Feedback: {response.prompt_feedback}")
            elif not raw_text_response: self.log_queue.put(f"[Gemini Proofreader] Warn: Empty response for lines {line_nums_being_proofread}. Response: {response}")

            parsed_results = {}
            translations_text_block, changes_summary_block = raw_text_response, ""
            summary_start_marker, summary_end_marker = "---CHANGES SUMMARY START---", "---CHANGES SUMMARY END---"
            if summary_start_marker in raw_text_response:
                parts = raw_text_response.split(summary_start_marker, 1)
                translations_text_block = parts[0].strip()
                if len(parts) > 1:
                    summary_part = parts[1]
                    changes_summary_block = summary_part.split(summary_end_marker, 1)[0].strip() if summary_end_marker in summary_part else summary_part.strip()
            
            for line in (translations_text_block or "").splitlines():
                match = re.match(r"^\s*(\d+)\.\s*(.*)", line.strip())
                if match:
                    num = int(match.group(1))
                    text = match.group(2).strip() 
                    if num in line_nums_being_proofread: 
                        parsed_results.setdefault(num, {})["revised_target"] = text
            
            parsed_summaries = {}
            if "No changes made to any segment in this batch." not in changes_summary_block and changes_summary_block:
                for line in changes_summary_block.splitlines():
                    match = re.match(r"^\s*(\d+)\.\s*(.*)", line.strip())
                    if match: parsed_summaries[match.group(1)] = match.group(2).strip()
            
            for num in line_nums_being_proofread:
                if num not in parsed_results: parsed_results[num] = {}
                if "revised_target" not in parsed_results[num]:
                    parsed_results[num]["revised_target"] = lines_to_proofread_map[num]["target_original"]
                    self.log_queue.put(f"[Gemini Proofreader] Warn: Missing revised target for line {num}. Using original.")
                parsed_results[num]["changes_summary"] = parsed_summaries.get(str(num))
                parsed_results[num]["original_target"] = lines_to_proofread_map[num]["target_original"]
            self.log_queue.put(f"[Gemini Proofreader] Proofreading for chunk done. Processed {len(parsed_results)} segments.")
            return parsed_results
        except Exception as e:
            self.log_queue.put(f"[Gemini Proofreader] Error during proofreading ('{self.model_name}'): {e}")
            return {n: {"revised_target": lines_to_proofread_map[n]["target_original"], "changes_summary": f"[Proofread Err line {n}: {e}]"} for n in line_nums_being_proofread}

# --- Claude Agent Classes ---
class ClaudeTranslationAgent(BaseTranslationAgent):
    def __init__(self, api_key, log_queue, model_name='claude-3-5-sonnet-20241022'):
        super().__init__(api_key, log_queue, model_name, "Claude")
        if not CLAUDE_AVAILABLE: self.log_queue.put("[Claude Translator] ERROR: Anthropic library not available."); return
        if not api_key:
            self.log_queue.put("[Claude Translator] ERROR: API Key is missing.")
            return
        try:
            self.client = anthropic.Anthropic(api_key=api_key)
            self.model = True  # Flag to indicate successful initialization
            self.log_queue.put(f"[Claude Translator] Agent with model '{self.model_name}' initialized.")
        except Exception as e: self.log_queue.put(f"[Claude Translator] ERROR init ('{self.model_name}'): {e}.")

    def translate_specific_lines_with_drawings_context(self,
                                               lines_map_to_translate,
                                               full_document_context_text_str,
                                               source_lang, target_lang,
                                               all_source_segments_original_list,
                                               drawings_images_map,
                                               user_custom_instructions=""):
        if not self.model: self.log_queue.put(f"[Claude Translator] Model ('{self.model_name}') not init."); return {n: f"[Err: Model not init]" for n in lines_map_to_translate.keys()}
        if not lines_map_to_translate: self.log_queue.put(f"[Claude Translator] No lines for chunk."); return {}

        line_nums_being_translated = sorted(list(lines_map_to_translate.keys()))
        self.log_queue.put(f"[Claude Translator] Translating {len(line_nums_being_translated)} lines: {line_nums_being_translated[:3]}... w/ '{self.model_name}' (drawings if ref)...")

        # Build system prompt
        system_prompt = f"You are an expert {source_lang} to {target_lang} translator specialized in patent documents."
        if user_custom_instructions:
            system_prompt += f"\n\nIMPORTANT USER-PROVIDED INSTRUCTIONS:\n{user_custom_instructions}"

        # Build user prompt
        user_prompt_parts = []
        user_prompt_parts.extend([
            "The full patent text for overall context is in 'FULL PATENT CONTEXT' below. Translate ONLY sentences from 'PATENT SENTENCES TO TRANSLATE' later. These are listed with their original line numbers from the full document.",
            "If a sentence refers to a Figure (e.g., 'Figure 1A', 'Figuur X'), relevant images may be provided just before that sentence. Use these images as crucial context for accurately translating references to parts, features, or relationships shown in those figures.",
            "Present your output ONLY as a numbered list of the translations for the requested sentences, using their original numbering. Maintain accuracy and appropriate patent terminology.\n",
            f"FULL PATENT CONTEXT:\n{full_document_context_text_str}\n",
            "PATENT SENTENCES TO TRANSLATE (translate only these, using preceding images if provided for a figure reference):\n"])

        # Build message content with images
        message_content = []
        current_text = "\n".join(user_prompt_parts)
        
        images_added_this_api_call = set()
        for global_ln_num in line_nums_being_translated:
            original_line_text_for_ref_scan = all_source_segments_original_list[global_ln_num - 1]
            numbered_src_line_to_translate = lines_map_to_translate[global_ln_num]
            found_fig_refs_in_line = re.findall(r"(?:figure|figuur|fig\.?)\s*([\w\d]+(?:[\s\.\-]*[\w\d]+)?)", original_line_text_for_ref_scan, re.IGNORECASE)
            
            if PIL_AVAILABLE and found_fig_refs_in_line and drawings_images_map:
                for raw_fig_ref_tuple in found_fig_refs_in_line:
                    raw_fig_ref = raw_fig_ref_tuple if isinstance(raw_fig_ref_tuple, str) else raw_fig_ref_tuple[0]
                    normalized_ref = normalize_figure_ref(f"fig {raw_fig_ref}")
                    if normalized_ref and normalized_ref in drawings_images_map and normalized_ref not in images_added_this_api_call:
                        pil_image = drawings_images_map[normalized_ref]
                        current_text += f"\n--- Context Image: Figure {raw_fig_ref} (Referenced in or near the following text) ---\n"
                        
                        # Convert PIL image to base64 for Claude
                        import base64
                        import io as image_io
                        img_buffer = image_io.BytesIO()
                        pil_image.save(img_buffer, format='PNG')
                        img_data = base64.b64encode(img_buffer.getvalue()).decode()
                        
                        message_content.append({
                            "type": "text",
                            "text": current_text
                        })
                        message_content.append({
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": img_data
                            }
                        })
                        current_text = ""  # Reset for next part
                        images_added_this_api_call.add(normalized_ref)
                        self.log_queue.put(f"[Claude Translator] Added Image for Figure Ref '{raw_fig_ref}' (norm: {normalized_ref}) for line {global_ln_num}.")
            
            current_text += numbered_src_line_to_translate + "\n"

        current_text += "\nTRANSLATED SENTENCES (numbered list for 'PATENT SENTENCES TO TRANSLATE' only):"
        message_content.append({
            "type": "text", 
            "text": current_text
        })

        try:
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=4000,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": message_content
                }]
            )
            
            raw_text = response.content[0].text if response.content else ""
            if not raw_text: self.log_queue.put(f"[Claude Translator] Warn: Empty response for lines {line_nums_being_translated}.")

            translations = {}
            for line in (raw_text or "").splitlines():
                match = re.match(r"^\s*(\d+)\.\s*(.*)", line.strip())
                if match:
                    num = int(match.group(1))
                    text = match.group(2).strip()
                    if num in line_nums_being_translated:
                        translations[num] = text
            for num in line_nums_being_translated:
                if num not in translations:
                    self.log_queue.put(f"[Claude Translator] Warn: Missing TL line {num}. Placeholder.")
                    translations[num] = f"[TL Missing line {num}]"
            self.log_queue.put(f"[Claude Translator] Multimodal TL for chunk done. Got {len(translations)} segs.")
            return translations
        except Exception as e:
            self.log_queue.put(f"[Claude Translator] Error multimodal TL ('{self.model_name}'): {e}")
            return {n: f"[TL Err line {n} (multimodal): {e}]" for n in line_nums_being_translated}

class ClaudeProofreadingAgent(BaseProofreadingAgent):
    def __init__(self, api_key, log_queue, model_name='claude-3-5-sonnet-20241022'):
        super().__init__(api_key, log_queue, model_name, "Claude")
        if not CLAUDE_AVAILABLE: self.log_queue.put("[Claude Proofreader] ERROR: Anthropic library not available."); return
        if not api_key:
            self.log_queue.put("[Claude Proofreader] ERROR: API Key is missing."); return
        try:
            self.client = anthropic.Anthropic(api_key=api_key)
            self.model = True  # Flag to indicate successful initialization
            self.log_queue.put(f"[Claude Proofreader] Agent initialized with model '{self.model_name}'.")
        except Exception as e: self.log_queue.put(f"[Claude Proofreader] ERROR initializing ('{self.model_name}'): {e}.")

    def proofread_specific_lines_with_context(self, lines_to_proofread_map, full_source_doc_str,
                                             full_original_target_doc_str, source_lang, target_lang,
                                             all_source_segments_original_list, drawings_images_map,
                                             user_custom_instructions=""):
        if not self.model: self.log_queue.put(f"[Claude Proofreader] Model not initialized."); return {n: {"revised_target": lines_to_proofread_map[n]["target_original"], "changes_summary": "[Proofread Err: Model not init]"} for n in lines_to_proofread_map.keys()}
        if not lines_to_proofread_map: self.log_queue.put(f"[Claude Proofreader] No lines for proofreading chunk."); return {}

        line_nums_being_proofread = sorted(list(lines_to_proofread_map.keys()))
        self.log_queue.put(f"[Claude Proofreader] Proofreading {len(line_nums_being_proofread)} lines: {line_nums_being_proofread[:3]}... w/ '{self.model_name}'...")

        # Build system prompt
        system_prompt = f"You are an expert proofreader and editor for {source_lang} to {target_lang} translations, specializing in patent documents."
        if user_custom_instructions: system_prompt += f"\n\nIMPORTANT USER-PROVIDED INSTRUCTIONS:\n{user_custom_instructions}"

        # Build user prompt
        user_prompt_parts = [
            "For each segment below, you are given the 'SOURCE SEGMENT' and the 'EXISTING TRANSLATION'. Review the 'EXISTING TRANSLATION' against the 'SOURCE SEGMENT' based on the following criteria, using the 'FULL SOURCE DOCUMENT CONTEXT' and 'FULL ORIGINAL TARGET DOCUMENT CONTEXT' (provided earlier, if any) for reference. If images for Figures are provided with a segment, use them as crucial context.",
            "Checks to perform:\n1. Accuracy: Faithfully convey source meaning. Correct mistranslations.\n2. Terminology: Ensure correct and consistent use of patent-specific terms.\n3. Tone & Style: Ensure formal, objective, and precise tone appropriate for patents.\n4. Grammar, Spelling, Punctuation: Correct all errors in the {target_lang} translation.\n5. Fluency & Naturalness: Ensure smooth, natural {target_lang} reading.\n6. Completeness: No omissions or additions.\n7. Figure Reference Consistency: Align with any provided images for figure refs.",
            f"Your response MUST be structured as follows:\nFirst, provide a numbered list of ONLY the revised and improved {target_lang} translations for each segment. If an existing translation is already perfect and needs NO changes, return the original EXISTING TRANSLATION for that number.\nSecond, after the complete list of revised translations, add a section explicitly titled '---CHANGES SUMMARY START---'. Under this title, for EACH line number that you modified, provide a brief, clear explanation of the key changes you made (e.g., '27. Corrected spelling; rephrased for flow.'). If NO changes were made to ANY segment in this batch, this section should contain only the text 'No changes made to any segment in this batch.'.\nEnd this section with '---CHANGES SUMMARY END---'.\n",
            f"FULL SOURCE DOCUMENT CONTEXT (for your reference):\n{full_source_doc_str}\n",
            f"FULL ORIGINAL TARGET DOCUMENT CONTEXT (for consistency reference):\n{full_original_target_doc_str}\n",
            "SEGMENTS FOR PROOFREADING (review 'EXISTING TRANSLATION' for each, using preceding images if provided for a figure reference in source):\n"]

        # Build message content with images
        message_content = []
        current_text = "\n".join(user_prompt_parts)

        images_added_this_api_call = set()
        for global_ln_num in line_nums_being_proofread:
            segment_data = lines_to_proofread_map[global_ln_num]
            original_source_text_for_ref_scan = all_source_segments_original_list[global_ln_num - 1]
            fig_refs = re.findall(r"(?:figure|figuur|fig\.?)\s*([\w\d]+(?:[\s\.\-]*[\w\d]+)?)", original_source_text_for_ref_scan, re.IGNORECASE)
            
            if PIL_AVAILABLE and fig_refs and drawings_images_map:
                for raw_fig_ref_tuple in fig_refs:
                    raw_fig_ref = raw_fig_ref_tuple if isinstance(raw_fig_ref_tuple, str) else raw_fig_ref_tuple[0]
                    normalized_ref = normalize_figure_ref(f"fig {raw_fig_ref}")
                    if normalized_ref and normalized_ref in drawings_images_map and normalized_ref not in images_added_this_api_call:
                        pil_image = drawings_images_map[normalized_ref]
                        current_text += f"\n--- Context Image: Figure {raw_fig_ref} (for segment {global_ln_num}) ---\n"
                        
                        # Convert PIL image to base64 for Claude
                        import base64
                        import io as image_io
                        img_buffer = image_io.BytesIO()
                        pil_image.save(img_buffer, format='PNG')
                        img_data = base64.b64encode(img_buffer.getvalue()).decode()
                        
                        message_content.append({
                            "type": "text",
                            "text": current_text
                        })
                        message_content.append({
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": img_data
                            }
                        })
                        current_text = ""  # Reset for next part
                        images_added_this_api_call.add(normalized_ref)
            
            current_text += f"{global_ln_num}. SOURCE SEGMENT: {segment_data['source']}\n"
            current_text += f"{global_ln_num}. EXISTING TRANSLATION: {segment_data['target_original']}\n\n"

        current_text += f"\nREVISED AND PROOFREAD {target_lang.upper()} TARGET SENTENCES (numbered list for the segments above only):"
        message_content.append({
            "type": "text",
            "text": current_text
        })

        try:
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=4000,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": message_content
                }]
            )
            
            raw_text_response = response.content[0].text if response.content else ""
            if not raw_text_response: self.log_queue.put(f"[Claude Proofreader] Warn: Empty response for lines {line_nums_being_proofread}.")

            parsed_results = {}
            translations_text_block, changes_summary_block = raw_text_response, ""
            summary_start_marker, summary_end_marker = "---CHANGES SUMMARY START---", "---CHANGES SUMMARY END---"
            if summary_start_marker in raw_text_response:
                parts = raw_text_response.split(summary_start_marker, 1)
                translations_text_block = parts[0].strip()
                if len(parts) > 1:
                    summary_part = parts[1]
                    changes_summary_block = summary_part.split(summary_end_marker, 1)[0].strip() if summary_end_marker in summary_part else summary_part.strip()

            for line in (translations_text_block or "").splitlines():
                match = re.match(r"^\s*(\d+)\.\s*(.*)", line.strip())
                if match:
                    num = int(match.group(1))
                    text = match.group(2).strip()
                    if num in line_nums_being_proofread:
                        parsed_results.setdefault(num, {})["revised_target"] = text

            parsed_summaries = {}
            if "No changes made to any segment in this batch." not in changes_summary_block and changes_summary_block:
                for line in changes_summary_block.splitlines():
                    match = re.match(r"^\s*(\d+)\.\s*(.*)", line.strip())
                    if match: parsed_summaries[match.group(1)] = match.group(2).strip()

            for num in line_nums_being_proofread:
                if num not in parsed_results: parsed_results[num] = {}
                if "revised_target" not in parsed_results[num]:
                    parsed_results[num]["revised_target"] = lines_to_proofread_map[num]["target_original"]
                    self.log_queue.put(f"[Claude Proofreader] Warn: Missing revised target for line {num}. Using original.")
                parsed_results[num]["changes_summary"] = parsed_summaries.get(str(num))
                parsed_results[num]["original_target"] = lines_to_proofread_map[num]["target_original"]
            self.log_queue.put(f"[Claude Proofreader] Proofreading for chunk done. Processed {len(parsed_results)} segments.")
            return parsed_results
        except Exception as e:
            self.log_queue.put(f"[Claude Proofreader] Error during proofreading ('{self.model_name}'): {e}")
            return {n: {"revised_target": lines_to_proofread_map[n]["target_original"], "changes_summary": f"[Proofread Err line {n}: {e}]"} for n in line_nums_being_proofread}

# --- OpenAI Agent Classes ---
class OpenAITranslationAgent(BaseTranslationAgent):
    def __init__(self, api_key, log_queue, model_name='gpt-4o'):
        super().__init__(api_key, log_queue, model_name, "OpenAI")
        if not OPENAI_AVAILABLE: self.log_queue.put("[OpenAI Translator] ERROR: OpenAI library not available."); return
        if not api_key:
            self.log_queue.put("[OpenAI Translator] ERROR: API Key is missing.")
            return
        try:
            self.client = openai.OpenAI(api_key=api_key)
            self.model = True  # Flag to indicate successful initialization
            self.log_queue.put(f"[OpenAI Translator] Agent with model '{self.model_name}' initialized.")
        except Exception as e: self.log_queue.put(f"[OpenAI Translator] ERROR init ('{self.model_name}'): {e}.")

    def translate_specific_lines_with_drawings_context(self,
                                               lines_map_to_translate,
                                               full_document_context_text_str,
                                               source_lang, target_lang,
                                               all_source_segments_original_list,
                                               drawings_images_map,
                                               user_custom_instructions=""):
        if not self.model: self.log_queue.put(f"[OpenAI Translator] Model ('{self.model_name}') not init."); return {n: f"[Err: Model not init]" for n in lines_map_to_translate.keys()}
        if not lines_map_to_translate: self.log_queue.put(f"[OpenAI Translator] No lines for chunk."); return {}

        line_nums_being_translated = sorted(list(lines_map_to_translate.keys()))
        self.log_queue.put(f"[OpenAI Translator] Translating {len(line_nums_being_translated)} lines: {line_nums_being_translated[:3]}... w/ '{self.model_name}' (drawings if ref)...")

        # Build system prompt
        system_prompt = f"You are an expert {source_lang} to {target_lang} translator specialized in patent documents."
        if user_custom_instructions:
            system_prompt += f"\n\nIMPORTANT USER-PROVIDED INSTRUCTIONS:\n{user_custom_instructions}"

        # Build user prompt
        user_prompt_parts = []
        user_prompt_parts.extend([
            "The full patent text for overall context is in 'FULL PATENT CONTEXT' below. Translate ONLY sentences from 'PATENT SENTENCES TO TRANSLATE' later. These are listed with their original line numbers from the full document.",
            "If a sentence refers to a Figure (e.g., 'Figure 1A', 'Figuur X'), relevant images may be provided just before that sentence. Use these images as crucial context for accurately translating references to parts, features, or relationships shown in those figures.",
            "Present your output ONLY as a numbered list of the translations for the requested sentences, using their original numbering. Maintain accuracy and appropriate patent terminology.\n",
            f"FULL PATENT CONTEXT:\n{full_document_context_text_str}\n",
            "PATENT SENTENCES TO TRANSLATE (translate only these, using preceding images if provided for a figure reference):\n"])

        # Build message content with images
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        user_content = []
        current_text = "\n".join(user_prompt_parts)
        
        images_added_this_api_call = set()
        for global_ln_num in line_nums_being_translated:
            original_line_text_for_ref_scan = all_source_segments_original_list[global_ln_num - 1]
            numbered_src_line_to_translate = lines_map_to_translate[global_ln_num]
            found_fig_refs_in_line = re.findall(r"(?:figure|figuur|fig\.?)\s*([\w\d]+(?:[\s\.\-]*[\w\d]+)?)", original_line_text_for_ref_scan, re.IGNORECASE)
            
            if PIL_AVAILABLE and found_fig_refs_in_line and drawings_images_map:
                for raw_fig_ref_tuple in found_fig_refs_in_line:
                    raw_fig_ref = raw_fig_ref_tuple if isinstance(raw_fig_ref_tuple, str) else raw_fig_ref_tuple[0]
                    normalized_ref = normalize_figure_ref(f"fig {raw_fig_ref}")
                    if normalized_ref and normalized_ref in drawings_images_map and normalized_ref not in images_added_this_api_call:
                        pil_image = drawings_images_map[normalized_ref]
                        current_text += f"\n--- Context Image: Figure {raw_fig_ref} (Referenced in or near the following text) ---\n"
                        
                        # Convert PIL image to base64 for OpenAI
                        import base64
                        import io as image_io
                        img_buffer = image_io.BytesIO()
                        pil_image.save(img_buffer, format='PNG')
                        img_data = base64.b64encode(img_buffer.getvalue()).decode()
                        
                        user_content.append({
                            "type": "text",
                            "text": current_text
                        })
                        user_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_data}"
                            }
                        })
                        current_text = ""  # Reset for next part
                        images_added_this_api_call.add(normalized_ref)
                        self.log_queue.put(f"[OpenAI Translator] Added Image for Figure Ref '{raw_fig_ref}' (norm: {normalized_ref}) for line {global_ln_num}.")
            
            current_text += numbered_src_line_to_translate + "\n"

        current_text += "\nTRANSLATED SENTENCES (numbered list for 'PATENT SENTENCES TO TRANSLATE' only):"
        user_content.append({
            "type": "text",
            "text": current_text
        })
        
        messages.append({
            "role": "user",
            "content": user_content
        })

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=4000,
                temperature=0.3
            )
            
            raw_text = response.choices[0].message.content if response.choices else ""
            if not raw_text: self.log_queue.put(f"[OpenAI Translator] Warn: Empty response for lines {line_nums_being_translated}.")

            translations = {}
            for line in (raw_text or "").splitlines():
                match = re.match(r"^\s*(\d+)\.\s*(.*)", line.strip())
                if match:
                    num = int(match.group(1))
                    text = match.group(2).strip()
                    if num in line_nums_being_translated:
                        translations[num] = text
            for num in line_nums_being_translated:
                if num not in translations:
                    self.log_queue.put(f"[OpenAI Translator] Warn: Missing TL line {num}. Placeholder.")
                    translations[num] = f"[TL Missing line {num}]"
            self.log_queue.put(f"[OpenAI Translator] Multimodal TL for chunk done. Got {len(translations)} segs.")
            return translations
        except Exception as e:
            self.log_queue.put(f"[OpenAI Translator] Error multimodal TL ('{self.model_name}'): {e}")
            return {n: f"[TL Err line {n} (multimodal): {e}]" for n in line_nums_being_translated}

class OpenAIProofreadingAgent(BaseProofreadingAgent):
    def __init__(self, api_key, log_queue, model_name='gpt-4o'):
        super().__init__(api_key, log_queue, model_name, "OpenAI")
        if not OPENAI_AVAILABLE: self.log_queue.put("[OpenAI Proofreader] ERROR: OpenAI library not available."); return
        if not api_key:
            self.log_queue.put("[OpenAI Proofreader] ERROR: API Key is missing."); return
        try:
            self.client = openai.OpenAI(api_key=api_key)
            self.model = True  # Flag to indicate successful initialization
            self.log_queue.put(f"[OpenAI Proofreader] Agent initialized with model '{self.model_name}'.")
        except Exception as e: self.log_queue.put(f"[OpenAI Proofreader] ERROR initializing ('{self.model_name}'): {e}.")

    def proofread_specific_lines_with_context(self, lines_to_proofread_map, full_source_doc_str,
                                             full_original_target_doc_str, source_lang, target_lang,
                                             all_source_segments_original_list, drawings_images_map,
                                             user_custom_instructions=""):
        if not self.model: self.log_queue.put(f"[OpenAI Proofreader] Model not initialized."); return {n: {"revised_target": lines_to_proofread_map[n]["target_original"], "changes_summary": "[Proofread Err: Model not init]"} for n in lines_to_proofread_map.keys()}
        if not lines_to_proofread_map: self.log_queue.put(f"[OpenAI Proofreader] No lines for proofreading chunk."); return {}

        line_nums_being_proofread = sorted(list(lines_to_proofread_map.keys()))
        self.log_queue.put(f"[OpenAI Proofreader] Proofreading {len(line_nums_being_proofread)} lines: {line_nums_being_proofread[:3]}... w/ '{self.model_name}'...")

        # Build system prompt
        system_prompt = f"You are an expert proofreader and editor for {source_lang} to {target_lang} translations, specializing in patent documents."
        if user_custom_instructions: system_prompt += f"\n\nIMPORTANT USER-PROVIDED INSTRUCTIONS:\n{user_custom_instructions}"

        # Build user prompt
        user_prompt_parts = [
            "For each segment below, you are given the 'SOURCE SEGMENT' and the 'EXISTING TRANSLATION'. Review the 'EXISTING TRANSLATION' against the 'SOURCE SEGMENT' based on the following criteria, using the 'FULL SOURCE DOCUMENT CONTEXT' and 'FULL ORIGINAL TARGET DOCUMENT CONTEXT' (provided earlier, if any) for reference. If images for Figures are provided with a segment, use them as crucial context.",
            "Checks to perform:\n1. Accuracy: Faithfully convey source meaning. Correct mistranslations.\n2. Terminology: Ensure correct and consistent use of patent-specific terms.\n3. Tone & Style: Ensure formal, objective, and precise tone appropriate for patents.\n4. Grammar, Spelling, Punctuation: Correct all errors in the {target_lang} translation.\n5. Fluency & Naturalness: Ensure smooth, natural {target_lang} reading.\n6. Completeness: No omissions or additions.\n7. Figure Reference Consistency: Align with any provided images for figure refs.",
            f"Your response MUST be structured as follows:\nFirst, provide a numbered list of ONLY the revised and improved {target_lang} translations for each segment. If an existing translation is already perfect and needs NO changes, return the original EXISTING TRANSLATION for that number.\nSecond, after the complete list of revised translations, add a section explicitly titled '---CHANGES SUMMARY START---'. Under this title, for EACH line number that you modified, provide a brief, clear explanation of the key changes you made (e.g., '27. Corrected spelling; rephrased for flow.'). If NO changes were made to ANY segment in this batch, this section should contain only the text 'No changes made to any segment in this batch.'.\nEnd this section with '---CHANGES SUMMARY END---'.\n",
            f"FULL SOURCE DOCUMENT CONTEXT (for your reference):\n{full_source_doc_str}\n",
            f"FULL ORIGINAL TARGET DOCUMENT CONTEXT (for consistency reference):\n{full_original_target_doc_str}\n",
            "SEGMENTS FOR PROOFREADING (review 'EXISTING TRANSLATION' for each, using preceding images if provided for a figure reference in source):\n"]

        # Build message content with images
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        user_content = []
        current_text = "\n".join(user_prompt_parts)

        images_added_this_api_call = set()
        for global_ln_num in line_nums_being_proofread:
            segment_data = lines_to_proofread_map[global_ln_num]
            original_source_text_for_ref_scan = all_source_segments_original_list[global_ln_num - 1]
            fig_refs = re.findall(r"(?:figure|figuur|fig\.?)\s*([\w\d]+(?:[\s\.\-]*[\w\d]+)?)", original_source_text_for_ref_scan, re.IGNORECASE)
            
            if PIL_AVAILABLE and fig_refs and drawings_images_map:
                for raw_fig_ref_tuple in fig_refs:
                    raw_fig_ref = raw_fig_ref_tuple if isinstance(raw_fig_ref_tuple, str) else raw_fig_ref_tuple[0]
                    normalized_ref = normalize_figure_ref(f"fig {raw_fig_ref}")
                    if normalized_ref and normalized_ref in drawings_images_map and normalized_ref not in images_added_this_api_call:
                        pil_image = drawings_images_map[normalized_ref]
                        current_text += f"\n--- Context Image: Figure {raw_fig_ref} (for segment {global_ln_num}) ---\n"
                        
                        # Convert PIL image to base64 for OpenAI
                        import base64
                        import io as image_io
                        img_buffer = image_io.BytesIO()
                        pil_image.save(img_buffer, format='PNG')
                        img_data = base64.b64encode(img_buffer.getvalue()).decode()
                        
                        user_content.append({
                            "type": "text",
                            "text": current_text
                        })
                        user_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_data}"
                            }
                        })
                        current_text = ""  # Reset for next part
                        images_added_this_api_call.add(normalized_ref)
            
            current_text += f"{global_ln_num}. SOURCE SEGMENT: {segment_data['source']}\n"
            current_text += f"{global_ln_num}. EXISTING TRANSLATION: {segment_data['target_original']}\n\n"

        current_text += f"\nREVISED AND PROOFREAD {target_lang.upper()} TARGET SENTENCES (numbered list for the segments above only):"
        user_content.append({
            "type": "text",
            "text": current_text
        })
        
        messages.append({
            "role": "user",
            "content": user_content
        })

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=4000,
                temperature=0.3
            )
            
            raw_text_response = response.choices[0].message.content if response.choices else ""
            if not raw_text_response: self.log_queue.put(f"[OpenAI Proofreader] Warn: Empty response for lines {line_nums_being_proofread}.")

            parsed_results = {}
            translations_text_block, changes_summary_block = raw_text_response, ""
            summary_start_marker, summary_end_marker = "---CHANGES SUMMARY START---", "---CHANGES SUMMARY END---"
            if summary_start_marker in raw_text_response:
                parts = raw_text_response.split(summary_start_marker, 1)
                translations_text_block = parts[0].strip()
                if len(parts) > 1:
                    summary_part = parts[1]
                    changes_summary_block = summary_part.split(summary_end_marker, 1)[0].strip() if summary_end_marker in summary_part else summary_part.strip()

            for line in (translations_text_block or "").splitlines():
                match = re.match(r"^\s*(\d+)\.\s*(.*)", line.strip())
                if match:
                    num = int(match.group(1))
                    text = match.group(2).strip()
                    if num in line_nums_being_proofread:
                        parsed_results.setdefault(num, {})["revised_target"] = text

            parsed_summaries = {}
            if "No changes made to any segment in this batch." not in changes_summary_block and changes_summary_block:
                for line in changes_summary_block.splitlines():
                    match = re.match(r"^\s*(\d+)\.\s*(.*)", line.strip())
                    if match: parsed_summaries[match.group(1)] = match.group(2).strip()

            for num in line_nums_being_proofread:
                if num not in parsed_results: parsed_results[num] = {}
                if "revised_target" not in parsed_results[num]:
                    parsed_results[num]["revised_target"] = lines_to_proofread_map[num]["target_original"]
                    self.log_queue.put(f"[OpenAI Proofreader] Warn: Missing revised target for line {num}. Using original.")
                parsed_results[num]["changes_summary"] = parsed_summaries.get(str(num))
                parsed_results[num]["original_target"] = lines_to_proofread_map[num]["target_original"]
            self.log_queue.put(f"[OpenAI Proofreader] Proofreading for chunk done. Processed {len(parsed_results)} segments.")
            return parsed_results
        except Exception as e:
            self.log_queue.put(f"[OpenAI Proofreader] Error during proofreading ('{self.model_name}'): {e}")
            return {n: {"revised_target": lines_to_proofread_map[n]["target_original"], "changes_summary": f"[Proofread Err line {n}: {e}]"} for n in line_nums_being_proofread}

# --- Agent Factory ---
def create_translation_agent(provider, api_key, log_queue, model_name):
    """Factory function to create appropriate translation agent based on provider"""
    if provider.lower() == "gemini":
        return GeminiTranslationAgent(api_key, log_queue, model_name)
    elif provider.lower() == "claude":
        return ClaudeTranslationAgent(api_key, log_queue, model_name)
    elif provider.lower() == "openai":
        return OpenAITranslationAgent(api_key, log_queue, model_name)
    else:
        log_queue.put(f"[Factory] Unknown provider: {provider}")
        return None

def create_proofreading_agent(provider, api_key, log_queue, model_name):
    """Factory function to create appropriate proofreading agent based on provider"""
    if provider.lower() == "gemini":
        return GeminiProofreadingAgent(api_key, log_queue, model_name)
    elif provider.lower() == "claude":
        return ClaudeProofreadingAgent(api_key, log_queue, model_name)
    elif provider.lower() == "openai":
        return OpenAIProofreadingAgent(api_key, log_queue, model_name)
    else:
        log_queue.put(f"[Factory] Unknown provider: {provider}")
        return None

def get_available_models(provider, api_key, log_queue):
    """Get available models for the specified provider"""
    if provider.lower() == "gemini":
        if not GOOGLE_AI_AVAILABLE or not api_key:
            return GEMINI_MODELS  # Return static list if can't query
        try:
            genai.configure(api_key=api_key)
            dynamic_models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    model_name = m.name.split('/')[-1] if '/' in m.name else m.name
                    dynamic_models.append(model_name)
            return dynamic_models if dynamic_models else GEMINI_MODELS
        except Exception as e:
            log_queue.put(f"[Models] Error fetching Gemini models: {e}")
            return GEMINI_MODELS
    elif provider.lower() == "claude":
        return CLAUDE_MODELS  # Claude doesn't have a public API to list models
    elif provider.lower() == "openai":
        return OPENAI_MODELS  # OpenAI doesn't require listing models via API
    else:
        return []

class OutputGenerationAgent:
    def process(self, source_data_list_for_output, target_data_list_for_output, output_path, log_queue, mode="Translate", comments_list_for_output=None):
        log_queue.put(f"[Outputter] Generating output file: {output_path} for mode: {mode}")
        
        if len(source_data_list_for_output) != len(target_data_list_for_output):
            log_queue.put(f"[Outputter] FATAL ERROR: Mismatch between number of source items ({len(source_data_list_for_output)}) and target items ({len(target_data_list_for_output)}).")
            return False
        if mode == "Proofread" and comments_list_for_output is not None and len(comments_list_for_output) != len(source_data_list_for_output):
            log_queue.put(f"[Outputter] FATAL ERROR: Mismatch between number of source items ({len(source_data_list_for_output)}) and comments ({len(comments_list_for_output)}) in Proofread mode.")
            return False

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for i in range(len(source_data_list_for_output)):
                    source_text = source_data_list_for_output[i]
                    target_text = target_data_list_for_output[i]
                    
                    f.write(f"{source_text}\t{target_text if target_text is not None else '[ERR - Target Missing]'}")
                    
                    if mode == "Proofread" and comments_list_for_output and i < len(comments_list_for_output) and comments_list_for_output[i] is not None:
                        # Replace newline characters in the comment with a space to keep the output on a single line
                        comment_to_write = comments_list_for_output[i].replace("\n", " ")
                        f.write(f"\t{comment_to_write}")
                    f.write("\n")
            log_queue.put(f"[Outputter] Output file saved to: {output_path}")
            return True
        except Exception as e: 
            log_queue.put(f"[Outputter] Error writing output file {output_path}: {e}")
            return False

class TranslationApp:
    def __init__(self, root):
        self.root = root
        root.title("Supervertaler (v9.0) - Multi-LLM AI-powered Translator & Proofreader") 
        root.geometry("750x920") 

        self.log_queue = queue.Queue()
        self.api_keys = API_KEYS
        self.tm_agent = TMAgent(self.log_queue)
        self.drawings_images_map = {} 

        # Create the log widget instance early to make it available for logging during init
        self.log_text = scrolledtext.ScrolledText(root, width=80, height=10, wrap=tk.WORD, state="disabled")

        # --- UNIFIED INFO TEXT ---
        self.info_text_content_unified = (
            "Supervertaler is an AI-powered document translation & proofreading tool that can operate in two modes: TRANSLATE or PROOFREAD. It leverages multiple context sources for enhanced accuracy:\n\n"
            "COMMON CONTEXT SOURCES (for both modes):\n"
            "• Full Document Content: The AI considers the entire document for better contextual understanding.\n"
            "• Images: If a 'Drawings Image Folder' is provided, images (e.g., 'Fig 1A.png') are shown to the AI when the text references them, aiding in visual context.\n\n"
            "Other features:\n"
            "• Multiple AI Providers: Choose between Claude (Anthropic), Gemini (Google), and ChatGPT (OpenAI) models\n"
            "• Text field for custom instructions to be added to system prompt on-the-fly\n"
            "• System prompt (partially) editable in python code\n" 
            "• Chunking: System breaks large documents into manageable chunks for the AI.\n\n"
            "--- MODE-SPECIFIC DETAILS ---\n\n"
            "TRANSLATE MODE:\n"
            "• Function: Translates source text to the target language.\n"
            "• TM Usage: Uses a Translation Memory (.txt/.tmx) for exact matches before AI processing.\n"
            "• Input Format: Text file with one source text per line.\n"
            "• Output Format: 'source_text<tab>translated_text'.\n\n"
            "PROOFREAD MODE:\n"
            "• Function: Reviews and revises existing target text against the source text.\n"
            "• TM Usage: TM is bypassed in this mode; all segments are sent to the AI for review.\n"
            "• Input Format: Text file with 'source_text<tab>EXISTING_target_text<tab>[optional_original_comment]'. (3rd column is optional).\n"
            "• Output Format: 'source_text<tab>REVISED_target_text<tab>[comments_including_AI_changes_and_original]'.\n"
        )
        
        # Check if any libraries are available
        libraries_available = GOOGLE_AI_AVAILABLE or CLAUDE_AVAILABLE or OPENAI_AVAILABLE
        if not libraries_available: 
            error_msg = "Critical Error: No AI libraries available!\n"
            if not GOOGLE_AI_AVAILABLE: error_msg += f"Google AI: {GOOGLE_AI_IMPORT_ERROR_MESSAGE}\n"
            if not CLAUDE_AVAILABLE: error_msg += f"Claude: {CLAUDE_IMPORT_ERROR_MESSAGE}\n"
            if not OPENAI_AVAILABLE: error_msg += f"OpenAI: {OPENAI_IMPORT_ERROR_MESSAGE}\n"
            messagebox.showerror("Critical Error", error_msg + "App will close.")
            root.destroy()
            return

        # Check API keys
        if not self.api_keys["google"] and not self.api_keys["claude"] and not self.api_keys["openai"]:
            messagebox.showwarning("API Keys Missing", "No API keys found in api_keys.txt. Please configure at least one API key.")
            self.update_log("CRITICAL: No API keys configured. Check api_keys.txt file.")

        current_row = 0
        self.info_label = tk.Label(root,text=self.info_text_content_unified,wraplength=720,justify=tk.LEFT,anchor="w",relief=tk.SOLID,borderwidth=1,padx=5, pady=5)
        self.info_label.grid(row=current_row, column=0, columnspan=3, padx=5, pady=(5,10), sticky="ew"); current_row += 1
        
        mode_frame = tk.Frame(root)
        mode_frame.grid(row=current_row, column=0, columnspan=3, pady=2, sticky="w", padx=5)
        tk.Label(mode_frame, text="Operation Mode:").pack(side=tk.LEFT, padx=(0,5))
        self.operation_mode_var = tk.StringVar(value="Translate")
        tk.Radiobutton(mode_frame, text="Translate", variable=self.operation_mode_var, value="Translate", command=self.update_ui_for_mode).pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="Proofread", variable=self.operation_mode_var, value="Proofread", command=self.update_ui_for_mode).pack(side=tk.LEFT, padx=(10,0))
        current_row += 1

        self.input_file_var = tk.StringVar(); self.output_file_var = tk.StringVar()
        self.tm_file_var = tk.StringVar(); self.drawings_folder_var = tk.StringVar() 

        self.input_file_label = tk.Label(root, text="Input Text File (one source per line):") 
        self.input_file_label.grid(row=current_row, column=0, padx=5, pady=2, sticky="w")
        tk.Entry(root, textvariable=self.input_file_var, width=60, state="readonly").grid(row=current_row, column=1, padx=5, pady=2, sticky="ew")
        tk.Button(root, text="Browse...", command=self.browse_input_file).grid(row=current_row, column=2, padx=5, pady=2); current_row += 1
        
        tk.Label(root, text="Output File:").grid(row=current_row, column=0, padx=5, pady=2, sticky="w")
        tk.Entry(root, textvariable=self.output_file_var, width=60, state="readonly").grid(row=current_row, column=1, padx=5, pady=2, sticky="ew")
        tk.Button(root, text="Browse...", command=self.browse_output_file).grid(row=current_row, column=2, padx=5, pady=2); current_row += 1

        self.tm_file_label = tk.Label(root, text="TM File (txt/tmx):") 
        self.tm_file_label.grid(row=current_row, column=0, padx=5, pady=2, sticky="w")
        tk.Entry(root, textvariable=self.tm_file_var, width=60, state="readonly").grid(row=current_row, column=1, padx=5, pady=2, sticky="ew")
        tk.Button(root, text="Browse TM...", command=self.browse_tm_file).grid(row=current_row, column=2, padx=5, pady=2); current_row += 1

        self.drawings_folder_label = tk.Label(root, text="Drawings Image Folder:")
        self.drawings_folder_label.grid(row=current_row, column=0, padx=5, pady=2, sticky="w")
        tk.Entry(root, textvariable=self.drawings_folder_var, width=60, state="readonly").grid(row=current_row, column=1, padx=5, pady=2, sticky="ew")
        tk.Button(root, text="Browse...", command=self.browse_drawings_folder).grid(row=current_row, column=2, padx=5, pady=2); current_row += 1
        
        self.source_lang_var = tk.StringVar(value="Dutch")
        self.target_lang_var = tk.StringVar(value="English")
        self.chunk_size_var = tk.StringVar(value="100")

        # AI Provider and Model Selection
        provider_frame = tk.Frame(root)
        provider_frame.grid(row=current_row, column=0, columnspan=3, pady=2, sticky="ew", padx=5)
        tk.Label(provider_frame, text="AI Provider:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        
        self.provider_var = tk.StringVar(value="Claude")  # Claude as default
        provider_combo = ttk.Combobox(provider_frame, textvariable=self.provider_var, width=15, state="readonly")
        available_providers = []
        if CLAUDE_AVAILABLE and self.api_keys["claude"]: available_providers.append("Claude")
        if GOOGLE_AI_AVAILABLE and self.api_keys["google"]: available_providers.append("Gemini")
        if OPENAI_AVAILABLE and self.api_keys["openai"]: available_providers.append("OpenAI")
        
        if not available_providers:
            # Add all providers but with warnings
            if CLAUDE_AVAILABLE: available_providers.append("Claude")
            if GOOGLE_AI_AVAILABLE: available_providers.append("Gemini")
            if OPENAI_AVAILABLE: available_providers.append("OpenAI")
        
        provider_combo['values'] = available_providers
        if available_providers and self.provider_var.get() not in available_providers:
            self.provider_var.set(available_providers[0])
        provider_combo.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        provider_combo.bind('<<ComboboxSelected>>', self.on_provider_changed)
        
        tk.Label(provider_frame, text="Model:").grid(row=0, column=2, padx=(20,5), pady=2, sticky="w")
        self.model_var = tk.StringVar()
        self.model_combo = ttk.Combobox(provider_frame, textvariable=self.model_var, width=30, state="readonly")
        self.model_combo.grid(row=0, column=3, padx=5, pady=2, sticky="w")
        
        # Initialize models for default provider
        self.update_available_models()
        current_row += 1

        setting_fields_data = [
            ("Source Language:", self.source_lang_var, 30), ("Target Language:", self.target_lang_var, 30),
            ("Chunk Size (lines):", self.chunk_size_var, 10)
        ]
        for text, var, width in setting_fields_data:
            tk.Label(root, text=text).grid(row=current_row, column=0, padx=5, pady=2, sticky="w")
            tk.Entry(root, textvariable=var, width=width).grid(row=current_row, column=1, padx=5, pady=2, sticky="w"); current_row += 1

        tk.Label(root, text="Custom Instructions for AI (optional):").grid(row=current_row, column=0, padx=5, pady=(5,0), sticky="nw")
        self.custom_instructions_text = tk.Text(root, height=4, width=60, wrap=tk.WORD, borderwidth=1, relief="solid")
        self.custom_instructions_text.grid(row=current_row, column=1, columnspan=2, padx=5, pady=2, sticky="ew"); current_row += 1

        buttons_frame = tk.Frame(root); buttons_frame.grid(row=current_row, column=0, columnspan=3, pady=5); current_row += 1
        self.process_button = tk.Button(buttons_frame, text="Start Process", command=self.start_processing_thread, width=15, height=2); self.process_button.pack(side=tk.LEFT, padx=10) 
        self.list_models_button = tk.Button(buttons_frame, text="List Models", command=self.list_available_models, width=15); self.list_models_button.pack(side=tk.LEFT, padx=10) 
        self.refresh_models_button = tk.Button(buttons_frame, text="Refresh Models", command=self.update_available_models, width=15); self.refresh_models_button.pack(side=tk.LEFT, padx=10)
        
        tk.Label(root, text="Log:").grid(row=current_row, column=0, padx=5, pady=2, sticky="nw"); current_row += 1
        self.log_text = scrolledtext.ScrolledText(root, width=80, height=10, wrap=tk.WORD, state="disabled"); self.log_text.grid(row=current_row, column=0, columnspan=3, padx=5, pady=2, sticky="nsew")
        root.grid_columnconfigure(1, weight=1); root.grid_rowconfigure(current_row, weight=1)
        
        self.check_log_queue()
        if not PIL_AVAILABLE: self.update_log("WARN: Drawings Folder feature limited (Pillow library not found).")
        self.update_log("Select operation mode. Ensure input file format matches selected mode.")
        
        # Final library checks
        if not GOOGLE_AI_AVAILABLE: self.update_log(f"WARN: Google AI unavailable: {GOOGLE_AI_IMPORT_ERROR_MESSAGE}")
        if not CLAUDE_AVAILABLE: self.update_log(f"WARN: Claude unavailable: {CLAUDE_IMPORT_ERROR_MESSAGE}")
        if not OPENAI_AVAILABLE: self.update_log(f"WARN: OpenAI unavailable: {OPENAI_IMPORT_ERROR_MESSAGE}")
        
        # Disable buttons if no working providers
        working_providers = self.get_working_providers()
        if not working_providers:
            self.update_log("CRITICAL: No working AI providers available!")
            self.process_button.config(state="disabled")
            self.list_models_button.config(state="disabled")
            self.refresh_models_button.config(state="disabled")

    def get_working_providers(self):
        """Get list of providers that have both library and API key available"""
        working = []
        if CLAUDE_AVAILABLE and self.api_keys["claude"]:
            working.append("Claude")
        if GOOGLE_AI_AVAILABLE and self.api_keys["google"]:
            working.append("Gemini")
        if OPENAI_AVAILABLE and self.api_keys["openai"]:
            working.append("OpenAI")
        return working

    def on_provider_changed(self, event=None):
        """Called when user changes AI provider"""
        self.update_available_models()

    def update_available_models(self):
        """Update the model dropdown based on selected provider"""
        provider = self.provider_var.get()
        if not provider:
            return
            
        # Get appropriate API key
        api_key = ""
        if provider == "Claude":
            api_key = self.api_keys["claude"]
        elif provider == "Gemini":
            api_key = self.api_keys["google"]
        elif provider == "OpenAI":
            api_key = self.api_keys["openai"]
        
        # Get available models
        models = get_available_models(provider, api_key, self.log_queue)
        self.model_combo['values'] = models
        
        # Set default model
        if models:
            if provider == "Claude":
                default_model = "claude-3-5-sonnet-20241022"
            elif provider == "OpenAI":
                default_model = "gpt-4o"
            else:  # Gemini
                default_model = "gemini-2.5-pro-preview-05-06"
            
            if default_model in models:
                self.model_var.set(default_model)
            else:
                self.model_var.set(models[0])
        
        self.update_log(f"Updated models for {provider}: {len(models)} available")

    def update_ui_for_mode(self):
        mode = self.operation_mode_var.get()
        if mode == "Translate":
            self.input_file_label.config(text="Input Text File (one source per line):")
            self.tm_file_label.config(text="TM File (txt/tmx):") 
            self.process_button.config(text="Translate")
        elif mode == "Proofread":
            self.input_file_label.config(text="Input Text File (source<tab>TARGET<tab>[comment]):")
            self.tm_file_label.config(text="TM File (N/A for Proofread):") 
            self.process_button.config(text="Proofread")

    def browse_drawings_folder(self):
        if not PIL_AVAILABLE: messagebox.showwarning("Feature Disabled", "Pillow (PIL) library not found."); return
        folderpath = filedialog.askdirectory(title="Select Folder Containing Drawing Images")
        if folderpath: self.drawings_folder_var.set(folderpath); self.update_log(f"Drawings image folder: {folderpath}")
    
    def browse_tm_file(self):
        filepath = filedialog.askopenfilename(title="Select TM File", filetypes=(("TMX", "*.tmx"),("TXT", "*.txt"),("All", "*.*")))
        if filepath: self.tm_file_var.set(filepath); self.update_log(f"TM file: {filepath}")
    
    def browse_input_file(self):
        filepath = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if filepath: 
            self.input_file_var.set(filepath)
            if not self.output_file_var.get(): 
                base, ext = os.path.splitext(filepath)
                suffix = "_proofread" if self.operation_mode_var.get() == "Proofread" else "_translated"
                self.output_file_var.set(f"{base}{suffix}{ext}")

    def browse_output_file(self):
        filepath = filedialog.asksaveasfilename(title="Save Output File As", filetypes=(("Text files", "*.txt"),("All files", "*.*")), defaultextension=".txt")
        if filepath: self.output_file_var.set(filepath)
    
    def update_log(self, msg): 
        self.log_text.config(state="normal"); self.log_text.insert(tk.END, str(msg) + "\n"); self.log_text.see(tk.END); self.log_text.config(state="disabled"); self.root.update_idletasks()
    
    def check_log_queue(self): 
        while not self.log_queue.empty(): self.update_log(self.log_queue.get_nowait())
        self.root.after(100, self.check_log_queue)
    
    def list_available_models(self):
        provider = self.provider_var.get()
        if not provider:
            messagebox.showerror("Error", "No provider selected")
            return
            
        self.update_log(f"\n--- Listing Models for {provider} ---")
        
        # Get appropriate API key
        api_key = ""
        if provider == "Claude":
            api_key = self.api_keys["claude"]
        elif provider == "Gemini":
            api_key = self.api_keys["google"]
        elif provider == "OpenAI":
            api_key = self.api_keys["openai"]
        
        if not api_key:
            self.update_log(f"API Key missing for {provider}")
            return
            
        if provider == "Gemini" and GOOGLE_AI_AVAILABLE:
            try:
                genai.configure(api_key=api_key)
                self.update_log("Fetching Gemini models...")
                models_info = []
                for m in genai.list_models():
                    model_desc_text = m.description if hasattr(m, 'description') and m.description else "N/A"
                    models_info.append(f"Model: {m.name}\n  Display: {m.display_name}\n  Desc: {model_desc_text[:100]}...\n  Methods: {m.supported_generation_methods}\n  {'✅ genContent' if 'generateContent' in m.supported_generation_methods else '❌ No genContent'}")
                if not models_info: self.update_log("No Gemini models found.")
                else: self.update_log("\n---\n".join(models_info)); self.update_log(f"\nFound {len(models_info)} Gemini models. For drawings, use multimodal.")
            except Exception as e: self.update_log(f"Error listing Gemini models: {e}"); messagebox.showerror("List Models Error", f"{e}")
        elif provider == "Claude":
            self.update_log("Available Claude models:")
            for i, model in enumerate(CLAUDE_MODELS, 1):
                self.update_log(f"{i}. {model}")
            self.update_log(f"\nFound {len(CLAUDE_MODELS)} Claude models. All support multimodal capabilities.")
        elif provider == "OpenAI":
            self.update_log("Available OpenAI models:")
            for i, model in enumerate(OPENAI_MODELS, 1):
                self.update_log(f"{i}. {model}")
            self.update_log(f"\nFound {len(OPENAI_MODELS)} OpenAI models. Models with 'gpt-4' prefix support multimodal capabilities.")
        else:
            self.update_log(f"Cannot list models for {provider} - library not available or API key missing")
            
        self.update_log("--- Done Listing ---\n")
    
    def load_drawing_images_from_folder(self, folder_path):
        if not PIL_AVAILABLE or not folder_path: self.log_queue.put("[Drawings] Pillow lib not avail or no folder path."); return {}
        loaded_images_map = {}; self.log_queue.put(f"[Drawings] Loading images from: {folder_path}")
        valid_extensions = ('.png', '.jpg', '.jpeg', '.webp'); count = 0
        try:
            for fname in os.listdir(folder_path):
                if fname.lower().endswith(valid_extensions):
                    try:
                        base_name = os.path.splitext(fname)[0]; normalized_ref = normalize_figure_ref(base_name)
                        if normalized_ref: img = Image.open(os.path.join(folder_path, fname)); loaded_images_map[normalized_ref] = img; self.log_queue.put(f"[Drawings] Loaded '{fname}' as Fig Ref '{normalized_ref}'."); count += 1
                        else: self.log_queue.put(f"[Drawings] Could not normalize: {fname}")
                    except Exception as e_img: self.log_queue.put(f"[Drawings] Err loading img {fname}: {e_img}")
            self.log_queue.put(f"[Drawings] Loaded {count} images."); 
        except Exception as e_list_dir: self.log_queue.put(f"[Drawings] Error listing dir {folder_path}: {e_list_dir}"); messagebox.showerror("Drawings Folder Error", f"Could not read drawings folder: {e_list_dir}")
        return loaded_images_map

    def start_processing_thread(self):
        provider = self.provider_var.get()
        model_name = self.model_var.get()
        mode = self.operation_mode_var.get()
        
        # Validate provider and model
        if not provider or not model_name:
            messagebox.showerror("Error", "Please select both AI provider and model")
            return
            
        # Check if provider is working
        working_providers = self.get_working_providers()
        if provider not in working_providers:
            api_key_type = "OpenAI" if provider == "OpenAI" else "Claude" if provider == "Claude" else "Google"
            messagebox.showerror("Error", f"{provider} not available. Check if {api_key_type} API key is configured in api_keys.txt and library is installed.")
            return
        
        input_f = self.input_file_var.get(); output_f = self.output_file_var.get()
        tm_f = self.tm_file_var.get(); drawings_folder = self.drawings_folder_var.get()
        src_l = self.source_lang_var.get(); tgt_l = self.target_lang_var.get()
        custom_instr = self.custom_instructions_text.get("1.0", tk.END).strip()
        
        try: chunk_s = int(self.chunk_size_var.get()); assert chunk_s > 0
        except: messagebox.showerror("Error", "Invalid Chunk Size."); return
        
        if not input_f or not output_f: messagebox.showerror("File Error", "Select input & output files."); return
        if drawings_folder and not PIL_AVAILABLE: messagebox.showerror("Image Error", "Pillow (PIL) library needed for drawings folder feature."); return

        self.process_button.config(state="disabled", text=f"{mode}ing...")
        self.list_models_button.config(state="disabled")
        self.refresh_models_button.config(state="disabled")
        self.update_log(f"--- Starting {mode} Process with {provider} ({model_name}) ---")
        
        if mode == "Translate" and tm_f: self.tm_agent.load_tm(tm_f, src_l, tgt_l)
        self.drawings_images_map = {} 
        if drawings_folder and PIL_AVAILABLE: self.drawings_images_map = self.load_drawing_images_from_folder(drawings_folder)
        
        thread = threading.Thread(target=self.run_pipeline,
                                  args=(mode, input_f, output_f, src_l, tgt_l, provider, model_name, chunk_s, 
                                        self.drawings_images_map, custom_instr)) 
        thread.daemon = True; thread.start()

    def run_pipeline(self, mode, input_f, output_f, src_lang, tgt_lang, provider, model_name, chunk_s, drawings_map, user_custom_instructions):
        ingestor = BilingualFileIngestionAgent(); output_gen = OutputGenerationAgent()
        
        all_original_data = ingestor.process(input_f, self.log_queue, mode=mode) 
        if not all_original_data: self.log_queue.put("No data from input file."); messagebox.showerror("Input Err", "No data in input file."); self.root.after(0, self.enable_buttons); return

        source_segments_original = []
        original_target_segments = [] 
        original_comments = []    
        modified_lines_count = 0

        # Get appropriate API key
        api_key = ""
        if provider == "Claude":
            api_key = self.api_keys["claude"]
        elif provider == "Gemini":
            api_key = self.api_keys["google"]
        elif provider == "OpenAI":
            api_key = self.api_keys["openai"]
        
        if not api_key:
            self.log_queue.put(f"No API key available for {provider}")
            messagebox.showerror("API Key Error", f"No API key configured for {provider}")
            self.root.after(0, self.enable_buttons)
            return

        if mode == "Translate":
            source_segments_original = all_original_data
            translator = create_translation_agent(provider, api_key, self.log_queue, model_name)
            if not translator or not translator.model: self.log_queue.put("Translator init fail."); messagebox.showerror("Model Err", "Translator model init failed."); self.root.after(0, self.enable_buttons); return
        elif mode == "Proofread":
            proofreader = create_proofreading_agent(provider, api_key, self.log_queue, model_name)
            if not proofreader or not proofreader.model: self.log_queue.put("Proofreader init fail."); messagebox.showerror("Model Err", "Proofreader model init failed."); self.root.after(0, self.enable_buttons); return
            for item in all_original_data:
                source_segments_original.append(item["source"])
                original_target_segments.append(item["target"])
                original_comments.append(item["comment"]) 

        final_output_targets_or_proofread_results = [None] * len(source_segments_original)
        tm_hits = 0; llm_processed_map = {}

        if mode == "Translate":
            if self.tm_agent.tm_data:
                self.log_queue.put(f"[TM] Applying {len(self.tm_agent.tm_data)} TM entries...")
                for i, seg in enumerate(source_segments_original):
                    tm_tgt = self.tm_agent.get_translation(seg)
                    if tm_tgt is not None: final_output_targets_or_proofread_results[i] = tm_tgt; tm_hits += 1
                self.log_queue.put(f"[TM] Applied TM to {tm_hits} segments.")
            else: self.log_queue.put("[TM] No TM data or file not specified.")
        
        full_source_doc_str = "\n".join([f"{i+1}. {line}" for i, line in enumerate(source_segments_original)])
        full_original_target_doc_str = "\n".join([f"{i+1}. {line}" for i, line in enumerate(original_target_segments)]) if mode == "Proofread" else ""
        
        lines_needing_llm_count = len(source_segments_original) - (tm_hits if mode == "Translate" else 0)

        if lines_needing_llm_count > 0:
            llm_indices = [i for i, processed_item in enumerate(final_output_targets_or_proofread_results) if processed_item is None]
            num_llm_chunks = math.ceil(lines_needing_llm_count / chunk_s)
            self.log_queue.put(f"LLM Segments for {mode}: {lines_needing_llm_count}. LLM Chunks: {num_llm_chunks if num_llm_chunks > 0 else '0'}")
            
            for i in range(num_llm_chunks):
                current_orig_doc_indices = llm_indices[i * chunk_s : min((i + 1) * chunk_s, lines_needing_llm_count)] 
                if not current_orig_doc_indices: continue
                self.log_queue.put(f"LLM Chunk {i+1}/{num_llm_chunks} ({mode}): Sending {len(current_orig_doc_indices)} segments...")
                
                if mode == "Translate":
                    lines_map_for_llm = {orig_idx + 1: f"{orig_idx + 1}. {source_segments_original[orig_idx]}" for orig_idx in current_orig_doc_indices}
                    chunk_results = translator.translate_specific_lines_with_drawings_context(lines_map_for_llm, full_source_doc_str, src_lang, tgt_lang, source_segments_original, drawings_map, user_custom_instructions)
                elif mode == "Proofread":
                    lines_map_for_llm = { orig_idx + 1: {"source": source_segments_original[orig_idx], "target_original": original_target_segments[orig_idx]} for orig_idx in current_orig_doc_indices }
                    chunk_results = proofreader.proofread_specific_lines_with_context(lines_map_for_llm, full_source_doc_str, full_original_target_doc_str, src_lang, tgt_lang, source_segments_original, drawings_map, user_custom_instructions)
                
                llm_processed_map.update(chunk_results)
                self.log_queue.put(f"Finished LLM Chunk {i+1}/{num_llm_chunks} for {mode}.")
        else: self.log_queue.put(f"No segments require LLM {mode} after TM (if applicable).")

        output_source_list = []
        output_target_list = []
        output_comment_list = [] 

        for i in range(len(source_segments_original)):
            source_text = source_segments_original[i]
            output_source_list.append(source_text)
            if mode == "Translate":
                target_text = final_output_targets_or_proofread_results[i] if final_output_targets_or_proofread_results[i] is not None else llm_processed_map.get(i + 1)
                output_target_list.append(target_text if target_text is not None else "[ERR - No TL]")
            elif mode == "Proofread":
                proofread_entry = llm_processed_map.get(i + 1) 
                original_target_text = original_target_segments[i]
                
                if proofread_entry:
                    revised_target = proofread_entry.get("revised_target", original_target_text)
                    ai_summary = proofread_entry.get("changes_summary")
                else: 
                    revised_target = original_target_text
                    ai_summary = "[Segment not processed by AI Proofreader]"
                
                output_target_list.append(revised_target)
                existing_comment = original_comments[i]
                comment_parts = []
                if existing_comment: comment_parts.append(f"ORIGINAL COMMENT:\n{existing_comment}")
                if revised_target.strip() != original_target_segments[i].strip(): 
                    if ai_summary and "No changes made" not in ai_summary:
                        comment_parts.append(f"PROOFREADER COMMENT (AI):\n{ai_summary}")
                    else: 
                        comment_parts.append(f"PROOFREADER COMMENT (AI):\nSegment was modified by AI.")
                    modified_lines_count +=1
                elif ai_summary and "No changes made" not in ai_summary: 
                     comment_parts.append(f"PROOFREADER COMMENT (AI):\n{ai_summary} (Note: Text appears identical to original despite summary.)")
                output_comment_list.append("\n\n".join(comment_parts).strip() if comment_parts else None)
        
        had_errors = any(t is None or "[Err" in str(t) or "[Missing" in str(t) or "[SYS ERR" in str(t) for t in output_target_list)
        file_ok = output_gen.process(output_source_list, output_target_list, output_f, self.log_queue, mode=mode, comments_list_for_output=output_comment_list if mode=="Proofread" else None)

        msg_title = "Success" if file_ok and not had_errors else "Partial Success" if file_ok else "Error"
        msg_detail_key = "SUCCESS" if file_ok and not had_errors else "PARTIAL" if file_ok else "FAIL"

        base_log_message_suffix = f"Output: {output_f}"
        if msg_detail_key == "PARTIAL":
            base_log_message_suffix += ". Check logs."
        elif msg_detail_key == "FAIL":
            base_log_message_suffix = "Check logs."

        final_log_message = f"\n--- {mode.upper()} {msg_detail_key}! "
        
        if mode == "Translate":
            final_log_message += f"TM Hits: {tm_hits}. LLM Segs processed: {len(llm_processed_map)}. "
        elif mode == "Proofread":
            final_log_message += f"LLM Segs processed: {len(llm_processed_map)}. Lines Modified by AI: {modified_lines_count}. "
        
        final_log_message += base_log_message_suffix + " ---"
        self.log_queue.put(final_log_message)

        messagebox_func = messagebox.showinfo if msg_title == "Success" else messagebox.showwarning if msg_title == "Partial Success" else messagebox.showerror
        messagebox_func(msg_title, f"{mode} {msg_detail_key.lower()}! Output: {output_f if file_ok else 'not saved'}\nSee logs for details.")
        self.root.after(0, self.enable_buttons)

    def enable_buttons(self): 
        self.process_button.config(state="normal", text="Start Process")
        self.list_models_button.config(state="normal")
        self.refresh_models_button.config(state="normal")

if __name__ == "__main__":
    # Check if at least one library is available
    if not GOOGLE_AI_AVAILABLE and not CLAUDE_AVAILABLE and not OPENAI_AVAILABLE:
        error_details = f"Google AI: {GOOGLE_AI_IMPORT_ERROR_MESSAGE}\nClaude: {CLAUDE_IMPORT_ERROR_MESSAGE}\nOpenAI: {OPENAI_IMPORT_ERROR_MESSAGE}"
        print(f"\nApp cannot init: No AI libraries available.\nDetails:\n{error_details}\nInstall at least one library per console instructions.")
        try: 
            root_err = tk.Tk(); root_err.withdraw()
            messagebox.showerror("Critical Startup Error", f"No AI libraries available:\n{error_details}\nInstall libraries & restart.\nApp will close.")
            root_err.destroy()
        except: pass 
        sys.exit(1) 
    
    # Load and check API keys
    api_keys = load_api_keys()
    if not api_keys["google"] and not api_keys["claude"] and not api_keys["openai"]:
        print("WARNING: No API keys configured in api_keys.txt...")
    
    if not PIL_AVAILABLE: print("NOTE: Pillow (PIL) not found. Image features disabled.")
    
    root = tk.Tk(); app = TranslationApp(root); root.mainloop()