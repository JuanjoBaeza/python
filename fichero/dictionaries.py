# Version A
names_and_ages = {'Pedro':20, 'Juan':30, 'Pepe':50}
print ('A', names_and_ages)

# Version B
names_and_ages = dict(Pedro=20, Juan=30, Pepe=50)
print ('B', names_and_ages)

# Version C
names_and_ages = dict([('Pedro',20), ('Juan',30), ('Pepe',50)])
print ('C', names_and_ages)

# Version D
names = 'Pedro', 'Juan', 'Pepe'
ages = 20,30,50
names_and_ages = dict(zip(names, ages))

print ('D', names_and_ages)