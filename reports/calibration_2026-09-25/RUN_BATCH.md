# Search one batch of the calibration test

Paste this same prompt into each new chat. Each chat claims its own batch.

---

Calibration search run. Working directory: C:\Code\Ripple_v6.

1. Run `python reports/calibration_2026-09-25/claim.py`. It prints your batch name and its 19 story IDs. If it prints "none left", stop and tell me.
2. Read `reports/calibration_2026-09-25/SEARCHER.md`. Every searcher follows it exactly.
3. Split your 19 stories across 4 searcher subagents, about 5 each, running in parallel. Give each one the path to SEARCHER.md and its story IDs.
4. This chat has 200 web searches in total, shared by every agent. Each searcher uses at most 10 per story.
5. Skip any story whose `reports/calibration_2026-09-25/search/<id>.json` already exists.
6. Searching only: no judging, no git, no warehouse, no edits to any other file.
7. When all 4 finish, reply with the batch name, then one line per story: id, queries run, sources found. Flag any story that wasn't searched.
