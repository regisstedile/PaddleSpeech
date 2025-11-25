@echo off
chcp 65001 >nul
title Teste Simples - Whisper Russo

echo 🧪 Teste Simples - Whisper para Russo
echo =====================================

cd /d "C:\Users\Admin\Videos\1-PaddleSpeech"

:: Mostrar onde estamos
echo 📍 Diretório atual: %CD%
echo.

:: Listar arquivos MP3
echo 📁 Procurando arquivos MP3...
echo.
echo INPUT principal:
dir "INPUT\*.mp3" 2>nul
echo.
echo PaddleSpeech\INPUT:
dir "PaddleSpeech\INPUT\*.mp3" 2>nul
echo.

:: Verificar Python
echo 🐍 Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado
    goto :end
)

:: Testar importação básica
echo 📦 Testando importações...
python -c "print('✅ Python funcionando')"

:: Tentar instalar whisper temporariamente
echo 🎙️ Testando Whisper...
pip install openai-whisper --quiet --user
python -c "import whisper; print('✅ Whisper disponível')" 2>nul
if %errorlevel% equ 0 (
    echo 🎯 Whisper está funcionando!
    
    :: Se tudo estiver OK, processar arquivo pequeno primeiro
    echo.
    echo 💡 Para processar seu arquivo russo, use:
    echo whisper "caminho\completo\do\arquivo.mp3" --language ru --output_dir OUTPUT
    echo.
    echo 📝 Comando específico para seu arquivo:
    echo whisper "INPUT\Tramplin - Deep House Lost. Act .mp3" --language russian --output_dir OUTPUT
    
) else (
    echo ❌ Problema com Whisper
)

:end
echo.
echo Pressione qualquer tecla para continuar...
pause >nul