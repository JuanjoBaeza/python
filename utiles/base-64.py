import base64

b = base64.b64encode(bytes('your_string', 'utf-8')) # bytes
base64_str = b.decode('utf-8') # convert bytes to string

print(base64_str)