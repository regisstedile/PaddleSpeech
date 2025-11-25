#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 SCRIPT FINAL DE TRANSCRIÇÃO COM SRT - USE ESTE!
==================================================

Este é o script principal para transcrição de áudio.
Funciona perfeitamente no Windows com o ambiente whisper_nocache.
Exporta tanto arquivo TXT quanto SRT sincronizado com o áudio.

Como usar:
1. Ative o ambiente: whisper_nocache\Scripts\Activate.ps1
2. Execute: python USAR_ESTE_SCRIPT.py
3. Aguarde o processamento (pode demorar alguns minutos)
4. Resultado aparece na pasta OUTPUT (TXT e SRT)
"""

import os
import sys
import glob
from pathlib import Path
import time
import io

# Garantir que a saída não quebre em consoles sem UTF-8
# Ignora caracteres não representáveis em cp1252 (ex.: ✓, emojis)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=(sys.stdout.encoding or 'utf-8'), errors='ignore')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding=(sys.stderr.encoding or 'utf-8'), errors='ignore')

def print_header():
    print("=" * 60)
    print("    SISTEMA DE TRANSCRICAO COM SRT - PROJETO ORGANIZADO")
    print("=" * 60)
    print(f"Python: {sys.executable}")
    print(f"Diretorio: {os.getcwd()}")
    print()

def check_whisper():
    """Verifica se Whisper está disponível"""
    try:
        import whisper
        print("✓ Whisper: OK")
        return True
    except ImportError:
        print("✗ Whisper: ERRO - nao encontrado")
        print("  Instale com: pip install openai-whisper")
        return False

def find_audio_files():
    """Encontra arquivos de áudio para processar"""
    input_dirs = [
        "INPUT",
        os.path.join("PaddleSpeech", "INPUT")
    ]
    
    audio_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg']
    audio_files = []
    
    print("Procurando arquivos de audio...")
    for input_dir in input_dirs:
        if os.path.exists(input_dir):
            for ext in audio_extensions:
                pattern = os.path.join(input_dir, f"*{ext}")
                files = glob.glob(pattern)
                audio_files.extend(files)
            print(f"✓ {input_dir}: {len([f for f in os.listdir(input_dir) if any(f.lower().endswith(ext) for ext in audio_extensions)])} arquivo(s)")
        else:
            print(f"✗ {input_dir}: pasta nao encontrada")
    
    return audio_files

def format_timestamp(seconds):
    """Converte segundos para formato SRT (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def create_srt_from_segments(segments):
    """Cria conteúdo SRT a partir dos segmentos do Whisper"""
    srt_content = []
    subtitle_index = 1
    
    for segment in segments:
        start_time = format_timestamp(segment["start"])
        end_time = format_timestamp(segment["end"])
        text = segment["text"].strip()
        
        # Adicionar entrada SRT
        srt_content.append(f"{subtitle_index}")
        srt_content.append(f"{start_time} --> {end_time}")
        srt_content.append(text)
        srt_content.append("")  # Linha em branco entre legendas
        
        subtitle_index += 1
    
    return "\n".join(srt_content)

def transcribe_audio(audio_file):
    """Transcreve um arquivo de áudio e gera TXT e SRT"""
    import whisper
    
    filename = Path(audio_file).stem
    output_dir = "OUTPUT"
    os.makedirs(output_dir, exist_ok=True)
    
    output_txt = os.path.join(output_dir, f"{filename}_transcricao.txt")
    output_srt = os.path.join(output_dir, f"{filename}_transcricao.srt")
    
    # Verificar se já existe
    if os.path.exists(output_txt) and os.path.exists(output_srt):
        print(f"  >> Arquivo ja processado: {os.path.basename(output_txt)}")
        print(f"  >> Arquivo ja processado: {os.path.basename(output_srt)}")
        return True, output_txt
    
    print(f"  >> Carregando modelo Whisper...")
    try:
        # Usar modelo tiny para ser mais rápido
        model = whisper.load_model("tiny")
        print(f"  >> Modelo carregado (tiny - mais rapido)")
    except Exception as e:
        print(f"  >> ERRO ao carregar modelo: {e}")
        return False, None
    
    print(f"  >> Iniciando transcricao...")
    print(f"  >> NOTA: Modelo 'tiny' - processo mais rapido, qualidade boa")
    
    try:
        start_time = time.time()
        
        # Transcrever com segmentos para gerar SRT
        result = model.transcribe(
            audio_file,
            language="en",  # Mude para "pt" se for português
            word_timestamps=False,
            verbose=False
        )
        
        # Salvar arquivo TXT (texto completo)
        text = result["text"].strip()
        with open(output_txt, 'w', encoding='utf-8') as f:
            f.write(text)
        
        # Salvar arquivo SRT (legendas sincronizadas)
        if "segments" in result and len(result["segments"]) > 0:
            srt_content = create_srt_from_segments(result["segments"])
            with open(output_srt, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            print(f"  >> ✓ Arquivo SRT salvo: {os.path.basename(output_srt)}")
        else:
            # Se não houver segmentos, criar SRT básico com todo o texto
            print(f"  >> ⚠ Aviso: Nenhum segmento encontrado, criando SRT basico")
            # Tentar obter duração do áudio
            try:
                import whisper.audio as audio_module
                audio_data = audio_module.load_audio(audio_file)
                duration = len(audio_data) / 16000.0  # Whisper usa 16kHz
            except:
                duration = 0
            
            if duration > 0:
                srt_content = f"1\n{format_timestamp(0)} --> {format_timestamp(duration)}\n{text}\n"
                with open(output_srt, 'w', encoding='utf-8') as f:
                    f.write(srt_content)
                print(f"  >> ✓ Arquivo SRT basico salvo: {os.path.basename(output_srt)}")
            else:
                print(f"  >> ⚠ Nao foi possivel criar SRT (duracao desconhecida)")
        
        duration = time.time() - start_time
        
        print(f"  >> ✓ Concluido em {duration:.1f} segundos")
        print(f"  >> ✓ Arquivo TXT salvo: {os.path.basename(output_txt)}")
        print(f"  >> ✓ Tamanho: {len(text)} caracteres")
        
        return True, output_txt
        
    except Exception as e:
        print(f"  >> ERRO na transcricao: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def main():
    print_header()
    
    # Verificar Whisper
    if not check_whisper():
        print("\nERRO: Whisper nao esta disponivel!")
        print("Execute no ambiente correto:")
        print("  whisper_nocache\\Scripts\\Activate.ps1")
        print("  pip install openai-whisper")
        return
    
    # Encontrar arquivos
    audio_files = find_audio_files()
    
    if not audio_files:
        print("\nERRO: Nenhum arquivo de audio encontrado!")
        print("Coloque arquivos .mp3/.wav/.m4a nas pastas:")
        print("  - INPUT/")
        print("  - PaddleSpeech/INPUT/")
        return
    
    print(f"\n📁 Encontrados {len(audio_files)} arquivo(s) para processar:")
    for i, f in enumerate(audio_files, 1):
        size_mb = os.path.getsize(f) / (1024 * 1024)
        print(f"  {i}. {os.path.basename(f)} ({size_mb:.1f} MB)")
    
    print(f"\n🎯 Iniciando processamento...")
    print("=" * 60)
    
    # Processar cada arquivo
    success_count = 0
    total_files = len(audio_files)
    
    for i, audio_file in enumerate(audio_files, 1):
        print(f"\n[{i}/{total_files}] {os.path.basename(audio_file)}")
        
        success, output_file = transcribe_audio(audio_file)
        
        if success:
            success_count += 1
        
        # Pausa entre arquivos
        if i < total_files:
            time.sleep(1)
    
    # Resumo final
    print("\n" + "=" * 60)
    print("📊 RESUMO FINAL")
    print("=" * 60)
    print(f"✓ Processados com sucesso: {success_count}")
    print(f"✗ Falhas: {total_files - success_count}")
    print(f"📁 Total: {total_files}")
    
    if success_count > 0:
        print(f"\n📂 Arquivos de saida na pasta: {os.path.abspath('OUTPUT')}")
        
        # Listar arquivos criados
        txt_files = glob.glob(os.path.join("OUTPUT", "*_transcricao.txt"))
        srt_files = glob.glob(os.path.join("OUTPUT", "*_transcricao.srt"))
        
        if txt_files or srt_files:
            print(f"\n📝 Arquivos criados:")
            for txt_file in txt_files:
                size = os.path.getsize(txt_file)
                print(f"  - {os.path.basename(txt_file)} ({size} bytes)")
            for srt_file in srt_files:
                size = os.path.getsize(srt_file)
                print(f"  - {os.path.basename(srt_file)} ({size} bytes)")
    
    print(f"\n🎉 Processamento concluido!")
    
    if success_count == total_files:
        print("✅ Todos os arquivos foram processados com sucesso!")
    elif success_count > 0:
        print(f"⚠️  {success_count} de {total_files} arquivos processados.")
    else:
        print("❌ Nenhum arquivo foi processado com sucesso.")
    
    print("\n💡 Para usar novamente:")
    print("  1. Coloque novos arquivos nas pastas INPUT")
    print("  2. Execute: python USAR_ESTE_SCRIPT.py")
    print("\n📌 NOTA: Este script agora gera tanto TXT quanto SRT sincronizado!")

if __name__ == "__main__":
    main()
