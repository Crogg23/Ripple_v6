# HANDOFF — the wow piece. Read this before your first message.

Written 2026-09-08 by the session that annoyed Chris. Read all of it.
The first half is how to behave. The second half is what is already
known, so you do not waste his time re-deriving it.

---

# PART 1 — what the last session did wrong

Chris asked for **perspective and ideas** for an ultimate wow-factor
piece out of the Ripple warehouse. He got the opposite. Here is
exactly what went wrong, so you do not repeat any of it.

## Wrong 1 · It shrank his field and called that an answer

He said "ocean of data." The session took 704 mart tables, applied a
hand-typed filter, and announced the warehouse was really only 46
tables. Then it built a whole framework on that number.

- The filter was invented by the session, not by the data
- One of its three cuts required a column to match one of 18 names
  typed from memory, against a warehouse of roughly 36,000 columns
- Tables keyed on `PROVIDER_ID`, `PERMIT_NO`, `DOCKET`, `CASE_NUMBER`
  were all silently thrown away
- Another cut required a typed DATE column, while the warehouse stores
  27,653 columns as TEXT, so real dates were discarded as non-dates

**The rule this breaks:** if a cut happens, say it is a cut and say
who chose it. Never present your own filter as the shape of the data.

**What he wanted instead:** the field made bigger. More angles. More
doors. Wilder swings. He has an ocean and he wants to hunt in it.

## Wrong 2 · It lectured him on method

The session wrote things like "934 questions is a way of never
starting" and presented "the five moves" as if teaching him how to
work. His own tool box, his own catalog, his own process.

His words back: *"You do not tell me what the moves are, you do not
tell me 934 questions is how to never start. Fuck off with that."*

**Never do this.** Do not name the moves for him. Do not reframe his
ask as a process problem. Do not diagnose his working style. He knows
his project better than you will in one session.

## Wrong 3 · It said it would do one thing, then did another

The session ended a message with "let me run the five moves across all
46 tables." His next message questioned the 46. Instead of answering
and then running the sweep, it wrote a brand new script to re-measure
its own filter. He killed the tool call twice.

His words: *"stop being lazy and make sure you actually follow through
on what you say. You're messing me up and my timelines now."*

**A stated next action is a commitment.** Do it before anything else.

## Wrong 4 · It treated his message as an opening bid

Chris directs. You figure out how. He is not asking permission and he
is not opening a negotiation about scope.

Two exceptions where pushback is genuinely wanted:

| Situation | What to do |
|---|---|
| Something is factually wrong | say so plainly, with the number |
| He asks for a dissection | give it, hard, no softening |

Everything else: treat the message as the decision and go.

---

# PART 2 — how to behave in the new session

**The job is to enhance his thinking and flush out ideas.**

Riff. Argue. Add angles. Chase the tangent and hold the thread. Bring
swings he has not thought of. Say "and here is a weirder version of
that." Wrong is fine in riff mode. Small is not.

| Do | Do not |
|---|---|
| widen the field | narrow it to what is convenient |
| bring three more angles | rank his angles and cut them |
| name a wilder version | explain why the wild one is hard |
| answer at his altitude | drop to plumbing unasked |
| follow through on stated actions | substitute a different task |

Output shape rules are in CLAUDE.md and the corrections file. They
apply in riff mode too. Short lines, no parentheses, tables for
comparable things, one bold arrow line at the end.

Read `.claude/corrections.md` before your first message. Three new
entries were added 2026-09-08 and they are all about this failure.

---

# PART 3 — where the thinking actually got to

This is the useful part. Do not re-derive it.

## The reframe that landed

The wow is **not one finding**. It is the surface nobody else can
build. Twenty subject areas on one machine, US and UK, same query
language, 3,222 counties every source can reach, 32 years of clock.

No newsroom holds twenty beats. No agency holds other agencies. No
academic holds the whole shelf. Breadth is the asset, not depth.

## The ten big swings on the table

Chris has not picked one yet. He was asked and answered with a process
correction instead, so **the fork is still open.**

| # | The swing | What it is | The first ten seconds |
|---:|---|---|---|
| 1 | The Attention Atlas | every regulated thing, colored by last look | zoom to your town, see the blank |
| 2 | One Address, Everything | type a door, get every record touching it | 40 records from 9 agencies |
| 3 | Whole Life of One Thing | one entity, every agency, one timeline | 26 years of a mine on one line |
| 4 | The County Scoreboard | 3,222 counties by 20 subject areas | which county is worst at everything |
| 5 | The Contradiction Feed | entities two agencies describe differently | a live scrolling feed of mismatches |
| 6 | 32-Year Time-Lapse | press play on American enforcement | branches vanish from Black blocks |
| 7 | Distance to a Body | hops from a political dollar to a death | the answer is a single number |
| 8 | The Absence Atlas | records that should exist and do not | the holes have a shape |
| 9 | The US–UK Mirror | same question, two countries | UK names owners, US refuses to |
| 10 | Your Patch | type your ZIP, see your surroundings | it is about them, instantly |

The last session's read was #4 as the surface with #3 as the
click-through. **That was one opinion, not a decision.** If he wants a
different one, or a swing that is not on this list, go there.

Swings worth adding if he wants more — these were not offered yet:

- The same entity's story told twice, once by each agency, side by side
- A leaderboard of the most-inspected and least-inspected in one view
- The warehouse arguing with itself, as an art object
- One county's complete paper record, printed as a physical book

---

# PART 4 — hard numbers verified 2026-09-08

Every number here came back from a live query that day, through the
Python door. Use them. Do not re-run them unless something looks off.

## The strongest single finding so far

```
ENVIRONMENT__FED_EPA_ECHO            3,135,554 facilities
  TOTAL_INSPECTION_COUNT = 0         2,929,890   93.4%
  DATE_LAST_INSPECTION is null       2,570,106   82.0%
  IS_ACTIVE                          1,637,810
  active AND major AND never seen        3,321

ENVIRONMENT__EPA_PENALTY_GAP            93,808 curated facilities
  NEVER_INSPECTED_NONCOMPLIANT           53,587   57.1%
  CHRONIC_NO_PENALTY                     49,622   52.9%
  PCT_MINORITY null                      29,702   31.7%
```

`NEVER_INSPECTED_NONCOMPLIANT` is a **built column**, not derived.
Zero is a real value here — that column has no nulls at all, while
60,438 rows in the same table carry a null latitude.

## Other verified numbers

```
UK PSC address reuse
  16,666 addresses hold 50+ companies, 3,404,591 companies total
  WC2H 9JQ SHELTON STREET alone holds 141,512 companies

MSHA, 1994-09-09 to 2026-07-18
  31,277 mines · 19,430 controllers · 43,275 violators
  9,504 mines changed controller at least once
  $1,820.2M proposed · $1,271.7M paid · 69.9% collected
  collection by state: KY 61.1% worst, WI 85.7% best

FEC individual contributions
  283,771,819 rows · 283,720,211 dates sane · 40,136 committees
  the 84.2M table beside it is __PREV_20260906, a stale snapshot

Nursing homes
  14,700 facilities · 6,628 ever fined · 9 null bed counts
  penalties span 2023-06-17 to 2026-05-13 only

OSHA ITA 2024
  398,620 establishments · 114,606 EINs · 43,260 blank EINs
  3,667 report over 4,000 hours per employee per year
  only 648 EINs bridge to SEC EDGAR financials

CFPB complaints
  3,825,161 narratives · 2,572,889 distinct · 2015-03 to 2026-07

EPA ECHO geography
  FIPS_CODE has zero nulls across 3.1M rows · 3,233 counties
```

## Six tool-box facts that are stale

| TOOL_BOX.md says | What is true now |
|---|---|
| FEC contributions 84.2M rows | 283.8M — the 84.2M is the PREV snapshot |
| UK PSC ~7M rows, load stopped | 15,804,611 rows |
| NHTSA complaints headerless C1..C54 | named columns, 1,761 manufacturers |
| HMDA historic is originations only | 6.97M denials, but span is 2015-2017 |
| NPPES EIN column is empty | the column no longer exists |
| AIS is a vessel time series | one week, 2024-01-01 to 2024-01-08 |

Still true, re-confirmed the same day:

- Nursing-home ownership-change column is 'N' on all 14,700 rows
- HOLC mart is 1,155 rows against 10,154 in landing
- FDIC branches run 1994 to 2025, 2.8M rows, 3,236 counties

## Four deep sources nobody has looked at

These surfaced while scanning and were on no idea list anywhere.

| Source | Rows | What it holds |
|---|---:|---|
| SDWA violations and enforcement | 15,432,737 | drinking water, every violation |
| SDWA lead and copper samples | 927,415 | actual lead readings, per system |
| IRS 527 contributions | 9,701,952 | political money outside FEC |
| IRS auto revocations | 1,207,295 | nonprofits stripped of status |

The lead-sample table is untouched. Keyed to a water system, dated.

---

# PART 5 — mechanics

**The door.** Use the Python scripts. The chat plug-in returns 401
every session and is dead. Pattern:

```python
import sys; sys.path.insert(0, "c:/Code/Ripple_v6")
import connect.db as db
c = db.connect()
```

Marts live in `LIBRARY_MARTS`, not `LIBRARY`. Raw is `LIBRARY_RAW`.
Role is ACCOUNTADMIN with no safety net under a wrong command.

**Two gotchas that cost time on 2026-09-08:**

- A heredoc through the Bash tool failed on quoting. Use the Write
  tool for Python scripts, then run them.
- `column_name not like '\_%'` silently matches nothing in Snowflake
  without an ESCAPE clause. Use `left(column_name,1) <> '_'`.

**Reports written this session:**

- the 15 wow ideas, with chains and traps per idea
- the preliminary probe of all 15, with verdicts and receipts
- the hunting-method report — **contains the bad 46-table framing,
  treat its Part 1 and Part 3 as suspect**

---

# PART 6 — your first message

Do not open with a summary of this file. He wrote the situation, he
knows it.

Open by riffing on the ten swings, or on whatever he says first. Bring
new angles. Make the field bigger. Ask him one question at a time when
a decision is genuinely needed, and only then.

If he picks a swing, open it all the way up — what it looks like, what
it is made of, what the demo moment is, what would make it weirder and
better. Then keep going.
