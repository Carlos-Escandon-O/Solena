# Solena · Probador virtual

Prototipo de probador virtual de joyería funciona en el navegador, sin instalar nada.
Usa la cámara + MediaPipe (gratis) para colocar aretes, collar y anillos sobre tu imagen en tiempo real.

## Cómo verlo

La cámara solo funciona en **HTTPS** o en **localhost**. Tienes dos opciones:

### Opción rápida (en tu computadora, sin subir nada)
```bash
cd solena-probador
python3 -m http.server 8000
```
Abre http://localhost:8000 en tu navegador.

### Opción para compartir (gratis, con HTTPS)
1. Crea una cuenta en **Netlify Drop** (https://app.netlify.com/drop) o **Vercel**.
2. Arrastra la carpeta `solena-probador` completa.
3. Te dan un link `https://...netlify.app` — ese link puedes ponerlo en un QR en tu puesto y compartirlo por WhatsApp/Instagram.

## Cómo usarlo

1. Activa la cámara.
2. Elige **Aretes**, **Collar** o **Anillo**.
3. Ajusta **Mover ↔ / Mover ↕ / Tamaño** hasta que la pieza quede bien.
4. Para anillos elige el dedo.
5. **Tomar foto** → descargar o compartir.

## Poner TUS piezas reales

Por defecto usa piezas de ejemplo dibujadas en SVG. Para usar tus joyas:

1. Toma una foto de cada pieza con **fondo transparente** (PNG).
   - Quita el fondo con https://remove.bg o https://www.adobe.com/express/feature/image/remove-background
   - La joya debe estar centrada y de frente.
2. En la web, selecciona el tipo (Aretes/Collar/Anillo) y sube el PNG con "Tu pieza (opcional)".
3. Ajusta posición y tamaño con los controles.

> Las imágenes que subes se guardan solo en el navegador de quien las sube; no se envían a ningún servidor.

## Notas

- El **collar** es aproximado (la malla facial no incluye el cuello), por eso tiene controles de ajuste. Los aretes y anillos son más precisos.
- Funciona mejor con buena luz y la cara/mano bien visible.
- En móvil usa la cámara frontal; la imagen se muestra en modo espejo.
- Librerías usadas: MediaPipe Tasks Vision v0.10.14 (CDN). No hay costos ni API keys.

## Posibles mejoras siguientes
- Modo "subir foto" para probar sobre una imagen guardada.
- Guardar automáticamente la pieza elegida por cliente.
- Catálogo de varias piezas reales con selector de modelo.
- Botón "Agregar a mi pedido" / WhatsApp al final.
