@echo off

chcp 65001 >nul
echo 🇷🇺 Instalador Whisper para Áudio Russo
echo ========================================

cd /d "C:\Users\Admin\Videos\1-PaddleSpeech"

echo 🔧 Criando ambiente Python limpo...
python -m venv whisper_russo_env

echo ⚡ Ativando ambiente...
call whisper_russo_env\Scripts\activate.bat

echo 📦 Atualizando pip...
python -m pip install --upgrade pip

echo 🎙️ Instalando OpenAI Whisper...
pip install openai-whisper

echo 🧪 Testando instalação...
python -c "import whisper; print('✅ Whisper instalado com sucesso!')"

if %errorlevel%==0 (
    echo.
    echo 🎉 Instalação concluída!
    echo.
    echo 📋 Para usar:
    echo 1. Ativação: whisper_russo_env\Scripts\activate.bat
    echo 2. Processar: whisper "arquivo.mp3" --language ru
    echo.
    echo 🎯 Comando para seu arquivo:
    echo whisper "INPUT\Tramplin - Deep House Lost. Act .mp3" --language ru --output_dir OUTPUT
    echo.
    echo 💡 Pressione qualquer tecla para processar o arquivo agora...
    pause >nul
    
    echo 🚀 Processando arquivo russo...
    whisper "INPUT\Tramplin - Deep House Lost. Act .mp3" --language ru --output_dir OUTPUT --model base
    
    if %errorlevel%==0 (
        echo ✅ Processamento concluído!
        echo 📁 Verifique a pasta OUTPUT para os resultados
    ) else (
        echo ❌ Erro no processamento
    )
) else (
    echo ❌ Erro na instalação
    exit /b 1
)

echo.
echo Pressione qualquer tecla para continuar...
pause >nul