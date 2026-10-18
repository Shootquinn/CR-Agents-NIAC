# NIAC Phase I Step A proposal repo

This is not a NASA site. This is not a NASA product. It has nothing to do with NASA at all. NASA did not write these words, review them, or bless them. Everything here is merely advisory in nature, which is lawyer for "take it or leave it, friend." The current NASA solicitation in NSPIRES governs. Read it, follow it, and ignore us wherever it disagrees.

## What this repo does

It helps you write one thing: the 3-page NIAC Phase I Step A proposal. The output is three parts: an overview chart, a 3-page body, and references, saved in `proposal/`. Before a work order your idea is a bar-napkin sketch; the work order is its first step to a preliminary idea, and the Step A and then Step B proposals are its initial TRL 1 definition. So the proposal claims entry TRL 1 and leans on the heritage technologies it builds on for credibility. It does not write Step B. It does not write your idea for you. Bring a concept, or ask for orientation and it will help you find one.

## Quick start

1. Clone this repo.
2. Open Claude Code in the folder.
3. Claude reads CLAUDE.md on its own. Do not paste anything.
4. Answer the six intake questions.
5. No concept yet? Say so. Orientation is offered.

## How it runs

This is designed to run in Claude Code in a terminal, using spawned light-weight Haiku agents so it can work with the $20 Claude plan. Run the orchestrator (your main session) on Sonnet: type `/model sonnet` before you start. A Haiku orchestrator works too, but needs more steering.

It runs its own literature review. Agents search for primary sources, download the full text where it is open, and summarize only what they read in full. Any paper they could not get goes, with a full citation, on a SOURCES TO GET BEFORE THE NEXT REVISION list at the end of your References page. Delete that list before you upload.

Haiku cannot read figure details reliably. Bar heights, plotted points and small print in chart images are marked NOT-READ, and any claim that leans on them is flagged in the Fact-Checker's review. Opus figure analysis is default off and runs only when you authorize it, per method/opus_figure_rule.md.

## Requirements

1. Python 3.
2. `pip install -r scripts/requirements.txt`
3. LibreOffice, for PDF output.

A file called prompt0 is included to help orient Claude with what you have installed and check to make sure it can access everything, and teach it skills. It is targeted towards Windows but you can work with it to adjust the prompt0 file if you are on a different system. 

## Sample work order

`Example Workorder.txt` in the root is a sample work order. Look at it to see what a finished request looks like. The workorder doesn't need to be anything more than a summary of your idea, but it should indicate how you feel about challenges. If you've thought about competing approaches, it would be good to write that down in here too. 

## What is in docs/

1. Example proposals.
2. The 2027 solicitation in markdown, labeled 2027 A1 (Revision A1).
3. The parent SpaceTech REDDI 2026 NRA in markdown. The solicitation is an appendix to it.
4. The 2027 A1 FAQ in markdown.
5. The overview chart template.

## Folder map

1. `CLAUDE.md`: the orchestrator's entry point and wake-up/post-compaction instructions.
2. `method/`: the guide, personas, spawn files, tests method, pull protocol.
3. `prompts/`: intake, sources, orientation and the three method prompts.
4. `scripts/`: format and tool checks, the editor grep, the chart and docx builders, PDF assembly.
5. `skills/`: the overview chart skill.
6. `supplements/`: the proposal arc, NIAC advice, mission checklist, figure guidance, style subset and grep list.
7. `templates/`: the intake summary, briefs, logs, accumulator and the proposal template docx.
8. `tests/seed/`: the 60 seed tests, scoring protocol and rubric.
9. `docs/`: the 2027 solicitation, FAQ and parent NRA in markdown, the chart template, three example proposals.
10. `sources/`: drop your solicitation, FAQ and source papers here.
11. `cr_scratch/`: working notes and logs, created during a run.
12. `PROVENANCE.md`: where each derived file came from.
13. `prompt0.md`: first-session tool checks and Windows setup.
14. `proposal/`: the files you submit (chart, body docx, PDF), created during a run.

## Big brothers

1. Original: https://github.com/Shootquinn/CR-Agents (general Engineering method and docx bundle). This can be used for 3D modeling, engineering design, pretty much everything. This NIAC variant is a lighter-weight more focused version of this main thread.
2. Legal: https://github.com/Shootquinn/CR-Agents-Legal (contract work). The legal variant is beta.
