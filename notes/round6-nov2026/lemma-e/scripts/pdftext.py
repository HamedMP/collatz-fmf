"""Extract text from pages of a PDF (untrusted input: run with python -I).
usage: python -I pdftext.py file.pdf first last  (1-based, inclusive)"""
import sys
try:
    import fitz  # pymupdf
    doc = fitz.open(sys.argv[1])
    a, b = int(sys.argv[2]), int(sys.argv[3])
    for i in range(a - 1, min(b, len(doc))):
        print(f"=== page {i+1} ===")
        print(doc[i].get_text())
except ImportError:
    from pypdf import PdfReader
    r = PdfReader(sys.argv[1])
    a, b = int(sys.argv[2]), int(sys.argv[3])
    for i in range(a - 1, min(b, len(r.pages))):
        print(f"=== page {i+1} ===")
        print(r.pages[i].extract_text())
