"""Transliteración básica devanāgarī -> IAST.

Implementación didáctica y parcial. Para producción conviene una librería
madura (p. ej. indic-transliteration). Mantiene los diacríticos IAST:
ā ī ū ṛ ṝ ṃ ḥ ś ṣ ñ ṅ ṭ ḍ.
"""
from __future__ import annotations

# Vocales independientes.
VOWELS = {
    "अ": "a", "आ": "ā", "इ": "i", "ई": "ī", "उ": "u", "ऊ": "ū",
    "ऋ": "ṛ", "ॠ": "ṝ", "ए": "e", "ऐ": "ai", "ओ": "o", "औ": "au",
}

# Consonantes (con la 'a' inherente).
CONSONANTS = {
    "क": "k", "ख": "kh", "ग": "g", "घ": "gh", "ङ": "ṅ",
    "च": "c", "छ": "ch", "ज": "j", "झ": "jh", "ञ": "ñ",
    "ट": "ṭ", "ठ": "ṭh", "ड": "ḍ", "ढ": "ḍh", "ण": "ṇ",
    "त": "t", "थ": "th", "द": "d", "ध": "dh", "न": "n",
    "प": "p", "फ": "ph", "ब": "b", "भ": "bh", "म": "m",
    "य": "y", "र": "r", "ल": "l", "व": "v",
    "श": "ś", "ष": "ṣ", "स": "s", "ह": "h",
}

# Signos: anusvāra y visarga.
MARKS = {"ं": "ṃ", "ः": "ḥ"}


def to_iast(text: str) -> str:
    """Convierte una cadena devanāgarī a IAST (aproximación didáctica)."""
    out: list[str] = []
    for ch in text:
        if ch in VOWELS:
            out.append(VOWELS[ch])
        elif ch in CONSONANTS:
            out.append(CONSONANTS[ch] + "a")
        elif ch in MARKS:
            out.append(MARKS[ch])
        else:
            out.append(ch)
    return "".join(out)
