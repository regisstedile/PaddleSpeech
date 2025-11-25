#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test Single File Transcription
"""

import os
import sys
import subprocess
import time

def transcribe_single_file():
    """Test transcribing a single file."""
    
    # Test with the first Pluralsight file
    audio_file = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/PaddleSpeech/INPUT/Pluralsight - Accountability in 5 Steps.mp3"
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🎵 Testing transcription of: {os.path.basename(audio_file)}")
    
    # Check if file exists
    if not os.path.exists(audio_file):
        print(f"❌ File not found: {audio_file}")
        return False
    
    try:
        # Use Whisper Python module
        cmd = [
            sys.executable, '-m', 'whisper', audio_file,
            '--language', 'en',
            '--model', 'base',
            '--output_dir', output_dir,
            '--output_format', 'txt',
            '--output_format', 'srt',
            '--fp16', 'False',
            '--verbose', 'True'
        ]
        
        print("⚙️  Running Whisper...")
        print(f"Command: {' '.join(cmd)}")
        
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        end_time = time.time()
        
        print(f"Return code: {result.returncode}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        
        if result.returncode == 0:
            duration = end_time - start_time
            print(f"✅ Transcription completed in {duration:.1f} seconds")
            return True
        else:
            print(f"❌ Transcription failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    transcribe_single_file()