"""Build the NasriTools site from the portal source.

    python build.py        # then: git add -A; git commit; git push

Source of truth: C:/Users/nasri/ESCUELA/jardin.html (also published as the Claude artifact).
Output: jardin/index.html (+ manifest + icons) so it installs as a home-screen app.
"""
import json, os, re
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:\Users\nasri\ESCUELA\jardin.html"
OUT = os.path.join(HERE, "jardin")
os.makedirs(OUT, exist_ok=True)

def flor(size):
    im = Image.new("RGB", (size, size), "#F8F3FB"); d = ImageDraw.Draw(im)
    c, r = size / 2, size * 0.16
    for k, (dx, dy) in enumerate([(0, -1), (0.95, -0.31), (0.59, 0.81), (-0.59, 0.81), (-0.95, -0.31)]):
        x, y = c + dx * size * 0.2, c + dy * size * 0.2
        d.ellipse([x - r, y - r, x + r, y + r], fill="#E8578B")
    d.ellipse([c - r * 0.8, c - r * 0.8, c + r * 0.8, c + r * 0.8], fill="#F6B940")
    return im

for s in (192, 512):
    flor(s).save(os.path.join(OUT, f"icon-{s}.png"))

json.dump({"name": "Mi Jardín de Estudio · NasriTools", "short_name": "Mi Jardín", "start_url": "./", "display": "standalone",
           "background_color": "#F8F3FB", "theme_color": "#E8578B", "lang": "es",
           "icons": [{"src": f"icon-{s}.png", "sizes": f"{s}x{s}", "type": "image/png", "purpose": "any maskable"} for s in (192, 512)]},
          open(os.path.join(OUT, "manifest.webmanifest"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

body = open(SRC, encoding="utf-8").read()
body = re.sub(r"<title>.*?</title>", "<title>Mi Jardín de Estudio · NasriTools</title>", body, count=1)
# Off claude.ai there is no shared db: progress lives in this device's localStorage only.
body = re.sub(r"^if\(window\.claude.*?\n(?=</script>)", "", body, flags=re.S | re.M)
assert "claude" not in body.lower(), "Claude reference left in the NasriTools build"
head = """<!doctype html>
<html lang="es"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#E8578B">
<meta name="author" content="NasriTools">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-192.png">
"""
foot = """<footer style="text-align:center;padding:18px 16px 28px;color:var(--tinta-2);font-size:13px">Hecho con cariño por <b>NasriTools</b> · © 2026</footer>
</body></html>"""
# The artifact skeleton adds <head>/<body>; here we add them ourselves.
html = head + body.replace("<header", "</head><body>\n<header", 1) + foot
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)

open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(
    '<!doctype html><meta charset="utf-8"><title>NasriTools</title><meta http-equiv="refresh" content="0; url=jardin/">'
    '<a href="jardin/">Mi Jardín de Estudio</a>')
print("built", os.path.join(OUT, "index.html"), len(html), "bytes")
