"""
Extract text from a PDF file (page by page) and write to a .txt file.

Usage:
    python extract_pdf_text.py <input.pdf> [output.txt]

If output path is omitted, saves as <input>.txt in the same directory.
"""

import sys
import os


def extract_text(input_path: str, output_path: str | None = None) -> None:
    try:
        import pdfplumber
    except ImportError:
        print("pdfplumber not found. Install it with: pip install pdfplumber")
        sys.exit(1)

    if not os.path.isfile(input_path):
        print(f"File not found: {input_path}")
        sys.exit(1)

    if output_path is None:
        base, _ = os.path.splitext(input_path)
        output_path = f"{base}.txt"

    try:
        with pdfplumber.open(input_path) as pdf:
            pages_text = []
            for i, page in enumerate(pdf.pages, start=1):
                text = page.extract_text(layout=True) or ""
                pages_text.append(f"=== Página {i} ===\n{text}")

        full_text = "\n\n".join(pages_text)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        print(f"Texto extraído em: {output_path}")
        print(f"Total de páginas: {len(pages_text)}")
    except Exception as e:
        print(f"Erro ao extrair texto: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_txt = sys.argv[2] if len(sys.argv) >= 3 else None

    extract_text(input_pdf, output_txt)
