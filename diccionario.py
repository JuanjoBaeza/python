
def main():

  thisdict =	{
    "brand": "Ford",
    "electric": False,
    "year": 1964,
    "colors": ["red", "white", "blue"]
  } 

  for x, y in thisdict.items():
    print(x, y) 

  print("")

  for x in thisdict.values():
    print(x)

  print("")

  for x, y in thisdict.items():
    print(x,":",y)

if __name__ == "__main__":
  main()