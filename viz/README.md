# The Investigator Instrument

Ask the Library a question, get a **real, editable Plotly chart** back in seconds.
Any table, any domain, live off the catalog — nothing pre-decided, nothing hardcoded.

```
python ripple.py chart find opioid          # what's chartable about opioids?
python ripple.py chart profile <fqn>        # which columns can be axes?
python ripple.py chart "SELECT state, COUNT(*) FROM ... GROUP BY 1"
```

That last command runs your SQL (read-only), auto-picks a chart, writes a **card**,
and opens the chart in your browser.

## The card — where the loop lives

Every question becomes `investigations/<slug>_<date>/qNN_<name>.py`:

```
edit the SQL or plug kwargs in the card  ->  python <card>  ->  F5 the browser tab
```

- The card is **committed**; the `.html` next to it is regenerated and gitignored.
- Same slug + name = the card is **overwritten** (iterating one question doesn't
  scatter 15 files). `--new` forks a fresh card.
- `ripple chart last` re-runs your newest card.

## The learning ramp (how you actually learn Plotly)

| week | what you type | what you're learning |
|------|---------------|----------------------|
| 1 | `plugs.bar(df)` | nothing — inference picks x/y |
| 2 | `plugs.bar(df, x="STATE", y="TOTAL")` | the mapping |
| 3 | `plugs.bar(df, color="PARTY", log_y=True)` | **any plotly.express kwarg passes straight through** |
| 4 | `ripple chart eject <card.py>` | the plug's real px/go source is inlined into YOUR card — tune it line by line |

The plugs themselves live in [plugs.py](plugs.py) — short, readable, real Plotly.
`bar line area scatter hist heatmap choropleth_state treemap big_number table`

## Discovery — live, never a list

- `ripple chart shelves` — domains by real data volume (CATALOG + the mart arm)
- `ripple chart find <term>` — sources AND typed marts (incl. marts CATALOG can't
  see, like the POLITICS suite); sampled data is badged, not hidden
- `ripple chart cols <fqn>` — any table, metadata-only (no warehouse spin-up)
- `ripple chart profile <fqn>` — chart-roles per column; works on all-TEXT landing
  tables (all-digit strings are numeric, never dates)
- `ripple chart cast <fqn>` — drafts the casted SELECT for a landing table

A source that lands tomorrow is chartable tomorrow. Zero wiring.

## The rules (built in, not optional)

- **Read-only lane.** SELECT/WITH/SHOW/DESCRIBE/EXPLAIN only; one statement;
  no SYSTEM$/CALL/TO_QUERY. `ripple chart budget` shows the lane. Until you run
  [scripts/instrument_snowflake_setup.sql](../scripts/instrument_snowflake_setup.sql)
  it says so, loudly — enforcement is verified at connect, never assumed.
- **Facts vs leads.** A name-only join badges the chart `[LEAD]`. A raw read of
  `"CONNECT".LEADS` is refused — query `V_LEADS_PUBLISHED` instead, or pass
  `--unsafe-claims` and wear the badge. Anything the classifier can't parse
  fails closed to `[UNVERIFIED]`. It never certifies "fact".
- **Honest charts.** Neutral noun-phrase titles, a "data as of" stamp when the
  result carries one, one axis (no dual-axis, ever), validated colorblind-safe
  palette, >8 categories fold to 'Other'.
- **Budget.** SERVE_WH (its own monitor-capped lane — live numbers via
  `ripple chart budget`, never prose) when it exists, else COMPUTE_WH. Never the
  pour warehouse. Every run prints the budget line. Results capped at 10k rows
  (`--limit` raises it) and 2M cells.

## Asking in plain English

Open a Claude Code session in this repo and ask in your own words — Fable drafts
the SQL, shows it, you say go, `ripple chart` renders it. The session IS the NL
layer; a standalone `ripple chart nl` is a v1.1 candidate (see the handoff doc).
