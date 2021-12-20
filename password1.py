import getpass

database = {"juanjo": "123", "juan": "1234"}
username = input("Enter Your Username : ")
password = getpass.getpass("Enter Your Password : ")

for i in database.keys():

    if i == username:
        while password != database.get(i):
            password = getpass.getpass("Enter Your Password Again: ")
        print("Verified")
        break
    else:
        print ("User not found")