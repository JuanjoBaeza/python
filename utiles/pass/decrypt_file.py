from cryptography.fernet import Fernet

# opening the key
with open('utiles/pass/filekey.key', 'rb') as filekey:
    key = filekey.read()

# using the key
fernet = Fernet(key)
 
# opening the encrypted file
with open('utiles/pass/pass_file', 'rb') as enc_file:
    encrypted = enc_file.read()
 
# decrypting the file
decrypted = fernet.decrypt(encrypted)

myclearpass = decrypted

print(myclearpass.decode('UTF-8'))

# opening the file in write mode and
# writing the decrypted data

#with open('utiles/pass/pass_file', 'wb') as dec_file:
#    dec_file.write(decrypted)