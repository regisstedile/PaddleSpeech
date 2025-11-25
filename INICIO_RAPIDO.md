# ⚡ Início Rápido - Sistema de Transcrição

## 🚀 Setup em 5 Passos (2 minutos)

### 1️⃣ Criar Ambiente Virtual

**Windows:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/WSL:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

**Tempo:** ~2-5 minutos (depende da conexão)

### 3️⃣ Preparar Arquivos

Coloque seus arquivos de áudio em:
```
INPUT/
├── audio1.mp3
├── audio2.wav
└── video.m4a
```

**Formatos aceitos:** MP3, WAV, M4A, FLAC, OGG

### 4️⃣ Executar Transcrição

```bash
python src/transcribe.py
```

O script irá:
- ✅ Detectar arquivos automaticamente
- ✅ Processar cada arquivo
- ✅ Mostrar progresso em tempo real
- ✅ Gerar TXT + SRT em `OUTPUT/`

### 5️⃣ Verificar Resultados

```
OUTPUT/
├── audio1_transcricao.txt
├── audio1_transcricao.srt
├── audio2_transcricao.txt
└── audio2_transcricao.srt
```

---

## 🎯 Uso Avançado

### Transcrever Arquivo Específico

```bash
python -c "
import whisper
model = whisper.load_model('base')
result = model.transcribe('INPUT/meu_audio.mp3', language='pt')
with open('OUTPUT/resultado.txt', 'w') as f:
    f.write(result['text'])
"
```

### Escolher Modelo

**Modelos disponíveis:**
- `tiny` - Rápido (32x), qualidade básica
- `base` - **RECOMENDADO** (16x), boa qualidade
- `small` - Lento (6x), qualidade alta
- `medium` - Muito lento (2x), qualidade excelente
- `large` - Extremamente lento (1x), melhor qualidade

**Editar em `src/transcribe.py` linha 120:**
```python
model = whisper.load_model("base")  # Mudar aqui
```

### Escolher Idioma

**Editar em `src/transcribe.py` linha 135:**
```python
result = model.transcribe(
    audio_file,
    language="pt",  # Português
    # language="en",  # Inglês
    # language="es",  # Espanhol
```

---

## 🔧 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'whisper'"

**Solução:**
```bash
# Verificar se ambiente está ativo
# Windows: deve aparecer (.venv) no prompt
# Linux: deve aparecer (.venv) no prompt

# Reinstalar
pip install openai-whisper
```

### Erro: "ffmpeg not found"

**Windows:**
1. Baixar: https://www.gyan.dev/ffmpeg/builds/
2. Extrair para `C:\ffmpeg`
3. Adicionar ao PATH: `C:\ffmpeg\bin`

**Linux:**
```bash
sudo apt install ffmpeg
```

### Transcrição muito lenta

**Soluções:**
1. Use modelo `tiny` (mais rápido)
2. Verifique se GPU está disponível: `python -c "import torch; print(torch.cuda.is_available())"`
3. Reduza qualidade do áudio antes de transcrever

### Resultado com baixa qualidade

**Soluções:**
1. Use modelo `medium` ou `large`
2. Verifique qualidade do áudio original
3. Especifique idioma correto

---

## 📚 Documentação Completa

- **Guia Detalhado:** [`README.md`](README.md)
- **Setup Ambiente:** [`docs/AMBIENTE_VIRTUAL.md`](docs/AMBIENTE_VIRTUAL.md)
- **Reorganização:** [`docs/REORGANIZACAO_COMPLETA.md`](docs/REORGANIZACAO_COMPLETA.md)
- **Como Usar:** [`docs/COMO_USAR.txt`](docs/COMO_USAR.txt)

---

## 💡 Dicas

1. **Primeira vez?** Use modelo `tiny` para testar
2. **Produção?** Use modelo `base` ou `small`
3. **Múltiplos arquivos?** Coloque todos em `INPUT/`
4. **Arquivo já processado?** Script detecta e pula automaticamente
5. **Legendas?** Arquivos `.srt` são gerados automaticamente

---

## 📞 Suporte

**Problemas?**
1. Verifique [`docs/REORGANIZACAO_COMPLETA.md`](docs/REORGANIZACAO_COMPLETA.md)
2. Revise logs em `logs/`
3. Teste scripts de exemplo em `scripts/deprecated/`

---

**✅ Pronto para começar!**
**⏱️ Tempo total de setup:** ~5 minutos
**🎯 Próximo passo:** Coloque arquivos em `INPUT/` e execute `python src/transcribe.py`
