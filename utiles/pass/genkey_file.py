from cryptography.fernet import Fernet

# key generation
key = Fernet.generate_key()
 
# string the key in a file
with open('utiles/pass/filekey.key', 'wb') as filekey:
   filekey.write(key)