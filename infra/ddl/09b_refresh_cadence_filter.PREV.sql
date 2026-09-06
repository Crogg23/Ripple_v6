CREATE OR REPLACE PROCEDURE "RIPPLE_REFRESH_ENABLED"()
RETURNS VARCHAR
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'run'
COMMENT='Refresh every ENABLED + SCHEDULABLE source in BULK_REFRESH via RIPPLE_REFRESH_SOURCE. Called by the RIPPLE_BULK_REFRESH_TASK.'
EXECUTE AS OWNER
AS '
import json


def run(session):
    rows = session.sql(
        "SELECT SOURCE_ID FROM LIBRARY_META.REGISTRY.BULK_REFRESH "
        "WHERE ENABLED = TRUE AND SCHEDULABLE = TRUE ORDER BY SOURCE_ID").collect()
    out = []
    for r in rows:
        sid = r[0]
        try:
            res = session.sql(
                f"CALL LIBRARY_META.REGISTRY.RIPPLE_REFRESH_SOURCE(''{sid}'')").collect()
            out.append(json.loads(res[0][0]))
        except Exception as e:
            out.append({"source_id": sid, "status": f"ERROR: {str(e)[:150]}"})
    return json.dumps({"refreshed": len(out), "results": out})
';