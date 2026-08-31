# The Reading Room

Analyst-grade review surface over the Library's leads — two desks, one app.
Zero AI anywhere in this layer — runs air-gapped from every AI company on
earth (enforced by `tests/test_reading_room_ai_free.py`). For live counts,
query `LIBRARY_META.REGISTRY.V_STATE` — never trust a number pasted in prose
(POLICY v_state_numbers_only).

## The two desks

| desk | grain | detectors | verdict target |
|---|---|---|---|
| **Case Desk** | one person/entity, every claim about them in one case file | the hard-ID detectors (LEIE/SAM/OFAC/SEC joins) | per-lead (`TARGET_KIND='lead'`) — each claim decided on its own receipt |
| **Pattern Desk** | one peer cohort (NAICS-4 x size band), member establishments as receipts | `osha_cohort_outlier_2024` | per-cohort (`TARGET_KIND='cohort'`) — one verdict covers members with no individual decision |

Inheritance is **specific-beats-general** (`LIBRARY_META.REVIEW.
V_EFFECTIVE_LEAD_DECISIONS`): a lead-level decision always wins for that
lead; the cohort verdict fills the gaps. `needs_work` is non-suppressing at
both levels. Neither desk can write `published` — that stays a separate
per-lead act via `scripts/publish_lead.py` (two-step gate, beta ruling B1).

## Run

```bash
pip install -r reading_room/requirements.txt   # once
./reading_room/run.sh                          # -> http://127.0.0.1:8890
```

## The two lanes

| lane | credential | role | can do |
|---|---|---|---|
| reader | `SNOWFLAKE_SERVE_PAT` | `RIPPLE_READER` | SELECT on the queue marts, decision views, safe leads view, landing records |
| writer | `RIPPLE_REVIEW_PAT` | `RIPPLE_REVIEW_WRITER` | INSERT + SELECT on `LIBRARY_META.REVIEW.DECISIONS` — nothing else |

Append-only is enforced by the DATABASE (the writer role holds no
UPDATE/DELETE/TRUNCATE/DDL), not by this app. If `RIPPLE_REVIEW_PAT` is
missing or expired the app runs read-only with a banner and never falls
back to another credential. That rule has no exceptions.

## Provisioning order (Chris, in Snowsight)

1. `scripts/provision_review_lane.sql` — schema, table, role, grants (A14).
2. Mint the PAT restricted to `RIPPLE_REVIEW_WRITER` → `.env` as
   `RIPPLE_REVIEW_PAT`; prove the wall with
   `scripts/verify_review_lane.sql` as that role.
3. `scripts/provision_pattern_desk.sql` — cohort decision views, the
   effective-decisions inheritance view, v1-vessel retirement, grants (A15).
4. `library-onboarding/ripple_dbt/build_review.bat` — builds LEAD_QUEUE,
   COHORT_QUEUE, CASE_QUEUE. **Never a bare `dbt build`** — the wrapper
   forces UTF-8 (audit F1: a cp1252 read shipped mojibake em-dashes into
   every headline; `tests/assert_no_mojibake.sql` fails such a build now).

## Layout

```
app.py           router only — desk switch, portfolio header, lane banners
case_desk.py     Case Desk UI (person-grouped, per-lead decision forms)
pattern_desk.py  Pattern Desk UI (cohort case files, cohort decision form)
ui_common.py     shared plumbing: lanes, read helper, write-confirm-flash
connections.py   the two lanes; load_dotenv(override=True); no-fallback rule
queries.py       ALL SQL, parameterized (bind variables only)
render.py        case-file helpers, pure functions
```

Offline tests: `pytest tests/test_reading_room_offline.py
tests/test_pattern_desk_offline.py tests/test_decision_inheritance_sql.py
tests/test_cohort_queue_parity.py tests/test_reading_room_ai_free.py`
(no network, mocked lanes).
