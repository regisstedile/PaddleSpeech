# 🔧 Configuração do Ambiente Virtual

## 📋 Ambiente Recomendado

O projeto agora usa um **único ambiente virtual** chamado `.venv/`

## 🚀 Criação do Ambiente (Windows)

```powershell
# 1. Criar ambiente virtual
python -m venv .venv

# 2. Ativar ambiente
.\.venv\Scripts\Activate.ps1

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Instalar projeto em modo desenvolvimento
pip install -e .
```

## 🐧 Criação do Ambiente (Linux/WSL)

```bash
# 1. Criar ambiente virtual
python3 -m venv .venv

# 2. Ativar ambiente
source .venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Instalar projeto em modo desenvolvimento
pip install -e .
```

## 📦 Dependências Principais

- **openai-whisper** - Engine de transcrição
- **torch** - Framework de deep learning
- **ffmpeg-python** - Processamento de áudio
- **tqdm** - Barras de progresso

## ⚠️ Ambientes Antigos Removidos

Os seguintes ambientes duplicados foram removidos:
- `whisper_compativel/` (1.5GB)
- `whisper_nocache/` (1.7GB)
- `whisper_russo_env/` (1.4GB)
- `paddlespeech_env/`

**Total economizado:** ~4.6GB de espaço em disco

## 🔄 Migração de Ambiente Antigo

Se você tinha scripts que usavam o ambiente antigo:

**Antes:**
```powershell
& c:/Users/Admin/Videos/2-PaddleSpeech/whisper_nocache/Scripts/Activate.ps1
```

**Depois:**
```powershell
.\.venv\Scripts\Activate.ps1
```

## 📝 Verificação

Para verificar se o ambiente está correto:

```bash
# Verificar Python
python --version

# Verificar Whisper
python -c "import whisper; print('Whisper OK')"

# Listar pacotes instalados
pip list
```

## 💡 Dicas

1. **Sempre ative o ambiente** antes de usar os scripts
2. **Use o mesmo ambiente** para todo o projeto
3. **Não commite .venv/** no git (já está no .gitignore)
4. **Atualize dependências** com: `pip install -r requirements.txt --upgrade`
