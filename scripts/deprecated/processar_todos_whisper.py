#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Transcrição Completa - Todos os Arquivos de Áudio
================================================

Este script processa todos os arquivos de áudio em inglês da pasta INPUT
usando OpenAI Whisper e gera arquivos TXT limpos.
"""

import os
import sys
import glob
import subprocess
import time
import re
from pathlib import Path

def check_whisper_installation():
    """Verifica se Whisper está instalado."""
    try:
        result = subprocess.run([sys.executable, '-m', 'whisper', '--help'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Whisper instalado e funcionando")
            return True
    except:
        pass
    
    print("❌ Whisper não encontrado")
    return False

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
        
        print(f"✅ Convertido: {os.path.basename(txt_file)}")
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

def create_output_dir():
    """Cria diretório de saída."""
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def transcribe_file(audio_file, output_dir):
    """Transcreve um arquivo de áudio usando Whisper."""
    filename = Path(audio_file).stem
    
    print(f"\n🎵 Processando: {filename}")
    
    # Verifica se já existe TXT
    txt_file = os.path.join(output_dir, f"{filename}.txt")
    if os.path.exists(txt_file):
        print(f"⏭️  Arquivo TXT já existe: {txt_file}")
        return True
    
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
        start_time = time.time()
        
        # Timeout de 10 minutos por arquivo
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ Transcrição concluída em {duration:.1f} segundos")
            
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
    """Processo principal de transcrição."""
    print("🎙️  TRANSCRIÇÃO COMPLETA - WHISPER")
    print("=" * 50)
    
    # Verifica instalação do Whisper
    if not check_whisper_installation():
        print("❌ Whisper não está instalado. Use: pip install openai-whisper")
        return
    
    # Obtém arquivos de áudio
    audio_files = get_audio_files()
    if not audio_files:
        print("❌ Nenhum arquivo de áudio encontrado")
        return
    
    print(f"\n📁 Encontrados {len(audio_files)} arquivos para processar")
    
    # Cria diretório de saída
    output_dir = create_output_dir()
    print(f"📂 Diretório de saída: {output_dir}")
    
    # Processa cada arquivo
    successful = 0
    failed = 0
    
    for i, audio_file in enumerate(audio_files, 1):
        print(f"\n📋 Progresso: {i}/{len(audio_files)}")
        print(f"🎵 Arquivo: {os.path.basename(audio_file)}")
        
        if transcribe_file(audio_file, output_dir):
            successful += 1
        else:
            failed += 1
        
        # Pausa breve entre arquivos
        time.sleep(2)
    
    # Resumo
    print(f"\n📊 RESUMO DA TRANSCRIÇÃO")
    print("=" * 30)
    print(f"✅ Sucessos: {successful}")
    print(f"❌ Falhas: {failed}")
    print(f"📁 Total: {len(audio_files)}")
    print(f"📂 Localização: {output_dir}")
    
    if successful > 0:
        print(f"\n🎉 Transcrição concluída! Verifique a pasta OUTPUT para os arquivos TXT.")
        
        # Lista arquivos TXT criados
        txt_files = glob.glob(os.path.join(output_dir, "*.txt"))
        if txt_files:
            print(f"\n📝 Arquivos TXT criados:")
            for txt_file in txt_files:
                print(f"   - {os.path.basename(txt_file)}")

if __name__ == "__main__":
    main()