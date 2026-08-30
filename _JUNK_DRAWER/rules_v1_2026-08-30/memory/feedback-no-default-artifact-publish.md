---
name: feedback-no-default-artifact-publish
description: "2026-08-30: stop defaulting to publishing Claude artifacts for Ripple deliverables — the repo HTML file is the real, standalone deliverable; only publish an artifact if Chris explicitly asks for that link"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b3eeac94-389f-4ecc-be3a-a1812c354077
  modified: 2026-08-30T15:01:15.868Z
---

Chris: "can we stop defaulting to claude artifacts. Its fucking annoying."

**Why:** every Ripple page (the handbook, viz pages, etc.) is meant to be a standalone file in the repo —
double-click, opens in a browser, no Claude account needed. Auto-publishing it as a Claude artifact on
every update is an extra unasked-for step, not a convenience. See [[feedback-standalone-html-in-repo]].

**How to apply:**
- Build and update the repo HTML file. Stop there.
- Do NOT call the Artifact publish action as a matter of course after building/updating a Ripple page.
- Only publish/update an artifact when Chris explicitly asks for the shareable/claude.ai link.
- If a page already has a live published artifact from before this rule, don't feel obligated to keep
  syncing it — say so if asked, but don't proactively republish.
