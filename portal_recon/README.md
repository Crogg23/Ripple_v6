# portal_recon — Wave 1: platform fingerprint

**Goal:** for every open-data portal in the Catalog (`SOURCE_REGISTRY`, the ~321
"portal supercluster"), figure out **which platform it runs** — Socrata / CKAN /
ArcGIS Hub / OpenDataSoft / GeoNode / Junar / custom — so Wave 2 knows which reader
to point at each one.

**This wave does NOT harvest datasets.** Every probe is a count-only / metadata
endpoint (`limit=0`, `rows=0`, `?f=json`). Fingerprint only.

---

## Run it

```bash
# 0. fresh PAT must be live (see "Blocker" below)
set -a; source ../library-onboarding/.env; set +a

# prove the prober with zero Snowflake:
python fingerprint_portals.py --selftest

# inspect the registry's CATEGORY breakdown + which one it'd auto-pick:
python fingerprint_portals.py --distribution

# full run -> writes portal_recon_results.md:
python fingerprint_portals.py

# pin the category if auto-pick is off, or cap politeness:
python fingerprint_portals.py --category 'Open Data Portal'
python fingerprint_portals.py --budget 2
```

Output: **`portal_recon_results.md`** — summary headline + per-portal table
(`portal name | base URL | platform detected | API base URL | responded? | notes`).

---

## Blocker (as of this commit)

The `SNOWFLAKE_PAT` injected into this container is **dead** — the SQL API returns
`401 / 394400 "Programmatic access token is invalid."` The fresh PAT the task
expected at `library-onboarding/.env` isn't present (that file is gitignored, so it
never ships with a fresh clone). **Step 1 can't pull the portal list until a valid
PAT is supplied.** The prober itself is built and verified (`--selftest` = 4/4).

---

## Detection signatures (only asserted when an endpoint actually responds)

| Platform | Endpoint probed (count-only) | Confirmed by |
|---|---|---|
| Socrata | `/api/catalog/v1?limit=0` | `resultSetSize`+`results`, or `X-Socrata-*` header |
| CKAN | `/api/3/action/package_search?rows=0` | `{"success": true, "result": …}` |
| OpenDataSoft | `/api/v2/catalog/datasets?limit=0` | `total_count` / `nhits` |
| GeoNode | `/api/v2/` | `geonode` marker or GeoNode resource keys |
| Junar | `/api/v2/datastreams/?format=json` | body names `auth_key` / `junar` (401/403 ok) |
| ArcGIS Hub | `/data.json` | feed saturated with `arcgis.com` (backstop, runs last) |

Anything no endpoint confirms is **UNKNOWN** — never guessed.

## Politeness

- Short timeouts (4s connect / 6s read), **no retries**, normal identifying User-Agent.
- **Bounded reads** — every probe caps at 64 KB; we never download a full catalog.
- **Stop at first match** — a Socrata portal costs 1 request, CKAN 2, … only an
  unknown/custom portal spends the full budget.
- Budget default **6** (the six platforms). Strict "one or two requests" can't tell
  six platforms apart on custom domains; `--budget 2` reliably gets the headline
  Socrata/CKAN split but will mark more ArcGIS/ODS/GeoNode/Junar as UNKNOWN.
