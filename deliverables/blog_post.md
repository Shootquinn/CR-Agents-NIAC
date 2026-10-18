# Three pages, one screen, no grants office

## Action

You have an idea. Maybe it came from a class, a garage, or a long shower. You think NASA might care, and you have heard of a program that funds strange, early ideas. You open the instructions and find a limit: 3 pages for the whole technical case. Before anyone reads those pages for quality, a screen decides whether they get read at all.

So you do what everyone does. You paste your notes into an AI tool and ask for a proposal. Back comes smooth, generic text that could describe any idea ever had. It sounds fine and says nothing. A reviewer will see that in one paragraph.

The problem is that nobody told the AI what passing looks like, so it guessed.

This repo fixes that order of operations. It is a small team of Haiku agents run by a Sonnet orchestrator. You hand it a raw idea. It hands back an overview chart, a 3-page body and references, each checked against tests that were written before a single sentence of the draft existed. You do not need a grants office.

The repo is CR-Agents-NIAC (https://github.com/Shootquinn/CR-Agents-NIAC). It descends from a parent method called CR-Agents (https://github.com/Shootquinn/CR-Agents), which handles general writing and research. This one is tuned for one job: a first-timer's Step A proposal to NASA's NIAC program.

If you have never written a federal proposal, good. Neither had anyone, the first time.

## Background

Step A is small on purpose. It has four parts: a cover page you fill in on NSPIRES, one overview chart in wide format, a 3-page Technical and Management section, and optional references. Budget and staffing stay out of it. NASA wants to know whether your idea is worth a closer look.

First comes a screen. The 2027 solicitation lists three elimination criteria. Fail any of them and the proposal is out of scope and never invited to Step B.

1. Relevance to NASA's mission. Does the idea improve space or aeronautics for the country?
2. Technical credibility. Does it avoid conflict with established physics or engineering, or defend itself when it must?
3. Programmatic credibility. Is there a reasonable path to implementation, with the barriers named?

Survivors get scored on four weighted criteria: Innovation, Impact, Mission and Technical Approach, weighted 30, 30, 20 and 20 percent. Each is scored from 1 to 5.

Here is the limitation, once, so nobody feels tricked later. Passing the screen does not ensure selection. This method gives you a compliant, readable draft. The idea still has to win on its own merits, and no tool can write a better idea than the one you bring.

The method makes the weighted criteria visible from the first minute. Every test it writes traces back to the screen or to one of the four scores. Your three pages stop being a pile of enthusiasm and start being an argument aimed at the exact things a reviewer will check. The method cannot pick your idea for you. It can make sure your idea gets heard clearly.

## Development

The method runs in order. Each step finishes before the next one starts.

**Intake.** The orchestrator asks six questions. Haiku agents read the solicitation, the FAQ and any amendments in page chunks, so no single agent has to hold a whole document. The intake summary marks the cycle OPEN or CLOSED, computed from the release and due dates.

**Orientation.** If you have no concept yet, the repo offers an orientation to help you find one worth testing.

**Test suite.** This comes before any prose. The repo builds 60 tests from a seed library: 25 compliance, 24 sizzle and 11 format. Each test is rated CRITICAL, MAJOR or MINOR, so you know what to fix first.

**Outline.** One topic sentence per paragraph, each checked against the tests before any paragraph exists.

**Draft.** Written against the outline, one paragraph at a time. A sentence that fails a test goes back for a fix, and the draft does not move forward until it passes. This is slower than pasting notes into a chat box on day one.

**Review and scoring.** Scoring agents run the tests in three batches, one per group, and a rubric scores the four weighted criteria. Each result comes with a quoted line from your draft, so a FAIL tells you what to change.

**Figures.** The overview chart and other figures come next. Where code cannot draw the art, the caption gets an Image prompt line underneath, so you can make the picture yourself.

**Build.** A script produces the docx and the PDF, then runs a format check on both.

The "wholly new" rule has two sentences. The Mission section opens by naming the wholly new capability your idea would enable. That phrase appears one to three times in the body, so reviewers cannot miss the claim and cannot find it diluted.

Then there is AI use. If NSPIRES asks, the repo gives you one plain sentence to enter: AI tools were used in the drafting and copy-editing of this proposal.

Why is it lighter than its parent? The CR-Agents guide is 28,321 tokens. The NIAC session start is held under 8,000 tokens, which is lighter per the baseline table. Smaller sessions suit small models. Opus figure analysis is off by default, so you pay for it only when you ask.

**Build-time dry run.** Before publishing the repo, I ran it end to end with Haiku as the orchestrator and a script playing the user, on the Jupiter concept from my own earlier proposal. The second run went from intake to an assembled PDF in 8 user turns, about 43 minutes and $1.16 of model time. The page layout passed every format check. The draft did not pass review: the last review cycle ended on real faults, including a dive schedule that did not add up in my own notes, and the final check called it NOT READY. That is the method doing its job. The two runs found eleven gaps in the repo itself: six were fixed between the runs and five after the second. A later run on the current repo, with Sonnet as the orchestrator and the same Haiku agents, went from intake to an assembled PDF in 2 user turns, about 37 minutes and $3.63. The scripted user told it to skip the web literature search, and it also ended NOT READY, with three figures still to draw.

## Climax: a worked run

[AUTHOR RUN PENDING]

## Ending

What you do next depends on one word in your intake summary.

If the solicitation is OPEN, the deadline sits in the intake summary. Read it first. Then check the contact rules, because they change at release. Before release, you may send a 2-page summary to the NIAC office and ask whether your idea has been explored and whether it fits. After release, questions go only to the published FAQ. The office stops discussing individual ideas once the window opens, and that window is easy to miss.

If it is CLOSED, you have time, which is the best thing a first-timer can own. Use it. Build the mission context: which representative mission carries your idea, and what that mission needs. Build the test suite for the next cycle while the FAQ and the solicitation are still fresh. Run the draft early, fail it often and fix it cheaply. A draft that fails in a quiet month costs you an evening. The same failure under a deadline costs you the cycle.

Either way, one rule holds. Take every date from NSPIRES and the intake summary, never from a blog post, this one included.

Expect to rewrite. Expect the first draft to be a junk draft, and let it be one. The tests will tell you where it breaks.

You do not need a grants office. You need an idea, three pages, and a checklist that does not get tired. Go find out whether your idea survives the screen.
