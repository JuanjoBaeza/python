def busqueda_secuencial(list_, n):

    found = False
    
    for i in list_:
        if i == n:
            found = True
            print(i)
            break
    return found

numeros = list(range(0,20))
print(busqueda_secuencial(numeros,16))