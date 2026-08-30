---
name: feedback-verify-mechanism-before-rebuilding
description: "After a build gets rejected on a metaphor-described tool request (Lego, toolbox, Tetris), stop and pin down the concrete mechanism before building again — don't treat each new metaphor as license for another full build"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 99f5b04d-070f-4f01-9a60-38d1eac7b3fd
  modified: 2026-08-23T21:45:38.978Z
---

When Chris describes a wanted tool only through casual metaphor across several
messages (Lego bricks, "smart if/then," a "toolbox," "Tetris concept") and a
built artifact gets rejected, the failure isn't usually the underlying
research/content — it's that the metaphor got translated into a concrete
mechanism without confirming the translation first. Building a second, then a
third full artifact on successive new guesses compounds the miss instead of
correcting it.

**Why:** [[deadspace-and-counterweight]] and a follow-up "Layout Picker" tool
were each built same-session (2026-08-23) on my own translation of Chris's
metaphors, and each got rejected — "wtf is this... its an advertisement" for
one, "not helpful in the slightest" for the next. Chris then supplied a
sharper metaphor each time (configuration → Tetris) rather than a spec, which
means the ambiguity was real, not a fake-ask situation — but I kept resolving
that ambiguity by building instead of by confirming.

**How to apply:** After ONE rejected build on a vague/metaphor-led ask, the
next response is a concrete restatement (or, better, 2-3 distinct concrete
mockups/descriptions via AskUserQuestion previews) to confirm the mechanism —
not a fourth guess dressed as a new artifact. Cheap to check, expensive to
keep missing. This is a taste question (what tool Chris wants), squarely his
call per the Ask Filter — stop guessing on his behalf once a guess has already
missed.

**Same failure, different medium (2026-08-23, later same week):** the
pattern isn't limited to building artifacts. Asked to write a brief for
Claude Design describing [[board-segments-webflow-2026-08-23|Board
Segments]], the first draft was pixel/hex-level "orders" (exact coordinates,
CSS values) — Chris: "do not give orders you are failing at the task." He
wanted the CONCEPT (why it exists, how it feels, what problem it solves),
not a spec to execute. Then, asked what Webflow unlocks, a build got started
on a 20-theme switcher inferred from an unrelated engine found in a design
file — also wrong; Chris only wanted the ALREADY-CHOSEN style used to build
components, no alternate themes at all ("i led you astray... i dont give a
fuck about whats there now"). Same root cause each time: turning an
open/creative ask into a concrete deliverable without checking the register
(concept vs. spec) or the scope (use what exists vs. propose alternates)
first. Apply this lesson to briefs and creative-tool handoffs, not just
Claude Code artifacts.
