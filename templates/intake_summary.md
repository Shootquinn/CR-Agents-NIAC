## Files read
Each READ LIST path with its first 8 words quoted.

## Fields
| id | field | value | page cite |
| --- | --- | --- | --- |
| F01 | solicitation number | | |
| F02 | release date | | |
| F03 | latest amendment date | | |
| F04 | Step A due date and time | | |
| F05 | award cap | | |
| F06 | anticipated number of awards | | |
| F07 | period of performance | | |
| F08 | overview chart page limit and orientation | | |
| F09 | Technical and Management page limit | | |
| F10 | references rule | | |
| F11 | characters per inch limit | | |
| F12 | lines per vertical inch limit | | |
| F13 | margins | | |
| F14 | paper size | | |
| F15 | elimination criterion 1 | | |
| F16 | elimination criterion 2 | | |
| F17 | elimination criterion 3 | | |
| F18 | weight Innovation | | |
| F19 | weight Impact | | |
| F20 | weight Mission | | |
| F21 | weight Technical Approach | | |
| F22 | invite threshold score | | |
| F24 | blackout rule | | |
| F25 | submission system | | |

## Weights line
Four values in the order Innovation, Impact, Mission, Technical Approach, separated by slashes.

## Requirements
| id | requirement | found | page cite |
| --- | --- | --- | --- |
| R-c01 | Overview chart has Title, Innovation, Impact, Mission, Approach boxes and a central graphic | | |
| R-c02 | Technical and Management Section addresses the Step A criteria in the page limit | | |
| R-c03 | Four areas addressed: innovation, impact, representative mission, technical approach | | |
| R-c04 | Top-level list of Phase I objectives | | |
| R-c05 | Back-of-the-envelope calculation justifying feasibility of the innovation | | |
| R-c06 | Back-of-the-envelope calculation justifying impact in an exemplar mission | | |
| R-c07 | At least one plausible development path, substantiated by a back-of-the-envelope calculation | | |
| R-c08 | Single representative mission with architecture, science objectives, operations, system-level design, applicability | | |
| R-c09 | Mission size, weight and power estimate (beneficial, not mandatory) | | |
| R-c10 | Rudimentary comparison with alternatives and state of the art | | |
| R-c11 | Entry TRL 2 or lower (TRL 3+ elements not disqualifying) | | |
| R-c12 | Mission-context assumptions stated explicitly | | |
| R-c13 | Significant challenges not deferred to later phases | | |
| R-c14 | No Phase II content and no Phase II resource request | | |
| R-c15 | Proposal stands alone: no reference to other proposals, no reliance on web links | | |
| R-c16 | Body self-sufficient without the cover page | | |
| R-c18 | References optional, standard format | | |
| R-c19 | Step A body and cover page carry no budget and no proposed team | | |
| R-c20 | Work-plan outline showing understanding of major issues and course of study | | |
| R-c21 | Export-control section for foreign participation (Step A applicability not stated) | | |
| R-c22 | Data Management Plan (Step A requirement unclear; in NSPIRES cover data) | | |

## Status
Status: OPEN or CLOSED
Rule: OPEN if the DATE STRING is earlier than or equal to the F04 date, CLOSED if later; compare year, then month, then day.

## Early warning
Warning line: SAM.gov UEI registration can take weeks. The Step A deadline is {F04}. Start registration now.
Write the warning line only if answer 6 is "no" and status is OPEN. Otherwise write "none".

## Verbatim answers
1. Current solicitation file path.
2. Amendment file paths, or "none".
3. FAQ file path, or "none".
4. One-paragraph concept.
5. Model name shown by the /model command.
6. Does the proposer have a UEI in SAM.gov, yes or no.

## Checklist
1. 25 field rows.
2. 22 requirement rows.
3. Every row has a page cite or NOT FOUND.
4. Weights line has 4 values.
5. Status line is OPEN or CLOSED.
6. Early-warning line is derived from answer 6 and the status.
7. Answer 5 is copied exactly.
