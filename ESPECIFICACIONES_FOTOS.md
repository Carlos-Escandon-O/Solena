# Especificaciones de fotos para el catálogo de Solena

Esto es lo que necesito para reemplazar las piezas de ejemplo por tus joyas reales.

## ⚠️ Regla de oro

Usa la IA **solo para limpiar/recortar/fondo transparente**. No le pidas que "mejore", "embellezca" o "rediseñe" la joya: puede inventar piedras o cambiar el metal, y entonces la web mostraría un producto que no es el que vendes.

---

## Especificaciones generales

| Concepto | Requisito |
|---|---|
| Formato | **PNG con transparencia** (canal alpha). Nunca JPG. |
| Fondo | **Completamente transparente**. Sin blanco, sin sombra, sin reflejo, sin mesa. |
| Resolución | **1200 px de ancho** (o más). Alto según el tipo. |
| Encuadre | La joya ocupa ~85% del ancho; margen transparente de 5–8% alrededor. |
| Vista | **De frente**, sin inclinación ni perspectiva. Nada de ángulos artísticos. |
| Luz | Uniforme, suave, sin sombras proyectadas ni brillos quemados. |
| Enfoque | Nítida en todo el objeto. Sin desenfoque artístico. |
| Color | Real. Sin filtros, sin saturación extra, sin retoque de color. |
| Extras | Sin texto, sin logo, sin marca de agua, sin manos, sin caja, sin cinta. |
| Consistencia | Fotografía todas las piezas de un mismo tipo **a la misma escala** (para que el tamaño relativo entre piezas sea real). |

---

## Por tipo de pieza

### Aretes
- **Un solo arete** por imagen (el probador lo duplica en ambas orejas). Si tienes un par, recorta uno.
- El **gancho, perno o perforación debe quedar arriba**, a ~10% desde el borde superior de la imagen (ahí lo ancla el probador).
- Proporción ideal: **600 × 1200 px** (alto ≈ 2× el ancho).
- Centrado horizontalmente.

### Collares
- El collar **completo**, con la cadena formando una **curva en U simétrica**.
- Los **extremos de la cadena en las esquinas superiores** y el **dije centrado abajo** (el probador ancla la imagen por el borde superior).
- Proporción ideal: **1200 × 960 px**.
- La cadena debe verse entera, no cortada.

### Anillos
- **Un anillo**, vista frontal: la argolla como una **elipse horizontal** y la piedra **arriba y centrada**.
- El eje largo de la argolla debe estar **horizontal** en la imagen (el probador lo gira para ponerlo en el dedo).
- Proporción ideal: **1200 × 675 px**.
- Centrado, sin sombra interior.

---

## Prompt para tu IA (copiar y pegar)

```
Edita esta foto de producto de joyería. Elimina COMPLETAMENTE el fondo y devuelve
la imagen como PNG con transparencia real (canal alpha). Deja un margen transparente
de aproximadamente 6% alrededor del objeto.

Mantén la joya EXACTAMENTE igual: no cambies su forma, diseño, piedras, metales,
proporciones ni colores. No añadas ni quites ningún elemento. No generes detalles
nuevos. No la embellezcas ni la rediseñes.

Endereza el objeto de frente y céntralo en el cuadro. Iluminación uniforme y suave,
sin sombras proyectadas ni reflejos artificiales. Máxima nitidez. Sin texto, sin
marca de agua, sin manos, sin caja ni accesorios. Guarda a 1200 px de ancho.
```

### Añade al final según el tipo

**Aretes:**
```
Es SOLO UN arete. El gancho o perforación queda arriba, a ~10% del borde superior.
Lienzo vertical 600 × 1200 px, arete centrado horizontalmente.
```

**Collares:**
```
Devuelve el collar COMPLETO: cadena en curva en U simétrica, extremos en las
esquinas superiores y dije centrado abajo. Lienzo 1200 × 960 px.
```

**Anillos:**
```
Un anillo en vista frontal: argolla como elipse horizontal, piedra arriba y centrada.
Lienzo 1200 × 675 px. El eje largo de la argolla queda horizontal.
```

---

## Cómo entregármelas

1. Nombra los archivos así: `aretes-sol.png`, `collar-perla.png`, `anillo-aurora.png`.
2. Pásame también esta tabla (o dímela en el chat):

| id | nombre | tipo | categoría | precio |
|---|---|---|---|---|
| a1 | Aretes Sol | aretes | oro | 380 |
| c3 | Collar Perla | collar | perlas | 780 |
| r2 | Anillo Luna | anillo | plata | 340 |

Categorías válidas: `oro`, `plata`, `perlas`, `piedras`.
Tipos válidos: `aretes`, `collar`, `anillo`.

Con eso reemplazo el `CATALOGO` y el mismo QR empieza a mostrar tus piezas reales.
