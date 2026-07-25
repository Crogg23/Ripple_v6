# Plan: Vsauce-Style Terrain Map

## The Problem

The terrain map currently reads like a database monitoring dashboard. Jargon-heavy sidebar cards ("CORROBORATED | NAME@ZIP | 7,760 shared entities") tell you nothing about *why* these connections matter or what they reveal about the real world.

Additionally, only 100 of 242 tables (25% of the data) are currently connected — the biggest tables are locked out by a safety threshold.

## What "Vsauce Style" Means Here

- Lead with the surprising human insight, not the technical mechanism
- Make the reader go "wait, really?" before explaining how
- Be honest about what we DON'T know (the gaps)
- Every connection should answer "so what?" — what could you DO with this?

## Changes

### 1. Rewrite `_explain_text()` in `build_terrain_map.py`

Current:
> "7,760 entities share name+ZIP between Epa Echo and Irs Bmf. Multi-signal corroboration (not deterministic but strong — same name at same location in both datasets)."

Rewritten:
> "7,760 organizations appear in BOTH EPA enforcement records AND on the IRS tax-exempt master list. Same name, same ZIP code — these are nonprofits and companies that the EPA is simultaneously monitoring for environmental compliance. Cross-reference these to find who's claiming tax-exempt status while racking up violations."

### 2. Coverage Health Panel

Add a "What You're Seeing (and What You're Not)" section:
- **Connected:** 100 tables, 389M rows accessible, 27M entity matches found
- **In the Dark:** 142 tables can't connect yet — their only shared keys are names/addresses, and fuzzy matching at 17M+ rows is too slow without a smarter engine
- List the 5 biggest "dark" tables with row counts and what keys they have

### 3. Human-Readable Domain Labels

| Internal | Display |
|----------|---------|
| corporate_entities | Who Owns What |
| money_in_politics | Money in Politics |
| health_medicine | Healthcare |
| sanctions_enforcement | Who's Banned |
| transport_movement | Planes, Trains & Ships |
| energy_environment | Energy & Environment |
| crime_security | Crime & Security |
| justice_courts | Courts & Justice |
| spending_budget | Government Spending |
| economy_labor_trade | Economy & Labor |
| housing_social | Housing & Social |
| education | Education |
| elections_voting | Elections |
| government_power | Government |

### 4. "So What?" Context Per Connection

Each sidebar card gets a third line: what this connection *enables*. Examples:
- **FCC License Holders ↔ Campaign Donors:** "Trace whether telecom companies and broadcast owners donate to the legislators who regulate them."
- **EPA Facilities ↔ Federal Contractors:** "Find companies receiving government contracts while simultaneously under environmental enforcement action."
- **SEC Companies ↔ Insider Trading:** "Every insider trade linked back to the company's full financial filings — see who sold before bad earnings."

### 5. Header Narrative

Replace:
> "Cross-domain entity connections across 242 sources, 15 domains."

With:
> "This map shows where 389 million rows of public data secretly share entities — the same people, companies, and places appearing across datasets that were never designed to talk to each other. Each line is a proven pathway: a question you can ask that spans two worlds."

### 6. (Optional) Raise discover threshold to connect more data

Change `NAME_MAX_ROWS` from 300K → 2M in `connect/discover.py`. Then re-run `python -m connect discover` to unlock NAME@ZIP connections for mid-size tables like CFPB (17M), SBA Loans (2M), NHTSA (2M). The truly huge ones (58M NOAA AIS) would still need a different approach (blocking/LSH).

## Files Modified

- `scripts/build_terrain_map.py` — rewrite `_explain_text()`, `_friendly_name()`, add coverage query, update HTML template
- `outputs/terrain_map.html` — regenerated output
- `connect/discover.py` line 35 — raise `NAME_MAX_ROWS` (optional, step 6 only)
