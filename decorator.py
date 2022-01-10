def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.\n")
    return wrapper

# Esto es lo mismo que esto: say_whee = my_decorator(say_whee)

@my_decorator
def say_whee():
    print("Whee!")

say_whee()

# ------------------------------------------------------------------------------------------------

# Ahora agregamos otra funcion para que ejecute 2 veces la funcion decorator

def do_twice(func):
    def wrapper_do_twice():
        func()
        func()
    return wrapper_do_twice

@do_twice
def say_whee():
    print("Whee!")

say_whee()

# ------------------------------------------------------------------------------------------------

# Otro ejemplo de decorator basico

def myWrapper(func):
    def myInnerFunc():
      print("\nDentro del wrapper")
      func()
    return myInnerFunc

@myWrapper
def myFunc():
    print("Hola mundo!")

myFunc()