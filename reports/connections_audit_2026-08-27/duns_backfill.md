# DUNS Backfill — Verification + Path Finding (2026-08-27)

Follow-up to `join_layer.md` §5 (DUNS 94% orphaned). Read-only work only —
**no code was changed and nothing was written to the warehouse.** Reason below.

## 1. Column verification (guarded lane, SERVE_WH enforced)

Table: `LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FULL`
Column: `recipient_duns` (lowercase quoted ident, TEXT; `recipient_parent_duns`
also exists but is the parent = a different entity → graph-key territory, not
an extra_key).

| Check | Result |
|---|---|
| Total rows | 19,902,879 |
| `COUNT(col)` "filled" | 19,902,879 (100% — **misleading**) |
| Blank-string rows | 12,655,018 (63.6% — the usual sentinel mask) |
| Real non-blank rows | 7,247,861 |
| Distinct non-blank | **478,278** |
| Not 9-digit shaped | 1,578 rows (0.02%) |
| Placeholder values (999999999 etc.) | 7,298 rows (killed by pad-mode PAD_PLACEHOLDERS anyway) |
| Top-10 non-blank values | real 9-digit DUNS, largest = 41,755 rows (0.6% of non-blank) — no sentinel concentration |

**Verdict: the column is real.** ~478K distinct legitimate DUNS, matching the
audit's 478,231 post-norm figure. The existing DUNS pad-9 norm rule handles it
as-is (blanks and placeholders die in normalization; no new norm rule needed).

## 2. Which path exists

**Only the full-rebuild path. No incremental-safe path exists — for two
independent reasons:**

1. **Structural:** the fix is a DISPLAY_SPECS edit, and the incremental config
   guard (`connect/incremental.py`, `_config_fingerprint`) hashes
   `repr(sorted(DISPLAY_SPECS.items()))`. ANY spec edit — even adding one
   extra_key to one table — changes the fingerprint, and `connect-one` /
   `connect-changed` then refuse to run until a full `connect spine` +
   `connect.incremental seed` re-pin. This is by design (an incremental MERGE
   after a re-keying spec change would create duplicates/orphans). There is no
   per-source spec-addition lane.

2. **Already frozen anyway:** the stored config sentinel in
   `LIBRARY_META."CONNECT".CONNECT_WATERMARK` (`__CONFIG__` row) is
   `f233aaad571d23ff8ec328f4f871b054`, but the current repo computes
   `da3181695496dcd81adf2a5d04a83be7`. The specs have ALREADY drifted since the
   last full rebuild (the post-rebuild additions — e.g. the
   FED_USASPENDING_CONTRACTS_FULL_R2 spec with its own DUNS extra_key — are in
   the file but not in the pinned config). Incremental ingest is refused today,
   before any DUNS work. This is also why the contracts table's DUNS extra_key
   (507K distinct) is spec'd but absent from the entity index — it is queued
   behind the same rebuild.

Note: the 2026-08 batch flag (`ENABLE_SPINE_BATCH_2026_08`) is already `True`
in `connect/keys.py` and its keys are live in the index (per the audit), so
that batch's rebuild happened; this drift is *newer* spec additions. The flag
was NOT touched.

Per the fix brief's rule ("if only the frozen path exists, implement nothing"),
no edit was made — staging it would only widen the fingerprint drift outside
the rebuild session that owns it.

## 3. Exactly what the rebuild session must do

1. **One-line spec edit** in `connect/entity_index_specs.py`, in the existing
   `FED_USASPENDING_ASSISTANCE_FULL` spec (~line 346, main DISPLAY_SPECS, not
   flag-gated), following the exact NIH Reporter / SBIR / CONTRACTS_FULL_R2
   pattern (same-row UEI+DUNS = same recipient = sanctioned extra_keys use):

   ```python
   "FED_USASPENDING_ASSISTANCE_FULL": {
       "key": "UEI", "key_col": "recipient_uei",
       "org": "recipient_name",
       "authority": 6,
       "extra_keys": [{"key": "DUNS", "key_col": "recipient_duns"}],
   },
   ```

   (`recipient_parent_duns` stays out — parent company, different entity.)

2. Run the full rebuild: `python -m connect spine` (X-Small ≈ 4.5h / $10–15 —
   RED-lane money, price it to Chris first), then
   `python -m connect.incremental seed` to re-pin the config sentinel.

3. This one rebuild also flushes the *already-pending* drift, so the contracts
   table's 507K-distinct DUNS extra_key lands in the same pass — after it, the
   DUNS family should hold roughly 478K (assistance) + 507K (contracts) + the
   existing 36K, heavily overlapping, and the 94% orphan rate should collapse
   to ~0%.

4. Post-rebuild check: rerun the §5 orphan query from `join_layer.md`
   (KEYSET_LIVE DUNS distinct vs ENTITY_INDEX DUNS) and confirm ~0%.
