
class Persona:
    
    "Informacion de la clase"
    edad=10

    def saludo(self):
        print("Hola")

str = Persona()

print(Persona.edad)
print(Persona.saludo)
print(Persona.__doc__)

str.saludo()