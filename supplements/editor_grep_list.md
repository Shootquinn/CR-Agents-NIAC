# Editor grep list

Run `python scripts/editor_grep.py FILE` on every draft. Each hit is a flag. Fix by rewriting the sentence.

1. Em or en dash: `[—–]` => replace with a period, comma, or colon.
2. Sentence-start transitions: `(^|[.!?]\s+)(Additionally|Moreover|Furthermore)\b` => delete the word or restructure.
3. Copula avoidance: `\b(serves as|stands as|acts as)\b` => use "is".
4. Negative parallelism: `\b(not only|it is not just|it's not just|rather than)\b|\bno \w+, no \w+` (ignore case) => state the positive claim directly.
5. Banned openers and phrases: `\b(Let me be clear|It'?s important to|In conclusion)\b` (ignore case) => cut.
6. Title-case headings in the body: `^#{1,6}\s+([A-Z][a-z]+\s+){2,}[A-Z][a-z]+` => use sentence case.
7. Stock words: `\b(delve|leverage|robust|pivotal|tapestry|landscape of)\b` (ignore case) => use a plain word. The word "landscape" alone is allowed (chart orientation).
8. Procedural self-report: `\b(ensured|preserved|retained|aiming to)\b` (ignore case) => describe the result, not the process.
