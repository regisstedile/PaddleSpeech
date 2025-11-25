@echo off
chcp 65001 >nul
title Processador de Áudio Russo - Whisper

echo 🇷🇺 Processador de Áudio Russo - Whisper
echo ==========================================

cd /d "C:\Users\Admin\Videos\1-PaddleSpeech"

:: Verificar se o arquivo existe
if not exist "INPUT\Tramplin - Deep House Lost. Act .mp3" (
    echo ❌ Arquivo não encontrado: INPUT\Tramplin - Deep House Lost. Act .mp3
    echo 📁 Copie o arquivo para a pasta INPUT primeiro
    pause
    exit /b 1
)

:: Criar pasta OUTPUT se não existir
if not exist "OUTPUT" mkdir OUTPUT

echo 🎵 Arquivo encontrado: Tramplin - Deep House Lost. Act .mp3
echo 📊 Tamanho: ~283MB
echo 🌍 Idioma: Russo
echo.

:: Verificar se Whisper está instalado
echo 🔍 Verificando instalação do Whisper...

:: Tentar usar ambiente existente
if exist "whisper_russo_env\Scripts\activate.bat" (
    echo ✅ Ambiente Whisper encontrado
    call whisper_russo_env\Scripts\activate.bat
    goto :process
)

:: Tentar usar ambiente PaddleSpeech
if exist "paddlespeech_env\Scripts\activate.bat" (
    echo ⚡ Usando ambiente PaddleSpeech...
    call paddlespeech_env\Scripts\activate.bat
    
    :: Tentar instalar Whisper
    echo 📦 Instalando Whisper...
    pip install openai-whisper --quiet
    goto :process
)

:: Instalar do zero
echo 🔧 Criando novo ambiente...
python -m venv whisper_temp_env
call whisper_temp_env\Scripts\activate.bat
pip install openai-whisper --quiet

:process
echo.
echo 🚀 Iniciando processamento...
echo ⏳ Isso pode demorar alguns minutos (arquivo grande)...
echo.

:: Processar o arquivo
whisper "INPUT\Tramplin - Deep House Lost. Act .mp3" --language russian --model base --output_dir OUTPUT --output_format txt --verbose False

if %errorlevel%==0 (
    echo.
    echo ✅ Processamento concluído com sucesso!
    echo.
    echo 📁 Resultados salvos em:
    echo    - OUTPUT\Tramplin - Deep House Lost. Act .txt
    echo.
    echo 📋 Abrindo resultado...
    
    :: Mostrar conteúdo se o arquivo existe
    if exist "OUTPUT\Tramplin - Deep House Lost. Act .txt" (
        echo ==========================================
        type "OUTPUT\Tramplin - Deep House Lost. Act .txt"
        echo ==========================================
    )
    
    echo.
    echo 🎉 Transcrição em russo concluída!
    
) else (
    echo.
    echo ❌ Erro no processamento
    echo.
    echo 💡 Soluções alternativas:
    echo 1. Verificar se o arquivo não está corrompido
    echo 2. Tentar com modelo menor: --model tiny
    echo 3. Usar serviços online como AssemblyAI
    echo 4. Converter para WAV primeiro
)

echo.
echo Pressione qualquer tecla para continuar...
pause >nul