# Playground Study — Findings & Ideas (2026-08-01)

Full detail behind the chat brief. Two sweeps: one deep in `playground/` + `viz/`,
one across the whole platform (reading_room, connect, honesty, serve, docs).

---

## The one-sentence verdict

The Playground's *honesty engineering* (verified read lane, downgrade-only LEAD
badges, trap surfacing, reproducible cards) is way ahead of its *ergonomics* —
and the biggest thing missing isn't a widget at all: the lab can't see the map,
even though the map is the mission.

---

## Part 1 — Fix-it list (GREEN lane: I can just do these)

Ranked by pain-per-hour-of-work.

1. **Real SQL editor.** The whole loop is "write SQL," and the editor is a bare
   `st.text_area` — no highlighting, no line numbers, no Ctrl+Enter. Swap in a
   code-editor component (streamlit-ace or st-monaco). This is the single
   biggest daily-feel upgrade.
2. **Query history.** Reload the tab and everything is gone. Keep a small
   on-disk history (last ~50 queries + chart settings) with a "recall" picker.
   Cheap, huge.
3. **Click-to-scaffold.** Next to every table in the dictionary panel, a button
   that drops `SELECT * FROM <FQN> LIMIT 100` into the editor. Today Chris
   hand-types every FQN the panel is already showing him.
4. **Kill the N+1 count stall.** Each pack switch fires one live `COUNT(*)` per
   table, serially — 4–6 Snowflake round trips before the panel paints
   (`ask.py:78`, `queries.py:37-43`). Fetch in one UNION query (or from
   metadata) and cache across packs.
5. **Stop swallowing errors.** `_catalog_rows` / `_live_count` catch ALL
   exceptions silently (`ask.py:32-33, 53-54`). A dead PAT or suspended
   warehouse renders as "row count unavailable" with a misleading "rebuild the
   catalog" hint. Surface the real error.
6. **Stale-widget bleed.** Chart settings (`pg_x`, `pg_laby`, log-y) are global
   keys — switch packs and old selections silently apply to the new result.
   Key them per query.
7. **Card-save gaps.** (a) The Save button hides under the *Code* tab — move it
   up top. (b) No name input, so every save forks `q01_bar`, `q02_bar`,
   `q03_bar` forever. (c) A card can be saved even when the chart failed to
   render. (d) Cards are never test-run on save — save should execute the card
   once and confirm it works.
8. **Saved-cards room is a text dump.** The rendered `.html` files sit on disk
   and are never shown (`cards_browser.py:47-49`). Show the chart previews,
   add search, add a run button. This is where the lab becomes a *body of
   work* instead of a folder of scripts.
9. **Small stuff:** empty-SQL Run does nothing silently; truncated results get
   no badge on the chart; heatmap/treemap/choropleth slots aren't editable;
   dictionary panel can't collapse.

## Part 2 — One honesty hole (YELLOW: I'd fix it, you get the receipt)

The senate-trades legal banner triggers on a naive substring match for **one
raw table name only** — querying `POLITICS__SENATE_TRADES` (the mart the pack
itself tells you to prefer!) does NOT trigger the journalism-use-only banner
(`dictionary.py:92-95` vs `packs.py:232`). The mart is the same restricted
disclosure data. The banner rule should key off a restricted-source registry,
not a string.

## Part 3 — The big ideas (the "wow" section)

### A. Let the lab see the map ("Connections" room)
The mission says the map is the deliverable — but the Playground's entire view
of "what connects to what" is the joins hand-typed into 8 packs. Meanwhile
`connect/` holds a 22.6M-entity spine, key-tier metadata, and a cross-reference
map. **Add a third room that renders the join map**: pick any table, see every
table it can reach, over which key, at which trust tier, with gotchas — generated
from `connect` metadata, not hand-authored. That turns "8 questions" into "the
whole Library, navigable." (The old serve/ Workbench had a graph view; nothing
was carried over.)

### B. Bridge the lab and the desks
The lab and the sign-off flow never touch. Two cheap wires:
- A pack (or panel chip) pointing at `V_LEADS_PUBLISHED` and the detector
  lead tables — "what has the machine flagged in this realm?" while you explore.
- A "flag from the lab" affordance: when a query surfaces something real, one
  click files it toward the review flow instead of it dying in a card folder.

### C. Dictionary panel: show provenance and grades
Two metadata layers already exist and aren't surfaced next to tables:
honesty mart grades (`honesty/mart_grades.json` — fact/lead/unverified) and the
source registry (license, refresh cadence, staleness). The trades pack proves
license metadata matters; put grade + license + freshness chips on every table
expander.

### D. Grow COLUMN_CATALOG beyond pack tables
Today the tailored dictionary only covers the 8 packs' tables; everything else
degrades to a live profile. Run the catalog builder across all of THE_LIBRARY /
LIBRARY_MARTS on a schedule. Then a "free explore" mode (any table, full
dictionary) stops being a degraded path and the pack list stops being the
ceiling of the app's reach.

### E. Retire the zombie surfaces
Four browse/review surfaces exist: Reading Room (current), Playground (current),
Atlas/serve (legacy, still boots), Mission Control (older, still boots) — plus
evidence.dev policy with a dead token. Archive serve/ and mission_control/
(after salvaging serve's graph view for idea A). Fewer front doors = less
confusion every session.

### F. The thing that outranks all UI work
**decisions.total = 0.** ~17,300 leads sit unreviewed; the entire review →
publish machinery has never processed one real human decision. And both current
surfaces are dark pending your one-sitting Snowsight work: A15 (Pattern Desk
provisioning), A16 (COLUMN_CATALOG DDL + builds), A00 (PAT cutover). No UX
polish matters as much as lighting the pipeline and pushing one real finding
end-to-end — that shakedown cruise will surface more true UX problems than any
code study can.

## Part 4 — RED lane (your calls, not mine)

1. **Pack-only vs free-explore philosophy.** Packs-with-no-SQL was deliberate.
   Idea D adds a free-explore mode — does that fit what the Playground *is*,
   or dilute it?
2. **Retiring serve/ + mission_control** (idea E) — archival is reversible but
   it's a "what Ripple is" call.
3. **The lead-framing question** already open: "1,041 targeted leads" vs
   "17,256 leads" (94% from the one OSHA statistical sweep).
4. **Which realm gets the next packs** — where the light points is always yours.
