"""fetch_sources.py - fetch full text for the literature review.

Usage: python scripts/fetch_sources.py [--search cr_scratch/lit/search.md ...]
         [--user sources] [--out cr_scratch/lit]
         [--to-get cr_scratch/sources_to_get.md]
         [--skip cr_scratch/intake_answers.md]

Safe to rerun after a second Lit search: it adds to what is there.
1. Reads the `| K1 | claim |` and `| S01 | K ids | citation | url |` rows of
   every search file (default: each cr_scratch/lit/search*.md). The S ids in
   a search file are local to it; a url or citation already saved in OUT is
   skipped (SEEN), and a new one gets the next free S number.
2. Each url is downloaded (arXiv abs links become pdf links). PDF text comes
   from pypdf; HTML has tags stripped. Full text means: a scholarly page (a
   DOI in the url, or a journal, archive or agency host) with 2,000 words or
   more, and an HTML one also needs two section words (introduction,
   background, methods, results, discussion, conclusion); any other page
   (news, trade press, company sites) with 800 words or more. Full text is
   written to OUT/Snn.txt with Citation, URL and Claims header lines; the
   Claims line carries the K ids and claim text the source serves.
3. Each .pdf, .txt or .md file in the user folder becomes OUT/Unn.txt once,
   except files named in the skip file (the solicitation, FAQ and NRA).
4. The to-get file keeps its earlier entries, adds each source not fetched,
   and drops any entry fetched since: a heading, then one numbered full
   citation per source.
Prints one line per source (OK, SEEN or TO GET), a NEW line naming the files
written this run (the files to digest), and a final count line. Exit 0.
"""
import argparse
import glob
import html
import io
import logging
import os
import re
import sys
import urllib.parse
import urllib.request
import warnings

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows cp1252 consoles
logging.getLogger("pypdf").setLevel(logging.ERROR)  # "Multiple definitions" noise
warnings.filterwarnings("ignore")

MIN_WORDS = 2000
MIN_WORDS_OTHER = 800
MAX_BYTES = 40 * 1024 * 1024
SECTIONS = ("introduction", "background", "methods", "results", "discussion", "conclusion")
SCHOLARLY = ("doi.org", "arxiv.org", "ntrs.nasa.gov", "nature.com", "wiley.com", "springer.com",
             "sciencedirect.com", "elsevier.com", "iop.org", "aiaa.org", "mdpi.com", "frontiersin.org",
             "plos.org", "ieee.org", "agu.org", "cambridge.org", "tandfonline.com", "sagepub.com",
             "acs.org", "rsc.org", "aps.org", "copernicus.org", "ncbi.nlm.nih.gov", "osti.gov",
             "jstor.org", "science.org", "pnas.org", "aanda.org", "hou.usra.edu", "lpi.usra.edu",
             "iopscience", "researchgate.net", "semanticscholar.org", "core.ac.uk", "hal.science")
CLAIM_RE = re.compile(r"^\|\s*(K\d+)\s*\|([^|]+)\|")
ROW_RE = re.compile(r"^\|\s*(S\d+)\s*\|([^|]*)\|([^|]+)\|([^|]*)\|")
HEAD_RE = re.compile(r"^(Citation|URL|File): (.*)$", re.M)


def pdf_text(data):
    from pypdf import PdfReader
    r = PdfReader(io.BytesIO(data))
    return "\n".join((p.extract_text() or "") for p in r.pages)


def html_text(raw):
    raw = re.sub(r"(?is)<(script|style|nav|header|footer)\b.*?</\1>", " ", raw)
    return html.unescape(re.sub(r"(?s)<[^>]+>", " ", raw))


def scholarly(url):
    host = urllib.parse.urlparse(url).netloc.lower()
    return bool(re.search(r"10\.\d{4,}/", url)) or host.endswith((".edu", ".ac.uk")) or \
        any(h in host or h in url.lower() for h in SCHOLARLY)


def fetch(url):
    """Return (text, minimum words) or raise."""
    url = re.sub(r"arxiv\.org/abs/([^\s?#]+)", r"arxiv.org/pdf/\1", url)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (fetch_sources.py)"})
    with urllib.request.urlopen(req, timeout=45) as r:
        data = r.read(MAX_BYTES)
    need = MIN_WORDS if scholarly(url) else MIN_WORDS_OTHER
    if data[:5] == b"%PDF-":
        return pdf_text(data), need
    text = html_text(data.decode("utf-8", errors="replace"))
    if need == MIN_WORDS and len([w for w in SECTIONS if w in text.lower()]) < 2:
        return "", need  # an abstract or landing page, not the paper
    return text, need


def file_text(path):
    if path.lower().endswith(".pdf"):
        return pdf_text(open(path, "rb").read())
    return open(path, encoding="utf-8", errors="replace").read()


def words(t):
    return len(t.split())


def norm(s):
    return re.sub(r"\W+", " ", s or "").strip().lower()


def saved(out):
    """Headers of files already in OUT: {prefix: [numbers]}, seen urls, citations, user files."""
    nums, urls, cites, files = {"S": [0], "U": [0]}, set(), set(), set()
    for p in glob.glob(os.path.join(out, "[SU][0-9]*.txt")):
        base = os.path.basename(p)
        m = re.match(r"([SU])(\d+)\.txt$", base)
        if not m:
            continue
        nums[m.group(1)].append(int(m.group(2)))
        head = open(p, encoding="utf-8", errors="replace").read(4000)
        for k, v in HEAD_RE.findall(head):
            if k == "URL":
                urls.add(v.strip())
            elif k == "Citation":
                cites.add(norm(v))
            elif k == "File":
                files.add(os.path.basename(v.strip()))
    return nums, urls, cites, files


def read_to_get(path):
    if not os.path.exists(path):
        return []
    return [re.sub(r"^\d+\.\s*", "", ln.strip()) for ln in open(path, encoding="utf-8-sig")
            if re.match(r"^\d+\.\s", ln.strip())]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--search", action="append")
    ap.add_argument("--user", default="sources")
    ap.add_argument("--out", default="cr_scratch/lit")
    ap.add_argument("--to-get", default="cr_scratch/sources_to_get.md")
    ap.add_argument("--skip", default="cr_scratch/intake_answers.md")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    searches = a.search or sorted(glob.glob(os.path.join(a.out, "search*.md")))
    nums, urls, cites, files = saved(a.out)
    to_get = read_to_get(a.to_get)
    fetched, seen, new = 0, 0, []

    rows = []
    for path in searches:
        if not os.path.exists(path):
            continue
        claims = {}
        lines = open(path, encoding="utf-8-sig").read().splitlines()
        for ln in lines:
            m = CLAIM_RE.match(ln.strip())
            if m:
                claims[m.group(1)] = m.group(2).strip()
        for ln in lines:
            m = ROW_RE.match(ln.strip())
            if m:
                ks = re.findall(r"K\d+", m.group(2))
                served = "; ".join("%s %s" % (k, claims.get(k, "")) for k in ks).strip()
                rows.append((m.group(1), m.group(3).strip(), m.group(4).strip(), served))
    for sid, cite, url, served in rows:
        if url in urls or norm(cite) in cites:
            seen += 1
            print("SEEN %s %s" % (sid, url or cite[:60]))
            continue
        text, why, need = "", "no url", MIN_WORDS
        if url.lower().startswith("http"):
            try:
                text, need = fetch(url)
                why = "words=%d" % words(text)
            except Exception as e:  # any download or parse failure
                why = type(e).__name__
        if words(text) >= need:
            nums["S"].append(max(nums["S"]) + 1)
            nid = "S%02d" % max(nums["S"])
            with open(os.path.join(a.out, nid + ".txt"), "w", encoding="utf-8") as f:
                f.write("Citation: %s\nURL: %s\nClaims: %s\n\n%s\n" % (cite, url, served or "none", text))
            urls.add(url)
            cites.add(norm(cite))
            to_get = [c for c in to_get if norm(c) != norm(cite)]
            fetched += 1
            new.append(nid + ".txt")
            print("OK %s %s %s.txt" % (sid, why, nid))
        else:
            if norm(cite) not in [norm(c) for c in to_get]:
                to_get.append(cite)
            print("TO GET %s %s" % (sid, why))

    skip = open(a.skip, encoding="utf-8").read() if os.path.exists(a.skip) else ""
    user = 0
    if os.path.isdir(a.user):
        for name in sorted(os.listdir(a.user)):
            path = os.path.join(a.user, name)
            if not name.lower().endswith((".pdf", ".txt", ".md")) or name in skip or name in files:
                continue
            try:
                text = file_text(path)
            except Exception as e:
                print("TO GET user file %s %s" % (name, type(e).__name__))
                continue
            user += 1
            nums["U"].append(max(nums["U"]) + 1)
            uid = "U%02d" % max(nums["U"])
            with open(os.path.join(a.out, uid + ".txt"), "w", encoding="utf-8") as f:
                f.write("Citation: see file text (%s)\nFile: %s\nClaims: none\n\n%s\n" % (name, path, text))
            new.append(uid + ".txt")
            print("OK %s words=%d %s.txt (%s)" % (uid, words(text), uid, name))

    with open(a.to_get, "w", encoding="utf-8") as f:
        f.write("## SOURCES TO GET BEFORE THE NEXT REVISION\n\n")
        for i, c in enumerate(to_get, 1):
            f.write("%d. %s\n" % (i, c))
    print("NEW %s" % (" ".join(new) or "none"))
    print("FETCHED %d SEEN %d USER %d TO GET %d" % (fetched, seen, user, len(to_get)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
