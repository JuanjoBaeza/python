import pyqrcode 
from pyqrcode import QRCode
from svglib.svglib import svg2rlg

qr = "https://www.123sms.es"
url = pyqrcode.create(qr)

url.svg("images/qr-code.svg", scale = 8)