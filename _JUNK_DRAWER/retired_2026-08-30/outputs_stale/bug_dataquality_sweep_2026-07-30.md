# Bug / Data-Quality Sweep — 2026-07-30

19 candidates found, 19 confirmed by an independent adversarial-verify pass (each read the actual file before agreeing). Ranked by severity.

## HIGH — data can be silently wrong, or the app can crash mid-workflow

1. **`scripts/_bulk_load_utils.py:53,132-141`** — Every bulk loader built on this shares a hardcoded `nrows=500_000` pandas cap. A 2M-row source silently truncates to 500k, overwrites the old table, and logs `status='success'`. Nothing compares loaded rows to true source size.
2. **`scripts/tier1_bulk_batch_load.py:460`** — Same 500k-row silent-truncation cap, CLI default, across `load_csv/load_zip_csv/load_zip_multi/load_xlsx/load_bz2_csv`.
3. **`scripts/tier1_bulk_retry.py:167-244`** — Same pattern again, repeated across `tier1_bulk_retry2.py`, `osha_ita_bulk_load.py`, `sec_bulk_discover_load.py`, `irs_bulk_discover_load.py`, `cms_bulk_discover_load.py`. This is a systemic pattern, not a one-off bug — every loader built on this shared cap can lose the tail of a large federal file with zero signal.
4. **`honesty/grading.py:45-49,126-134`** — `HARD_ID_TOKENS` grades a join as trustworthy ("FACT") purely by column *name* (e.g. anything named `*_EIN`), never by querying `COUNT(DISTINCT ...)`. This is exactly the sentinel-masked-ID trap CLAUDE.md already documents (NPPES EIN, FCC ULS EIN) — the honesty engine has no mechanism to catch a repeat of it.
5. **`honesty/traps.py:45-53` (`SOURCE_TRAPS`)** — Only 5 tables are registered as known traps. NPPES and FCC ULS — the platform's own two confirmed sentinel-ID incidents — aren't in the list, so marts built on them get a clean trap report.
6. **`reading_room/app.py:112-116`** — The queue's `st.radio` widget is keyed with sticky session state; after a Confirm/Reject click, `st.rerun()` re-fetches a queue that no longer contains the just-decided lead, and Streamlit throws when a stored widget value isn't in the new options — the reviewer can hit an app crash right after signing off a lead instead of moving to the next one.

## MEDIUM

7. **`serve/app.py:232-234,326-352`** — If a dossier's "jump to connection graph" focus list resolves to zero valid nodes (e.g. graph cache is stale), the code silently falls back to rendering the *entire* unfiltered graph — but the caption still claims it's showing a filtered neighborhood.
8. **`reading_room/app.py:253-263`** — The post-decision confirmation reads back the *globally latest* decision row for a lead with no filter tying it to the current user's write. Two reviewers racing on the same lead can cause reviewer A to see reviewer B's verdict flashed as confirmation of A's own click.
9. **`viz/sqlrun.py:91-94`** — `USE DATABASE THE_LIBRARY` failures are swallowed by a bare `except: pass` with no note logged, so `lane_status()` reports a clean lane even when the documented default-database convenience silently didn't take effect.
10. **`scripts/courtlistener_dockets_load.py:42-43`** (and matching code in `dea_arcos_full_load.py`) — Multi-GB download cache path is hardcoded to a Claude-Code-session-scoped scratch directory, not a stable project path. A new session/machine loses the cache and re-downloads, or fails if the temp dir was cleaned up.
11. **`infra/keys_ledger.json`** — `RIPPLE_REVIEW_PAT` and `LDA_API_KEY` are live, in-use credentials with zero entries in the ledger `check_keys.py` monitors — they can expire with no warning, unlike the 7 tracked keys.
12. **`.../stg_fed_slavevoyages_intraamerican__intra_american_voyages.sql:38,45-51`** — Dedup-by-voyage_id orders by `_ingested_at`, but that column is `current_timestamp()` computed in the same query — not a real landing timestamp. If a duplicate voyage_id ever lands, which row survives is arbitrary and can flip between dbt runs, despite the model claiming deterministic dedup.
13. **`honesty/grading.py:1-22,401-405`** — Structural version of #4/#5: the entire grading engine is text/lineage-only, no live data check anywhere in the file. Any future masked-ID column with a matching name token passes as FACT-grade with no data-layer check possible.

## LOW

14. **`serve/serve_graph.py:79`** — Unchecking every edge-tier checkbox silently reverts to default tiers (`set() or DEFAULT_TIERS` — empty set is falsy) instead of showing an empty graph; UI and rendered plot disagree.
15. **`serve/app.py:216`** — "Appears across N sources" prefers a possibly-stale cached count over the live row count shown two lines below on the same page; also a genuine `SOURCE_COUNT=0` gets silently replaced by the live count due to `or` truthiness.
16. **`serve/serve_queries.py:179-198`** — Facility affiliations hard-capped at `LIMIT 100` with no "showing top 100" indicator — a heavily-affiliated NPI's dossier silently undercounts.
17. **`serve/serve_queries.py:129-160`** — Name/source search capped at `LIMIT 50` with no total-match indicator; a search can look like "not in the platform" when it's just past the cutoff.
18. **`reading_room/app.py:89-91`** — Queue rows and queue-depth count are two separate, non-atomic queries; a decision landing between them can make the "showing N of depth" header cosmetically wrong.
19. **`viz/sqlrun.py:150`** — The warehouse-existence check builds SQL via raw f-string interpolation of an env var (`RIPPLE_SERVE_WH`), while the same value is correctly sanitized via `guard.validate_fqn()` two lines later for the `USE WAREHOUSE` call. Inconsistent guard — a malformed env var could break or inject into that query.
