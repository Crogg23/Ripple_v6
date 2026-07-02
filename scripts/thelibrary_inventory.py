"""C1.5a -- build the DATASET inventory that drives the Reading Room.

A "dataset" = one thing that gets a friendly view:
  - every physical mart (best layer = the mart), OR
  - a named landing source that has NO real mart (best layer = the landing table).
Sources whose data lives in a mart are represented by the mart (their raw landing
table is recorded as LANDING_FQN, not a second dataset).

Deterministic here: friendly_domain (mart-name prefix -> FACET_VOCAB, POLITICS by
keyword, CORE dims -> geo_demographics), best-layer FQN, columns. The creative bits
(friendly_name, one-liner, Cox-voice comment) are added by the content workflow.

Writes outputs/thelibrary_inventory.json.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

_LIB = Path(__file__).resolve().parents[1] / "library-onboarding"
sys.path.insert(0, str(_LIB))
from snow import connect  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "outputs" / "thelibrary_inventory.json"

# mart-name prefix (before '__') -> FACET_VOCAB domain
PREFIX_DOMAIN = {
    "HEALTH": "health_medicine", "MARITIME": "transport_movement",
    "PROCUREMENT": "procurement_intl", "JUSTICE": "justice_courts",
    "ECONOMICS": "economy_labor_trade", "ENERGY": "energy_environment",
    "FOREIGN_INFLUENCE": "targeted_investigation", "REGULATORY": "government_power",
    "HOUSING": "housing_social", "SCIENCE_RESEARCH": "science_research",
    "GOVERNANCE": "government_power", "MONEY": "money_finance",
    "JUDICIARY": "justice_courts", "CONSUMER_PROTECTION": "government_power",
    "HISTORY": "history_culture", "GOVERNMENT_RECORDS": "government_power",
    "CIVIL_RIGHTS": "justice_courts", "CORPORATE_REGISTRY": "corporate_entities",
    "LEGAL_ENFORCEMENT": "justice_courts", "REGULATION": "government_power",
    "HISTORICAL_RECORDS": "history_culture", "REVENUE": "money_finance",
}


def politics_domain(tbl: str) -> str:
    n = tbl.upper()
    if any(k in n for k in ("FEC", "DONATION", "MONEY", "PAC")):
        return "money_in_politics"
    if "WHO_WON" in n or "ELECTION" in n:
        return "elections_voting"
    if any(k in n for k in ("FJC", "JUDGE", "SCOTUS", "JCS", "APPOINTMENT")):
        return "justice_courts"
    return "government_power"


def mart_domain(schema: str, tbl: str) -> str:
    if schema == "POLITICS":
        return politics_domain(tbl)
    if schema == "EPSTEIN":
        return "targeted_investigation"
    if schema == "CORE":
        return "geo_demographics"
    if "__" in tbl:
        return PREFIX_DOMAIN.get(tbl.split("__", 1)[0], "targeted_investigation")
    return "targeted_investigation"


def q(cur, sql):
    cur.execute(sql)
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def main():
    conn = connect(); cur = conn.cursor()

    # catalog metadata per source
    cat = {r["SOURCE_ID"]: r for r in q(cur, """
        SELECT source_id, name, description, domain_primary, join_keys_std, join_key_tier,
               is_sample, landed_row_count, mart_row_count, last_ingested_at, url, publisher,
               _real_mart, lifecycle
        FROM LIBRARY_META.REGISTRY.CATALOG""")}

    # columns in bulk (1 query per db)
    def cols_by_table(db):
        out = {}
        for r in q(cur, f"""SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME
                            FROM {db}.INFORMATION_SCHEMA.COLUMNS
                            WHERE TABLE_SCHEMA NOT IN ('INFORMATION_SCHEMA')
                            ORDER BY ORDINAL_POSITION"""):
            out.setdefault((r["TABLE_SCHEMA"], r["TABLE_NAME"]), []).append(r["COLUMN_NAME"])
        return out
    mart_cols = cols_by_table("LIBRARY_MARTS")
    land_cols = cols_by_table("LIBRARY_RAW")

    # physical marts (exclude restore/backup schemas)
    marts = q(cur, """SELECT TABLE_SCHEMA, TABLE_NAME, ROW_COUNT
                      FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
                      WHERE TABLE_TYPE='BASE TABLE'
                        AND TABLE_SCHEMA NOT IN ('INFORMATION_SCHEMA')
                        AND NOT STARTSWITH(TABLE_SCHEMA,'_')""")
    landed = {r["TABLE_NAME"].lower(): r["ROW_COUNT"] for r in q(cur, """
        SELECT TABLE_NAME, ROW_COUNT FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='LANDING'""")}

    datasets = []
    mart_covered_sources = set()

    for m in marts:
        sch, tbl = m["TABLE_SCHEMA"], m["TABLE_NAME"]
        sid = None
        if "__" in tbl:
            cand = tbl.split("__", 1)[1].lower()
            if cand in cat or cand in landed:
                sid = cand
        if sid:
            mart_covered_sources.add(sid)
        meta = cat.get(sid, {}) if sid else {}
        landing_fqn = f"LIBRARY_RAW.LANDING.{sid.upper()}" if (sid and sid in landed) else None
        datasets.append({
            "kind": "mart",
            "object_fqn": f"LIBRARY_MARTS.{sch}.{tbl}",
            "landing_fqn": landing_fqn,
            "source_id": sid,
            "physical_name": tbl,
            "friendly_domain": mart_domain(sch, tbl),
            "row_count": m["ROW_COUNT"],
            "name": meta.get("NAME") or tbl,
            "description": meta.get("DESCRIPTION"),
            "join_keys": meta.get("JOIN_KEYS_STD"),
            "join_key_tier": meta.get("JOIN_KEY_TIER"),
            "is_sample": bool(meta.get("IS_SAMPLE")),
            "last_ingested_at": str(meta.get("LAST_INGESTED_AT")) if meta.get("LAST_INGESTED_AT") else None,
            "url": meta.get("URL"), "publisher": meta.get("PUBLISHER"),
            "columns": mart_cols.get((sch, tbl), []),
        })

    # named landing sources with NO mart (skip PORTAL_ firehose + mart-covered)
    for sid, meta in cat.items():
        if meta.get("LIFECYCLE") not in ("landed", "modeled"):
            continue
        if sid in mart_covered_sources:
            continue
        if sid.startswith("portal_"):
            continue
        if sid not in landed:
            continue
        upper = sid.upper()
        datasets.append({
            "kind": "landing",
            "object_fqn": f"LIBRARY_RAW.LANDING.{upper}",
            "landing_fqn": f"LIBRARY_RAW.LANDING.{upper}",
            "source_id": sid,
            "physical_name": upper,
            "friendly_domain": meta.get("DOMAIN_PRIMARY") or "targeted_investigation",
            "row_count": meta.get("LANDED_ROW_COUNT"),
            "name": meta.get("NAME") or upper,
            "description": meta.get("DESCRIPTION"),
            "join_keys": meta.get("JOIN_KEYS_STD"),
            "join_key_tier": meta.get("JOIN_KEY_TIER"),
            "is_sample": bool(meta.get("IS_SAMPLE")),
            "last_ingested_at": str(meta.get("LAST_INGESTED_AT")) if meta.get("LAST_INGESTED_AT") else None,
            "url": meta.get("URL"), "publisher": meta.get("PUBLISHER"),
            "columns": land_cols.get(("LANDING", upper), []),
        })

    OUT.write_text(json.dumps(datasets, indent=2, default=str), encoding="utf-8")

    from collections import Counter
    print(f"datasets: {len(datasets)}  (marts={sum(1 for d in datasets if d['kind']=='mart')}, "
          f"mart-less landing={sum(1 for d in datasets if d['kind']=='landing')})")
    print("\nby friendly_domain:")
    for dom, n in Counter(d["friendly_domain"] for d in datasets).most_common():
        print(f"   {dom:24} {n}")
    print(f"\nsamples flagged: {sum(1 for d in datasets if d['is_sample'])}")
    print(f"wrote -> {OUT}")
    cur.close(); conn.close()


if __name__ == "__main__":
    main()
