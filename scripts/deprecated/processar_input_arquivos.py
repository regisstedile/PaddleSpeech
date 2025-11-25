#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Processamento dos 3 Arquivos da Pasta INPUT
==========================================
"""

import os
import sys
import subprocess
import re
from pathlib import Path
import time

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

def process_file(audio_file, output_dir):
    """Processa um arquivo individual."""
    filename = Path(audio_file).stem
    
    # Verifica se já existe TXT
    txt_file = os.path.join(output_dir, f"{filename}.txt")
    if os.path.exists(txt_file):
        print(f"⏭️  Já processado: {filename}.txt")
        return True
    
    print(f"\n🎵 PROCESSANDO: {filename}")
    print(f"📁 Arquivo: {os.path.basename(audio_file)}")
    
    try:
        # Comando Whisper otimizado para velocidade
        cmd = [
            sys.executable, '-m', 'whisper', audio_file,
            '--language', 'en',
            '--model', 'tiny',  # Modelo mais rápido
            '--output_dir', output_dir,
            '--output_format', 'srt',  # SRT primeiro, depois convertemos
            '--fp16', 'False',
            '--verbose', 'False',
            '--no_speech_threshold', '0.8',  # Otimização
            '--condition_on_previous_text', 'False'  # Mais rápido
        ]
        
        print(f"⚙️  Executando Whisper (modelo: tiny)...")
        start_time = time.time()
        
        # Timeout de 15 minutos por arquivo
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ Transcrição SRT concluída em {duration:.1f} segundos")
            
            # Converte SRT para TXT
            srt_file = os.path.join(output_dir, f"{filename}.srt")
            if os.path.exists(srt_file):
                txt_result = convert_srt_to_txt(srt_file)
                if txt_result:
                    print(f"📝 Arquivo final: {os.path.basename(txt_result)}")
                    return True
            
        else:
            print(f"❌ Falha na transcrição:")
            print(f"   Erro: {result.stderr[:200]}...")
            return False
        
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout (15 minutos excedidos)")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    """Processa os 3 arquivos da pasta INPUT."""
    print("🎙️  PROCESSAMENTO DOS ARQUIVOS INPUT")
    print("=" * 50)
    
    # Diretório de saída
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    os.makedirs(output_dir, exist_ok=True)
    
    # Lista específica dos 3 arquivos
    files_to_process = [
        "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/PaddleSpeech/INPUT/IO Music Academy Melodic Techno with Enamour.mp3",
        "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/PaddleSpeech/INPUT/IO Music Academy, Enamour - Inspiration Workflow with Enamour.mp3",
        "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/PaddleSpeech/INPUT/Master LangChain with No-Code tools - Flowise and LangFlow.mp3"
    ]
    
    print(f"📁 Arquivos para processar: {len(files_to_process)}")
    print(f"📂 Diretório de saída: {output_dir}")
    
    successful = 0
    failed = 0
    
    for i, audio_file in enumerate(files_to_process, 1):
        print(f"\n{'='*60}")
        print(f"📋 ARQUIVO {i}/{len(files_to_process)}")
        print(f"{'='*60}")
        
        if os.path.exists(audio_file):
            if process_file(audio_file, output_dir):
                successful += 1
            else:
                failed += 1
        else:
            print(f"❌ Arquivo não encontrado: {os.path.basename(audio_file)}")
            failed += 1
    
    # Resumo final
    print(f"\n{'='*60}")
    print(f"📊 RESUMO FINAL")
    print(f"{'='*60}")
    print(f"✅ Sucessos: {successful}")
    print(f"❌ Falhas: {failed}")
    print(f"📁 Total: {len(files_to_process)}")
    
    # Lista arquivos TXT criados
    txt_files = [f for f in os.listdir(output_dir) if f.endswith('.txt')]
    if txt_files:
        print(f"\n📝 ARQUIVOS TXT DISPONÍVEIS ({len(txt_files)}):")
        for txt_file in sorted(txt_files):
            file_path = os.path.join(output_dir, txt_file)
            file_size = os.path.getsize(file_path)
            print(f"   📄 {txt_file} ({file_size//1024} KB)")
    
    if successful > 0:
        print(f"\n🎉 Processamento concluído!")
        print(f"📂 Localização: {output_dir}")

if __name__ == "__main__":
    main()