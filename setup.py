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
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "Topic :: Text Processing :: Linguistic",
        "Environment :: X11 Applications :: Qt",
    ],
    python_requires=">=3.10",
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
