# The Playground

Question-driven exploration — you write the SQL, you build the charts. The
platform's job is the **map**: pick a plain-English question and get the
tailored dictionary for its realm — the exact tables, every column
translated, the join keys with their strength, and the known data traps.
No SQL generation, no AI at runtime, nothing here can write to the
warehouse.

## Run

```
playground\run.bat        (Windows — opens http://127.0.0.1:8502)
./playground/run.sh       (POSIX)
```

Rides the same read-only lane as everything else (`SNOWFLAKE_SERVE_PAT` via
`viz/sqlrun`, which refuses any role holding write privileges).

## The loop

1. **Ask** — pick a question pack (who pays for this politician's campaign?
   did the votes follow the donors? ...). The left panel is the dictionary:
   per table, its plain-English role, live row count, key columns, joins
   (with strength badges and gotchas), traps, and every column translated.
2. Write one read-only SQL statement in the box. Run it.
3. Chart it — pick a chart type, then change x / y / color / labels / log
   scale. The chart is real Plotly; the Code tab shows the exact artifact.
4. **Save as card** — a committed, editable, re-runnable `.py` under
   `investigations/`. Saved cards has them all.

## Where things live

```
app.py            router (Ask | Saved cards)
ask.py            the main room (dictionary panel + SQL box + chart editor)
packs.py          the question packs — DATA only, edit freely, git-reviewed
dictionary.py     pure assembly of the dictionary panel (offline-testable)
queries.py        the Playground's own SQL (guard-validated)
cards_browser.py  read-only browser over investigations/
```

The per-column dictionary is `LIBRARY_META.REGISTRY.COLUMN_CATALOG`, built
by `scripts/build_column_catalog.py` (preview → `--apply`). Curated column
glosses live in `glossary/column_gloss.py` — edit there, rebuild, done. If
the catalog is empty the panel degrades to a live profile.

## The rules that don't bend

- Read-only lane, verified at connect time. One statement per run.
- Fact vs lead badges on every chart (`viz/safety`) — a name-match query
  can never masquerade as fact.
- The Senate financial-disclosure pack is **journalism use only**
  (5 USC 13107(c)(1)) — the app banners it, the registry records it, and it
  must be excluded from any commercial release, forever.
- Adding a question pack = editing `packs.py` (plain data) — the offline
  tests validate every table name against the committed inventory snapshot.
