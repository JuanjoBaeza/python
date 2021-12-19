# PDF to Images
import fitz
pdf = 'sample.pdf'
doc = fitz.open(pdf)
 
for page in doc:
    pix = page.getPixmap(alpha=False)
    pix.writePNG('page-%i.png' % page.number)