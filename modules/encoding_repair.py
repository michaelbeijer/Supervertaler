"""
Text Encoding Corruption Detection and Repair Module

Detects and fixes common text encoding issues (mojibake), particularly:
- UTF-8 text incorrectly decoded as Latin-1 (Windows-1252)
- Double-encoded Unicode escape sequences
- Common encoding corruption patterns
"""

import re
from pathlib import Path
from typing import Tuple, List, Dict
import chardet


class EncodingRepair:
    """Detect and repair text encoding corruption."""
    
    # Common mojibake patterns (UTF-8 misinterpreted as Latin-1)
    CORRUPTION_PATTERNS = {
        # En dash, em dash, hyphen variants
        r'\u00e2\u20ac\u201c': '–',  # en dash
        r'\u00e2\u20ac\u201d': '—',  # em dash
        r'\u00e2\u20ac\u0090': '-',  # non-breaking hyphen
        
        # Quotes and apostrophes
        r'\u00e2\u20ac\u0153': '"',  # left double quote
        r'\u00e2\u20ac\u009d': '"',  # right double quote
        r'\u00e2\u20ac\u0098': ''',   # left single quote
        r'\u00e2\u20ac\u0099': ''',   # right single quote
        r'\u00e2\u20ac\u2122': ''',   # apostrophe/right single quote
        
        # Ellipsis and other punctuation
        r'\u00e2\u20ac\u00a6': '…',   # ellipsis
        r'\u00e2\u20ac\u00a2': '•',   # bullet
        
        # Spaces
        r'\u00c2\u00a0': ' ',          # non-breaking space
        
        # Degree and special symbols
        r'\u00c2\u00b0': '°',          # degree
        r'\u00c3\u00a9': 'é',          # e acute (example)
    }
    
    # Regex pattern to find potential corruption sequences
    UNICODE_ESCAPE_PATTERN = re.compile(r'\\u[0-9a-fA-F]{4}')
    
    @staticmethod
    def detect_corruption(text: str) -> Tuple[bool, int, List[str]]:
        """
        Detect if text contains encoding corruption patterns.
        
        Args:
            text: Text content to analyze
            
        Returns:
            Tuple of (has_corruption, corruption_count, list_of_patterns_found)
        """
        corruptions_found = []
        patterns_found = []
        
        for pattern in EncodingRepair.CORRUPTION_PATTERNS.keys():
            matches = text.count(pattern)
            if matches > 0:
                corruptions_found.append(pattern)
                corrected_char = EncodingRepair.CORRUPTION_PATTERNS[pattern]
                patterns_found.append(f"{pattern} → {corrected_char} ({matches} occurrences)")
        
        has_corruption = len(corruptions_found) > 0
        corruption_count = sum(text.count(p) for p in corruptions_found)
        
        return has_corruption, corruption_count, patterns_found
    
    @staticmethod
    def repair_text(text: str) -> str:
        """
        Repair encoding corruption in text.
        
        Args:
            text: Text content to repair
            
        Returns:
            Repaired text
        """
        repaired = text
        
        for pattern, replacement in EncodingRepair.CORRUPTION_PATTERNS.items():
            repaired = repaired.replace(pattern, replacement)
        
        return repaired
    
    @staticmethod
    def repair_file(file_path: str, encoding: str = 'utf-8') -> Tuple[bool, str, Dict]:
        """
        Detect and repair encoding corruption in a file.
        
        Args:
            file_path: Path to the file to repair
            encoding: Encoding to use when reading the file
            
        Returns:
            Tuple of (success, message, repair_info)
        """
        try:
            file_path = Path(file_path)
            
            # Read file
            with open(file_path, 'r', encoding=encoding) as f:
                original_text = f.read()
            
            # Detect corruption
            has_corruption, corruption_count, patterns = EncodingRepair.detect_corruption(original_text)
            
            repair_info = {
                'file': str(file_path),
                'encoding': encoding,
                'has_corruption': has_corruption,
                'corruption_count': corruption_count,
                'patterns_found': patterns,
                'original_size': len(original_text),
            }
            
            if not has_corruption:
                return True, "No encoding corruption detected.", repair_info
            
            # Repair
            repaired_text = EncodingRepair.repair_text(original_text)
            
            # Write back
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(repaired_text)
            
            repair_info['repaired_size'] = len(repaired_text)
            
            message = (
                f"✅ File repaired successfully!\n"
                f"Found and fixed {corruption_count} corruption(s) in {len(patterns)} pattern(s).\n"
                f"Patterns:\n" + "\n".join(f"  • {p}" for p in patterns)
            )
            
            return True, message, repair_info
            
        except Exception as e:
            return False, f"❌ Error: {str(e)}", {'error': str(e)}
    
    @staticmethod
    def repair_with_encoding_fallback(file_path: str) -> Tuple[bool, str, Dict]:
        """
        Try to repair a file by attempting different encodings.
        
        This handles the case where the file itself might be in the wrong encoding.
        
        Args:
            file_path: Path to the file to repair
            
        Returns:
            Tuple of (success, message, repair_info)
        """
        try:
            file_path = Path(file_path)
            
            # Try to detect encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read()
            
            detected = chardet.detect(raw_data)
            detected_encoding = detected.get('encoding', 'utf-8')
            
            # Try reading with detected encoding first
            try:
                with open(file_path, 'r', encoding=detected_encoding) as f:
                    text = f.read()
            except (UnicodeDecodeError, LookupError):
                # Fall back to utf-8
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
            
            # Now detect corruption
            has_corruption, corruption_count, patterns = EncodingRepair.detect_corruption(text)
            
            if not has_corruption:
                return True, "No encoding corruption detected.", {
                    'file': str(file_path),
                    'detected_encoding': detected_encoding,
                    'corruption_count': 0,
                }
            
            # Repair
            repaired_text = EncodingRepair.repair_text(text)
            
            # Write back as UTF-8
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(repaired_text)
            
            message = (
                f"✅ File repaired successfully!\n"
                f"Original encoding: {detected_encoding}\n"
                f"Fixed {corruption_count} corruption(s) in {len(patterns)} pattern(s).\n"
                f"Saved as UTF-8.\n"
                f"Patterns:\n" + "\n".join(f"  • {p}" for p in patterns)
            )
            
            return True, message, {
                'file': str(file_path),
                'detected_encoding': detected_encoding,
                'corruption_count': corruption_count,
                'patterns_found': patterns,
            }
            
        except Exception as e:
            return False, f"❌ Error: {str(e)}", {'error': str(e)}
    
    @staticmethod
    def scan_directory(directory_path: str, file_extensions: List[str] = None) -> Dict:
        """
        Scan a directory for files with encoding corruption.
        
        Args:
            directory_path: Path to directory to scan
            file_extensions: List of file extensions to check (e.g., ['.txt', '.csv'])
                           If None, scans all files.
            
        Returns:
            Dictionary with scan results
        """
        if file_extensions is None:
            file_extensions = ['.txt', '.csv', '.tsv', '.md']
        
        dir_path = Path(directory_path)
        results = {
            'directory': str(dir_path),
            'files_scanned': 0,
            'files_with_corruption': [],
            'total_corruptions': 0,
        }
        
        try:
            for file_path in dir_path.rglob('*'):
                # Skip directories
                if file_path.is_dir():
                    continue
                
                # Check extension if specified
                if file_extensions and file_path.suffix.lower() not in file_extensions:
                    continue
                
                results['files_scanned'] += 1
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    has_corruption, count, patterns = EncodingRepair.detect_corruption(content)
                    
                    if has_corruption:
                        results['files_with_corruption'].append({
                            'file': str(file_path),
                            'corruptions': count,
                            'patterns': patterns,
                        })
                        results['total_corruptions'] += count
                
                except Exception as e:
                    pass  # Skip files that can't be read
        
        except Exception as e:
            results['error'] = str(e)
        
        return results


# Example usage / testing
if __name__ == '__main__':
    # Test text with mojibake
    test_text = (
        'young concrete\u00e2\u20ac\u201cjong beton\n'
        'aggregate \u00e2\u20ac\u201c chemical impurities\u00e2\u20ac\u201ctoeslagmateriaal\n'
        'Poisson\u00e2\u20ac\u2122s ratio\u00e2\u20ac\u201ccoëfficiënt van Poisson'
    )
    
    print("Original text:")
    print(test_text)
    print("\n" + "="*60 + "\n")
    
    # Detect corruption
    has_corruption, count, patterns = EncodingRepair.detect_corruption(test_text)
    print(f"Corruption detected: {has_corruption}")
    print(f"Total corruptions: {count}")
    print("Patterns found:")
    for p in patterns:
        print(f"  • {p}")
    print("\n" + "="*60 + "\n")
    
    # Repair
    repaired = EncodingRepair.repair_text(test_text)
    print("Repaired text:")
    print(repaired)
