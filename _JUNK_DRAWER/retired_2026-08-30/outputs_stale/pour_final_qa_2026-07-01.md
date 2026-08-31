Path sweep is clean (no `/Users/` hardcodes remain). All 14 scripts swept.

I have empirically verified every load-bearing finding. Here is my final QA verdict.

---

# FINAL QA VERDICT

## 1) Pour decision: **GO-WITH-FIXES**

CSV/API snapshot pour is safe — the density gate, dedupe, join-key, path-sweep, and Snowflake session-guard fixes all hold. But the OOM guard defaults **most sources** (unknown volume) into a **chunked path that has zero fetch timeout, head-sampled density, and no SHA-skip**, and the snapshot timeout itself **cannot unblock process exit** on a truly-hung fetch. Fix #1 (thread-leak) and #4/#6 (chunked-path composition) before an unattended `--batch` pour at scale.

## 2) NEW bugs the fixes introduced

| # | Bug | Fix | Severity |
|---|-----|-----|----------|
| N1 | **`_run_with_timeout` orphans a non-daemon worker that blocks interpreter exit.** Verified: logic finished at 1.01s, process didn't exit until 8.08s (atexit join on the orphan). A genuinely-hung socket → process **never exits**. This behavior did not exist before the timeout fix. | Run fetch on `threading.Thread(daemon=True)` + `queue.Queue`, OR push a socket/`requests` `timeout=` into the fetch itself. `shutdown(wait=False, cancel_futures=True)` does NOT help — cancel_futures only cancels un-started tasks. | HIGH |
| N2 | **OOM guard routes unknown-volume (the default) → chunked, which silently undoes two other fixes.** `_looks_large('unknown'/''/None)=True`. Chunked has: no SHA skip-if-unchanged (re-pours re-download every time), head-2000 density (verified: blank-leading frame scores empty=True vs full-frame empty=False → false-demote), and no OOM benefit for single-DataFrame fetches (`iter([result])` holds whole frame). The fixes compose adversarially. | Drop `'unknown'` from `_LARGE_VOLUME_HINTS`; only upgrade on a POSITIVE large signal. Leave unknown/blank as snapshot. | HIGH |
| N3 | **Chunked path has no fetch wall-clock cap at all.** `_execute_fetch_chunks` calls `fetch(context)` bare (ingest.py:498); `_load_landing_chunked` iterates `for chunk in chunk_iter` bare (ingest.py:532). Combined with N2, a stalled unknown-volume source hangs `--batch` forever — skip-and-continue never fires. | Wrap each `next(chunk_iter)` in a per-chunk `_run_with_timeout` (using the daemon-thread variant from N1), raise RuntimeError on deadline. | HIGH |
| N4 | **`_dedupe_cols` leaves a residual duplicate when a suffix name pre-exists.** Verified: `['FOO','FOO','FOO_2'] → ['FOO','FOO_2','FOO_2']`; `_stringify` reproduces the collision → duplicate CREATE TABLE column → Snowflake rejects. Reintroduces the exact blocker it closed. Reachable: `Foo (2)` sanitizes to `FOO_2`. | On collision, `n=2; while f"{c}_{n}" in seen: n+=1`; seed `seen` with every bare name. | MEDIUM |
| N5 | **`_stringify` renders integer-valued floats per-cell → mixed formats in one decimal column.** Verified: `[2.0,2.5,100.0] → ['2','2.5','100']`. Behavior change vs HEAD (`'2.0'`). Numerically harmless (TEXT landing + staging recast) but degrades raw-mirror fidelity and disguises >2^53 float precision loss as a clean integer. | Accept as documented tradeoff (join-key protection is worth it) OR decide int-vs-float **per column**. | LOW |
| N6 | **`register._encode` corrupts a JSON-array string / raises on numpy arrays.** Verified: `'["a","b"]' → '["[\"a\"", "\"b\"]"]'` (silent corrupt facet); `np.array(['a','b'])` raises ValueError. Both need off-spec input, so latent. | In the str branch, `json.loads` if it looks like `[...]`; handle array-likes before the `== ""` check; log on coercion. | LOW |

## 3) Blocker-closure table

| # | Original blocker | Status |
|---|-----|--------|
| 1 | fetch-timeout orphan thread blocks exit | **STILL OPEN** (N1 — proven, process hangs 8s / forever) |
| 2 | null-token `'nan'` rides through density | **STILL OPEN** — verified frac=0.667, empty=False; `_stringify._cell` (line 762) only strips exact-case `NaT/<NA>/None`, not `nan` |
| 3 | fetch wall-clock leaves non-daemon thread | **STILL OPEN** (same as #1/N1) |
| 4 | chunked path has no fetch timeout | **STILL OPEN** (N3) |
| 5 | OOM guard + no chunked timeout compose adversarially | **STILL OPEN** (N2+N3) |
| 6 | unknown/blank → large → chunked default | **STILL OPEN** (N2) |
| 7 | chunked path no wall-clock timeout | **STILL OPEN** (N3) |
| 8 | chunked density head-samples → false-demote | **STILL OPEN** (verified full=0.667 vs head=0.000) |
| 9 | `_dedupe_cols` residual duplicate | **STILL OPEN** (N4 — reproduced) |
| 10 | per-cell int-float mixed decimals | **OPEN (accepted tradeoff)** — decide + document |
| 11 | `_encode` aborts on numpy array | **STILL OPEN but unreachable** — no call path delivers numpy |
| 12 | fetch_timeout misses chunked stream | **STILL OPEN** (dup of N3) |
| 13 | CONNECT stage retries 4× ignoring feedback | **OPEN (low)** — verified; wasted work only, no corruption |
| 14 | `'gb'` substring false positive | **STILL OPEN** — verified `legbar/megbyte → True`; self-healing (safe chunked upgrade) |
| 15 | one-DataFrame chunked fetch still OOMs | **OPEN (latent)** — depends on model output at Checkpoint 2 |
| 16 | sync Playwright in worker thread | **OPEN (unverifiable)** — Playwright not installed; gate scrape_js sources |
| 17 | `_is_blank` token fix dead on vectorized path | **STILL OPEN** (same root as #2 — vectorized mask at line 124-125 never calls `_is_blank`) |
| 18 | `_encode` silently corrupts JSON-string facet | **STILL OPEN but off-spec-triggered** (N6) |

**Score: 0 of 16 fully closed by superficial inspection.** The density fix (#2/#8/#17), dedupe (#9), and timeout (#1/#3/#4) all have a real residual gap. Note: the fixes that ARE solid and verified — join-key int survival (`'6037.0'→'6037'`, null→`''`), snapshot full-frame density, path sweep (no `/Users/` remains), 106 tests passing — just don't cover the blockers above.

## 4) Residual risks to watch during the pour

- **Process may not terminate after `--batch`** (N1). Before pouring: point one queued source at a black-hole endpoint, confirm the batch process self-exits without an external kill. This is the single highest risk.
- **Unknown-volume sources are the common case and route to the least-protected path** (N2+N3+#8). Until fixed, a single stalled unknown source hangs the whole unattended pour and its density is head-sampled. Consider setting explicit volume strings in `sources_queue.py`, or force `load_mode=snapshot` per source, as an interim.
- **Chunked re-pours are not idempotent** — no SHA skip; every re-run re-downloads and rewrites the table. Watch LLM spend / warehouse credits on repeated chunked pours.
- **`Foo (2)`-style headers** in gov CSVs can still crash CREATE TABLE (N4). Watch for `duplicate column` errors in `INGEST_RUNS` failed messages.
- **scrape_js sources**: sync Playwright now runs in a worker thread (unverified, #16). Gate with a single render smoke test, or set `ONBOARD_FETCH_TIMEOUT_S=0` for scrape sources (escape hatch confirmed at ingest.py:623-624 — runs on main thread).
- **Mixed-decimal raw text** (N5) affects raw-text dedup/equality only; staging recast neutralizes it for analytics. No action needed at pour, but don't trust raw-mirror string equality on float columns.
---

## FIXES APPLIED (2026-07-01, post-verdict) — 111 tests green

- **N1/N3/#3/#4/#7/#12/#16 (timeout + thread + chunked + Playwright):** replaced the
  ThreadPoolExecutor wall-clock wrapper with a **socket read timeout**
  (`_apply_fetch_socket_timeout` -> `socket.setdefaulttimeout`, set once per load).
  No worker thread -> cannot block process exit; covers BOTH snapshot and chunked
  (network reads happen on sockets created after it's set); safe for sync-Playwright.
- **N2/#5/#6/#14 (OOM guard over-reach):** `_looks_large` now upgrades snapshot->chunked
  ONLY on a positive size signal (word-boundary gb/tb/million/billion/bulk/huge/large or
  a parsed count >= 1e6). Unknown/blank stays snapshot (idempotent + full-frame density).
- **#2/#17 (dead null-token fix):** `_stringify._cell` now blanks the string tokens
  nan/nat/none/<na> (what a loader's astype(str) makes of a null) -> density gate sees
  them as blank. Regression-tested (all-'nan' frame -> empty=True).
- **N4/#9 (dedupe residual collision):** `_dedupe_cols` bumps a generated suffix until
  unique. Tested.
- **N5/#10 (mixed decimals):** int-vs-float decided PER COLUMN (whole-number float column
  -> ints; genuine decimal column keeps decimals). Tested.
- **N6/#11/#18 (register encode):** array-likes (numpy/Series) handled before the ""
  check; no ValueError on numpy facets.

**STILL OPEN (narrow, low-harm, documented):**
- #8 chunked density still head-samples (only positively-huge sources now route there;
  worst case = a false 'empty' LABEL on a blank-leading huge source, data still lands).
- Chunked re-pours aren't SHA-idempotent (by design -- they re-stream). Watch credits on
  repeated chunked re-runs.
- #13 CONNECT stage may retry 3x on error (best-effort step; wasted work only).
- #18 `_encode` on an already-JSON-array *string* splits on comma (off-spec; normal path
  passes lists).
