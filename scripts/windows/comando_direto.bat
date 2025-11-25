@echo off
cd /d "C:\Users\Admin\Videos\1-PaddleSpeech"
pip install openai-whisper
whisper "INPUT\Tramplin - Deep House Lost. Act .mp3" --language russian --output_dir OUTPUT
pause