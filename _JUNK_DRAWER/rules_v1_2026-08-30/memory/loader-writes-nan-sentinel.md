---
name: loader-writes-nan-sentinel
description: "2026-08-11 — bulk loaders wrote the literal text 'nan' where NULL belonged (pandas NaN is not None); 4.2M corrupted cells found. Fixed via _as_text; repair tool is scripts/repair_nan_text.py."
metadata: 
  node_type: memory
  type: project
  originSessionId: 2abe330a-1107-4aec-8937-200e6edcd021
  modified: 2026-08-11T14:53:32.430Z
---

Every bulk loader in `scripts/` stringified values for its all-VARCHAR landing
table with:

```python
df[c] = df[c].apply(lambda v: None if v is None else str(v))
```

**pandas does not keep a JSON null as `None`** — it becomes float `NaN` the
moment the column is built. So `v is None` was False and `str(NaN)` wrote the
three characters `nan` into the warehouse.

Damage found 2026-08-11:
- FDIC BankFind `LEI`: 6,260 "populated", of which **4,008 were the string 'nan'**.
- FDIC Summary of Deposits: **4,235,099 sentinel cells across 15 columns**,
  including the branch identifier (75,838) and both coordinate columns (~191k each).
- The FEMA disaster-aid table carries it too, at a much lower rate.
- Treasury's daily-cash loader was clean (that API returns real nulls).

**Why it is worse than an empty column:** `'nan'` reads as populated to any null
check, and on a key column **`'nan'` joins to `'nan'`**, silently fabricating
matches. This is the third instance of the masked-blank class on this platform —
see [[bridge-fuel-reality]] for the first two.

**How to apply:**
- New loaders must use the shared `_as_text` helper (present in
  `fdic_institutions_load.py`, `fdic_sod_load.py`, `fema_ia_load.py`,
  `nih_reporter_load.py`, `treasury_dts_deposits_load.py`). It also catches
  pandas `NA`/`NaT` and whitespace-only strings, while preserving a genuine
  source value of `"nan"` and a real `0`/`False`.
- `tests/test_loader_null_handling.py` fails the build if the broken coercion
  returns.
- For tables loaded before the fix: `python scripts/repair_nan_text.py --dry-run`
  first (it shows per-column counts), then without the flag. One UPDATE per
  table, cheap.
- When validating any new column, `COUNT(col)` is still not the test — pair it
  with `COUNT(DISTINCT col)` **and look at actual values**. A length check caught
  a related problem the same day: FDIC publishes `LEI` truncated to 16 characters
  against a real LEI's 20, so it joins to GLEIF only on `LEFT(gleif.LEI,16)`.
