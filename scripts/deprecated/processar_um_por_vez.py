#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processador Individual - Um arquivo por vez
==========================================
Processa um arquivo de cada vez para controle melhor.
"""
import os
import sys
import glob
import subprocess
import json
from datetime import datetime

def obter_proximo_arquivo():
    """Obtém o próximo arquivo para processar."""
    input_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/PaddleSpeech/INPUT"
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    
    # Extensões de áudio suportadas
    audio_extensions = ['*.mp3', '*.mp4', '*.wav', '*.m4a', '*.wmv', '*.avi']
    arquivos_audio = []
    
    for ext in audio_extensions:
        arquivos_audio.extend(glob.glob(os.path.join(input_dir, ext)))
    
    # Encontrar o primeiro arquivo não processado
    for arquivo_audio in sorted(arquivos_audio):
        nome_base = os.path.splitext(os.path.basename(arquivo_audio))[0]
        arquivo_srt = os.path.join(output_dir, f"{nome_base}.srt")
        
        if not os.path.exists(arquivo_srt):
            return arquivo_audio
    
    return None

def processar_arquivo():
    """Processa um único arquivo."""
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    os.makedirs(output_dir, exist_ok=True)
    
    # Obter próximo arquivo
    arquivo = obter_proximo_arquivo()
    
    if not arquivo:
        print("🎉 Todos os arquivos foram processados!")
        return
    
    nome_arquivo = os.path.basename(arquivo)
    tamanho_mb = os.path.getsize(arquivo) / (1024*1024)
    
    print(f"🎵 Processando: {nome_arquivo}")
    print(f"📏 Tamanho: {tamanho_mb:.1f} MB")
    print(f"📁 Arquivo: {arquivo}")
    
    try:
        # Comando Whisper
        cmd = [
            sys.executable, '-m', 'whisper', arquivo,
            '--language', 'en',
            '--model', 'base',
            '--output_dir', output_dir,
            '--output_format', 'srt',
            '--verbose', 'False'
        ]
        
        print("⚙️  Iniciando transcrição...")
        resultado = subprocess.run(cmd, capture_output=True, text=True)
        
        if resultado.returncode == 0:
            print("✅ Transcrição concluída com sucesso!")
            
            # Verificar se arquivo foi criado
            nome_base = os.path.splitext(nome_arquivo)[0]
            arquivo_srt = os.path.join(output_dir, f"{nome_base}.srt")
            
            if os.path.exists(arquivo_srt):
                print(f"📄 Arquivo SRT criado: {nome_base}.srt")
            else:
                print("⚠️  Arquivo SRT não encontrado na saída")
                
        else:
            print(f"❌ Erro na transcrição:")
            print(resultado.stderr)
            
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")

if __name__ == "__main__":
    processar_arquivo()