"""assemble_pdf.py - merge the overview chart and the proposal body into one PDF.

Usage: assemble_pdf.py --chart proposal/overview_chart.docx
         --body proposal/proposal_body.docx --out proposal/proposal_stepA.pdf

Converts both files with LibreOffice headless into a temp folder, merges the
chart first and the body second, prints the page count and the size in MB, and
exits 1 when the size is 20 MB or more. LibreOffice is found in this order:
env NIAC_SOFFICE (a path; the value `none` hides LibreOffice), `soffice` on
PATH, then the default install paths for Windows, macOS and Linux. Not found:
prints RENDER TOOL MISSING and exits 1.
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows cp1252 consoles
import tempfile

LIMIT_MB = 20.0
DEFAULTS = [
    "C:/Program Files/LibreOffice/program/soffice.exe",
    "C:/Program Files (x86)/LibreOffice/program/soffice.exe",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    "/usr/bin/soffice", "/usr/local/bin/soffice",
    "/usr/lib/libreoffice/program/soffice",
    "/opt/libreoffice/program/soffice", "/snap/bin/libreoffice",
]


def find_soffice():
    env = os.environ.get("NIAC_SOFFICE")
    if env:
        if env.lower() == "none":
            return None
        return env if os.path.isfile(env) else None
    w = shutil.which("soffice")
    if w:
        return w
    for d in DEFAULTS + glob.glob("/opt/libreoffice*/program/soffice"):
        if os.path.isfile(d):
            return d
    return None


def convert(soffice, src, tmp, tag):
    sub = os.path.join(tmp, tag)
    os.makedirs(sub)
    profile = "file:///" + os.path.join(tmp, "profile").replace(
        "\\", "/").lstrip("/")
    r = subprocess.run([soffice, "-env:UserInstallation=" + profile,
                        "--headless", "--convert-to", "pdf", "--outdir", sub,
                        os.path.abspath(src)], capture_output=True, text=True,
                       timeout=300)
    pdf = os.path.join(sub, os.path.splitext(os.path.basename(src))[0]
                       + ".pdf")
    if not os.path.isfile(pdf):
        print("CONVERT FAILED %s: %s" % (src, (r.stderr or r.stdout).strip()))
        return None
    return pdf


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--chart", required=True)
    ap.add_argument("--body", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    soffice = find_soffice()
    if not soffice:
        print("RENDER TOOL MISSING")
        return 1
    for f in (a.chart, a.body):
        if not os.path.isfile(f):
            print("FILE NOT FOUND %s" % f)
            return 2
    import pypdf
    with tempfile.TemporaryDirectory() as tmp:
        c = convert(soffice, a.chart, tmp, "chart")
        b = convert(soffice, a.body, tmp, "body")
        if not c or not b:
            return 1
        w = pypdf.PdfWriter()
        for f in (c, b):
            for pg in pypdf.PdfReader(f).pages:
                w.add_page(pg)
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        with open(a.out, "wb") as fh:
            w.write(fh)
    mb = os.path.getsize(a.out) / 1048576.0
    print("PAGES %d" % len(pypdf.PdfReader(a.out).pages))
    print("SIZE_MB %.2f" % mb)
    print("WROTE %s" % a.out)
    if mb >= LIMIT_MB:
        print("FAIL size %.2f MB is 20 MB or more" % mb)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
