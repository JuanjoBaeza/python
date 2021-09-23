# -*- coding: utf-8 -*

# Buscador de cadenas en ficheros de un directorio

import os
import re

cadena    = input("Cadena a buscar: ")
ruta      = input("Ruta (formato c:/temp/): ")
ignorados = {"Crack"}

print ()

entradas = [i for i in os.listdir(ruta) if i not in ignorados]

for entrada in entradas:
    f = open(ruta + entrada, 'r', encoding="utf-8")
    
    contenido = f.read()
    palabra  = re.findall(cadena + '\w+', contenido)
    
    print(entrada, palabra)
