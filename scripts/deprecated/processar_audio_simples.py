#!/usr/bin/env python3
"""
Processador de Áudio Simples
Funciona com áudio em russo usando bibliotecas básicas
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🎵 Processador de Áudio Simples")
    print("================================")
    
    # Caminhos
    input_file = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/INPUT/Tramplin - Deep House Lost. Act .mp3"
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    
    # Verificar se arquivo existe
    if not os.path.exists(input_file):
        print(f"❌ Arquivo não encontrado: {input_file}")
        return 1
    
    # Criar diretório de saída
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🎵 Arquivo encontrado: {os.path.basename(input_file)}")
    print("🚀 Iniciando processamento...")
    
    # Tentar usar PaddleSpeech com modelo padrão
    try:
        print("🔄 Tentando PaddleSpeech ASR...")
        cmd = ["paddlespeech", "asr", "--input", input_file]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            output_file = os.path.join(output_dir, "transcricao_simples.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result.stdout.strip())
            
            print("✅ Processamento concluído!")
            print(f"📄 Resultado salvo em: {output_file}")
            print("")
            print("📋 Conteúdo da transcrição:")
            print("=" * 40)
            print(result.stdout.strip())
            print("=" * 40)
            return 0
        else:
            print(f"❌ Erro no PaddleSpeech: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⏰ Timeout no PaddleSpeech")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
    
    # Informações sobre o arquivo
    try:
        print("")
        print("📊 Informações do arquivo:")
        print(f"📁 Nome: {os.path.basename(input_file)}")
        print(f"📏 Tamanho: {os.path.getsize(input_file) / (1024*1024):.1f} MB")
        print("")
        print("💡 Para melhor suporte ao russo:")
        print("   - Use OpenAI Whisper: pip install openai-whisper")
        print("   - Use Google Speech-to-Text API")
        print("   - Use Yandex SpeechKit (especializado em russo)")
        print("")
        print("🎯 Comando Whisper recomendado:")
        print('   whisper "arquivo.mp3" --language ru --output_format txt')
        
    except Exception as e:
        print(f"❌ Erro ao obter informações: {e}")
    
    return 1

if __name__ == "__main__":
    sys.exit(main())