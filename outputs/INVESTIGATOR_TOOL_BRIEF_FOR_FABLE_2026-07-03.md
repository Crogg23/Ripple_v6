# Mission brief for Claude Fable 5 — the Ripple Investigator Instrument

Paste this whole file as your first message in a fresh session with the model set to Fable
(`/model fable` or equivalent), run from this repo. You'll have CLAUDE.md, build-state.md, and
the full codebase in context — read them yourself rather than trusting this brief's summaries.

---

## The mission, in one line

Build Chris his own Power BI over the Library — except the "reports" don't exist yet, because
nobody's decided what's worth looking at. That decision is his to make, every time, live. And the
Library is not a fixed dataset — it grows every week (SCOUT/COLLECT never stop) — so this can't be
scoped to what's landed today. Build for a Library that's 5x bigger and more domain-diverse a year
from now, not a fixed catalog you enumerate once.

## The shape it has to take — Plotly, plug-and-play, hybrid

Chris wants to learn Plotly, not be abstracted away from it — but he also doesn't want to eat the
full boilerplate cost every time. The resolution is a **hybrid**: a library of reusable, plug-in
chart components (point a component at a query result, get a sane chart with almost no glue code)
where the actual Plotly code behind each one is visible and editable, not hidden inside a chat
response or a black-box renderer. Chris should be able to start from a plug, then start hand-tuning
the `fig = px.___(...)` or `go.Figure(...)` underneath it as he gets more comfortable — ease and
speed on day one, real fluency by week four. This is a hard requirement on the interaction model,
not something left fully open below.

## The crux — read this twice before doing anything

**This is not an autonomous-investigator agent.** Ripple's onboarding pipeline (`onboard.py`)
runs on "the agent does everything, Chris approves" — six checkpoints, Chris rubber-stamps.
**Do not build that pattern here.** For this tool, Chris drives. He asks the question, he reads
the chart, he decides what it means, he decides what to ask next. Your job is to make that loop
fast and unblocked — not to run the loop for him and hand him conclusions.

Concretely: if you build something that autonomously cross-references data and hands Chris a
finished "here's what I found," you've built the wrong thing, no matter how good the finding is.
If you build something that lets Chris ask "show me X broken down by Y" in plain English (or raw
SQL) about *any* table in the Library and get a chart back in a few seconds — with room to ask
the next question, and the one after that — you've built the right thing.

## Why now, and why not just extend `serve/app.py`

`serve/` already exists — Search / Dossier / Graph / Source, four fixed pages. That's a reading
room: good for looking up one entity you already know you care about. It is explicitly **not**
what's being asked for. Chris wants dynamic, not "let's look at these 5 things" — the ability to
point at *anything* in the warehouse and cut it a new way, session to session, without a human
(you, in a prior session, or Chris in a spec doc) having pre-decided which visuals matter.
Whether that means extending `serve/`, replacing it, or building something adjacent is your call
— see "Explicitly delegated to you" below.

## Unbiased — what that word is doing here

Your own audit (`outputs/FABLE_AUDIT_2026-07-02.md`) found that of 1,030 leads ever generated,
**1,020 (99%) ride a single pairing** — LEIE × NPI, the banned-doctor-still-getting-paid pattern.
That's not because it's the only story in the warehouse; it's because the leads engine only has
6 hardcoded rules and they're skewed toward the data that was easiest to wire up first. Don't
build this tool anchored to that same gravity well. There are 800+ landing tables across ~22
domains (money, elections, shipping, courts, procurement, environment...) — the instrument should
make all of them equally reachable, not just the health/provider slice that happens to be mature.
"Unbiased" means: don't let precedent, not even your own, decide what Chris is allowed to ask about.

## Built to grow — this can't be a snapshot

Do not hardcode today's ~22 domains, ~800 tables, or 160 `THE_LIBRARY` views into whatever you
build. Drive table/domain/column discovery **live off the catalog**
(`LIBRARY_META.REGISTRY.CATALOG` / `SOURCE_REGISTRY` / `THE_LIBRARY`'s own metadata) so that when a
new source lands next month, it shows up as something Chris can plug a chart into automatically —
not something that needs a follow-up build session to wire in. If your design has a step where a
human (you or Chris) has to register a new table before the tool can chart it, that's the wrong
design. Treat the instrument's reach as a query against the current state of the catalog, not a
list you compile once.

## What already exists — go read it, don't take my word for it

- `serve/` — the Streamlit reading room + its Snowflake connection layer (`serve_session.py`,
  reusable), plus `THE_LIBRARY` — 160 friendly views, one per domain, built for exactly this kind
  of human browsing. Strong candidate substrate, not a mandate to reuse.
- `connect/` — the leads engine (`leads.py`, 6 rules), the entity spine, `dossier.py`, the safety
  gate (`safety.py` / `leads.published()`) that enforces **same hard ID = fact, same name only =
  lead, a human confirms before anything is treated as true.** This rule is load-bearing for the
  whole platform's credibility and it doesn't stop applying just because a query is ad hoc instead
  of rule-engine-generated. Any name-only match this tool surfaces needs to look like a lead, not
  a fact, in the UI — same discipline, new surface.
- `ripple/` — the CLI front door (`ripple status`, `ripple review`, `ripple doctor`), and the
  credit/budget guardrail pattern (`scripts/budget_sprint.py`, `SERVE_MON` — a 5 cr/mo cap so the
  reading room can't drain the ETL budget). Match that discipline for whatever compute this thing
  burns.
- `LIBRARY_META.REGISTRY.V_STATE` — the "never trust prose numbers" derived-state view your own
  audit built after catching itself hallucinating headline counts. Any number this tool's UI shows
  (row counts, freshness, lead counts) should trace to something like this, not be hand-computed
  and left to rot.

## Non-negotiable constraints

- **Stack**: Python, Snowflake, dbt, Plotly. Per CLAUDE.md, this is not up for reinterpretation.
- **Read path only for ad hoc/generated queries**: whatever executes an LLM-drafted or
  Chris-typed query against Snowflake runs least-privilege and read-only (reuse or extend
  `CLAUDE_MCP_READONLY` / the `SERVE_WH` pattern). No generated SQL gets write access.
- **Facts vs. leads discipline extends here.** Non-negotiable per the above.
- **Ground truth over prose.** Any claim your build process or the tool itself makes about scale
  gets a query behind it.
- **Plug-and-play, code-visible Plotly.** Whatever surface you build, the chart the user ends up
  with is real, editable Plotly code backed by a library of reusable components — never a chart
  that only exists as a rendered image or a hidden call inside your own code. See "The shape it
  has to take" above.
- **Live off the catalog, not a fixed list.** See "Built to grow" above — no hardcoded table/domain
  enumeration.

## Explicitly delegated to you — your call, don't ask Chris to pick

- The exact authoring surface (notebook cells, a query-box-plus-plug-gallery, something else) —
  as long as it satisfies the plug-and-play + code-visible + catalog-driven requirements above,
  the concrete shell is your call.
- Whether to extend `serve/app.py`, replace it, or build a new surface alongside it.
- What "Fable assists" means mechanically day to day — SQL drafting Chris reviews before it runs,
  which plug/chart-type to suggest for a given result shape, schema/catalog search so he doesn't
  need to remember hundreds of table names, surfacing "this looks unusual" prompts he can choose
  to chase or ignore. Your judgment on the mix, bounded by the crux above: assist, don't conclude.

## Autonomy — how far to run before checking in

You've already run one big session in this repo end to end (audit → plan → 8-lens stress-test →
execution, `outputs/INSTRUMENT_HARDENING_HANDOFF_2026-07-02.md`) — multi-agent fan-out, real
commits, a handoff doc with action items at the end, no turn-by-turn sign-off on reversible work.
Operate the same way here. Scope, design, and build incrementally; you don't need Chris's
go-ahead for local/reversible work (new files, new dbt models, new Streamlit pages, read-only
Snowflake objects). Stop and flag before anything hard to reverse or costly: new warehouses/paid
infra, schema changes to shared tables, anything that'd affect the live pour or the leads safety
spine's behavior.

## What "done" looks like

Not a mockup. A live proof: Chris can sit down, ask a real question in his own words (or SQL)
about a domain nobody built a page for — money-in-politics, shipping, whatever's actually landed
— and get a chart back inside the normal back-and-forth of a session, then ask the next question
off the back of it. Prove it on at least 2–3 domains that are nothing alike, not the same
health/provider slice everything else in this repo already leans on. Then prove the "built to
grow" claim directly: land or point at one table that wasn't part of your design-time survey and
show it's chartable with zero extra wiring. Every chart along the way should leave Chris looking
at real, editable Plotly code, not a black box. Close with a handoff doc in the `outputs/` style
(what shipped, what's live in Snowflake, what Chris needs to do to turn it on) — same shape as
your last one.
