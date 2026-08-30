---
name: board-segments-webflow-2026-08-23
description: "Reference pointers for Chris's personal portfolio work: the live Webflow site tied to the Ripple blueprint design system, and where the source design-system export file lives"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 679061ff-26b2-4311-b078-2e0ba0740ccc
  modified: 2026-08-23T21:45:52.816Z
---

Chris's personal investigative-journalism portfolio (separate from the
Ripple data platform — Ripple's CLAUDE.md constitution does not govern this
work) is being built in Webflow.

**Site:** "Ripple: Connecting the Dots" — site_id `6a85e725782a7847c62c3539`,
one page "Home" — page_id `6a85e72f782a7847c62c365d`. No custom domain yet.
Chris treats the site's existing content as disposable scratch, not
something to protect ("the start of one until I realized I needed a lot of
help using it").

**Design tokens are live in Webflow**, not just documented in files: 23
Variables (13 colors, 3 fonts, 7 spacing sizes) in the site's default "Base
collection," plus 5 global classes (`Body`, `heading-1`, `heading-2`,
`mono-label`, `hairline`) bound to them — built 2026-08-23. This is the
`blueprintInk` visual identity: bg #0a1620, ink #f2e9d8, sage #5f7a4f, rust
#b5703f, teal #3d8f82, gold #c9a25a, bp #2f6f8f; Space Grotesk / Work Sans /
JetBrains Mono. Chris confirmed this exact style is final — don't propose
palette alternates.

**Source design-system file:** `c:\Code\Ripple_v6\Ripple Design System -
Blueprint (standalone) (9).html` — a ~5.9MB bundled Claude Design canvas
export (JSON blob, not plain HTML; needs decoding — see the handoff doc at
`C:\Users\wroge\AppData\Local\Temp\handoff-ripple-blueprint-webflow-components.md`
for the exact decode script) referencing the 4-section blueprint (Color /
Type / Spacing / Components) these Webflow tokens were extracted from. It
also contains an unused 20-theme parametric engine — explicitly not wanted,
don't build a theme switcher from it.

**Separate, unrelated effort in the same repo:** `reports/viz/board_segments.html`
is a Claude Code Artifact — an interactive layout-shape generator tool, built
the same week, sharing only the visual token palette (not the Webflow work).
Don't conflate the two.
