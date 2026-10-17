"""fetch_sources.py - fetch full text for the literature review.

Usage: python scripts/fetch_sources.py [--search cr_scratch/lit/search.md]
         [--user sources] [--out cr_scratch/lit]
         [--to-get cr_scratch/sources_to_get.md]
         [--skip cr_scratch/intake_answers.md]

1. Reads the `| S01 | claims | citation | url |` rows of the search file.
   Each url is downloaded (arXiv abs links become pdf links). PDF text comes
   from pypdf; HTML has tags stripped. 2,000 words or more counts as full
   text (an HTML page also needs two section words: introduction, background,
   methods, results, discussion, conclusion) and is written to OUT/S01.txt with Citation and URL header lines.
   Fewer words (an abstract or a paywall page) or a failed download puts the
   citation on the to-get list.
2. Each .pdf, .txt or .md file in the user folder becomes OUT/U01.txt,
   except files named in the skip file (the solicitation, FAQ and NRA).
3. The to-get file is rewritten on every run: a heading, then one numbered
   full citation per source not fetched.
Prints one line per source (OK or TO GET) and a final count line. Exit 0.
"""
import argparse
import html
import io
import os
import re
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows cp1252 consoles

MIN_WORDS = 2000
MAX_BYTES = 40 * 1024 * 1024
SECTIONS = ("introduction", "background", "methods", "results", "discussion", "conclusion")
ROW_RE = re.compile(r"^\|\s*(S\d+)\s*\|([^|]*)\|([^|]+)\|([^|]*)\|")


def pdf_text(data):
    from pypdf import PdfReader
    r = PdfReader(io.BytesIO(data))
    return "\n".join((p.extract_text() or "") for p in r.pages)


def html_text(raw):
    raw = re.sub(r"(?is)<(script|style|nav|header|footer)\b.*?</\1>", " ", raw)
    return html.unescape(re.sub(r"(?s)<[^>]+>", " ", raw))


def fetch(url):
    url = re.sub(r"arxiv\.org/abs/([^\s?#]+)", r"arxiv.org/pdf/\1", url)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (fetch_sources.py)"})
    with urllib.request.urlopen(req, timeout=45) as r:
        data = r.read(MAX_BYTES)
    if data[:5] == b"%PDF-":
        return pdf_text(data)
    text = html_text(data.decode("utf-8", errors="replace"))
    low = text.lower()
    found = [w for w in SECTIONS if w in low]
    if len(found) < 2:
        return ""  # an abstract or landing page, not the paper
    return text


def file_text(path):
    if path.lower().endswith(".pdf"):
        return pdf_text(open(path, "rb").read())
    return open(path, encoding="utf-8", errors="replace").read()


def words(t):
    return len(t.split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--search", default="cr_scratch/lit/search.md")
    ap.add_argument("--user", default="sources")
    ap.add_argument("--out", default="cr_scratch/lit")
    ap.add_argument("--to-get", default="cr_scratch/sources_to_get.md")
    ap.add_argument("--skip", default="cr_scratch/intake_answers.md")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    fetched, to_get, user = 0, [], 0

    rows = []
    if os.path.exists(a.search):
        for ln in open(a.search, encoding="utf-8-sig"):
            m = ROW_RE.match(ln.strip())
            if m:
                rows.append((m.group(1), m.group(3).strip(), m.group(4).strip()))
    for sid, cite, url in rows:
        text, why = "", "no url"
        if url.lower().startswith("http"):
            try:
                text = fetch(url)
                why = "words=%d" % words(text)
            except Exception as e:  # any download or parse failure
                why = type(e).__name__
        if words(text) >= MIN_WORDS:
            with open(os.path.join(a.out, sid + ".txt"), "w", encoding="utf-8") as f:
                f.write("Citation: %s\nURL: %s\n\n%s\n" % (cite, url, text))
            fetched += 1
            print("OK %s %s %s.txt" % (sid, why, sid))
        else:
            to_get.append(cite)
            print("TO GET %s %s" % (sid, why))

    skip = open(a.skip, encoding="utf-8").read() if os.path.exists(a.skip) else ""
    if os.path.isdir(a.user):
        for name in sorted(os.listdir(a.user)):
            path = os.path.join(a.user, name)
            if not name.lower().endswith((".pdf", ".txt", ".md")) or name in skip:
                continue
            try:
                text = file_text(path)
            except Exception as e:
                print("TO GET user file %s %s" % (name, type(e).__name__))
                continue
            user += 1
            uid = "U%02d" % user
            with open(os.path.join(a.out, uid + ".txt"), "w", encoding="utf-8") as f:
                f.write("Citation: see file text (%s)\nFile: %s\n\n%s\n" % (name, path, text))
            print("OK %s words=%d %s.txt (%s)" % (uid, words(text), uid, name))

    with open(a.to_get, "w", encoding="utf-8") as f:
        f.write("## SOURCES TO GET BEFORE THE NEXT REVISION\n\n")
        for i, c in enumerate(to_get, 1):
            f.write("%d. %s\n" % (i, c))
    print("FETCHED %d USER %d TO GET %d" % (fetched, user, len(to_get)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
