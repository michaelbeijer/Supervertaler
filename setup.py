#!/usr/bin/env python
"""
Setup configuration for Supervertaler - AI-powered context-aware translation tool

This script configures Supervertaler for distribution via PyPI.
Install with: pip install Supervertaler
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
    return "1.6.0"

setup(
    name="Supervertaler",
    version=get_version(),
    author="Michael Beijer",
    author_email="info@michaelbeijer.co.uk",
    description="Professional AI-powered CAT tool with complete termbase system, voice dictation, and modern PyQt6 interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://michaelbeijer.github.io/Supervertaler",
    project_urls={
        "Bug Tracker": "https://github.com/michaelbeijer/Supervertaler/issues",
        "Documentation": "https://github.com/michaelbeijer/Supervertaler/blob/main/docs/PROJECT_CONTEXT.md",
        "Source Code": "https://github.com/michaelbeijer/Supervertaler",
        "Changelog": "https://github.com/michaelbeijer/Supervertaler/blob/main/CHANGELOG.md",
        "Author Website": "https://michaelbeijer.co.uk",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "Topic :: Text Processing :: Linguistic",
        "Environment :: X11 Applications :: Qt",
    ],
    python_requires=">=3.12",
    install_requires=[
        "PyQt6>=6.5.0",
        "python-docx>=0.8.11",
        "openpyxl>=3.1.0",
        "Pillow>=10.0.0",
        "openai>=1.0.0",
        "anthropic>=0.7.0",
        "google-generativeai>=0.3.0",
        "sacrebleu>=2.3.1",
    ],
    entry_points={
        "console_scripts": [
            "supervertaler=Supervertaler:main",
        ],
    },
    include_package_data=True,
    keywords=[
        "translation",
        "CAT",
        "AI",
        "LLM",
        "GPT",
        "Claude",
        "Gemini",
        "termbase",
        "translation-memory",
        "PyQt6",
        "localization",
        "memoQ",
        "Trados",
    ],
    zip_safe=False,
)
