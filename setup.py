#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audio Transcription System
Setup configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

setup(
    name="audio-transcription",
    version="1.0.0",
    description="Audio transcription system using OpenAI Whisper with SRT subtitle generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Audio Transcription Team",
    python_requires=">=3.8",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "openai-whisper>=20230314",
        "torch>=2.0.0",
        "torchaudio>=2.0.0",
        "ffmpeg-python>=0.2.0",
        "pydub>=0.25.1",
        "tqdm>=4.65.0",
        "numpy>=1.24.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "translation": [
            "deep-translator>=1.11.4",
        ],
    },
    entry_points={
        "console_scripts": [
            "transcribe=transcribe:main",
            "translate-subs=translate:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
