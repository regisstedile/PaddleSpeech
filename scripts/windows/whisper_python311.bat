@echo off
title Whisper com Python 3.11

echo Solucao: Usar Python 3.11 (mais compativel)
echo ==============================================

cd /d "C:\Users\Admin\Videos\1-PaddleSpeech"

echo Verificando se Python 3.11 esta disponivel...
py -3.11 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python 3.11 encontrado!
    
    echo Criando ambiente com Python 3.11...
    py -3.11 -m venv whisper_py311
    call whisper_py311\Scripts\activate.bat
    
    echo Instalando dependencias...
    python -m pip install --upgrade pip
    pip install openai-whisper
    
    echo Processando audio...
    whisper "INPUT\Tramplin - Deep House Lost. Act .mp3" --language russian --output_dir OUTPUT
    
) else (
    echo Python 3.11 nao encontrado.
    echo.
    echo INSTALANDO Python 3.11...
    echo Por favor, instale Python 3.11 de python.org
    echo.
    echo Ou use este comando:
    echo winget install Python.Python.3.11
    echo.
    echo Depois execute este script novamente.
)

pause