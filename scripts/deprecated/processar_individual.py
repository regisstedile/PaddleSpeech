#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Processamento Individual de Arquivos de Áudio
============================================

Este script processa arquivos de áudio individualmente usando Whisper
"""

import os
import sys
import glob
import subprocess
import re
from pathlib import Path

def convert_srt_to_txt(srt_file):
    """Converte arquivo SRT para TXT limpo."""
    txt_file = srt_file.replace('.srt', '.txt')
    
    try:
        with open(srt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove timestamps and numbers from SRT
        lines = content.split('\n')
        text_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip empty lines, numbers, and timestamp lines
            if line and not re.match(r'^\d+$', line) and not re.match(r'^\d{2}:\d{2}:\d{2}', line):
                text_lines.append(line)
        
        # Join all text
        clean_text = ' '.join(text_lines)
        
        # Save as TXT
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(clean_text)
        
        print(f"✅ TXT criado: {os.path.basename(txt_file)}")
        return txt_file
        
    except Exception as e:
        print(f"❌ Erro ao converter {srt_file}: {e}")
        return None

def get_audio_files():
    """Obtém lista de arquivos de áudio para processar."""
    input_dirs = [
        "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/INPUT/",
        "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/PaddleSpeech/INPUT/"
    ]
    
    audio_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg', '.wmv']
    audio_files = []
    
    for input_dir in input_dirs:
        if os.path.exists(input_dir):
            for ext in audio_extensions:
                files = glob.glob(f"{input_dir}*{ext}")
                audio_files.extend(files)
    
    return audio_files

def process_single_file(audio_file):
    """Processa um único arquivo de áudio."""
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    os.makedirs(output_dir, exist_ok=True)
    
    filename = Path(audio_file).stem
    
    # Verifica se já existe TXT
    txt_file = os.path.join(output_dir, f"{filename}.txt")
    if os.path.exists(txt_file):
        print(f"⏭️  Arquivo TXT já existe: {filename}.txt")
        return True
    
    print(f"\n🎵 Processando: {filename}")
    
    try:
        # Executa Whisper para gerar SRT
        cmd = [
            sys.executable, '-m', 'whisper', audio_file,
            '--language', 'en',
            '--model', 'base',
            '--output_dir', output_dir,
            '--output_format', 'srt',
            '--fp16', 'False'
        ]
        
        print(f"⚙️  Executando Whisper...")
        
        # Timeout de 10 minutos por arquivo
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print(f"✅ Transcrição SRT concluída")
            
            # Converte SRT para TXT
            srt_file = os.path.join(output_dir, f"{filename}.srt")
            if os.path.exists(srt_file):
                txt_file = convert_srt_to_txt(srt_file)
                if txt_file:
                    return True
            
        else:
            print(f"❌ Falha na transcrição: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout (10 minutos excedidos)")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    """Lista arquivos e permite escolher qual processar."""
    print("🎙️  PROCESSAMENTO INDIVIDUAL - WHISPER")
    print("=" * 50)
    
    # Obtém arquivos de áudio
    audio_files = get_audio_files()
    if not audio_files:
        print("❌ Nenhum arquivo de áudio encontrado")
        return
    
    print(f"\n📁 Arquivos encontrados:")
    for i, audio_file in enumerate(audio_files, 1):
        filename = os.path.basename(audio_file)
        print(f"{i:2d}. {filename}")
    
    # Se executado com argumento, processa todos
    if len(sys.argv) > 1 and sys.argv[1] == "all":
        print(f"\n🚀 Processando todos os {len(audio_files)} arquivos...")
        successful = 0
        failed = 0
        
        for i, audio_file in enumerate(audio_files, 1):
            print(f"\n📋 Progresso: {i}/{len(audio_files)}")
            if process_single_file(audio_file):
                successful += 1
            else:
                failed += 1
        
        print(f"\n📊 RESUMO:")
        print(f"✅ Sucessos: {successful}")
        print(f"❌ Falhas: {failed}")
        print(f"📁 Total: {len(audio_files)}")
        
    else:
        print(f"\nPara processar todos: python3 {sys.argv[0]} all")
        print(f"Para processar um específico, edite este script")

if __name__ == "__main__":
    main()