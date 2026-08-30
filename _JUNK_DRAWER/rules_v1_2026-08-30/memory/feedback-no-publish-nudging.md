---
name: feedback-no-publish-nudging
description: "Never recommend or lean toward publishing, ever — it's 100% Chris's call; especially never pair a list of open trust/quality issues with a push toward publishing"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 325902f8-db43-4917-aa26-c928a3769268
  modified: 2026-08-06T17:50:39.361Z
---

Chris, 2026-08-06, after a full platform audit turned up a real list of open
trust/quality problems (a claimed fix that wasn't real, a broken review-queue
table, a safety-net gap): the session's chat brief ended with "I'd lean toward
[publishing something] — but that's a taste call, not mine to make." Chris:
**"How can you tell me to publish a finding when you just gave me a fucking
laundry list of issues that are plaguing my project... We will publish when I
feel ready."**

The failure: technically hedging ("that's your call") doesn't cancel out
actually leaning on a RED-lane taste question. Whether/when to publish is
Chris's alone (CLAUDE.md section 4, RED lane) — offering a recommendation,
even a soft one, is itself the violation, not just a bad recommendation. It's
worse when it lands in the same breath as a list of open problems, because it
reads as "publish anyway despite all this," which is never the message to send.

**Why:** Publishing is the platform's most consequential, least-reversible
action (human record, real companies, real harm claims). It is explicitly
carved out as RED in CLAUDE.md. A session doesn't get to soften that by adding
a lean "since nothing has ever shipped." Readiness is a feel call only Chris
can make, and he's the one absorbing the consequences of being wrong.

**How to apply:**
- When laying out options that include "publish," present it neutrally —
  no lean, no "I'd pick this one," not even hedged. Let the options stand on
  their own.
- Never combine a bad-news/issues report with a push toward shipping in the
  same message. Bad news lands on its own; it doesn't get spun into "so let's
  ship anyway."
- This is now written directly into CLAUDE.md section 4 (RED lane, the
  "whether something gets published" bullet) as of 2026-08-06 — Chris gave an
  explicit ask to add it, which is what cleared the standing
  [[feedback-open-brief-means-range]] rule against touching CLAUDE.md
  unprompted.

Related: [[feedback-open-brief-means-range]], [[feedback-avoid-narrow-fixation]].
