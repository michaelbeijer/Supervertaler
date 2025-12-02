"""
Local LLM Setup Module for Supervertaler
=========================================

Provides setup wizard, status checking, and model management for local LLM
integration via Ollama.

Features:
- Ollama installation detection and guidance
- Hardware detection (RAM, GPU) for model recommendations
- Model download and management
- Connection testing

Usage:
    from modules.local_llm_setup import LocalLLMSetupDialog, check_ollama_status
    
    # Check if Ollama is running
    status = check_ollama_status()
    if status['running']:
        print(f"Ollama running with models: {status['models']}")
    
    # Show setup wizard
    dialog = LocalLLMSetupDialog(parent)
    dialog.exec()

Author: Supervertaler Team
Date: December 2025
"""

import os
import sys
import subprocess
import webbrowser
from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QComboBox, QProgressBar, QTextEdit, QWidget,
    QMessageBox, QFrame, QSizePolicy, QApplication
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont


# =============================================================================
# CONSTANTS
# =============================================================================

DEFAULT_OLLAMA_ENDPOINT = "http://localhost:11434"

# Recommended models with metadata
RECOMMENDED_MODELS = {
    "qwen2.5:3b": {
        "name": "Qwen 2.5 3B",
        "description": "Fast & lightweight - good for simple translations",
        "size_gb": 2.0,
        "ram_required_gb": 4,
        "quality_stars": 3,
        "strengths": ["Fast", "Low memory", "Multilingual"],
        "use_case": "Quick drafts, simple text, low-end hardware",
        "download_size": "1.9 GB"
    },
    "qwen2.5:7b": {
        "name": "Qwen 2.5 7B",
        "description": "Recommended - excellent multilingual quality",
        "size_gb": 4.4,
        "ram_required_gb": 8,
        "quality_stars": 4,
        "strengths": ["Excellent multilingual", "Good quality", "Balanced speed"],
        "use_case": "General translation, most European languages",
        "download_size": "4.4 GB",
        "recommended": True
    },
    "llama3.2:3b": {
        "name": "Llama 3.2 3B",
        "description": "Meta's efficient model - good English",
        "size_gb": 2.0,
        "ram_required_gb": 4,
        "quality_stars": 3,
        "strengths": ["Fast", "Good English", "Efficient"],
        "use_case": "English-centric translations, quick drafts",
        "download_size": "2.0 GB"
    },
    "mistral:7b": {
        "name": "Mistral 7B",
        "description": "Strong European language support",
        "size_gb": 4.1,
        "ram_required_gb": 8,
        "quality_stars": 4,
        "strengths": ["European languages", "French", "Fast inference"],
        "use_case": "French, German, Spanish translations",
        "download_size": "4.1 GB"
    },
    "gemma2:9b": {
        "name": "Gemma 2 9B",
        "description": "Google's quality model - best for size",
        "size_gb": 5.5,
        "ram_required_gb": 10,
        "quality_stars": 5,
        "strengths": ["High quality", "Good reasoning", "Multilingual"],
        "use_case": "Quality-focused translation, technical content",
        "download_size": "5.4 GB"
    },
    "qwen2.5:14b": {
        "name": "Qwen 2.5 14B",
        "description": "Premium quality - needs 16GB+ RAM",
        "size_gb": 9.0,
        "ram_required_gb": 16,
        "quality_stars": 5,
        "strengths": ["Excellent quality", "Complex text", "Nuanced translation"],
        "use_case": "Premium translations, complex documents",
        "download_size": "8.9 GB"
    },
    "llama3.1:8b": {
        "name": "Llama 3.1 8B",
        "description": "Meta's capable model - good all-rounder",
        "size_gb": 4.7,
        "ram_required_gb": 8,
        "quality_stars": 4,
        "strengths": ["Versatile", "Good quality", "Well-tested"],
        "use_case": "General purpose translation",
        "download_size": "4.7 GB"
    },
    # === LARGE MODELS (32GB+ RAM required) ===
    "qwen2.5:32b": {
        "name": "Qwen 2.5 32B",
        "description": "Alibaba's flagship model - excellent for translation",
        "size_gb": 19.9,
        "ram_required_gb": 32,
        "quality_stars": 5,
        "strengths": ["Top translation quality", "Excellent multilingual", "Nuanced output"],
        "use_case": "High-quality professional translation",
        "download_size": "19.9 GB"
    },
    "qwen2.5:72b": {
        "name": "Qwen 2.5 72B",
        "description": "Alibaba's largest model - best quality, very slow on CPU",
        "size_gb": 43.0,
        "ram_required_gb": 48,
        "quality_stars": 5,
        "strengths": ["Highest quality", "Best multilingual", "Near cloud-level"],
        "use_case": "Maximum quality (needs 48GB+ RAM, very slow)",
        "download_size": "43 GB"
    },
    "mixtral:8x7b": {
        "name": "Mixtral 8x7B",
        "description": "Mistral's mixture-of-experts model - very capable",
        "size_gb": 26.4,
        "ram_required_gb": 32,
        "quality_stars": 5,
        "strengths": ["Excellent reasoning", "Strong multilingual", "Efficient inference"],
        "use_case": "High-quality translation with fast inference",
        "download_size": "26.4 GB"
    },
    "command-r:35b": {
        "name": "Command R 35B",
        "description": "Cohere's RAG-optimized model - excellent for context",
        "size_gb": 20.0,
        "ram_required_gb": 40,
        "quality_stars": 5,
        "strengths": ["Context-aware", "Strong reasoning", "Good for technical text"],
        "use_case": "Technical and specialized translation",
        "download_size": "20.0 GB"
    },
    # === DUTCH/MULTILINGUAL SPECIALISTS ===
    "aya-expanse:8b": {
        "name": "Aya Expanse 8B",
        "description": "Cohere's multilingual model - excellent for Dutch",
        "size_gb": 4.8,
        "ram_required_gb": 8,
        "quality_stars": 5,
        "strengths": ["Top Dutch support", "High fidelity translation", "23 languages"],
        "use_case": "Dutch-English translation (Top Pick)",
        "download_size": "4.8 GB"
    },
    "openeurollm-dutch": {
        "name": "OpenEuroLLM Dutch 9B",
        "description": "Gemma3 fine-tuned for Dutch - strong grammar",
        "size_gb": 5.4,
        "ram_required_gb": 8,
        "quality_stars": 4,
        "strengths": ["Dutch grammar/idioms", "European tech docs", "Fine-tuned"],
        "use_case": "Dutch technical documentation",
        "download_size": "5.4 GB"
    },
    "geitje-7b-ultra": {
        "name": "GEITje 7B Ultra",
        "description": "Dutch-specialized Mistral - conversational",
        "size_gb": 4.1,
        "ram_required_gb": 6,
        "quality_stars": 4,
        "strengths": ["Dutch-specialized", "Adaptable prompts", "Fast"],
        "use_case": "Dutch conversational translation",
        "download_size": "4.1 GB"
    },
    "stablelm2:12b": {
        "name": "StableLM 2 12B",
        "description": "Multilingual training including Dutch",
        "size_gb": 7.3,
        "ram_required_gb": 10,
        "quality_stars": 4,
        "strengths": ["Multilingual", "Stable output", "Good for summaries"],
        "use_case": "General multilingual tasks",
        "download_size": "7.3 GB"
    }
}


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_ollama_endpoint() -> str:
    """Get Ollama endpoint from environment or return default."""
    return os.environ.get('OLLAMA_ENDPOINT', DEFAULT_OLLAMA_ENDPOINT)


def check_ollama_status(endpoint: str = None) -> Dict:
    """
    Check if Ollama is running and get available models.
    
    Args:
        endpoint: Ollama API endpoint (default: http://localhost:11434)
        
    Returns:
        Dict with:
            - running: bool - whether Ollama is running
            - models: list - available model names  
            - version: str - Ollama version if available
            - error: str - error message if not running
    """
    try:
        import requests
    except ImportError:
        return {
            'running': False,
            'models': [],
            'version': None,
            'endpoint': endpoint or get_ollama_endpoint(),
            'error': "Requests library not installed"
        }
    
    endpoint = endpoint or get_ollama_endpoint()
    
    try:
        # Check if Ollama is running by getting model list
        response = requests.get(f"{endpoint}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = [m['name'] for m in data.get('models', [])]
            
            # Try to get version
            version = None
            try:
                ver_response = requests.get(f"{endpoint}/api/version", timeout=2)
                if ver_response.status_code == 200:
                    version = ver_response.json().get('version')
            except:
                pass
            
            return {
                'running': True,
                'models': models,
                'version': version,
                'endpoint': endpoint,
                'error': None
            }
        else:
            return {
                'running': False,
                'models': [],
                'version': None,
                'endpoint': endpoint,
                'error': f"Ollama returned status {response.status_code}"
            }
    except requests.exceptions.ConnectionError:
        return {
            'running': False,
            'models': [],
            'version': None,
            'endpoint': endpoint,
            'error': "Cannot connect to Ollama. Is it installed and running?"
        }
    except Exception as e:
        return {
            'running': False,
            'models': [],
            'version': None,
            'endpoint': endpoint,
            'error': str(e)
        }


def detect_system_specs() -> Dict:
    """
    Detect system hardware specifications.
    
    Returns:
        Dict with:
            - ram_gb: Total RAM in GB
            - gpu_name: GPU name if detected
            - gpu_vram_gb: GPU VRAM in GB if detected
            - os_name: Operating system name
            - recommended_model: Suggested model based on specs
    """
    import platform
    
    specs = {
        'ram_gb': 8,  # Default assumption
        'gpu_name': None,
        'gpu_vram_gb': None,
        'os_name': platform.system(),
        'recommended_model': 'qwen2.5:7b'
    }
    
    # Detect RAM
    try:
        import psutil
        specs['ram_gb'] = round(psutil.virtual_memory().total / (1024**3), 1)
    except ImportError:
        # Try Windows-specific method
        if platform.system() == 'Windows':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                c_ulonglong = ctypes.c_ulonglong
                
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ('dwLength', ctypes.c_ulong),
                        ('dwMemoryLoad', ctypes.c_ulong),
                        ('ullTotalPhys', c_ulonglong),
                        ('ullAvailPhys', c_ulonglong),
                        ('ullTotalPageFile', c_ulonglong),
                        ('ullAvailPageFile', c_ulonglong),
                        ('ullTotalVirtual', c_ulonglong),
                        ('ullAvailVirtual', c_ulonglong),
                        ('ullAvailExtendedVirtual', c_ulonglong),
                    ]
                
                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(stat)
                kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                specs['ram_gb'] = round(stat.ullTotalPhys / (1024**3), 1)
            except:
                pass
    
    # Detect GPU (basic detection)
    try:
        if platform.system() == 'Windows':
            # Try to detect NVIDIA GPU
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                parts = result.stdout.strip().split(', ')
                if len(parts) >= 2:
                    specs['gpu_name'] = parts[0]
                    # Parse VRAM (e.g., "8192 MiB" -> 8)
                    vram_str = parts[1].replace(' MiB', '').replace(' MB', '')
                    try:
                        specs['gpu_vram_gb'] = round(int(vram_str) / 1024, 1)
                    except:
                        pass
    except:
        pass
    
    # Recommend model based on RAM
    ram = specs['ram_gb']
    if ram >= 16:
        specs['recommended_model'] = 'qwen2.5:14b'
    elif ram >= 10:
        specs['recommended_model'] = 'gemma2:9b'
    elif ram >= 8:
        specs['recommended_model'] = 'qwen2.5:7b'
    elif ram >= 4:
        specs['recommended_model'] = 'qwen2.5:3b'
    else:
        specs['recommended_model'] = 'llama3.2:3b'
    
    return specs


def get_model_recommendations(ram_gb: float) -> List[Dict]:
    """
    Get model recommendations based on available RAM.
    
    Args:
        ram_gb: Available RAM in gigabytes
        
    Returns:
        List of model dicts sorted by recommendation priority
    """
    compatible = []
    
    for model_id, info in RECOMMENDED_MODELS.items():
        if info['ram_required_gb'] <= ram_gb:
            model_info = info.copy()
            model_info['id'] = model_id
            model_info['compatible'] = True
            compatible.append(model_info)
        else:
            model_info = info.copy()
            model_info['id'] = model_id
            model_info['compatible'] = False
            compatible.append(model_info)
    
    # Sort: compatible first, then by quality (descending), then by size (ascending)
    compatible.sort(key=lambda x: (
        not x['compatible'],
        -x['quality_stars'],
        x['ram_required_gb']
    ))
    
    return compatible


# =============================================================================
# BACKGROUND WORKERS
# =============================================================================

class ModelDownloadWorker(QThread):
    """Background worker for downloading Ollama models."""
    
    progress = pyqtSignal(str)  # Progress message
    finished = pyqtSignal(bool, str)  # Success, message
    
    def __init__(self, model_name: str, endpoint: str = None):
        super().__init__()
        self.model_name = model_name
        self.endpoint = endpoint or get_ollama_endpoint()
        self._cancelled = False
    
    def cancel(self):
        self._cancelled = True
    
    def run(self):
        """Download model using Ollama API."""
        try:
            import requests
            
            self.progress.emit(f"Starting download of {self.model_name}...")
            
            # Use streaming pull endpoint
            response = requests.post(
                f"{self.endpoint}/api/pull",
                json={"name": self.model_name, "stream": True},
                stream=True,
                timeout=3600  # 1 hour timeout for large models
            )
            
            if response.status_code != 200:
                self.finished.emit(False, f"Download failed: HTTP {response.status_code}")
                return
            
            last_status = ""
            for line in response.iter_lines():
                if self._cancelled:
                    self.finished.emit(False, "Download cancelled")
                    return
                
                if line:
                    try:
                        import json
                        data = json.loads(line)
                        status = data.get('status', '')
                        
                        # Show progress
                        if 'completed' in data and 'total' in data:
                            pct = int(data['completed'] / data['total'] * 100)
                            completed_mb = data['completed'] / (1024 * 1024)
                            total_mb = data['total'] / (1024 * 1024)
                            self.progress.emit(f"{status}: {completed_mb:.0f} MB / {total_mb:.0f} MB ({pct}%)")
                        elif status != last_status:
                            self.progress.emit(status)
                            last_status = status
                    except:
                        pass
            
            self.finished.emit(True, f"Successfully downloaded {self.model_name}")
            
        except requests.exceptions.ConnectionError:
            self.finished.emit(False, "Cannot connect to Ollama. Is it running?")
        except Exception as e:
            self.finished.emit(False, f"Download error: {str(e)}")


class ConnectionTestWorker(QThread):
    """Background worker for testing Ollama connection with a simple prompt."""
    
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str, str)  # Success, message, response
    
    def __init__(self, model_name: str, endpoint: str = None):
        super().__init__()
        self.model_name = model_name
        self.endpoint = endpoint or get_ollama_endpoint()
    
    def run(self):
        """Test model with a simple translation prompt."""
        try:
            import requests
            
            self.progress.emit(f"Loading model {self.model_name}...")
            self.progress.emit("(First load may take 30-60 seconds)")
            
            # Simple test prompt
            test_prompt = "Translate to Dutch: Hello, how are you today?"
            
            response = requests.post(
                f"{self.endpoint}/api/chat",
                json={
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": test_prompt}],
                    "stream": False,
                    "options": {"temperature": 0.3, "num_predict": 50}
                },
                timeout=180  # 3 min for model loading
            )
            
            if response.status_code == 200:
                result = response.json()
                translation = result.get('message', {}).get('content', 'No response')
                self.finished.emit(True, "Model is working!", translation.strip())
            else:
                self.finished.emit(False, f"Model test failed: HTTP {response.status_code}", "")
                
        except requests.exceptions.Timeout:
            self.finished.emit(False, "Test timed out. Model may still be loading.", "")
        except requests.exceptions.ConnectionError:
            self.finished.emit(False, "Cannot connect to Ollama", "")
        except Exception as e:
            self.finished.emit(False, f"Test error: {str(e)}", "")


# =============================================================================
# SETUP DIALOG
# =============================================================================

class LocalLLMSetupDialog(QDialog):
    """
    Setup wizard for local LLM configuration.
    
    Guides users through:
    1. Checking if Ollama is installed and running
    2. Detecting hardware specs
    3. Recommending and downloading a model
    4. Testing the connection
    """
    
    def __init__(self, parent=None, log_callback: Callable = None):
        super().__init__(parent)
        self.log = log_callback or print
        self.download_worker = None
        self.test_worker = None
        
        self.setWindowTitle("Local LLM Setup")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        self.init_ui()
        self.refresh_status()
    
    def init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("🖥️ Local LLM Setup")
        header.setStyleSheet("font-size: 18pt; font-weight: bold; color: #1976D2;")
        layout.addWidget(header)
        
        desc = QLabel(
            "Run AI translation locally on your computer - no API keys needed, "
            "complete privacy, works offline."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666; padding: 5px; background-color: #E3F2FD; border-radius: 5px;")
        layout.addWidget(desc)
        
        # === STEP 1: Ollama Status ===
        self.ollama_group = QGroupBox("Step 1: Ollama Status")
        ollama_layout = QVBoxLayout()
        
        self.status_label = QLabel("Checking Ollama status...")
        self.status_label.setStyleSheet("padding: 10px;")
        ollama_layout.addWidget(self.status_label)
        
        btn_row = QHBoxLayout()
        self.install_btn = QPushButton("📥 Download Ollama")
        self.install_btn.clicked.connect(self.open_ollama_download)
        self.install_btn.setToolTip("Opens Ollama download page in your browser")
        btn_row.addWidget(self.install_btn)
        
        self.start_btn = QPushButton("▶️ Start Ollama")
        self.start_btn.clicked.connect(self.start_ollama)
        self.start_btn.setToolTip("Start the Ollama service on your computer")
        btn_row.addWidget(self.start_btn)
        
        self.refresh_btn = QPushButton("🔄 Refresh Status")
        self.refresh_btn.clicked.connect(self.refresh_status)
        btn_row.addWidget(self.refresh_btn)
        
        btn_row.addStretch()
        ollama_layout.addLayout(btn_row)
        
        self.ollama_group.setLayout(ollama_layout)
        layout.addWidget(self.ollama_group)
        
        # === STEP 2: Hardware & Model Selection ===
        self.model_group = QGroupBox("Step 2: Select Model")
        model_layout = QVBoxLayout()
        
        self.specs_label = QLabel("Detecting hardware...")
        model_layout.addWidget(self.specs_label)
        
        model_row = QHBoxLayout()
        model_row.addWidget(QLabel("Model:"))
        
        self.model_combo = QComboBox()
        self.model_combo.setMinimumWidth(350)
        self.model_combo.currentIndexChanged.connect(self.on_model_selected)
        model_row.addWidget(self.model_combo)
        model_row.addStretch()
        model_layout.addLayout(model_row)
        
        self.model_info_label = QLabel("")
        self.model_info_label.setWordWrap(True)
        self.model_info_label.setStyleSheet("color: #666; padding: 5px;")
        model_layout.addWidget(self.model_info_label)
        
        # Download button and progress
        download_row = QHBoxLayout()
        self.download_btn = QPushButton("📦 Download Selected Model")
        self.download_btn.clicked.connect(self.download_model)
        download_row.addWidget(self.download_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.cancel_download)
        self.cancel_btn.setVisible(False)
        download_row.addWidget(self.cancel_btn)
        
        download_row.addStretch()
        model_layout.addLayout(download_row)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        model_layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet("color: #666;")
        model_layout.addWidget(self.progress_label)
        
        self.model_group.setLayout(model_layout)
        layout.addWidget(self.model_group)
        
        # === STEP 3: Test Connection ===
        self.test_group = QGroupBox("Step 3: Test Connection")
        test_layout = QVBoxLayout()
        
        self.test_btn = QPushButton("🧪 Test Translation")
        self.test_btn.clicked.connect(self.test_connection)
        self.test_btn.setToolTip("Send a test translation to verify everything works")
        test_layout.addWidget(self.test_btn)
        
        self.test_result = QTextEdit()
        self.test_result.setMaximumHeight(100)
        self.test_result.setReadOnly(True)
        self.test_result.setPlaceholderText("Test results will appear here...")
        test_layout.addWidget(self.test_result)
        
        self.test_group.setLayout(test_layout)
        layout.addWidget(self.test_group)
        
        # === Bottom buttons ===
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.close_btn)
        
        layout.addLayout(btn_layout)
        
        # Initial state
        self.model_group.setEnabled(False)
        self.test_group.setEnabled(False)
    
    def refresh_status(self):
        """Refresh Ollama status and hardware specs."""
        # Check Ollama
        status = check_ollama_status()
        
        if status['running']:
            models_str = ", ".join(status['models'][:5]) if status['models'] else "None"
            if len(status['models']) > 5:
                models_str += f" (+{len(status['models']) - 5} more)"
            
            version_str = f" v{status['version']}" if status['version'] else ""
            
            self.status_label.setText(
                f"✅ Ollama is running{version_str}\n"
                f"📍 Endpoint: {status['endpoint']}\n"
                f"📦 Installed models: {models_str}"
            )
            self.status_label.setStyleSheet("padding: 10px; background-color: #E8F5E9; border-radius: 5px;")
            self.install_btn.setVisible(False)
            self.model_group.setEnabled(True)
            self.test_group.setEnabled(True)
            
            # Store installed models for later
            self.installed_models = status['models']
        else:
            self.status_label.setText(
                f"❌ Ollama is not running\n"
                f"Error: {status['error']}\n\n"
                "Please install and start Ollama to use local LLM translation."
            )
            self.status_label.setStyleSheet("padding: 10px; background-color: #FFEBEE; border-radius: 5px;")
            self.install_btn.setVisible(True)
            self.model_group.setEnabled(False)
            self.test_group.setEnabled(False)
            self.installed_models = []
        
        # Detect hardware
        specs = detect_system_specs()
        gpu_str = f", GPU: {specs['gpu_name']} ({specs['gpu_vram_gb']}GB)" if specs['gpu_name'] else ""
        self.specs_label.setText(
            f"💻 Your system: {specs['ram_gb']:.0f} GB RAM{gpu_str}"
        )
        
        # Populate model combo
        self.model_combo.clear()
        recommendations = get_model_recommendations(specs['ram_gb'])
        
        for model in recommendations:
            stars = "★" * model['quality_stars'] + "☆" * (5 - model['quality_stars'])
            
            # Mark if already installed
            installed_marker = " ✓" if model['id'] in self.installed_models else ""
            
            # Mark if not compatible
            if not model['compatible']:
                label = f"⚠️ {model['name']} ({model['download_size']}) - Needs {model['ram_required_gb']}GB RAM"
            elif model.get('recommended'):
                label = f"⭐ {model['name']} ({model['download_size']}) {stars}{installed_marker} - RECOMMENDED"
            else:
                label = f"{model['name']} ({model['download_size']}) {stars}{installed_marker}"
            
            self.model_combo.addItem(label, model['id'])
        
        # Select recommended model
        for i in range(self.model_combo.count()):
            model_id = self.model_combo.itemData(i)
            if model_id == specs['recommended_model']:
                self.model_combo.setCurrentIndex(i)
                break
    
    def on_model_selected(self, index):
        """Update model info when selection changes."""
        if index < 0:
            return
        
        model_id = self.model_combo.itemData(index)
        if model_id and model_id in RECOMMENDED_MODELS:
            info = RECOMMENDED_MODELS[model_id]
            self.model_info_label.setText(
                f"<b>{info['description']}</b><br>"
                f"Best for: {info['use_case']}<br>"
                f"Strengths: {', '.join(info['strengths'])}"
            )
            
            # Update download button
            if model_id in getattr(self, 'installed_models', []):
                self.download_btn.setText("✓ Already Installed")
                self.download_btn.setEnabled(False)
            else:
                self.download_btn.setText(f"📦 Download {info['name']} ({info['download_size']})")
                self.download_btn.setEnabled(True)
    
    def open_ollama_download(self):
        """Open Ollama download page."""
        webbrowser.open("https://ollama.com/download")
        QMessageBox.information(
            self,
            "Install Ollama",
            "The Ollama download page has been opened in your browser.\n\n"
            "After installation:\n"
            "1. Ollama should start automatically\n"
            "2. Click 'Refresh Status' to check\n"
            "3. If not running, open a terminal and run: ollama serve"
        )
    
    def start_ollama(self):
        """Start the Ollama service."""
        import subprocess
        import time
        
        # Common locations for Ollama on Windows
        ollama_paths = [
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama.exe"),
            os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Ollama\Ollama.lnk"),
            r"C:\Program Files\Ollama\ollama.exe",
        ]
        
        # Also check for the Start Menu shortcut
        start_menu_lnk = os.path.expandvars(
            r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Ollama\Ollama.lnk"
        )
        
        started = False
        
        # Try the Start Menu shortcut first (most reliable on Windows)
        if os.path.exists(start_menu_lnk):
            try:
                os.startfile(start_menu_lnk)
                started = True
                self.status_label.setText("⏳ Starting Ollama... please wait")
                self.status_label.setStyleSheet("background-color: #FFF3CD; padding: 10px;")
                QApplication.processEvents()
            except Exception as e:
                print(f"Failed to start via shortcut: {e}")
        
        # Try direct executable paths
        if not started:
            for path in ollama_paths:
                if os.path.exists(path) and path.endswith('.exe'):
                    try:
                        subprocess.Popen([path, "serve"], 
                                       creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0)
                        started = True
                        self.status_label.setText("⏳ Starting Ollama... please wait")
                        self.status_label.setStyleSheet("background-color: #FFF3CD; padding: 10px;")
                        QApplication.processEvents()
                        break
                    except Exception as e:
                        print(f"Failed to start {path}: {e}")
        
        if started:
            # Wait a moment for Ollama to start, then refresh
            QTimer.singleShot(3000, self.refresh_status)  # Check after 3 seconds
            QMessageBox.information(
                self,
                "Starting Ollama",
                "Ollama is starting...\n\n"
                "The status will refresh automatically in a few seconds.\n"
                "If it doesn't start, try opening Ollama from your Start Menu."
            )
        else:
            QMessageBox.warning(
                self,
                "Ollama Not Found",
                "Could not find Ollama installation.\n\n"
                "Please either:\n"
                "1. Open Ollama from your Start Menu manually\n"
                "2. Download and install Ollama from https://ollama.com\n\n"
                "After starting Ollama, click 'Refresh Status'."
            )

    def download_model(self):
        """Start downloading the selected model."""
        model_id = self.model_combo.currentData()
        if not model_id:
            return
        
        self.progress_bar.setVisible(True)
        self.progress_label.setText("Starting download...")
        self.download_btn.setEnabled(False)
        self.cancel_btn.setVisible(True)
        self.model_combo.setEnabled(False)
        
        self.download_worker = ModelDownloadWorker(model_id)
        self.download_worker.progress.connect(self.on_download_progress)
        self.download_worker.finished.connect(self.on_download_finished)
        self.download_worker.start()
    
    def cancel_download(self):
        """Cancel ongoing download."""
        if self.download_worker:
            self.download_worker.cancel()
    
    def on_download_progress(self, message):
        """Update download progress."""
        self.progress_label.setText(message)
    
    def on_download_finished(self, success, message):
        """Handle download completion."""
        self.progress_bar.setVisible(False)
        self.cancel_btn.setVisible(False)
        self.model_combo.setEnabled(True)
        
        if success:
            self.progress_label.setText(f"✅ {message}")
            self.progress_label.setStyleSheet("color: green;")
            self.refresh_status()  # Refresh to show new model
        else:
            self.progress_label.setText(f"❌ {message}")
            self.progress_label.setStyleSheet("color: red;")
            self.download_btn.setEnabled(True)
        
        self.download_worker = None
    
    def test_connection(self):
        """Test the selected model with a simple translation."""
        model_id = self.model_combo.currentData()
        if not model_id:
            return
        
        # Check if model is installed
        if model_id not in getattr(self, 'installed_models', []):
            self.test_result.setText("⚠️ Please download the model first")
            return
        
        self.test_btn.setEnabled(False)
        self.test_result.setText("🔄 Testing... (first load may take 30-60 seconds)")
        
        self.test_worker = ConnectionTestWorker(model_id)
        self.test_worker.progress.connect(lambda msg: self.test_result.setText(f"🔄 {msg}"))
        self.test_worker.finished.connect(self.on_test_finished)
        self.test_worker.start()
    
    def on_test_finished(self, success, message, response):
        """Handle test completion."""
        self.test_btn.setEnabled(True)
        
        if success:
            self.test_result.setText(
                f"✅ {message}\n\n"
                f"Test prompt: \"Translate to Dutch: Hello, how are you today?\"\n"
                f"Response: {response}"
            )
            self.test_result.setStyleSheet("background-color: #E8F5E9;")
        else:
            self.test_result.setText(f"❌ {message}")
            self.test_result.setStyleSheet("background-color: #FFEBEE;")
        
        self.test_worker = None
    
    def closeEvent(self, event):
        """Handle dialog close - cancel any running workers."""
        if self.download_worker and self.download_worker.isRunning():
            self.download_worker.cancel()
            self.download_worker.wait()
        
        if self.test_worker and self.test_worker.isRunning():
            self.test_worker.wait()
        
        super().closeEvent(event)


# =============================================================================
# COMPACT STATUS WIDGET (for embedding in settings)
# =============================================================================

class LocalLLMStatusWidget(QWidget):
    """
    Compact status widget for embedding in settings panel.
    Shows Ollama status and provides quick access to setup.
    """
    
    model_changed = pyqtSignal(str)  # Emitted when user selects a model
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.refresh_status()
    
    def init_ui(self):
        """Initialize the compact UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Status row
        status_row = QHBoxLayout()
        
        self.status_icon = QLabel("⏳")
        status_row.addWidget(self.status_icon)
        
        self.status_text = QLabel("Checking...")
        status_row.addWidget(self.status_text, 1)
        
        self.setup_btn = QPushButton("Setup...")
        self.setup_btn.setMaximumWidth(80)
        self.setup_btn.clicked.connect(self.show_setup_dialog)
        status_row.addWidget(self.setup_btn)
        
        layout.addLayout(status_row)
        
        # Model selection row
        model_row = QHBoxLayout()
        model_row.addWidget(QLabel("Model:"))
        
        self.model_combo = QComboBox()
        self.model_combo.setMinimumWidth(250)
        self.model_combo.currentIndexChanged.connect(self.on_model_changed)
        model_row.addWidget(self.model_combo, 1)
        
        self.refresh_btn = QPushButton("🔄")
        self.refresh_btn.setMaximumWidth(40)
        self.refresh_btn.setToolTip("Refresh status")
        self.refresh_btn.clicked.connect(self.refresh_status)
        model_row.addWidget(self.refresh_btn)
        
        layout.addLayout(model_row)
        
        # Info label
        self.info_label = QLabel("")
        self.info_label.setStyleSheet("color: #666; font-size: 9pt;")
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)
    
    def refresh_status(self):
        """Refresh Ollama status."""
        status = check_ollama_status()
        
        if status['running']:
            self.status_icon.setText("✅")
            self.status_text.setText(f"Ollama running ({len(status['models'])} models)")
            self.status_text.setStyleSheet("color: green;")
            self.model_combo.setEnabled(True)
            
            # Populate model combo with installed models
            current = self.model_combo.currentData()
            self.model_combo.clear()
            
            for model in status['models']:
                # Get friendly name if available
                base_model = model.split(':')[0] + ':' + model.split(':')[1] if ':' in model else model
                info = RECOMMENDED_MODELS.get(base_model, {})
                name = info.get('name', model)
                stars = "★" * info.get('quality_stars', 3) if info else ""
                
                self.model_combo.addItem(f"{name} {stars}", model)
            
            # Restore selection
            if current:
                for i in range(self.model_combo.count()):
                    if self.model_combo.itemData(i) == current:
                        self.model_combo.setCurrentIndex(i)
                        break
            
            self.info_label.setText("🔒 Local LLM: No API costs, complete privacy, works offline")
        else:
            self.status_icon.setText("❌")
            self.status_text.setText("Ollama not running")
            self.status_text.setStyleSheet("color: red;")
            self.model_combo.setEnabled(False)
            self.model_combo.clear()
            self.info_label.setText("Click 'Setup...' to install and configure Ollama")
    
    def on_model_changed(self, index):
        """Emit signal when model selection changes."""
        if index >= 0:
            model_id = self.model_combo.itemData(index)
            if model_id:
                self.model_changed.emit(model_id)
    
    def show_setup_dialog(self):
        """Show the full setup dialog."""
        dialog = LocalLLMSetupDialog(self)
        dialog.exec()
        self.refresh_status()
    
    def get_selected_model(self) -> Optional[str]:
        """Get currently selected model ID."""
        return self.model_combo.currentData()
    
    def set_selected_model(self, model_id: str):
        """Set the selected model."""
        for i in range(self.model_combo.count()):
            if self.model_combo.itemData(i) == model_id:
                self.model_combo.setCurrentIndex(i)
                return


# =============================================================================
# STANDALONE TEST
# =============================================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Test status check
    print("Checking Ollama status...")
    status = check_ollama_status()
    print(f"Running: {status['running']}")
    print(f"Models: {status['models']}")
    print(f"Error: {status['error']}")
    
    # Test hardware detection
    print("\nDetecting hardware...")
    specs = detect_system_specs()
    print(f"RAM: {specs['ram_gb']} GB")
    print(f"GPU: {specs['gpu_name']}")
    print(f"Recommended model: {specs['recommended_model']}")
    
    # Show dialog
    dialog = LocalLLMSetupDialog()
    dialog.exec()
