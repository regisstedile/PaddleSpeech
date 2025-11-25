#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Processamento de Múltiplos Arquivos em Sequência
"""

import os
import sys
import subprocess
import time

def process_next_files(count=5):
    """Processa os próximos N arquivos."""
    print(f"🎙️ Processando próximos {count} arquivos...")
    
    for i in range(count):
        print(f"\n📋 Arquivo {i+1}/{count}")
        print("=" * 40)
        
        try:
            # Execute o script de processamento individual
            result = subprocess.run([
                sys.executable, 'processar_continuo.py'
            ], capture_output=True, text=True, timeout=2000)
            
            print(result.stdout)
            
            if result.stderr:
                print("⚠️ Avisos:")
                print(result.stderr)
            
            if "Todos os arquivos já foram processados" in result.stdout:
                print("🎉 Processamento completo!")
                break
                
        except subprocess.TimeoutExpired:
            print("⏰ Timeout no arquivo atual - continuando...")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        # Pausa breve entre arquivos
        time.sleep(2)
    
    print(f"\n✅ Sessão de processamento concluída!")

if __name__ == "__main__":
    # Processa 5 arquivos por vez
    process_next_files(5)