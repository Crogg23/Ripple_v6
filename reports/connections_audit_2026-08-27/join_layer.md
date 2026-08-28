# Join-Layer Audit — 2026-08-27

Read-only audit via the guarded lane (SERVE_WH, enforced). Budget stayed at
SERVE_MON 5.29/100 credits before and after — the whole audit cost effectively
nothing (all queries were metadata-sized aggregates; biggest single query 5.3s).

## 1. STEEL key families (connect/keys.py + portal_recon/tag_portal_index.py)

The tagger's KEY_TOKENS holds 18 STEEL families; connect-local rules
(EXACT_TOKEN_KEYS / TABLE_COLUMN_KEYS) add 6 more, for **24 STEEL families
total** (the "13" in the task brief is stale — it predates the 2026-07-30 and
2026-08 spine batches).

| Family | Declared in | Norm rule (NORM_RULES) |
|---|---|---|
| EIN | KEY_TOKENS `ein` | pad 9 (digits-only, placeholder kill list) |
| NPI | KEY_TOKENS `npi` | pad 10 |
| CIK | KEY_TOKENS `cik` | pad 10 |
| UEI | KEY_TOKENS `uei` | fixed 12 |
| DUNS | KEY_TOKENS `duns` | pad 9 |
| BIOGUIDE | KEY_TOKENS `bioguide` | alnum_upper |
| ICPSR | KEY_TOKENS `icpsr` (excludes `state` co-token) | alnum_upper |
| PATENT | KEY_TOKENS `patent` | code |
| LEI | KEY_TOKENS `lei` | fixed 20 |
| IMO | KEY_TOKENS `imo` | imo 7 (digits, strips 'IMO' prefix, kills all-zero) |
| MMSI | KEY_TOKENS `mmsi` | pad 9 |
| CCN | KEY_TOKENS `ccn` | pad 6 |
| DEA_NO | KEY_TOKENS `dea` | alnum_upper |
| PWSID | KEY_TOKENS `pwsid` | fixed 9 |
| FRS_ID | pair-rules only (bare `frs` unsafe) | fixed 12 |
| MINE_ID | pair-rules only | pad 7 (quote-stripping via _alnum) |
| FEC_CMTE_ID | pair-rules + table-scoped FEC positional cols | alnum_upper |
| FEC_CAND_ID | pair-rules + table-scoped FEC positional cols | alnum_upper |
| COMPANY_NO | EXACT_TOKEN {company,number} | fixed 8 |
| NPDES_ID | EXACT_TOKEN {npdes,id} | alnum_upper (spine batch, flag ON) |
| ICE_FACILITY | EXACT_TOKEN {detention,facility,code} | alnum_upper |
| NCUA_CHARTER | EXACT_TOKEN (3 spellings) | alnum_upper |
| CL_PERSON_ID | EXACT_TOKEN + table-scoped bare ID | alnum_upper |
| CL_COURT_ID | EXACT_TOKEN + table-scoped bare ID | alnum_upper |

Normalization philosophy: PAD never strip (leading-zero stripping manufactured
the Alabama/Puerto-Rico false match); pad-mode kills repeated-digit fillers and
keyboard-walk sentinels (PAD_PLACEHOLDERS) — the fake-EIN-999999999 fix.
ENABLE_SPINE_BATCH_2026_08 = True (the batch is live).

## 2. Connect-layer objects

LIBRARY_META."CONNECT" (26 tables): the ones that matter —
- **ENTITY_INDEX** (90.0M rows) — entity_id / key_type / key_value / source_table; the spine.
- **KEYSET_LIVE** (177.0M) — (table, key, val), de-duplicated (rows == distinct per table): the per-table key inventory.
- **CONNECT_EDGES** (4,910) — table-pair edges with key, tier, matched counts.
- ENTITY_GOLDEN / ENTITY_MAP (35.95M), SPINE_KEYSET(_LIVE) (90.0M), MATCH_PAIRS (182.4M), GOLD_PAIRS, BRIDGE_ENTITIES, LEADS, ENTITY_LINKS (lane-blocked as leads — correct behavior, the libel firewall fired mid-audit).

LIBRARY_META.REGISTRY: SOURCE_REGISTRY (2,780 rows; JOIN_KEYS_STD / JOIN_KEY_TIER
columns are the per-source key registry), COLUMN_CATALOG (751), PORTAL_DATASET_INDEX
(338,520), plus 4 stale `_BAK_` copies of SOURCE_REGISTRY still sitting in the schema.
**No COLUMN_TRUST table exists in LIBRARY_META** (no `%TRUST%` object; the account-wide
probe errored out on the lead-guard before completing, but the named schemas are clean).
The task brief's "COLUMN_TRUST" appears to be a stale name.

## 3. Family coverage (KEYSET_LIVE tables / ENTITY_INDEX / CONNECT_EDGES)

| Family | Tables carrying it | Distinct vals | In entity index? | Edges | Verdict |
|---|---|---|---|---|---|
| NPI | 34 | 9.61M | yes (32 src) | 358 | healthy, biggest connector (117M matched pairs) |
| EIN | 34 | 3.41M | yes (35 src) | 366 | healthy |
| CCN | 25 | 82K | yes (23) | 78 | healthy |
| CIK | 19 | 181K | yes (19) | 128 | healthy |
| FRS_ID | 18 | 5.40M | yes (14) | 154 | healthy (56.9M matches) |
| FEC_CMTE_ID | 11 | 45K | yes (9) | 56 | healthy |
| FEC_CAND_ID | 10 | 23K | yes (6) | 47 | healthy |
| PWSID | 10 | 434K | yes (10) | 45 | healthy |
| NPDES_ID | 10 | 1.21M | yes (8) | 45 | healthy |
| UEI | 7 | 371K | yes (7) | 18 | healthy |
| LEI | 7 | 3.38M | yes (4) | 21 | healthy |
| CL_PERSON_ID | 8 | 16K | yes (8) | 28 | healthy |
| BIOGUIDE | 5 | 12.8K | yes (5) | 14 | healthy |
| CL_COURT_ID | 4 | 3.4K | yes (3) | 6 | healthy |
| NCUA_CHARTER | 4 | 4.3K | yes (4) | 6 | healthy |
| ICPSR | 3 | 12.7K | yes (2) | 3 | healthy, small |
| MINE_ID | 3 | 92K | yes (3) | 3 | healthy |
| ICE_FACILITY | 3 | 5.8K | yes (2) | 3 | healthy |
| DUNS | 3 | 495K | **partial (2 of 3)** | 3 | **94% of values orphaned** — see §5 |
| COMPANY_NO | 2 | 8.51M | yes (2) | 1 | works but is a closed 2-table island (UK CH ↔ PSC only) |
| IMO | 2 | 8.7K | yes (3: AIS/OFAC/UK-sanctions) | **0** | **indexed but edge-less** — the ship-sanctions join never built |
| MMSI | 1 (FED_NOAA_AIS) | 22.7K | **no** | **0** | **ONE-SIDED, connects nothing** |
| DEA_NO | 1 (FED_DEA_ARCOS_FULL) | 148.6K | yes (1) | **0** | **ONE-SIDED** — no second DEA-number table exists |
| PATENT | **0** | 0 | no | 0 | **DEAD family** — STEEL in the tagger, zero columns anywhere |

## 4. Sentinel screen

Top-10 value frequencies per family across ENTITY_INDEX: **clean everywhere**.
The single most concentrated value in any family is 0.09% of its family's rows
(an ICE facility hold code appearing twice out of 2,197). No family has any
value above the 1% flag line — the pad-mode placeholder kill list (all-zeros,
repeated-digit, keyboard walks, '<UNAVAIL>' letter-rejection) is doing its job;
no repeat of the fake-EIN-999999999 merge is present in the current index.
(KEYSET_LIVE itself is per-table de-duplicated, so the frequency screen was run
on ENTITY_INDEX, which keeps one row per source occurrence.)

## 5. Orphan rates (distinct keyset values with no entity-index entry)

| Family | Keyset distinct | Matched in index | Orphan % |
|---|---|---|---|
| NPI | 9,608,817 | 9,608,798 | 0.00% |
| CIK | 181,245 | 181,245 | 0.00% |
| NPDES_ID | 1,213,740 | 1,213,740 | 0.00% |
| UEI | 371,175 | 371,155 | 0.01% |
| EIN | 3,412,085 | 3,411,514 | 0.02% |
| **DUNS** | **494,789** | **29,664** | **94.00%** |

The DUNS gap is one table: FED_USASPENDING_ASSISTANCE_FULL carries 478,231
distinct DUNS values in the keyset, but the entity index only ingested DUNS from
FED_NIH_REPORTER (14,919) and FED_SBIR_STTR_AWARDS (21,594). The spine never
absorbed the assistance table's DUNS side — every grant recipient identified
only by DUNS is invisible to the graph. (UEI on the same table IS indexed, so
post-2022 awards resolve; the pre-UEI-transition history is what's dark.)

## 6. Ranked findings

1. **DUNS 94% orphaned** — USAspending assistance DUNS (478K recipients) never entered the entity index; historical (pre-UEI) grant recipients are disconnected.
2. **PATENT is a dead STEEL family** — declared in the tagger, zero carrying columns in the keyset or index.
3. **MMSI is one-sided** — AIS only, not even in the entity index; with IMO edge-less too, the ship axis (AIS ↔ OFAC/UK sanctions) is indexed but produces 0 edges — the sanctioned-vessel join the IMO normalizer was built for has never materialized.
4. **DEA_NO one-sided** — ARCOS only; harmless but a non-connector until a second DEA-registrant source lands.
5. **COMPANY_NO is a 2-table island** — real (2.34M matched pairs) but connects only UK CH ↔ PSC; no bridge to the rest of the graph.
6. Hygiene: 4 stale `_BAK_` SOURCE_REGISTRY copies in REGISTRY; no COLUMN_TRUST table exists (stale name in audit briefs).
7. Sentinel screen fully clean; core-family orphan rates ~0% — the pad/placeholder discipline and spine ingestion for the big 5 families are solid.
