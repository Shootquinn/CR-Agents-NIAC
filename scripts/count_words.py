"""count_words.py - word and sentence counts for the scoring batches.

Usage: python scripts/count_words.py DRAFT.md

Reads the ## Draft (or ## Edited draft) section up to the References line.
Caption lines (Figure N:) and Image prompt lines are not body words.
Prints one line per paragraph: `P<n> words <w> first_sentence <s> longest_sentence <l> label <run-in label or ->`,
then `CAPTIONS words <w>`, `BODY words <w>` and `SENTENCES over 30 words <n>`. Exit 0.
"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows cp1252 consoles

FIG_RE = re.compile(r"^Figure\s+\d+\s*:")
PROMPT_RE = re.compile(r"^Image prompt\s*:", re.I)
REF_RE = re.compile(r"^(?:#+\s*)?(?:\*\*)?References(?:\*\*)?\s*$", re.I)
LABEL_RE = re.compile(r"^\*\*([^*]+)\*\*|^([A-Z][\w ]{0,30}):\s")


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"(])", text.strip()) if s]


def main():
    if len(sys.argv) != 2:
        print("usage: python scripts/count_words.py DRAFT.md")
        return 2
    paras, cur, caps, on = [], [], 0, False
    for ln in open(sys.argv[1], encoding="utf-8-sig").read().splitlines():
        if ln.startswith("## "):
            if on:
                break
            on = ln.strip().lower() in ("## draft", "## edited draft")
            continue
        if not on:
            continue
        s = ln.strip()
        if REF_RE.match(s):
            break
        if FIG_RE.match(s):
            caps += len(s.split())
            continue
        if PROMPT_RE.match(s) or s.startswith("#"):
            continue
        if not s:
            if cur:
                paras.append(" ".join(cur))
                cur = []
            continue
        cur.append(s)
    if cur:
        paras.append(" ".join(cur))
    body = over = 0
    for i, p in enumerate(paras, 1):
        ss = sentences(p)
        lens = [len(x.split()) for x in ss] or [0]
        m = LABEL_RE.match(p)
        label = (m.group(1) or m.group(2)).strip() if m else "-"
        body += len(p.split())
        over += sum(1 for n in lens if n > 30)
        print("P%d words %d first_sentence %d longest_sentence %d label %s" % (
            i, len(p.split()), lens[0], max(lens), label))
    print("CAPTIONS words %d" % caps)
    print("BODY words %d" % body)
    print("SENTENCES over 30 words %d" % over)
    return 0


if __name__ == "__main__":
    sys.exit(main())
