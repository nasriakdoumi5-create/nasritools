"""Build the NasriTools site: one folder per study portal + a landing page.

    python build.py        # then: git add -A; git commit; git push

Sources of truth live in C:/Users/nasri/ESCUELA (also published as Claude artifacts).
Each portal becomes <folder>/index.html + manifest + icons, so it installs as a home-screen app.
"""
import json, os, re
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ESC = r"C:\Users\nasri\ESCUELA"

def flor(size):
    im = Image.new("RGB", (size, size), "#F8F3FB"); d = ImageDraw.Draw(im)
    c, r = size / 2, size * 0.16
    for dx, dy in [(0, -1), (0.95, -0.31), (0.59, 0.81), (-0.59, 0.81), (-0.95, -0.31)]:
        x, y = c + dx * size * 0.2, c + dy * size * 0.2
        d.ellipse([x - r, y - r, x + r, y + r], fill="#E8578B")
    d.ellipse([c - r * 0.8, c - r * 0.8, c + r * 0.8, c + r * 0.8], fill="#F6B940")
    return im

def faro(size):
    im = Image.new("RGB", (size, size), "#0F5A61"); d = ImageDraw.Draw(im); s = size / 100
    d.polygon([(0, 30 * s), (50 * s, 26 * s), (50 * s, 34 * s)], fill="#F5A524")           # light beam
    d.polygon([(100 * s, 30 * s), (50 * s, 26 * s), (50 * s, 34 * s)], fill="#F5A524")
    d.polygon([(40 * s, 86 * s), (60 * s, 86 * s), (56 * s, 40 * s), (44 * s, 40 * s)], fill="#FFFFFF")  # tower
    d.rectangle([43 * s, 55 * s, 57 * s, 62 * s], fill="#C24A3F"); d.rectangle([41 * s, 72 * s, 59 * s, 79 * s], fill="#C24A3F")
    d.rectangle([42 * s, 24 * s, 58 * s, 40 * s], fill="#F5A524"); d.polygon([(40 * s, 24 * s), (60 * s, 24 * s), (50 * s, 14 * s)], fill="#C24A3F")
    d.rectangle([20 * s, 86 * s, 80 * s, 92 * s], fill="#1B7F87")
    return im

SITES = [
    dict(src="jardin.html", folder="jardin", title="Mi Jardín de Estudio · NasriTools", short="Mi Jardín",
         theme="#E8578B", bg="#F8F3FB", icon=flor, db="alumna"),
    dict(src="portal.html", folder="faro", title="Faro de Estudio · NasriTools", short="Mi Faro",
         theme="#1B7F87", bg="#F4F7F6", icon=faro, db="alumno"),
]

BASE_CSS = "<style>[hidden]{display:none!important}body{margin:0}img{max-width:100%}</style>"
FOOT = ('<footer style="text-align:center;padding:18px 16px 28px;color:#888;font:13px Nunito,sans-serif">'
        'Hecho con cariño por <b>NasriTools</b> · © 2026</footer>\n</body></html>')

for s in SITES:
    out = os.path.join(HERE, s["folder"]); os.makedirs(out, exist_ok=True)
    for px in (192, 512):
        s["icon"](px).save(os.path.join(out, f"icon-{px}.png"))
    json.dump({"name": s["title"], "short_name": s["short"], "start_url": "./", "display": "standalone",
               "background_color": s["bg"], "theme_color": s["theme"], "lang": "es",
               "icons": [{"src": f"icon-{px}.png", "sizes": f"{px}x{px}", "type": "image/png", "purpose": "any maskable"} for px in (192, 512)]},
              open(os.path.join(out, "manifest.webmanifest"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    body = open(os.path.join(ESC, s["src"]), encoding="utf-8").read()
    body = re.sub(r"<meta charset[^>]*>\s*", "", body)
    body = re.sub(r"<title>.*?</title>", f"<title>{s['title']}</title>", body, count=1)
    # Off claude.ai there is no shared db: progress lives in this device's localStorage only.
    body = re.sub(r"^if\(window\.claude.*?\n(?=</script>)", "", body, flags=re.S | re.M)
    assert "claude" not in body.lower(), f"Claude reference left in {s['src']}"
    head = f"""<!doctype html>
<html lang="es"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="{s['theme']}">
<meta name="author" content="NasriTools">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-192.png">
{BASE_CSS}
"""
    # The artifact skeleton supplies <head>/<body>; here we add them: head ends after the page's own first <style>.
    body = body.replace("</style>", "</style>\n</head><body>", 1)
    html = head + body + FOOT
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(html)
    print("built", s["folder"], len(html), "bytes")

# Landing page: both portals, one address for the whole school year.
cards = "".join(f"""<a class="c" href="{s['folder']}/" style="--t:{s['theme']};--b:{s['bg']}">
  <img src="{s['folder']}/icon-192.png" alt=""><b>{s['short']}</b><span>{s['title'].split(' · ')[0]}</span></a>""" for s in SITES)
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>NasriTools</title><link rel="icon" href="jardin/icon-192.png">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@700&family=Nunito:wght@600;800&display=swap">
<style>body{{margin:0;background:#F6F4F8;color:#2E2440;font-family:Nunito,Segoe UI,sans-serif;padding:40px 16px}}
h1{{font-family:'Baloo 2',sans-serif;text-align:center;font-size:40px;margin:0 0 6px}}p{{text-align:center;color:#6E5A82;margin:0 0 28px}}
.g{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;max-width:640px;margin:0 auto}}
.c{{display:flex;flex-direction:column;align-items:center;gap:8px;padding:26px 16px;border-radius:22px;background:var(--b);border:2px solid var(--t);text-decoration:none;color:inherit}}
.c:hover{{transform:translateY(-3px)}}.c img{{width:84px;height:84px;border-radius:20px}}.c b{{font-family:'Baloo 2',sans-serif;font-size:24px;color:var(--t)}}
.c span{{font-size:14px;color:#6E5A82}}footer{{text-align:center;margin-top:36px;font-size:13px;color:#888}}</style></head>
<body><h1>NasriTools</h1><p>Portales de estudio · Curso 2026 / 2027</p><div class="g">{cards}</div>
<footer>© 2026 NasriTools</footer></body></html>""")
print("built landing")
