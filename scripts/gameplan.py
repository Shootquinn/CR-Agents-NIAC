"""gameplan.py - keep cr_scratch/gameplan.md in one shape. The orchestrator
never edits the table by hand.

Usage:
  python scripts/gameplan.py init --title "short proposal title"
  python scripts/gameplan.py set P6 cycle=2 spawn+=1 last_spawn="Writer" last_file=cr_scratch/step6_writer_draft.md status="in progress"
  python scripts/gameplan.py current P6
  python scripts/gameplan.py ruling "F24 dropped by the author"
  python scripts/gameplan.py show

init writes rows P1 to P9 (cycle 1, spawn_count 0, status not started) if the
file is missing. set changes only the named fields of one row; spawn+=N adds,
and spawn_count never goes down. ruling appends one line under Author rulings
unless the same line is there. Every command rewrites the whole file: header,
one table, then one Author rulings section. Prints the changed row or the file.
"""
import argparse
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows cp1252 consoles

PATH = "cr_scratch/gameplan.md"
COLS = ["step", "cycle", "spawn_count", "last_spawn", "last_file_verified", "status"]
KEYS = {"cycle": "cycle", "spawn": "spawn_count", "spawn_count": "spawn_count",
        "last_spawn": "last_spawn", "last_file": "last_file_verified",
        "last_file_verified": "last_file_verified", "status": "status"}


def num(x):
    m = re.match(r"\d+", x or "")
    return int(m.group(0)) if m else 0


def load(path):
    if not os.path.exists(path):
        return None
    g = {"title": "", "intake": "cr_scratch/intake_summary.md", "current": "P1",
         "rows": {}, "rulings": []}
    in_rulings = False
    for ln in open(path, encoding="utf-8-sig").read().splitlines():
        s = ln.strip()
        if s.startswith("# Gameplan:"):
            g["title"] = s[len("# Gameplan:"):].strip()
        elif s.startswith("Intake file:"):
            g["intake"] = s.split(":", 1)[1].strip()
        elif s.startswith("Current step:"):
            g["current"] = s.split(":", 1)[1].strip()
        elif s.lower().startswith("## author rulings"):
            in_rulings = True
        elif s.startswith("## "):
            in_rulings = False
        elif re.match(r"^\|\s*P\d+\s*\|", s):
            cells = [c.strip() for c in s.strip("|").split("|")]
            cells += [""] * (len(COLS) - len(cells))
            row = dict(zip(COLS, cells[:len(COLS)]))
            prev = g["rows"].get(cells[0])
            if prev is None or num(row["spawn_count"]) >= num(prev["spawn_count"]):
                g["rows"][cells[0]] = row  # a duplicate row keeps the higher spawn_count
        elif in_rulings and s.startswith("- ") and s[2:].strip() not in g["rulings"]:
            g["rulings"].append(s[2:].strip())
    return g


def save(g, path):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    order = sorted(g["rows"], key=lambda k: int(k[1:]))
    out = ["# Gameplan: %s" % g["title"], "Intake file: %s" % g["intake"],
           "Current step: %s" % g["current"], "",
           "| " + " | ".join(COLS) + " |", "|" + "---|" * len(COLS)]
    for k in order:
        out.append("| " + " | ".join(g["rows"][k][c] for c in COLS) + " |")
    out += ["", "## Author rulings"]
    out += ["- " + r for r in g["rulings"]] or ["- none"]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


def row_line(r):
    return "| " + " | ".join(r[c] for c in COLS) + " |"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["init", "set", "current", "ruling", "show"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--title", default="NIAC Phase I Step A proposal")
    ap.add_argument("--file", default=PATH)
    a = ap.parse_args()
    g = load(a.file)
    if a.cmd == "init":
        if g is None:
            g = {"title": a.title, "intake": "cr_scratch/intake_summary.md",
                 "current": "P1", "rulings": [],
                 "rows": {"P%d" % i: dict(zip(COLS, ["P%d" % i, "1", "0", "none", "none", "not started"]))
                          for i in range(1, 10)}}
            save(g, a.file)
            print("WROTE %s" % a.file)
        else:
            print("EXISTS %s" % a.file)
        return 0
    if g is None:
        print("NO GAMEPLAN %s: run init first" % a.file)
        return 2
    if a.cmd == "show":
        print(open(a.file, encoding="utf-8").read())
        return 0
    if a.cmd == "ruling":
        text = " ".join(a.args).strip()
        g["rulings"] = [r for r in g["rulings"] if r != "none"]
        if text and text not in g["rulings"]:
            g["rulings"].append(text)
        save(g, a.file)
        print("RULINGS %d" % len(g["rulings"]))
        return 0
    if not a.args or not re.match(r"^P\d+$", a.args[0]):
        print("NEED A ROW NAME such as P6")
        return 2
    step = a.args[0]
    r = g["rows"].setdefault(step, dict(zip(COLS, [step, "1", "0", "none", "none", "not started"])))
    if a.cmd == "current":
        g["current"] = step
        save(g, a.file)
        print("CURRENT %s" % step)
        return 0
    for kv in a.args[1:]:
        m = re.match(r"^(\w+)(\+?=)(.*)$", kv)
        if not m or m.group(1) not in KEYS:
            print("BAD FIELD %s (fields: %s)" % (kv, ", ".join(sorted(KEYS))))
            return 2
        col, op, val = KEYS[m.group(1)], m.group(2), m.group(3).strip().replace("|", "/")
        if col == "spawn_count":
            old = int(r[col] or 0)
            new = old + int(val) if op == "+=" else int(val)
            if new < old:
                print("SPAWN COUNT CANNOT DECREASE (%d to %d)" % (old, new))
                return 2
            r[col] = str(new)
        else:
            r[col] = val
    save(g, a.file)
    print(row_line(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
