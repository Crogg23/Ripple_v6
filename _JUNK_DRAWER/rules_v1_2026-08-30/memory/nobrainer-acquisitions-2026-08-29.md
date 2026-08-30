---
name: nobrainer-acquisitions-2026-08-29
description: 2026-08-29 "no-brainer" bulk acquisitions — what was ALREADY held (GLEIF Level-2, FDA NDC directory, GUDID full), what was landed (SAM public extract, USCG vessel doc, FMCSA census, EPA CAMPD), and the access quirks for each
metadata:
  type: project
---

Chris (2026-08-29): "just get me all the no brainers" — free public files that plug into ID
families the warehouse already verifies.

**Already in the warehouse before this session (my "not held" call was wrong — always check
landing tables, not just mart column names):** GLEIF Level-2 relationships (485K rows, parent
LEIs), FDA NDC directory (116K), AccessGUDID full device registry (5.2M devices / 6.8M identifiers,
columns PRIMARYDI/DEVICEID not "UDI").

**Landed via scripts/nobrainer_bulk_load_2026_08_29.py (raw VARCHAR mirror, provenance stamps,
quality gate):**
- SAM.gov Entity Management PUBLIC monthly extract V2 — UEI + CAGE + legacy DUNS + names/addresses.
  Needs SAM_API_KEY (in library-onboarding/.env); 147MB zip, pipe-delimited .dat, 142 columns,
  BOF/EOF header lines, `!end` terminator. ~895K entities.
- USCG "Merchant Vessels of the United States" (vesdoc) — official #, IMO, call sign, hull #,
  owner party. dco.uscg.mil returns 403 to every non-browser client; the Wayback Machine holds
  the monthly zips (CDX search on the Portals/9 path). Rtab release is quoted CSV, 78 fields,
  no header; layout from the ReadMe PDF (also via Wayback).
- FMCSA Company Census File — Socrata az4n-8mr2 rows.csv streaming export, 1.7GB, ~4.5M rows,
  147 cols incl. DOT_NUMBER, DUN_BRADSTREET_NO, LEGAL_NAME, PHY_* address.
- EPA CAMPD — bulk files at https://api.epa.gov/easey/bulk-files/<s3Path>; the LISTING endpoint
  needs an api.data.gov key but direct paths do not. Known-good paths: facility/facility-YYYY.csv,
  emissions/daily/state/emissions-daily-YYYY-<st lowercase>.csv (1995→2025), compliance/compliance-arp.csv.
  No annual/monthly/quarterly emissions path exists under those names. Facility ID = ORISPL = EIA plant id.

**Why:** these four each close a verified gap (94% orphaned DUNS; dead IMO/MMSI axis; empty trucking
domain; EIA plants with no emissions).

**How to apply:** re-run the loader monthly for SAM (new extract each 1st Sunday); use --uscg-url
for a newer archived vesdoc zip; CAMPD daily is checkpointed per state-year in
outputs/nobrainer_load_checkpoint_2026-08-29.json.
