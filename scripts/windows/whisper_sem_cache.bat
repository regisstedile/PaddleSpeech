@echo off
title Whisper sem Cache - Contorna Permissoes

echo Whisper sem Cache - Contorna Permissoes
echo =========================================

cd /d "C:\Users\Admin\Videos\1-PaddleSpeech"

echo Criando ambiente limpo...
if exist "whisper_nocache" rmdir /s /q "whisper_nocache"
python -m venv whisper_nocache

echo Ativando ambiente...
call whisper_nocache\Scripts\activate.bat

echo Instalando sem cache (contorna permissoes)...
pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

echo Instalando Whisper sem cache...
pip install --no-cache-dir openai-whisper

echo Testando instalacao...
python -c "import whisper; print('Whisper funcionando!')"

if %errorlevel% equ 0 (
    echo.
    echo SUCESSO: Whisper instalado!
    echo.
    echo Processando audio russo (pode demorar 10-20 minutos)...
    echo.
    
    whisper "INPUT\Tramplin - Deep House Lost. Act .mp3" --language russian --model tiny --output_dir OUTPUT --output_format txt
    
    if %errorlevel% equ 0 (
        echo.
        echo SUCESSO: Audio processado!
        echo.
        echo Resultado:
        echo ==========================================
        type "OUTPUT\Tramplin - Deep House Lost. Act .txt" 2>nul
        echo ==========================================
        echo.
        echo Arquivo salvo em: OUTPUT\Tramplin - Deep House Lost. Act .txt
    ) else (
        echo ERRO: Falha no processamento
    )
) else (
    echo ERRO: Ainda com problemas de instalacao
    echo.
    echo Tentando solucao manual...
    echo Execute como Administrador ou:
    echo 1. Clique direito no Prompt
    echo 2. Executar como Administrador
    echo 3. Execute este script novamente
)

echo.
pause