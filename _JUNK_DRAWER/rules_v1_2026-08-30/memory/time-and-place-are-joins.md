---
name: time-and-place-are-joins
description: 2026-08-29 DECISION — time and geography are first-class joins, equal to ID joins; the ID spine is deprioritized ("waste of time"); Chris is driving the build step by step
metadata:
  type: project
---

Chris, 2026-08-29: **"We will be using time and date and geography [to join]."** Two things
on the same day/month/year, or in the same state/district/county/ZIP, is a legitimate
join even with zero shared ID — "what two things looked like together." Example he gave:
a politician's district/state where something is happening, with no ID link.

The ID spine ("who's-who") was called a waste of time — ignore it unless he raises it.

**Why:** the join engine and the handbook page treat geography as the weakest tier
("same place, never identity") and never use time at all. That was the ID-spine era's
opinion, not his. Sessions that repeat it ("it doesn't say who", "coarse", "noise") are
defending the old way — CLAUDE.md §0 says the old way is stale.

**How to apply:**
- Treat a time/place match as a join, same standing as an ID match. Don't rank it below.
- Don't restate the limits he already knows (no identity, grain). He is building step by
  step and will get to "who" later.
- He drives. Answer what's asked; no roadmaps. See [[feedback-no-jumping-ahead]].
- Inventories built today: reports/time_index/DATE_COLUMNS_ALL.md (1,275 date columns,
  value-verified) and reports/location_index/LOCATION_COLUMNS_ALL.md (2,244 place columns,
  name-scan only).
