#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transcrição Rápida - Modelo Tiny para Teste
"""

import os
import sys
import glob
from pathlib import Path
import time

def main():
    print("=== TRANSCRICAO RAPIDA (MODELO TINY) ===")
    
    # Importar whisper
    try:
        import whisper
        print("OK - Whisper carregado!")
    except ImportError:
        print("ERRO - Whisper nao encontrado!")
        return
    
    # Criar diretório de saída
    output_dir = "OUTPUT"
    os.makedirs(output_dir, exist_ok=True)
    
    # Procurar arquivos
    audio_files = []
    input_dirs = ["INPUT", os.path.join("PaddleSpeech", "INPUT")]
    
    for input_dir in input_dirs:
        if os.path.exists(input_dir):
            for ext in ['.mp3', '.wav', '.m4a']:
                pattern = os.path.join(input_dir, f"*{ext}")
                files = glob.glob(pattern)
                audio_files.extend(files)
    
    if not audio_files:
        print("ERRO - Nenhum arquivo encontrado!")
        return
    
    print(f"Encontrados {len(audio_files)} arquivo(s)")
    
    # Carregar modelo tiny (mais rápido)
    print("Carregando modelo TINY (mais rapido)...")
    try:
        model = whisper.load_model("tiny")
        print("OK - Modelo tiny carregado!")
    except Exception as e:
        print(f"ERRO - {e}")
        return
    
    # Processar primeiro arquivo
    audio_file = audio_files[0]
    filename = Path(audio_file).stem
    output_file = os.path.join(output_dir, f"{filename}_tiny.txt")
    
    print(f"\nProcessando: {os.path.basename(audio_file)}")
    print("NOTA: Usando modelo TINY - qualidade menor mas muito mais rapido")
    
    try:
        start_time = time.time()
        
        # Transcrever
        result = model.transcribe(
            audio_file,
            language="en",
            word_timestamps=False,
            verbose=True  # Mostra progresso
        )
        
        # Salvar
        text = result["text"].strip()
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        duration = time.time() - start_time
        print(f"\nConcluido em {duration:.1f} segundos!")
        print(f"Arquivo salvo: {output_file}")
        print(f"Tamanho do texto: {len(text)} caracteres")
        
        # Preview
        lines = text.split('.')[:3]  # Primeiras 3 frases
        print(f"\nPreview:")
        for line in lines:
            if line.strip():
                print(f"  {line.strip()}.")
        
        print(f"\nTeste concluido! Arquivo completo em: {os.path.abspath(output_file)}")
        
    except Exception as e:
        print(f"ERRO: {e}")

if __name__ == "__main__":
    main()