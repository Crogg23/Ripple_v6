# Connections Audit — Combined Summary — 2026-08-27

Three read-only lanes (join layer / graph structure / coverage grid), all SQL
via the guarded read lane. Detail files in this directory:
`join_layer.md`, `graph_structure.md`, `coverage_grid.md`.
Compute cost: ~pennies (meter unmoved at 5.29/100 credits through the whole run).

## Anchor score: 58/100 — precision ~90, coverage ~35

The graph is TRUSTWORTHY but NARROW: what it connects, it connects correctly;
most of what could connect, it doesn't touch.

## What's strong (verified)

- Blob check CLEAN: spine entities are per-key, mega-merges structurally
  impossible; largest entity = Caterpillar's EIN across 20 tables, names
  consistent. Placeholder-key contamination down to 23 trivial rows.
- Sentinel screen fully clean: no key column has a value covering >0.09% of
  rows — the fake-EIN class of bug is dead.
- Core key orphan rates ~0: NPI/CIK/NPDES 0.00%, UEI 0.01%, EIN 0.02%.
- STEEL tier measured precision ~95–100% (3/75 unsure, all
  parent-vs-subsidiary EIN cases, arguably correct).
- Row-level edges: STEEL 206.7M / CORROBORATED 39.5M / BRIDGE 6.1M /
  GEO 578k / STRONG 9.2k / PROBABILISTIC 2.67M. Family counts match the
  registry exactly.
- All five 2026-08 spine-batch families live with edges.

## What's broken / missing (ranked levers)

1. **DUNS 94% orphaned** — 478k pre-UEI grant-recipient DUNS in the assistance
   bulk table never ingested by the spine. One ingestion spec fixes the
   single biggest recall hole. (join_layer.md)
2. **Half the connectable rows aren't connected** — same-universe name+zip
   probe (FHLB members vs FDIC banks) matched 48.6% where hard keys match ~0.
   The CORROBORATED machinery exists; it's pair-selection that's starved.
   Mismatched-universe pairs correctly score ~0 — pair choice is the lever.
3. **92% of the domain×key grid is empty; 17 of 32 domains carry zero STEEL
   keys** (ENERGY 29 tables, EDUCATION 17, TRANSPORT 12, CONSUMER_SAFETY 4
   all at 0%).
4. **Biggest tables are keyless islands**: FEMA housing 26.3M (has name+zip),
   HMDA 19.1M, CFPB complaints 17.2M, Canada contributions 12.6M, EOIR 12.6M,
   FJC/CourtListener block ~38M (internally docket-linked, invisible to spine).
5. **Three dead key families**: PATENT (STEEL, zero carrying columns anywhere),
   MMSI/IMO (ship axis, 0 edges — the sanctioned-vessel join never
   materialized), DEA_NO (ARCOS-only, 100% singleton).
6. **DOCKET key needs an issuer namespace** — FDIC certificate numbers collide
   with Supreme Court docket numbers; 3 of 5 STRONG families (~1,300 edges)
   confirmed false. STRONG tier measured ~40% precision.
7. **CORROBORATED tier ~75–85% precision** — systematic failure modes: bare
   surname@zip and place-name orgs. Fixable with name-shape rules, not rebuild.
8. **GEO tier is not identity** — some families match on 2-digit state/country
   codes; edge counts inflated by noise. Relabel or prune.
9. **Singleton rate 44.1%** (15.86M of 35.95M entities in exactly one source).
   Fine as a raw number; the near-dead axes above are what drive it.
10. **Politics half-refuted**: 26/79 politics tables DO carry STEEL keys and
    FEC bridges to money marts; but the 527-EIN bridge to the exempt-org
    master hits only 0.4%, and the state lobbying layer (~2.7M rows CA/TX/NYC)
    is 100% keyless.
11. Stale docs corrected: 24 STEEL families (not 13); no COLUMN_TRUST table —
    the key registry lives in SOURCE_REGISTRY JOIN_KEYS_STD/JOIN_KEY_TIER.
    (The 08-27 morning session updated a COLUMN_TRUST row — reconcile which
    registry object that actually was.)

## Levers ranked by connected-rows-per-hour

1. DUNS backfill ingestion spec (one table → 478k orphans fixed)
2. Corroborated pair-selection expansion (name+zip machinery to same-universe
   keyless pairs: FEMA/CFPB/FHLB/state-lobby first)
3. DOCKET issuer-namespace fix (kills ~1,300 false edges cheaply)
4. Ship axis: land a vessel registry (USCG PSIX) → IMO/MMSI edges exist
5. PATENT: land PatentsView or demote the family from STEEL
6. GEO tier prune/relabel
7. Name-shape rules for CORROBORATED (surname/place-name kill rules)
