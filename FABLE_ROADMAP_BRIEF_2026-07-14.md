# FABLE MISSION PACKET — Plan the Road (2026-07-14)

*v2 — hardened after an adversarial stress-test (5 lenses + live fact-check). Hand this whole file to a Fable session. See RUN CONTEXT below — this is not a "paste into any window" job.*

---

## ⛔ PRECONDITIONS — read before anything else

**RUN CONTEXT (hard):** Run this as a **local Claude Code session, model set to Fable (`/model fable`), started from the root of Chris's working tree.** This brief, `AUDIT_2026-07-14.md`, and the Constitution rewrite are **uncommitted / untracked**. A clone, cloud run, or CI checkout will read the WRONG files. First thing you do: run `git status`. If it does not show `FABLE_ROADMAP_BRIEF_2026-07-14.md` and `AUDIT_2026-07-14.md` present and `CLAUDE.md` modified, you are on the wrong checkout — **STOP and tell Chris.**

**CONSTITUTION TRIPWIRE (hard):** Open `CLAUDE.md`. Its first line **must** read `# Ripple — Operating Constitution`. If it instead reads `# CLAUDE.md — Ripple Library Onboarding Agent`, you are looking at the **stale committed manual** (opposite mission: "foreman," six checkpoints, no honesty doctrine, no lanes). **STOP, flag it, do not plan.** (Chris: committing the Constitution — `AUDIT §B.3`, "the single next thing" — is a precondition for this handoff.)

**PLAN, DON'T BUILD:** Produce a roadmap document. **Do not build, run, load, migrate, or mutate anything.** Read-only and plan-only.

---

## ROLE

You are a senior product architect and strategist. Think as deeply as you can before writing. Your job: plan **what Ripple could become**, and the road from where it is today to — at minimum — a **personal, self-serve exploration UI** Chris can play in like Power BI.

You are **NOT** here to change the mission, relitigate settled calls, or hunt new data patterns. You **add to, polish, and sequence** what already exists. You are the recon/hunting worker doing a thinking-worker's job — so treat this as a **verification task, not an essay**: every current-state claim must trace to a file you read or a query you ran. Anything you can't trace, label **PROPOSED** — never state it as fact. A full current-state audit already exists (`AUDIT_2026-07-14.md`); build on it, don't redo it.

---

## FIXED LAW (design within it — do not challenge)

1. **The Constitution** (`CLAUDE.md` — read in full *after* the tripwire above passes). In short:
   - **Mission:** map systemic patterns across public data to expose hidden harm to people. **THE MAP is the deliverable.** A single story is only a *pin* proving the machine works — "pick one lead and publish it" is explicitly NOT the goal. The question under everything: *who gets hurt, and does the data show it?* No human on the other end of the number → it's trivia.
   - **Three lanes:** GREEN (pure build, silent) / YELLOW (real technical call, one-line receipt) / RED (Chris's taste calls: mission, scope, whether anything publishes, money, legal/ethics).
   - **Honesty doctrine:** facts (shared hard government ID) vs leads (shared name only — never treated as true); **human sign-off on every finding; auto-publish structurally blocked; AI is a build-time tool, not a runtime dependency.**
2. **Stack is non-negotiable:** Python, Snowflake, dbt, Plotly. Never propose anything outside it — no BI SaaS, no new warehouse, no non-Plotly viz.
3. **Operating model:** Chris is CEO; agents do the labor; he has a day job. His hours are the one resource that doesn't scale — every plan must respect that.

---

## GROUND YOURSELF FIRST (verify — do not plan from the prose numbers below)

**How to query (read-only):** the `RIPPLE_READER` PAT lives in `library-onboarding/.env` (warehouse `SERVE_WH`). Run SQL via `viz/sqlrun.py` or a `library-onboarding/snow.py` `connect()` snippet.
**GROUNDING RECEIPT (required):** start your roadmap by pasting the exact `V_STATE` rows you pulled + timestamp, and cite a file path or query for every current-state number you use. **If any query fails or the warehouse is unreachable, write `GROUNDING FAILED — WAREHOUSE UNREACHABLE` at the top, mark every current-state number UNVERIFIED, and do NOT silently reuse the prose numbers in this packet as if you confirmed them.**

**Read:** `CLAUDE.md`, `AUDIT_2026-07-14.md`, `build-state.md`, `STRATEGIC_REVIEW.md`, `PROJECT_SHAPE.md`, `OVERVIEW.md`, `connect/README.md`, `viz/README.md`, **`serve/README.md`, `serve/app.py`, `serve/serve_workbench.py`, `reading_room/README.md`, `reading_room/app.py`**, and skim the `evidence/` scaffold.

**Query live:** `LIBRARY_META.REGISTRY.V_STATE`, `REGISTRY.CATALOG`, `REGISTRY.V_DOMAIN_SUMMARY`. **Prose rots — V_STATE wins.** (Mart/staging/evidence-page counts are NOT in V_STATE — re-derive them yourself from `INFORMATION_SCHEMA` and the repo before sizing any phase.)

**Current facts to verify, not trust:**
- **The core loop — review → decide → publish — has never once run. 0 human decisions ever, 0 published.** (Verified.)
- **The health concentration is in the ANALYTICAL layer, NOT the data.** The connect spine is ~98% NPPES/NPI and ~1,009 of 1,030 leads are LEIE health hits — *but the raw ~285M-row library is already multi-domain*: money-in-politics is a live, merged domain (FEC itcont firehose built) and rivals/exceeds health **by rows** (~politics 30% vs health 20% at last live read — re-verify). **This concentration comes from the pipeline, not the library:** the entity index is fed by only ~15 ID-bearing tables (NPPES alone ≈ 89% of it) and detectors read only LEIE. So *widening the map is mostly GREEN/YELLOW BUILD* — extend the spine feed beyond NPPES, point detectors at already-landed politics/spending/transport marts — **NOT net-new acquisition.** "Census of all power" is the mission; a healthcare engine is the shape of the spine + detectors, not the data.
- **Staging surface:** ~844 `stg_` models sit un-marted — but **most are first-class federal sources** (CMS NPPES, FEC, DOL Form 5500, EPA ECHO, SEC EDGAR) cast to TEXT with no mart on top — **un-modeled high-value data, reuse fuel, NOT scrape junk.** (~58 mart models, 906 dbt models total; re-derive.)
- **The write lane isn't provisioned:** no `REVIEW` schema, `LEAD_QUEUE` mart not built, `V_LEADS_PUBLISHED` still joins the retired 0-row `CONNECT.DECISIONS` (`AUDIT §B.1`).
- **Surfaces that ALREADY EXIST (reuse, don't reinvent — verify each):**
  - **`serve/serve_workbench.py`** — "The Workbench: ask ANY question, get a chart," a thin Streamlit shell over `viz/*`. **This is already a point-and-click chart builder — the closest thing to the north star.**
  - **`serve/app.py`** — a shipped 4-view SERVE app (Search / Entity Dossier with live cross-domain threads over the 9.8M spine / Connection Graph / Source), already role- and `SERVE_WH`-locked.
  - **`reading_room/`** — the shipped review→decide UI over the ~1,030 leads (append-only two-lane writer, air-gapped from AI), blocked only on the write-lane provisioning above.
  - The **Investigator Instrument** (`ripple chart "<SQL>"` → editable Plotly + a committed `.py` "card" in `investigations/`) and the **guarded read lane** (`viz/sqlrun.py`, which badges name-only joins `[LEAD]` and refuses raw `CONNECT.LEADS`).
  - **evidence.dev** — 252 pages scaffolded (confirmed), build count unverified and undeployed — **treat as scaffold-only.**

---

## THE DESTINATION TO PLAN TOWARD

**Near-term north star (must reach at minimum): "Power BI for the Library" — a personal, self-serve exploration UI.** Concretely:
- Chris picks **measures and dimensions** and **builds/tweaks Plotly visuals interactively** (swap the measure, change grouping, add a filter, change chart type), **cross-filters, drills down**, and **saves/names views**.
- Reads **live off the marts through the safe read lane**. It is **for Chris to think with** — his private instrument, not a public product.
- **READ-ONLY: no publish button, records no decisions.** A saved/named view is a private thinking artifact, never a published finding. Publishing ALWAYS routes through the human-sign-off review lane (`REVIEW.DECISIONS`) — the UI must never become a shortcut around it. "Private instrument" is **not** an exemption from the honesty firewall.
- **No LLM in the query path.** Self-serve here = point-and-click over a governed measure layer → SQL → Plotly. **No natural-language-to-SQL box, no "ask in English" copilot, no AI in the render loop.** AI designs measures at build-time; it never sits in the runtime path (§7).

**The ceiling (sketch the arc):** what Ripple could become beyond the personal UI — the map as a public investigative instrument, the honesty engine as the differentiator, the portfolio/journalist payoff. As the map goes public, the auto-publish block and human-sign-off gate become **MORE** binding, never less — sketch the public instrument as gated on Chris's RED publish calls. Draw the near-term UI as a *step toward* the ceiling, not a detour.

---

## THE HARD PART — design it explicitly

How do you get genuine self-serve exploration out of **Python / Snowflake / dbt / Plotly**, **reusing what's already built**? Reason hard here — it's the crux.

- **Start the analysis FROM `serve/serve_workbench.py` + `serve/app.py` as the prototype to EXTEND.** "Reuse" means extending existing code, **not** merely reading the marts from new code. A greenfield Streamlit/Dash proposal is **out of bounds unless you first show why the Workbench cannot be extended.** Explicitly decide how the new UI, `serve/`, and `reading_room/` relate (one grows into the others / they merge / one is retired) — note that `serve/app.py` and `reading_room/` both call themselves "the Reading Room," so reconcile the naming too.
- **Measure layer — evaluate, don't assume.** The Constitution's marts are already "final, analytics-ready, wide, denormalized." So weigh: does this warrant a full **semantic-metrics layer** (dbt metrics / Python registry), or do the marts **already ARE the measures** and need only a **thin governed wrapper**? One-person maintenance cost is a first-class criterion. The layer must be **domain-agnostic** (new harm-classes plug in without a rebuild; never hard-code healthcare as THE spine), and its headline measures must **foreground who-gets-hurt / exposure / concentration** — a generic pivot-table with no harm lens is trivia by §1, even privately. State plainly that **v1 is bounded by today's ~58 marts (mostly health + politics)** — don't oversell census-wide self-serve.
- **Cross-filtering substrate.** The marts are deliberately *wide/denormalized — the opposite of a star schema*. Name the **conformed dimensions** that make cross-filtering possible: the **connect entity spine** (9.8M entities, already resolving cross-domain threads in `serve/app.py`'s Dossier) + **`JOIN_KEYS_STD`** (FIPS/EIN/NPI/CIK/IMO/…) + time. Call out the wide-mart-vs-star-schema mismatch and how you bridge it — don't assume cross-filter is free, and don't reinvent the spine.
- **Honesty at the measure level, not just the read lane.** `viz/sqlrun.py` classifies SQL *text* — a measure with a name-only join buried upstream defeats it. Every measure/dimension must carry a **fact/lead provenance flag**; a user-composed measure **inherits the WEAKEST provenance of its inputs** and fails closed to `[LEAD]`/`[UNVERIFIED]`; the layer **refuses to compute a single scalar that blends fact rows and lead rows.**
- **Performance/budget as an acceptance criterion.** The UI must live inside **`SERVE_WH` (X-Small, 5 cr/mo hard cap via `SERVE_MON`)**. Interactive cross-filter fires many queries — specify which marts are small enough to hit live and where **pre-aggregated, dimension-keyed "UI-summary" marts** are required. A tool that can suspend or drain its own warehouse mid-session is out of spec.
- **Persistence & hosting.** Reconcile save/name-views with the existing committed-**card model in `investigations/`** — don't invent a third store. Make hosting an explicit design task using `serve/README`'s documented **local-Streamlit v0 → Streamlit-in-Snowflake Phase-2** path, so the public ceiling is a *promotion, not a rebuild*.

Give **options → Pro / Con / Best-if → a recommendation**, with reuse and one-person maintenance cost front and center.

---

## CONSTRAINTS THE ROADMAP MUST HONOR

- **Closing the loop once is a HARD GATE — it is Phase 1.** ONE **harm-anchored, human-signed-off** pin recorded in `REVIEW.DECISIONS` and surfacing through a *fixed* `V_LEADS_PUBLISHED`. The UI may be **designed** in parallel but **must not be declared usable by Chris until the loop has closed once.** Any sequence that ships the UI before the first pin is wrong by construction.
- **Don't bank on the one existing finding.** The SBA 7(a) fee-cliff (`SYSTEMIC_FINDING.md`) names no harmed human ("Nothing about this loan is improper — that is the point"). Under §1 it may be **trivia, not a lead** — `AUDIT §A.2` puts "does it clear the harm bar?" on Chris as a RED call. Plan for producing a **fresh** harm-anchored pin; surface SBA as a RED decision, don't assume it qualifies.
- **The honesty firewall survives into every surface** you propose (measure-level provenance + read-only UI, above).
- **No new SaaS, no runtime AI dependency, preview-then-apply on every warehouse mutation.**
- **Widening the map is Chris's RED call only on WHICH harm-classes to light up first** — not whether the data exists (it does). Frame it that way.
- **Don't add durable runtime surface** (a standing app, new scheduled jobs) until the operability gaps — heartbeat install, DR/backup of the 284M-row warehouse, dbt live-build CI (`AUDIT §D`) — are addressed or explicitly accepted as risk by Chris. Any design whose steady-state upkeep exceeds a day-job owner's spare hours is disqualified.

---

## OUTPUT (write it to `ROADMAP_2026-07-14.md`)

Lead the document with a **one-screen, 60-second decision summary** Chris can read first. Then:

1. **"What this could be"** — the polished ceiling vision, 1–2 tight paragraphs, plain words.
2. **The road, phased.** For EACH phase: one-line goal · what gets built · what it unblocks/proves · dependencies · **size split into (a) Chris-only RED hours and (b) agent GREEN/YELLOW sessions — never one blended number** · **steady-state upkeep in Chris-hours/week** · a **checkable DONE** (a warehouse condition where possible, e.g. closed-loop DONE = `decisions.total ≥ 1` AND `V_LEADS_PUBLISHED` returns a signed-off row) · the **RED decisions it forces on Chris.** Phases chain: **today → close the loop (Phase 1, hard gate) → personal exploration UI → toward the ceiling.**
3. **The self-serve UI architecture recommendation** — the hard-part analysis above, options with a take.
4. **Sequencing logic** — why this order, 5–8 bullets. Name what gets PARKED — **but anything you park that touches mission scope, map breadth, money, DR/trust-of-the-data, or what publishes is a RED decision: surface it in "Open questions for Chris," do NOT resolve it yourself.** Sequencing may only park pure-build ordering.
5. **The first two weeks** — concrete starting moves, split by lane: agent GREEN/YELLOW vs. **Chris-only RED** (e.g. the ~1hr Snowsight write-lane provisioning that currently blocks the loop, and committing the Constitution).
6. **Open questions for Chris** — only genuine taste-calls. No rubber stamps.

---

## STYLE

- Final summary to Chris in **bar-words**: plain, direct, map not essay, every option carries a recommendation.
- **Flag every assumption.** Distinguish what **EXISTS** (verified with a receipt) from what you **PROPOSE.**
- The scope law cuts against **both story-drift AND trivia-drift**: the mission does not shrink to "one nice story," and a self-serve tool must not become a beautiful trivia generator. Every measure should be able to answer *who this could show is getting hurt* — not just be an easy metric. If a phase starts drifting either way, stop and zoom back out.
