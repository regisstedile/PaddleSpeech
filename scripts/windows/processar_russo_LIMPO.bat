@echo off
title Processador de Audio Russo - Whisper

echo Processador de Audio Russo - Whisper
echo ======================================

cd /d "C:\Users\Admin\Videos\1-PaddleSpeech"

echo Verificando arquivo...
if not exist "INPUT\Tramplin - Deep House Lost. Act .mp3" (
    echo ERRO: Arquivo nao encontrado na pasta INPUT
    echo Verificando em PaddleSpeech\INPUT...
    
    if exist "PaddleSpeech\INPUT\Tramplin - Deep House Lost. Act .mp3" (
        echo Arquivo encontrado em PaddleSpeech\INPUT
        echo Copiando para INPUT principal...
        if not exist "INPUT" mkdir INPUT
        copy "PaddleSpeech\INPUT\Tramplin - Deep House Lost. Act .mp3" "INPUT\" >nul
    ) else (
        echo ERRO: Arquivo nao encontrado
        pause
        exit /b 1
    )
)

if not exist "OUTPUT" mkdir OUTPUT

echo OK: Arquivo encontrado
echo.

echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado
    echo Instale Python de python.org
    pause
    exit /b 1
)

echo OK: Python encontrado
echo.

echo Instalando Whisper...
pip install openai-whisper --quiet
if %errorlevel% neq 0 (
    echo ERRO: Falha na instalacao do Whisper
    pause
    exit /b 1
)

echo OK: Whisper instalado
echo.

echo Processando audio russo...
echo Isso pode demorar 5-15 minutos...
echo.

whisper "INPUT\Tramplin - Deep House Lost. Act .mp3" --language russian --model base --output_dir OUTPUT --output_format txt

if %errorlevel% equ 0 (
    echo.
    echo SUCESSO: Processamento concluido!
    echo.
    echo Arquivos gerados:
    dir "OUTPUT\Tramplin*.txt"
    echo.
    echo Conteudo da transcricao:
    echo ==========================================
    type "OUTPUT\Tramplin - Deep House Lost. Act .txt" 2>nul
    echo ==========================================
    echo.
    echo Transcricao em russo concluida!
    
) else (
    echo.
    echo ERRO: Falha no processamento
    echo Tente com modelo menor: --model tiny
)

echo.
pause