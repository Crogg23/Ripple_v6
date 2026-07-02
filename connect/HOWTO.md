# How to use the Connection Explorer — step by step

No code knowledge needed. You run one command, a map pops up, you poke at it.

---

## First time: the one command

**1. Open a terminal in the project.**
In VS Code: top menu → **Terminal → New Terminal**. A box opens at the bottom.
Make sure the path on the left says `…/Ripple_v6` (the project folder). If it
doesn't, type this and hit Enter:
```
cd ~/Documents/GitHub/Ripple_v6        # Mac
cd C:\Code\Ripple_v6                   # Windows
```

**1a. First clone only — install the dependencies (once).**
If this is a fresh checkout, the tool needs its Python packages (plotly,
snowflake-connector, pandas, …) before it'll run. Do this one time:
```
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt   # Mac
py -m venv .venv; .venv\Scripts\activate; pip install -r requirements.txt               # Windows
```
On later runs you just re-activate the venv: `source .venv/bin/activate` (Mac)
or `.venv\Scripts\activate` (Windows).

**2. Run the tool.** Type this, hit Enter:
```
python -m connect all
```

**3. Wait ~2–3 minutes.** It prints what it's doing — profiling each dataset,
then testing every pair for real overlap. You'll see lines like
`[edge] NPI  FED_CMS_NPPES x FED_HHS_OIG_LEIE: 8,503 matched (100.0%)`.
That's it finding a real connection.

**4. The map opens by itself** in your browser when it's done. Done.

---

## Reading the map (top half)

- **Each dot = a dataset.** Bigger dot = more rows. Color = topic (health, justice,
  money, etc.).
- **Each line = a REAL connection** — rows that actually match between two datasets.
  Thicker line = more matches.
- **Line color = how much to trust it:**
  - 🟡 **Gold = rock solid** (a hard ID like NPI, CIK, court docket). Bet on these.
  - 🟢 **Green = location** (same place / sits-inside-the-map).
  - ⚪ **Gray dotted = fuzzy** (matched on a name — could be coincidence, eyeball it).
- **Hover anything.** Hover a line → "what key, how many matched, a few examples."
  Hover a dot → its size, topic, and what it connects to.
- **Drag to pan, scroll to zoom.** Click items in the legend (top right) to hide/show
  a trust level — e.g. click everything off except gold to see only the solid joins.

## Reading the list (bottom half)

Every connection, ranked, in a table.
- **Filter box:** type to narrow it. Try `STEEL` (only the rock-solid ones), or a
  dataset name like `LEIE`, or a key like `NPI`.
- **Click a column header to sort** — click "Matched" to put the biggest connections
  on top.
- **Bottom of the page** lists datasets with *no* connection found yet — your
  candidates for "needs a bridge later."

---

## Everyday use

**You loaded a new data source and want to see what it connects to:**
```
python -m connect all
```
(Same command. It re-checks everything and redraws.)

**You just want to re-open the map without recomputing** (nothing changed):
```
python -m connect explore
```
(Instant.)

**Quick question — do these two specific things connect?** (need the column names)
```
python -m connect probe --a FED_CMS_NPPES --akey NPI --b FED_HHS_OIG_LEIE --bkey NPI --key NPI
```
Prints the match count + a sample. Keys you can pass: `NPI`, `CCN`, `CIK`, `EIN`,
`ZIP`, `FIPS`, `COUNTRY`, `DOCKET`, `NAME`, `ADDRESS`.

---

## If it breaks

- **"Programmatic access token is invalid" / login errors** → the Snowflake token
  expired (current one is good to ~**Sept 20, 2026** — expiries are tracked in
  `infra/keys_ledger.json`). Drop a fresh one into
  `library-onboarding/.env` (the `SNOWFLAKE_PAT=` line) and run it again.
- **"No module named plotly" (or pandas / snowflake)** → the dependencies aren't
  installed. Do step 1a once: `pip install -r requirements.txt` (with the venv active).
- **"python: command not found"** → you're not in the project folder or Python isn't on
  PATH. Re-do step 1 (`cd ~/Documents/GitHub/Ripple_v6` on Mac, `cd C:\Code\Ripple_v6` on
  Windows), and re-activate the venv (`source .venv/bin/activate` / `.venv\Scripts\activate`).
- **Map didn't pop open** → open it by hand — double-click
  `outputs/connection_explorer.html` inside the project folder
  (`~/Documents/GitHub/Ripple_v6` on Mac, `C:\Code\Ripple_v6` on Windows).
