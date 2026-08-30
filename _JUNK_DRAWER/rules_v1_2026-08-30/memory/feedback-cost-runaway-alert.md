---
name: feedback-cost-runaway-alert
description: "Chris 2026-08-22 — alert IMMEDIATELY if a day's spend is trending toward a $300 day; check the warehouse meter during long-running sessions, don't just estimate"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4154f5c7-5881-4657-8fd6-ec08f82f44ab
  modified: 2026-08-22T19:04:28.872Z
---

Chris: "just let me know immediately if it's going to end up being one of those three hundred dollar days."

**Why:** he budgets by feel and a surprise big bill breaks trust; a $5 day and a $300 day must never look the same in chat.

**How to apply:** during any session with sustained warehouse work, pull real credits from the metering view (`information_schema.warehouse_metering_history`, ~$2-3/credit) rather than guessing — and the moment projected day spend crosses ~$50 trending upward, or any single planned operation could plausibly reach $100+, say so in chat immediately with the number, unprompted. This is on top of the existing §8.7 price-tag-before-spend rule ([[interaction-contract]]); §8.7 covers asking before, this covers watching during.
