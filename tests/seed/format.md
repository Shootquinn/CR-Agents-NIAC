## Format and structure tests (cycle label in each row)
Run `python niac-repo/scripts/check_format.py` first and paste its printed output to the scorer. Read the key named in each SCRIPT row.

| ID | name | method | criterion (PASS when) | priority | source | cycle |
|---|---|---|---|---|---|---|
| F01 | Body page count | SCRIPT | pdf_body_pages prints PASS (body at most 3 pages). | CRITICAL | SOL p.10 | 2027 A1 |
| F02 | Margins and Letter | SCRIPT | page_size, margin_left, margin_right, margin_top and margin_bottom all print PASS. | CRITICAL | SOL p.9 | 2027 A1 |
| F03 | Density | SCRIPT | cpi prints PASS (15 or less) and lpi prints PASS (5.5 or less). | CRITICAL | SOL p.9 | 2027 A1 |
| F04 | References from page 5 | SCRIPT | pdf_references_page prints PASS. | MAJOR | SOL p.11 Figure 1 template (2027 template docx) | 2027 A1 |
| F05 | Dash count | SCRIPT | dash_count prints PASS (0) and chart_dash_count prints PASS (0). | MAJOR | author rule | 2027 A1 |
| F06 | Chart landscape one page | SCRIPT | chart_landscape and chart_margin_left, chart_margin_right, chart_margin_top, chart_margin_bottom all print PASS. | CRITICAL | SOL p.10 | 2027 A1 |
| F07 | Chart font | SCRIPT | chart_font_arial12 prints PASS. | CRITICAL | SOL p.10 | 2027 A1 |
| F08 | Chart 2x2 order | READ | The chart lists Innovation, Impact, Mission, Approach in that order, top left to bottom right. | MAJOR | SOL p.11 Figure 1 template (2027 template docx) | 2027 A1 |
| F09 | Chart words | SCRIPT | chart_word_count prints PASS (200 to 360) and chart_word_schedule, chart_word_team, chart_word_cost, chart_see_refs all print PASS. | MAJOR | author rule | 2027 A1 |
| F10 | No PI or institution on chart | READ | The chart text holds no person name and no institution name. Quote the title line. | CRITICAL | SOL p.10 | 2027 A1 |
| W3 | Wholly new count | SCRIPT | Run `grep -o -i "wholly new" draft.md` and count the lines: 1 to 3, with one in the Mission section. | MAJOR | author rule | 2027 A1 |
