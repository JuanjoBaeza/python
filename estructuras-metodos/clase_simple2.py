class Estudiante:
    
    def __init__(self, nombre, edad, genero, altura):
        self.nombre = nombre
        self.edad   = edad
        self.genero = genero
        self.altura = altura
        
nombre = "Pepe"
edad = 25
genero = "M"
altura = 1.80

un_estudiante = Estudiante(nombre, edad, genero, altura)
print(un_estudiante.edad)

