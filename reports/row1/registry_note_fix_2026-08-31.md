# fed_nih_reporter registry note — stale, replacement staged

**Date:** 2026-08-31

**Why:** the 08-31 audit proved FED_NIH_REPORTER fully loaded:
FY2000–2026 contiguous, 2,122,611 rows, zero duplicate APPL_IDs,
FY2024 = 83,519 vs the API's published 83,516.
The registry NOTES still said "CAPPED at FY2000-2002".
The resume ran to completion after that note was written.

**Old note (preserved verbatim):**

> CAPPED at FY2000-2002 (206,333 rows, verified exact gap=0 against live API) by explicit operator instruction after the recursive date-bisection re-fetch crashed mid-FY2003 write (Snowflake numeric-cast error on a value serialized as '[276, 320]', likely from the amount-range density-rescue path). FY2003-2026 NOT landed. Old 405,000-row 15,000-per-year-flat-capped data has been REPLACED (was wrong for all 27 years); this smaller 206,333-row table is 100% verified-correct for the 3 years it covers. Real follow-up needed: fix the write-time serialization bug, resume for FY2003-2026.

**New note (what the fix script writes):**

> FULLY LOADED (verified 2026-08-31 audit): FY2000-2026 contiguous, 2,122,611 rows, zero duplicate APPL_IDs; FY2024 = 83,519 vs API published 83,516. The earlier 'CAPPED at FY2000-2002' note was overtaken - the resume ran to completion. Old note preserved in reports/row1/registry_note_fix_2026-08-31.md.

**How:** run `python3 scripts/fix_nih_registry_note_2026_08_31.py`.
The harness classifier blocked Claude running the UPDATE directly.
