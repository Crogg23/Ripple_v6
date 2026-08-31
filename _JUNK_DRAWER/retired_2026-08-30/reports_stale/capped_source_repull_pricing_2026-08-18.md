# Capped-Source Re-Pull Pricing — 2026-08-18

Follow-up to the round-number loader-cap audit (18 tables, section 4 of
`mart_defect_verdicts_2026-08-10.md`). That pass found the root cause and
confirmed status for all 18; this pass prices only what's still actually
capped and not yet re-pulled. **No data was touched and no warehouse queries
were run this session** — pricing comes from loader scripts, mart/schema
headers, git history, and a few free public-API/web checks (two portal
totals below were live-confirmed via their own APIs just now, at zero
warehouse cost).

## Already fixed, no cost needed (10 tables)

8 tables hit the shared 500,000-row loader-default bug and 2 hit a 10,000-row
API-page cap; all 10 were already re-pulled to real size before the 8/11
census scan (repo-convention header on each: "row count re-verified against
the live table 2026-08-11"). Nothing to price, nothing to do:
IRS auto-revocations, IRS Pub78 donees, Google political-ads geo-spend /
creative-stats / creative-ID-mapping, CourtListener investments, OSHA ITA
case detail 2023 & 2024, Treasury DTS deposits, FDIC bank data. (One loose
end: `schema_fed_fdic_bank_data.yml`'s description text still says "SAMPLE
ONLY" even though the data and .sql header are already fixed — a five-minute
doc fix, not a re-pull, flagging it here so it doesn't get lost.)

## Excluded — not confirmed capped

**BJS data collections** (`FED_BJS_DATA`, 1,000 rows): this is a catalog of
named BJS-sponsored research collections, not incident records. No
BJS-specific published total was found to compare against (only a
combined-agency NACJD figure of "2,700+ studies," which isn't the same
count). Leaving this off the priced list — pricing a re-pull assumes the cap
is real, and that isn't established here.

## Priced go/no-go — the 7 tables still open

| Table | Confirmed real size vs. current | Est. time | Est. $ | Notes |
|---|---|---|---|---|
| EPA Envirofacts (TRI facility names) | 64,990 vs. 5,000 (13x) | ~1 min run + ~30-60 min dev | <$1 | Cheapest item here — a full pull of this exact endpoint was already proven elsewhere in this repo (`scripts/recon_bulk_load_2026-08-07.py`, `FED_EPA_TRI_FACILITY` entry): 64,990 rows, ~50s, 19.6MB, free API, no auth. Just needs a persisted loader pointed at the mart (today's pull was ephemeral). Note: FRS/site/handler ID columns are blank even in a full TRI-facility pull — those live in a *different* Envirofacts program table and would need a separate pull to fill, out of scope of "just raise the row cap." |
| GovData.de (open-data catalog) | **156,122** (live-confirmed via its own CKAN API this session) vs. 5,000 (31x) | ~20-40 min run + ~30-60 min dev | <$2 | Biggest gap of the four open-data portals by far — the 5,000-row mart is under 4% of the real catalog. Same free, paginated CKAN `package_search` API pattern as the other three; no persisted loader exists yet. |
| datos.gob.cl (open-data catalog) | **3,184** (live-confirmed via its own CKAN API this session) vs. 1,000 (3.2x) | a few min + ~30 min dev | <$1 | Smallest, cheapest of the four portals. |
| opendata.swiss (open-data catalog) | ~7,000 (recent public figure — this session's direct CKAN API call got HTTP 403, likely bot-blocking of this exact tool, not proof the API is gone; not independently live-verified) | a few min + ~30-60 min dev | <$1 | Smallest real gap of the group (5,000 already landed is most of ~7,000) — lowest priority of the four portals for the money. |
| datos.gob.es (open-data catalog) | ~100,000 (recent public figure — the DCAT API endpoint tried this session paginates but doesn't advertise a total, so not independently confirmed) | fix bug first (~30-60 min dev), then ~30-60 min run | <$2 | **Sequencing matters**: this mart already has a documented parse bug (URI/title/description columns land blank). Fix that first — re-pulling a broken parser just reproduces the bug at 100x scale. Real catalog is reportedly ~10x bigger than GovData.de's confirmed total, so treat the ~100k figure as directional only until checked live. |
| HUDOC (ECHR case law) | ECHR's own FAQ: 40,000+ (41,621 with English text) vs. 2,000 (20x+) | ~2-3h dev + ~2-4h run | <$3 (mostly time, not $) | Highest-effort item on this list. Checked this session: HUDOC has **no official bulk-download/export API** — only its interactive search UI. Open-source scrapers exist (e.g. the `echr-extractor` PyPI package) that page through HUDOC's internal search JSON endpoint with rate limiting, proving a full pull is possible but requiring new loader code from scratch (nothing persisted in `scripts/` today, unlike every other table above). |
| USAspending subawards | Real total not pinned down — mart's own header already calls it "the multi-million-row subaward corpus"; web search didn't surface an exact government-wide count | ~2-4h dev + ~2-6h run, scope-dependent | ~$5-15 | **Needs a scope call before pricing tightens**: "current fiscal year" vs. "full history" changes size by 10x+. No subaward-specific loader exists — the only USASpending script in `scripts/` (`usaspending_load.py`) is a *deprecated* prime-contract-awards puller (non-atomic, kept for provenance only) using the same async POST→poll→zip job pattern subawards would need, chunked by month like it already does for contracts. Recommend Chris picks a year range before this gets built. |

## What this list is NOT

Not a go — nothing above was re-pulled or scheduled. Per this repo's
priced-go/no-go convention (`reports/warehouse_repair_2026-08-11.md`), the
decision to spend the time/money is Chris's, table by table or as a batch.

*No publish decisions are implied anywhere in this report; findings remain
human-gated per the constitution.*
