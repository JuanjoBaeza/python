import os
import cv2
import subprocess
import numpy as np
from pydub import AudioSegment
from pydub.utils import mediainfo

def extract_audio(video_file, audio_output):
    """ Extrae el audio del video original usando FFmpeg. """
    try:
        print(f"🎵 Extrayendo audio de {video_file}...")
        command = ["ffmpeg", "-y", "-i", video_file, "-q:a", "0", "-map", "a", audio_output]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print("✅ Audio extraído con éxito.")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error al extraer el audio.")
        return False

def fix_audio_header(audio_file, fixed_audio):
    """ Intenta reparar el archivo de audio con FFmpeg. """
    try:
        print(f"🔧 Intentando reparar el audio {audio_file}...")
        command = ["ffmpeg", "-y", "-i", audio_file, "-c:a", "copy", fixed_audio]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print("✅ Audio reparado correctamente.")
        return True
    except subprocess.CalledProcessError:
        print("❌ No se pudo reparar el audio.")
        return False

def validate_audio(audio_file):
    """ Verifica si el archivo de audio es válido. """
    try:
        info = mediainfo(audio_file)
        return "duration" in info and float(info["duration"]) > 0
    except Exception as e:
        print(f"⚠️ Error al verificar audio: {e}")
        return False

def improve_image(image):
    """ Mejora la imagen (brillo, contraste, nitidez). """
    # Aplicar filtros de mejora en la imagen
    image = cv2.GaussianBlur(image, (5, 5), 0)  # Suavizado
    sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])  # Nitidez
    image = cv2.filter2D(image, -1, sharpen_kernel)
    image = cv2.convertScaleAbs(image, alpha=1.0, beta=20)  # Ajuste de brillo y contraste
    image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)  # Reducción de ruido
    return image

# 🔹 Archivos de entrada y salida
input_file     = "/mnt/c/Temp/ein.jpg"  # Puedes cambiar esto a un video si lo prefieres
extracted_audio = "/mnt/c/Temp/extracted_audio.mp3"
fixed_audio     = "/mnt/c/Temp/fixed_audio.mp3"
output_video    = "/mnt/c/Temp/enhanced_video.mp4"
output_image    = "/mnt/c/Temp/enhanced_image.jpg"

# 🔹 Detectar si la entrada es un video o una imagen
if input_file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):  # Si es un video
    # 🔹 Extraer audio del video
    if not extract_audio(input_file, extracted_audio):
        print("❌ No se pudo extraer el audio. Verifica el archivo de video.")
        exit(1)

    # 🔹 Verificar y reparar el audio
    if not validate_audio(extracted_audio):
        if fix_audio_header(extracted_audio, fixed_audio) and validate_audio(fixed_audio):
            extracted_audio = fixed_audio
        else:
            print("❌ Error crítico: No se pudo arreglar el audio.")
            exit(1)

    print(f"🎵 Archivo de audio listo: {extracted_audio}")

    # 🔹 Procesar el video con OpenCV
    video = cv2.VideoCapture(input_file)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Nuevo tamaño escalado
    new_width, new_height = width * 2, height * 2

    # Configurar el escritor de video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    temp_video = "temp_video.mp4"
    out = cv2.VideoWriter(temp_video, fourcc, fps, (new_width, new_height))

    print("📺 Procesando video...")

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break  

        # Escalar el frame
        frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

        # Aplicar mejoras
        frame = improve_image(frame)

        out.write(frame)

    video.release()
    out.release()
    cv2.destroyAllWindows()

    print("✅ Video escalado y mejorado guardado como temp_video.mp4")

    # 🔹 Unir el video mejorado con el audio corregido
    print("🔄 Uniendo el video con el audio corregido...")
    command = [
        "ffmpeg", "-y",
        "-i", temp_video,
        "-i", extracted_audio,
        "-c:v", "copy",
        "-c:a", "aac",
        "-strict", "experimental",
        output_video
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 🔹 Eliminar archivos temporales
    os.remove(temp_video)

    print(f"✅ Proceso finalizado. Video guardado como: {output_video}")

elif input_file.lower().endswith(('.jpg', '.jpeg', '.png')):  # Si es una imagen
    # Cargar la imagen
    image = cv2.imread(input_file)

    # Mejorar la imagen
    enhanced_image = improve_image(image)

    # Guardar la imagen mejorada
    cv2.imwrite(output_image, enhanced_image)
    print(f"✅ Imagen mejorada guardada como: {output_image}")
else:
    print("❌ El archivo no es ni un video ni una imagen soportada.")
