#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple English Audio Transcription - Process 5 files at a time
"""

import os
import sys
import glob
import subprocess
import time
import json
from pathlib import Path

def get_pluralsight_files():
    """Get Pluralsight files to process."""
    input_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/PaddleSpeech/INPUT/"
    files = glob.glob(f"{input_dir}Pluralsight*.mp3")
    return sorted(files)[:5]  # Process 5 at a time

def transcribe_file(audio_file):
    """Transcribe a single file."""
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    filename = Path(audio_file).stem
    
    print(f"\n🎵 {filename}")
    
    cmd = [
        sys.executable, '-m', 'whisper', audio_file,
        '--language', 'en',
        '--model', 'base',
        '--output_dir', output_dir,
        '--output_format', 'txt',
        '--output_format', 'srt'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)
        return result.returncode == 0
    except:
        return False

def main():
    files = get_pluralsight_files()
    success = 0
    
    for i, file in enumerate(files, 1):
        print(f"\n📋 {i}/{len(files)}")
        if transcribe_file(file):
            success += 1
            print("✅ Success")
        else:
            print("❌ Failed")
    
    print(f"\n📊 Completed: {success}/{len(files)}")

if __name__ == "__main__":
    main()