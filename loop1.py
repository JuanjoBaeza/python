amigos = {'01':'Juanjo' , '02':'Pedro' , '03':'David' , '04':'Luis'}

amigos['05'] = 'Alejandro'

print ("Amigos:")

for amigo in amigos:
    print(amigos[amigo])

nombre = input("Entra ID del amigo: ")

for amigo in amigos:
    if amigo == nombre:
        print(amigos[amigo])
        break