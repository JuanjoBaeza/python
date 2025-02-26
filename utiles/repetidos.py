import os
from collections import defaultdict

def buscar_archivos_repetidos(ruta_base):
    # Diccionario para almacenar los archivos y sus rutas
    archivos_dict = defaultdict(list)

    # Recorrer la ruta de forma recursiva
    for ruta_actual, _, archivos in os.walk(ruta_base):
        for archivo in archivos:
            archivos_dict[archivo].append(os.path.join(ruta_actual, archivo))

    # Filtrar los archivos repetidos
    archivos_repetidos = {archivo: rutas for archivo, rutas in archivos_dict.items() if len(rutas) > 1}

    return archivos_repetidos

def main():
    ruta = input("Ingrese la ruta para buscar archivos repetidos: ").strip()

    if not os.path.isdir(ruta):
        print(f"La ruta {ruta} no es válida.")
        return

    repetidos = buscar_archivos_repetidos(ruta)

    if repetidos:
        print("Archivos repetidos encontrados:")
        for archivo, rutas in repetidos.items():
            print(f"\nArchivo: {archivo}")
            for ruta in rutas:
                print(f"  - {ruta}")
    else:
        print("No se encontraron archivos repetidos.")

if __name__ == "__main__":
    main()
