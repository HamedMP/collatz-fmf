"""pdf_tool.py -- extract text / render pages of a PDF given as argument.

Usage (run with -I, PDF path passed as argument, never run from inside the PDF dir):
  python -I pdf_tool.py text  <pdf> <out.txt>
  python -I pdf_tool.py png   <pdf> <outdir> <first_page> <last_page> [zoom]
"""
import sys
import fitz  # pymupdf


def main():
    mode, pdf = sys.argv[1], sys.argv[2]
    doc = fitz.open(pdf)
    if mode == "text":
        out = sys.argv[3]
        total = 0
        with open(out, "w") as f:
            for i, page in enumerate(doc):
                t = page.get_text()
                total += len(t)
                f.write(f"\n===== PAGE {i+1} =====\n")
                f.write(t)
        print("pages", len(doc), "chars", total)
    elif mode == "png":
        outdir, a, b = sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
        zoom = float(sys.argv[6]) if len(sys.argv) > 6 else 2.0
        for i in range(a - 1, min(b, len(doc))):
            pix = doc[i].get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            pix.save(f"{outdir}/page{i+1:02d}.png")
            print("wrote", f"{outdir}/page{i+1:02d}.png", pix.width, pix.height)


main()
