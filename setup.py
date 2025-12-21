#!/usr/bin/env python
"""
Setup configuration for Supervertaler - AI-powered translation workbench

This script configures Supervertaler for distribution via PyPI.
Install with: pip install Supervertaler

Note: pyproject.toml is the primary configuration file.
This setup.py exists for compatibility with older pip versions.
"""

from setuptools import setup, find_packages
import os

# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from main module
def get_version():
    """Extract version from Supervertaler.py"""
    try:
        with open("Supervertaler.py", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"')
    except FileNotFoundError:
        pass
    return "1.9.54"

setup(
    name="Supervertaler",
    version=get_version(),
    author="Michael Beijer",
    author_email="info@michaelbeijer.co.uk",
    description="Professional AI-powered translation workbench with multi-LLM support, glossary system, TM, spellcheck, voice commands, and PyQt6 interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://supervertaler.com",
    project_urls={
        "Bug Tracker": "https://github.com/michaelbeijer/Supervertaler/issues",
        "Documentation": "https://github.com/michaelbeijer/Supervertaler/blob/main/AGENTS.md",
        "Source Code": "https://github.com/michaelbeijer/Supervertaler",
        "Changelog": "https://github.com/michaelbeijer/Supervertaler/blob/main/CHANGELOG.md",
        "Author Website": "https://michaelbeijer.co.uk",
    },
    packages=find_packages(include=["modules*"]),
    py_modules=["Supervertaler"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "Topic :: Text Processing :: Linguistic",
        "Environment :: X11 Applications :: Qt",
    ],
    python_requires=">=3.10",
    install_requires=[
        # Core UI Framework
        "PyQt6>=6.5.0",
        "PyQt6-WebEngine>=6.5.0",
        
        # Document Processing
        "python-docx>=0.8.11",
        "openpyxl>=3.1.0",
        "Pillow>=10.0.0",
        "lxml>=4.9.0",
        
        # AI/LLM Providers
        "openai>=1.0.0",
        "anthropic>=0.7.0",
        "google-generativeai>=0.3.0",
        "requests>=2.28.0",
        
        # Document Conversion & Analysis
        "markitdown>=0.0.1",
        
        # Translation Quality Metrics
        "sacrebleu>=2.3.1",
        
        # Clipboard Operations
        "pyperclip>=1.8.2",
        
        # PDF Processing
        "PyMuPDF>=1.23.0",
        
        # Audio Processing
        "numpy>=1.24.0",
        "sounddevice>=0.4.6",
        
        # Semantic Search (Supermemory)
        "sentence-transformers>=2.2.0",
        "chromadb>=0.4.0",
        
        # YAML Support
        "pyyaml>=6.0.0",
        
        # Markdown Rendering
        "markdown>=3.4.0",
        
        # Spellchecking
        "pyspellchecker>=0.7.0",
        
        # Machine Translation APIs
        "boto3>=1.28.0",
        "deepl>=1.15.0",
    ],
    extras_require={
        "voice": [
            "openai-whisper>=20230314",
        ],
        "windows": [
            "keyboard>=0.13.5",
            "ahk>=1.0.0",
            "cyhunspell>=2.0.0",
        ],
        "all": [
            "openai-whisper>=20230314",
            "keyboard>=0.13.5",
            "ahk>=1.0.0",
            "cyhunspell>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "supervertaler=Supervertaler:main",
        ],
    },
    include_package_data=True,
    keywords=[
        "translation",
        "CAT",
        "CAT-tool",
        "AI",
        "LLM",
        "GPT",
        "Claude",
        "Gemini",
        "Ollama",
        "glossary",
        "termbase",
        "translation-memory",
        "TM",
        "PyQt6",
        "localization",
        "memoQ",
        "Trados",
        "SDLPPX",
        "XLIFF",
        "voice-commands",
        "spellcheck",
    ],
    zip_safe=False,
)
