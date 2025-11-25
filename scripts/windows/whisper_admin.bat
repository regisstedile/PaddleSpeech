@echo off
title Whisper como Administrador

:: Verificar se esta rodando como admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Este script precisa ser executado como Administrador
    echo.
    echo Clique direito no arquivo e selecione "Executar como administrador"
    echo Ou abra Prompt como Admin e execute o comando:
    echo cd C:\Users\Admin\Videos\1-PaddleSpeech
    echo pip install --user openai-whisper
    pause
    exit /b 1
)

echo Executando como Administrador - Whisper
echo ========================================

cd /d "C:\Users\Admin\Videos\1-PaddleSpeech"

echo Limpando cache problematico...
pip cache purge

echo Instalando Whisper para usuario (sem problemas de permissao)...
pip install --user --no-cache-dir openai-whisper

echo Testando...
python -c "import whisper; print('Whisper funcionando!')"

if %errorlevel% equ 0 (
    echo SUCESSO!
    echo.
    echo Processando audio russo...
    whisper "INPUT\Tramplin - Deep House Lost. Act .mp3" --language russian --model tiny --output_dir OUTPUT
    
    if %errorlevel% equ 0 (
        echo.
        echo Audio processado com sucesso!
        type "OUTPUT\Tramplin - Deep House Lost. Act .txt" 2>nul
    )
) else (
    echo Ainda com problemas...
)

pause