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

## The four folders

### 📁 `library-onboarding/` — the COLLECTOR
Give it a URL; it runs 5 steps (read the source → write fetch code → load → build dbt models → register) and
the data lands clean in Snowflake. Handles bulk files, APIs, and websites (incl. a real headless browser).
Mature. This is what filled the original Library.

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

### 📁 `outputs/` — the generated stuff
`connection_explorer.html` (the live map), plus data files and the older `trail_map`/`library_map` views.

---

## 🏢 The warehouse (Snowflake — what all this *builds*)
- **`LIBRARY_RAW.LANDING`** — the raw catch: **720 tables, ~24.3M rows** (everything stored as plain text).
- **`LIBRARY_META`** — the catalog: source registry + load logs + the 338k portal index + the connection edges.
- **`LIBRARY_STAGING` / `LIBRARY_MARTS`** — cleaned-up dbt output.
- **`LIBRARY_TOOLS`** — just hosts the read-only query connection (no data).

---

## Where things stand
- **720 datasets, 20,696 real connections** (638 datasets wired together), each confidence-scored.
- Strongest example: the federal **provider registry ↔ banned-providers list** match on NPI (8,503 exact matches).
- It's an **exploration / lead-generation** layer: it shows you *where* the stories are; pulling the full story
  (uncapping a thread, deeper analysis) is the move after.

## Read next
- **`connect/HOWTO.md`** — how to run the connection tool, step by step.
- **`build-state.md`** — the detailed running log + what's next.
- **`CLAUDE.md`** — the project's rules, stack, and conventions (the real "how we work here").
