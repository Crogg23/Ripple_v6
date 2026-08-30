---
name: feedback-the-handbook-is-the-chain-explorer
description: "2026-08-30 crashout: 'the handbook' means the PUBLISHED chain-explorer artifact ('Follow the joins out', dark Miller-column page, artifact 4fac05a9…), NOT the repo's rail-and-detail join_handbook.html or the markdown twin; a whole day of layers went into the wrong page"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b3eeac94-389f-4ecc-be3a-a1812c354077
  modified: 2026-08-30T14:40:37.047Z
---

When Chris says "the handbook" / "the join handbook" he means the published artifact **The Join Handbook**
(https://claude.ai/code/artifact/4fac05a9-e254-43ab-b4dd-e1787d1c44e9): the "Follow the joins out" chain
explorer — dark page, start table on the left, click a dataset and its joins open as the next column, solid /
dashed / dotted lines for new / already-reachable / loops-back, columns + notes fold open under each card.
Its data lives in four inline globals (tables+conns, meta, context, schema). Its source was NOT in the repo
until 2026-08-30 (it was built in-chat and published only).

The repo's `reports/viz/join_handbook.html` (rail + detail panel) and `reports/JOIN_HANDBOOK.md` are a
DIFFERENT, older-style page Chris called "that 2005 style markdown file" and threatened to cancel over.

**Why:** On 2026-08-30 I spent the whole day adding the pass-2 edges, the place layer and the clock layer to
the repo page and never once opened the published artifact. Chris had to attach the artifact's HTML to make
me see it. "If you show me that 2005 style markdown file again I'm going to cancel my subscription."

**How to apply:**
- Before touching "the handbook", `Artifact list` and READ the published one; build on that version.
- Any handbook change = update the chain explorer artifact (same URL) AND mirror its full HTML into the
  repo ([[feedback-standalone-html-in-repo]]). Never build a parallel page.
- When a deliverable already exists as an artifact, the artifact is the original; a repo file with a
  similar name is not proof it's the same thing — open both and compare before working.
- Related: [[feedback-verify-mechanism-before-rebuilding]], [[feedback-spine-is-red-lane]].
