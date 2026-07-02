"""Close the verifier-reach gap: grant the read-only MCP role SELECT on LIBRARY_STAGING.

THE BUG THIS FIXES (found in the trust-features pass): the read-only role CLAUDE_MCP_READONLY
is granted on LANDING / REGISTRY / MARTS (scripts/grant_mcp_readonly_catalog.py) but NOT on
LIBRARY_STAGING. The flagship detector `banned_but_paid` (~96% of all leads) reads its right side
from LIBRARY_STAGING.DBT_CROGERS.INT_OPEN_PAYMENTS_ALL_YEARS. So today a hostile skeptic using the
read-only role LITERALLY CANNOT SELECT the evidence table for the most important rule — the receipt's
"run it yourself" fails on the leads that matter most. Read-only grants only. Idempotent.

PREVIEW BY DEFAULT (prints the GRANT statements, runs nothing):
    python3 scripts/grant_mcp_readonly_staging.py
APPLY (runs them; needs a role with MANAGE GRANTS / ACCOUNTADMIN):
    python3 scripts/grant_mcp_readonly_staging.py --apply
"""
import sys
import warnings

warnings.filterwarnings("ignore")
sys.path.insert(0, "c:/Code/Ripple_v6/library-onboarding")
from snow import connect  # noqa: E402

ROLE = "CLAUDE_MCP_READONLY"
STAGING_DB = "LIBRARY_STAGING"
# the flagship evidence object the read-only role must be able to reach (the verify target)
FLAGSHIP = f"{STAGING_DB}.DBT_CROGERS.INT_OPEN_PAYMENTS_ALL_YEARS"

GRANTS = [
    f"GRANT USAGE ON DATABASE {STAGING_DB} TO ROLE {ROLE}",
    f"GRANT USAGE ON ALL SCHEMAS IN DATABASE {STAGING_DB} TO ROLE {ROLE}",
    f"GRANT USAGE ON FUTURE SCHEMAS IN DATABASE {STAGING_DB} TO ROLE {ROLE}",
    f"GRANT SELECT ON ALL TABLES IN DATABASE {STAGING_DB} TO ROLE {ROLE}",
    f"GRANT SELECT ON FUTURE TABLES IN DATABASE {STAGING_DB} TO ROLE {ROLE}",
    f"GRANT SELECT ON ALL VIEWS IN DATABASE {STAGING_DB} TO ROLE {ROLE}",
    f"GRANT SELECT ON FUTURE VIEWS IN DATABASE {STAGING_DB} TO ROLE {ROLE}",
]


def main() -> int:
    apply = "--apply" in sys.argv
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(f"SHOW ROLES LIKE '{ROLE}'")
        if not cur.fetchall():
            print(f"[SKIP] role {ROLE} not found — nothing to grant.")
            return 0

        print(f"{'APPLYING' if apply else 'PREVIEW (no changes)'} — read-only grants on {STAGING_DB}:\n")
        for g in GRANTS:
            print(f"   {g}")
            if apply:
                cur.execute(g)
        if not apply:
            print("\nPreview only. Re-run with --apply to grant. Then the read-only role can reach\n"
                  f"the flagship evidence ({FLAGSHIP}) and `connect receipt --check` works end-to-end.")
            return 0

        # as-role verify: prove the role can now actually SELECT the flagship evidence object.
        print("\n[VERIFY] confirming the role can reach the flagship evidence as itself…")
        try:
            cur.execute(f"USE ROLE {ROLE}")
            cur.execute(f"SELECT COUNT(*) FROM {FLAGSHIP}")
            n = cur.fetchone()[0]
            print(f"[VERIFY] ✓ {ROLE} SELECTed {FLAGSHIP}: {n:,} rows. The skeptic can now reproduce "
                  "the flagship leads.")
        except Exception as exc:
            print(f"[VERIFY] ✗ still unreachable: {type(exc).__name__}: {exc}\n"
                  "          (a warehouse may be needed for the role, or the schema name differs — "
                  "check SHOW SCHEMAS IN DATABASE LIBRARY_STAGING.)")
        finally:
            cur.execute("USE ROLE ACCOUNTADMIN")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
