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
    """Extract version from Supervertaler_v3.7.7.py"""
    try:
        with open("Supervertaler_v3.7.7.py", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("APP_VERSION"):
                    return line.split("=")[1].strip().strip('"')
    except FileNotFoundError:
        pass
    return "3.7.4"

setup(
    name="Supervertaler",
    version=get_version(),
    author="Michael Beijer",
    author_email="info@michaelbeijer.co.uk",
    description="AI-powered context-aware translation tool for professional translators with CAT editor, multi-provider LLM support, and advanced features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michaelbeijer/Supervertaler",
    project_urls={
        "Bug Tracker": "https://github.com/michaelbeijer/Supervertaler/issues",
        "Documentation": "https://github.com/michaelbeijer/Supervertaler#readme",
        "Source Code": "https://github.com/michaelbeijer/Supervertaler",
        "Author Website": "https://michaelbeijer.co.uk",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "Topic :: Text Processing :: Linguistic",
        "Environment :: X11 :: Tk",
    ],
    python_requires=">=3.12",
    install_requires=[
        "python-docx>=0.8.11",
        "openpyxl>=3.1.0",
        "Pillow>=10.0.0",
        "openai>=1.0.0",
        "anthropic>=0.7.0",
        "google-generativeai>=0.3.0",
    ],
    entry_points={
        "console_scripts": [
            "supervertaler=Supervertaler_v3.7.3:main",
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
        "translation-memory",
        "localization",
        "DOCX",
        "memoQ",
        "CafeTran",
    ],
    zip_safe=False,
)
