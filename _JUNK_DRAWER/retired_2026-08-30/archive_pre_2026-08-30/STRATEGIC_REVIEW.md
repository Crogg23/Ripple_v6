# STRATEGIC REVIEW — Ripple

**Date:** 2026-07-13
**Written by:** an outside reviewer handed the whole operation cold, asked to tell the truth.
**Written for:** Chris.

**Method.** I did not take anyone's summary on faith, including the repo's own. I read CLAUDE.md, README, OVERVIEW, the founder doc, the design brief, the 2026-07-12 handoff, the 2026-07-12 govern recon, the 2026-07-13 library snapshot, and build-state.md; walked the git log and all 24 branches; and ran a **read-only live query against the warehouse this morning** (V_STATE, V_BUILD_STATE, and the PAT population, 2026-07-13 ~10:56 PDT). Where a doc and the warehouse disagreed, the warehouse won. Where I couldn't settle something, it's flagged in the "What I couldn't settle" section instead of reported as fact.

---

## The picture in one table

The whole assessment hangs on this funnel. Every number verified live today:

| Stage | Count |
|---|---|
| Datasets scouted into the catalog | 2,840 |
| Physical landing tables (incl. portal churn) | 1,784 · 284.8M rows |
| Sources actually landed + modeled (the real library) | 200 |
| Connection edges | 41,101 (trustworthy core ~4,308) |
| Active investigative leads | **1,030** |
| Human decisions ever recorded on a lead | **0** |
| Findings published, anywhere, ever | **0** |

Twenty-seven days of building. A genuinely working acquisition engine, a genuinely clever connection engine, a calibrated entity-resolution ladder that most funded data teams don't have — and **not one lead has ever been reviewed, and not one finding has ever reached a reader.**

That's the review. Everything below is detail.

---

## 1. Scope vs. capacity — is this sane?

**The platform is sane scope. The way it's being operated is not.**

The core loop — scout → collect → connect → review → publish — is a solo-viable product *because* the agents do the labor. That part of the thesis holds up. The engineering quality is real: I went in skeptical of the repo's self-congratulation and came out mostly agreeing with it. The confidence ladder is honestly calibrated (measured out-of-sample precision, not model-reported confidence). The catalog audits itself. The fact-vs-lead line is structurally enforced — I verified the libel firewall refused a raw `LEADS` read on the reader role. This is not a prototype held together with tape.

What's not sane is the number of simultaneously open fronts. Here's the honest inventory:

| Front | State | Idle since |
|---|---|---|
| Onboarding/pour engine | Working, paused | — |
| Connect graph + entity ladder | Built, calibrated, **unused for its purpose** | — |
| Detectors (6 live, 1,030 leads) | Waiting on review that never comes | 2026-06-28 |
| Politics domain (6-phase runbook, epic #44) | Plan-stage, P1–P5 unexecuted | 2026-06-30 (~2 weeks) |
| evidence.dev serve layer | Built, **dark** (dead token, credential swap undone) | 2026-07-06 |
| Reading-room review app | Shipped, blocked on provisioning (write PAT, A13 mart) | 2026-07-12 |
| The Plane (warehouse explorer) | v0, unfinished, fully spec'd | 2026-07-04 |
| Frontier backlog | 137 datasets scouted, none decided on | 2026-07-01 |
| Lead hunt results (8 verified leads) | Sitting in a markdown file | 2026-07-08 |
| Detector calibration battery | **New front, opened yesterday/today** | active |
| Library snapshot tool | **New front, opened today** | active |

That's the pattern you described — "loses track of the whole system every time he sits down" — made visible. It's not disorganization. It's that **each session opens a new front at roughly the rate of one every 2–3 days, and closes one at roughly half that rate.** The cost of a new front isn't build time (agents make building cheap). It's that every front deposits pending actions, defects, credentials, and apply-scripts that only you can clear — and your hours are the one resource that doesn't scale.

**Nothing needs to be killed.** But most of this needs to be *formally parked* — moved to the PARKED table you now have, with a written re-entry condition — rather than left ambient, where each one quietly taxes every session's startup.

And one thing needs to be said plainly: the detector-calibration work merged yesterday and today (PR #48) is new detector work, and your own standing policy from 2026-06-29 (`foundation_before_detectives`) says no new detector work. Either the policy changed and nobody updated it, or this is exactly the riffing pattern operating against your own written rules. I'm not scolding — the work looks good — but a policy you override silently isn't a policy, it's a mood.

---

## 2. The real bottleneck — visibility, or decision throughput?

I checked the numbers before answering, as instructed. **It's decision throughput, and it isn't close.**

The evidence:

- **1,030 active leads, 0 decisions, 0 published** — live today. The `DECISIONS` table has existed since 2026-06-25. It has never held a row.
- **8 hand-verified, receipt-backed leads** (the 07-08 hunt — EOIR detention-of-the-lawyered, the H-1B cliff, etc.) — some of the strongest material the platform has produced — parked in `outputs/LEADS_2026-07-08.md` with no next step.
- **The 9-script apply queue built 07-07 sat untouched for 5 days**, then — when the govern build turned it into an explicit, dependency-ordered, small queue — you cleared 10 items in one session (07-12). That's the single most instructive data point in the whole history: **when the decision queue is explicit, bounded, and ordered, you clear it fast.** When it's ambient (1,030 leads, 137 frontier datasets, 20 defects), you clear none of it.
- The funnel ratio: 2,840 scouted → 200 landed → 1,030 leads → 0 decided → 0 published. Every stage upstream of "decide" is overbuilt relative to the stage below it.

Here's the part that matters for how you spend the next month: **the visibility work wasn't wasted — it was the prerequisite — but it's done now.** V_STATE, the BUILD registry, the defect ledger, the generated build-state, the snapshot tool: that's more operational self-awareness than most seed-stage companies have. Another instrument will not move `decisions.total` off zero. Only you, sitting down and deciding things, moves it — and the honest sub-point is that 1,030 leads is not a reviewable queue for a human with a day job. Even at 5 minutes each that's ~86 hours. The reading room's `LEAD_QUEUE` triage mart is the right fix and it shipped yesterday — **and it's blocked on about an hour of provisioning only you can do** (mint the write PAT, run the A13 mart build). The bottleneck's bottleneck is a Snowsight session.

---

## 3. Technical debt — normal mess, or compounding?

**Mostly normal-for-stage, unusually well-inventoried, with two exceptions that compound and one that could end the project.**

Normal and fine (don't spend attention here):
- 233 orphan objects in dbt databases, 11 deliberately disabled models, 21 declared-never-built, restore artifacts, stale HTML viz pulling Plotly from a CDN. This is what a 4-week-old warehouse looks like. The flags list in the snapshot is honest about all of it.
- Doc-number rot — actively neutralized by the `v_state_numbers_only` policy and the generated build-state. Genuinely better handled than at most real companies.
- The 41k-edge graph being 52% bare-ZIP noise — quarantined by the tier system; `V_CONNECTIONS_CORE` (4,308 trustworthy edges) now exists. A design call, not decay.

Compounding — will bite in 3–6 months if untouched:
1. **The all-TEXT staging debt grows mechanically with every pour.** 819 of 1,033 staging views are 100% TEXT, and it got *worse* between the 07-06 audit (789) and the 07-12 recon (819). 99 of 199 landed sources have no staging view at all. Every new source you land adds to this pile. The deterministic generator exists; rerunning it is cheap now and expensive after another 500 sources. This is the one debt with a real interest rate.
2. **The empty-load gate holes keep letting junk in.** 49 landing tables at 1–3 rows, 8 junk sources still reading `landed`, and the `_reject_html` / density gates have known, documented holes that remain unfixed. As long as pours continue, the catalog keeps ingesting lies it later has to be cleaned of.

The existential one:
3. **Credentials.** Good news first, verified live this morning: the leaked ACCOUNTADMIN token (`THE_LIBRARY`) and the unrestricted `Ripple_v6` token are **gone** — revoked. That was the fire. But: the only remaining write lane is still an ACCOUNTADMIN token (`LIBRARY_PAT`), two straggler loader tokens on the revoke list are still active, no scoped write role PAT exists, and `RIPPLE_REVIEW_PAT` (which the review app requires) has never been minted. This project has already lost a database once (the old MCP host went down with `DISASTER_IMPACT`). A warehouse whose every write runs as ACCOUNTADMIN, operated by agents, at midnight, alongside a day job — that's the one debt class where the downside isn't "cleanup," it's "start over."

---

## 4. The operating structure — does "Chris decides, Claude executes" fit?

**Yes — and you should notice that you already built it.** The foreman model, preview/`--apply` on every mutation, `agent_never_closes_defects`, the BUILD registry with DEFECTS/ACTIONS/PARKED/POLICY tables, the generated build-state — that *is* the chief-of-staff + engineering + operations split, codified and live as of 07-12. The sketch you and your collaborator have been drawing this session isn't a new structure. It's a description of what shipped two days ago.

So here's the honest warning instead: **the risk isn't that the structure is wrong — it's that you'll respond to this review by building more structure.** Look at the trail: build-state generator, control panel, dashboard, heartbeat, govern registry, snapshot tool, and now a commissioned strategic review. Each individually good. Collectively, they're the riffing pattern applied to the tracking problem itself. Meta-work feels like progress because it produces artifacts, but `decisions.total` is still zero. The structure doesn't need another component. It needs to be *used*, on a cadence, with a WIP limit.

What I'd actually change — process, not tooling, all of it using what exists:

- **A WIP limit of two open fronts.** One primary, one background. Opening a third requires parking one first — in the PARKED table, with a re-entry condition, out loud.
- **Every session opens from the registry, not from an idea.** `python3 scripts/gen_build_state.py`, read NEXT ACTION, start there. The idea that arrived in the shower goes to PARKED before any code gets written. (Your CLAUDE.md already specifies exactly this ritual. It's the most-ignored section of the file.)
- **A standing "foreman day" — one session a week that builds nothing.** Only: clear pending actions, close or re-verify defects, review leads from the triage queue, approve/reject parked ideas. The 07-12 drain proved this works when the queue is explicit; make it a rhythm instead of a one-off.
- **Registry rows get closed in the same session the work happens.** Yesterday's drain revoked the leaked tokens but left A00/A03 showing pending and the blocker defect ambiguous — one day old and the tracker already drifted from reality. The tracker only beats prose if closing rows is part of the definition of done.

A smaller version of the project? No — I wouldn't shrink the vision, and the founder doc is right that the architecture handles the real target. But I'd shrink the *active surface* hard: the Library, the connect engine, the detectors, and one serve surface (evidence.dev) are the product. Politics P2–P5, the Plane, new detectors, the frontier list, state/local — all parked with re-entry conditions, not ambient.

---

## 5. The next 30 days — the one call

**Stop widening the library. Run one grain of sand through the entire machine, end to end, in public.**

One lead → receipts → a human decision recorded (the first row ever written to DECISIONS) → published on evidence.dev with reproducible SQL and primary-source links, gated exactly the way your trust doctrine demands.

Why this call and not "drain the debt" or "land EIN/CIK to break the concentration risk":

- **Both of your stated goals — the portfolio floor and the journalist ceiling — are served only by published artifacts.** Not by warehouses, not by instruments, not by governance. A hiring manager and a reader will judge the same thing: the story and the receipts behind it. Twenty-seven days have produced zero of those, and the 28th day of infrastructure won't change that.
- **The back half of the machine has never run.** Review, the decision ledger, the publish gate, the public read lane — all built, none ever exercised in anger. You do not know they work. Every additional source landed is inventory added to a warehouse whose front door has never once opened. Closing the loop is the only move that converts the last month from "impressive repo" to "working product."
- **The critical path is short and it's almost all yours.** Finish Move 0 in Snowsight (~30 min: mint the scoped write PAT and `RIPPLE_REVIEW_PAT`, revoke the two straggler loaders, retire routine ACCOUNTADMIN writes), swap the evidence.dev credential so the read lane lights up, run the A13 triage mart, then pick the story — the Eduardo Miranda banned-but-paid case already has 3-source receipts, or EOIR Lead 1 if you want the bigger headline — review it, decide it, publish it.
- Everything else stays frozen for 30 days: no new sources, no new detectors, no politics phases, no Plane, no new instruments. The one exception I'd allow: the staging-generator rerun to stop the TEXT debt accruing, because it's deterministic and doesn't need your attention.

Definition of done, measurable in V_STATE and in the world: `decisions.total ≥ 1`, at least one lead `published = TRUE`, one public URL a stranger can read, and zero ACCOUNTADMIN tokens in routine use.

If you do nothing else from this document, do Move 0. It's 30 minutes, it's been the literal NEXT ACTION in your own tracker for weeks, and every single other thing is queued behind it.

---

## What I couldn't settle (flagged, not settled)

- **The blocker-defect row vs. reality.** build-state (generated 07-12 20:58Z) shows the leaked-PAT blocker verdict "clear" while A00/A03 still show pending. Live check today: the two flagged tokens are revoked, so the revocation happened — but the action rows were never closed and two revoke-list stragglers (`ripple_loader`, `RIPPLE_LOADER_PAT2`) are still active. Registry needs a reconcile pass.
- **Who typed the reading-room views?** The 07-06 audit measured 171/233 zero-cast; the 07-12 recon measured 3/233 — a typed pass clearly landed, but no apply record exists on disk. Undocumented mutation; worth 10 minutes to reconstruct so the preview/apply discipline stays credible.
- **Two review systems.** `connect review` (CLI, writes `CONNECT.DECISIONS`) and the reading-room app (writes `REVIEW.DECISIONS`, which doesn't exist yet). Neither has ever recorded a decision. Pick one as canonical before the first real decision lands, or you'll have two half-truths.
- **The detector-calibration work vs. the standing policy** — covered in §1; either amend the policy row or acknowledge the drift.

---

## Bottom line

You've built, in four weeks, part-time, a data platform with better honesty infrastructure than most funded teams — and you've used it to make exactly zero decisions and publish exactly nothing. The founder doc says "the genius part is done; what's left is execution." I'd sharpen that: **what's left isn't execution — the agents execute fine. What's left is the discipline of not building, so the deciding can happen.** The machine is ready. It's waiting on its foreman.

One story, end to end, in public, in 30 days. Everything else is parked.
