# Calibration rubric, v1, frozen 2026-09-25

The question: when the warehouse flags something, has the press already found it?
A known-answer test. Point the instrument at stories other people already broke, and see if it reads true.

These rules were written and committed **before any press search**.
Any change after the pilot gets logged at the bottom, with the reason, and every pilot story is judged again under the final rules.

## What gets tested

- `stories.tsv`: 209 stories, folded from the 239 leads in the 2026-09-24 coverage pass through their "Same story as" links.
- Each story keeps its frozen headline, number, grade and novelty guess. The press search never changes any of them.
- **Novelty guess** came from the menus, scored before this test: 1 = famous story, 5 = nobody has it. 36 stories have none; they're mostly C/D leads below the menu cut.
- **pre_known** marks stories that aren't blind:
  - `press_checked_2026-09-24`: the top-3 brief already searched the press for S001 Sands, S002 Reliant and S007 hospice farms.
  - `lead_cites_press`: the lead's own text already points at coverage. Six stories.
  - Both get scored, but they're reported apart from the blind ones.

## The honest limit

- Claude wrote the leads, and Claude has read the news up to its training cutoff, June 2026.
- So a match with coverage **from before July 2026** shows the data agrees with the press. It doesn't prove the data found the story on its own.
- A match with coverage **published after 2026-06-30** is the truly blind part. It gets its own count.

## Who does what

| Role | Sees | Does |
|---|---|---|
| Searcher | the frozen lead | runs the searches, logs every query, returns candidate sources with exact quotes; **never assigns a bin** |
| Quote check | the URL and the quote | a script fetches the page and checks the quote is on it |
| Judge | the frozen lead + quotes, dates, outlets | assigns the bin; never sees the searcher's opinion |
| Skeptic | everything | re-checks every Matched, Matched + more and Contradicted call; re-searches 20 random Unreported stories |

Memory never counts. A source is evidence only with a live URL and a quote copied from the page.

## The six bins

A story's **entity** is the named thing in the lead: a company, facility, person, agency, or for a national number, the place + measure + period ("Arizona overdose deaths, 12 months to Oct 2025").

| Bin | Rule |
|---|---|
| **Matched** | a source names the same entity and reports the same finding, in the same direction |
| **Matched + more** | Matched, and our lead carries a specific number or link that no source found has |
| **Known pattern** | sources cover the same pattern or scheme, but not this entity |
| **Contradicted** | a source covers the same entity, same measure and an overlapping window, and disagrees on direction, or its number is off from ours by more than 25% |
| **Not comparable** | same entity, but a different window or definition, so the numbers can't be lined up |
| **Unreported** | five or more logged searches, and nothing reaches Known pattern |

Tie-breaks:
- Topic alone is never a match. "Nursing homes are understaffed" doesn't match Reliant Care.
- The entity must be in the source. A source about the scheme that doesn't name the entity is Known pattern.
- A source reporting the same finding without our number is still Matched. The number decides Matched vs Matched + more.
- When sources disagree with each other, the judge uses the strongest one: same entity, closest window, primary record over news.
- **Unreported means "not found in the logged searches."** It never means "nobody covered it."

## What each source records

| Field | Rule |
|---|---|
| url | the page itself, not a search result page |
| outlet | who published it |
| date | publication date, YYYY-MM-DD; "unknown" if the page has none |
| source_type | news · trade press · government (audit, OIG, GAO, agency release, enforcement) · court · testimony · research (academic, NGO, think tank) · company |
| quote | at most 40 words, copied exactly from the page, stating the fact that links to the lead |
| entity_named | yes / no: does the page name our entity |

The **earliest matching date** is the oldest source that reaches Matched. Coverage dated after 2026-06-30 gets the post-cutoff flag.

## Searches

- At least five queries per story before calling it Unreported. Every query gets logged, even the ones that found nothing.
- Mix them: entity + finding, entity + agency, the number, the local outlet, the agency's own enforcement pages.
- Private people: search a name only when the lead names them. Never publish anything.

## Scoring

- **Hit rate** = (Matched + Matched + more) / stories judged. Shown two ways: news sources only, and every source type.
- **Value added** = Matched + more as a share of all matches.
- **Blind hits** = matches whose earliest source is dated after 2026-06-30, from stories not pre_known.
- **Novelty test:** novelty guess vs bin. If "1 = famous" stories come back Unreported, or "5 = nobody" stories come back Matched, the guess was wrong, and that gets reported.
- **Miss audit:** the skeptic re-searches 20 random Unreported stories with fresh wording. Its catch rate is the error bar on Unreported.
- Everything is reported by grade. A C/D story matching the press is interesting. A Contradicted one is a data trap, or a bad story.

## Pilot

- 20 stories: two positive controls whose coverage we know exists, S001 Sands and S007 hospice farms, plus 18 drawn at random with a fixed seed, spread across novelty guesses. See `pilot.tsv`.
- The rules may change after the pilot. Every change is logged below with its reason.

## Change log

- v1, 2026-09-25: first version, frozen before any search.
