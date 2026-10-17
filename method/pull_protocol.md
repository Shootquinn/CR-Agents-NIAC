# Pull protocol

1. Big-brother repos. Original: https://github.com/Shootquinn/CR-Agents (general method and docx bundle). Legal: https://github.com/Shootquinn/CR-Agents-Legal (beta, contract work).
2. This product pulls no file from the legal repo at ship time. Every derived file comes from the original at commit 1fcc1a7efe3df180ac85aad5d802a84ad683d633.
3. Who pulls: only a maintainer. The product orchestrator never pulls during a proposal run.
4. How to pull one file:
   1. `git clone <repo URL>` into a folder outside the product folder.
   2. `git -C <clone> checkout <hash>`
   3. Copy the one file by path into the product folder.
   4. Add one row to PROVENANCE.md: path, source repo, source path, commit hash, date from the `date` command, kind (derived or verbatim).
5. Never copy `.git`, any `.pptx`, or `docs/technical_note.md`.
6. Recheck the legal repo only on the author's word. It is beta.
7. Candidate pulls:

| File | Repo | Why | Status |
|---|---|---|---|
| tdd_method.md (principles 9-10) | legal | provision-to-source tests, scripted checks | not pulled |
| guide A.10 items 8-9 | legal | scripted checks, seeded faults | not pulled |
| guide A.3.1.1 gate | legal | one-line self-check for stale decisions | not pulled |
| templates/gameplan.md | legal | Ground Truth, Error Log, Echo Site Registry, UNKNOWN and UNVERIFIED labels | not pulled |
| guide A.14 echo-site rule | legal | script-first consistency | not pulled |
| templates/persona_tunings.md | original | tuning instead of recruiting | not pulled |
| prompt0.md | original | identical in both repos | not pulled |
| CLAUDE.md anti-verbosity block | original | rephrase before reuse | not pulled |
| claude-docx-bundle SKILL and docx_style | original | unchanged between repos | not pulled |

8. Avoid: either repo's whole `operational_guide.md`, `contract-drafting.md`, the CAD supplements, `technical_note.md`, and the Trimble and Schimel writing guides.
