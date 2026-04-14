import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime

URL = "https://entradas.ataquilla.com/es/ventaentradas/recintos/251-auditorio-municipal-de-ourense"

r = requests.get(URL, timeout=20)
soup = BeautifulSoup(r.text, "html.parser")

fg = FeedGenerator()
fg.title("Auditorio Municipal de Ourense")
fg.link(href=URL)
fg.description("Eventos presentes y futuros del Auditorio de Ourense")
fg.language("es")

# ⚠️ Selector genérico (puede ajustarse si la web cambia)
eventos = soup.select("a")

seen = set()

for e in eventos:
    titulo = e.get_text(strip=True)
    link = e.get("href")

    # filtro básico: evita basura y duplicados
    if not titulo or len(titulo) < 5:
        continue

    if link and not link.startswith("http"):
        link = "https://entradas.ataquilla.com" + link

    key = (titulo, link)
    if key in seen:
        continue
    seen.add(key)

    entry = fg.add_entry()
    entry.title(titulo)
    entry.link(href=link)

fg.rss_file("feed.xml")
