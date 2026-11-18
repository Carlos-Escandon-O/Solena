"""
Prepara las fotos de Solenna para el probador virtual.

Qué hace:
  1. Quita el fondo con rembg (gratis, local, ilimitado).
  2. Detecta las piezas separadas dentro de cada foto (islas de transparencia)
     y las guarda como archivos individuales.
  3. Recorta y escala cada pieza a las medidas exactas según el tipo.
  4. Imprime entradas sugeridas para catalogo.json.

Uso:
  - Pon tus fotos en la carpeta "fotos-crudas/".
  - Nómbralas con el prefijo del tipo: aretes-..., collar-..., anillo-..., pulsera-...
    (para fotos con varias piezas usa el prefijo del tipo, ej. pulseras-lote.png)
  - Instala:  pip install -r requirements.txt
  - Corre:    python3 preparar_fotos.py
  - Las imágenes listas quedan en "assets/".

Ojo: si una pieza está sostenida por una mano o se toca con otra, el script
no puede separarla. Recorta esa foto antes (Photopea o tu IA de edición).
"""

import json
import re
from pathlib import Path

from PIL import Image
import numpy as np
import cv2
from rembg import remove

CRUDAS = Path("fotos-crudas")
SALIDA = Path("assets")
MARGEN = 0.06          # margen transparente alrededor de la pieza
AREA_MINIMA = 0.001    # descarta islas menores al 0.1% de la imagen

MEDIDAS = {
    "aretes":  (600, 1200),
    "collar":  (1200, 1200),
    "anillo":  (1200, 675),
    "pulsera": (1200, 720),
}
PREFIJOS = {
    "aretes": "a", "arete": "a",
    "collar": "c", "collares": "c",
    "anillo": "r", "anillos": "r",
    "pulsera": "p", "pulseras": "p",
}


def tipo_de(nombre):
    n = nombre.lower()
    for pref, tipo in PREFIJOS.items():
        if n.startswith(pref):
            return tipo
    return "collar"


def separar_islas(imagen):
    """Devuelve una lista de recortes (PIL RGBA), uno por pieza detectada."""
    alpha = np.array(imagen.getchannel("A"))
    mask = (alpha > 25).astype(np.uint8)

    # Cierra pequeños huecos (por ejemplo, dentro de un eslabón)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    n, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    total = imagen.width * imagen.height
    areas = []
    for i in range(1, n):
        area = stats[i, cv2.CC_STAT_AREA]
        if area >= total * AREA_MINIMA:
            areas.append((i, area, stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP],
                          stats[i, cv2.CC_STAT_WIDTH], stats[i, cv2.CC_STAT_HEIGHT]))

    if not areas:
        return []

    # De izquierda a derecha y arriba abajo para que el orden sea predecible
    areas.sort(key=lambda x: (x[2] // 80, x[3]))

    recortes = []
    for i, _, x, y, w, h in areas:
        pad = max(6, int(min(w, h) * 0.04))
        x0, y0 = max(0, x - pad), max(0, y - pad)
        x1, y1 = min(imagen.width, x + w + pad), min(imagen.height, y + h + pad)
        recorte = imagen.crop((x0, y0, x1, y1))

        # Aplica la máscara de esta isla para limpiar restos de otras piezas
        m = Image.fromarray((labels[y0:y1, x0:x1] == i).astype(np.uint8) * 255)
        recorte.putalpha(m)
        recortes.append(recorte)
    return recortes


def ajustar(recorte, tipo):
    """Centra la pieza en un lienzo del tamaño exacto, con margen transparente."""
    ancho, alto = MEDIDAS[tipo]
    bbox = recorte.getbbox()
    if not bbox:
        return None
    recorte = recorte.crop(bbox)

    util_ancho = ancho * (1 - 2 * MARGEN)
    util_alto = alto * (1 - 2 * MARGEN)
    escala = min(util_ancho / recorte.width, util_alto / recorte.height)
    nuevo = (max(1, round(recorte.width * escala)), max(1, round(recorte.height * escala)))
    recorte = recorte.resize(nuevo, Image.LANCZOS)

    lienzo = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    lienzo.alpha_composite(recorte, ((ancho - nuevo[0]) // 2, (alto - nuevo[1]) // 2))
    return lienzo


def slug(texto):
    texto = re.sub(r"\.(png|jpg|jpeg|webp)$", "", texto, flags=re.I).lower()
    texto = re.sub(r"[^a-z0-9]+", "-", texto).strip("-")
    return texto


def main():
    CRUDAS.mkdir(exist_ok=True)
    SALIDA.mkdir(exist_ok=True)

    archivos = [p for p in CRUDAS.iterdir()
                if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}]
    if not archivos:
        print(f"No hay fotos en {CRUDAS}/. Pon tus imágenes ahí y vuelve a correr.")
        return

    sugerencias = []
    contadores = {"aretes": 0, "collar": 0, "anillo": 0, "pulsera": 0}

    for archivo in sorted(archivos):
        tipo = tipo_de(archivo.name)
        print(f"\n→ {archivo.name}  (tipo: {tipo})")
        with Image.open(archivo) as img:
            img = img.convert("RGBA")
            sin_fondo = remove(img)

        islas = separar_islas(sin_fondo)
        if not islas:
            print("   ⚠ No se detectó ninguna pieza. ¿La joya se toca con la mano o con otra pieza?")
            continue

        print(f"   {len(islas)} pieza(s) detectada(s)")

        for idx, isla in enumerate(islas, start=1):
            lista = ajustar(isla, tipo)
            if lista is None:
                continue
            sufijo = f"-{idx}" if len(islas) > 1 else ""
            nombre = f"{slug(archivo.name)}{sufijo}.png"
            destino = SALIDA / nombre
            lista.save(destino, "PNG", optimize=True)

            contadores[tipo] += 1
            entrada = {
                "id": f"{PREFIJOS[tipo]}{contadores[tipo]}",
                "nombre": nombre.replace("-", " ").replace(".png", "").title(),
                "tipo": tipo,
                "cat": "perlas" if "perla" in nombre else "oro",
                "precio": 0,
                "stock": 1,
                "src": f"assets/{nombre}",
            }
            if tipo == "collar" and "oval" in archivo.name.lower():
                entrada["recortar"] = True
            sugerencias.append(entrada)
            print(f"   ✓ {destino}  {lista.width}×{lista.height}")

    if sugerencias:
        destino = Path("catalogo-sugerido.json")
        destino.write_text(json.dumps(sugerencias, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n✅ Listo. Sugerencias para catalogo.json en {destino}")
        print("   Revisa nombres, categorías, precios y stock antes de pegarlas en el panel Admin.")
    else:
        print("\nNo se generó ninguna imagen.")


if __name__ == "__main__":
    main()
