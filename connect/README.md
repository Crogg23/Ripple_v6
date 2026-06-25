# connect — the Ripple connection engine

Turns the Library's pile of landed tables into a graph of **real** connections:
which datasets actually share values on a join key (not just a key *type*), how
strongly, with a sample you can eyeball. Then renders it as an interactive map.

This exists because "these two carry an EIN-shaped column" lies. Proven on
2026-06-23: a nursing-home `NPI` column that's 100% empty; a `CCN` bridge that
was numeric noise (Alabama homes "matching" Puerto Rico drugstores). The portal
index and the trail maps both stop at key-*type* co-presence. This engine goes to
the data and measures the real overlap, so a dead key never poses as a live edge.

## Run

```bash
python -m connect all          # fingerprint -> discover -> explore (the usual run)
python -m connect fingerprint  # profile every landed table: keys + real population
python -m connect discover     # compute the real connection edge-list
python -m connect explore      # render outputs/connection_explorer.html
python -m connect probe --a FED_CMS_NPPES --akey NPI \
                        --b FED_HHS_OIG_LEIE --bkey NPI --key NPI   # one ad-hoc pair
```

Needs the live Snowflake PAT (reuses `../library-onboarding/.env` via `snow.py`).

## The entity layer (who's-who, dossiers, leads)

On top of the table-graph, a persisted entity layer in `LIBRARY_META.CONNECT`:
resolve the same real-world entity across sources, then look it up or let stories
surface. All hard-ID-only (zero false-merge); fuzzy matching is built but **gated**.

```bash
python -m connect spine          # build the who's-who: every hard ID value -> one ENTITY_ID
                                 #   + golden record (canonical name/addr) + entity index
python -m connect dossier --npi 1164450573        # every cross-domain row for an entity
python -m connect dossier --q "frank alexander"   # search by name (order-insensitive)
python -m connect dossier --id ENT_31f9… --html   # shareable outputs/dossier_<id>.html
python -m connect leads          # run lead jobs (dry-run); --run to persist LEADS
python -m connect resolve        # fuzzy person linkage (GATED preview); --write -> ENTITY_LINKS
python -m connect eval           # precision/recall of the fuzzy resolver (the merge gate)
```

| Module | Job | Snowflake table |
|---|---|---|
| `spine.py` | hard-ID entity resolution + golden survivorship | `ENTITY_MAP`, `ENTITY_GOLDEN`, `CONNECT_NODES`, `MATCH_PAIRS` |
| `entity_index.py` | per-(entity, source) projection for dossiers | `ENTITY_INDEX` |
| `dossier.py` | resolve a name/ID → cross-domain rollup (CLI / JSON / HTML) | — |
| `leads.py` (+`leads_specs.py`) | codified scored cross-domain leads; flagship = "banned but still operating" | `LEADS` |
| `resolve.py` | fuzzy name+place linkage (blocking + Jaro-Winkler), **gated** | `ENTITY_LINKS` |
| `evaluate.py` | P/R/F1 of the resolver vs hard-ID ground truth | `GOLD_PAIRS` |

**Why fuzzy is gated:** `connect eval` shows name+ZIP fuzzy matching tops out ~0.77
precision (two different "JOHN SMITH"s in one ZIP both score 1.0) — a lead generator,
not safe for auto-merge. So `resolve` only writes `ENTITY_LINKS` (REVIEW band); it never
touches the spine. Promoting links is a deliberate post-eval step.

## How it works

| Module | Job |
|---|---|
| `db.py` | short-lived Snowflake connection (reuses `library-onboarding/snow.py`) |
| `keys.py` | key detection (**reuses** `portal_recon`'s tagger) + per-key value normalizers |
| `fingerprint.py` | per table: which keys, and `populated_pct` for each (the missing half) |
| `overlap.py` | the engine: `value_overlap` (equi-join on canonical value) + `spatial_overlap` (point-in-polygon) |
| `discover.py` | run the engine over every candidate pair → `outputs/connect_graph.json` |
| `explore.py` | draw it → `outputs/connection_explorer.html` (Plotly, self-contained) |

**Trust tiers** (from the portal-recon tagger): `STEEL` (hard entity IDs — EIN/NPI/CIK/CCN…),
`STRONG` (domain IDs), `GEO` (place/spatial), `PROBABILISTIC` (name/address — fuzzy).
The explorer styles edges by tier so a clean ID join never looks like a fuzzy name match.

## Honest limits (read these)

- **Name/address joins** over tables bigger than `--name-max-rows` (default 300k) are
  **skipped and logged**, never silently dropped — multi-million-row fuzzy matching is
  slow and low-trust. Raise the flag to include them.
- **Spatial** skips point tables over 100k rows (e.g. NOAA AIS) — log says which.
- A value match is **exact on the normalized key**. It does not yet corroborate
  (e.g. same ID *and* same state). High match rate + a sane sample = trust it; a low
  rate on a short numeric key = suspect collisions (that's how the CCN noise showed up).
- Covers the **landed** Library today. The 338k-row `PORTAL_DATASET_INDEX` (potential,
  not-yet-loaded sources) is the natural next universe to point this at.
