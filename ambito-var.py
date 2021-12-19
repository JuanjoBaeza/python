def saludar(*personas): 
    
    for name in personas:
        print("Hello " + name)
    
saludar ("Juan", "Maria", "Pedro")

x = "5"

def foo():
    x = "10"
    print(x)

foo()

print (x)
