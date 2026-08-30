# RIPPLE STATUS — 2026-08-29 (evening) — Joins re-founded: time + place are first-class joins; master connections list (pass 1) shipped; four no-brainer sources landed

*One screen. Rewritten (never appended) at the end of every session.*

## 🚨 Read this first

1. **Two standing rules from Chris today, both in memory:** (a) *stop jumping ahead* — answer
   the question asked, no build plans / costs / next steps unless he says "think it through";
   (b) *time and geography are joins* — same day/month + same state/district/county is a
   first-class connection with no ID needed. The ID spine is deprioritized ("waste of time").
   Do not restate limits he already knows.
2. **The SAM public extract does NOT carry DUNS anymore** (column present, 100% empty). The
   "fix the 94% orphaned assistance-table DUNS" promise is NOT delivered. What landed instead:
   CAGE↔UEI for 795K entities (93% of contract CAGEs / 92% of contract UEIs resolve).
3. **Landed today (raw layer, gate PASS):** SAM entity registry 895,429; USCG documented vessels
   391,684 (Dec-2025 release via Wayback — the Coast Guard site 403s every bot); FMCSA carrier
   census 4,493,662; EPA CAMPD plant/unit attributes 128,525 (1995–2025) + daily unit emissions
   16,513,971 (2015–2025). Loader: `scripts/nobrainer_bulk_load_2026_08_29.py`.
   Measured: 1 in 3 AIS vessels now resolve to a US-documented vessel (by IMO and by call sign);
   81% of CAMPD plants match EIA plant ids; sanctioned vessels 0 (foreign flag, expected).
4. **Already held before today (my "not held" call was wrong):** GLEIF Level-2 parent links
   (485K), FDA NDC directory (116K), GUDID device registry (5.2M). Check landing tables, not
   mart column names, before calling anything missing.
5. **Pass-1 master connections list** (beyond-reasonable-doubt noun joins) is at
   `reports/recon/master_connections_pass1_2026-08-29.md`: 22 wired families with measured
   edges, 11 wired-not-mapped, 5 crosswalks, ~50 newly value-verified ID systems (section G:
   95 candidates × 391 live columns checked), dead/masked list, today's landings (section H).
   The 08-05 "747-key sweep" was web research with 5 verified — now fully checked.
6. **Inventories filed:** every real date/datetime/month/year column (1,275 cols / 453 tables,
   value-verified) at `reports/time_index/DATE_COLUMNS_ALL.md`; every location-shaped column
   (2,244 / 386 tables, NAME-scan only) at `reports/location_index/LOCATION_COLUMNS_ALL.md`.
7. **Unchanged from this morning:** apply-config not yet run (drift test red until it is);
   8 spatial join errors (TRI + NTSB coords); DOCKET ~40% wrong; Snowflake MCP token rejected
   (the direct python connection works fine — use it); overnight loads (MAUDE, subawards, LDA)
   unchecked. Contradiction flag: FDIC LEI is 8% filled / 2,241 distinct, not "empty".
8. **Git:** an auto-commit ("Refactor code structure…") landed mid-session; working tree now
   holds the loader, its checkpoint, and the updated pass-1 file.

## BROKE

Nothing broke. All five new tables passed the quality gate. The one miss is item 2
(DUNS not in the public SAM file) — a source limitation, not a failure.

## YOUR MOVE (Chris)

Nothing blocking. Pass 2 of the master list (name-scan-only IDs, the 747 reach list,
parent/owner pointers) and the time/place inventories are ready whenever you point at them.

## NEXT (only when asked)

- Pass 2 of the connections list.
- Value scan of the 2,244 place columns (same shape as the time scan, ~$1–2).
- DUNS alternatives: pre-2022 SAM monthly files via Wayback, or the FOUO extract.
- Register the new families (CAGE↔UEI from SAM, USCG official #, USDOT #, CAMPD facility id)
  once Chris wants them in the join map.

**Cost note:** ~$4 warehouse compute this session (live column checks ~$1, five loads ~$2,
overlap measurements ~$1). Storage added ≈ 22M rows.
