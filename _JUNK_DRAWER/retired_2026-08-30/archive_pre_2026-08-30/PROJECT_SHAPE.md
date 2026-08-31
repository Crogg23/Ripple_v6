# PROJECT SHAPE — What Ripple Actually Is

**Date:** 2026-07-13 · Written by an outside reviewer handed the operation cold. Companion to `STRATEGIC_REVIEW.md` (which covered operational health — none of that is repeated here). This is the picture, whole, off the chalkboard.

---

## 1. The one paragraph

You built a factory that turns the open web's scattered public records into one connected map of who's-who — the same doctor, company, or ship traced by its government ID across every dataset that mentions it — with an honesty machine welded on top: every connection graded by how sure you can be, every hunch structurally walled off from every fact, every claim about the system itself audited against the warehouse instead of trusted from prose. On that map sit tripwires that catch the government contradicting itself — banned doctors still cashing pharma checks, sanctioned ships still broadcasting, debarred companies still getting paid — and they work: 1,030 story candidates are in the hopper. Underneath it all, half by accident, you built the most original thing in the repo: an operating system for one human safely commanding an AI workforce. What does not exist yet is the door. Both things this was built to earn — the credential and the byline — end with a stranger seeing something, and nothing here has ever been seen. It is a printing press, fully assembled, ink loaded, with the first page never pulled.

---

## 2. What this actually is

Strip away every component name and here's the idea. Public data is enormous and free, but it lives in thousands of disconnected boxes that don't know about each other. The ban list doesn't know the payment list exists. Ripple's bet is that **the connections between the boxes — not the data — are the product**: draw the line "this exact person is on both lists," at scale, honestly, and you've built something nobody else has. The whole system is that one bet, industrialized.

"Honestly" is the load-bearing word, and it's the part a smart stranger needs to hear to get why this isn't just an ETL pile. Every connection carries a grade — a shared government ID is a *fact* you can bet a byline on; a shared name is a *hunch* the system refuses to treat as true — and that boundary is enforced in code, not policy: the match ladder's precision is measured out-of-sample, the auto-publish path is hardwired shut, the read lane physically refuses to serve unreviewed leads, and the catalog computes what it owns from the actual tables instead of believing its own records. For a machine whose purpose is catching other people's data lying, it is unusually obsessed with not lying about itself. That obsession is the moat as much as the graph is.

The third thing this is — visible from outside, probably not from inside — is **a working model of a one-person, AI-staffed organization**. One human sets policy and approves; agents do all labor; every mutation ships as a previewable script; a registry tracks defects, decisions, and parked ideas as data. That architecture wasn't the goal, it accreted out of necessity. But it's the layer with no prior art, and it's what makes the other two layers operable by a person with a day job.

One piece of archaeology, flagged as inference: the warehouse predates this repo. Epstein-era staging views (June 12), wayback-page-change marts, an `EPSTEIN_RELEVANT` column in the registry, and the `Ripple_v5` sibling all point to an earlier life as a narrower watch-the-government-records project. Ripple_v6 is that project having discovered its general form — the strata are still visible in the rock.

---

## 3. The map — every major piece, by the goal it actually serves

**Serves both goals — the shared spine.** This is the core asset; everything else stands on it.
- **The Library + its self-auditing catalog** — the 6-checkpoint onboarding agent, portal scout (338k datasets indexed), deterministic loaders and loadkit; 200 real sources / ~285M rows landed; a catalog that computes lifecycle from physical reality and a freshness ledger that computes staleness from the data itself.
- **The trust engine** — the 6-tier connection graph (41k edges, ~4.3k trustworthy core), the hard-ID entity spine (9.8M entities), the calibrated Fellegi-Sunter ladder, and the fact-vs-lead doctrine that governs all of it.

**Serves the journalism goal.** The story machinery — built end to end, exercised only at the front.
- **Detectors + leads** — six declarative contradiction-finders, 1,030 candidates, a 3-source receipts methodology proven on the banned-but-paid flagship, plus the 8 hand-verified leads from the July hunt.
- **The publish chain** — decision ledger, libel firewall, review app, evidence.dev surface, and a complete design brief for the public face. Every link built; no link ever used.

**Serves the portfolio goal.** The written-to-be-shown layer.
- **The explanation corpus** — founder doc, design brief, plain-English pitch, HOWTOs: docs written for an eventual audience, and good enough to be the exhibit themselves.
- **The governance layer** — BUILD registry, V_STATE, defect ledger, preview/`--apply` discipline: senior-operator maturity most portfolios can't show. (It also *runs* the operating model, so it earns its keep twice.)

**Serves neither goal directly — the machine looking at itself, and the collection for its own sake.**
- **The mirror pile** — roughly a dozen overlapping ways to view the warehouse (connection explorer, leads overlay, the Plane, library map, ERD, control panel, two dashboards, Streamlit reading room, THE_LIBRARY views, snapshot, generated build-state). Each real; collectively, a habit.
- **The long tail of the Library** — ~1,580 sampled portal tables and the breadth-first acquisitions (world-issues coverage, OWID misc, historical archives) that no current detector or story can reach.
- **The politics spine** — a full parallel domain at plan stage, oriented toward analysis rather than the detector pattern; a second product living in the first one's house.
- **Vestigial strata** — the Epstein-era marts and trackers, carried forward but disconnected from either goal.

---

## 4. Where vision and reality don't match

**Tested against the build record, the two-goal hypothesis is real but incomplete.** Portfolio and journalism are both genuinely present in the artifacts — the trust doctrine is journalist-native thinking, the docs are portfolio-native writing. But the record shows a third, unstated driver that has consumed most of the acquisition energy: **the Library as an end in itself.** "The Library of Alexandria" is the emotional center of the blueprint, and the behavior matches the librarian, not the journalist: a journalist acquires backwards from a story; a librarian acquires forward from a taxonomy. The portal firehose, the 75-issue coverage sprint, the 137-item frontier list — that's shelf-filling, and it ran directly against the founder doc's own June conclusion that "the next 10x comes from a handful of identified gaps, not more crawling." The identifier gaps it named (wire EIN, fix CIK) remain unwired; the shelf kept growing.

**Both stated goals terminate at an audience, and the system has no audience-facing surface at all.** This is the single largest gap between vision and reality. The three-layer platform vision — Library, Catalog, Publishing — has zero build on layer three; the credential has no packaging a hiring manager could see; the journalism has no page a reader could load. Every one of the ~285M rows is upstream of a door that has never opened. Notably, the two goals are *not* in tension with each other — they converge on the identical missing artifact, one published receipts-backed story — the tension is between both of them and the collector instinct.

**The system's most sacred verb has never executed.** The trust doctrine calls human review "the difference between journalism and a rumor mill," the whole safety architecture exists to protect the pending→confirmed transition, and that transition has never happened once. The machinery guarding the door is more sophisticated than any traffic that has ever approached it.

**The penthouse is finished; the plumbing is bare.** A match ladder calibrated to 0.876 measured precision sits on a warehouse where 819 of 1,033 staging views are untyped TEXT and half the graph is ZIP-code coincidence. The intellectually hardest layers got built to research grade while the boring middle — typing, casting, deduplication — stayed at day one. That inversion is the signature of what was fun to build versus what the goals needed.

**The mirror pile is the chalkboard problem, made of software.** A dozen instruments for seeing the whole system, each built in a session where the whole system couldn't be felt — including, in the end, the commissioning of this document. The recurring need was never for a better mirror; the pictures were always in the repo. What kept resetting was the sitting-down-with-one.

**And the quiet strength, stated plainly because it's also part of the shape:** the honesty infrastructure is not aspiration, it's implemented — the catalog that caught its own 4-million-row lie, the numbers policy that distrusts its own prose, the firewall that refused this reviewer's read of raw leads. Whatever this project becomes, that property is rare, it is the hardest part to retrofit, and it already exists.
