@echo off
chcp 65001 >nul
title Processador de Áudio Russo - VERSÃO CORRIGIDA

echo 🇷🇺 Processador de Áudio Russo - VERSÃO CORRIGIDA
echo ==================================================

cd /d "C:\Users\Admin\Videos\1-PaddleSpeech"

:: Verificar se o arquivo existe
if not exist "INPUT\Tramplin - Deep House Lost. Act .mp3" (
    echo ❌ Arquivo não encontrado na pasta INPUT
    echo 📁 Verificando na pasta PaddleSpeech\INPUT...
    
    if exist "PaddleSpeech\INPUT\Tramplin - Deep House Lost. Act .mp3" (
        echo ✅ Arquivo encontrado em PaddleSpeech\INPUT
        echo 📋 Copiando para INPUT principal...
        copy "PaddleSpeech\INPUT\Tramplin - Deep House Lost. Act .mp3" "INPUT\" >nul
    ) else (
        echo ❌ Arquivo não encontrado em nenhuma pasta
        pause
        exit /b 1
    )
)

:: Criar pasta OUTPUT se não existir
if not exist "OUTPUT" mkdir OUTPUT

echo ✅ Arquivo encontrado: Tramplin - Deep House Lost. Act .mp3
echo 📊 Preparando processamento...
echo.

:: Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado
    echo 💡 Instale Python de python.org ou Microsoft Store
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

:: Criar ambiente virtual se não existir
if not exist "whisper_russo_env" (
    echo 🔧 Criando ambiente virtual...
    python -m venv whisper_russo_env
)

:: Ativar ambiente
echo ⚡ Ativando ambiente...
call whisper_russo_env\Scripts\activate.bat

:: Verificar se Whisper está instalado
python -c "import whisper" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Instalando OpenAI Whisper...
    pip install openai-whisper --quiet --no-warn-script-location
    
    if %errorlevel% neq 0 (
        echo ❌ Erro na instalação do Whisper
        pause
        exit /b 1
    )
)

echo ✅ Whisper está pronto
echo.

:: Processar arquivo - USAR ASPAS CORRETAS E CAMINHO ABSOLUTO
echo 🚀 Iniciando processamento do áudio russo...
echo ⏳ Isso pode demorar 5-15 minutos...
echo 📝 Processando com modelo 'base' para melhor qualidade...
echo.

:: Usar caminho completo e aspas para evitar problemas
set "INPUT_FILE=C:\Users\Admin\Videos\1-PaddleSpeech\INPUT\Tramplin - Deep House Lost. Act .mp3"
set "OUTPUT_DIR=C:\Users\Admin\Videos\1-PaddleSpeech\OUTPUT"

whisper "%INPUT_FILE%" --language russian --model base --output_dir "%OUTPUT_DIR%" --output_format txt --verbose True

if %errorlevel% equ 0 (
    echo.
    echo ✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!
    echo.
    echo 📁 Arquivos gerados em OUTPUT:
    dir "OUTPUT\Tramplin*.txt" 2>nul
    echo.
    
    :: Mostrar primeiras linhas do resultado
    echo 📋 Primeiras linhas da transcrição:
    echo ==========================================
    for %%f in ("OUTPUT\Tramplin*.txt") do (
        echo Arquivo: %%~nxf
        type "%%f" 2>nul | more +0
        echo.
    )
    echo ==========================================
    
    echo 🎉 Transcrição em russo concluída!
    echo 📄 Arquivo completo disponível na pasta OUTPUT
    
) else (
    echo.
    echo ❌ ERRO NO PROCESSAMENTO
    echo.
    echo 🔧 Tentativas de solução:
    echo 1. Verificar se o arquivo não está corrompido
    echo 2. Tentar novamente com modelo menor:
    echo    whisper "arquivo.mp3" --language ru --model tiny
    echo 3. Converter arquivo para WAV primeiro
    echo 4. Usar serviços online como AssemblyAI
)

echo.
echo ⏸️ Pressione qualquer tecla para fechar...
pause >nul