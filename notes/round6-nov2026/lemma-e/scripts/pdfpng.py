"""Render PDF pages to PNG (untrusted input: run with python -I).
usage: python -I pdfpng.py file.pdf outprefix first last [zoom]"""
import sys
import pymupdf
doc = pymupdf.open(sys.argv[1])
a, b = int(sys.argv[3]), int(sys.argv[4])
z = float(sys.argv[5]) if len(sys.argv) > 5 else 1.6
for i in range(a - 1, min(b, len(doc))):
    pix = doc[i].get_pixmap(matrix=pymupdf.Matrix(z, z))
    out = f"{sys.argv[2]}_p{i+1}.png"
    pix.save(out)
    print(out, pix.width, pix.height)
