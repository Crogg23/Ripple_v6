# Cost estimate — fingerprinting the dark tables (2026-08-01)

The census flagged 1,032 landed tables with no fingerprint. Composition
(measured today, metadata-only, registry CATALOG row counts):

| Slice | Tables | Rows | What they are |
|---|---:|---:|---|
| Portal scrapes | 899 | 2.7M | Excluded ON PURPOSE by fingerprint.py's connectable-first gate (no hard entity key in their columns — NAME/ZIP-only city scrapes) |
| **Core sources** | **133** | **482.3M** | Landed AFTER the last fingerprint run — genuinely dark |

**The headline: the 133 dark core tables hold 482M rows — more than half the
Library's landing rows — and they are exactly the accountability-heavy
sources.** Biggest: DEA ARCOS opioid shipments (178.6M), SEC 13F holdings
(101.3M), CourtListener dockets (71.7M), the FDA FAERS adverse-event suite
(~62M across 5 tables), UK Companies House (5.7M), GLEIF (6.3M), EPA FRS
(5.3M). The lattice's biggest blind spot is the richest shelf in the building.

## What fingerprinting costs

Per table (`connect/fingerprint.py`): one `COUNT(*)` (metadata-served, free)
plus ONE combined aggregate scanning only the detected key columns
(`APPROX_COUNT_DISTINCT`, capped at 16 columns). Cost is one columnar scan of
the key columns per table — not a full-table read.

| Option | Warehouse time (XS) | Est. cost | Notes |
|---|---|---|---|
| 133 dark core tables only | ~20–60 min | **~$1–3** | scan ≈ 10–40 GB of key columns; +~4 min round-trip overhead |
| Full re-run (all ~1,040 connectable tables) | ~1–2 h | **~$3–8** | also REFRESHES stale fingerprints (current file predates recent loads) |
| The 899 portal scrapes | ~30–45 min | ~$2 | latency-dominated, near-zero data; excluded by design — not recommended |

Rates assumed ~$3/credit, XS = 1 credit/hr; halve or double per the actual
Snowflake plan. Every number here is a scan estimate with honest ±2× slack.

**Recommendation (yellow-lane): full re-run.** `fingerprint.run(tables=[...])`
on a subset OVERWRITES the whole JSON with only that subset (no merge), so the
subset path needs a wrapper; the full re-run needs zero new code, refreshes
everything, and the price difference is beer money. After it lands, re-run
`scripts/hunch_census.py --with-registry` — the lattice number will jump.

**The RED part, per the constitution:** this runs INSERT-free on the standard
loader lane but it is real warehouse spend on your account. Say go and it runs;
this note is the ask.
