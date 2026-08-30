---
name: feedback-grilling-calibration
description: "When Chris asks for high-level/vision framing (not implementation), don't multi-select-interrogate every fork — synthesize big-picture and produce the concrete deliverable"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 61965679-380f-42e6-9a63-e8ce0ede6471
---

During a /grill-me session (2026-07-03) about a new "investigator tool," Chris got visibly
frustrated ("jesus christ") after two rounds of AskUserQuestion multi-selects asking him to pick
UX/interaction-model details. His actual ask was for big-picture synthesis ending in a concrete
artifact (a prompt to hand to another AI session) — not a decision tree he had to walk personally.
He said outright he keeps asking for "high level things" specifically so he can do the detailed
analysis/design work himself later — grilling him on those same details defeats the point.

**Why**: Chris repeatedly asks for high-level framing because that's the layer he wants outside
help on; the implementation-detail layer is the part he wants to own. Treating every fork as a
menu he must pick from (rather than making a judgment call and stating it) reads as making him do
work he explicitly delegated away.

**How to apply**: when a request is framed as "think big picture" / "from scratch, top-down" /
architecture-vision level, ask at most 1-2 genuinely blocking questions (things with no
inferable answer and high cost if wrong), then move to synthesizing a concrete deliverable and
let Chris react/edit. Don't keep drilling into implementation-level forks (interaction paradigm,
UI layout, which library) once he's signaled he wants to own those decisions or have another
agent (e.g. Fable) scope them. See [[feedback-chris-drives-analysis]] for the related preference
about who does the actual decision-making on analysis tools.
