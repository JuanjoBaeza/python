# f = open("datos/diccionario_ingles.txt", "r")

# seq = f.read()

seq = "teenager"

def valide(seq) :

    sub = ["t","e","e","n"]
    
    if all(s in sub for s in seq):
      print("True")
    else:
      print("False")

valide(seq)

