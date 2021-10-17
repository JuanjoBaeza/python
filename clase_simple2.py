class Estudiante:
    
    def __init__(self, nombre, edad, genero, altura):
        self.nombre = nombre
        self.edad   = edad
        self.genero = genero
        self.altura = altura
        
un_estudiante = Estudiante('Pepe',15,'masculino','1.80m')

print(un_estudiante.altura)

