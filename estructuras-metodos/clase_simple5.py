class Circle:

    #pi es un atributo de clase, está fuera del constructor
    pi = 3.14159

    def __init__(self, radius):

        # radius es un atributo de instancia, pertenece a un metodo de la clase
        self.radius = radius
        self.pi = Circle.pi

    def area(self):
        return self.pi * self.radius**2

    def calc_cir(self, radius):
        self.radius = radius

    def circumference(self):
        return 2 * self.pi * self.radius

radius = 10

d = Circle(radius)
print(Circle.pi)
print(d.circumference())