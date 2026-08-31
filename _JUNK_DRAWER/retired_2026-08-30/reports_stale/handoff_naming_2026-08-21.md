# HANDOFF — one vocabulary for Ripple's thinking layer (written 2026-08-21, late)

**The mission of the next session:** Chris's words — "I want to focus on
different naming conventions of mental models etc. Or land on something
consistent. Because this is hell a complicated." The machinery now works;
the WORDS for it grew in four separate riff sessions and never got
reconciled. The next session's deliverable is ONE consistent vocabulary,
chosen with Chris (naming is a TASTE call — RED lane — so the session
proposes, Chris picks), then written into docs/RIPPLES.md and used
everywhere after.

**This is a talking session, not a build session.** No warehouse needed.
Read this file + docs/RIPPLES.md, then run the conversation. Chris thinks
in throughput/change/time and wants plain bar-words; he explicitly banned
jargon and codenames in chat.

---

## The problem, concretely: we have ~6 overlapping vocabularies for ONE machine

### Vocabulary A — "The five pieces" (Game-of-Life translation, docs/RIPPLES.md)
nouns → measurements → neighbors → ticks → **the rule**
(Chris also saw these as: the nouns / the census / the wires / the tick /
the dumb question — from tonight's animated explainer, which he liked.)

### Vocabulary B — "The formula" (tonight's chat, landed well with Chris)
LEAD = ( THING + MEASURE + NEIGHBORS + CLOCK ) × QUESTION − CHANCE
Same five pieces, different names, plus two new terms (CHANCE, LEAD).

### Vocabulary C — "The Ripples" (the three lenses, docs/RIPPLES.md)
Ripple 1 STATE (what things are) / Ripple 2 NEIGHBORS (who touches whom —
wire vs. resemblance) / Ripple 3 FLOW (when things move). A possible 4th
was floated tonight: SILENCE (the wave that should ripple but doesn't).
Note the collision: "NEIGHBORS" is both piece 3 of vocabulary A AND lens 2
of vocabulary C.

### Vocabulary D — "The flow ladder" (Boxes 0–5, inside Ripple 3)
Box 0 staleness / 1 does it flow / 2 heartbeat / 3 co-movement / 4 who
moves first / 5 where the wave breaks. Tonight's chat also called these:
the pulse, lead-lag, the pipeline, backlog, the echo, the two clocks —
SIX pictures that only partly map onto the six boxes.

### Vocabulary E — the pass/sweep names (what actually ran, in reports/)
trend sweep, lag sweep, lead-lag pass, lag-drift pass, wire-confirm pass,
neighbor-spike rule (+ region fix), wave-break traces. Ad-hoc, coined per
session, no system.

### Vocabulary F — the older strata still in the repo
detectors (the 6 contradiction-finders) / lenses (the 52-lens catalogue) /
the spine / connection tiers (STEEL, STRONG, BRIDGE, CORROBORATED, GEO,
PROBABILISTIC) / clock lanes (happened, reported, decided, span_start,
span_end, planned) / queue vs. finding / fact vs. lead (design brief).
These are load-bearing and mostly fine — the chaos is in A–E.

## The specific collisions to resolve

1. **"NEIGHBORS" means two different things** (a piece of the machine vs. a
   lens of investigation).
2. **"Ripple" means three different things** (the whole platform, the three
   lenses, and informally "a spreading disturbance").
3. **"lead" means two different things** (a queue item worth a human's
   time vs. "stream A leads stream B" in time). Both are now live in
   reports. This one bites hardest.
4. **"rule" vs "question" vs "pass" vs "sweep"** — four words for "a dumb
   question asked of everything." Piece 5 is called all four in different
   files.
5. The six chat pictures (pulse/echo/pipeline/backlog/two-clocks/lead-lag)
   vs. the six ladder boxes — near-duplicates, neither official.

## What Chris has already reacted well to (evidence for the choosing)

- The **formula** framing (one line, plus/times/minus) — he asked for it
  and built on it ("go for all" followed it).
- The **water language** — rings, ripples, "a disturbance spreading
  outward through the record." He asked the emergence page to be "more
  Ripple-y" and approved the result.
- **The nouns / the census / the wires / the tick / the dumb question** —
  bar-words versions of the five pieces, used in the approved artifact.
- He thinks in **throughput, change, effects over time** (his words) — the
  vocabulary should make the time dimension first-class, not a bolt-on.
- Landmines reframed as "wrong explanations, never forbidden data" — he
  drove that reframe himself tonight; whatever the trap-list is called, it
  should carry that meaning.

## Suggested shape for the session (adjust freely)

1. Present the collision list above in plain words, one at a time (one
   decision per message — contract 8.4).
2. For each, offer 2–3 candidate names WITH the tradeoff, let Chris pick.
   The strongest existing candidates, from his own reactions: the
   five-piece bar-words set, the formula terms, and water-words for the
   outputs (a RING = something that answered loudly; keep LEAD for the
   human-queue meaning only, per the design brief's fact-vs-lead law).
3. Write the chosen vocabulary into docs/RIPPLES.md as a short GLOSSARY
   section (that doc changes only on Chris's word — he'll be in the room).
4. Sweep the living docs (RIPPLES.md, STATUS.md template, future report
   titles) to the chosen words. Do NOT rename code/files/tables — real
   names live in files and stay stable; this is about the words used in
   chat, docs, and thinking (contract 8.3 already bans codenames in chat).
5. Park a tally of anything that needs a rename beyond docs; that's a
   separate (cheap, GREEN) cleanup session.

## Context you'll need (receipts, not homework)

- `docs/RIPPLES.md` — the thinking model this glossary lands in. Two
  pending edits Chris hasn't ruled on: the 5th landmine (inspector
  scheduling — now MEASURED: it was ~half the nursing-home neighbor signal
  and ALL of the toxic-site one) and the piece-5 status row (first rules
  exist and ran; the "automatic every tick" part is still unbuilt).
- `STATUS.md` — full state of what ran today.
- `reports/ripples_confirm_and_break_2026-08-21.md` — the latest results
  the new vocabulary has to be able to describe cleanly (a good stress
  test: if the chosen words can't retell that report simply, they're wrong).
- Chris's standing rules: no jargon ever (memory: treat Chris as
  non-expert), chat is the interface, ADHD-shaped formatting, one decision
  per message.
