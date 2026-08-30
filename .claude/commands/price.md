---
description: Show what something cost last time, from the warehouse query log. Usage /price <SQL text pattern or table name>
---
Run `python scripts/price_it.py --like "%$ARGUMENTS%"` (add `--days 180` if nothing comes back in 90).

Report the result as one line: what, p50 and max dollars, how many past runs it's based on, and whether the $/credit rate is a default. If it says "no real number for this", say exactly that — never substitute a guess.

This also unlocks greenlights for the next hour.
