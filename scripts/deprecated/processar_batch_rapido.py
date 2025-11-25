#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Processamento Rápido em Batch
============================
"""

import os
import sys
import subprocess
import re
from pathlib import Path

def convert_srt_to_txt(srt_file):
    """Converte SRT para TXT."""
    txt_file = srt_file.replace('.srt', '.txt')
    
    try:
        with open(srt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        text_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not re.match(r'^\d+$', line) and not re.match(r'^\d{2}:\d{2}:\d{2}', line):
                text_lines.append(line)
        
        clean_text = ' '.join(text_lines)
        
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(clean_text)
        
        return txt_file
        
    except Exception as e:
        print(f"❌ Erro ao converter: {e}")
        return None

def process_single(audio_file, output_dir):
    """Processa um arquivo individual."""
    filename = Path(audio_file).stem
    txt_file = os.path.join(output_dir, f"{filename}.txt")
    
    if os.path.exists(txt_file):
        print(f"⏭️  Já existe: {filename}.txt")
        return True
    
    print(f"🎵 Processando: {filename}")
    
    try:
        # Comando Whisper otimizado
        cmd = [
            sys.executable, '-m', 'whisper', audio_file,
            '--language', 'en',
            '--model', 'tiny',  # Modelo menor para velocidade
            '--output_dir', output_dir,
            '--output_format', 'srt',
            '--fp16', 'False',
            '--verbose', 'False'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)  # 5 min timeout
        
        if result.returncode == 0:
            srt_file = os.path.join(output_dir, f"{filename}.srt")
            if os.path.exists(srt_file):
                txt_result = convert_srt_to_txt(srt_file)
                if txt_result:
                    print(f"✅ Concluído: {filename}.txt")
                    return True
        
        print(f"❌ Falha: {filename}")
        return False
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    """Processa os 3 arquivos específicos."""
    print("⚡ PROCESSAMENTO RÁPIDO - 3 ARQUIVOS")
    print("=" * 45)
    
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    os.makedirs(output_dir, exist_ok=True)
    
    # Lista específica dos 3 arquivos
    files = [
        "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/PaddleSpeech/INPUT/IO Music Academy Melodic Techno with Enamour.mp3",
        "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/PaddleSpeech/INPUT/IO Music Academy, Enamour - Inspiration Workflow with Enamour.mp3",
        "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/PaddleSpeech/INPUT/Master LangChain with No-Code tools - Flowise and LangFlow.mp3"
    ]
    
    successful = 0
    
    for i, audio_file in enumerate(files, 1):
        if os.path.exists(audio_file):
            print(f"\n📋 Arquivo {i}/3")
            if process_single(audio_file, output_dir):
                successful += 1
        else:
            print(f"❌ Não encontrado: {os.path.basename(audio_file)}")
    
    print(f"\n📊 RESULTADO:")
    print(f"✅ Sucessos: {successful}/3")
    
    # Lista arquivos TXT finais
    txt_files = [f for f in os.listdir(output_dir) if f.endswith('.txt')]
    if txt_files:
        print(f"\n📝 ARQUIVOS TXT ({len(txt_files)}):")
        for txt in sorted(txt_files):
            print(f"   📄 {txt}")

if __name__ == "__main__":
    main()