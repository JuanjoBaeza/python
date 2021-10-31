try:
   f = open("/mnt/c//Repo/python/datos/fichero3.txt", encoding = 'utf-8')
   print (f)
   
finally:
   f.close()