from datetime import datetime
import OpenSSL
import ssl

cert=ssl.get_server_certificate(('www.yahoo.com', 443))
x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
bytes=x509.get_notAfter()

print(bytes)
timestamp = bytes.decode('utf-8')
fecha = datetime.strptime(timestamp, '%Y%m%d%H%M%S%z').date().isoformat()

conv = datetime.strptime(fecha, "%Y-%m-%d").strftime("%d-%m-%Y")

print(conv)