# Ripple — The Design Brief

*For whoever builds the publishing/visual layer. The visual identity is unbuilt and yours to invent. This brief is self-contained — start here, no other reading required.*

*(Companion doc: the founder's deep system explainer is [`RIPPLE_FOR_THE_FOUNDER.md`](RIPPLE_FOR_THE_FOUNDER.md). You don't need it to start — but its §8 and §9 hold the full data caveats referenced below.)*

### 90-second primer (everything you need to start)

- **What Ripple is:** a private map of how 720 public datasets connect, plus six "detectors" that surface where two datasets contradict each other in a way that smells like a story (banned doctors still paid, sanctioned ships still broadcasting).
- **The one concept that governs everything — fact vs. lead:** a **fact** is two records sharing the same government-issued **hard ID** (same NPI = the same doctor, certain). A **lead** is two records sharing a name with no shared ID (maybe the same person — a hunch). **Facts are publishable. Leads need a human. Never let a viz blur the two.**
- **Four data traps constrain what any viz may honestly claim:** (1) AIS = one 24-hr snapshot, **never draw a time series**; (2) same-name ≠ same person, **never merge in a viz**; (3) top-contractor rankings are *floors*, not truth; (4) LEIE's all-zero NPI = **libel risk if drawn as a confirmed fact.** (Full detail: [`RIPPLE_FOR_THE_FOUNDER.md`](RIPPLE_FOR_THE_FOUNDER.md) §8.)

## D0. The one thing to know first — your permission

**The publishing layer does not exist yet, and the visual identity is yours to invent.** No logo, no palette beyond a functional tier-color mapping (D2), no name treatment, no chosen typeface, no design system. **Greenfield. Go nuts.** Two ethos rules you must not break:

1. **Honest encoding.** Trust = connection strength, never topic. The confidence ladder (D2) is load-bearing — never draw a weak connection like a strong one.
2. **Never auto-publish a person's name.** A lead is a hunch until a human confirms it. **A lead card showing a named person at `review_state != confirmed` / `published = False` MUST visually read as INTERNAL / UNCONFIRMED** — watermark, draft chrome, no shareable URL. The `confirmed → publishable` transition is the single most ethically load-bearing state change you'll design. (See the LEAD schema in D4.)

Everything else — color, type, motion, layout, the whole storytelling surface — throw it out and reinvent it if you want.

## D1. Who is this for? (resolve this first — it drives everything)

The repo is ambiguous on purpose, so here's the call: **phase it.**

- **Phase 1 — Chris's private investigative workbench.** Dense, high-information, exploration-first. Bloomberg terminal, not landing page. **Design for this now** — the artifacts below all serve it.
- **Phase 2 — public newsroom storytelling site.** Narrative scrollytelling, one investigation at a time, citation-forward. The eventual ceiling, gated behind the safety layer being wired into output.

If you want to push toward Phase 2, the question to bring back is: *which single confirmed lead becomes the first public story, and what does that page look like?*

## D2. The visual grammar you're inheriting — including the real palette

This grammar is baked into the system. **Keep the *meaning* and *ordering* of the confidence ladder — that's sacred (it encodes honesty). The palette is yours.** Below is the *current functional palette*, lifted straight from the live files — **your starting reference, not a mandate.**

| Tier | Meaning | Current hex | What it encodes |
|---|---|---|---|
| **STEEL** | hard ID, certain | `#f4a23a` (gold/orange) | the spine — bet-on-it connections |
| **STRONG** | domain ID | blue | very likely |
| **BRIDGE** | via a 3rd dataset's key (transitive) | `#b07cf0` (purple) | reached, not direct |
| **CORROBORATED** | name + place | cyan | better than name alone |
| **GEO** | location | green | a hint |
| **PROBABILISTIC** | fuzzy name | gray | a hunch |

**The UI chrome already in the files (your reference, also overridable):**

| Role | Hex |
|---|---|
| Background | `#0d1117` (near-black) |
| Body text | `#e8eaed` |
| Flag / danger (a banned/sanctioned hit) | `#e5534b` (red) |
| Accent / link | `#4c9aff` (blue) |
| Bridge-key colors on the red-string board | NPI `#f4a23a` · IMO `#3ab0c4` · UEI `#b07cf0` |

**THE central UX challenge — name it before your first sketch:** there are **20,696 edges**, and STRONG (9,396) + GEO (5,633) = **73% of them, both weaker tiers.** Drawing everything at once is a **hairball.** The core interaction to solve is **selective tier visibility** — letting the 350-edge STEEL spine surface from the noise. The default view is overwhelming on purpose; your job is to make the signal pullable.

**Other encoding rules already in play (reinvent freely, but know them):**

- **Node size = degree (connectivity), NOT row count.** Hard-won: sizing by rows once buried everything under a few giant tables.
- **Edge width = match count** (records that actually intersect).
- **Red-string board:** detector edges, width = lead count, colored by bridge key.
- **Entity tiers** — four kinds of "thing": **provider** (NPI) / **facility** (CCN) / **organization** (EIN/CIK/UEI) / **vessel** (IMO/MMSI). A dossier picks the "golden name" by authority rank — NPPES *(the national provider registry)* rank 1 beats LEIE rank 4 when they disagree on a doctor's name.

## D3. What exists — the design surface inventory *(the NOT-built list at the end doubles as the founder's build backlog)*

Open these first. They're the starting point, not a blank page.

> **Offline reality — test this in your first 90 seconds:**
> - **`plane.html` is fully offline** — vendored `mermaid.min.js` sibling, zero external URLs. Works airgapped, on a plane, behind a firewall.
> - **`connection_explorer.html` and `leads_overlay.html` pull Plotly from a CDN** (`cdn.plot.ly`). Double-click works on any **networked** machine; they render **blank offline.** To make them truly offline, swap the `<script src>` to the **vendored `outputs/plotly.min.js`** (4.8MB, already sitting in the folder, just not wired in) — or re-render with `include_plotlyjs='inline'`.

| File (absolute path) | What it is + what it LOOKS like | State / what's wrong |
|---|---|---|
| `/Users/chrisr./Documents/GitHub/Ripple_v6/outputs/connection_explorer.html` | Plotly force-graph: 720 nodes (sized by degree, spring-layout), 20,696 edges (6 tiers), sortable edge table below. **Looks like:** a dense constellation — **a near-hairball until you filter tiers.** | **Done & usable.** ~17MB. 660/720 nodes are domain=`other` so the domain color is mostly noise. CDN-dependent. |
| `/Users/chrisr./Documents/GitHub/Ripple_v6/outputs/plane.html` | Mermaid ER explorer, 4 semantic-zoom altitudes via a relayout listener. **Looks like:** a Google-Earth orbit-to-street zoom over your warehouse, sparse and structural. | **v0, unfinished.** CARD altitude **not implemented.** No domain/lifecycle color, no search/filter. ~1.8MB + 3.6MB mermaid sibling ≈ **5.3MB delivered.** Fully offline. |
| `/Users/chrisr./Documents/GitHub/Ripple_v6/outputs/leads_overlay.html` | Plotly 2-column board. Left = flag sources (LEIE, OFAC, SAM); right = active sources (OpenPayments, AIS, USASpending); edges = detector rules, width ∝ lead count, color = bridge key. **Looks like:** a clean red-string board — 3 thin lines and one thick one. | **Done — but built 6/27.** Shows "338/353 on ONE edge" with only 4 detectors; this predates the 6/28 additions (live system is now 6 detectors, ~1,030 leads, 773 on that edge) — **re-render before relying on it as current.** Callout: NOAA AIS is an island (IMO bridge never built). CDN-dependent. |
| `/Users/chrisr./Documents/GitHub/Ripple_v6/outputs/connect_graph.json` | ~7.3MB graph-of-graphs: `{nodes:[{id,rows,domain,keys[],x,y}], edges:[{a,b,key,tier,matched,match_rate,sample[]}]}`. Cached spring positions. | **The data behind every map.** Read this directly to build anything new. |
| `/Users/chrisr./Documents/GitHub/Ripple_v6/outputs/PLANE_handoff.md` | Design spec for The Plane (v0/v1/v2). | **Read before touching the Plane.** |

*(No screenshot folder exists yet. If you want thumbnails to react to, render the three files once and drop PNGs in `docs/screenshots/` — that'd also catch the offline issue on sight.)*

**NOT built yet — this is the actual job:**

- **Lead-detail dossier card** — click a lead, see the full story: two source rows side by side, the matched key, the evidence, the score, first/last seen, review state. **Must obey the D0 publish-boundary rule** (unconfirmed = draft chrome). *No render exists yet — the lead data is in `LIBRARY_META.CONNECT.LEADS` (D4); the card is yours to build.*
- **Entity "corkboard"** — one person/org/vessel, every record about them across all sources, on one card. *A bare v0 already renders: `connect dossier --id ENT_… --html` writes a dark-themed dossier page (every source the entity appears in, plus affiliated facilities). Your job is the designed, interactive version.*
- **The Plane CARD altitude + v1/v2** — dataset profile cards, lifecycle+domain colors, search/filter/minimap.
- **The lead-review UI** — confirm/reject/retract. **CLI only today** (`connect review --id LEAD_xxx --decision confirmed`).
- **A treatment for the 82 keyless/isolated nodes** — datasets with no join keys, parked in a gutter (see D6).

## D4. The data shapes to design against

You can't lay out a card without the fields. Here they are — design against these literal shapes.

**A LEAD** (populates a lead-detail card and the gallery):
```
{ LEAD_ID, title, detector, score (0–1), bridge_key,
  evidence: [ matched source rows ], first_seen, last_seen,
  review_state ('pending'|'confirmed'|'rejected'|'retracted'|'stale'),
  published (bool) }
```
Live in `LIBRARY_META.CONNECT.LEADS`. All ~1,030 are `review_state='pending'`, `published=False` today. **Per D0: any card where `published=False` must read as INTERNAL/DRAFT, never as a finished public claim about a named person.**

**An ENTITY / dossier** (populates the corkboard):
```
{ ENTITY_ID = 'ENT_' || LEFT(MD5(key_type || '|' || val), 16),   # ENT_-prefixed, 16-hex-char truncation
  golden_name (chosen by authority rank: NPPES=1 beats LEIE=4),
  entity_type ('provider'|'facility'|'organization'|'vessel'),
  source_rows: [ every row across every source carrying this ID ] }
```
The spine resolves source ID values into **~9.68M entities (9,678,735)**, of which **~953k are multi-source** (appear in 2+ datasets) — **hard-ID only, never fuzzy-merged.** That conservatism *is* the safety guarantee made visible; the ~953k multi-source subset is the interesting set to design a corkboard around.

**A NODE / EDGE** (for any map): nodes carry `{id, rows, domain, keys[], x, y}`; edges carry `{a, b, key, tier, matched, match_rate, sample[]}`. The bbox is real geometry, **not [-1,1]:** x ∈ [-6.74, 7.82], y ∈ [-7.43, 5.47], extent ≈ 14.5. Build zoom math off that.

## D5. The Plane spec (the next deliverable)

**The Plane** is the warehouse seen from altitude — Google Earth for your data. Mermaid ER diagrams stratified by zoom. Ships offline (currently ~5.3MB once the vendored mermaid sibling is counted), no Snowflake. Four altitudes:

- **ORBIT** — join-key bubbles (NPI, EIN, UEI, IMO, FIPS…) sized by how many datasets carry them; hubs >50 degree at zoom >8×.
- **REGION** — all 638 connected datasets, STEEL/STRONG backbone lit up (zoom ~0.55× extent).
- **STREET** — viewport-culled edges, join key on hover (zoom ~0.12× extent).
- **CARD** — one dataset + its ranked neighbors, on click. **(not built — this is the deliverable).**

Hysteresis (asymmetric enter/exit thresholds) keeps altitudes from flapping at the seams. Full spec: `outputs/PLANE_handoff.md`.

## D6. Seven calls that are yours to make *(each doubles as a founder product-roadmap call)*

The most actionable content in the brief. Each has a current default — accept it or override it.

| # | The call | Current default |
|---|---|---|
| 1 | **The 82 keyless islands.** Hide at ORBIT? Gray at REGION? Show with a *reason* label ("NOAA AIS is IMO/MMSI only; IMO→OFAC bridge unbuilt")? And: are all 82 *real* islands or some falsely isolated? Worth a "show only >0 join keys" filter? | Show but gray out. No filter yet. |
| 2 | **Domain color now or v1?** 660/720 nodes are `other` (backfill not done). Ship v0 with *tier color only* (honest) and add domain later, or wait? | Tier color only in v0; domain deferred to v1. |
| 3 | **Lead-review UI: web, or Slack + Sheet?** The safety layer (DECISIONS table) is built; the surface is undecided. | Undecided — CLI only today. |
| 4 | **Dossier-card timing.** Entity corkboard in v1 (plane + dossiers + lead detail together), or Phase 2 (after leads mature)? | Undecided. |
| 5 | **Lazy vs. pre-render the Mermaid ER diagrams.** ~100ms per key. Lazy-load on click, or pre-render and cache all? | Pre-render + vendor mermaid.js locally. |
| 6 | **Lifecycle colors in v0?** 9 stubs are now trust-gated. "Solid = real / faded = empty" live in v0, or stay v1 to keep v0 strictly offline? | v1. |
| 7 | **Detector ideation — in scope?** Backlog of 37 STEEL / 39 CCN~NPI / 21 NPI edges with zero detectors. Sketch what an EIN (revoked-org), NAICS (polluter), DOCKET (regulatory), or ZIP (county-burden) detector *looks like* so engineering has templates? | Out of scope unless you want it in. |

## D7. How to run it and see real output (90 seconds)

**Fastest path:** double-click **`outputs/plane.html`** — it's fully offline, opens anywhere, zero setup. The two Plotly files (`connection_explorer.html`, `leads_overlay.html`) also double-click, **but need internet** (CDN Plotly) — see the D3 offline note to make them airgapped.

**To rebuild from live data:**

```
# one-time setup
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt          # plotly, pandas, snowflake-connector, rich, dbt-snowflake
# then set SNOWFLAKE_PAT in library-onboarding/.env

python -m connect all      # rebuild the full map → outputs/connection_explorer.html (auto-opens)
python -m connect plane    # rebuild The Plane → outputs/plane.html (reads cached JSON, no Snowflake)
python -m connect leads --job all      # print all ~1,030 leads (preview only — no writes without --run)
python -m connect dossier --npi 1164450573 --html   # entity dossier page for one provider
python3 scripts/dashboard_server.py    # live dashboard at http://localhost:8765 (insights/library/compare/connections)
```

*(Ignore `python onboard.py` — that's the ingestion CLI, not a visual tool.)*

## D8. Brand / ethos to riff on

- **Investigative journalism, accountability-first.** The voice is *we show our work.* Citations for every finding, landmines surfaced not hidden, hunches labeled as hunches.
- **Credibility through honesty.** The system admits what it doesn't know — gated fuzzy matches, pending leads, empty datasets demoted. The design should *feel* like that: trustworthy because it's transparent about uncertainty, not despite it.
- **The smells raise their own hand.** Banned, sanctioned, debarred — the detectors find the patterns; the human decides. Make a person *see* the smell in one glance, then drill all the way down to the receipts.
- **Tone + aesthetic north star.** Sharp, plain, unembellished. No marketing gloss on a libel risk; make the honest number the loudest thing on the screen. **Aesthetically this wants to feel like an editorial investigative desk or a data terminal — monospace-adjacent, evidence-forward, sharp — not a rounded consumer app or a marketing landing page.** Beyond that, go nuts.

---

**Designer — your latitude.** Start with `plane.html` open in one tab (fully offline) and `PLANE_handoff.md` in the other. Keep three things sacred: the confidence ladder's *meaning + ordering*, the fact-vs-lead boundary, and the unconfirmed-name draft rule. **Everything else — color, type, motion, layout, the entire storytelling surface — is yours to invent. Go nuts.**

*Methodology: built from a multi-agent read of every corner of the repo plus an adversarial skeptic pass over the impressive claims; every number reconciled against live repo state on `main`, 2026-06-28.*
