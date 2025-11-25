#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processador de Arquivo Único - Teste
===================================
Processa um arquivo específico para testar o funcionamento.
"""
import os
import sys
import subprocess

def processar_arquivo_especifico():
    """Processa o primeiro arquivo da lista para teste."""
    
    # Arquivo para teste (o menor disponível)
    arquivo = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/PaddleSpeech/INPUT/Lynda - Innovative Customer Service Techniques.mp3"
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    
    if not os.path.exists(arquivo):
        print(f"❌ Arquivo não encontrado: {arquivo}")
        return False
    
    # Criar diretório de saída
    os.makedirs(output_dir, exist_ok=True)
    
    nome_arquivo = os.path.basename(arquivo)
    tamanho_mb = os.path.getsize(arquivo) / (1024*1024)
    
    print(f"🎵 TESTE DE TRANSCRIÇÃO")
    print("=" * 50)
    print(f"📄 Arquivo: {nome_arquivo}")
    print(f"📏 Tamanho: {tamanho_mb:.1f} MB")
    print(f"📁 Saída: {output_dir}")
    print()
    
    try:
        # Comando Whisper
        cmd = [
            sys.executable, '-m', 'whisper', arquivo,
            '--language', 'en',
            '--model', 'base',
            '--output_dir', output_dir,
            '--output_format', 'srt',
            '--fp16', 'False'  # Desabilitar FP16 para compatibilidade
        ]
        
        print("⚙️  Executando comando Whisper...")
        print(f"   {' '.join(cmd[:5])}...")
        
        resultado = subprocess.run(cmd, capture_output=True, text=True)
        
        if resultado.returncode == 0:
            print("✅ Transcrição concluída com sucesso!")
            
            # Verificar arquivos criados
            nome_base = os.path.splitext(nome_arquivo)[0] 
            arquivo_srt = os.path.join(output_dir, f"{nome_base}.srt")
            
            if os.path.exists(arquivo_srt):
                print(f"📄 Arquivo SRT criado: {os.path.basename(arquivo_srt)}")
                
                # Mostrar primeiras linhas
                try:
                    with open(arquivo_srt, 'r', encoding='utf-8') as f:
                        conteudo = f.read()
                    
                    linhas = conteudo.split('\n')[:10]
                    print("\n📋 PRÉVIA DO RESULTADO:")
                    print("-" * 30)
                    for linha in linhas:
                        if linha.strip():
                            print(linha)
                    print("-" * 30)
                    
                except Exception as e:
                    print(f"⚠️  Erro ao ler arquivo: {e}")
                
                return True
            else:
                print("❌ Arquivo SRT não foi criado")
                return False
                
        else:
            print(f"❌ Erro na transcrição:")
            print(f"   Return code: {resultado.returncode}")
            if resultado.stderr:
                print(f"   Stderr: {resultado.stderr[:500]}")
            if resultado.stdout:
                print(f"   Stdout: {resultado.stdout[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        return False

if __name__ == "__main__":
    processar_arquivo_especifico()