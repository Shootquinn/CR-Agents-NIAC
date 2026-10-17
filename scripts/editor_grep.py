"""Editor grep. Usage: python editor_grep.py FILE
Prints one line per hit and a final FLAGS count. Exit 1 if any flag, else 0."""
import re
import sys

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


def main():
    if len(sys.argv) != 2:
        print("usage: python editor_grep.py FILE")
        return 2
    with open(sys.argv[1], encoding="utf-8") as f:
        lines = f.read().splitlines()
    flags = 0
    for n, rx in RULES:
        for i, line in enumerate(lines, 1):
            c = len(rx.findall(line))
            if c:
                flags += c
                print("rule %d count %d line %d: %s" % (n, c, i, line.strip()[:60]))
    print("FLAGS: %d" % flags)
    return 1 if flags else 0


if __name__ == "__main__":
    sys.exit(main())
