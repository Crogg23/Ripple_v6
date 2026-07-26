# Handoff: Data Coverage Expansion — 2026-07-25

## What got done (code changes, all tests green — 478/478)

### Phase 1.1 — Fanout cap (discover.py)
Added `VALUE_FANOUT_CAP = 50`. The self-join now uses a CTE with
`QUALIFY COUNT(DISTINCT table_name) OVER (PARTITION BY key, val) <= 50`
so a single hot value (e.g. one ZIP shared across 1,500 portal tables) can't
emit ~1M pairs and blow up the graph.

### Phase 1.2 — Bare NAME gated (discover.py)
Bare NAME and ADDRESS keys are now **completely blocked** from the keyset.
Only the corroborated composite (`NAME@ZIP`, `NAME@FIPS`) can produce edges.
This kills the single biggest junk source at scale.

### Phase 2.1 — Fingerprint filter narrowed (fingerprint.py)
`landed_tables()` no longer blanket-excludes all `PORTAL_%` tables. Instead it
includes a portal table **only if** at least one of its columns carries a
STEEL/STRONG entity key (EIN, NPI, CIK, UEI, etc.) per `detect_key()` from
`keys.py`. NAME/ZIP-only city scrapes stay excluded.

---

## What's blocked — needs a fresh PAT

The live pipeline (`python -m connect fingerprint` → `discover` → `spine` →
terrain map) requires a working Snowflake credential for the Python connector.

- **Password alone won't work** — MFA is enforced on the account.
- **The old PAT (eyJraWQ...) is invalid** — Snowflake rejects it.

### To unblock:
1. In Snowsight: avatar → Developer → Programmatic Access Tokens → Generate
2. Copy the new token
3. Put it in `library-onboarding/.env` as `SNOWFLAKE_PAT=<token>`
4. Optionally add `SNOWFLAKE_AUTHENTICATOR=PROGRAMMATIC_ACCESS_TOKEN`

### Then run:
```bash
cd /path/to/Ripple_v6
python3 -m connect fingerprint   # ~3 min, scans 242+ tables
python3 -m connect discover      # verify edge count stays ~1,506
python3 -m connect spine
python3 -m connect.incremental seed
python3 -m connect.incremental validate
python3 scripts/build_terrain_map.py
```

---

## What's next after the pipeline runs

- **Phase 1.3**: Confirm edge count ~1,506 (no legitimate edges lost by the guards).
- **Phase 2.2–2.4**: Measure new portal edges, rebuild spine, regenerate terrain map.
- **Phase 3**: Loader campaign for 769 cataloged-but-unloaded sources (triage by access method, batch spec-able Tier-1 sources, incremental discover after each batch).

---

## Key files changed
- `connect/discover.py` — fanout cap + bare-NAME gate
- `connect/fingerprint.py` — connectable-first portal allowlist

## Baseline to verify against
- `LIBRARY_META.CONNECT.CONNECT_EDGES` currently has **1,506 rows**
- `pytest -q -m "not snowflake"` → 478 passed, 2 skipped
