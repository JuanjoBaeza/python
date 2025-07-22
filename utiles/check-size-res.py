import os
import subprocess

def convertir_tamano(bytes):
    """Convierte el tamaño de bytes a MB o GB según corresponda."""
    mb = bytes / (1024 * 1024)
    if mb < 1024:
        return f"{mb:.2f} MB"
    gb = mb / 1024
    return f"{gb:.2f} GB"

def obtener_resolucion(ruta_video):
    """Obtiene la resolución del video usando ffprobe."""
    try:
        resultado = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", ruta_video],
            capture_output=True, text=True, check=True
        )
        resolucion = resultado.stdout.strip().replace(',', 'x')
        if resolucion:
            ancho, alto = map(int, resolucion.split('x'))
            return ancho, alto
        return None
    except subprocess.CalledProcessError:
        return None

def buscar_archivos_video(directorio, archivo_salida):
    extensiones_video = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"}  # Agrega más si es necesario
    archivos_encontrados = []
    limite_tamano = 1.5 * 1024 * 1024 * 1024  # 1.5GB en bytes
    
    for raiz, _, archivos in os.walk(directorio):
        for archivo in archivos:
            extension = os.path.splitext(archivo)[1].lower()
            if extension in extensiones_video:
                ruta_completa = os.path.join(raiz, archivo)
                tamano = os.path.getsize(ruta_completa)
                if tamano < limite_tamano:  # Filtrar archivos menores a 2GB
                    resolucion = obtener_resolucion(ruta_completa)
                    if resolucion:
                        ancho, alto = resolucion
                        # Solo incluir archivos con resolución horizontal menor a 1280
                        if ancho < 1280:
                            nombre_sin_extension = os.path.splitext(archivo)[0]
                            archivos_encontrados.append((raiz, nombre_sin_extension, f"{ancho}x{alto}", tamano))
     
    archivos_encontrados.sort(key=lambda x: x[3])
    
    with open(archivo_salida, 'a', encoding='utf-8') as f:
        for raiz, nombre, resolucion, tamano in archivos_encontrados:
            f.write(f"{nombre} - {resolucion} - {convertir_tamano(tamano)}\n")
    
    print(f"Información guardada en {archivo_salida} directorio {directorio}")


alfa = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0-9']

for i in alfa:
    dir = "/mnt/z/" + i
    archivo_salida = "/home/juanjo/informacion_videos.txt"
    buscar_archivos_video(dir, archivo_salida)
