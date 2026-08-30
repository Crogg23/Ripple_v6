---
name: feedback-chris-drives-analysis
description: "For exploration/analysis/investigator tools, Chris wants to do the investigating himself with AI building infrastructure — not an autonomous agent that produces findings for him"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 61965679-380f-42e6-9a63-e8ce0ede6471
---

For any tool where Chris is meant to *investigate* or *analyze* data (as opposed to the onboarding
pipeline), the agent's job is to build the infrastructure/copilot, not to do the investigating and
hand him conclusions. Chris explicitly rejected framing an "investigator tool" as something that
autonomously cross-references data and hands him findings — he wants to ask the questions, read
the charts, and decide what they mean himself, session to session, dynamically (his own words:
"my own PBI situation").

**Why**: this is the opposite pattern from `onboard.py`'s "the agent does everything, Chris
approves" model (see [[CLAUDE.md]] "Working With Chris" section). That pattern is specific to
onboarding/collection — mechanical, repeatable work he doesn't want to do by hand. Analysis and
investigation is the part he actually wants to keep doing; the floor/ceiling goal in
[[platform-vision]] is Chris becoming a working investigative journalist, not automating that role
away.

**How to apply**: before designing any exploration/BI/analysis surface, check which side of this
line the task falls on. If it's "help Chris look at data and draw his own conclusions," build
tools/infra/copilot assistance, keep him in the loop on every real judgment call, and preserve the
facts-vs-leads discipline (same hard ID = fact, name-only match = unconfirmed lead a human must
confirm — this applies to ANY surface, not just the rule-based leads engine in `connect/leads.py`).
If it's mechanical/repeatable collection work, the onboarding-agent pattern (agent does everything,
human approves at checkpoints) is correct instead.
