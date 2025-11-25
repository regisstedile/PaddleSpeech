#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Batch English Audio Transcription - Whisper
===========================================

Processes all English audio files in batches with progress tracking.
"""

import os
import sys
import glob
import subprocess
import time
import json
from pathlib import Path

def load_progress():
    """Load progress from file."""
    progress_file = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/transcription_progress.json"
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            return json.load(f)
    return {"completed": [], "failed": []}

def save_progress(progress):
    """Save progress to file."""
    progress_file = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/transcription_progress.json"
    with open(progress_file, 'w') as f:
        json.dump(progress, f, indent=2)

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

def transcribe_file(audio_file, output_dir, model="base"):
    """Transcribe a single audio file using Whisper."""
    filename = Path(audio_file).stem
    
    print(f"\n🎵 Processing: {filename}")
    
    try:
        cmd = [
            sys.executable, '-m', 'whisper', audio_file,
            '--language', 'en',
            '--model', model,
            '--output_dir', output_dir,
            '--output_format', 'txt',
            '--output_format', 'srt',
            '--fp16', 'False',
            '--verbose', 'False'  # Less verbose for batch processing
        ]
        
        print(f"⚙️  Running Whisper (model: {model})...")
        start_time = time.time()
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ Completed in {duration:.1f} seconds")
            return True
        else:
            print(f"❌ Failed: {result.stderr[:200]}...")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout (30 minutes exceeded)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main batch processing."""
    print("🎙️  Batch English Audio Transcription")
    print("=" * 50)
    
    # Load previous progress
    progress = load_progress()
    
    # Get all audio files
    audio_files = get_audio_files()
    if not audio_files:
        print("❌ No audio files found")
        return
    
    # Filter out already completed files
    remaining_files = [f for f in audio_files if f not in progress["completed"] and f not in progress["failed"]]
    
    print(f"📁 Total files: {len(audio_files)}")
    print(f"✅ Already completed: {len(progress['completed'])}")
    print(f"❌ Previously failed: {len(progress['failed'])}")
    print(f"📋 Remaining to process: {len(remaining_files)}")
    
    if not remaining_files:
        print("🎉 All files already processed!")
        return
    
    # Create output directory
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    os.makedirs(output_dir, exist_ok=True)
    
    # Process files
    for i, audio_file in enumerate(remaining_files, 1):
        print(f"\n📋 Progress: {i}/{len(remaining_files)} (Total completed: {len(progress['completed'])})")
        
        if transcribe_file(audio_file, output_dir):
            progress["completed"].append(audio_file)
        else:
            progress["failed"].append(audio_file)
        
        # Save progress after each file
        save_progress(progress)
        
        # Brief pause between files
        time.sleep(2)
    
    # Final summary
    print(f"\n📊 FINAL SUMMARY")
    print("=" * 30)
    print(f"✅ Successfully completed: {len(progress['completed'])}")
    print(f"❌ Failed: {len(progress['failed'])}")
    print(f"📁 Total files: {len(audio_files)}")
    
    if progress["failed"]:
        print(f"\n❌ Failed files:")
        for f in progress["failed"]:
            print(f"   - {Path(f).name}")

if __name__ == "__main__":
    main()