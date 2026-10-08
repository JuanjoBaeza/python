#!/usr/bin/env python3
import os
import shutil
import warnings
import numpy as np
from tqdm import tqdm
from PIL import Image, ImageFile

warnings.filterwarnings("ignore", category=UserWarning)

ImageFile.LOAD_TRUNCATED_IMAGES = True

import face_recognition

# ==================== CONFIGURACIÓN DE VELOCIDAD ====================
ACTIVAR_OCR = False       # Mantenlo en False si solo buscas por cara
MODELO_FACIAL = "dlib"    # ⚡ "hog" es instantáneo en CPU. Cambia a "cnn" solo si dlib usa GPU real.
MAX_RESOLUCION = 1200     # 📉 Redimensiona fotos grandes a este ancho/alto máximo para ir 10x más rápido.
# ===================================================================

# === CONFIGURACIÓN DE RUTAS ===
FOTO_REFERENCIA = "/mnt/c/Users/Admin/Downloads/Fotos_Caravaca/mi_cara.jpg"
DIR_ORIGEN = "/mnt/c/Users/Admin/Downloads/Fotos_Caravaca"
DIR_DESTINO = "/mnt/c/Users/Admin/Downloads/Fotos_Caravaca/fotos_encontradas"

DORSAL_OBJETIVO = "1091"
EXTENSIONES_VALIDAS = ('.jpg', '.jpeg', '.png', '.webp')

def cargar_imagen_optimizada(ruta):
    """Abre la imagen de forma segura, la fuerza a RGB y la redimensiona para acelerar el proceso."""
    try:
        with Image.open(ruta) as img:
            # Forzar la carga física de los píxeles aquí dentro del try para capturar cualquier fallo de archivo corrupto
            img.load() 
            
            img_rgb = img.convert('RGB')
            ancho, alto = img_rgb.size
            
            # Redimensionamiento manual seguro: evita problemas internos de la función thumbnail()
            if max(ancho, alto) > MAX_RESOLUCION:
                if ancho > alto:
                    nuevo_ancho = MAX_RESOLUCION
                    nuevo_alto = int(alto * (MAX_RESOLUCION / ancho))
                else:
                    nuevo_alto = MAX_RESOLUCION
                    nuevo_ancho = int(ancho * (MAX_RESOLUCION / alto))
                
                # Usamos un método de redimensionamiento directo y rápido
                img_rgb = img_rgb.resize((nuevo_ancho, nuevo_alto), Image.NEAREST)
                
            return np.array(img_rgb, dtype=np.uint8)
    except Exception as e:
        # Si la foto está totalmente rota, la saltará silenciosamente para no detener el escaneo de las 9,000 fotos
        return None

def cargar_perfil_referencia(ruta_referencia):
    """Carga tu rostro de referencia."""
    imagen_normalizada = cargar_imagen_optimizada(ruta_referencia)
    if imagen_normalizada is None:
        return None
    try:
        codificaciones = face_recognition.face_encodings(imagen_normalizada)
        if len(codificaciones) == 0:
            print("⚠️ Aviso: No se detectó rostro en la foto de referencia.")
            return None
        print("✅ Foto de referencia cargada correctamente.")
        return codificaciones[0]  # Retorna la lista completa de codificaciones
    except Exception as e:
        print(f"❌ Error al procesar la referencia: {e}")
        return None

def buscar_y_copiar_fotos():
    print(f"⚙️ Modo de escaneo activo: Modelo Facial = '{MODELO_FACIAL}' | OCR = {ACTIVAR_OCR}")
    
    lector_ocr = None
    if ACTIVAR_OCR:
        import easyocr
        import torch
        lector_ocr = easyocr.Reader(['en'], gpu=torch.cuda.is_available(), recog_network='standard')

    mi_perfil = cargar_perfil_referencia(FOTO_REFERENCIA)
    if mi_perfil is None and not ACTIVAR_OCR:
        print("❌ Error: Nada que buscar.")
        return

    if not os.path.exists(DIR_DESTINO):
        os.makedirs(DIR_DESTINO)

    print("📁 Indexando archivos de imagen...")
    lista_fotos = []
    for raiz, _, archivos in os.walk(DIR_ORIGEN):
        if os.path.abspath(raiz).startswith(os.path.abspath(DIR_DESTINO)):
            continue
        for archivo in archivos:
            if archivo.lower().endswith(EXTENSIONES_VALIDAS):
                if os.path.basename(FOTO_REFERENCIA) != archivo:
                    lista_fotos.append(os.path.join(raiz, archivo))

    total_fotos = len(lista_fotos)
    print(f"📸 Se encontraron {total_fotos} fotos para analizar.")
    
    if total_fotos == 0:
        return

    total_copiadas = 0
    print("\n🔍 Escaneando a alta velocidad...")

    with tqdm(lista_fotos, desc="Progreso", unit="foto") as barra_progreso:
        for ruta_completa in barra_progreso:
            archivo = os.path.basename(ruta_completa)
            hacer_copia = False
            motivo = ""
            
            try:
                # 1. OCR (Dorsal)
                if ACTIVAR_OCR and lector_ocr is not None:
                    resultados_ocr = lector_ocr.readtext(ruta_completa, detail=0)
                    texto_unido = "".join(resultados_ocr)
                    if DORSAL_OBJETIVO in texto_unido:
                        hacer_copia = True
                        motivo = f"Dorsal {DORSAL_OBJETIVO}"

                # 2. Rostro (Usa la imagen encogida optimizada)
                if not hacer_copia and mi_perfil is not None:
                    imagen_busqueda = cargar_imagen_optimizada(ruta_completa)
                    if imagen_busqueda is not None:
                        # Ejecutamos el modelo HOG, optimizado para CPU
                        caras_en_foto = face_recognition.face_encodings(imagen_busqueda, model=MODELO_FACIAL)
                        
                        if len(caras_en_foto) > 0:
                            coincidencias = face_recognition.compare_faces(caras_en_foto, mi_perfil, tolerance=0.55)
                            if any(coincidencias):
                                hacer_copia = True
                                motivo = "Rostro"

                # 3. Copiar acierto
                if hacer_copia:
                    nombre_destino = archivo
                    ruta_destino_final = os.path.join(DIR_DESTINO, nombre_destino)
                    
                    contador = 1
                    while os.path.exists(ruta_destino_final):
                        nombre, ext = os.path.splitext(archivo)
                        nombre_destino = f"{nombre}_{contador}{ext}"
                        ruta_destino_final = os.path.join(DIR_DESTINO, nombre_destino)
                        contador += 1
                    
                    shutil.copy2(ruta_completa, ruta_destino_final)
                    total_copiadas += 1
                    barra_progreso.set_postfix_str(f"Match: {archivo} ({motivo})")
                        
            except Exception as e:
                tqdm.write(f"⚠️ Error en {archivo}: {e}")

    print(f"\n🎉 Escaneo finalizado. Se copiaron {total_copiadas} fotos.")

if __name__ == "__main__":
    buscar_y_copiar_fotos()
