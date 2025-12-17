# translator_hf.py
# -*- coding: utf-8 -*-

import sys
import warnings
warnings.filterwarnings("ignore")

import torch
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

MODEL_NAME = "facebook/m2m100_418M"
TARGET_LANG = "tr"

# Basit dil kodu normalizasyonu (ekstra güvenlik)
LANG_MAP = {
    "zh-cn": "zh",
    "zh-tw": "zh",
    "pt-br": "pt",
}


def normalize_lang(lang: str) -> str:
    if not lang:
        return lang
    return LANG_MAP.get(lang.lower(), lang.lower())


def translate_lines(lines, src_lang: str):
    """
    lines: çevrilecek metin listesi
    src_lang: kaynak dil kodu
    return: çevrilmiş metin listesi
    """
    tokenizer = M2M100Tokenizer.from_pretrained(MODEL_NAME)
    model = M2M100ForConditionalGeneration.from_pretrained(MODEL_NAME)
    model.eval()

    src_lang = normalize_lang(src_lang)
    tokenizer.src_lang = src_lang

    results = []

    # Tek tek encode/generate yapıyoruz.
    # İstersen ileride hız için burada batch tokenization da yapılabilir.
    for text in lines:
        encoded = tokenizer(text, return_tensors="pt", truncation=True)
        with torch.no_grad():
            generated = model.generate(
                **encoded,
                forced_bos_token_id=tokenizer.get_lang_id(TARGET_LANG),
                max_new_tokens=256,
            )
        translated = tokenizer.batch_decode(generated, skip_special_tokens=True)[0]
        results.append(translated)

    return results


def main():
    # Kullanım: python translator_hf.py <girdi.txt> <cikti.txt> <kaynak_dil>
    if len(sys.argv) < 4:
        print(
            "Kullanım: python translator_hf.py <input_txt> <output_txt> <src_lang>",
            file=sys.stderr
        )
        sys.exit(1)

    in_path = sys.argv[1]
    out_path = sys.argv[2]
    src_lang = sys.argv[3]

    # Girdi dosyasını oku
    with open(in_path, "r", encoding="utf-8") as f:
        raw = f.read()

    raw = raw.strip()

    # Dosya boşsa boş yaz
    if not raw:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("")
        sys.exit(0)

    # Batch mantığı:
    # - Eğer dosyada birden fazla satır varsa her satırı ayrı yorum kabul et.
    # - Tek satır varsa eski davranışla aynı şekilde tek metin çevir.
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    if not lines:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("")
        sys.exit(0)

    print(">> translator_hf: model yükleniyor...")
    translated_lines = translate_lines(lines, src_lang)
    print(">> translator_hf: model yüklendi ve çeviri tamamlandı.")

    # Çıkışta:
    # - Batch ise her çeviriyi yeni satıra yaz.
    # - Tek satır ise yine tek satır yazmış olacağız.
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(translated_lines))


if __name__ == "__main__":
    main()
