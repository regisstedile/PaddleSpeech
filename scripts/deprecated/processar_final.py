#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Processamento Final dos Arquivos Restantes
=========================================
"""

import os
import sys
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
        
        return txt_file
        
    except Exception as e:
        print(f"❌ Erro ao converter {srt_file}: {e}")
        return None

def process_file(audio_file):
    """Processa um único arquivo."""
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    os.makedirs(output_dir, exist_ok=True)
    
    filename = Path(audio_file).stem
    print(f"🎵 Processando: {filename}")
    
    # Verifica se já existe TXT
    txt_file = os.path.join(output_dir, f"{filename}.txt")
    if os.path.exists(txt_file):
        print(f"⏭️  Arquivo TXT já existe: {filename}.txt")
        return True
    
    try:
        cmd = [
            sys.executable, '-m', 'whisper', audio_file,
            '--language', 'en',
            '--model', 'base',
            '--output_dir', output_dir,
            '--output_format', 'srt',
            '--fp16', 'False'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            srt_file = os.path.join(output_dir, f"{filename}.srt")
            if os.path.exists(srt_file):
                txt_file = convert_srt_to_txt(srt_file)
                if txt_file:
                    print(f"✅ Concluído: {filename}.txt")
                    return True
        
        print(f"❌ Falha: {filename}")
        return False
        
    except Exception as e:
        print(f"❌ Erro em {filename}: {e}")
        return False

def main():
    """Processa os 3 arquivos especificados."""
    print("🎙️  PROCESSAMENTO FINAL - 3 ARQUIVOS")
    print("=" * 45)
    
    # Arquivos específicos da pasta INPUT
    files_to_process = [
        "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/PaddleSpeech/INPUT/IO Music Academy Melodic Techno with Enamour.mp3",
        "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/PaddleSpeech/INPUT/IO Music Academy, Enamour - Inspiration Workflow with Enamour.mp3",
        "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/PaddleSpeech/INPUT/Master LangChain with No-Code tools - Flowise and LangFlow.mp3"
    ]
    
    successful = 0
    
    for i, audio_file in enumerate(files_to_process, 1):
        if os.path.exists(audio_file):
            print(f"\n📋 Arquivo {i}/{len(files_to_process)}")
            if process_file(audio_file):
                successful += 1
        else:
            print(f"❌ Arquivo não encontrado: {os.path.basename(audio_file)}")
    
    print(f"\n📊 PROCESSAMENTO CONCLUÍDO:")
    print(f"✅ Sucessos: {successful}/{len(files_to_process)}")
    
    # Lista todos os arquivos TXT criados
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    txt_files = [f for f in os.listdir(output_dir) if f.endswith('.txt')]
    
    if txt_files:
        print(f"\n📝 ARQUIVOS TXT DISPONÍVEIS ({len(txt_files)}):")
        for txt_file in sorted(txt_files):
            print(f"   ✅ {txt_file}")

if __name__ == "__main__":
    main()