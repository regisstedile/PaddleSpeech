#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste Simples do Whisper
"""
import sys
import os

print("Testando Whisper...")
print(f"Python: {sys.executable}")
print(f"Diretorio atual: {os.getcwd()}")

# Teste 1: Import direto
print("\nTeste 1: Import do modulo")
try:
    import whisper
    print("OK - Modulo whisper importado com sucesso!")
    
    # Mostra modelos disponíveis
    print("Modelos disponiveis:")
    for model in whisper.available_models():
        print(f"  - {model}")
        
except ImportError as e:
    print(f"ERRO - Erro ao importar whisper: {e}")

# Teste 2: Linha de comando
print("\nTeste 2: Comando via subprocess")
try:
    import subprocess
    result = subprocess.run([sys.executable, '-m', 'whisper', '--help'], 
                          capture_output=True, text=True, timeout=10)
    if result.returncode == 0:
        print("OK - Comando whisper funciona!")
        print("Versao encontrada no help:")
        # Mostra primeiras linhas do help
        help_lines = result.stdout.split('\n')[:5]
        for line in help_lines:
            if line.strip():
                print(f"  {line}")
    else:
        print(f"ERRO - Comando falhou: {result.stderr}")
        
except Exception as e:
    print(f"ERRO - Erro no subprocess: {e}")

# Teste 3: Verificar arquivos de entrada
print("\nTeste 3: Verificar arquivos de entrada")
input_dirs = [
    "INPUT",
    os.path.join("PaddleSpeech", "INPUT")
]

for input_dir in input_dirs:
    if os.path.exists(input_dir):
        files = os.listdir(input_dir)
        audio_files = [f for f in files if f.lower().endswith(('.mp3', '.wav', '.m4a', '.flac'))]
        print(f"Pasta {input_dir}: {len(audio_files)} arquivo(s) de audio")
        for f in audio_files[:3]:  # Mostra até 3 arquivos
            print(f"  - {f}")
        if len(audio_files) > 3:
            print(f"  ... e mais {len(audio_files) - 3} arquivo(s)")
    else:
        print(f"ERRO - Diretorio nao encontrado: {input_dir}")

print("\nResultado do teste concluido!")