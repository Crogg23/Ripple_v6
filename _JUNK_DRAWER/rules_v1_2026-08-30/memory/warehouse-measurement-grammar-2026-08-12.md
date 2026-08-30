---
name: warehouse-measurement-grammar-2026-08-12
description: "the semantic-layer model Chris wants over all 558 sources — nouns/events/links/codes, surface-pass grid, six universal ratios; census before curated cases"
metadata: 
  node_type: memory
  type: project
  originSessionId: f9ae8e11-5610-49a3-9670-51a0ef1f586a
  modified: 2026-08-12T20:54:14.294Z
---

Green-lit direction as of 2026-08-12. Chris wants an **unbiased description of
the whole warehouse** before any more curated harm cases. His framing comes from
his day job doing emergency-department analytics: encounters, completed visits,
medication orders, medication administrations — **multiple fact tables at their
own natural grains, conformed on shared dimensions**, with the metric library
defined once so anything can cross anything without a new build. (I initially and
wrongly told him ED data has "one grain" — he corrected it; the ED playbook
transfers directly and Ripple is not a special hard case.)

**The model:** every row is a NOUN (persists, has an ID, is a denominator), an
EVENT (happened, has a date, belongs to a noun, is a numerator), a LINK (joins two
nouns — the scarcest and most valuable rows), or a CODE (vocabulary, sliced by,
never counted). Every measure is events per noun, cut by codes, traversed along
links.

**The output shape:** a grid — things down the side, ~30 display slots across the
top (count, over time, by place, by entity, by type, per entity, rank,
distribution, concentration, zero-count, first/last, gap, mix). ~50 things × ~30
slots ≈ 1,500 surface views, none requiring anyone to have a hunch. Follow
[[feedback-breadth-first-surface-pass]] to build it.

**Why census before cases:** a single finding is uninterpretable without a
baseline — 82% of chronic violators unenforced could be the worst number in
American regulation or completely unremarkable, and nobody knows which. The harm
cases are cells in the frame, not a substitute for it.

**The unique output** (only possible with 558 sources on one spine): the same
ratios computed for every domain in identical units — observations per noun (the
surveillance rate), findings per observation, consequences per finding (the
accountability rate), money per consequence, harm per finding, harm per noun.
"Somebody looked" is the thinnest event family and gates everything.

**Five rules the build ships with** (found by stress-testing it, all real):
1. No conversion rates without row-level lineage — most chains are parallel counts
   at a shared entity, not funnels. "X% of exceedances became violations" is
   fabricated unless a column links them.
2. Every cell carries a coverage grade; 376 of 558 sources have unknown
   completeness, and a zero surveillance rate has three different meanings.
3. Cross-domain comparison is legitimate for SHAPE (where does the funnel
   collapse), never for LEVEL (agency A is stricter than B).
4. The sweep emits hypotheses, never findings — wide search manufactures
   significance.
5. Population served is a mandatory dimension wherever it exists, or the cell is
   flagged process-only. Otherwise it's a beautiful description of paperwork with
   no human in it.

One design call still open: when an event gets promoted to a noun (suggestion:
when it has children of its own — recalls, contracts, dockets all do).
