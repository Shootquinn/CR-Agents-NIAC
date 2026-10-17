# Test-Driven Documentation (TDD)

Treat the proposal like a software project: define acceptance tests first, then build content that passes them. A 3-page document with explicit tests gives the writer a specification instead of a guess.

## The Process (3 Prompts)

Each prompt can run in a separate chat. Attach the output of each step to the next.

### Prompt 1: Test Suite

```
I need to write a [DOCUMENT TYPE] about [TOPIC].

Requirements:
- [Audience]
- [Purpose]
- [Constraints: length, format, deadline]
- [Key questions it must answer]
- [Source materials available]

Create a test suite this document must pass. Organize tests by scope:
WHOLE-DOCUMENT TESTS: apply to the complete document, validated once
against the finished draft.
SECTION-LEVEL TESTS: apply to one section, validated while drafting it.

For each test, specify what is tested, the pass/fail criteria, and the
evidence required.
```

### Prompt 2: Outline

```
Generate a paragraph-level outline which, if followed correctly, yields a
document that passes every test in the attached test suite. Represent each
paragraph by its topic sentence, the claim that paragraph will make.

[Attach: test suite from Prompt 1]
```

### Prompt 3: Draft

```
Write the document from the attached outline. Develop each topic sentence
into a complete paragraph.

[Attach: outline from Prompt 2]
[Attach: reference materials]
```

## Key Principles

1. **Tests before content.** Always.
2. **Organize by location, tag by severity.** When drafting Section 3, the writer needs Section 3's tests, not a list sorted by importance.
3. **Topic sentences, not headings.** "This proposal shows X is feasible because Y" says what to write. "Introduction" does not.
4. **Trace everything.** Every test maps to content. Every claim maps to evidence. Orphans mark gaps.
5. **Validate at outline stage.** A missing section costs minutes in an outline and hours in a draft.
7. **Verify test sources against primary materials.** A test that cites a source (solicitation, FAQ, paper) is checked against that source before the suite becomes the contract. LLMs fabricate plausible citations. The agent writing the test carries the verification.
8. **Every claim of fact gets a test linked to a primary source.** Numbers, measurements, thresholds, and cited results need a test naming the source that confirms them. A claim with no test and no source is flagged. Analytical conclusions and design rationale are the author's territory.

## Test Count

9. Target 60 tests, cap 70, in three groups: compliance, sizzle, format.

## Revision Pass (Optional Prompt 4)

After the draft passes its suite, one editing pass can remove decorative prose without changing technical content. Targets: filler transitions ("Additionally," "Furthermore"), dangling participles ("ensuring," "highlighting"), puffery, elegant variation, superficial analysis. Constraints: subtract or replace, never add; every replacement is shorter than the original; technical terms and numbers stay; rerun the suite afterward.

```
Revise the attached document for prose quality. Only subtract or replace
words, each replacement shorter than the original. Remove decorative
adjectives, dangling participle phrases, puffery, elegant variation,
superficial analysis, and empty transitions. Keep all technical terms,
quantitative claims, and specific facts.

[Attach: document that passed all tests]
[Attach: test suite, for re-validation]
```
