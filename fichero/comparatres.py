
def populat(File1, File2, File3):

    with open(File1,'r') as f:
        Lines1=set(f.readlines())

    with open(File2,'r') as f:
        Lines2=set(f.readlines())

    with open(File3,'a') as f:
      for line1 in Lines1:
        for line2 in Lines2:
          if(line1 == line2):
              f.write(line1)

def compare(File1, File2, File3):

    with open(File1,'r') as f:
        d=set(f.readlines())

    with open(File2,'r') as f:
        e=set(f.readlines())

    with open(File3,'a') as f:

        for line in list(e-d):
           f.write(line)

File1 = 'fichero/a.txt'
File2 = 'fichero/b.txt'
File3 = 'fichero/prod.txt'

populat(File1, File2, File3)
compare(File1, File2, File3)