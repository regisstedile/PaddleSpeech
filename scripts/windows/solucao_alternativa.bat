@echo off
title Solucao Alternativa - Whisper CPU

echo Solucao Alternativa - Whisper CPU Only
echo ========================================

cd /d "C:\Users\Admin\Videos\1-PaddleSpeech"

echo Instalando versoes especificas compateis...

pip uninstall torch torchvision torchaudio -y
pip uninstall openai-whisper -y

echo Instalando PyTorch CPU only (compativel)...
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cpu

echo Instalando Whisper...
pip install openai-whisper==20230314

echo Testando...
python -c "import torch; print('PyTorch:', torch.__version__)"
python -c "import whisper; print('Whisper funcionando!')"

if %errorlevel% equ 0 (
    echo.
    echo Processando com versoes estables...
    whisper "INPUT\Tramplin - Deep House Lost. Act .mp3" --language ru --model tiny --output_dir OUTPUT
    
    if %errorlevel% equ 0 (
        echo SUCESSO!
        type "OUTPUT\Tramplin - Deep House Lost. Act .txt" 2>nul
    )
) else (
    echo Ainda com problema...
)

pause