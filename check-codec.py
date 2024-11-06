import os
import subprocess

# Función para obtener el códec de un archivo de video
def get_video_codec_and_resolution(file_path):
    try:
        # Ejecuta ffprobe para obtener el códec y la resolución del video
        codec_result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 
             'stream=codec_name,width,height', '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        codec_info = codec_result.stdout.strip().split('\n')
        codec = codec_info[0] if len(codec_info) > 0 else 'Desconocido'
        resolution = f"{codec_info[1]}x{codec_info[2]}" if len(codec_info) > 2 else 'Resolución desconocida'
        return codec, resolution
    except Exception as e:
        return f"Error obteniendo información: {e}", "Resolución desconocida"

# Función para recorrer el directorio, analizar los archivos de video y guardar los archivos HEVC en un fichero de texto
def check_video_codecs(directory, output_file):
    with open(output_file, 'w') as f_out:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv')):
                    file_path = os.path.join(root, file)
                    codec, resolution = get_video_codec_and_resolution(file_path)
                    print(f"Archivo: {file}, Códec de video: {codec}, Resolucion {resolution}")
                    if codec == 'hevc':
                        f_out.write(f"{file_path} - Resolución: {resolution}\n")
#                       print(f"Archivo HEVC encontrado: {file_path}, Resolución: {resolution}")

# Cambia 'ruta_del_directorio' a la ruta de tu directorio de video y 'salida.txt' al nombre del archivo de salida
check_video_codecs('/mnt/z/E01', '/tmp/salidaE1.txt')
