import polib

from pathlib import Path
import time

import ollama

def traducir(texto):

    prompt = f"""You are a professional Spanish (es) to Catalan (ca) translator.
Your goal is to accurately convey the meaning and nuances of the original Spanish text.

Produce only the Catalan translation, without explanations.

Please translate the following Spanish text into Catalan:


{texto}
"""

    response = ollama.chat(
        model="translategemma:4b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0
        }
    )

    return response["message"]["content"].strip()





directorio_proyecto = Path(__file__).resolve().parents[3]

archivo_origen = directorio_proyecto / "locale/es/LC_MESSAGES/django.po"
archivo_destino = directorio_proyecto / "locale/ca/LC_MESSAGES/django.po"

po = polib.pofile(archivo_origen)

# Recopilar entradas pendientes
entradas_pendientes = [
    entry for entry in po
    if entry.msgid
    and not entry.obsolete
    and not entry.msgid_plural
    and not entry.msgstr.strip()
]

# Procesar por lotes
TAMANO_LOTE = 20

for i in range(0, len(entradas_pendientes), TAMANO_LOTE):

    lote = entradas_pendientes[i:i + TAMANO_LOTE]

    textos = [entry.msgid for entry in lote]

    try:

        traducciones = [traducir(texto) for texto in textos]

        for entry, traduccion in zip(lote, traducciones):

            entry.msgstr = traduccion

            if "fuzzy" not in entry.flags:
                entry.flags.append("fuzzy")

            print(f"Original: {entry.msgid}")
            print(f"Traducido: {traduccion}")
            print("-" * 40)

        # Guardar después de cada lote
        po.save(archivo_destino)

        print(
            f"Progreso: {min(i + TAMANO_LOTE, len(entradas_pendientes))}"
            f"/{len(entradas_pendientes)}"
        )

        time.sleep(2)

    except Exception as error:
        print(f"Error procesando lote {i}: {error}")

        po.save(archivo_destino)
        time.sleep(10)

print("Proceso de traducción finalizado.")