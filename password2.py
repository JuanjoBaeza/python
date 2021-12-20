import random

passlon = int(input("Longitud... "))
caracteres = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
resultado = "".join(random.sample(caracteres, passlon))
print(resultado)