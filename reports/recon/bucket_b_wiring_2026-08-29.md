# Bucket-B wiring batch — 2026-08-29 (staged, dark)

Chris: "go" on wiring the held-but-unregistered ID systems, in order CAGE + award keys →
PECOS → FDIC cert + RSSD → EIA plant/utility → NDC/FDA.

Everything below is registered in code behind `keys.ENABLE_SPINE_BATCH_2026_08_29 = False`.
Flipping it changes the incremental fingerprint and freezes incremental until a full spine
rebuild (~$10–15 on X-Small, ~4.5h per the 08-08 run). Flip only in that session.

## Live verification (all numbers 2026-08-29, landing tables, normalizer SQL applied)

| Family | Anchor table | Distinct (normalized) | Cross-table overlap | Verdict |
|---|---|---|---|---|
| CAGE | contracts R2 | 246,832 (55.4M of 93.2M rows filled) | SAM exclusions: 182 of 392 CAGE-bearing rows also in contracts (46%) | wired — entity axis, extra key on the recipient row |
| AWARD_KEY | contracts R2 / assistance / subawards | 74.5M / 14.25M / 279,553 | subawards prime key → contracts 39.4% (R2 stops at FY2021), → assistance 94,063 | wired — graph key only (award = document) |
| PECOS_PAC_ID | FFS enrollment | 2,456,135 | facility affiliation 99.7%; hospital 99.7%, SNF 98.6% | wired — entity axis, extra key on NPI rows |
| PECOS_ENRLMT_ID | FFS enrollment | 2,978,925 (1 per row) | hospital enrollment file 99.2% | wired — graph key only (enrollment = event) |
| FDIC_CERT | FDIC institution master | 27,830 | branch/deposits 99.9%; **FHLB members 3,983 / 3,984 (99.97%) after zero-pad** (raw string compare said 69%) | wired — entity axis, 3 tables |
| RSSD | FDIC institution master | 26,576 | branch file 15,302 / 15,541 (98.5%); holding-company column 74–83% (parent → graph only) | wired — entity axis; CERT↔RSSD collide on 2.4% of values so they stay separate families |
| EIA_PLANT_ID | EIA-860 plant master | 16,128 | generators 100%, owners 100%, **eGRID 2022 emissions 11,800 / 11,971 (98.6%)** | wired — facility axis, 10 tables |
| EIA_UTILITY_ID | EIA-860 utility master | 6,643 | plant file 100%, eGRID 94.6%, EIA-861 22% (different reporting universe) | wired — org axis, 12 tables |

## Excluded / parked (one line each)

- **FDIC failed-banks + OCC bank/thrift lists** — CERT/RSSD stored as float text (`19117.0`, `nan`); the normalizer would mint `191170`. Repair the text first, then add (three table-scoped entries).
- **NDC** — NADAC holds 11-digit package codes, the FDA directory holds hyphenated 2-segment product codes: 0 overlap is a grain mismatch, not a fault. Needs a segment-aware normalizer mode = a normalizer code change = its own guard trip. Not this batch.
- **FDA 510(k)/PMA/FEI tables** — 88 / 29 / 166 rows; stubs, not worth an axis until re-landed.
- **FHLB NCUA_ID / NAIC_ID / FED_ID columns** — probably credit-union charter / insurer / RSSD ids; unverified, parked.
- **Duplicate EIA tables** (`FED_EIA_860_*`, one extra row each) and the FFS enrollment twin — graph keys registered on the twin; spine spec only on the one already specced.
- Pad-mode placeholder kill drops 6 FDIC certs and 4 EIA plant codes (all-same-digit values like `1111`); possibly real, ≤0.03%, noted not fixed.

## What changed in code

- `connect/keys.py` — flag, 8 norm rules, 40 table-scoped key columns (all under the flag).
- `connect/entity_index_specs.py` — 6 new spine specs (FDIC master, branch/deposits, FHLB members, EIA utility master, EIA plant master, eGRID plants), 10 extra-key patches on already-wired tables, 6 entity-type entries.
- `connect/discover.py` — collision value-spaces for the 8 new families **plus CUSIP and the two MSHA ids, which were wired 08-28 without one** (same footgun the COMPANY_NO fix documented).
- `tests/test_spine_batch_2026_08_29.py` — 8 tests, flag simulated ON.

Evidence: `reports/recon/bucket_b_verify_2026-08-29.json`, `bucket_b_verify2_2026-08-29.json`.
