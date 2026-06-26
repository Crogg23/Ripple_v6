"""Pass 0h of the faceted-catalog build: grant the read-only MCP role (CLAUDE_MCP_READONLY)
SELECT on the data the CATALOG view points at, so the Snowflake MCP server can actually query it.
Read-only grants only. Idempotent. Run as a role with MANAGE GRANTS / ACCOUNTADMIN.

    python3 scripts/grant_mcp_readonly_catalog.py
"""
import sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, "/Users/chrisr./Documents/GitHub/Ripple_v6/library-onboarding")
from snow import connect

conn = connect(); cur = conn.cursor()
def ex(sql): cur.execute(sql)
def scalar(sql):
    cur.execute(sql); r = cur.fetchone(); return r[0] if r else None

cur.execute("SHOW ROLES LIKE 'CLAUDE_MCP_READONLY'")
if not cur.fetchall():
    print("[SKIP] role CLAUDE_MCP_READONLY not found"); conn.close(); sys.exit(0)

grants = [
    "GRANT USAGE ON DATABASE LIBRARY_RAW TO ROLE CLAUDE_MCP_READONLY",
    "GRANT USAGE ON SCHEMA LIBRARY_RAW.LANDING TO ROLE CLAUDE_MCP_READONLY",
    "GRANT SELECT ON ALL TABLES IN SCHEMA LIBRARY_RAW.LANDING TO ROLE CLAUDE_MCP_READONLY",
    "GRANT SELECT ON FUTURE TABLES IN SCHEMA LIBRARY_RAW.LANDING TO ROLE CLAUDE_MCP_READONLY",
    "GRANT USAGE ON DATABASE LIBRARY_META TO ROLE CLAUDE_MCP_READONLY",
    "GRANT USAGE ON SCHEMA LIBRARY_META.REGISTRY TO ROLE CLAUDE_MCP_READONLY",
    "GRANT SELECT ON ALL TABLES IN SCHEMA LIBRARY_META.REGISTRY TO ROLE CLAUDE_MCP_READONLY",
    "GRANT SELECT ON FUTURE TABLES IN SCHEMA LIBRARY_META.REGISTRY TO ROLE CLAUDE_MCP_READONLY",
    "GRANT SELECT ON ALL VIEWS IN SCHEMA LIBRARY_META.REGISTRY TO ROLE CLAUDE_MCP_READONLY",
    "GRANT SELECT ON FUTURE VIEWS IN SCHEMA LIBRARY_META.REGISTRY TO ROLE CLAUDE_MCP_READONLY",
    "GRANT USAGE ON DATABASE LIBRARY_MARTS TO ROLE CLAUDE_MCP_READONLY",
    "GRANT USAGE ON ALL SCHEMAS IN DATABASE LIBRARY_MARTS TO ROLE CLAUDE_MCP_READONLY",
    "GRANT USAGE ON FUTURE SCHEMAS IN DATABASE LIBRARY_MARTS TO ROLE CLAUDE_MCP_READONLY",
    "GRANT SELECT ON ALL TABLES IN DATABASE LIBRARY_MARTS TO ROLE CLAUDE_MCP_READONLY",
    "GRANT SELECT ON FUTURE TABLES IN DATABASE LIBRARY_MARTS TO ROLE CLAUDE_MCP_READONLY",
    "GRANT SELECT ON ALL VIEWS IN DATABASE LIBRARY_MARTS TO ROLE CLAUDE_MCP_READONLY",
    "GRANT SELECT ON FUTURE VIEWS IN DATABASE LIBRARY_MARTS TO ROLE CLAUDE_MCP_READONLY",
]
ok = 0
for g in grants:
    try: ex(g); ok += 1
    except Exception as e: print(f"  ERR {g[:60]}... -> {e}")
print(f"[{'PASS' if ok==len(grants) else 'WARN'}] {ok}/{len(grants)} grants applied")

try:
    ex("USE ROLE CLAUDE_MCP_READONLY")
    n1 = scalar("SELECT COUNT(*) FROM LIBRARY_RAW.LANDING.FED_OYEZ")
    n2 = scalar("SELECT COUNT(*) FROM LIBRARY_META.REGISTRY.CATALOG")
    n3 = scalar("SELECT COUNT(*) FROM LIBRARY_META.REGISTRY.V_SOURCE_KEY WHERE JOIN_KEY='IMO'")
    print(f"[{'PASS' if all(x is not None for x in (n1,n2,n3)) else 'FAIL'}] read-role can query: "
          f"OYEZ={n1}, CATALOG={n2}, vessel-key rows={n3}")
except Exception as e:
    print(f"[FAIL] read-role verify: {e}")
finally:
    ex("USE ROLE ACCOUNTADMIN")
conn.close()
print("PASS 0h COMPLETE")
