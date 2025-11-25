@echo off
chcp 65001
echo 🎙️  English Audio Transcription - Command Line Tool
echo ==================================================
echo.

cd /d "C:\Users\Admin\Videos\1-PaddleSpeech"

echo ⚙️  Processing English audio files with Whisper...
echo.

REM Process individual files manually to control better
python -m whisper "PaddleSpeech\INPUT\Pluralsight - Becoming a Better Listener.mp3" --language en --model base --output_dir OUTPUT --output_format txt --output_format srt

python -m whisper "PaddleSpeech\INPUT\Pluralsight - Becoming a Better Negotiator.mp3" --language en --model base --output_dir OUTPUT --output_format txt --output_format srt

python -m whisper "PaddleSpeech\INPUT\Pluralsight - Becoming a Better Presenter.mp3" --language en --model base --output_dir OUTPUT --output_format txt --output_format srt

python -m whisper "PaddleSpeech\INPUT\Pluralsight - Career Management 2.0.mp3" --language en --model base --output_dir OUTPUT --output_format txt --output_format srt

python -m whisper "PaddleSpeech\INPUT\Pluralsight - Creating a Culture of Motivation at Work.mp3" --language en --model base --output_dir OUTPUT --output_format txt --output_format srt

echo.
echo ✅ Batch processing completed!
echo 📂 Check the OUTPUT folder for transcription results
echo.
pause