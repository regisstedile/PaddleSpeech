#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conversor SRT para TXT - Texto Limpo
====================================
Converte arquivos SRT para TXT removendo timestamps e numeração,
mantendo apenas o texto limpo e legível.
"""
import os
import re
import glob

def converter_srt_para_txt(arquivo_srt):
    """
    Converte um arquivo SRT para TXT removendo timestamps e numeração.
    """
    if not os.path.exists(arquivo_srt):
        print(f"❌ Arquivo não encontrado: {arquivo_srt}")
        return False
    
    try:
        # Ler o arquivo SRT
        with open(arquivo_srt, 'r', encoding='utf-8') as f:
            conteudo_srt = f.read()
        
        # Processar o conteúdo SRT
        linhas = conteudo_srt.split('\n')
        texto_limpo = []
        
        for linha in linhas:
            linha = linha.strip()
            
            # Pular linhas vazias
            if not linha:
                continue
            
            # Pular números de sequência (apenas números)
            if linha.isdigit():
                continue
            
            # Pular timestamps (formato: 00:00:00,000 --> 00:00:00,000)
            if '-->' in linha and ':' in linha:
                continue
            
            # Adicionar texto limpo
            if linha:
                texto_limpo.append(linha)
        
        # Juntar o texto com espaços
        texto_final = ' '.join(texto_limpo)
        
        # Limpar espaços duplos e formatação
        texto_final = re.sub(r'\s+', ' ', texto_final)
        texto_final = texto_final.strip()
        
        # Criar arquivo TXT
        nome_base = os.path.splitext(arquivo_srt)[0]
        arquivo_txt = f"{nome_base}.txt"
        
        with open(arquivo_txt, 'w', encoding='utf-8') as f:
            f.write(texto_final)
        
        print(f"✅ Convertido: {os.path.basename(arquivo_srt)} → {os.path.basename(arquivo_txt)}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao converter {arquivo_srt}: {str(e)}")
        return False

def processar_todos_srt():
    """
    Processa todos os arquivos SRT na pasta OUTPUT.
    """
    # Diretório de saída
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    
    if not os.path.exists(output_dir):
        print(f"❌ Diretório não encontrado: {output_dir}")
        return
    
    # Encontrar todos os arquivos SRT
    arquivos_srt = glob.glob(os.path.join(output_dir, "*.srt"))
    
    if not arquivos_srt:
        print("❌ Nenhum arquivo SRT encontrado!")
        return
    
    print(f"🎯 Encontrados {len(arquivos_srt)} arquivos SRT para converter")
    print("=" * 60)
    
    sucessos = 0
    falhas = 0
    
    for arquivo_srt in sorted(arquivos_srt):
        if converter_srt_para_txt(arquivo_srt):
            sucessos += 1
        else:
            falhas += 1
    
    print("=" * 60)
    print(f"📊 RESULTADO DA CONVERSÃO:")
    print(f"   ✅ Sucessos: {sucessos}")
    print(f"   ❌ Falhas: {falhas}")
    print(f"   📁 Total: {len(arquivos_srt)}")
    
    if sucessos > 0:
        print(f"\n🎉 {sucessos} arquivos TXT criados com sucesso!")
        print(f"📂 Arquivos salvos em: {output_dir}")

def mostrar_exemplo():
    """
    Mostra um exemplo de conversão para verificar qualidade.
    """
    output_dir = "/mnt/c/Users/Admin/Videos/1-PaddleSpeech/OUTPUT"
    arquivos_txt = glob.glob(os.path.join(output_dir, "*.txt"))
    
    if arquivos_txt:
        arquivo_exemplo = arquivos_txt[0]
        print(f"\n📄 EXEMPLO DE CONVERSÃO:")
        print(f"   Arquivo: {os.path.basename(arquivo_exemplo)}")
        print("-" * 50)
        
        try:
            with open(arquivo_exemplo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            # Mostrar primeiros 300 caracteres
            if len(conteudo) > 300:
                print(conteudo[:300] + "...")
            else:
                print(conteudo)
                
        except Exception as e:
            print(f"❌ Erro ao ler exemplo: {e}")

if __name__ == "__main__":
    print("🔄 CONVERSOR SRT PARA TXT")
    print("=" * 40)
    
    # Processar todos os arquivos
    processar_todos_srt()
    
    # Mostrar exemplo
    mostrar_exemplo()