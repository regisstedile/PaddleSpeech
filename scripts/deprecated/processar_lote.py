#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Processamento em Lotes de Arquivos de Áudio
==========================================
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
        
        return txt_file
        
    except Exception as e:
        print(f"❌ Erro ao converter {srt_file}: {e}")
        return None

def get_pending_files():
    """Obtém arquivos que ainda não foram processados."""
    input_dirs = [
        "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/INPUT/",
        "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/PaddleSpeech/INPUT/"
    ]
    
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    
    audio_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg', '.wmv']
    pending_files = []
    
    for input_dir in input_dirs:
        if os.path.exists(input_dir):
            for ext in audio_extensions:
                files = glob.glob(f"{input_dir}*{ext}")
                for audio_file in files:
                    filename = Path(audio_file).stem
                    txt_file = os.path.join(output_dir, f"{filename}.txt")
                    if not os.path.exists(txt_file):
                        pending_files.append(audio_file)
    
    return pending_files

def process_file(audio_file):
    """Processa um único arquivo."""
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    os.makedirs(output_dir, exist_ok=True)
    
    filename = Path(audio_file).stem
    print(f"🎵 Processando: {filename}")
    
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
    """Processa próximos 3 arquivos."""
    print("🎙️  PROCESSAMENTO EM LOTE - WHISPER")
    print("=" * 45)
    
    pending_files = get_pending_files()
    
    if not pending_files:
        print("✅ Todos os arquivos foram processados!")
        return
    
    print(f"📁 Arquivos pendentes: {len(pending_files)}")
    
    # Processa próximos 3 arquivos
    batch_size = 3
    batch = pending_files[:batch_size]
    
    print(f"🚀 Processando {len(batch)} arquivos...")
    
    successful = 0
    for i, audio_file in enumerate(batch, 1):
        print(f"\n📋 Arquivo {i}/{len(batch)}")
        if process_file(audio_file):
            successful += 1
    
    remaining = len(pending_files) - len(batch)
    
    print(f"\n📊 LOTE CONCLUÍDO:")
    print(f"✅ Processados: {successful}/{len(batch)}")
    print(f"📁 Restantes: {remaining}")
    
    if remaining > 0:
        print(f"\n💡 Execute novamente para processar os próximos arquivos:")
        print(f"   python3 processar_lote.py")

if __name__ == "__main__":
    main()