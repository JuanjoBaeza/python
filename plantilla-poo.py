
# 3 tipos de metodos en POO Python:
#
# - Instance methods -> Get/Set de atributos. 
#      Metodo de acceso get -> funcion mostrar_articulos.
#      Metodo de acceso set -> funcion actualiza_articulos.
# - Class methods - > Para trabajar con variables estáticas / de clase.
# - Static methods -> Cualquier método que no esté relacionado con un método de clase u objeto.

class BlogAutores:

    """ Aqui variables de clase/estaticas """

    tipo_autor = "Freelancer"

    def __init__(self, nombre_autor, numero_articulos):

        """ Aqui variables de instancia """

        self.nombre_autor = nombre_autor
        self.numero_articulos = numero_articulos
        print(f"Inicializado el constructor\n")

    def mostrar_articulos(self):

        """ Este metodo muestra los detalles del autor """

        print("Metodo Mostrar")
        print(f"Nombre de autor: {self.nombre_autor}\nArticulos publicados: {self.numero_articulos}\nTipo de autor: {BlogAutores.tipo_autor}\n")

    def actualiza_articulos(self, numero_articulos):

        """ Este metodo actualiza el nº de articulos """
        """ Aqui variables locales """

        print("Metodo Acualiza_articulos\n")
        self.numero_articulos = numero_articulos


if __name__ == '__main__':

    """ Instanciamos el objeto autor """

    autor = BlogAutores("Pedro", 10)

    """ Llamamos a los metodos """

    autor.mostrar_articulos()
    autor.actualiza_articulos(30)
    autor.mostrar_articulos()