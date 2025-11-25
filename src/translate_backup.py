#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Traduz todas as transcrições da pasta OUTPUT para PT-BR.
- Entrada: OUTPUT/*_transcricao.txt
- Saída:  OUTPUT/*_transcricao_pt.txt
Requisitos: transformers, sentencepiece (modelo Helsinki-NLP/opus-mt-en-pt) OU deep-translator.
"""

import os
import glob
import sys
import time
from pathlib import Path
from typing import List, Optional

CHUNK_CHARS = 900  # tamanho dos pedaços para evitar estouro do modelo


def chunk_text(text: str, chunk_size: int = CHUNK_CHARS) -> List[str]:
    text = text.strip()
    if not text:
        return []
    # Quebra preferindo espaços próximos do limite
    chunks, start = [], 0
    n = len(text)
    while start < n:
        end = min(start + chunk_size, n)
        if end < n:
            # recua até espaço/pontuação para evitar cortar palavras
            pivot = max(text.rfind(" ", start, end), text.rfind(". ", start, end), text.rfind("\n", start, end))
            if pivot == -1 or pivot <= start + int(chunk_size * 0.6):
                pivot = end
            end = pivot
        chunks.append(text[start:end].strip())
        start = end
    return [c for c in chunks if c]


# ————— Backend 1: HuggingFace Transformers —————

def ensure_hf() -> bool:
    try:
        import transformers  # noqa: F401
        import sentencepiece  # noqa: F401
        return True
    except Exception:
        return False


def load_hf_pipeline():
    from transformers import pipeline
    return pipeline(
        "translation_en_to_pt",
        model="Helsinki-NLP/opus-mt-en-pt",
        device=-1,
    )


def translate_text_hf(nlp, text: str) -> str:
    parts = chunk_text(text)
    out_parts: List[str] = []
    for i in range(0, len(parts), 16):  # processa em lotes para eficiência
        batch = parts[i:i+16]
        preds = nlp(batch, clean_up_tokenization_spaces=True)
        out_parts.extend(p["translation_text"].strip() for p in preds)
    return "\n\n".join(out_parts).strip()


# ————— Backend 2: deep-translator (Google / MyMemory) —————

def ensure_dt() -> bool:
    try:
        import deep_translator  # noqa: F401
        return True
    except Exception:
        return False


def load_dt_provider():
    # Tenta Google primeiro; se falhar, usa MyMemory
    try:
        from deep_translator import GoogleTranslator
        return ("google", GoogleTranslator(source="en", target="pt"))
    except Exception:
        pass
    from deep_translator import MyMemoryTranslator
    return ("mymemory", MyMemoryTranslator(source="en", target="pt"))


def translate_text_dt(provider, text: str) -> str:
    name, translator = provider
    parts = chunk_text(text, 4000 if name == "mymemory" else 1500)
    out: List[str] = []
    for ch in parts:
        out.append(translator.translate(ch))
        time.sleep(0.2)  # pequena pausa para evitar limites
    return "\n\n".join(out).strip()


def pick_translator():
    # 1) tenta HF
    if ensure_hf():
        try:
            nlp = load_hf_pipeline()
            return ("hf", nlp)
        except Exception as e:
            print(f"⚠️  Falha ao carregar modelo HF: {e}")
    # 2) tenta deep-translator
    if ensure_dt():
        try:
            provider = load_dt_provider()
            return ("dt", provider)
        except Exception as e:
            print(f"⚠️  Falha ao iniciar deep-translator: {e}")
    return (None, None)


def translate_any(translator, text: str) -> str:
    kind, obj = translator
    if kind == "hf":
        return translate_text_hf(obj, text)
    if kind == "dt":
        return translate_text_dt(obj, text)
    raise RuntimeError("Nenhum tradutor disponível")


def main():
    base = os.getcwd()
    output_dir = os.path.join(base, "OUTPUT")
    if not os.path.isdir(output_dir):
        print("❌ Pasta OUTPUT não encontrada.")
        sys.exit(1)

    pattern = os.path.join(output_dir, "*_transcricao.txt")
    files = sorted(glob.glob(pattern))
    if not files:
        print("❌ Nenhum arquivo *_transcricao.txt encontrado em OUTPUT.")
        sys.exit(1)

    print("🌐 Preparando tradutor (EN -> PT-BR)...")
    translator = pick_translator()
    if translator[0] is None:
        print("❌ Não foi possível inicializar um mecanismo de tradução.")
        print("   Instale uma das opções:")
        print("   - pip install -U transformers sentencepiece")
        print("   - pip install -U deep-translator")
        sys.exit(2)

    print(f"✅ Tradutor selecionado: {'HuggingFace' if translator[0]=='hf' else 'DeepTranslator'}")
    print(f"🗂️  Arquivos para traduzir: {len(files)}")

    ok = 0
    for idx, src in enumerate(files, 1):
        name = Path(src).stem  # sem extensão
        dst = os.path.join(output_dir, f"{name}_pt.txt")

        print(f"\n[{idx}/{len(files)}] {os.path.basename(src)} → {os.path.basename(dst)}")
        if os.path.exists(dst) and os.path.getsize(dst) > 0:
            print("   ↪ Já existe, pulando.")
            ok += 1
            continue

        try:
            with open(src, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
            if not text.strip():
                print("   ⚠️  Arquivo vazio, pulando.")
                continue

            t0 = time.time()
            translated = translate_any(translator, text)
            dt = time.time() - t0

            with open(dst, "w", encoding="utf-8") as f:
                f.write(translated)
            print(f"   ✅ OK em {dt:.1f}s ({len(translated)} chars)")
            ok += 1
        except Exception as e:
            print(f"   ❌ Erro: {e}")

    print("\n📊 RESUMO")
    print("=========")
    print(f"Traduzidos com sucesso: {ok}/{len(files)}")
    print(f"Pasta: {output_dir}")


if __name__ == "__main__":
    main()
