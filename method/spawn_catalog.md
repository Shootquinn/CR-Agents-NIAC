## Intake chunk extractor
Field 1 AGENT PARAMETER: model: haiku
Field 2 OUTPUT PATH: "{ROOT}/cr_scratch/intake_chunk_{N}.md"
Field 3 PERSONA: method/personas/software_engineer.md
Field 4 TASK: Extract fields and requirement rows from page range {FIRST}-{LAST} of {SOURCE_PATH}, label {SOURCE_LABEL}, per prompts/00_intake.md.
Field 5 FIXED CONTEXT: the Field 3 file
Field 6 READ LIST (base {ROOT}/): `prompts/00_intake.md` `templates/intake_summary.md` `{SOURCE_PATH}`
Field 7 CHECKLIST: 1) every row has a page cite. 2) no value comes from outside the range. 3) row count is stated.
Field 8 REQUIRED HEADINGS: ## Files read; ## Rows; ## Checklist
Field 9 MAX LINES 80, MAX WORDS 700; TRUNCATED at item n rule
Field 10 RULES: R-a to R-h pasted from the template

## Intake merge
Field 1 AGENT PARAMETER: model: haiku
Field 2 OUTPUT PATH: "{ROOT}/cr_scratch/intake_summary.md"
Field 3 PERSONA: method/personas/software_engineer.md
Field 4 TASK: Merge the chunk rows into the template headings per prompts/00_intake.md. Copy the six intake answers verbatim.
Field 5 FIXED CONTEXT: the Field 3 file
Field 6 READ LIST (base {ROOT}/): `prompts/00_intake.md` `templates/intake_summary.md` `cr_scratch/intake_chunks.md` `cr_scratch/intake_answers.md`
DATE STRING {DATE_STRING} in Field 4
Field 7 CHECKLIST: 1) one row per field in the template. 2) one row per requirement in the template. 3) every row has a page cite or NOT FOUND. 4) weights line has 4 values. 5) status line reads {OPEN_CLOSED_RULE}, computed by comparison only. 6) early-warning line is derived from answer 6 and the status. 7) answer 5 is copied exactly.
Field 8 REQUIRED HEADINGS: ## Files read; ## Fields; ## Weights line; ## Requirements; ## Status; ## Early warning; ## Verbatim answers; ## Checklist
Field 9 MAX LINES 120, MAX WORDS 1200; TRUNCATED at item n rule
Field 10 RULES: R-a to R-h pasted from the template

## Lit search
Field 1 AGENT PARAMETER: model: haiku
Field 2 OUTPUT PATH: "{ROOT}/cr_scratch/lit/search.md" (gap search: "{ROOT}/cr_scratch/lit/search_2.md")
Field 3 PERSONA: method/personas/fact_checker.md
Field 4 TASK: Find primary sources for the concept's technical claims per prompts/00c_lit_review.md. Use WebSearch and WebFetch. Gap search: search only these inputs: {GAP_INPUTS}.
Field 5 FIXED CONTEXT: the Field 3 file
Field 6 READ LIST (base {ROOT}/): `prompts/00c_lit_review.md` `cr_scratch/concept_notes.md` (when it exists; else `cr_scratch/intake_answers.md`) `cr_scratch/intake_summary.md`
Field 7 CHECKLIST: 1) claims 10 or fewer, each 20 words or fewer. 2) sources 16 or fewer; a NIAC prior-art search ran. 3) each citation value seen on an opened page or [REFERENCE NEEDED]. 4) each url is full text or none. 5) no paper summary.
Field 8 REQUIRED HEADINGS: ## Files read; ## Claims; ## Sources; ## Checklist
Field 9 MAX LINES 60, MAX WORDS 1200; TRUNCATED at item n rule
Field 10 RULES: R-a to R-h pasted from the template

## Sources digest
Field 1 AGENT PARAMETER: model: haiku
Field 2 OUTPUT PATH: "{ROOT}/cr_scratch/sources_digest_{B}.md"
Field 3 PERSONA: method/personas/fact_checker.md
Field 4 TASK: Batch {B}. One row per source per prompts/00b_sources.md. Delete unused source paths first.
Field 5 FIXED CONTEXT: the Field 3 file
Field 6 READ LIST (base {ROOT}/): `prompts/00b_sources.md` `cr_scratch/lit/{SOURCE_1}` `cr_scratch/lit/{SOURCE_2}` `cr_scratch/lit/{SOURCE_3}` `cr_scratch/lit/{SOURCE_4}`
Field 7 CHECKLIST: 1) one row per source. 2) each citation value is in its file (grep count). 3) each K id on a file's Claims line has 1 to 3 quotes. 4) each flag is Y or N. 5) absent values read [REFERENCE NEEDED].
Field 8 REQUIRED HEADINGS: ## Files read; ## Digest; ## Open items; ## Checklist
Field 9 MAX LINES 60, MAX WORDS 700; TRUNCATED at item n rule
Field 10 RULES: R-a to R-h pasted from the template

## Test suite
Field 1 AGENT PARAMETER: model: haiku
Field 2 OUTPUT PATH: "{ROOT}/cr_scratch/step{N}_software_engineer_tests.md"
Field 3 PERSONA: method/personas/software_engineer.md
Field 4 TASK: Select 60 tests, 70 at most, from the three seed groups: compliance, sizzle, format. Keep each seed ID. List cuts in the cut log.
Field 5 FIXED CONTEXT: the Field 3 file
Field 6 READ LIST (base {ROOT}/): `prompts/01_test_suite.md` `tests/seed/compliance.md` `tests/seed/sizzle.md` `tests/seed/format.md` `cr_scratch/intake_summary.md`
Field 7 CHECKLIST: 1) rows 60 to 70 (script). 2) each ID is in a seed file (grep). 3) all 11 format IDs present. 4) row form ID | group | text. 5) each cut has a reason.
Field 8 REQUIRED HEADINGS: ## Files read; ## Tests; ## Cut log; ## Checklist
Field 9 MAX LINES 110, MAX WORDS 1800; TRUNCATED at item n rule
Field 10 RULES: R-a to R-h pasted from the template

## Outline
Field 1 AGENT PARAMETER: model: haiku
Field 2 OUTPUT PATH: "{ROOT}/cr_scratch/step{N}_writer_outline.md"
Field 3 PERSONA: method/personas/writer.md
Field 4 TASK: Per section: one topic sentence testable true or false, its sources, and the compliance test ids it will pass. 3 to 7 figure slots in all.
Field 5 FIXED CONTEXT: the Field 3 file, supplements/proposal_arc.md
Field 6 READ LIST (base {ROOT}/): `prompts/02_outline.md` `cr_scratch/intake_summary.md` `cr_scratch/sources_digest.md` `cr_scratch/step3_software_engineer_tests.md` `cr_scratch/concept_notes.md` (when it exists)
Field 7 CHECKLIST: 1) one topic sentence per section. 2) each names a number or a named thing. 3) each claim cites a digest id or reads [SOURCE NEEDED]. 4) figure slots 3 to 7. 5) dash count is 0 (grep). 6) every CRITICAL and MAJOR compliance id in the suite has a slot.
Field 8 REQUIRED HEADINGS: ## Files read; ## Outline; ## Topic sentences; ## Sources; ## Figure slots; ## Checklist
Field 9 MAX LINES 70, MAX WORDS 700; TRUNCATED at item n rule
Field 10 RULES: R-a to R-h pasted from the template

## Draft
Field 1 AGENT PARAMETER: model: haiku
Field 2 OUTPUT PATH: "{ROOT}/cr_scratch/step{N}_writer_draft.md"
Field 3 PERSONA: method/personas/writer.md
Field 4 TASK: Unheaded arc, 1,300 to 1,500 words. Body font {FONT} at 12 pt (Step 3 gate). Fix pass: read {DRAFT} and `cr_scratch/step6_fix_list.md` in place of the outline; change the listed lines only and copy every other line unchanged, in order. Propose any missing mission, number or assumption yourself.
Field 5 FIXED CONTEXT: the Field 3 file, supplements/writer_style_subset.md, supplements/mission_context_checklist.md
Field 6 READ LIST (base {ROOT}/): `prompts/03_draft.md` `cr_scratch/intake_summary.md` `cr_scratch/sources_digest.md` `cr_scratch/step4_writer_outline.md` `cr_scratch/concept_notes.md` (when it exists; else the step 3 test suite file)
Field 7 CHECKLIST: 1) word count 1300 to 1500. 2) Mission Context in paragraphs 1 and 2. 3) dash count 0. 4) unsourced claims listed under Open items with line numbers; no bracket marker, file name or path in the draft. 5) budget terms: 0 (grep). 6) references in APA 7, cited by author and year. 7) inline "(assumed)" tags: 0 (grep). 8) no numbered study steps in the body.
Field 8 REQUIRED HEADINGS: ## Files read; ## Draft; ## Open items; ## Checklist
Field 9 MAX LINES 70, MAX WORDS 1800; TRUNCATED at item n rule
Field 10 RULES: R-a to R-h pasted from the template

## Edit
Field 1 AGENT PARAMETER: model: haiku
Field 2 OUTPUT PATH: "{ROOT}/cr_scratch/step{N}_editor_pass.md"
Field 3 PERSONA: method/personas/editor.md
Field 4 TASK: Apply the editor_grep.py output. Rewrite each flagged sentence as a wholly new sentence of equal or fewer words. No synonym swap. Add no words.
Field 5 FIXED CONTEXT: the Field 3 file, supplements/editor_grep_list.md
Field 6 READ LIST (base {ROOT}/): `cr_scratch/step{N}_writer_draft.md` `cr_scratch/step{N}_editor_grep.txt` `supplements/editor_grep_list.md` `supplements/writer_style_subset.md`
Field 7 CHECKLIST: 1) each grep hit is fixed or in Review flags. 2) edited word count is at most draft word count (script). 3) dash count is 0 (grep). 4) synonym swaps: 0. 5) each changed line is listed by number.
Field 8 REQUIRED HEADINGS: ## Files read; ## Grep results; ## Review flags; ## Edited draft; ## Checklist
Field 9 MAX LINES 110, MAX WORDS 2200; TRUNCATED at item n rule
Field 10 RULES: R-a to R-h pasted from the template

## Fact-Checker
Field 1 AGENT PARAMETER: model: haiku
Field 2 OUTPUT PATH: "{ROOT}/cr_scratch/step{N}_fact_checker_review.md"
Field 3 PERSONA: method/personas/fact_checker.md
Field 4 TASK: Claim table for checkable facts only: claim | source id | VERIFIED or [SOURCE NEEDED]. Vision and framing sentences get no row. Check novelty of the wholly new capability, each number against its first occurrence, and the elimination criteria.
Field 5 FIXED CONTEXT: the Field 3 file, supplements/mission_context_checklist.md
Field 6 READ LIST (base {ROOT}/): `{DRAFT}` `cr_scratch/sources_digest.md` `cr_scratch/intake_summary.md` `tests/seed/compliance.md` `cr_scratch/sources_to_get.md`
Field 7 CHECKLIST: 1) each claim row has a status. 2) each number traces to a source quote or a shown calculation. 3) references use supplied text only. 4) novelty verdict has a quote. 5) each elimination criterion has a verdict.
Field 8 REQUIRED HEADINGS: ## Files read; ## Claim table; ## Novelty; ## Solicitation compliance; ## Checklist
Field 9 MAX LINES 100, MAX WORDS 1500; TRUNCATED at item n rule
Field 10 RULES: R-a to R-h pasted from the template

## Designer figure brief
Field 1 AGENT PARAMETER: model: haiku
Field 2 OUTPUT PATH: "{ROOT}/cr_scratch/step{N}_designer_figure_brief.md"
Field 3 PERSONA: method/personas/designer.md
Field 4 TASK: One brief per figure, 3 to 7 figures: Figure ID, claim served, hand-drawn spec or Image prompt, caption with real quantities. A code-drawn plot has no Image prompt.
Field 5 FIXED CONTEXT: the Field 3 file, supplements/figure_guidance.md
Field 6 READ LIST (base {ROOT}/): `templates/figure_brief.md` `cr_scratch/step4_writer_outline.md` `cr_scratch/sources_digest.md` `cr_scratch/intake_summary.md`
Field 7 CHECKLIST: 1) figures 3 to 7. 2) each brief names its claim. 3) each Image prompt is one sentence, landscape, no text in the image. 4) each caption quantity is in the digest or intake (grep). 5) each caption starts "Figure N:".
Field 8 REQUIRED HEADINGS: ## Files read; ## Briefs; ## Checklist
Field 9 MAX LINES 60, MAX WORDS 500; TRUNCATED at item n rule
Field 10 RULES: R-a to R-h pasted from the template

## Overview chart
Field 1 AGENT PARAMETER: model: haiku
Field 2 OUTPUT PATH: "{ROOT}/cr_scratch/step{N}_overview_chart_brief.md"
Field 3 PERSONA: method/personas/designer.md
Field 4 TASK: Fill the overview chart brief by following skills/overview_chart/SKILL.md step by step. Use only quantities found in the READ LIST.
Field 5 FIXED CONTEXT: the Field 3 file, skills/overview_chart/SKILL.md
Field 6 READ LIST (base {ROOT}/): `skills/overview_chart/SKILL.md` `templates/overview_chart_brief.md` `cr_scratch/intake_summary.md` `cr_scratch/step4_writer_outline.md` `cr_scratch/sources_digest.md`
Field 7 CHECKLIST: 1) each template field is filled. 2) each quantity is in a READ LIST file (grep). 3) each skill step has a done row. 4) chart title under 12 words (script).
Field 8 REQUIRED HEADINGS: ## Files read; ## Chart brief; ## Open items; ## Checklist
Field 9 MAX LINES 50, MAX WORDS 450; TRUNCATED at item n rule
Field 10 RULES: R-a to R-h pasted from the template

## Designer review
Field 1 AGENT PARAMETER: model: haiku
Field 2 OUTPUT PATH: "{ROOT}/cr_scratch/step{N}_designer_review.md"
Field 3 PERSONA: method/personas/designer.md
Field 4 TASK: P6 review. Answer the reader questions (a) to (f) cold, list echo sites, critique the design (advisory Step B lens), check the figures. Write each FAIL as a fix list line for the Writer; a missing mission, number or assumption reads "propose X".
Field 5 FIXED CONTEXT: the Field 3 file
Field 6 READ LIST (base {ROOT}/): `{DRAFT}` `cr_scratch/step7_designer_figure_brief.md` (when it exists) `cr_scratch/intake_summary.md`
Field 7 CHECKLIST: 1) reader questions (a) to (f) all YES. 2) echo-site mismatches: 0. 3) figures 3 to 7, each cited. 4) each caption starts "Figure N:". 5) mission-context image present. 6) design critique names the weakest point and its fix (advisory).
Field 8 REQUIRED HEADINGS: ## Files read; ## Reader questions; ## Echo sites; ## Design critique; ## Figures; ## Fix list; ## Checklist
Field 9 MAX LINES 80, MAX WORDS 900; TRUNCATED at item n rule
Field 10 RULES: R-a to R-h pasted from the template

## Outline validation
Field 1 AGENT PARAMETER: model: haiku
Field 2 OUTPUT PATH: "{ROOT}/cr_scratch/step{N}_software_engineer_outline_validation.md"
Field 3 PERSONA: method/personas/software_engineer.md
Field 4 TASK: P4 check. For each topic sentence write n | PASS/FAIL | reason. PASS means the sentence is a testable claim against the suite.
Field 5 FIXED CONTEXT: the Field 3 file
Field 6 READ LIST (base {ROOT}/): `cr_scratch/step4_writer_outline.md` `cr_scratch/step3_software_engineer_tests.md` `cr_scratch/intake_summary.md`
Field 7 CHECKLIST: 1) one row per topic sentence. 2) each FAIL names heading, label or untestable claim. 3) each reason quotes 15 words or fewer. 4) no sentence graded by its author. 5) each CRITICAL and MAJOR compliance id has a slot; a missing id is a FAIL row.
Field 8 REQUIRED HEADINGS: ## Files read; ## Rows; ## Checklist; ## Open items
Field 9 MAX LINES 50, MAX WORDS 500; TRUNCATED at item n rule
Field 10 RULES: R-a to R-h pasted from the template

## Scoring batch compliance
Field 1 AGENT PARAMETER: model: haiku
Field 2 OUTPUT PATH: "{ROOT}/cr_scratch/step{N}_software_engineer_scoring_compliance.md"
Field 3 PERSONA: method/personas/software_engineer.md
Field 4 TASK: Score the compliance tests on {DRAFT}. Word and sentence counts: use the pasted count_words.py output: {COUNT_WORDS}. BATCH_SIZE {BATCH_SIZE} (seed group 25; suite lists 20 at most). Row: ID | PASS/FAIL | quote of 15 words or fewer or script value.
Field 5 FIXED CONTEXT: the Field 3 file
Field 6 READ LIST (base {ROOT}/): `tests/seed/compliance.md` `tests/seed/scoring_protocol.md` `cr_scratch/step3_software_engineer_tests.md` `{DRAFT}`
Field 7 CHECKLIST: 1) row count equals {BATCH_SIZE} (orchestrator compares). 2) mechanical tests quote the script value; none means FAIL. 3) last Scores line is TRUNCATED or the rows are complete.
Field 8 REQUIRED HEADINGS: ## Files read; ## Scores; ## Checklist
Field 9 MAX LINES 40, MAX WORDS 500; TRUNCATED at item n rule
Field 10 RULES: R-a to R-h pasted from the template

## Scoring batch sizzle
Field 1 AGENT PARAMETER: model: haiku
Field 2 OUTPUT PATH: "{ROOT}/cr_scratch/step{N}_software_engineer_scoring_sizzle.md"
Field 3 PERSONA: method/personas/software_engineer.md
Field 4 TASK: Score the sizzle tests on {DRAFT}. Word and sentence counts: use the pasted count_words.py output: {COUNT_WORDS}. BATCH_SIZE {BATCH_SIZE} (seed group 24; suite lists 20 at most). Row: ID | PASS/FAIL | quote of 15 words or fewer or script value.
Field 5 FIXED CONTEXT: the Field 3 file
Field 6 READ LIST (base {ROOT}/): `tests/seed/sizzle.md` `tests/seed/scoring_protocol.md` `cr_scratch/step3_software_engineer_tests.md` `{DRAFT}`
Field 7 CHECKLIST: 1) row count equals {BATCH_SIZE} (orchestrator compares). 2) mechanical tests quote the script value; none means FAIL. 3) last Scores line is TRUNCATED or the rows are complete.
Field 8 REQUIRED HEADINGS: ## Files read; ## Scores; ## Checklist
Field 9 MAX LINES 40, MAX WORDS 500; TRUNCATED at item n rule
Field 10 RULES: R-a to R-h pasted from the template

## Scoring batch format
Field 1 AGENT PARAMETER: model: haiku
Field 2 OUTPUT PATH: "{ROOT}/cr_scratch/step{N}_software_engineer_scoring_format.md"
Field 3 PERSONA: method/personas/software_engineer.md
Field 4 TASK: Score the format tests on {DRAFT}. BATCH_SIZE {BATCH_SIZE} (seed group 11; suite lists 20 at most). Row: ID | PASS/FAIL | quote of 15 words or fewer or script value.
Field 5 FIXED CONTEXT: the Field 3 file
Field 6 READ LIST (base {ROOT}/): `tests/seed/format.md` `tests/seed/scoring_protocol.md` `cr_scratch/step3_software_engineer_tests.md` `{DRAFT}` `cr_scratch/step8_format_check.txt`
Field 7 CHECKLIST: 1) row count equals {BATCH_SIZE} (orchestrator compares). 2) mechanical tests quote the script value; none means FAIL. 3) last Scores line is TRUNCATED or the rows are complete.
Field 8 REQUIRED HEADINGS: ## Files read; ## Scores; ## Checklist
Field 9 MAX LINES 40, MAX WORDS 500; TRUNCATED at item n rule
Field 10 RULES: R-a to R-h pasted from the template

## Manager close
Field 1 AGENT PARAMETER: model: haiku
Field 2 OUTPUT PATH: "{ROOT}/cr_scratch/step{N}_manager_close.md" "{ROOT}/cr_scratch/accumulator.md"
Field 3 PERSONA: method/personas/manager.md
Field 4 TASK: P6 close. Append one accumulator line per persona per cycle. Verdict: READY or NOT READY. Marker count: {MARKERS_LINE}. Write no submit check.
Field 5 FIXED CONTEXT: the Field 3 file
Field 6 READ LIST (base {ROOT}/): `cr_scratch/step6_fix_list.md` `cr_scratch/step6_fact_checker_review.md` `cr_scratch/step6_designer_review.md`
Field 7 CHECKLIST: 1) no submit check at P6. 2) counts are script values. 3) one accumulator line per persona per cycle. 4) Open items lists FAILs only: no to-get entry, novelty verdict or ruling.
Field 8 REQUIRED HEADINGS: ## Files read; ## Accumulator entries; ## Verdict; ## Open items; ## Checklist
Field 9 MAX LINES 80, MAX WORDS 900; TRUNCATED at item n rule
Field 10 RULES: R-a to R-h pasted from the template

## Manager close P9
Field 1 AGENT PARAMETER: model: haiku
Field 2 OUTPUT PATH: "{ROOT}/cr_scratch/step{N}_manager_close.md" "{ROOT}/cr_scratch/accumulator.md"
Field 3 PERSONA: method/personas/manager.md
Field 4 TASK: P9 close. Write the submit check from the draft and the format check. Append one accumulator line per persona. Verdict: READY or NOT READY. Marker count: {MARKERS_LINE}.
Field 5 FIXED CONTEXT: the Field 3 file
Field 6 READ LIST (base {ROOT}/): `templates/submit_checklist.md` `{DRAFT}` `cr_scratch/step8_format_check.txt` `cr_scratch/step9_systems_engineer_coherence.md`
Field 7 CHECKLIST: 1) each submit row has a yes or no with a cite (file and line). 2) counts are script values. 3) one accumulator line per persona. 4) Open items lists FAILs only: no to-get entry, novelty verdict or ruling.
Field 8 REQUIRED HEADINGS: ## Files read; ## Submit check; ## Accumulator entries; ## Verdict; ## Open items; ## Checklist
Field 9 MAX LINES 80, MAX WORDS 900; TRUNCATED at item n rule
Field 10 RULES: R-a to R-h pasted from the template

## Systems Engineer one-shot
Field 1 AGENT PARAMETER: model: haiku
Field 2 OUTPUT PATH: "{ROOT}/cr_scratch/step{N}_systems_engineer_coherence.md"
Field 3 PERSONA: method/personas/systems_engineer.md
Field 4 TASK: P9 final coherence review. Check coherence across chart brief, outline, draft and gameplan row; list gaps.
Field 5 FIXED CONTEXT: the Field 3 file
Field 6 READ LIST (base {ROOT}/): `{DRAFT}` `cr_scratch/step7_overview_chart_brief.md` `cr_scratch/intake_summary.md` `cr_scratch/step4_writer_outline.md` `cr_scratch/gameplan.md`
Field 7 CHECKLIST: 1) four criteria each have an answering section. 2) repeated figures match the first (grep). 3) each topic sentence is in the draft. 4) each gap has a quote and line number. 5) spawn_count and cycles are within caps.
Field 8 REQUIRED HEADINGS: ## Files read; ## Coherence; ## Checklist
Field 9 MAX LINES 60, MAX WORDS 700; TRUNCATED at item n rule
Field 10 RULES: R-a to R-h pasted from the template

## Recovery planning
Field 1 AGENT PARAMETER: model: haiku
Field 2 OUTPUT PATH: "{ROOT}/cr_scratch/recovery_{PERSONA}.md"
Field 3 PERSONA: method/personas/{PERSONA}.md (manager, software_engineer, fact_checker, designer, systems_engineer, writer)
Field 4 TASK: The step closed NOT READY. Plan the fix from your role, per templates/recovery_plan.md: blocker, cause, proposed action, owner. Fact-Checker: source gaps as a list of Lit search inputs. Writer: line edits or a restructure.
Field 5 FIXED CONTEXT: the Field 3 file
Field 6 READ LIST (base {ROOT}/): `templates/recovery_plan.md` `cr_scratch/step{N}_manager_close.md` `cr_scratch/step6_fix_list.md` `{DRAFT}` `{ROLE_FILE}` (the persona's latest review or score file)
Field 7 CHECKLIST: 1) at most 10 lines under ## Plan. 2) each line names blocker, cause, action and owner. 3) owner is a roster persona or the orchestrator.
Field 8 REQUIRED HEADINGS: ## Files read; ## Plan; ## Checklist
Field 9 MAX LINES 25, MAX WORDS 300; TRUNCATED at item n rule
Field 10 RULES: R-a to R-h pasted from the template
