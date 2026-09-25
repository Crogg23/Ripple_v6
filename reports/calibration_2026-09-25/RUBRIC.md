# Calibration rubric, v3, 2026-09-25 (v1 frozen before any search)

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
| source_type | news · trade press · opinion · government (audit, OIG, GAO, agency release, enforcement) · court · testimony · research (academic, NGO, think tank) · company |
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
- v2, 2026-09-25, after the pilot's first judging:
  - **Fetch path.** The quote checker now tries python, then curl, then the Internet Archive's copy of the same URL. A quote found in the archived copy counts as verified.
    - Why: v1 threw out JAMA, SEC and a law-firm page that sit behind bot walls, not paywalls. That flipped control S007 to Known pattern: its only San Antonio quote was on a blocked page. The archive recovered 5 of 8 blocked quotes.
  - **Second judge.** Every pilot story is judged again by a fresh judge under v2, into `judge_v2/`. Where the evidence didn't change, agreement between the two judges is reported as the judge's reliability.
  - **Search budget.** The session allows 200 web searches in total, shared by every agent; the pilot used all 200 on 19 stories, 10.5 each. The full run targets 8 queries a story: at least 5, at most 10. S174 wasn't searched and moves to the full run.
  - No bin rule changed.
- v3, 2026-09-25, after the pilot skeptic. The skeptic found the judges split on 5 of 16 stories where the evidence held still, all at rule edges. Every change below makes a line sharper; none was chosen to move a count.
  - **The entity is the headline's subject**: who or what did the thing. When a lead names several things, a drug and its makers, sources about the others are Known pattern. For a national number, the entity is place + measure; the period is the window.
  - **"More" means something countable**: a number, a named entity or a comparison in our headline or number line that no usable source states. "At every big lender," with no count and no names, isn't more.
  - **Claims one by one.** If a usable same-entity source contradicts any claim in the lead, the bin is Contradicted, even when another claim matches. This rule was only in JUDGE.md; now it's the rubric's.
  - **Matched vs Not comparable.** A source that names the entity and states the same finding in words is Matched, even with no number. Not comparable is only for a source with a number for the entity that differs from ours because its window or definition differs.
  - **Known pattern needs a finding** about other entities or in general. An explainer on a rule, program or deadline isn't a pattern; with nothing else, that's Unreported.
  - **Copies count once.** A rewrite of another outlet's story, a wire copy, or the same URL twice is one source. An op-ed is `opinion`, never news.
  - **Judges see page context**: about 300 characters either side of each quote, from the saved page.
  - **Quote check** splits letters from digits, so "PM2.5" and "PM 2.5" match. Before, it dropped S092's only disagreeing source.
  - **Four rates, always**: any source, news only, blind (not pre_known, not a control), and post-cutoff. "News only" means a deciding source is news or trade press; opinion, government, court, research and company sources don't count toward it.
  - **Novelty test** uses the headline lead's guess, not the lowest guess across folded leads. S103 was scored 1 from a folded lead; its own guess is 2.
  - **Two judges per story in the full run**; a third settles any disagreement.
  - On the record: the v2 fetch change came after control S007 failed. The archive copy is a real fetch of the same URL, but the fix was made after seeing the miss, and S007 counts only through a law-firm blog; The Texan's article on the same testimony was never found.
