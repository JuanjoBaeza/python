class Human:

    '''
    This is a docstring.
    it is highly recommended that you put here a brief description    
    of the class
    '''

    def __init__(self): 
        self.name = 'Daisy'
        self.age = '24' 
        self.gender = 'Women' 

    def listen_to_music(self, song):
        return "{} is listening {}".format(self.name, song)
    def running(self, km):
         return "{} is running {}".format(self.name, km)
    def sing(self, song):
        return "{} is singing {}".format(self.name, song)
    def skate(self):
        return "{} is skating".format(self.name)

if __name__ == '__main__':
    persona = Human()
    
    a = persona.listen_to_music('MI_cancion')
    print (a)