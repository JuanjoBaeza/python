grados = float(input("Grados a convertir: "))
tipo   = input("A Farenhait o Celsius? (C o F): ").capitalize()

def f2c(grados):

        gradoscen = (grados - 32) * 5/9
        print(gradoscen , "Celsius")
        quit()

def c2f(grados):

        gradosfaren = (grados * 1.8) + 32
        print(gradosfaren , "Farenhait")
        quit()

while (tipo != "F" or tipo != "C"):

    tipo = input("Farenhait o Celsius? (C o F): ").capitalize()

    if(tipo == "F"):
        c2f(grados)
    elif(tipo == "C"):
        f2c(grados)