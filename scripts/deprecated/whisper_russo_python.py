#!/usr/bin/env python3
"""
Script Python para processar áudio russo com Whisper
Solução alternativa para problemas de permissão no Windows
"""

import os
import sys
import subprocess
import venv
from pathlib import Path

def run_command(cmd, cwd=None):
    """Executa comando com tratamento de erro"""
    try:
        print(f"Executando: {cmd}")
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            cwd=cwd
        )
        if result.returncode == 0:
            print(f"✅ Sucesso: {result.stdout}")
            return True, result.stdout
        else:
            print(f"❌ Erro: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ Exceção: {e}")
        return False, str(e)

def create_venv(venv_path):
    """Cria ambiente virtual"""
    print(f"Criando ambiente virtual em: {venv_path}")
    venv.create(venv_path, with_pip=True)
    return True

def install_whisper(venv_path):
    """Instala Whisper no ambiente virtual"""
    # Ativar ambiente e instalar
    if os.name == 'nt':  # Windows
        python_path = os.path.join(venv_path, 'Scripts', 'python.exe')
        pip_path = os.path.join(venv_path, 'Scripts', 'pip.exe')
    else:  # Linux/Mac
        python_path = os.path.join(venv_path, 'bin', 'python')
        pip_path = os.path.join(venv_path, 'bin', 'pip')
    
    # Atualizar pip
    success, _ = run_command(f'"{pip_path}" install --upgrade pip')
    if not success:
        return False
    
    # Instalar Whisper
    success, _ = run_command(f'"{pip_path}" install openai-whisper')
    return success

def process_audio(venv_path, input_file, output_dir):
    """Processa o áudio com Whisper"""
    if os.name == 'nt':  # Windows
        python_path = os.path.join(venv_path, 'Scripts', 'python.exe')
    else:  # Linux/Mac
        python_path = os.path.join(venv_path, 'bin', 'python')
    
    # Comando Whisper
    cmd = f'"{python_path}" -m whisper "{input_file}" --language ru --output_dir "{output_dir}" --model base'
    return run_command(cmd)

def main():
    print("🇷🇺 Processador de Áudio Russo com Whisper")
    print("=" * 50)
    
    # Caminhos
    base_dir = Path("C:/Users/Admin/Videos/1-PaddleSpeech")
    venv_path = base_dir / "whisper_russo_env"
    input_dir = base_dir / "INPUT"
    output_dir = base_dir / "OUTPUT"
    
    # Verificar arquivos disponíveis
    input_files = list(input_dir.glob("*.mp3"))
    if not input_files:
        print(f"❌ Nenhum arquivo MP3 encontrado em: {input_dir}")
        return 1
    
    print(f"📁 Arquivos encontrados:")
    for i, file in enumerate(input_files, 1):
        print(f"  {i}. {file.name} ({file.stat().st_size / (1024*1024):.1f}MB)")
    
    # Usar o primeiro arquivo (maior)
    input_file = max(input_files, key=lambda x: x.stat().st_size)
    print(f"\n🎵 Processando: {input_file.name}")
    
    # Criar diretório de saída
    output_dir.mkdir(exist_ok=True)
    
    print(f"📁 Saída: {output_dir}")
    
    # Criar ambiente virtual se não existir
    if not venv_path.exists():
        print("🔧 Criando ambiente virtual...")
        create_venv(venv_path)
    
    # Instalar Whisper
    print("📦 Instalando Whisper...")
    if not install_whisper(venv_path):
        print("❌ Falha na instalação do Whisper")
        return 1
    
    # Processar áudio
    print("🎵 Processando áudio...")
    success, result = process_audio(venv_path, input_file, output_dir)
    
    if success:
        print("✅ Processamento concluído!")
        print(f"📁 Resultados em: {output_dir}")
        
        # Listar arquivos gerados
        output_files = list(output_dir.glob("*"))
        if output_files:
            print("\n📋 Arquivos gerados:")
            for file in output_files:
                print(f"  - {file.name}")
    else:
        print("❌ Erro no processamento")
        print(f"Detalhes: {result}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())