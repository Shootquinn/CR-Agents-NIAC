---
name: overview_chart
description: Fill the overview chart brief from the intake summary, outline and sources digest, build the one-page chart, and fix every FAIL line.
---

# Overview chart

Replace N with the current step number. Every quantity you write comes from the intake summary, the outline or the sources digest. Invent none.

1. Copy templates/overview_chart_brief.md to cr_scratch/stepN_overview_chart_brief.md.
2. Fill fields 1 to 8 and the six keys TITLE, INNOVATION, IMPACT, MISSION, APPROACH, GRAPHIC_CAPTION. Write each key on its own line as `KEY: text`. Bullets inside a box are lines starting `- `.
3. Check the rules below against your draft. Fix each miss before you build.
4. Pick the graphic. Use one file from figures/. If figures/ holds none, build without `--image`, write "hero graphic pending" as an open item, and continue; the chart_images FAIL is that open item.
5. Run: `python scripts/build_overview_chart.py --brief cr_scratch/stepN_overview_chart_brief.md --template docs/2027_Overview_Chart_Template.docx --image figures/<file> --out proposal/overview_chart.docx`
6. Run: `python scripts/check_format.py proposal/overview_chart.docx --chart-only`
7. Read each printed PASS or FAIL line. Copy the list of FAIL lines into your report.
8. For each FAIL line, edit the brief to fix it, then repeat steps 5 and 6. Make at most 2 reruns. After the second rerun, report any remaining FAIL lines to the user.

## Rules

Page and type
1. The page is 11 in wide by 8.5 in tall, with 1-inch borders.
2. No text is under Arial 12 pt.
3. The chart is one page.

Content
4. The title has no PI name and no institution name.
5. The chart stands alone. It has no "see Section" and no "see Figure".
6. Quadrant order: Innovation top left, Impact top right, Mission bottom left, Technical Approach bottom right.
7. The title sits in a navy band. One central graphic sits at the crossing.
8. Total words across all boxes: 180 to 240. Each box holds about 60 words at Arial 12 pt; scripts/check_format.py prints chart_box_overflow when a box is full. Fit wins over count: to fix an overflow, move words to a box with room first, then shorten words, and stay at 180 or more. Count them and write the count in field 7.
9. Innovation: 3 to 5 bullets, 45 to 60 words, with 1 or 2 quantified claims.
10. Impact: 3 to 5 bullets, 40 to 55 words. Include one Earth or spin-off use.
11. Mission: 3 to 5 bullets, 45 to 60 words. Name the representative mission (place, scale, platform).
12. The first Mission line contains "wholly new" or "no mission has". See supplements/mission_context_checklist.md, lines 12 and 13.
13. Approach: 4 to 6 bullets, 45 to 60 words. Each bullet starts with a task verb (Evaluate, Assess, Optimize, Develop, Identify). A bullet with the word schedule, team, cost, month, year, staff or budget fails. Rewrite it.
14. The graphic is self-generated, public domain, or used with permission. Write the source in field 8.
15. The graphic has no text labels in the image.
