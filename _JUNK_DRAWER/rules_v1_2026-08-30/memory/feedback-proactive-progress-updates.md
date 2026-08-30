---
name: feedback-proactive-progress-updates
description: "user wants regular proactive status updates during long background waits, not silence until the final completion notification"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b210958a-f764-4a67-876a-d2dbc8f4a979
  modified: 2026-07-28T23:50:42.480Z
---

When a long-running background operation is in flight (Snowflake rebuild, dbt run, any multi-minute job), proactively check and report progress at reasonable intervals rather than going silent until the final completion notification lands.

**Why:** launched a `connect discover` + `connect spine` rebuild in the background during the 2026-07-28 repair pass and then said nothing until the user had to ask "dont let me wait around for nothing. regularly check and give me updates wtf." The harness auto-notifies on task completion, but that's not enough — the user wants visibility *during* the wait, not just a report at the very end.

**How to apply:** for any long-running background operation (Bash `run_in_background`, a `Workflow`, a background `Agent`), use the `Monitor` tool to stream progress lines/status at a reasonable poll interval instead of just saying "I'll report back when done" and going quiet. Set it up proactively, before the user has to ask — don't wait for a nudge like this one.
