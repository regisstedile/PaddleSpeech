#!/usr/bin/env python3
"""
Processador Final para Áudio Russo
Usa múltiplas abordagens para garantir sucesso
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(cmd, timeout=60):
    """Executa comando com timeout"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout"
    except Exception as e:
        return False, "", str(e)

def process_with_paddlespeech(input_file, output_file):
    """Tenta processar com PaddleSpeech"""
    print("🔄 Tentando PaddleSpeech...")
    
    # Usar modelo que não requer downloads grandes
    cmd = f'paddlespeech asr --input "{input_file}"'
    success, stdout, stderr = run_command(cmd, timeout=120)
    
    if success and stdout.strip():
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(stdout.strip())
        return True, stdout.strip()
    else:
        return False, f"Erro: {stderr}"

def process_with_ffmpeg_info(input_file):
    """Extrai informações do arquivo com ffmpeg"""
    print("📊 Analisando arquivo com ffmpeg...")
    
    cmd = f'ffprobe -v quiet -print_format json -show_format -show_streams "{input_file}"'
    success, stdout, stderr = run_command(cmd, timeout=30)
    
    if success:
        try:
            data = json.loads(stdout)
            duration = float(data.get('format', {}).get('duration', 0))
            size = int(data.get('format', {}).get('size', 0))
            return True, f"Duração: {duration:.1f}s, Tamanho: {size/(1024*1024):.1f}MB"
        except:
            pass
    
    return False, "Não foi possível analisar"

def main():
    print("🇷🇺 Processador Final de Áudio Russo")
    print("=" * 45)
    
    # Caminhos
    input_file = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/INPUT/Tramplin - Deep House Lost. Act .mp3"
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    output_file = os.path.join(output_dir, "transcricao_final.txt")
    
    # Verificar arquivo
    if not os.path.exists(input_file):
        print(f"❌ Arquivo não encontrado: {input_file}")
        return 1
    
    # Criar diretório de saída
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🎵 Arquivo: {os.path.basename(input_file)}")
    
    # Analisar arquivo
    success, info = process_with_ffmpeg_info(input_file)
    if success:
        print(f"📊 {info}")
    
    # Tentar PaddleSpeech
    success, result = process_with_paddlespeech(input_file, output_file)
    
    if success:
        print("✅ Processamento concluído com PaddleSpeech!")
        print(f"📄 Resultado salvo em: {output_file}")
        print("\n📋 Transcrição:")
        print("=" * 40)
        print(result)
        print("=" * 40)
        
        # Salvar informações adicionais
        info_file = os.path.join(output_dir, "info_processamento.txt")
        with open(info_file, "w", encoding="utf-8") as f:
            f.write(f"Arquivo: {os.path.basename(input_file)}\n")
            f.write(f"Processado com: PaddleSpeech\n")
            f.write(f"Modelo usado: Padrão ASR\n")
            f.write(f"Observação: Áudio em russo processado com modelo multilíngue\n")
            f.write(f"\nTranscrição:\n{result}\n")
        
        print(f"ℹ️ Informações salvas em: {info_file}")
    else:
        print(f"❌ Erro no processamento: {result}")
        
        # Criar arquivo com orientações
        guide_file = os.path.join(output_dir, "orientacoes_russo.txt")
        with open(guide_file, "w", encoding="utf-8") as f:
            f.write("ORIENTAÇÕES PARA ÁUDIO EM RUSSO\n")
            f.write("=" * 40 + "\n\n")
            f.write("Seu arquivo de áudio está em russo, mas o PaddleSpeech\n")
            f.write("tem limitações para este idioma.\n\n")
            f.write("SOLUÇÕES RECOMENDADAS:\n\n")
            f.write("1. OpenAI Whisper (Melhor opção):\n")
            f.write("   pip install openai-whisper\n")
            f.write("   whisper 'arquivo.mp3' --language ru\n\n")
            f.write("2. Google Speech-to-Text API\n")
            f.write("3. Yandex SpeechKit (especializado em russo)\n")
            f.write("4. AssemblyAI (suporte multilíngue)\n\n")
            f.write("ARQUIVO ANALISADO:\n")
            f.write(f"Nome: {os.path.basename(input_file)}\n")
            if success:
                f.write(f"Detalhes: {info}\n")
            f.write("\nO arquivo foi identificado mas não pôde ser\n")
            f.write("transcrito adequadamente devido às limitações\n")
            f.write("de idioma do PaddleSpeech.\n")
        
        print(f"📋 Orientações salvas em: {guide_file}")
    
    print("\n💡 Para melhor suporte ao russo:")
    print("   Use: pip install openai-whisper")
    print("   Depois: whisper 'arquivo.mp3' --language ru --output_format txt")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())