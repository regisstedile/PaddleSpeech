#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador de Novos Arquivos para Transcrição
==============================================
Identifica arquivos de áudio que ainda não foram processados.
"""
import os
import glob

def verificar_arquivos_novos():
    """
    Verifica quais arquivos ainda não foram processados.
    """
    # Diretórios
    input_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/PaddleSpeech/INPUT"
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    
    print("🔍 VERIFICANDO NOVOS ARQUIVOS PARA TRANSCRIÇÃO")
    print("=" * 60)
    
    # Encontrar todos os arquivos de áudio
    audio_extensions = ['*.mp3', '*.mp4', '*.wav', '*.m4a', '*.wmv', '*.avi']
    arquivos_audio = []
    
    for ext in audio_extensions:
        arquivos_audio.extend(glob.glob(os.path.join(input_dir, ext)))
    
    print(f"📁 Total de arquivos de áudio encontrados: {len(arquivos_audio)}")
    
    # Verificar quais já foram processados
    arquivos_processados = []
    arquivos_nao_processados = []
    
    for arquivo_audio in arquivos_audio:
        nome_base = os.path.splitext(os.path.basename(arquivo_audio))[0]
        
        # Verificar se existe arquivo SRT correspondente
        arquivo_srt = os.path.join(output_dir, f"{nome_base}.srt")
        arquivo_txt = os.path.join(output_dir, f"{nome_base}.txt")
        
        if os.path.exists(arquivo_srt) or os.path.exists(arquivo_txt):
            arquivos_processados.append(nome_base)
        else:
            arquivos_nao_processados.append(arquivo_audio)
    
    print(f"✅ Arquivos já processados: {len(arquivos_processados)}")
    print(f"⏳ Arquivos pendentes: {len(arquivos_nao_processados)}")
    print()
    
    # Mostrar arquivos novos para processar
    if arquivos_nao_processados:
        print("📋 NOVOS ARQUIVOS PARA TRANSCREVER:")
        print("-" * 50)
        for i, arquivo in enumerate(arquivos_nao_processados, 1):
            nome = os.path.basename(arquivo)
            tamanho = os.path.getsize(arquivo) / (1024*1024)  # MB
            print(f"{i:2d}. {nome}")
            print(f"    📏 Tamanho: {tamanho:.1f} MB")
            print()
        
        print("=" * 60)
        print(f"🎯 TOTAL DE NOVOS ARQUIVOS: {len(arquivos_nao_processados)}")
        
        # Categorizar por fonte/tipo
        categorias = {}
        for arquivo in arquivos_nao_processados:
            nome = os.path.basename(arquivo)
            if "Lynda" in nome:
                categoria = "Lynda"
            elif "MasterClass" in nome:
                categoria = "MasterClass"
            elif "Pluralsight" in nome:
                categoria = "Pluralsight"
            elif "LinkedIn" in nome or "Linkedin" in nome:
                categoria = "LinkedIn Learning"
            elif "Train Simple" in nome:
                categoria = "Train Simple"
            else:
                categoria = "Outros"
            
            if categoria not in categorias:
                categorias[categoria] = []
            categorias[categoria].append(nome)
        
        print("\n📊 CATEGORIAS DOS NOVOS ARQUIVOS:")
        for categoria, arquivos in categorias.items():
            print(f"   {categoria}: {len(arquivos)} arquivo(s)")
        
        return arquivos_nao_processados
    else:
        print("🎉 Todos os arquivos já foram processados!")
        return []

if __name__ == "__main__":
    novos_arquivos = verificar_arquivos_novos()
    
    if novos_arquivos:
        print(f"\n⚡ Para processar os novos arquivos, execute:")
        print(f"   python3 processar_novos_arquivos.py")