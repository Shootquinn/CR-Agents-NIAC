# Recovery plan: [step]

Each planning spawn writes at most 10 lines under ## Plan, one per blocker:
`blocker | cause (system or one-off) | proposed action | owner`

The orchestrator merges the six planning files into cr_scratch/recovery_plan.md:

## Actions
1. [action] | [owner] | [blocker it clears]

## Executive decisions
- [decision] (logged with `python scripts/gameplan.py ruling "..."`)

## Budget
Fresh 3-cycle budget for this step. One recovery round per step; a second NOT READY goes to the user as an abstract plus AskUserQuestion with the plan's real options.
