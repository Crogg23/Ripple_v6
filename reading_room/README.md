# The Reading Room

Analyst-grade review surface over the Library's ~1,030 leads. One command,
a case file in plain English, three buttons. Zero AI anywhere in this layer
— runs air-gapped from every AI company on earth (enforced by
`tests/test_reading_room_ai_free.py`).

## Run

```bash
pip install -r reading_room/requirements.txt   # once
./reading_room/run.sh                          # -> http://127.0.0.1:8890
```

## The two lanes

| lane | credential | role | can do |
|---|---|---|---|
| reader | `SNOWFLAKE_SERVE_PAT` | `RIPPLE_READER` | SELECT on the queue mart, decision view, safe leads view, landing records |
| writer | `RIPPLE_REVIEW_PAT` | `RIPPLE_REVIEW_WRITER` | INSERT + SELECT on `LIBRARY_META.REVIEW.DECISIONS` — nothing else |

Append-only is enforced by the DATABASE (the writer role holds no
UPDATE/DELETE/TRUNCATE/DDL), not by this app. If `RIPPLE_REVIEW_PAT` is
missing or expired the app runs read-only with a banner and never falls
back to another credential. That rule has no exceptions.

## Provisioning order (Chris, in Snowsight)

1. `scripts/provision_review_lane.sql` — schema, table, role, grants,
   view re-points (includes the A12 safe-view refresh).
2. Mint the PAT restricted to `RIPPLE_REVIEW_WRITER` → `.env` as
   `RIPPLE_REVIEW_PAT`.
3. `scripts/verify_review_lane.sql` **as that role** — its two
   PERMISSION DENIEDs are the proof the wall holds.
4. A00 write PAT + `dbt build --select marts.review` (A13) materializes
   the queue mart.

## Layout

```
app.py          Streamlit UI only — no SQL strings here
connections.py  the two lanes; load_dotenv(override=True); no-fallback rule
queries.py      ALL SQL, parameterized (bind variables only)
render.py       case-file helpers, pure functions
```

Offline tests: `pytest tests/test_reading_room_offline.py
tests/test_reading_room_ai_free.py` (no network, mocked lanes).
