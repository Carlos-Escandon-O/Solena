# Solena · Probador virtual

Probador virtual de joyería que funciona en el navegador, sin instalar nada.
Usa la cámara o una foto subida + MediaPipe (gratis) para colocar aretes, collar, anillos y pulseras en tiempo real.

## 🌐 Sitio en vivo

**https://carlos-escandon-o.github.io/Solena/**

Publicado con GitHub Pages (HTTPS, funciona desde el celular).

## ✨ Funciones

- **Dos modos:** cámara en vivo o subir una selfie guardada (ideal si no quieres abrir la cámara en el bazar).
- **Catálogo de 16 piezas** de ejemplo (aretes, collares, anillos y pulseras) con filtros **Oro / Plata / Perlas / Piedras** y orden por precio o nombre.
- **Ajuste manual** de posición y tamaño, dedo para anillos, muñeca para pulseras, y opción de subir tu propia joya en PNG.
- **Pedir por WhatsApp:** abre un chat con el nombre y precio de la pieza ya escritos.
- **Foto descargable** y botón compartir.
- **Contador social diario.**

## ⚙️ Configuración ( importante )

Al inicio del `<script>` en `index.html` hay dos valores que debes editar:

```js
const WHATSAPP = "525539753964";                  // configurado con tu número
const BASE_PRUEBAS_REALES_POR_PIEZA = {};         // solo con pruebas reales documentadas
```

1. **WHATSAPP:** ya está tu número (`52` + `55 3975 3964`). El botón abre el chat con el nombre y precio de la pieza ya escritos.
2. **Contador:** es **real y por pieza**: cuenta una prueba por sesión, se reinicia cada día y muestra qué pieza está siendo más probada (ej. *"💫 4 personas se lo probaron hoy · Collar Perla ×2"*). Las variaciones salen solas porque cada persona elige una joya distinta.
   Si llevas un registro **verdadero** de pruebas anteriores, puedes cargarlo como base, por ejemplo: `{ a1: 2, c3: 1, r2: 1 }`. Déjalo vacío si no: un cartel con números inventados se nota y rompe la confianza del cliente (además de ser publicidad engañosa).

## 📱 Cartel QR para el bazar

![Cartel QR de Solena](cartel-qr-solena.png)

`cartel-qr-solena.png` está listo para imprimir. Si cambias la URL, regenera:

```bash
python3 generar_qr.py   # requiere: pip install qrcode pillow
```

## 🔄 Cómo actualizar el sitio

Cada cambio en `index.html` se publica solo con:

```bash
git add . && git commit -m "describe el cambio" && git push
```

GitHub Pages tarda ~1 minuto en reflejarlo.

## 📸 Poner tus piezas reales

1. Foto de cada joya de frente, bien iluminada y centrada, con fondo liso o transparente (PNG). Yo puedo quitar el fondo si me la mandas.
2. Reemplaza el array `CATALOGO` en `index.html` con tus piezas reales: `nombre`, `tipo`, `cat`, `precio` y la ruta de la imagen.
3. Con 5–10 piezas ya tienes el catálogo completo.

## Notas

- El collar es aproximado (la malla facial no cubre el cuello), por eso tiene controles de ajuste. Aretes, anillos y pulseras son más precisos.
- Funciona mejor con buena luz y la cara o mano bien visibles.
- Las fotos que sube cada persona no se envían a ningún servidor: se procesan en su propio navegador.
- Librerías: MediaPipe Tasks Vision v0.10.14 (CDN). Sin costos ni API keys.
