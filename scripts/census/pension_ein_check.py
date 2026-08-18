"""The owed pension tax-ID reality check (one aggregate + one sample).

The failed-pension table's EIN column has existence but no populate test, and
sentinel-masked ID columns have fooled this platform twice (NPPES EIN,
NOAA_AIS imo_number). Per CLAUDE.md section 7: COUNT + COUNT(DISTINCT) + value
sample before trusting it as a join key. Read-only.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _snowflake_conn import connect  # noqa: E402

T = 'LIBRARY_MARTS."LABOR"."LABOR__FED_PBGC_TRUSTEED_PLANS"'


def main():
    conn = connect(database="LIBRARY_MARTS")
    cur = conn.cursor()
    cur.execute(
        f"select count(*), count(ein), count(distinct ein), "
        f"min(length(to_varchar(ein))), max(length(to_varchar(ein))), "
        f"count_if(lower(to_varchar(ein)) in ('nan','none','null','n/a','na','unknown','')), "
        f"count_if(to_varchar(ein) rlike '^0+$' or to_varchar(ein) rlike '^9+$') "
        f"from {T}"
    )
    n, nn, dn, mnl, mxl, sent, repeat = cur.fetchone()
    print(f"rows={n:,} nonnull={nn:,} distinct={dn:,} len={mnl}-{mxl} "
          f"sentinel_text={sent} all-0/all-9={repeat}", flush=True)
    cur.execute(
        f"select to_varchar(ein), count(*) c from {T} group by 1 order by c desc limit 15"
    )
    print("top repeated values:")
    for v, c in cur.fetchall():
        print(f"  {v!r} x{c}")
    cur.execute(
        f"select to_varchar(ein), sponsor_name from {T} where ein is not null "
        f"order by random() limit 10"
    )
    print("random sample:")
    for v, s in cur.fetchall():
        print(f"  {v!r}  {str(s)[:50]}")
    conn.close()


if __name__ == "__main__":
    main()
