#!/bin/bash

echo "🇷🇺 Instalador Whisper para Áudio Russo"
echo "========================================"

# Criar ambiente limpo para Whisper
echo "🔧 Criando ambiente Python limpo..."
python3 -m venv whisper_russo_env

# Ativar ambiente
echo "⚡ Ativando ambiente..."
source whisper_russo_env/bin/activate

# Atualizar pip
echo "📦 Atualizando pip..."
pip install --upgrade pip

# Instalar Whisper
echo "🎙️ Instalando OpenAI Whisper..."
pip install openai-whisper

# Testar instalação
echo "🧪 Testando instalação..."
python3 -c "import whisper; print('✅ Whisper instalado com sucesso!')"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Instalação concluída!"
    echo ""
    echo "📋 Para usar:"
    echo "1. Ativar ambiente: source whisper_russo_env/bin/activate"
    echo "2. Processar áudio: whisper 'arquivo.mp3' --language ru"
    echo ""
    echo "🎯 Comando específico para seu arquivo:"
    echo "whisper \"/mnt/c/Users/Admin/Videos/1-PaddleSpeech/INPUT/Tramplin - Deep House Lost. Act .mp3\" --language ru --output_dir \"/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT\""
else
    echo "❌ Erro na instalação"
    exit 1
fi