"""Genera el cartel QR del probador virtual de Solena."""
import qrcode
from PIL import Image, ImageDraw, ImageFont

URL = "https://carlos-escandon-o.github.io/Solena/"
OUT = "cartel-qr-solena.png"

CREAM = "#f7f3ea"
INK = "#2a2318"
GOLD = "#b8892b"

font_paths = [
    "/Library/Fonts/Georgia.ttf",
    "/Library/Fonts/Georgia Bold.ttf",
    "/System/Library/Fonts/Supplemental/Georgia.ttf",
    "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
]

def font(size, bold=False):
    candidates = ([p for p in font_paths if "Bold" in p] if bold else font_paths) + font_paths
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default()

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=14,
    border=3,
)
qr.add_data(URL)
qr.make(fit=True)
qr_img = qr.make_image(fill_color=INK, back_color=CREAM).convert("RGB")

W = 900
H = 300 + qr_img.height + 220
canvas = Image.new("RGB", (W, H), CREAM)
draw = ImageDraw.Draw(canvas)

def centered(text, y, f, color=INK):
    box = draw.textbbox((0, 0), text, font=f)
    draw.text(((W - (box[2] - box[0])) / 2, y), text, font=f, fill=color)

centered("SOLENA", 60, font(78, bold=True))
centered("P R O B A D O R   V I R T U A L", 160, font(22), GOLD)

qr_x = (W - qr_img.width) // 2
qr_y = 230
canvas.paste(qr_img, (qr_x, qr_y))
draw.rectangle(
    [qr_x - 10, qr_y - 10, qr_x + qr_img.width + 10, qr_y + qr_img.height + 10],
    outline=GOLD,
    width=4,
)

centered("Escanea y pruébate las joyas", qr_y + qr_img.height + 50, font(38, bold=True))
centered("Aretes · Collares · Anillos", qr_y + qr_img.height + 110, font(24), GOLD)

canvas.save(OUT, "PNG", optimize=True)
print(f"Generado: {OUT} ({W}x{H}) -> {URL}")
