# Ripple — what this repo is (plain English)

You're building a **data library**: software that goes out, grabs public datasets, lands them in a Snowflake
warehouse in one clean standard shape, and then finds the **real connections** between them so you can explore
what those connections reveal. The repo is the *machinery*; the actual data lives in Snowflake.

Everything maps to four verbs: **scout → collect → connect → explore.**

```
   SCOUT            COLLECT             CONNECT              EXPLORE
   portal_recon  →  library-onboarding → connect/          → outputs/*.html
   (find sources)   (load them)          (wire them up)      (walk the map)
```

---

## The folders

### 📁 `library-onboarding/` — the COLLECTOR
Give it a URL; it runs 6 steps (read the source → write fetch code → load → build dbt models → register →
wire into the connection graph) and the data lands clean in Snowflake. Handles bulk files, APIs, and
websites (incl. a real headless browser). Mature. This is what filled the original Library.

### 📁 `portal_recon/` — the SCOUT
Crawled open-data portals and built a catalog of **338,520 datasets** out in the world, tagging each by what
kind of ID it carries. Your "what should I grab next" map. Key file: `tag_portal_index.py` (the join-key tagger,
reused by `connect/`).

### 📁 `connect/` — the CONNECTOR + EXPLORER  *(built 2026-06)*
Turns the landed Library into a graph of **real** connections — datasets that actually share matching records
on a key (not just "both have an ID-shaped column"). Read **`connect/HOWTO.md`** for the dead-simple guide.
- `python -m connect all` → finds every connection, draws the interactive map.
- `python -m connect harvest --connectable --run` → bulk-loads new datasets that wire into what you have (no LLM).
- Each connection is scored 0–1 by confidence; fake/coincidental ones are thrown out.

### 📁 `serve/` — the READING ROOM
A Streamlit app for browsing what's in the warehouse without writing SQL, backed by the `THE_LIBRARY`
database of friendly, plain-named views (one topic schema per domain, `START_HERE` as the card catalog).
The human front door to everything the collector lands.

### 📁 `loadkit/` — the LOADER TOOLBELT
Shared building blocks every hand-written loader imports instead of reinventing: pre-flight gates
(token/budget checks before a long load starts), atomic staging-swap loads, durable checkpoints,
quarantining FEC parsers, reconciliation referees.

### 📁 `politics/` — the POLITICS DOMAIN BUILD
Deterministic loaders + SQL for the US-politics spine: member crosswalk, committee/FEC bridges,
campaign money. These canonical tables are Python-built; the matching dbt models only mirror + test them.

### 📁 `infra/` — the PLUMBING AS CODE
DDL for the warehouse's own infrastructure (registry tables, views, monitors) plus the scheduled
keep-alive/heartbeat configs. Exists so the stack can be rebuilt from the repo, not just from memory.

### 📁 `outputs/` — the generated stuff
`connection_explorer.html` (the live map), plus data files and the older `trail_map`/`library_map` views.

---

## 🏢 The warehouse (Snowflake — what all this *builds*)
- **`LIBRARY_RAW.LANDING`** — the raw catch (everything stored as plain text).
- **`LIBRARY_META`** — the catalog: source registry + load logs + the 338k portal index + the connection edges.
- **`LIBRARY_STAGING` / `LIBRARY_MARTS`** — cleaned-up dbt output.
- **`THE_LIBRARY`** — friendly read-only views over all of the above, for humans (what `serve/` browses).
- **`LIBRARY_TOOLS`** — just hosts the read-only query connection (no data).

---

## Where things stand
- **Don't trust counts written in a doc — they rot.** For live numbers (tables, rows, connections,
  leads) query `LIBRARY_META.REGISTRY.V_STATE` (one row per metric) or the `CATALOG` view.
- The raw catch lives in `LIBRARY_RAW.LANDING`, the cleaned marts in `LIBRARY_MARTS`, the connection
  graph + leads in `LIBRARY_META.CONNECT`, and the human-browsable face of all of it in `THE_LIBRARY`.
- The strongest recurring example: the federal **provider registry ↔ banned-providers list** matched
  exactly on NPI — a hard-ID join, not a name guess.
- It's an **exploration / lead-generation** layer: it shows you *where* the stories are; pulling the full story
  (uncapping a thread, deeper analysis) is the move after.

## Read next
- **`connect/HOWTO.md`** — how to run the connection tool, step by step.
- **`build-state.md`** — the detailed running log + what's next.
- **`CLAUDE.md`** — the project's rules, stack, and conventions (the real "how we work here").
