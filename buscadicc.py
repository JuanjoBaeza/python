words = []
f = open("datos/diccionario_ingles.txt", "r")
words = f.read().split()

for word in words:

  chars  = ["t","e","e","n","c","a","n","r"]
  truths = []

  # 1. Loop through the chars
  for char in chars:
      # 2. Check if a character is in the target string
      truth = char in word
      # 3. Add the truth to a truths list
      truths.append(truth)
            
  # 4. Check if all boolean values are True
  has_all = True

  for truth in truths:
    has_all = has_all and truth
              
  print(has_all, word)