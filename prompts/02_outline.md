## Prompt 2: generate your outline
Read cr_scratch/intake_summary.md, cr_scratch/sources_digest.md and the test suite file. [CHANGED: product input files replace chat context]
The NASA solicitation governs over any advice. [CHANGED: product rule, solicitation has final authority]
Generate a paragraph-level outline which, if followed correctly, will result in a document that passes all of the tests in the TDD test plan.

Each paragraph in the outline should be represented by its topic sentence, the claim that the paragraph will make. It's often easier to just write the sentence than to expend effort crafting a terse bullet point that you'll later have to re-expand anyway.

Examples of topic sentences:
1. [Opening hook]: "Imagine a spacecraft that could reach Alpha Centauri in a human lifetime. this mission architecture makes that possible using technology we could begin developing today."
2. [Problem statement]: "Current propulsion systems limit interstellar missions to multi-generational timescales, making them effectively impossible to plan, fund, or execute."
3. [Solution introduction]: "Directed energy propulsion using ground-based laser arrays could accelerate lightweight probes to 20% the speed of light, reducing transit time to decades instead of millennia." [CHANGED: removes a banned phrase]

If your topic sentences pass all your tests, your proposal will pass when you expand them into paragraphs. If they don't pass, fix them now. Add more sources in at this step if you have them.
Use real sources, correct DOIs, and no invented references. [CHANGED: adds the exact phrase real sources, correct DOIs]
A red flag here is if all AI sources are from PubMed (huge sign of laziness).
Each topic sentence names a number or a named thing. [CHANGED: makes each sentence testable]
Cite each claim with an id from cr_scratch/sources_digest.md. [CHANGED: sources come from the digest file]
A claim with no digest id reads [SOURCE NEEDED]. [CHANGED: unsourced claim rule]
Add 3 to 7 figure slots in all. [CHANGED: figure count rule]
The Mission topic sentence names the wholly new capability that no existing or previously explored mission has. [CHANGED: author rule for the Mission section]
Write the outline to cr_scratch/step{N}_writer_outline.md. [CHANGED: output is a file in cr_scratch named by the catalog]
