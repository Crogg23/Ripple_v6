# RIPPLE STATUS — 2026-08-20 (still later) — one counts page: Chris's palette, evidence-based fonts, every table's columns

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE: nothing new this session.** Carried, both untouched: (1) the roll-call
vote mart still disagrees with its Python-built twin — standing since 2026-08-18.
(2) Twelve Python test modules fail to COLLECT on this machine for a missing
charting library, hiding ~1,400 tests. The column-classifier substring-match
cosmetic bug (misreads columns like "facility" as name/id columns) is also still
there, still not fixed, still doesn't affect any number's correctness.

**Also worth knowing, found but not acted on:** the count-question generator caps
how many columns of each type it turns into questions per table — 6 ids/names, 6
categories, 3 places, 3 flags, 2 money, 2 quantity, no matter how many actually
exist. 320 of 647 tables lose at least one already-classified column to that cap
(5,222 columns total; worst table drops 325). Chris didn't ask for that fixed —
he asked for a plain column reference instead (below) — but the cap is real and
still there if he wants it raised later.

**Then a color-scheme pass, optimized for ADHD — took three tries, landed on
Chris's own exact palette.** Chris asked to reoptimize the page's colors for
his brain. Round 1: sketched three real palette directions side by side,
Chris picked "warm/muted earthy" — shipped it, Chris called it worse, too
washed out, asked for earth tones with real contrast, and said stop
overthinking it — function over nuance. Round 2: rebuilt with deep/saturated
earth tones plus obvious bordered-card sections for the toolbar and each
opened dataset. Round 3: Chris handed over an exact 5-color hex palette
(`#264653 #2a9d8f #e9c46a #f4a261 #e76f51` — dark teal, teal, gold, orange,
red-orange) and said figure out the rest myself, no more back-and-forth.
Mapped it functionally: the dark teal is the page's ink/text color and the
dark-mode card surface; teal is the one chrome/interactive accent; gold,
orange, and red-orange are the three tiers respectively (plain counts /
cross & share / real joins) — four clearly distinct hues, all five of
Chris's colors used, nothing invented. Caught and fixed one real contrast
bug this round would otherwise have shipped: three of Chris's colors are
medium-light, so the page's old assumption (always use light "ground" text
on top of a filled/active chip) would have been nearly illegible on gold and
orange fills — fixed by giving light and dark fills their own correct text
color instead of one blanket rule. Every round verified in headless
Chromium, light and dark, same interaction checks throughout, all still
pass, zero console errors. **Chris hasn't confirmed this third pass yet.**

**Then a font overhaul, researched first.** Chris asked for the best fonts
for his brain specifically and to actually research it, not guess. Real
finding, web-verified this session, not recalled from memory: the page's
headings and dataset names were set in a serif typeface (Newsreader), and
general accessibility guidance is fairly consistent that serifs add visual
complexity that hurts ADHD readers more than it helps — sans-serif is the
safer default throughout, headings included. Swapped the whole page (body
text, headings, dataset names, questions) from Newsreader+IBM Plex Sans to
**Lexend** — a font built specifically on reading-speed research (Shaver-Troup
/ Vanderbilt study, ~2,700 students; Lexend's own published numbers claim
~20% faster reading vs. Times New Roman for struggling readers, though that
stat is the font project's own number, not independently re-verified here).
Runner-up considered and set aside: Atkinson Hyperlegible, which optimizes
for telling similar letters apart rather than reading speed — more of a
dyslexia/low-vision fit than an ADHD one specifically. Also removed the
tightened letter-spacing the serif headings used to have (negative tracking
reads worse for ADHD; wider spacing reads better) and opened up line-height
on the actual paragraph text — lede, dataset descriptions, the trust-notes
list — from ~1.45 to 1.6, inside the commonly-cited 1.5–2.0 range. Left the
monospace font (IBM Plex Mono, for SQL/labels/column names) untouched —
nothing in the research flagged monospace code text as an ADHD pain point.
Verified in headless Chromium, light and dark, same interaction checks as
every round before it — all pass, zero console errors.

---

## THIS SESSION — a pure UI session: merged layer 1 + layer 2 into one page

Chris's ask: figure out the optimal UI/usability for the two counts pages — not
a polish pass, a real "is this even the right shape" pass.

- **Used both live pages hands-on first**, in a real headless browser, before
  proposing anything. Confirmed by clicking, not just reading code: the kind
  filters (per year, flags, repeat rate, etc.) were invisible until you were
  already inside one of 647 datasets or mid-search — no way to browse "every
  flagged-percent question in the warehouse" from a cold landing. Also found
  the two pages are close to line-for-line the same interface published twice,
  with only a one-way link between them.
- **Brought Chris 3 real sketch-level options**, not one polished build:
  merge into one page with filters visible on landing; keep two pages plus add
  a small hub page between them; or a bigger swing — a command-palette /
  search-first workbench. Chris picked **option 1: one page, tiered.**
- **Built it.** New script `scripts/census/build_count_page_unified.py` reads
  the same three untouched source files (`count_possibilities.json`,
  `count_possibilities_layer2.json`, `layer2_joins.json` if it exists) and
  renders one page — it does not touch the question-generation or
  classification logic in any of the three scripts that produce those files,
  only how the output is shown. **23,381 questions, one dataset list of 647,
  one URL.** A tier row (plain counts / cross & share / real join, each with
  a live count) and the kind row both sit on the landing page now, always
  visible — pick a tier or kind straight from the landing view and it browses
  that alone across every dataset, no search term or dataset click required
  first. Same design system as both prior pages on purpose (Newsreader /
  IBM Plex Sans / IBM Plex Mono, slate-teal palette) — this replaces them,
  it isn't a new product.
- **Caught and fixed two real bugs before shipping**, both found by actually
  clicking through it, not by reading the code: (1) resetting the tier filter
  back to "everything" didn't clear an active kind filter, so it got stuck
  showing a filtered list instead of returning to the dataset index; (2) the
  small tier-color dot next to each question-type heading inside a dataset
  had no CSS rule wired to it and was rendering invisible.
- **Verified for real** in headless Chromium after the fixes: light theme,
  dark theme, mobile width, tier-click-from-landing, kind-click auto-syncing
  the tier highlight, dataset drill-down, search, copy-to-clipboard, and the
  empty-state message for "real joins" (correctly explains they're queued,
  not run — doesn't say "try a plainer word" like a real search miss would).
  Zero console errors throughout.
- **Then Chris asked for something different mid-session**: every column of
  a table available to reference, plain name plus a jargon-free definition,
  nothing fancy. First read of that ask was wrong — went looking at the
  question-generator's column cap instead (see above) before Chris corrected
  it. What actually shipped: opening any of the 647 datasets now has a
  collapsed "All N columns in this table" section — every column's real name
  next to a one-line plain-English definition, reusing the exact classifier
  and glossary already trusted for the questions (no new logic, no new
  curation). One table ran as high as 473 columns; the list scrolls inside a
  capped box instead of stretching the page. Adds well under 1MB to the page
  (10.2MB → 10.9MB) since it's one reference per table, not repeated per
  question. Verified in headless Chromium on the widest table (473 columns):
  collapsed by default, expands clean, no console errors.

**Live link:** https://claude.ai/code/artifact/937c6d0e-3c0b-4442-bc39-a8edb391f068
This supersedes the two prior links in practice — Chris should use this one
going forward. Neither old link was deleted or touched; they still work if
Chris wants them:
- layer 1 (old): https://claude.ai/code/artifact/f0308e10-6a7c-4049-97fd-075df7737106
- layer 2 (old): https://claude.ai/code/artifact/fe571d24-0f99-49f7-b870-8ee20b10251a

## Still open, unrelated to this session's work

- **The trend list has a known, unrepaired defect Chris was told about and
  has not ruled on.** 67 of 403 charts waste more than half their x-axis on
  under 1% of their rows. Not touched this session — waiting on Chris's call.
- Warehouse lane (canonical clock, 771-measurement time census) is exactly
  where the last warehouse session left it — nothing here changed it.
- **The 206 real joins are still priced, not run.** Nothing about this
  session's UI work changes that decision — still waiting on Chris to say go
  (`python scripts/census/run_layer2_joins.py --sample 15` or `--run`). The
  new unified page already knows how to pick up `reports/layer2_joins.json`
  the moment it exists, same as the old layer 2 page did — no rebuild-time
  change needed once Chris says go, just re-run the unified build script.

## Carried from the 2026-08-20 warehouse session, untouched since

**435-model canonical clock is live** (403 of 647 tables get a shared timeline;
244 documented as "here's what kind of nothing this one has"). Full detail: ask,
or check commit `80e63d79` / `ccd1d01f`.

**Open items carried unchanged:** roll-call mart mismatch; 12 Python test
collection errors (missing charting lib); 20 tables with only a download-stamp
clock; clock LABEL correctness untested; 30 tables with no per-entity rate; 13
tables with clocks in the wrong order; opioid data covers 2006–2012 not
2006–2026; nobody has read the connection map (4,899 links); 182 columns with
literal 'nan' text; FAERS 76% dup; ~900 gated portal tables; roll-call mart
rebuild; source-registry reconciliation; six unparseable polygon tables; the
column-classifier substring-match bug noted above.

**YOUR MOVE:** look at the new unified page and confirm the merge is the shape
you want to keep using day to day. If yes, the two old links can just be
ignored (or ask for them to be formally retired later — not done this
session, nothing destructive happened). Separately, standing: whenever you
want the 206 real joins run, say go. Also open, not decided: whether the
5,222-column question-generator cap (above) is worth raising — flagged, not
acted on, since it wasn't what was asked for.

**NEXT SESSION:** nothing queued specifically by this session. Whenever real
joins run, rebuild the unified page (`python
scripts/census/build_count_page_unified.py`) and it picks the real numbers up
automatically, same hookup the old layer 2 page had. Everything else carried
above is still just waiting on a Chris pick — the trend-list axis defect, the
classifier bug, the column-cap question above, the two warehouse-lane options
from the prior evening session, the Webflow crash course queued 2026-08-19.

**Tests:** nothing run this session outside the new census page-builder
script and its Playwright verification (local, free, in a scratch dir — no
warehouse, no repo test suite touched). Last dbt run: 435 timeline models
green, guard passes. Last full Python run: 1,671 passed, 2 skipped, 1 failed
(known roll-call mismatch), 12 collection errors (unchanged).

**COST this session:** $0 warehouse, $0 external spend throughout, including
the column-reference add-on and the color pass (all local — one
`_all_columns.csv` read, no new warehouse query, no paid tools). One new
script (`build_count_page_unified.py`), one one-off local column-cap
analysis (read-only, no files changed), one throwaway color-comparison
artifact plus three publishes total to the counts page's artifact link, six
real headless-browser verification passes across the session, light and dark
theme screenshotted repeatedly.
