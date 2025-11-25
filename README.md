# 🎙️ Audio Transcription System

Sistema profissional de transcrição de áudio usando **OpenAI Whisper** com geração automática de legendas SRT.

## ⚡ Quick Start

```bash
# 1. Criar ambiente virtual
python -m venv .venv

# 2. Ativar ambiente (Windows)
.\.venv\Scripts\Activate.ps1

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Colocar arquivos de áudio em INPUT/

# 5. Executar transcrição
python src/transcribe.py
```

## 📁 Estrutura do Projeto

```
2-PaddleSpeech/
├── src/                          # Código fonte
│   ├── transcribe.py            # 🎯 Script principal de transcrição
│   ├── transcribe_linux.py      # Versão para Linux/WSL
│   ├── translate.py             # Tradução de transcrições
│   └── utils/                   # Utilitários
├── scripts/                      # Scripts de automação
│   ├── windows/                 # Scripts .bat (Windows)
│   ├── linux/                   # Scripts .sh (Linux)
│   └── deprecated/              # Scripts antigos (backup)
├── INPUT/                        # 📥 Coloque arquivos de áudio aqui
├── OUTPUT/                       # 📤 Transcrições geradas (TXT + SRT)
├── docs/                         # 📚 Documentação
│   ├── AMBIENTE_VIRTUAL.md      # Setup do ambiente
│   ├── COMO_USAR.txt            # Guia de uso
│   └── reports/                 # Relatórios históricos
├── tests/                        # Testes automatizados
├── logs/                         # Logs do sistema
├── .venv/                        # Ambiente virtual (não commitado)
├── requirements.txt              # Dependências Python
├── setup.py                      # Instalação do projeto
├── .gitignore                    # Arquivos ignorados pelo Git
└── README.md                     # Este arquivo
```

## 🎯 Funcionalidades

- ✅ **Transcrição automática** de áudio para texto
- ✅ **Geração de legendas SRT** sincronizadas
- ✅ **Múltiplos formatos** (MP3, WAV, M4A, FLAC, OGG)
- ✅ **Suporte multilíngue** (90+ idiomas)
- ✅ **Processamento em lote** de múltiplos arquivos
- ✅ **Interface clara** com progresso em tempo real
- ✅ **Tradução de transcrições** (opcional)

## 📦 Dependências Principais

| Pacote | Versão | Descrição |
|--------|--------|-----------|
| openai-whisper | >=20230314 | Engine de transcrição de áudio |
| torch | >=2.0.0 | Framework de deep learning |
| ffmpeg-python | >=0.2.0 | Processamento de áudio |
| tqdm | >=4.65.0 | Barras de progresso |

## 🚀 Uso Básico

### Transcrição Simples

```bash
# Ativar ambiente
.\.venv\Scripts\Activate.ps1  # Windows
# ou
source .venv/bin/activate      # Linux

# Executar transcrição
python src/transcribe.py
```

### Transcrição com Configuração

```python
import whisper

# Carregar modelo
model = whisper.load_model("base")

# Transcrever
result = model.transcribe(
    "INPUT/audio.mp3",
    language="pt",  # Português
    task="transcribe"
)

# Salvar resultado
with open("OUTPUT/transcricao.txt", "w") as f:
    f.write(result["text"])
```

## 🎚️ Modelos Disponíveis

| Modelo | Tamanho | VRAM | Velocidade | Qualidade |
|--------|---------|------|------------|-----------|
| tiny   | 39M     | ~1GB | 32x        | ⭐⭐ |
| base   | 74M     | ~1GB | 16x        | ⭐⭐⭐ |
| small  | 244M    | ~2GB | 6x         | ⭐⭐⭐⭐ |
| medium | 769M    | ~5GB | 2x         | ⭐⭐⭐⭐⭐ |
| large  | 1550M   | ~10GB| 1x         | ⭐⭐⭐⭐⭐⭐ |

**Recomendação:** Use `base` para balance qualidade/velocidade

## 📊 Performance Esperada

| Duração Audio | Tamanho | Tempo (base) | Tempo (tiny) |
|---------------|---------|--------------|--------------|
| 10 min        | ~10MB   | 2-3 min      | 1-2 min      |
| 30 min        | ~30MB   | 5-8 min      | 2-4 min      |
| 60 min        | ~60MB   | 10-15 min    | 5-8 min      |
| 90 min        | ~130MB  | 15-25 min    | 8-15 min     |

## 🌍 Idiomas Suportados

Alguns dos 90+ idiomas suportados:
- `pt` - Português
- `en` - Inglês
- `es` - Espanhol
- `fr` - Francês
- `de` - Alemão
- `it` - Italiano
- `ru` - Russo
- `zh` - Chinês
- `ja` - Japonês
- `ko` - Coreano

## 🔧 Configuração Avançada

### Variáveis de Ambiente

```bash
# Desabilitar cache de modelos (opcional)
export WHISPER_CACHE_DIR=""

# Forçar CPU (sem GPU)
export CUDA_VISIBLE_DEVICES=""
```

### Script Personalizado

```python
from pathlib import Path
import whisper

def transcribe_batch(input_dir, output_dir, model="base", language="en"):
    """Transcreve múltiplos arquivos"""
    model = whisper.load_model(model)

    for audio_file in Path(input_dir).glob("*.mp3"):
        result = model.transcribe(str(audio_file), language=language)

        # Salvar TXT
        txt_path = Path(output_dir) / f"{audio_file.stem}.txt"
        txt_path.write_text(result["text"], encoding="utf-8")

        print(f"✓ {audio_file.name} -> {txt_path.name}")
```

## 📚 Documentação Adicional

- [`docs/AMBIENTE_VIRTUAL.md`](docs/AMBIENTE_VIRTUAL.md) - Setup do ambiente virtual
- [`docs/COMO_USAR.txt`](docs/COMO_USAR.txt) - Guia de uso detalhado
- [`docs/README_PROJETO_ORGANIZADO.md`](docs/README_PROJETO_ORGANIZADO.md) - Histórico do projeto

## 🛠️ Desenvolvimento

### Executar Testes

```bash
pytest tests/
```

### Formatação de Código

```bash
black src/
flake8 src/
```

### Instalar em Modo Desenvolvimento

```bash
pip install -e .[dev]
```

## 📋 Changelog

### v1.0.0 (2025-01-25)
- ✅ Reorganização completa do projeto
- ✅ Estrutura profissional de diretórios
- ✅ Consolidação de scripts
- ✅ Documentação atualizada
- ✅ Remoção de ambientes duplicados (~4.6GB economizados)
- ✅ Sistema de build com setup.py
- ✅ .gitignore configurado

### Versões Anteriores
- Múltiplos ambientes virtuais (removidos)
- Scripts dispersos (consolidados)
- PaddleSpeech clonado (removido - deve ser pip install se necessário)

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é de uso interno. Consulte os termos de uso do OpenAI Whisper para distribuição.

## 🙏 Créditos

- **OpenAI Whisper** - https://github.com/openai/whisper
- **PyTorch** - https://pytorch.org/
- **FFmpeg** - https://ffmpeg.org/

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a documentação em `docs/`
2. Consulte os scripts de exemplo em `scripts/deprecated/`
3. Revise os logs em `logs/`

---

**Status:** ✅ Projeto reorganizado e funcional
**Última atualização:** 2025-01-25
**Versão:** 1.0.0
