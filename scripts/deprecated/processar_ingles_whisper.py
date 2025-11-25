#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
English Audio Transcription Tool - Whisper
==========================================

This script processes English audio files from the INPUT folder using OpenAI Whisper.
Optimized for Pluralsight and career development audio content.

Dependencies:
- openai-whisper
- python 3.8+
"""

import os
import sys
import glob
import subprocess
import time
from pathlib import Path

def check_whisper_installation():
    """Check if Whisper is installed and install if needed."""
    try:
        result = subprocess.run([sys.executable, '-m', 'whisper', '--help'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Whisper already installed and working")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        pass
    
    print("⚠️  Installing Whisper...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'openai-whisper'], 
                      check=True, timeout=300)
        print("✅ Whisper installed successfully")
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"❌ Failed to install Whisper: {e}")
        return False

def get_audio_files():
    """Get list of audio files to process."""
    input_dirs = [
        "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/INPUT/",
        "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/PaddleSpeech/INPUT/"
    ]
    
    audio_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg']
    audio_files = []
    
    for input_dir in input_dirs:
        if os.path.exists(input_dir):
            for ext in audio_extensions:
                files = glob.glob(f"{input_dir}*{ext}")
                audio_files.extend(files)
    
    return audio_files

def create_output_dir():
    """Create output directory if it doesn't exist."""
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def transcribe_file(audio_file, output_dir, model="base"):
    """Transcribe a single audio file using Whisper."""
    filename = Path(audio_file).stem
    
    print(f"\n🎵 Processing: {filename}")
    print(f"   File: {audio_file}")
    
    try:
        # Use Whisper Python module with optimized settings for English
        cmd = [
            sys.executable, '-m', 'whisper', audio_file,
            '--language', 'en',
            '--model', model,
            '--output_dir', output_dir,
            '--output_format', 'txt',
            '--output_format', 'srt',
            '--fp16', 'False',  # Better compatibility
            '--verbose', 'True'
        ]
        
        print(f"⚙️  Running Whisper (model: {model})...")
        start_time = time.time()
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)  # 30 min timeout
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ Transcription completed in {duration:.1f} seconds")
            
            # Check if output files were created
            txt_file = os.path.join(output_dir, f"{filename}.txt")
            srt_file = os.path.join(output_dir, f"{filename}.srt")
            
            if os.path.exists(txt_file):
                print(f"   📝 Text file: {txt_file}")
            if os.path.exists(srt_file):
                print(f"   🎬 SRT file: {srt_file}")
                
            return True
        else:
            print(f"❌ Transcription failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ Transcription timeout (30 minutes exceeded)")
        return False
    except Exception as e:
        print(f"❌ Error processing {filename}: {e}")
        return False

def main():
    """Main transcription process."""
    print("🎙️  English Audio Transcription Tool")
    print("=" * 50)
    
    # Check Whisper installation
    if not check_whisper_installation():
        print("❌ Cannot proceed without Whisper. Please install manually.")
        return
    
    # Get audio files
    audio_files = get_audio_files()
    if not audio_files:
        print("❌ No audio files found in INPUT directories")
        return
    
    print(f"\n📁 Found {len(audio_files)} audio files to process")
    
    # Create output directory
    output_dir = create_output_dir()
    print(f"📂 Output directory: {output_dir}")
    
    # Process each file
    successful = 0
    failed = 0
    
    # Use smaller model for faster processing, can be changed to 'small', 'medium', 'large'
    model = "base"
    
    for i, audio_file in enumerate(audio_files, 1):
        print(f"\n📋 Progress: {i}/{len(audio_files)}")
        
        if transcribe_file(audio_file, output_dir, model):
            successful += 1
        else:
            failed += 1
            
        # Brief pause between files
        time.sleep(1)
    
    # Summary
    print(f"\n📊 TRANSCRIPTION SUMMARY")
    print("=" * 30)
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Total files: {len(audio_files)}")
    print(f"📂 Output location: {output_dir}")
    
    if successful > 0:
        print(f"\n🎉 Transcription completed! Check the OUTPUT folder for results.")

if __name__ == "__main__":
    main()