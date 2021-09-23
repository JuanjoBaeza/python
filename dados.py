import random

min_val = 1
max_val = 6

nuevatirada = "Si"

while nuevatirada == "Si" or nuevatirada == "S":

    #generating and printing 1st random integer from 1 to 6
    print(random.randint(min_val, max_val))
    
    #generating and printing 2nd random integer from 1 to 6
    print(random.randint(min_val, max_val))
    
    nuevatirada = input("Lanzar dados? ").capitalize()