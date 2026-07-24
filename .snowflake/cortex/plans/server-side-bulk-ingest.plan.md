---
name: "server-side-bulk-ingest"
created: "2026-07-23T16:37:43.956Z"
status: pending
---

# Server-Side Bulk Ingestion (move GB-scale pours off the laptop)

## Why

The write path is unblocked and small files land fine (SEC insiders = 14 MB, instant). But the CFPB file (1.4 GB) stalls at 0 bytes downloading through this machine, and every high-value stub left is big (CFPB, GLEIF \~GB, plus refreshing Open Payments/Part D/ECHO). Pulling them through the laptop doesn't work. Chris chose: **have Snowflake fetch the files directly** (cloud-to-cloud), so bandwidth stops being the wall.

## What exists today (verified this session)

- **No External Access Integration** on the account (must build one). All 311 network rules are Snowflake-owned *ingress* rules for BI tools — none reusable.
- `bridge_fuel_load.py` already has the *post-landing* logic worth reusing: density gate, `INGEST_RUNS` logging, `SOURCE_REGISTRY` upsert, atomic staging swap (`loadkit.atomic_load`). Today it only fetches via local `requests` — that's the only part that must move server-side.
- No existing inbound server-side fetch pattern (`export_control_plane.py` is outbound-only).
- We hold ACCOUNTADMIN (via `LIBRARY_PAT` now in `.env`), which can create network rules + integrations.

## Architecture (recommended)

Snowflake pulls the URL on its own compute, lands the file in an internal stage, then `COPY INTO` the all-TEXT landing table:

1. **EGRESS network rule** listing source hosts (start focused: `files.consumerfinance.gov`, `leidata.gleif.org`, `www.sec.gov`, `www.irs.gov`, `apps.irs.gov`, `www.fec.gov`, `echo.epa.gov`, `download.cms.gov`, `data.cms.gov`).
2. **External Access Integration** referencing that rule (+ an optional SECRET slot for keyed sources like SAM later).
3. **Internal stage** `LIBRARY_RAW.LANDING.BULK_STAGE`.
4. **Python stored proc** `RIPPLE_FETCH_TO_STAGE(url, stage_path)` — packages `requests` + `snowflake-snowpark-python`, bound to the integration. Streams the URL straight to the stage via `session.file.put_stream` (no full-file buffering → dodges proc memory/disk limits).
5. **Load**: `COPY INTO <TABLE>` from the staged file with an all-TEXT CSV file format, then reuse `bridge_fuel_load`'s density gate + `INGEST_RUNS` log + registry upsert so server-side loads are first-class in the same ledger.

## The one real risk: ZIP decompression inside Snowflake

`COPY INTO` reads `.gz`/`.bz2` natively but **not `.zip`**. The big targets split two ways:

- **Plain CSV / .gz** (CMS Part D, Medicare provider, Open Payments, OpenSanctions): stream to stage → `COPY` directly. Clean, low risk.
- **`.zip`** (CFPB, IRS revocation, FEC, ECHO, SEC data sets): must unzip server-side. Plan: open the staged zip as a seekable stream (`SnowflakeFile`/`get_stream`), use Python `zipfile` to stream the chosen member out via another `put_stream` as a `.gz`, then `COPY`. This needs a spike to confirm proc seekability + memory behavior on a 1.4 GB zip — **prove it before committing to the full source list.**

## Proof-first sequencing (don't build it all before it's proven)

- Prove the integration + proc + COPY on **one plain-CSV source** end-to-end first.
- Then spike the **zip path on CFPB** (the source that actually failed) before wiring the rest.
- Only then batch the remaining big sources.

## Decisions / notes for Chris

- **Security:** the integration opens egress only to the listed government data hosts, ACCOUNTADMIN-owned, scoped by network rule — low risk. Listed for visibility, not a blocker.
- **Cost:** proc runs on COMPUTE\_WH (X-Small, \~1 cr/hr); a 1.4 GB pull is minutes. This is the one-time sprint cost you approved.
- **Reminder:** revert `.env` to the reader token after the sprint; the write token is ACCOUNTADMIN.
- **GLEIF is doubly special:** its URL needs a JSON-resolver hop (302 → metadata JSON → real download link) *and* it's XML/CSV-golden-copy — handle after the CSV+zip paths work.

## Reversibility

Every new object (network rule, integration, stage, proc) is independently `DROP`-able; landing stays atomic (staging + swap), so a failed server-side load never touches a live table.
