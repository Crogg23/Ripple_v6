"""Build THE_LIBRARY reading room + the friendly layer (C1 + C1.5b + A2 + C2 + C3).

Consumes:
  outputs/thelibrary_inventory.json   (structural, from thelibrary_inventory.py)
  outputs/thelibrary_content.json     (friendly_name/one_liner/comment, from the content workflow)

Does (all idempotent; preview unless --apply):
  C1.5b  LIBRARY_META.REGISTRY.FRIENDLY_LAYER  -- one row per dataset, the source of truth
  A2     COMMENT ON TABLE for each dataset's object (+ its raw landing table if distinct)
  C1     CREATE DATABASE THE_LIBRARY + one schema per friendly domain present
  C2     CREATE OR REPLACE VIEW per dataset (concept name), then PRUNE orphaned views
  C3     THE_LIBRARY.PUBLIC.START_HERE master index
  A3     (--portals) templated comments on the 655 PORTAL_ firehose tables

Usage:
  python scripts/thelibrary_build.py                 # preview
  python scripts/thelibrary_build.py --apply         # build the reading room
  python scripts/thelibrary_build.py --apply --portals   # + portal comments
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "library-onboarding"))
from snow import connect  # noqa: E402

APPLY = "--apply" in sys.argv
PORTALS = "--portals" in sys.argv
INV = _ROOT / "outputs" / "thelibrary_inventory.json"
CONTENT = _ROOT / "outputs" / "thelibrary_content.json"

DB = "THE_LIBRARY"
DOMAIN_SCHEMA = {
    "health_medicine": "HEALTH", "government_power": "GOVERNMENT", "justice_courts": "JUSTICE",
    "money_in_politics": "CAMPAIGN_FINANCE", "money_finance": "MONEY", "crime_security": "CRIME_SECURITY",
    "economy_labor_trade": "ECONOMY", "targeted_investigation": "INVESTIGATIONS",
    "corporate_entities": "COMPANIES", "geo_demographics": "GEOGRAPHY",
    "energy_environment": "ENERGY_ENVIRONMENT", "elections_voting": "ELECTIONS",
    "history_culture": "HISTORY", "science_research": "SCIENCE", "housing_social": "HOUSING",
    "spending_budget": "GOVERNMENT_SPENDING", "sanctions_enforcement": "SANCTIONS",
    "procurement_intl": "PROCUREMENT", "transport_movement": "TRANSPORT",
    "immigration_migration": "IMMIGRATION", "open_data_portal": "OPEN_DATA",
    "education": "EDUCATION", "UNCLASSIFIED": "MISC",
}


def ident(s: str, fallback: str) -> str:
    s = re.sub(r"[^A-Za-z0-9_]", "_", (s or "").upper()).strip("_")
    s = re.sub(r"_+", "_", s)
    if not s or not s[0].isalpha():
        s = "X_" + s if s else fallback
    return s[:80]


def esc(s):
    return (s or "").replace("'", "''")


def q(cur, sql):
    cur.execute(sql)
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def run(cur, sql, label=""):
    if APPLY:
        try:
            cur.execute(sql)
        except Exception as e:
            print(f"   ERROR {label}: {str(e)[:160]}")
            print(f"      SQL: {sql[:200]}")


def main():
    if not CONTENT.exists():
        print(f"MISSING {CONTENT} -- run the content workflow first."); return
    inv = {d["object_fqn"]: d for d in json.loads(INV.read_text(encoding="utf-8"))}
    content = {c["object_fqn"]: c for c in json.loads(CONTENT.read_text(encoding="utf-8"))}
    missing = set(inv) - set(content)
    if missing:
        print(f"WARN: {len(missing)} datasets have no generated content; using fallbacks:")
        for m in list(missing)[:10]:
            print("   ", m)

    # ---- merge + resolve schema + collision-safe names -------------------
    rows = []
    for fqn, d in inv.items():
        c = content.get(fqn, {})
        schema = DOMAIN_SCHEMA.get(d["friendly_domain"], "MISC")
        base = ident(c.get("friendly_name") or d["physical_name"], d["physical_name"])
        rows.append({
            "object_fqn": fqn, "landing_fqn": d.get("landing_fqn"), "source_id": d.get("source_id"),
            "layer": d["kind"], "friendly_schema": schema, "friendly_name": base,
            "friendly_domain": d["friendly_domain"], "one_liner": c.get("one_liner") or (d.get("description") or d["name"]),
            "comment": c.get("comment") or (d.get("description") or d["name"]),
            "is_sample": bool(d.get("is_sample")), "row_count": d.get("row_count"),
        })
    # de-collide within (schema, name): deterministic order, suffix with source stem
    seen = {}
    for r in sorted(rows, key=lambda x: x["object_fqn"]):
        key = (r["friendly_schema"], r["friendly_name"])
        if key in seen:
            stem = ident((r["source_id"] or r["object_fqn"].split(".")[-1]), "X")
            r["friendly_name"] = ident(f"{r['friendly_name']}_{stem}", r["friendly_name"])[:80]
        seen[(r["friendly_schema"], r["friendly_name"])] = True
    schemas = sorted({r["friendly_schema"] for r in rows})
    print(f"datasets={len(rows)}  schemas={len(schemas)}: {schemas}")

    # ---- C1.5b FRIENDLY_LAYER -------------------------------------------
    print(f"\n[{'APPLY' if APPLY else 'PREVIEW'}] C1.5b build FRIENDLY_LAYER ({len(rows)} rows)")
    if APPLY:
        cur = conn.cursor()
        cur.execute("""CREATE OR REPLACE TABLE LIBRARY_META.REGISTRY.FRIENDLY_LAYER(
            OBJECT_FQN STRING, LANDING_FQN STRING, SOURCE_ID STRING, LAYER STRING,
            FRIENDLY_SCHEMA STRING, FRIENDLY_NAME STRING, FRIENDLY_DOMAIN STRING,
            ONE_LINER STRING, COMMENT STRING, IS_SAMPLE BOOLEAN, ROW_COUNT NUMBER,
            THE_LIBRARY_FQN STRING, GENERATED_AT TIMESTAMP_NTZ)""")
        cur.executemany(
            """INSERT INTO LIBRARY_META.REGISTRY.FRIENDLY_LAYER
               (OBJECT_FQN,LANDING_FQN,SOURCE_ID,LAYER,FRIENDLY_SCHEMA,FRIENDLY_NAME,FRIENDLY_DOMAIN,
                ONE_LINER,COMMENT,IS_SAMPLE,ROW_COUNT,THE_LIBRARY_FQN,GENERATED_AT)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP())""",
            [(r["object_fqn"], r["landing_fqn"], r["source_id"], r["layer"], r["friendly_schema"],
              r["friendly_name"], r["friendly_domain"], r["one_liner"], r["comment"], r["is_sample"],
              r["row_count"], f'{DB}.{r["friendly_schema"]}.{r["friendly_name"]}') for r in rows])
        cur.close()

    # ---- A2 comments on the physical objects ----------------------------
    print(f"[{'APPLY' if APPLY else 'PREVIEW'}] A2 comment {len(rows)} objects (+ raw landing where distinct)")
    if APPLY:
        cur = conn.cursor()
        for r in rows:
            cur.execute(f"COMMENT ON TABLE {r['object_fqn']} IS %s", (r["comment"],))
            if r["landing_fqn"] and r["landing_fqn"] != r["object_fqn"]:
                cur.execute(f"COMMENT ON TABLE {r['landing_fqn']} IS %s",
                            (r["comment"] + "  (Raw as-loaded copy; the cleaned version is in LIBRARY_MARTS.)",))
        cur.close()

    # ---- C1 database + schemas ------------------------------------------
    print(f"[{'APPLY' if APPLY else 'PREVIEW'}] C1 create {DB} + {len(schemas)} schemas")
    cur = conn.cursor()
    run(cur, f"CREATE DATABASE IF NOT EXISTS {DB} "
             f"COMMENT='The front door. Every dataset in the library under a plain-English name, "
             f"shelved by topic. Browse here; START_HERE (in PUBLIC) is the index. These are views "
             f"over the real tables -- read-only, safe, regenerated from the catalog.'", "createdb")
    for sch in schemas:
        run(cur, f"CREATE SCHEMA IF NOT EXISTS {DB}.{sch}", f"schema {sch}")

    # ---- C2 views (create-or-replace) + prune orphans -------------------
    print(f"[{'APPLY' if APPLY else 'PREVIEW'}] C2 {len(rows)} friendly views + prune")
    target = {}
    for r in rows:
        target.setdefault(r["friendly_schema"], set()).add(r["friendly_name"])
        badge = ""
        if r["is_sample"]:
            badge = f"  [Thin sample: only {r['row_count']:,} rows loaded, not the full source.]" if r["row_count"] else "  [Thin sample -- not the full source.]"
        vcomment = esc(r["comment"] + badge)
        run(cur, f'CREATE OR REPLACE VIEW {DB}.{r["friendly_schema"]}.{r["friendly_name"]} '
                 f"COMMENT='{vcomment}' AS SELECT * FROM {r['object_fqn']}",
            f'view {r["friendly_name"]}')
    if APPLY:
        for sch in schemas:
            have = {v["name"] for v in q(cur, f"SHOW VIEWS IN SCHEMA {DB}.{sch}")}
            orphans = have - target.get(sch, set())
            for o in orphans:
                print(f"   prune orphan view {DB}.{sch}.{o}")
                run(cur, f"DROP VIEW IF EXISTS {DB}.{sch}.{o}", f"prune {o}")

    # ---- C3 START_HERE ---------------------------------------------------
    print(f"[{'APPLY' if APPLY else 'PREVIEW'}] C3 START_HERE index")
    start_here = f"""CREATE OR REPLACE VIEW {DB}.PUBLIC.START_HERE
      COMMENT='The card catalog. Every dataset in plain English: what it is, how big, how fresh,
      what it links by, and where to find it. Filter by SHELF to browse a topic.' AS
    SELECT
      f.FRIENDLY_SCHEMA         AS SHELF,
      f.FRIENDLY_NAME           AS DATASET,
      f.ONE_LINER               AS WHAT_IT_IS,
      f.ROW_COUNT               AS ROW_COUNT,
      CASE WHEN f.IS_SAMPLE THEN 'sample' WHEN f.LAYER='mart' THEN 'curated' ELSE 'raw' END AS STATUS,
      f.SOURCE_ID,
      c.LAST_INGESTED_AT::date  AS LAST_UPDATED,
      c.JOIN_KEYS_STD           AS LINKS_BY,
      f.THE_LIBRARY_FQN         AS BROWSE_AT,
      f.OBJECT_FQN              AS REAL_TABLE
    FROM LIBRARY_META.REGISTRY.FRIENDLY_LAYER f
    LEFT JOIN LIBRARY_META.REGISTRY.CATALOG c ON c.SOURCE_ID = f.SOURCE_ID
    ORDER BY SHELF, DATASET"""
    run(cur, start_here, "start_here")

    # ---- A3 portal comments (optional) ----------------------------------
    if PORTALS:
        print(f"[{'APPLY' if APPLY else 'PREVIEW'}] A3 templated comments on PORTAL_ tables")
        portals = q(cur, """SELECT TABLE_NAME, ROW_COUNT FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
                            WHERE TABLE_SCHEMA='LANDING' AND STARTSWITH(TABLE_NAME,'PORTAL_')""")
        print(f"   {len(portals)} portal tables")
        for p in portals:
            txt = (f"Portal-net feed harvested from an open-data portal (~{p['ROW_COUNT']:,} rows). "
                   f"A thin sample kept because it carries an ID we can join on -- a connector for "
                   f"cross-source matching, not yet a full standalone source.")
            run(cur, f"COMMENT ON TABLE LIBRARY_RAW.LANDING.{p['TABLE_NAME']} IS %s" if False else
                     f"COMMENT ON TABLE LIBRARY_RAW.LANDING.{p['TABLE_NAME']} IS '{esc(txt)}'", "portal")

    cur.close()
    print("\nDONE." + ("" if APPLY else "  (preview -- re-run with --apply)"))


if __name__ == "__main__":
    conn = connect()
    main()
    conn.close()
