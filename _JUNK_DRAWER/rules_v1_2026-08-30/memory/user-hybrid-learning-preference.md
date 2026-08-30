---
name: user-hybrid-learning-preference
description: Chris wants tools that are fast/easy via AI assistance AND teach him the underlying technology hands-on — not fully black-boxed abstractions
metadata: 
  node_type: memory
  type: user
  originSessionId: 61965679-380f-42e6-9a63-e8ce0ede6471
---

When Chris asks for an AI-assisted tool around a specific technology (e.g. Plotly), he wants a
**hybrid**: reusable plug-and-play components that get him productive immediately with minimal
boilerplate, but with the real underlying code (e.g. actual `fig = px.___(...)` / `go.Figure(...)`
calls) visible and editable — not hidden behind a chat response or a rendered-image-only output.
He explicitly wants to *learn* the tool (Plotly) by using it, with the AI removing friction rather
than removing the mechanism.

**Why**: came up designing the [[feedback-chris-drives-analysis]] investigator tool — he rejected
a pure black-box "ask in English, get a chart back" design as not cutting it, specifically because
it would deny him the "best of both worlds" of ease/speed plus actually building Plotly fluency.

**How to apply**: when scaffolding a tool around any library/technology Chris will use repeatedly,
default to exposing real, editable source (starter templates / plug components with visible code)
rather than a fully generated/opaque output, even if the opaque version would be faster to build or
smoother to demo. Speed should come from good starting points, not from hiding the mechanism.
