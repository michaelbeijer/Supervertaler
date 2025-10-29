"""
AutoFingers Translation Automation Engine
Replicates AutoHotkey AutoFingers functionality in Python
Automates translation pasting in memoQ from TMX translation memory
"""

import time
import xml.etree.ElementTree as ET
from typing import Dict, Optional, Tuple
import pyperclip
import pyautogui
import re

# Try to import AHK for better keyboard control
try:
    from ahk import AHK
    HAS_AHK = True
    _ahk_instance = None  # Lazy initialization
    print("✓ AHK library imported successfully")
except ImportError as e:
    HAS_AHK = False
    _ahk_instance = None
    print(f"✗ AHK library not available: {e}")


def get_ahk():
    """Get or create AHK instance lazily"""
    global _ahk_instance
    if _ahk_instance is None and HAS_AHK:
        try:
            _ahk_instance = AHK()
            print(f"✓ AHK instance created: {_ahk_instance}")
        except Exception as e:
            print(f"✗ AHK instance creation failed: {e}")
            return None
    return _ahk_instance


class AutoFingersEngine:
    """
    Translation automation engine for CAT tools like memoQ.
    Loads translations from TMX and automates the paste workflow.
    """
    
    def __init__(self, tmx_file: str, source_lang: str = "en", target_lang: str = "nl"):
        """
        Initialize the AutoFingers engine.
        
        Args:
            tmx_file: Path to TMX translation memory file
            source_lang: Source language code (e.g., 'en')
            target_lang: Target language code (e.g., 'nl')
        """
        self.tmx_file = tmx_file
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.tm_database: Dict[str, str] = {}
        self.tm_count = 0
        
        # Timing settings (milliseconds)
        self.loop_delay = 4000
        self.confirm_delay = 900
        self.copy_source_delay = 600
        self.select_all_delay = 400
        self.copy_delay = 800
        self.paste_delay = 800
        self.confirm_enter_delay = 1200
        
        # Behavior settings
        self.auto_confirm = True
        self.skip_no_match = False
        
        # State tracking
        self.is_running = False
        self.segments_processed = 0
        
    def load_tmx(self) -> Tuple[bool, str]:
        """
        Load and parse TMX translation memory file.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            self.tm_database.clear()
            self.tm_count = 0
            
            # Parse TMX XML
            tree = ET.parse(self.tmx_file)
            root = tree.getroot()
            
            # Find all translation units
            for tu in root.findall('.//tu'):
                source_text = None
                target_text = None
                
                # Extract source and target segments
                for tuv in tu.findall('tuv'):
                    lang = tuv.get('{http://www.w3.org/XML/1998/namespace}lang', 
                                   tuv.get('lang', ''))
                    
                    seg = tuv.find('seg')
                    if seg is not None and seg.text:
                        if lang.lower().startswith(self.source_lang.lower()):
                            source_text = seg.text.strip()
                        elif lang.lower().startswith(self.target_lang.lower()):
                            target_text = seg.text.strip()
                
                # Add to database if both source and target found
                if source_text and target_text:
                    # Normalize dashes for matching
                    normalized_source = self._normalize_dashes(source_text)
                    self.tm_database[normalized_source] = target_text
                    self.tm_count += 1
            
            return True, f"Loaded {self.tm_count} translation units"
            
        except FileNotFoundError:
            return False, f"TMX file not found: {self.tmx_file}"
        except ET.ParseError as e:
            return False, f"XML parse error: {str(e)}"
        except Exception as e:
            return False, f"Error loading TMX: {str(e)}"
    
    def _normalize_dashes(self, text: str) -> str:
        """
        Normalize different types of dashes to regular hyphen for matching.
        
        Args:
            text: Text to normalize
            
        Returns:
            Text with normalized dashes
        """
        # Replace en-dash (–) and em-dash (—) with regular hyphen
        text = text.replace('–', '-')  # En-dash
        text = text.replace('—', '-')  # Em-dash
        text = text.replace('−', '-')  # Minus sign
        return text
    
    def lookup_translation(self, source_text: str) -> Optional[str]:
        """
        Look up translation for source text in TM database.
        
        Args:
            source_text: Source text to translate
            
        Returns:
            Translation if found, None otherwise
        """
        if not source_text:
            return None
        
        # Normalize and lookup
        normalized = self._normalize_dashes(source_text.strip())
        return self.tm_database.get(normalized)
    
    def process_single_segment(self) -> Tuple[bool, str]:
        """
        Process a single translation segment in memoQ.
        Automates: copy source to target, lookup translation, paste, confirm.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Clear clipboard
            pyperclip.copy('')
            time.sleep(0.2)
            
            # Step 1: Copy source to target (Ctrl+Shift+S in memoQ)
            pyautogui.hotkey('ctrl', 'shift', 's')
            time.sleep(self.copy_source_delay / 1000)
            
            # Step 2: Select all (Ctrl+A)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(self.select_all_delay / 1000)
            
            # Step 3: Copy to clipboard (Ctrl+C)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(self.copy_delay / 1000)
            
            # Step 4: Get clipboard content
            source_text = pyperclip.paste().strip()
            
            if not source_text:
                return False, "Empty source text"
            
            # Step 5: Look up translation
            translation = self.lookup_translation(source_text)
            
            if not translation:
                if self.skip_no_match:
                    # Clear target box
                    pyautogui.hotkey('ctrl', 'a')  # Select all
                    time.sleep(0.1)
                    pyautogui.press('backspace')  # Delete
                    time.sleep(0.3)
                    
                    # Use Alt+N (Go to Next) in memoQ
                    pyautogui.hotkey('alt', 'n')
                    time.sleep(self.confirm_delay / 1000)
                    
                    return True, f"No translation - skipped: {source_text[:50]}..."
                else:
                    # Pause for manual handling
                    self.is_running = False
                    return False, f"No translation found. Paused at: {source_text[:50]}..."
            
            # Step 6: Copy translation to clipboard and paste
            pyperclip.copy(translation)
            time.sleep(0.4)
            
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(self.paste_delay / 1000)
            
            # Step 7: Confirm and move to next (Ctrl+Enter)
            if self.auto_confirm:
                time.sleep(self.confirm_delay / 1000)
                pyautogui.hotkey('ctrl', 'enter')
                time.sleep(self.confirm_enter_delay / 1000)
            
            self.segments_processed += 1
            return True, f"Processed: {source_text[:30]}... → {translation[:30]}..."
            
        except Exception as e:
            self.is_running = False
            return False, f"Error processing segment: {str(e)}"
    
    def process_multiple_segments(self, max_segments: int = 0, 
                                   callback=None) -> Tuple[int, str]:
        """
        Process multiple segments in loop mode.
        
        Args:
            max_segments: Maximum segments to process (0 = infinite)
            callback: Optional callback function(success, message) called after each segment
            
        Returns:
            Tuple of (segments_processed: int, final_message: str)
        """
        self.is_running = True
        self.segments_processed = 0
        
        try:
            while self.is_running:
                # Check if reached limit
                if max_segments > 0 and self.segments_processed >= max_segments:
                    msg = f"Completed {self.segments_processed} segments"
                    return self.segments_processed, msg
                
                # Process one segment
                success, message = self.process_single_segment()
                
                # Call callback if provided
                if callback:
                    callback(success, message)
                
                # If failed and not skipping, stop loop
                if not success and not self.skip_no_match:
                    break
                
                # Wait before next segment
                time.sleep(self.loop_delay / 1000)
            
            msg = f"Processed {self.segments_processed} segment(s)"
            return self.segments_processed, msg
            
        except KeyboardInterrupt:
            self.is_running = False
            return self.segments_processed, "Stopped by user"
        except Exception as e:
            self.is_running = False
            return self.segments_processed, f"Error: {str(e)}"
    
    def stop(self):
        """Stop the automation loop."""
        self.is_running = False
    
    def create_empty_tmx(self) -> bool:
        """
        Create an empty TMX file with proper structure.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            tmx_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE tmx SYSTEM "tmx14.dtd">
<tmx version="1.4">
  <header
    creationtool="AutoFingers"
    creationtoolversion="1.0"
    datatype="PlainText"
    segtype="sentence"
    adminlang="en-US"
    srclang="{self.source_lang}"
    o-tmf="AutoFingers"
  />
  <body>
    <!-- Add translation units here -->
    <!-- Example:
    <tu>
      <tuv xml:lang="{self.source_lang}">
        <seg>Source text here</seg>
      </tuv>
      <tuv xml:lang="{self.target_lang}">
        <seg>Target translation here</seg>
      </tuv>
    </tu>
    -->
  </body>
</tmx>
"""
            with open(self.tmx_file, 'w', encoding='utf-8') as f:
                f.write(tmx_content)
            return True
        except Exception as e:
            print(f"Error creating TMX: {e}")
            return False


# Example usage
if __name__ == "__main__":
    # Create engine instance
    engine = AutoFingersEngine(
        tmx_file="autofingers_tm.tmx",
        source_lang="en",
        target_lang="nl"
    )
    
    # Load TMX
    success, message = engine.load_tmx()
    print(message)
    
    if success:
        # Process single segment
        print("\nProcessing single segment...")
        print("Switch to memoQ window in 3 seconds...")
        time.sleep(3)
        
        success, msg = engine.process_single_segment()
        print(msg)
