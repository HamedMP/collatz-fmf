"""Extract text from a PDF (untrusted data) to a .txt file. Usage: pdf2txt.py in.pdf out.txt"""
import sys
import fitz  # PyMuPDF

doc = fitz.open(sys.argv[1])
with open(sys.argv[2], "w") as f:
    for i, page in enumerate(doc):
        f.write(f"\n===== PAGE {i+1} =====\n")
        f.write(page.get_text())
print("pages:", len(doc), "metadata:", doc.metadata)
