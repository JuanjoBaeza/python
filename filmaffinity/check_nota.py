from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def crear_driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/129.0.0.0 Safari/537.36")
    options.add_argument("--accept-language=es-ES,es;q=0.9")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # 👇 Ejecuta Chromium directamente (sin undetected)
    service = Service("/snap/bin/chromium.chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def obtener_nota_filmaffinity(nombre_pelicula):
    query = nombre_pelicula.replace(" ", "+")
    url_busqueda = f"https://www.filmaffinity.com/es/search.php?stype=title&stext={query}"

    try:
        driver = crear_driver()
        driver.get(url_busqueda)

        # aceptar cookies si aparecen
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button#didomi-notice-agree-button"))
            ).click()
        except TimeoutException:
            pass

        # esperar a resultados o ficha
        WebDriverWait(driver, 15).until(
            lambda d: "/es/film" in d.current_url
            or d.find_elements(By.CSS_SELECTOR, "a[href*='/es/film']")
        )

        # si no es ficha, entrar en la primera
        if "/es/film" not in driver.current_url:
            enlaces = driver.find_elements(By.CSS_SELECTOR, "a[href*='/es/film']")
            if not enlaces:
                print(f"⚠ No se encontraron enlaces para '{nombre_pelicula}'")
                driver.quit()
                return None
            enlace_url = enlaces[0].get_attribute("href")
            driver.get(enlace_url)

        print(f"🎬 Entrando en ficha: {driver.current_url}")

        try:
            # Esperar a que se cargue el contenedor principal
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "rat-container"))
            )

            # Esperar adicional por seguridad
            time.sleep(3)

            # Esperar hasta que movie-rat-avg tenga texto visible
            nota_elem = WebDriverWait(driver, 10).until(
                lambda d: (
                    (el := d.find_element(By.ID, "movie-rat-avg"))
                    and el.text.strip() != ""
                )
            )

            # Obtener texto y limpiar
            nota = driver.find_element(By.ID, "movie-rat-avg").text.strip()
            print(f"⭐ Nota encontrada: {nota}")

        except Exception:
            # Último intento: usar JS directo (por si está oculto o cargado con delay)
            nota = driver.execute_script("""
                const el = document.querySelector('#movie-rat-avg');
                return el ? el.textContent.trim().replace(',', '.') : null;
            """)
            if nota and any(c.isdigit() for c in nota):
                print(f"⭐ Nota (vía JS): {nota}")
            else:
                print(f"⚠ No se logró obtener la nota de '{nombre_pelicula}'.")
                nota = None

    except WebDriverException as e:
        print(f"❌ Error general con '{nombre_pelicula}': {e}")
        return None


def procesar_archivo(entrada, salida):
    with open(entrada, "r", encoding="utf-8") as f_in, open(salida, "w", encoding="utf-8") as f_out:
        for linea in f_in:
            if "-" not in linea:
                continue
            nombre = linea.split("-")[0].strip()
            print(f"\n🔎 Buscando: {nombre} ...")
            nota = obtener_nota_filmaffinity(nombre)
            if nota:
                f_out.write(f"{nombre} - {nota}\n")
                print(f"✅ {nombre}: {nota}")
            else:
                f_out.write(f"{nombre} - No encontrada\n")
                print(f"❌ {nombre}: No encontrada")
            time.sleep(1)

if __name__ == "__main__":
    procesar_archivo("peliculas.txt", "resultados.txt")
