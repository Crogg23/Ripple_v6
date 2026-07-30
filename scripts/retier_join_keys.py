"""Derive JOIN_KEYS_STD and JOIN_KEY_TIER from what the marts actually contain.

Why: 74 sources were marked STEEL or GEO tier with an EMPTY JOIN_KEYS_STD array. The
tier was asserted without naming a single key, so "connectable" could not be checked --
and where it was checked it was sometimes wrong (fed_va_allcause_mortality claimed GEO
while its only columns are FIGURES_AND_TABLES / COL_1 / COL_2).

This looks at the real mart columns, keeps only keys that are actually populated
(COUNT(DISTINCT) > 1 and non-blank, because a column full of '' or 'N/A' has already
faked a 100%-populated reading twice on this platform), and rewrites both the key list
and the tier from the evidence.

Tiers: STEEL = a hard entity identifier. GEO = geography only. NONE = neither.

Usage:
    python scripts/retier_join_keys.py            # report only
    python scripts/retier_join_keys.py --apply
"""
import argparse
import collections
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _snowflake_conn as sc  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Tier strength, used only to tell an upgrade from a downgrade. The registry uses five
# values, not the three the handoff described: STRONG (365 sources) sits alongside
# STEEL as a hard-identifier tier, so it is ranked equal and never silently downgraded.
RANK = {"NONE": 0, "PROBABILISTIC": 1, "GEO": 2, "STEEL": 3, "STRONG": 3}

# Hard identifiers. Key = canonical name, value = accepted column names.
STEEL_KEYS = {
    "NPI": ["NPI", "PRESCRIBER_NPI", "PRSCRBR_NPI", "REFERRING_NPI", "SUPPLIER_NPI",
            "RNDRNG_NPI", "COVERED_RECIPIENT_NPI"],
    "EIN": ["EIN", "EMPLOYER_IDENTIFICATION_NUMBER", "TAX_ID"],
    "CIK": ["CIK", "CENTRAL_INDEX_KEY", "CIK_NUMBER"],
    "LEI": ["LEI", "LEI_CODE", "LEGAL_ENTITY_IDENTIFIER"],
    "CUSIP": ["CUSIP", "CUSIP_NUMBER"],
    "UEI": ["UEI", "RECIPIENT_UEI", "AWARDEE_UEI", "UNIQUE_ENTITY_ID"],
    "DEA_NO": ["DEA_NO", "DEA_NUMBER", "REPORTER_DEA_NO", "BUYER_DEA_NO"],
    "CCN": ["CCN", "PROVIDER_CCN", "FEDERAL_PROVIDER_NUMBER", "PRVDR_NUM",
            "CMS_CERTIFICATION_NUMBER"],
    "BIOGUIDE": ["BIOGUIDE", "BIOGUIDE_ID"],
    "ICPSR": ["ICPSR", "ICPSR_ID"],
    "IMO": ["IMO", "IMO_NUMBER"],
    "FRS_ID": ["FRS_ID", "REGISTRY_ID"],
    "PWSID": ["PWSID", "PWS_ID"],
    "MINE_ID": ["MINE_ID", "MINE_ID_NUMBER"],
    "DUNS": ["DUNS", "DUNS_NUMBER"],
    "FEC_ID": ["FEC_CANDIDATE_ID", "FEC_COMMITTEE_ID", "CAND_ID", "CMTE_ID"],
    "NCES_ID": ["NCES_ID", "NCESSCH", "LEAID"],
    "ACCESSION_NUMBER": ["ACCESSION_NUMBER", "SEC_ACCESSION_NUMBER"],
    "RECALL_NUMBER": ["RECALL_NUMBER"],
    "DOCKET_ID": ["DOCKET_ID", "DOCKET_NUMBER"],
}

GEO_KEYS = {
    "FIPS": ["FIPS", "FIPS_CODE", "COUNTY_FIPS", "STATE_FIPS", "GEOID", "STATE_COUNTY_FIPS"],
    "STATE": ["STATE", "STATE_ABBR", "STATE_CODE", "STATE_NAME", "STATE_ABBREVIATION",
              "PRSCRBR_STATE_ABRVTN", "PROVIDER_STATE", "RECIPIENT_STATE_CODE"],
    "ZIP": ["ZIP", "ZIPCODE", "ZIP_CODE", "POSTAL_CODE", "ZIP5"],
    "COUNTY": ["COUNTY", "COUNTY_NAME"],
    "COUNTRY": ["COUNTRY", "COUNTRY_CODE", "COUNTRY_NAME"],
    "CENSUS_TRACT": ["CENSUS_TRACT", "TRACT", "TRACT_FIPS"],
}

# Values that look populated but mean nothing.
SENTINELS = ("", " ", "N/A", "NA", "NULL", "NONE", "UNKNOWN", "0", "-", "--",
             "NOT AVAILABLE", "NOT APPLICABLE")


def mart_relations(cur):
    """source_id -> (schema, table, {COLUMN}) for the largest mart per source."""
    cur.execute("""
        select c.table_schema, c.table_name, c.column_name, coalesce(t.row_count, 0)
        from LIBRARY_MARTS.information_schema.columns c
        join LIBRARY_MARTS.information_schema.tables t
          on t.table_schema = c.table_schema and t.table_name = c.table_name
        where c.table_schema not in ('INFORMATION_SCHEMA','DBT_CROGERS','_RESTORE_20260701')
          and position('__' in c.table_name) > 0
    """)
    acc = collections.defaultdict(lambda: {"cols": set(), "rows": 0})
    for schema, table, col, rows in cur.fetchall():
        sid = table.split("__", 1)[1].lower()
        entry = acc[(sid, schema, table)]
        entry["cols"].add(col.upper())
        entry["rows"] = rows
    best = {}
    for (sid, schema, table), e in acc.items():
        if sid not in best or e["rows"] > best[sid][2]:
            best[sid] = (schema, table, e["rows"], e["cols"])
    return best


def populated(cur, schema, table, column, rows):
    """True if the column holds more than one real, non-sentinel value."""
    limit = "sample (200000 rows)" if rows and rows > 500_000 else ""
    sent = ", ".join(f"'{s}'" for s in SENTINELS)
    cur.execute(f'''
        select count(distinct v) from (
          select upper(trim(to_varchar("{column}"))) as v
          from LIBRARY_MARTS."{schema}"."{table}" {limit}
        ) where v is not null and v not in ({sent})
    ''')
    return (cur.fetchone()[0] or 0) > 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only-empty", action="store_true",
                    help="only touch sources whose JOIN_KEYS_STD is empty")
    args = ap.parse_args()

    conn = sc.connect()
    cur = conn.cursor()
    cur.execute("""
        select SOURCE_ID, JOIN_KEY_TIER, JOIN_KEYS_STD
        from LIBRARY_META.REGISTRY.CATALOG
        where LIFECYCLE = 'modeled'
    """)
    sources = []
    for sid, tier, keys in cur.fetchall():
        parsed = json.loads(keys) if keys else []
        if args.only_empty and parsed:
            continue
        sources.append((sid, tier, parsed))

    marts = mart_relations(cur)
    print(f"{len(sources)} modeled sources to evaluate, "
          f"{len(marts)} mart relations indexed\n")

    changes, unchanged, nomart = [], 0, 0
    for sid, tier, _keys in sources:
        rel = marts.get(sid.lower())
        if not rel:
            nomart += 1
            continue
        schema, table, rows, cols = rel
        found_steel, found_geo = [], []
        for canon, variants in STEEL_KEYS.items():
            hit = next((v for v in variants if v in cols), None)
            if hit and populated(cur, schema, table, hit, rows):
                found_steel.append(canon)
        for canon, variants in GEO_KEYS.items():
            hit = next((v for v in variants if v in cols), None)
            if hit and populated(cur, schema, table, hit, rows):
                found_geo.append(canon)
        new_keys = sorted(set(found_steel + found_geo))
        new_tier = "STEEL" if found_steel else ("GEO" if found_geo else "NONE")
        if new_tier != tier or new_keys != sorted(set(_keys)):
            changes.append((sid, tier, new_tier, new_keys))
        else:
            unchanged += 1

    downgrades = [c for c in changes if RANK.get(c[2], 0) < RANK.get(c[1], 0)]
    safe = [c for c in changes if RANK.get(c[2], 0) >= RANK.get(c[1], 0)]
    print(f"unchanged: {unchanged}   no mart: {nomart}   changing: {len(changes)}")
    print(f"   SAFE  (tier held or upgraded, key list filled in): {len(safe)}")
    print(f"   REVIEW (would downgrade the tier):                 {len(downgrades)}")
    print("\nsample of safe changes:")
    for sid, old, new, keys in safe[:20]:
        print(f"   {old:5} -> {new:5}  {sid:52} {keys}")

    # Downgrades are NOT applied. The key catalog above is known to be incomplete --
    # CMS nursing homes key on PROVNUM, FDA FAERS on PRIMARYID/CASEID, the FAA registry
    # on tail number, and none of those are listed here. Auto-downgrading on a
    # not-found would just swap one wrong answer for another, so these go to a review
    # file instead. Add the missing names to STEEL_KEYS/GEO_KEYS and re-run to clear.
    review = os.path.join(REPO, "outputs", "join_key_tier_review.csv")
    os.makedirs(os.path.dirname(review), exist_ok=True)
    with open(review, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["source_id", "current_tier", "detected_tier", "detected_keys"])
        for sid, old, new, keys in sorted(downgrades):
            w.writerow([sid, old, new, ";".join(keys)])
    print(f"\n{len(downgrades)} possible downgrades written to {review} (NOT applied)")

    if args.apply:
        for sid, _old, new_tier, new_keys in safe:
            cur.execute(
                "update LIBRARY_META.REGISTRY.SOURCE_REGISTRY "
                "set JOIN_KEY_TIER = %s, JOIN_KEYS_STD = parse_json(%s) "
                "where lower(SOURCE_ID) = %s",
                (new_tier, json.dumps(new_keys), sid.lower()),
            )
        print(f"applied {len(safe)} registry updates (downgrades skipped)")
    else:
        print("DRY RUN -- rerun with --apply to update the registry")
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
