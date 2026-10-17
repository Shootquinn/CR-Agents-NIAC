## Scoring protocol
1. Score in 3 batches, one scorer agent per group file: compliance.md, sizzle.md, format.md.
2. Scorer input: the group file, the draft text, and the printed output of `check_format.py`.
3. Scorer output: one row per test, in file order, in the form `| ID | PASS/FAIL | quote |`, with no header row.
4. The quote is copied from the draft and is 15 words or fewer (<= 15 words). For a SCRIPT test the third cell is the printed script value. A FAIL for absence writes `absent`.
5. Row count check (the row count rule): the orchestrator runs `grep -c "^| [CSFW][0-9]"` on the scorer output. The count must equal the test count of the group (compliance 25, sizzle 24, format 11).
6. A short file is TRUNCATED. Write `TRUNCATED` on the last line, then respawn the scorer once for the missing IDs only.
7. Scorers never add, average or compute scores. The orchestrator computes the weighted score by running the one-line python command written in score_rubric.md.
8. Pass rule: every CRITICAL test passes, and MAJOR tests pass at 90 percent or more. MINOR and ADVISORY results are advisory.
9. Scorer output path: `cr_scratch/score_<group>_c<cycle>.md`, where group is compliance, sizzle or format.
10. The orchestrator fills scoring_report_template.md from the three scorer files and the python output.
