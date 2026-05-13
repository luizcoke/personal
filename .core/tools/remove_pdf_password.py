"""
Remove password protection from a PDF file.

Usage:
    python remove_pdf_password.py <input.pdf> <password> [output.pdf]

If output path is omitted, saves as <input>_unlocked.pdf in the same directory.
"""

import sys
import os


def remove_password(input_path: str, password: str, output_path: str | None = None) -> None:
    try:
        import pikepdf
    except ImportError:
        print("pikepdf not found. Install it with: pip install pikepdf")
        sys.exit(1)

    if not os.path.isfile(input_path):
        print(f"File not found: {input_path}")
        sys.exit(1)

    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_unlocked{ext}"

    try:
        with pikepdf.open(input_path, password=password) as pdf:
            pdf.save(output_path)
        print(f"Saved unlocked PDF to: {output_path}")
    except pikepdf.PasswordError:
        print("Wrong password.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    input_pdf = sys.argv[1]
    password = sys.argv[2]
    output_pdf = sys.argv[3] if len(sys.argv) >= 4 else None

    remove_password(input_pdf, password, output_pdf)
