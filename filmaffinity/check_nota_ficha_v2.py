from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


def crear_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/118.0.0.0 Safari/537.36")
    return webdriver.Chrome(service=Service(), options=options)


def aceptar_cookies(driver):
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"))
        )
        driver.find_element(By.CSS_SELECTOR, "button#onetrust-accept-btn-handler").click()
        print("🍪 Cookies aceptadas.")
        time.sleep(1)
    except Exception:
        pass


def obtener_url_ficha(pelicula: str) -> str | None:
    driver = crear_driver()
    try:
        query = pelicula.replace(" ", "+")
        url_busqueda = f"https://www.filmaffinity.com/es/search.php?stext={query}"
        driver.get(url_busqueda)
        aceptar_cookies(driver)

        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".mc-title a"))
        )
        enlaces = driver.find_elements(By.CSS_SELECTOR, ".mc-title a")
        
        if not enlaces:
            print(f"⚠️ No se encontraron resultados para '{pelicula}'.")
            return None
        elif len(enlaces) > 1:
            print(f"📊 Varios resultados para '{pelicula}'. Se devuelve el primero.")

        url_ficha = enlaces[0].get_attribute("href")
        print(f"🔗 {pelicula} → {url_ficha}")
        return url_ficha

    except TimeoutException:
        print(f"❌ Timeout buscando '{pelicula}'. Posible bloqueo o challenge.")
        return None
    finally:
        driver.quit()
        time.sleep(2)  # pequeña pausa entre peticiones


def procesar_peliculas(peliculas: list[str]):
    resultados = {}
    for pelicula in peliculas:
        print(f"\n🔎 Buscando: {pelicula}")
        url = obtener_url_ficha(pelicula)
        resultados[pelicula] = url or "No encontrada"
        guardar_resultados(resultados, archivo_salida)
    return resultados

# === Guardar resultados ===
def guardar_resultados(resultados: dict, ruta_archivo: str):
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write("✅ Resultados:\n\n")
        for nombre, url in resultados.items():
            linea = f"{nombre}: {url}\n"
            f.write(linea)
            print(linea.strip())  # También imprime en consola
    print(f"\n💾 Resultados guardados en '{ruta_archivo}'")

if __name__ == "__main__":
    
    archivo_salida = "resultados.txt"
    peliculas = [
        "The Godfather",
        "Inception",
        "Interstellar",
        "Amelie",
        "Matrix"
    ]

    resultados = procesar_peliculas(peliculas)