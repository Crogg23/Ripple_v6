CREATE OR REPLACE PROCEDURE LIBRARY_META.REGISTRY.RIPPLE_REFRESH_ENABLED()
RETURNS VARCHAR
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'run'
COMMENT='Refresh every ENABLED + SCHEDULABLE source in BULK_REFRESH that is DUE for its cadence. The refresh proc downloads before it compares ETags, so an unfiltered run pays full download nightly for every source.'
EXECUTE AS OWNER
AS '
import json

# How long a source may sit before the nightly driver fetches it again.
# The refresh proc downloads BEFORE it compares the origin ETag, so an
# un-filtered nightly run pays full download for every source every night.
# A monthly file was costing 30 fetches to catch one change.
PERIOD_DAYS = {
    "real_time": 1,
    "daily": 1,
    "weekly": 6,
    "monthly": 27,
    "quarterly": 85,
    "cycle": 30,
    "annual": 350,
    "static": 365,
}
DEFAULT_DAYS = 7


def run(session):
    rows = session.sql(
        "SELECT SOURCE_ID, CADENCE_BUCKET, LAST_REFRESH_AT, "
        "DATEDIFF(''day'', LAST_REFRESH_AT, CURRENT_TIMESTAMP()) AS AGE_DAYS "
        "FROM LIBRARY_META.REGISTRY.BULK_REFRESH "
        "WHERE ENABLED = TRUE AND SCHEDULABLE = TRUE ORDER BY SOURCE_ID").collect()

    due, skipped = [], []
    for r in rows:
        sid, cadence, last_at, age = r[0], (r[1] or "").lower(), r[2], r[3]
        need = PERIOD_DAYS.get(cadence, DEFAULT_DAYS)
        # Never refreshed => always due. Otherwise wait out its own period.
        if last_at is None or age is None or age >= need:
            due.append(sid)
        else:
            skipped.append({"source_id": sid, "status": "not due",
                            "cadence": cadence, "age_days": age, "period_days": need})

    out = []
    for sid in due:
        try:
            # chr(39) is a single quote. Writing it literally here means escaping
            # it for the SQL string that wraps this whole body, and getting that
            # count wrong turns the argument into a bare identifier.
            q = chr(39)
            res = session.sql(
                f"CALL LIBRARY_META.REGISTRY.RIPPLE_REFRESH_SOURCE({q}{sid}{q})").collect()
            out.append(json.loads(res[0][0]))
        except Exception as e:
            out.append({"source_id": sid, "status": f"ERROR: {str(e)[:150]}"})

    return json.dumps({"enabled": len(rows), "due": len(due),
                       "not_due": len(skipped), "results": out + skipped})
';
