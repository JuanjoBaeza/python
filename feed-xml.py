import feedparser
import requests
import re

def leer_feed_y_mostrar_mp3(url):
    """
    Lee un feed RSS/Atom (por ejemplo de un podcast) y muestra las URLs
    de los archivos MP3 encontrados en cada entrada.
    No descarga nada.
    """
    print(f"📡 Leyendo feed: {url}\n")
    feed = feedparser.parse(url)

    if not feed.entries:
        print("⚠️ No se encontraron entradas en el feed.")
        return

    for i, entry in enumerate(feed.entries, start=1):
        print(f"🔹 Entrada {i}: {entry.get('title', '(sin título)')}")
        mp3_urls = set()

        # 1️⃣ Buscar enlaces MP3 en 'enclosures' (típico de podcasts)
        if "enclosures" in entry:
            for enc in entry.enclosures:
                href = enc.get("href", "")
                if href.lower().endswith(".mp3"):
                    mp3_urls.add(href)

        # 2️⃣ Buscar enlaces MP3 en el contenido o resumen
        contenido = ""
        if "content" in entry and entry.content:
            contenido = entry.content[0].value
        elif "summary" in entry:
            contenido = entry.summary
        mp3_urls.update(re.findall(r"https?://[^\s\"']+\.mp3", contenido))

        # 3️⃣ Si no se encuentra, buscar en la página enlazada
        if not mp3_urls and entry.get("link"):
            link = entry.link
            try:
                html = requests.get(link, timeout=10).text
                encontrados = re.findall(r"https?://[^\s\"']+\.mp3", html)
                mp3_urls.update(encontrados)
            except Exception as e:
                print(f"   ⚠️ Error al acceder a la página: {e}")

        # Mostrar resultados
        if mp3_urls:
            for mp3_url in sorted(mp3_urls):
                print(f"   🎧 {mp3_url}")
        else:
            print("   ❌ No se encontró audio en esta entrada.")

        print("-" * 80)

# Ejemplo de uso:
if __name__ == "__main__":
    # Puedes cambiar esta URL por la de cualquier podcast o feed RSS
    url_feed = "https://media.rss.com/excelsior-by-rentero/feed.xml"  # Ejemplo: podcast de Lex Fridman
    leer_feed_y_mostrar_mp3(url_feed)
