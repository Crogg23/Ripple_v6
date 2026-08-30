---
name: standalone-html-in-repo
description: "Every visualization/deliverable page must also land as a standalone HTML file in reports/viz/ — Claude artifacts are mirrors, not the durable copy"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e8d6f6bb-8f74-45ab-9b67-728cba8c7538
  modified: 2026-08-22T21:33:03.172Z
---

Chris (2026-08-22, viz sprint): "i need things like this as standalone html files in my
repo please - right now its a claude artifact - what if claude goes down for a while."

**Why:** Artifacts live on claude.ai; if Claude is down or the account changes, the work
is gone. The repo copy is the durable original; the artifact is a convenience mirror.

**How to apply:** whenever publishing a viz/report page as an artifact, ALSO write the
full self-contained HTML (wrapped in a real doctype/html/head/body skeleton — artifacts
add that at publish, files need it inline) to `reports/viz/` in the repo, and keep the
extraction scripts + `__PLACEHOLDER__` templates in `reports/viz/_build/` so pages can be
rebuilt without the session scratchpad. See [[interaction-contract]].
