#!/bin/bash

# Script para processar áudio em russo usando OpenAI Whisper
echo "🇷🇺 Processador de Áudio Russo - OpenAI Whisper"
echo "================================================="

# Ativar ambiente virtual
source /mnt/c/Users/Admin/Videos/1-PaddleSpeech/paddlespeech_env/bin/activate

# Verificar se o arquivo existe
INPUT_FILE="/mnt/c/Users/Admin/Videos/1-PaddleSpeech/INPUT/Tramplin - Deep House Lost. Act .mp3"
OUTPUT_DIR="/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"

if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ Arquivo não encontrado: $INPUT_FILE"
    echo "📁 Copie o arquivo para a pasta INPUT primeiro"
    exit 1
fi

# Criar diretório de saída se não existir
mkdir -p "$OUTPUT_DIR"

echo "🎵 Arquivo encontrado: $(basename "$INPUT_FILE")"
echo "🚀 Iniciando processamento com OpenAI Whisper..."

# Instalar OpenAI Whisper se não estiver instalado
echo "🔧 Verificando instalação do Whisper..."
python -c "import whisper" 2>/dev/null || {
    echo "📦 Instalando OpenAI Whisper..."
    pip install openai-whisper --quiet
}

# Processar o arquivo com Whisper
OUTPUT_FILE="$OUTPUT_DIR/transcricao_russo_whisper.txt"

echo "📝 Executando reconhecimento de voz em russo..."
echo "⏳ Isso pode demorar alguns minutos na primeira execução..."

# Usar Whisper para transcrição em russo
python3 << EOF
import whisper
import os

try:
    print("🔄 Carregando modelo Whisper...")
    model = whisper.load_model("base")
    
    print("🎯 Processando arquivo em russo...")
    result = model.transcribe("$INPUT_FILE", language="ru")
    
    # Salvar resultado
    with open("$OUTPUT_FILE", "w", encoding="utf-8") as f:
        f.write(result["text"])
    
    print("✅ Transcrição concluída!")
    print(f"📄 Resultado salvo em: $OUTPUT_FILE")
    print("")
    print("📋 Conteúdo da transcrição:")
    print("=" * 50)
    print(result["text"])
    print("=" * 50)
    
except Exception as e:
    print(f"❌ Erro no processamento: {e}")
    exit(1)
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Processamento concluído com sucesso!"
    echo "📁 Arquivo de saída: $OUTPUT_FILE"
else
    echo ""
    echo "❌ Erro no processamento"
fi

echo ""
echo "💡 Whisper suporta nativamente:"
echo "   - 🇷🇺 Russo (ru)"
echo "   - 🇺🇸 Inglês (en)"
echo "   - 🇪🇸 Espanhol (es)"
echo "   - 🇫🇷 Francês (fr)"
echo "   - 🇩🇪 Alemão (de)"
echo "   - 🇨🇳 Chinês (zh)"
echo "   - E mais de 90 idiomas!"