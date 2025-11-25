#!/usr/bin/env python3
"""
Versão simplificada para processar áudio russo
Tenta usar Whisper já instalado ou instala sem cache
"""

import os
import sys
import subprocess
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
            print(f"✅ Sucesso")
            return True, result.stdout
        else:
            print(f"❌ Erro: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ Exceção: {e}")
        return False, str(e)

def check_whisper_installed():
    """Verifica se Whisper já está instalado"""
    try:
        import whisper
        print("✅ Whisper já está instalado!")
        return True
    except ImportError:
        print("❌ Whisper não encontrado")
        return False

def install_whisper_no_cache():
    """Instala Whisper sem usar cache"""
    print("📦 Instalando Whisper sem cache...")
    cmd = "pip install --no-cache-dir openai-whisper"
    return run_command(cmd)

def process_audio_direct(input_file, output_dir):
    """Processa áudio diretamente com Python"""
    print("🎵 Processando áudio com Python...")
    
    # Converter caminhos para formato seguro
    input_file_str = str(input_file).replace('\\', '/')
    output_dir_str = str(output_dir).replace('\\', '/')
    
    # Script Python para processar
    script = f'''
import whisper
import os

# Carregar modelo
print("Carregando modelo Whisper...")
model = whisper.load_model("base")

# Processar arquivo
print("Processando áudio...")
result = model.transcribe(
    r"{input_file_str}",
    language="ru",
    verbose=True
)

# Salvar resultado
output_file = os.path.join(r"{output_dir_str}", "transcricao_russo.txt")
with open(output_file, "w", encoding="utf-8") as f:
    f.write(result["text"])

print(f"Resultado salvo em: {{output_file}}")
print("\\nTranscrição:")
print("=" * 50)
print(result["text"])
print("=" * 50)
'''
    
    # Salvar script temporário
    temp_script = "temp_whisper.py"
    with open(temp_script, "w", encoding="utf-8") as f:
        f.write(script)
    
    # Executar script
    success, result = run_command(f"python {temp_script}")
    
    # Limpar arquivo temporário
    if os.path.exists(temp_script):
        os.remove(temp_script)
    
    return success, result

def main():
    print("🇷🇺 Processador Simplificado de Áudio Russo")
    print("=" * 50)
    
    # Caminhos
    base_dir = Path("C:/Users/Admin/Videos/1-PaddleSpeech")
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
    
    # Usar o arquivo maior
    input_file = max(input_files, key=lambda x: x.stat().st_size)
    print(f"\n🎵 Processando: {input_file.name}")
    
    # Criar diretório de saída
    output_dir.mkdir(exist_ok=True)
    
    # Verificar se Whisper já está instalado
    if not check_whisper_installed():
        # Tentar instalar sem cache
        if not install_whisper_no_cache():
            print("❌ Não foi possível instalar Whisper")
            print("💡 Tente executar como administrador ou use:")
            print("   pip install --user openai-whisper")
            return 1
    
    # Processar áudio
    success, result = process_audio_direct(input_file, output_dir)
    
    if success:
        print("✅ Processamento concluído!")
        print(f"📁 Resultados em: {output_dir}")
        
        # Verificar arquivo gerado
        output_file = output_dir / "transcricao_russo.txt"
        if output_file.exists():
            print(f"📄 Arquivo gerado: {output_file.name}")
            # Mostrar primeiras linhas
            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()
                if content.strip():
                    print("\n📋 Primeiras linhas da transcrição:")
                    print("=" * 40)
                    lines = content.split('\n')[:5]
                    for line in lines:
                        if line.strip():
                            print(line)
                    print("=" * 40)
                else:
                    print("⚠️ Arquivo vazio - verifique se o áudio contém fala")
    else:
        print("❌ Erro no processamento")
        print(f"Detalhes: {result}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())