from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def crear_driver():
    options = Options()
    options.add_argument("--headless=new")  # Headless moderno
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/118.0.0.0 Safari/537.36")
    return webdriver.Chrome(service=Service(), options=options)

def obtener_nota_filmaffinity(url):
    driver = crear_driver()
    driver.get(url)

    try:
        # Espera hasta que el elemento aparezca (máx. 20 s)
        nota_elem = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "movie-rat-avg"))
        )
        nota = nota_elem.text.strip()
    except Exception as e:
        print("❌ No se encontró el rating:", e)
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        nota = None
    finally:
        driver.quit()

    return nota

# 🧪 Ejemplo real:
url = "https://www.filmaffinity.com/es/film809297.html"  # El Padrino
print("⭐ La nota es:", obtener_nota_filmaffinity(url))
