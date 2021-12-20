try:
   f = open("../datos/fichero3.txt", encoding = 'utf-8')
   print (f)
   
finally:
   f.close()