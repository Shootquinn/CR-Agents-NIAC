## Prompt 1: build the test suite
Read cr_scratch/intake_summary.md and cr_scratch/orientation_sketch.md if it exists. The concept is verbatim answer 4 in the intake summary. [CHANGED: the product reads files instead of pasted text]
The NASA solicitation governs over any advice. [CHANGED: product rule, solicitation has final authority]
I need to write a NIAC Phase I Step A proposal (3 pages maximum). Before writing any copy, I need a comprehensive test suite which defines what "winning" looks like. A winning proposal would pass all of the tests.

ATTACHMENTS:
- cr_scratch/intake_summary.md and the three seed files tests/seed/compliance.md, tests/seed/sizzle.md and tests/seed/format.md. [CHANGED: attachments become intake summary and seed files]

SPLIT: compliance=25 sizzle=24 format=11 total=60 [CHANGED: fixed split replaces the blog's 80-100 tests]
Select 60 tests, target 60, cap 70. Pick them from the three seed groups and keep every seed ID. [CHANGED: tests come from the seed library]
Output the cuts in a cut log with a reason for each. [CHANGED: product keeps a cut log]
Scoring runs in 3 batches, one per group: compliance, sizzle and format. [CHANGED: scoring batches follow the three groups]
Name the four weighted criteria in this order: Innovation, Impact, Mission, Technical Approach, with the weights from rows F18 to F21 of cr_scratch/intake_summary.md and the invite threshold from row F22 of that file. Each criterion needs tests in the compliance group. [CHANGED: ties the tests to the solicitation criteria]
The Mission section needs a test that one sentence names the wholly new capability that no existing or previously explored mission has, and a test that "wholly new" appears 1 to 3 times. [CHANGED: author rule for the Mission section]
The text contains no em dash and no en dash. [CHANGED: format rule]

FOR EACH TEST, SPECIFY:
- Test ID and name
- Pass/fail criteria (be specific)
- Priority: CRITICAL (must pass all) / MAJOR (must pass 90%+) / MINOR
Priority meaning: CRITICAL must pass all, MAJOR must pass 90 percent, MINOR is advisory. [CHANGED: states each priority meaning as a rule]
Write each test as one row: ID | group | text | priority. [CHANGED: fixed row form for small models]

IMPORTANT FRAMING:

NIAC proposals must be 1/3 sci-fi (visionary, exciting), 1/3 technical (credible, physics check out), and 1/3 gamesmanship (stands out from 250+ competitors). The test suite must include tests for ALL THREE categories, not just compliance.

The proposal must pass all 9 elimination criteria (Thou-Shall-Nots) but that's table stakes. The sizzle tests ("would I want to keep reading?" and "does this stick in my memory after 30 proposals?") are what separate INVITED from DECLINED.

Write the suite to cr_scratch/step{N}_software_engineer_tests.md. [CHANGED: output is a file in cr_scratch named by the catalog]
