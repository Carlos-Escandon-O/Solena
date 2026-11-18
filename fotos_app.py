"""
Interfaz web local para preparar las fotos de Solenna.

Uso:
    pip install -r requirements.txt
    python3 fotos_app.py

Luego abre http://localhost:8080 en tu navegador.
"""

import io
import json
import re
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from PIL import Image
from preparar_fotos import ajustar, separar_islas, tipo_de, slug, SALIDA, PREFIJOS, quitar_fondo

SALIDA.mkdir(exist_ok=True)
resultados = []
contadores = {"aretes": 0, "collar": 0, "anillo": 0, "pulsera": 0}

HTML = r"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Solenna · Preparar fotos</title>
<style>
  :root{--bg:#f7f3ea;--ink:#241f19;--muted:#7a7062;--gold:#b8892b;--line:#e2d8c5;--card:#fffdf8}
  *{box-sizing:border-box}
  body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;color:var(--ink);background:var(--bg);min-height:100vh}
  header{padding:26px 20px 6px;text-align:center}
  header h1{font-family:Georgia,serif;margin:0;font-size:28px;letter-spacing:.08em}
  header p{margin:6px 0 0;font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.14em}
  main{max-width:1000px;margin:0 auto;padding:22px 16px 60px}
  .card{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:22px;box-shadow:0 8px 26px rgba(60,45,20,.07)}
  .card+.card{margin-top:16px}
  h2{font-size:15px;margin:0 0 14px}
  #drop{border:2px dashed var(--line);border-radius:16px;padding:40px 20px;text-align:center;cursor:pointer;transition:.2s;background:#fff}
  #drop:hover,#drop.over{border-color:var(--gold);background:#fffaf0}
  #drop .ico{font-size:40px}
  #drop strong{display:block;margin-top:8px;font-size:16px}
  #drop span{display:block;margin-top:6px;font-size:12px;color:var(--muted)}
  input[type=file]{display:none}
  .btn{display:inline-block;padding:12px 18px;border:0;border-radius:11px;background:linear-gradient(135deg,#c99a37,#a8761f);color:#fff;font-size:14px;font-weight:600;cursor:pointer;text-decoration:none}
  .btn.secondary{background:#fff;color:var(--ink);border:1px solid var(--line)}
  .btn:disabled{opacity:.5;cursor:not-allowed}
  .barra{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:16px}
  .progreso{height:8px;background:#eee4d2;border-radius:99px;overflow:hidden;margin-top:16px;display:none}
  .progreso i{display:block;height:100%;background:var(--gold);width:0;transition:.3s}
  .msg{font-size:13px;margin-top:12px;line-height:1.5;color:var(--muted)}
  .msg.error{color:#a33}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px;margin-top:16px}
  .item{border:1px solid var(--line);border-radius:14px;background:#fff;padding:10px;text-align:center}
  .item img{width:100%;height:130px;object-fit:contain;background:repeating-conic-gradient(#f2ece2 0 25%,#fff 0 50%) 50%/20px 20px}
  .item b{display:block;font-size:11px;margin-top:8px;word-break:break-all}
  .item small{display:block;color:var(--muted);font-size:10px;margin-top:3px}
  .hint{font-size:11px;color:#9a8f7e;line-height:1.6;margin-top:14px}
  code{background:#f3ecdd;padding:1px 5px;border-radius:4px}
</style>
</head>
<body>
<header><h1>Solenna</h1><p>Preparar fotos para el probador</p></header>
<main>
  <section class="card">
    <h2>1. Sube tus fotos</h2>
    <div id="drop">
      <div class="ico">📸</div>
      <strong>Arrastra tus fotos aquí</strong>
      <span>o haz clic para elegirlas · varias a la vez</span>
    </div>
    <input type="file" id="file" accept="image/*" multiple>
    <div class="progreso" id="progreso"><i id="barra"></i></div>
    <p class="msg" id="msg"></p>
    <div class="barra">
      <button class="btn" id="procesar" disabled>Procesar fotos</button>
      <button class="btn secondary" id="limpiar">Limpiar</button>
    </div>
    <p class="hint">
      Nombra tus archivos con el prefijo del tipo: <code>aretes-…</code>,
      <code>collar-…</code>, <code>anillo-…</code>, <code>pulsera-…</code>.
      Si una foto tiene varias piezas separadas, el programa las divide solo.
    </p>
  </section>

  <section class="card">
    <h2>2. Resultado</h2>
    <div class="grid" id="grid"></div>
    <p class="msg" id="vacio">Todavía no hay piezas procesadas.</p>
    <div class="barra">
      <a class="btn" id="descargar" href="/catalogo-sugerido.json" download="catalogo-sugerido.json">Descargar catálogo sugerido</a>
      <a class="btn secondary" href="https://carlos-escandon-o.github.io/Solenna/admin.html" target="_blank">Ir al panel Admin</a>
    </div>
    <p class="hint">Las imágenes ya están en <code>assets/</code> dentro del repo. El JSON sugerido tiene precios en 0: pon los reales antes de pegarlo en el Admin.</p>
  </section>
</main>

<script>
const drop = document.getElementById('drop');
const file = document.getElementById('file');
const btn = document.getElementById('procesar');
const msg = document.getElementById('msg');
const barra = document.getElementById('barra');
const progreso = document.getElementById('progreso');
const grid = document.getElementById('grid');
const vacio = document.getElementById('vacio');
let archivos = [];

function elegir(lista){
  archivos = [...lista].filter(f => f.type.startsWith('image/'));
  btn.disabled = archivos.length === 0;
  msg.textContent = archivos.length ? `${archivos.length} foto(s) lista(s) para procesar.` : '';
}
drop.onclick = () => file.click();
drop.ondragover = e => { e.preventDefault(); drop.classList.add('over'); };
drop.ondragleave = () => drop.classList.remove('over');
drop.ondrop = e => { e.preventDefault(); drop.classList.remove('over'); elegir(e.dataTransfer.files); };
file.onchange = e => elegir(e.target.files);

function pintar(items){
  grid.innerHTML = items.map(it => `
    <div class="item">
      <img src="/salida/${encodeURIComponent(it.archivo)}?t=${Date.now()}" alt="${it.archivo}">
      <b>${it.archivo}</b>
      <small>${it.ancho} × ${it.alto} · ${it.tipo}</small>
    </div>`).join('');
  vacio.style.display = items.length ? 'none' : 'block';
}

btn.onclick = async () => {
  btn.disabled = true;
  progreso.style.display = 'block';
  msg.className = 'msg';
  const salida = [];
  for (let i = 0; i < archivos.length; i++){
    const f = archivos[i];
    barra.style.width = Math.round(i / archivos.length * 100) + '%';
    msg.textContent = `Procesando ${i+1} de ${archivos.length}: ${f.name}…`;
    try {
      const r = await fetch('/procesar?nombre=' + encodeURIComponent(f.name), {
        method:'POST', body: await f.arrayBuffer()
      });
      const j = await r.json();
      if (!r.ok) throw new Error(j.error || 'Error al procesar');
      salida.push(...j.piezas);
      if (j.aviso) msg.textContent = j.aviso;
    } catch(e){
      msg.className = 'msg error';
      msg.textContent = 'Error con ' + f.name + ': ' + e.message;
      break;
    }
  }
  barra.style.width = '100%';
  progreso.style.display = 'none';
  btn.disabled = false;
  await actualizar();
  msg.textContent = salida.length ? `✅ ${salida.length} pieza(s) lista(s).` : msg.textContent;
};

async function actualizar(){
  const r = await fetch('/resultados');
  pintar(await r.json());
}

document.getElementById('limpiar').onclick = async () => {
  await fetch('/limpiar', {method:'POST'});
  archivos = []; file.value = ''; btn.disabled = true;
  msg.textContent = ''; await actualizar();
};

actualizar();
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def _json(self, obj, status=200):
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _html(self, text):
        data = text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        ruta = urlparse(self.path).path
        if ruta == "/":
            return self._html(HTML)
        if ruta == "/resultados":
            return self._json([x for x in resultados])
        if ruta == "/catalogo-sugerido.json":
            return self._json([{k: v for k, v in x["entrada"].items()} for x in resultados])
        if ruta.startswith("/salida/"):
            nombre = unquote(ruta.split("/salida/")[1])
            destino = SALIDA / nombre
            if not destino.exists() or destino.parent != SALIDA:
                self.send_error(404)
                return
            data = destino.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        self.send_error(404)

    def do_POST(self):
        ruta = urlparse(self.path).path
        if ruta == "/limpiar":
            resultados.clear()
            for k in contadores:
                contadores[k] = 0
            return self._json({"ok": True})

        if ruta == "/procesar":
            nombre = unquote(urlparse(self.path).query.split("nombre=")[1]) if "nombre=" in urlparse(self.path).query else "foto.png"
            nombre = re.sub(r"[^A-Za-z0-9._-]", "_", nombre.split("?")[0])
            largo = int(self.headers.get("Content-Length", 0))
            if not largo:
                return self._json({"error": "Archivo vacío"}, 400)

            with tempfile.NamedTemporaryFile(suffix=".img", delete=False) as tmp:
                tmp.write(self.rfile.read(largo))
                ruta_tmp = tmp.name

            try:
                with Image.open(ruta_tmp) as img:
                    img = img.convert("RGBA")
                    sin_fondo = quitar_fondo(img)
                tipo = tipo_de(nombre)
                islas = separar_islas(sin_fondo)
                if not islas:
                    return self._json({
                        "piezas": [],
                        "aviso": f"No se detectó ninguna pieza en {nombre}. Si la joya está sostenida por una mano, recórtala primero."
                    })

                piezas = []
                base = slug(nombre)
                for idx, isla in enumerate(islas, 1):
                    lista = ajustar(isla, tipo)
                    if lista is None:
                        continue
                    sufijo = f"-{idx}" if len(islas) > 1 else ""
                    archivo = f"{base}{sufijo}.png"
                    lista.save(SALIDA / archivo, "PNG", optimize=True)

                    contadores[tipo] += 1
                    entrada = {
                        "id": f"{PREFIJOS[tipo]}{contadores[tipo]}",
                        "nombre": archivo.replace("-", " ").replace(".png", "").title(),
                        "tipo": tipo,
                        "cat": "perlas" if "perla" in archivo else "oro",
                        "precio": 0,
                        "stock": 1,
                        "src": f"assets/{archivo}",
                    }
                    if tipo == "collar" and "oval" in nombre.lower():
                        entrada["recortar"] = True

                    item = {
                        "archivo": archivo,
                        "ancho": lista.width,
                        "alto": lista.height,
                        "tipo": tipo,
                        "entrada": entrada,
                    }
                    resultados.append(item)
                    piezas.append({k: v for k, v in item.items() if k != "entrada"})

                return self._json({"piezas": piezas})
            except Exception as e:
                return self._json({"error": str(e)}, 500)
            finally:
                Path(ruta_tmp).unlink(missing_ok=True)

        self.send_error(404)

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    puerto = 8080
    print(f"\n  Solenna · Preparar fotos")
    print(f"  Abre en tu navegador:  http://localhost:{puerto}\n")
    ThreadingHTTPServer(("127.0.0.1", puerto), Handler).serve_forever()
