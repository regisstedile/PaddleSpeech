#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Processamento Contínuo - Um arquivo por vez
"""

import os
import sys
import glob
import subprocess
import time
import json
from pathlib import Path

def get_next_file():
    """Pega o próximo arquivo para processar."""
    progress_file = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/transcription_progress.json"
    
    # Carrega progresso
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            progress = json.load(f)
    else:
        progress = {"completed": [], "failed": []}
    
    # Lista todos os arquivos
    files = glob.glob("/mnt/c/Users/Admin/Videos/1-PaddleSpeech/PaddleSpeech/INPUT/*.mp3")
    
    # Encontra o próximo arquivo não processado
    for file in sorted(files):
        if file not in progress["completed"] and file not in progress["failed"]:
            return file, progress
    
    return None, progress

def update_progress(file_path, status, progress):
    """Atualiza o progresso."""
    progress[status].append(file_path)
    
    with open("/mnt/c/Users/Admin/Videos/1-PaddleSpeech/transcription_progress.json", 'w') as f:
        json.dump(progress, f, indent=2)

def transcribe_single():
    """Processa um único arquivo."""
    file_path, progress = get_next_file()
    
    if not file_path:
        print("🎉 Todos os arquivos já foram processados!")
        return
    
    filename = Path(file_path).stem
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    
    print(f"🎵 Processando: {filename}")
    print(f"📁 Arquivo: {file_path}")
    
    # Verifica se já existe
    txt_output = os.path.join(output_dir, f"{filename}.txt")
    srt_output = os.path.join(output_dir, f"{filename}.srt")
    
    if os.path.exists(txt_output) or os.path.exists(srt_output):
        print("✅ Arquivo já processado anteriormente")
        update_progress(file_path, "completed", progress)
        return
    
    try:
        cmd = [
            sys.executable, '-m', 'whisper', file_path,
            '--language', 'en',
            '--model', 'base',
            '--output_dir', output_dir,
            '--output_format', 'txt',
            '--output_format', 'srt'
        ]
        
        print("⚙️  Iniciando transcrição...")
        start_time = time.time()
        
        # Executa o comando
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ Concluído em {duration:.1f} segundos")
            update_progress(file_path, "completed", progress)
            
            # Mostra estatísticas
            total_completed = len(progress["completed"]) + 1
            total_failed = len(progress["failed"])
            print(f"📊 Progresso: {total_completed} concluídos, {total_failed} falharam")
            
        else:
            print(f"❌ Erro na transcrição:")
            print(result.stderr[:300])
            update_progress(file_path, "failed", progress)
            
    except subprocess.TimeoutExpired:
        print("⏰ Timeout - arquivo muito longo")
        update_progress(file_path, "failed", progress)
    except Exception as e:
        print(f"❌ Erro: {e}")
        update_progress(file_path, "failed", progress)

if __name__ == "__main__":
    transcribe_single()