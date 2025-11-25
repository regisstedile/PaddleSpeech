@echo off
title Instalador Whisper Compativel

echo Instalador Whisper Compativel
echo ================================

cd /d "C:\Users\Admin\Videos\1-PaddleSpeech"

echo Criando ambiente virtual limpo...
if exist "whisper_compativel" rmdir /s /q "whisper_compativel"
python -m venv whisper_compativel

echo Ativando ambiente...
call whisper_compativel\Scripts\activate.bat

echo Atualizando pip...
python -m pip install --upgrade pip

echo Instalando PyTorch compativel...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

echo Instalando Whisper...
pip install openai-whisper

echo Testando instalacao...
python -c "import whisper; print('Whisper funcionando!')"

if %errorlevel% equ 0 (
    echo.
    echo SUCESSO: Whisper instalado com sucesso!
    echo.
    echo Processando audio russo...
    echo Isso pode demorar 5-15 minutos...
    echo.
    
    whisper "INPUT\Tramplin - Deep House Lost. Act .mp3" --language russian --model base --output_dir OUTPUT --output_format txt
    
    if %errorlevel% equ 0 (
        echo.
        echo SUCESSO: Audio processado!
        echo Verificando resultado...
        
        if exist "OUTPUT\Tramplin - Deep House Lost. Act .txt" (
            echo.
            echo Transcricao encontrada:
            echo ==========================================
            type "OUTPUT\Tramplin - Deep House Lost. Act .txt"
            echo ==========================================
        )
    ) else (
        echo ERRO: Falha no processamento
    )
) else (
    echo ERRO: Falha na instalacao
)

echo.
pause