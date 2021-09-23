import getpass
import os

os.system('cls')

database = {"juanjo": "123456"}
username = input("Enter Your Username : ")
password = ""

for i in database.keys():
    if username == i:
        while password != database.get(i):
            password = getpass.getpass("Enter Your Password: ")
        print("OK")
    elif username !=i:
        print("User not in list")