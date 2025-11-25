#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transcrição Simples - Funciona no Windows
Usa whisper diretamente sem subprocess
"""

import os
import sys
import glob
from pathlib import Path
import time

def main():
    print("=== TRANSCRICAO SIMPLES ===")
    print(f"Python: {sys.executable}")
    print(f"Diretorio: {os.getcwd()}")
    
    # Importar whisper
    try:
        import whisper
        print("OK - Whisper carregado!")
    except ImportError:
        print("ERRO - Whisper nao encontrado!")
        print("Instale com: pip install openai-whisper")
        return
    
    # Criar diretório de saída
    output_dir = "OUTPUT"
    os.makedirs(output_dir, exist_ok=True)
    print(f"Pasta de saida: {output_dir}")
    
    # Procurar arquivos de áudio
    input_dirs = ["INPUT", os.path.join("PaddleSpeech", "INPUT")]
    audio_files = []
    
    for input_dir in input_dirs:
        if os.path.exists(input_dir):
            for ext in ['.mp3', '.wav', '.m4a', '.flac', '.ogg']:
                pattern = os.path.join(input_dir, f"*{ext}")
                files = glob.glob(pattern)
                audio_files.extend(files)
    
    if not audio_files:
        print("ERRO - Nenhum arquivo de audio encontrado!")
        print("Coloque arquivos .mp3, .wav, .m4a, .flac ou .ogg nas pastas INPUT")
        return
    
    print(f"\nEncontrados {len(audio_files)} arquivo(s):")
    for i, f in enumerate(audio_files, 1):
        print(f"  {i}. {os.path.basename(f)}")
    
    # Carregar modelo (pequeno para ser rápido)
    print("\nCarregando modelo Whisper (base)...")
    try:
        model = whisper.load_model("base")
        print("OK - Modelo carregado!")
    except Exception as e:
        print(f"ERRO - Falha ao carregar modelo: {e}")
        return
    
    # Processar cada arquivo
    success_count = 0
    
    for i, audio_file in enumerate(audio_files, 1):
        filename = Path(audio_file).stem
        output_file = os.path.join(output_dir, f"{filename}.txt")
        
        print(f"\n[{i}/{len(audio_files)}] Processando: {os.path.basename(audio_file)}")
        
        # Verificar se já existe
        if os.path.exists(output_file):
            print("  >> Ja processado, pulando...")
            success_count += 1
            continue
        
        try:
            print("  >> Transcrevendo...")
            start_time = time.time()
            
            # Transcrever usando whisper
            result = model.transcribe(
                audio_file,
                language="en",  # Pode mudar para "pt" para português
                word_timestamps=False,
                verbose=False
            )
            
            # Salvar texto
            text = result["text"].strip()
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            duration = time.time() - start_time
            print(f"  >> OK - Concluido em {duration:.1f}s")
            print(f"  >> Salvo: {output_file}")
            
            # Mostrar preview
            preview = text[:100] + "..." if len(text) > 100 else text
            print(f"  >> Preview: {preview}")
            
            success_count += 1
            
        except Exception as e:
            print(f"  >> ERRO: {e}")
    
    # Resumo
    print(f"\n=== RESUMO ===")
    print(f"Processados: {success_count}/{len(audio_files)}")
    print(f"Pasta de saida: {os.path.abspath(output_dir)}")
    
    if success_count > 0:
        print("\nARQUIVOS CRIADOS:")
        txt_files = glob.glob(os.path.join(output_dir, "*.txt"))
        for txt_file in txt_files:
            size = os.path.getsize(txt_file)
            print(f"  - {os.path.basename(txt_file)} ({size} bytes)")

if __name__ == "__main__":
    main()