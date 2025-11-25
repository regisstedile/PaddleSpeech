#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Verificação de Novos Arquivos para Transcrição
==============================================
"""

import os
import glob
from pathlib import Path

def verificar_arquivos():
    """Verifica arquivos pendentes de transcrição."""
    print("🔍 VERIFICAÇÃO DE ARQUIVOS PARA TRANSCRIÇÃO")
    print("=" * 50)
    
    # Diretórios de entrada
    input_dirs = [
        "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/INPUT/",
        "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/PaddleSpeech/INPUT/"
    ]
    
    # Diretório de saída
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    
    # Extensões de áudio
    audio_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg', '.wmv']
    
    all_audio_files = []
    processed_files = []
    pending_files = []
    
    # Busca todos os arquivos de áudio
    for input_dir in input_dirs:
        if os.path.exists(input_dir):
            print(f"\n📁 Verificando: {input_dir}")
            for ext in audio_extensions:
                files = glob.glob(f"{input_dir}*{ext}")
                for audio_file in files:
                    filename = os.path.basename(audio_file)
                    print(f"   🎵 Encontrado: {filename}")
                    all_audio_files.append(audio_file)
    
    # Verifica quais já foram processados
    if os.path.exists(output_dir):
        existing_txt = glob.glob(f"{output_dir}/*.txt")
        processed_names = [Path(f).stem for f in existing_txt]
        
        print(f"\n✅ ARQUIVOS JÁ PROCESSADOS ({len(processed_names)}):")
        for name in processed_names:
            print(f"   ✅ {name}.txt")
    
    # Identifica arquivos pendentes
    for audio_file in all_audio_files:
        filename = Path(audio_file).stem
        txt_file = os.path.join(output_dir, f"{filename}.txt")
        
        if os.path.exists(txt_file):
            processed_files.append(audio_file)
        else:
            pending_files.append(audio_file)
    
    print(f"\n⏳ ARQUIVOS PENDENTES ({len(pending_files)}):")
    if pending_files:
        for audio_file in pending_files:
            filename = os.path.basename(audio_file)
            print(f"   ⏳ {filename}")
    else:
        print("   🎉 Nenhum arquivo pendente!")
    
    print(f"\n📊 RESUMO:")
    print(f"   📁 Total encontrados: {len(all_audio_files)}")
    print(f"   ✅ Já processados: {len(processed_files)}")
    print(f"   ⏳ Pendentes: {len(pending_files)}")
    
    return pending_files

if __name__ == "__main__":
    pending = verificar_arquivos()
    
    if pending:
        print(f"\n💡 Para processar os arquivos pendentes:")
        print(f"   python3 processar_lote.py")
    else:
        print(f"\n🎉 Todos os arquivos foram processados!")