#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processador de Novos Arquivos de Áudio - Whisper
===============================================
Processa especificamente os 22 novos arquivos adicionados.
Otimizado para cursos de Lynda, MasterClass, Pluralsight e LinkedIn Learning.
"""
import os
import sys
import glob
import subprocess
import json
from datetime import datetime

def verificar_whisper():
    """Verifica se o Whisper está funcionando."""
    try:
        result = subprocess.run([sys.executable, '-m', 'whisper', '--help'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Whisper disponível e funcionando")
            return True
        else:
            print("❌ Erro ao verificar Whisper")
            return False
    except Exception as e:
        print(f"❌ Whisper não encontrado: {e}")
        return False

def carregar_progresso():
    """Carrega o progresso salvo."""
    try:
        if os.path.exists('transcription_progress_novos.json'):
            with open('transcription_progress_novos.json', 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return {"processados": [], "timestamp": datetime.now().isoformat()}

def salvar_progresso(progresso):
    """Salva o progresso atual."""
    try:
        progresso["timestamp"] = datetime.now().isoformat()
        with open('transcription_progress_novos.json', 'w', encoding='utf-8') as f:
            json.dump(progresso, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️  Erro ao salvar progresso: {e}")

def obter_novos_arquivos():
    """Obtém lista de arquivos que ainda não foram processados."""
    input_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/PaddleSpeech/INPUT"
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    
    # Extensões de áudio suportadas
    audio_extensions = ['*.mp3', '*.mp4', '*.wav', '*.m4a', '*.wmv', '*.avi']
    arquivos_audio = []
    
    for ext in audio_extensions:
        arquivos_audio.extend(glob.glob(os.path.join(input_dir, ext)))
    
    # Filtrar arquivos não processados
    arquivos_novos = []
    for arquivo_audio in arquivos_audio:
        nome_base = os.path.splitext(os.path.basename(arquivo_audio))[0]
        arquivo_srt = os.path.join(output_dir, f"{nome_base}.srt")
        
        if not os.path.exists(arquivo_srt):
            arquivos_novos.append(arquivo_audio)
    
    return sorted(arquivos_novos)

def transcrever_arquivo(arquivo_audio, output_dir, modelo='base'):
    """Transcreve um arquivo de áudio usando Whisper."""
    nome_arquivo = os.path.basename(arquivo_audio)
    print(f"\n🎵 Processando: {nome_arquivo}")
    print(f"📁 Arquivo: {arquivo_audio}")
    
    try:
        # Comando Whisper otimizado para inglês
        cmd = [
            sys.executable, '-m', 'whisper', arquivo_audio,
            '--language', 'en',
            '--model', modelo,
            '--output_dir', output_dir,
            '--output_format', 'srt',
            '--verbose', 'False'
        ]
        
        print("⚙️  Iniciando transcrição...")
        resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)  # 30 min timeout
        
        if resultado.returncode == 0:
            print("✅ Transcrição concluída com sucesso!")
            return True
        else:
            print(f"❌ Erro na transcrição: {resultado.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏱️  Timeout na transcrição (30 minutos)")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        return False

def processar_lote(quantidade=5):
    """Processa um lote de arquivos."""
    if not verificar_whisper():
        return
    
    # Configurações
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    os.makedirs(output_dir, exist_ok=True)
    
    # Carregar progresso
    progresso = carregar_progresso()
    
    # Obter arquivos novos
    arquivos_novos = obter_novos_arquivos()
    
    # Filtrar arquivos já processados
    arquivos_pendentes = [f for f in arquivos_novos 
                         if os.path.basename(f) not in progresso.get("processados", [])]
    
    if not arquivos_pendentes:
        print("🎉 Todos os novos arquivos já foram processados!")
        return
    
    print(f"🎙️  PROCESSANDO NOVOS ARQUIVOS DE ÁUDIO")
    print("=" * 60)
    print(f"📁 Total de arquivos novos: {len(arquivos_novos)}")
    print(f"✅ Já processados: {len(progresso.get('processados', []))}")
    print(f"⏳ Pendentes: {len(arquivos_pendentes)}")
    print(f"🎯 Processando agora: {min(quantidade, len(arquivos_pendentes))} arquivo(s)")
    print()
    
    sucessos = 0
    falhas = 0
    
    # Processar lote atual
    for i, arquivo in enumerate(arquivos_pendentes[:quantidade], 1):
        print(f"📋 Arquivo {i}/{min(quantidade, len(arquivos_pendentes))}")
        print("-" * 40)
        
        if transcrever_arquivo(arquivo, output_dir):
            sucessos += 1
            # Salvar progresso
            if "processados" not in progresso:
                progresso["processados"] = []
            progresso["processados"].append(os.path.basename(arquivo))
            salvar_progresso(progresso)
        else:
            falhas += 1
    
    # Resultado final
    print("\n" + "=" * 60)
    print("📊 RESULTADO DO LOTE:")
    print(f"   ✅ Sucessos: {sucessos}")
    print(f"   ❌ Falhas: {falhas}")
    print(f"   📁 Total processado: {sucessos}")
    
    # Status geral
    total_processados = len(progresso.get("processados", []))
    total_arquivos = len(arquivos_novos)
    progresso_pct = (total_processados / total_arquivos * 100) if total_arquivos > 0 else 0
    
    print(f"\n🎯 STATUS GERAL:")
    print(f"   📈 Progresso: {progresso_pct:.1f}% ({total_processados}/{total_arquivos})")
    print(f"   ⏳ Restantes: {total_arquivos - total_processados} arquivo(s)")
    
    if total_processados < total_arquivos:
        print(f"\n⚡ Para continuar, execute novamente:")
        print(f"   python3 processar_novos_arquivos.py")

if __name__ == "__main__":
    print("🎙️  TRANSCRIÇÃO DE NOVOS ARQUIVOS - WHISPER")
    print("Processando cursos de Lynda, MasterClass, Pluralsight e LinkedIn Learning")
    print("=" * 70)
    
    # Processar 3 arquivos por vez para evitar timeout
    processar_lote(3)