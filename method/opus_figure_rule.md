# Opus figure rule

Haiku limitation: Haiku cannot reliably read figure values (bar heights, points against an axis, small print in a chart image). The default is OFF. Any figure value the product cannot read is marked NOT-READ, and the claim that depends on it is marked [FIGURE UNVERIFIED]. This file and the prompts in `supplements/source_summaries/` (user-side chat tools, never spawned by the run) are the only product files allowed to name a model other than haiku.

## Triggers

Ask the user only when all six hold. Check T1 to T6 in order. The first failing code stops the check and goes in the log.

- T1. The step is a literature-review step (prior-art step, or any spawn that lists cited papers).
- T2. The cited figure is an image file (chart, plot, diagram, or table rendered as an image). Typed tables in the paper text fail T2.
- T3. The Fact-Checker's Claim table has a figure-check row for this figure with `Trigger: YES`.
- T4. `cr_scratch/opus_log.md` has no row for this figure ID.
- T5. Session setting is OFF and fewer than 4 Opus spawns have run this run.
- T6. A claim in the outline or draft depends on this figure.

Figure-check row, written in the Claim table by the Haiku Fact-Checker per figure: Figure ID `{CITEKEY}-F{n}`; Figure file; Claim ID; Needed values; one line per value, READ or NOT-READ; grep of the paper text per value, FOUND or NOT-FOUND; `Trigger: YES` if any value is NOT-READ or NOT-FOUND, else `Trigger: NO`.
A value is NOT-READ if: R1 it is not printed as text and must be estimated from position, and the claim states two or more significant figures; R2 digits, unit, or axis or legend label are unreadable; R3 the Read tool cannot open the file.

## Authorization prompt

Show verbatim as the only chat text, brackets filled. Ask once. 75 words.

```
Figure check: [FIG_ID] in [CITATION] has values Haiku cannot read reliably: [VALUE LIST]. Claim [CLAIM_ID] depends on them. An Opus agent would read only this figure and report the values. Why: Opus is the stronger reader for dense charts. Cost: higher than this run's Haiku agents, one Opus call. Reply: 1 = yes, this figure only (recommended). 2 = yes, all figures this session (up to 4). 3 = no, mark this claim [FIGURE UNVERIFIED].
```

| Reply | Effect |
|---|---|
| 1 | One Opus spawn for this figure. The next figure asks again. |
| 2 | Sets `Session setting: SESSION`. Later figures spawn without asking (answer AUTO), up to 4 Opus spawns. |
| 3 | No spawn. Setting stays OFF. The next figure asks again. |
| 3 plus "never" | Sets `Session setting: NEVER`. No more asks; later figures fall back with reason NEVER. |

## Spawn rule

Before the Agent call all hold: log answer is 1, 2, or AUTO; fewer than 4 Opus spawns used; no earlier spawn for this figure ID; the figure file exists.

Agent parameters: `description` = `Opus figure read {FIG_ID}`; `subagent_type` = `general-purpose`; `model` = `opus`; `prompt` = the text below.

```
You are a figure reader for the NIAC proposal run. Read one figure and report its values. Nothing else.
Read only: 1. {FIG_PATH} (PDF page {PAGE}) 2. {CITE_PATH}, only the passage that cites {FIG_ID}.
Claim to check: {CLAIM_TEXT}
Needed values: {VALUE_LIST}
Do not read the draft, gameplan, progress log, or any other file. Do not use the web.
Per value, one row: value as printed, unit, axis or legend label, READ or NOT-READ with reason. Then one verdict: SUPPORTED, NOT SUPPORTED, or UNCLEAR.
Write to {OUT_PATH} with headings in order, nothing before the first: ## Figure {FIG_ID}, ## Values, ## Claim verdict, ## Legibility notes. Maximum 400 words.
Chat reply, one line: VERDICT: <SUPPORTED | NOT SUPPORTED | UNCLEAR> | FILE: {OUT_PATH}
```

Output path: `cr_scratch/step{N}_opus_figure_{FIG_ID}.md`. After return, check the file exists and its first line is `## Figure {FIG_ID}`, and the reply has a VERDICT line. A miss logs fallback reason FAILED. No retry.

Caps: the product caps are 3 cycles and 14 spawns per step. Opus spawns are outside that count and capped at 4 per run. One Opus spawn per figure, run one at a time. Opus is never used in the review wave or on the proposal's own figures.

A claim is VERIFIED only if the Opus verdict is SUPPORTED and every needed value is READ. Otherwise its claim-table status is [FIGURE UNVERIFIED].

## Log

File `cr_scratch/opus_log.md`, created at run start from `templates/opus_log.md`. Line 1 is `Session setting: OFF`. Write a row for every ask, answer, spawn, and result. Never delete a row. On answer 2 or NEVER, update line 1.

The gate file `step{N}_manager_gate.md` gets `## Unverified figures`: one line per row with a fallback reason (figure ID, citation, claim ID, reason), or `None.`

## Fallback

Applies to answers 3, NO ANSWER, NEVER, CAP, FAILED. It also applies when the user declines or does not answer: the setting stays OFF.

1. No Opus spawn for this figure.
2. The Fact-Checker sets the claim status to `[FIGURE UNVERIFIED]` in her claim table. The draft carries no marker.
3. The claim stays in the draft. The step continues.
4. The log row gets the fallback reason.
5. The claim is listed at the gate.

NO ANSWER: if the next user message has no 1, 2, 3, or "never", log NO ANSWER and proceed. Do not re-ask in the step. CAP: 4 spawns used; do not ask. NEVER: do not ask. A fallback never blocks a step.
