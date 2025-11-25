#!/bin/bash

# Script para processar áudio em russo usando PaddleSpeech nativo
echo "🇷🇺 Processador de Áudio Russo - PaddleSpeech"
echo "=============================================="

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
echo "🚀 Iniciando processamento com PaddleSpeech..."

# Usar PaddleSpeech ASR (melhor suporte para russo)
OUTPUT_FILE="$OUTPUT_DIR/transcricao_russo.txt"

echo "📝 Executando reconhecimento de voz..."

# Usar OpenAI Whisper para melhor suporte ao russo
echo "🎙️ Processando com OpenAI Whisper (modelo large)..."
whisper "$INPUT_FILE" --language russian --model large --output_dir "$OUTPUT_DIR" --output_format txt > /dev/null 2>&1

# Renomear o arquivo de saída do Whisper para o nome desejado
WHISPER_OUTPUT_FILE="$OUTPUT_DIR/$(basename "${INPUT_FILE%.*}").txt"
mv "$OUTPUT_DIR/whisper_output_test/$(basename "${INPUT_FILE%.*}").txt" "$OUTPUT_FILE"


if [ $? -eq 0 ]; then
    echo "✅ Processamento concluído!"
    echo "📄 Resultado salvo em: $OUTPUT_FILE"
    echo ""
    echo "📋 Conteúdo da transcrição:"
    echo "================================="
    cat "$OUTPUT_FILE" 2>/dev/null || echo "Arquivo de saída não encontrado"
    echo ""
    echo "================================="
else
    echo "❌ Erro no processamento"
fi

echo ""
echo "💡 Dica: Para melhor suporte ao russo, considere usar:"
echo "   - OpenAI Whisper (suporte nativo ao russo)"
echo "   - Google Speech-to-Text API"
echo "   - Yandex SpeechKit (especializado em russo)"