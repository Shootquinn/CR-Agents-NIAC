"""Print one status line per tool. Exit code is always 0."""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows cp1252 consoles
import os
import shutil
import sys


def check_python():
    v = sys.version_info
    if v >= (3, 8):
        return "OK python %d.%d.%d" % (v[0], v[1], v[2])
    return "MISSING python"


def check_docx():
    try:
        import docx  # noqa: F401
        return "OK python-docx"
    except Exception:
        return "MISSING python-docx"


def check_libreoffice():
    if shutil.which("soffice") or shutil.which("libreoffice"):
        return "OK LibreOffice"
    for p in ("C:/Program Files/LibreOffice/program/soffice.exe",
              "C:/Program Files (x86)/LibreOffice/program/soffice.exe"):
        if os.path.exists(p):
            return "OK LibreOffice"
    return "MISSING LibreOffice"


def check_pdf():
    if shutil.which("pdftotext"):
        return "OK pdf-text"
    for mod in ("pypdf", "fitz"):
        try:
            __import__(mod)
            return "OK pdf-text"
        except Exception:
            pass
    return "MISSING pdf-text"


if __name__ == "__main__":
    for name, fn in (("python", check_python), ("python-docx", check_docx),
                     ("LibreOffice", check_libreoffice), ("pdf-text", check_pdf)):
        try:
            print(fn())
        except Exception:
            print("MISSING " + name)
    sys.exit(0)
