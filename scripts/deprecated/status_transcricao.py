#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Status da Transcrição
"""

import os
import json
import glob
from pathlib import Path

def show_status():
    """Mostra o status atual da transcrição."""
    
    # Carrega progresso
    progress_file = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/transcription_progress.json"
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            progress = json.load(f)
    else:
        progress = {"completed": [], "failed": []}
    
    # Lista todos os arquivos
    all_files = glob.glob("/mnt/c/Users/Admin/Videos/1-PaddleSpeech/PaddleSpeech/INPUT/*.mp3")
    total_files = len(all_files)
    completed = len(progress["completed"])
    failed = len(progress["failed"])
    remaining = total_files - completed - failed
    
    print("🎙️  STATUS DA TRANSCRIÇÃO DE ÁUDIOS EM INGLÊS")
    print("=" * 60)
    print(f"📁 Total de arquivos: {total_files}")
    print(f"✅ Concluídos: {completed}")
    print(f"❌ Falharam: {failed}")
    print(f"📋 Restantes: {remaining}")
    print(f"📊 Progresso: {(completed/total_files)*100:.1f}%")
    
    if completed > 0:
        print(f"\n📂 Últimos arquivos processados:")
        for file in progress["completed"][-5:]:
            name = Path(file).stem
            print(f"   ✅ {name}")
    
    if remaining > 0:
        print(f"\n📋 Próximos arquivos para processar:")
        for file in sorted(all_files)[:5]:
            if file not in progress["completed"] and file not in progress["failed"]:
                name = Path(file).stem
                print(f"   📋 {name}")
    
    # Verifica arquivos de saída
    output_files = glob.glob("/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT/*.txt")
    srt_files = glob.glob("/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT/*.srt")
    
    print(f"\n📂 Arquivos de saída criados:")
    print(f"   📝 Arquivos TXT: {len(output_files)}")
    print(f"   🎬 Arquivos SRT: {len(srt_files)}")
    
    if remaining == 0:
        print(f"\n🎉 TRANSCRIÇÃO COMPLETA! Todos os arquivos foram processados.")
    else:
        print(f"\n⚙️  Para continuar, execute:")
        print(f"   python3 processar_multiplos.py")

if __name__ == "__main__":
    show_status()