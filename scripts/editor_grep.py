"""Editor grep. Usage: python editor_grep.py FILE [--keep cr_scratch/must_keep.md]
Prints one line per hit and a final FLAGS count. Exit 1 if any flag, else 0.
Rule 9 counts "assum..." outside the one "Assumptions:" sentence; more than
2 is a flag. --keep: each `- ` line of the keep file is a feature the author
asked for, as a short phrase; a phrase not found in FILE (ignoring case)
prints `MISSING keep: <phrase>` and counts as a flag."""
import re
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows cp1252 consoles

DASH = "[—–]"
I = re.IGNORECASE
RULES = [
    (1, re.compile(DASH)),
    (2, re.compile(r"(^|[.!?]\s+)(Additionally|Moreover|Furthermore)\b")),
    (3, re.compile(r"\b(serves as|stands as|acts as)\b", I)),
    (4, re.compile(r"\b(not only|it is not just|it's not just|rather than)\b"
                   r"|\bno \w+, no \w+", I)),
    (5, re.compile(r"\b(Let me be clear|It'?s important to|In conclusion)\b", I)),
    (6, re.compile(r"^#{1,6}\s+([A-Z][a-z]+\s+){2,}[A-Z][a-z]+")),
    (7, re.compile(r"\b(delve|leverage|robust|pivotal|tapestry|landscape of)\b", I)),
    (8, re.compile(r"\b(ensured|preserved|retained|aiming to)\b", I)),
]
ASSUM = re.compile(r"\bassum\w*", I)
ASSUM_SENTENCE = re.compile(r"Assumptions:[^.]*\.")
ASSUM_CAP = 2


def main():
    args = sys.argv[1:]
    keep = None
    if "--keep" in args:
        i = args.index("--keep")
        keep = args[i + 1] if i + 1 < len(args) else None
        args = args[:i] + args[i + 2:]
    if len(args) != 1:
        print("usage: python editor_grep.py FILE [--keep cr_scratch/must_keep.md]")
        return 2
    with open(args[0], encoding="utf-8") as f:
        text = f.read()
    lines = text.splitlines()
    flags = 0
    for n, rx in RULES:
        for i, line in enumerate(lines, 1):
            c = len(rx.findall(line))
            if c:
                flags += c
                print("rule %d count %d line %d: %s" % (n, c, i, line.strip()[:60]))
    rest = [(i, ASSUM_SENTENCE.sub("", ln)) for i, ln in enumerate(lines, 1)]
    hits = [(i, ln) for i, ln in rest if ASSUM.search(ln)]
    n_assum = sum(len(ASSUM.findall(ln)) for _, ln in hits)
    print("rule 9 assum outside the Assumptions sentence: %d (cap %d)" % (n_assum, ASSUM_CAP))
    if n_assum > ASSUM_CAP:
        flags += 1
        for i, ln in hits:
            print("rule 9 line %d: %s" % (i, ln.strip()[:60]))
    if keep:
        low = text.lower()
        for ln in open(keep, encoding="utf-8-sig").read().splitlines():
            phrase = ln[2:].strip() if ln.startswith("- ") else ""
            if phrase and phrase.lower() not in low:
                flags += 1
                print("MISSING keep: %s" % phrase)
    print("FLAGS: %d" % flags)
    return 1 if flags else 0


if __name__ == "__main__":
    sys.exit(main())
