# Fable Mission Packet — Absence Sweep
**Date:** 2026-08-05
**Worker:** Fable (autonomous hunting), high effort / high thoroughness
**Prepared by:** Sonnet, reviewed by Chris before launch

---

## The mission, one sentence

Find every place in the map where a connection or a record *should* exist and doesn't — the survivorship-bias gaps a normal record-by-record read would never catch — and rank them by how credible and how harmful the gap is.

## Why this and why now

This platform already computed most of the raw material for this. Nobody has read it yet:

- `outputs/hunch_absence_verdicts.json` — **236 absence verdicts already scored.** Each one already has a verdict ("credible" / not) and a reason. Unread until this session.
- `outputs/hunch_lattice.json` — **19,326 table-pair comparisons**, tiered STEEL / GEO / STRONG / CORROBORATED / PROBABILISTIC, plus a `blind_spots` block that tells you exactly what's unprocessed.
- `outputs/atlas.json` / `outputs/connect_graph.json` — **2,694 verified real edges**, the ground truth to check absence claims against.
- `outputs/library.json` — all 1,043 fingerprinted tables, each with domain, row count, and candidate key columns.

A hand-picked, manual sweep (done earlier this session) checked ~30 tables by guessing plausible pairs from domain names and found 3 solid leads. That is not coverage — it's a proof of concept. Fable's job is to do the exhaustive version.

## Known false-negative trap — read this before scoring anything "no gap"

Several tables that look "unconnected" in a naive check are actually **zero-key tables** — nobody has identified a join column for them yet. This is NOT evidence of absence. Confirmed zero-key tables include (partial list, see `blind_spots.zero_key_tables` for full 895):

- `FED_EPA_NPDES_NPDES_CS_VIOLATIONS`, `_FORMAL_ENFORCEMENT_ACTIONS`, `_PS_VIOLATIONS`, `_SE_VIOLATIONS`, `_QNCR_HISTORY`
- `FED_FDA_FAERS_DRUG`, `_REAC`, `_INDI`, `_OUTC` (all FDA adverse-event tables)
- `FED_NHTSA_COMPLAINTS`, `_INVESTIGATIONS`, `_RECALLS`
- `FED_FEC_CANDIDATES`, `_CAND_CMTE_LINKAGE`, `_COMMITTEES`, `_LEADERSHIP_PAC`
- `FED_DOJ_EPSTEIN_LIBRARY`, `FED_FBI_NICS_CHECKS`, `FED_CDC_WONDER`, `FED_CDC_HEALTH_INSURANCE`

**Rule: before reporting "X should connect to Y and doesn't" as a finding, first confirm both X and Y have known join keys.** If either is zero-key, the correct output is "needs fingerprinting," not "absence gap."

## Scope of the sweep, in order

1. **Read every one of the 236 existing absence verdicts.** Rank by credibility score and by whether the underlying domain touches real human harm (health, safety, housing, labor, environment — not just administrative mismatches). Surface the top 15-20.

2. **Sweep the STEEL and STRONG tier comparisons in `hunch_lattice.json`** for table pairs that have no absence verdict yet but share a confirmed high-confidence key (CCN, NPI, EIN, FRS_ID, MINE_ID, CIK). These are the highest-signal untested pairs — legitimate joins nobody's checked for absence yet.

3. **Flag priority candidates for new fingerprinting** among the 895 unfingerprinted landing tables — prioritize ones in domains that already have rich connected clusters (HEALTH, ENVIRONMENT, FINANCE, JUSTICE) since they're most likely to plug into existing high-value chains rather than sit as new islands.

4. **For every candidate finding, apply the absence-vs-artifact test explicitly:** could this gap be explained by (a) reporting lag, (b) the two agencies using genuinely different populations, (c) a join key that's real but just noisy/low-population? If yes to any, downgrade or discard — do not pass it through as a finding.

## Output format required

For every surfaced finding, return:
- **The two (or more) tables and the join key**
- **What should exist and doesn't (or does, unexpectedly)**
- **Confidence tier and verdict reason** (pull straight from the data, don't editorialize)
- **The human-harm angle in one sentence** — who's affected if this gap is real
- **Artifact risk flag** — is there a plausible boring explanation, and did you rule it out?

No narrative, no draft copy, no visualization ideas — this is a findings list, ranked, for Chris to read and pick from. Formatting and story framing come after Chris signs off on which findings are real.

## Hard boundaries (constitution, non-negotiable)

- **No publishing, ever, from this run.** Findings come back for human sign-off. No exceptions.
- **Every "connected" claim must trace to `atlas.json`/`connect_graph.json` edges or a fresh, documented Snowflake check** — never assert a join exists without checking it.
- **Never treat a bare non-null count as proof a key is real.** Pair with `COUNT(DISTINCT ...)` and a value sample before trusting any column as a join key (see CLAUDE.md — NPPES EIN and NOAA_AIS imo_number both looked 100% populated and were sentinel-masked garbage).
- **Recon on power, not a target list.** No domain gets special scrutiny because it's politically interesting — score every credible gap the same way regardless of who it implicates.

## What already exists that this mission should NOT redo

Confirmed via manual check this session — do not re-surface these as "new" unless adding real depth beyond what's already found:
- Nursing home deficiencies ↔ penalties (1.0 confidence, gap already identifiable)
- SDWA drinking water violations ↔ public notice chain (full 4-table chain confirmed, strongest lead so far)
- IRS revoked/auto-revoked nonprofits ↔ still-listed-as-eligible-donee status
- Excluded provider (HHS OIG LEIE) ↔ still-billing (NPPES/Part D) — perfect 1.0 join, no prior news coverage found

Fable's job is to find the next 20 of these, exhaustively, not to re-confirm what a human already found by hand.
