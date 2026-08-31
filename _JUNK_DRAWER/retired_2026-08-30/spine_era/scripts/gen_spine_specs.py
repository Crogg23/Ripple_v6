"""Generate connect/entity_index_specs.py DISPLAY_SPECS entries from live evidence.

WHY THIS EXISTS
The spine's scope is a hand-written Python dict (DISPLAY_SPECS). 42 sources were in
it; ~110 more had a usable hard key sitting unused in LANDING. Hand-writing 110 specs
is both slow and exactly the kind of work that produces a wrong key_col nobody
notices, so this generates them -- but never on the strength of a registry label.

THE RULE THIS SCRIPT ENFORCES (CLAUDE.md section 7)
A registry JOIN_KEY_TIER of STEEL is a CLAIM, not evidence. Before emitting a spec,
every candidate key column is checked against the real table with the normalizer the
spine will actually use:
    total rows, rows surviving normalization, DISTINCT surviving values,
    length range, a value sample, and how many values are NEW to the spine.
A key that normalizes to nothing, to one value, or to a sentinel is REJECTED to
outputs/spine_wiring_rejects.csv instead of being wired. This pass has already caught
NPPES EIN and NOAA_AIS imo_number as false positives that way, and MSHA MINE_ID as a
7-digit ID wrapped in literal double quotes that a naive width rule would key on.

Nothing here writes to Snowflake and nothing here edits the specs file. It prints a
Python block to paste (or --out to write a file) plus two CSVs of evidence, so the
actual scope change lands as a reviewable git diff -- which is also what trips
incremental.py's config fingerprint and forces a full, reconciled rebuild.

Usage:
    python scripts/gen_spine_specs.py --wave 1
    python scripts/gen_spine_specs.py --tables FED_MSHA_VIOLATIONS,FED_MSHA_ACCIDENTS
    python scripts/gen_spine_specs.py --all --out outputs/spine_specs_generated.py
"""
import argparse
import collections
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

import _snowflake_conn as sc  # noqa: E402

from connect.entity_index_specs import DISPLAY_SPECS, ENTITY_TYPE_BY_KEY  # noqa: E402
from connect.keys import NORM_RULES, normalize_sql, quote_ident  # noqa: E402

OUT_DIR = os.path.join(REPO, "outputs")

# --------------------------------------------------------------------------- #
# Key column preference. detect_key() answers "does this column carry a key?" but
# NOT "which of a table's 3 NPI-ish columns is THE one this table is about". That
# needs judgement, so it's declared: first match in this list wins.
#
# Order matters and encodes a real decision. FED_CMS_HOSPITAL_ENROLLMENTS has both
# NPI and CCN; the row is a Medicare ENROLLMENT of a provider, so NPI is primary and
# CCN rides along as an extra_key. Getting this backwards would file hospitals under
# the wrong grain.
# --------------------------------------------------------------------------- #
KEY_COL_PREFERENCE = {
    "NPI": ["NPI", "RNDRNG_NPI", "PRSCRBR_NPI", "PRESCRIBER_NPI", "REFERRING_NPI",
            "SUPPLIER_NPI", "COVERED_RECIPIENT_NPI", "ORG_NPI", "PROVIDER_NPI"],
    "CCN": ["CCN", "PROVIDER_CCN", "CMS_CERTIFICATION_NUMBER_CCN",
            "CMS_CERTIFICATION_NUMBER__CCN", "CMS_CERTIFICATION_NUMBER",
            "FEDERAL_PROVIDER_NUMBER", "PRVDR_NUM", "CAH_OR_HOSPITAL_CCN"],
    "EIN": ["EIN", "EMPLOYER_IDENTIFICATION_NUMBER", "TAX_ID", "EIN_NUMBER"],
    "CIK": ["CIK", "CENTRAL_INDEX_KEY", "CIK_NUMBER", "RPTOWNERCIK"],
    "UEI": ["UEI", "RECIPIENT_UEI", "AWARDEE_UEI", "UNIQUE_ENTITY_ID"],
    "LEI": ["LEI", "LEI_CODE", "LEGAL_ENTITY_IDENTIFIER"],
    "DEA_NO": ["DEA_NO", "DEA_NUMBER", "REPORTER_DEA_NO", "BUYER_DEA_NO"],
    "IMO": ["IMO", "IMO_NUMBER"],
    "BIOGUIDE": ["BIOGUIDE", "BIOGUIDE_ID", "SPONSOR_BIOGUIDE", "COSPONSOR_BIOGUIDE"],
    "ICPSR": ["ICPSR", "ICPSR_ID"],
    # 2026-07-30 axes. FRS_ID: ECHO spells it FRS_ID, the FRS registry spells the
    # same 12-digit value REGISTRY_ID. PWSID: SELLER_PWSID is a DIFFERENT water
    # system on the row (who sells water to this one), never this row's identity.
    "FRS_ID": ["FRS_ID", "REGISTRY_ID"],
    "PWSID": ["PWSID", "PWS_ID"],
    "MINE_ID": ["MINE_ID", "MINE_ID_NUMBER"],
    "FEC_CMTE_ID": ["CMTE_ID", "FEC_CMTE_ID", "FEC_COMMITTEE_ID", "COMMITTEE_ID"],
    "FEC_CAND_ID": ["CAND_ID", "FEC_CAND_ID", "FEC_CANDIDATE_ID", "CANDIDATE_ID"],
}

# Display-column preference, first match wins. Used for the golden-record name and
# the dossier address line -- never for joining, so a miss costs a label, not a match.
ORG_COLS = ["FACILITY_NAME", "PROVIDER_NAME", "ORGANIZATION_NAME", "ORG_NAME",
            "LEGAL_NAME", "BUSINESS_NAME", "BUSNAME", "COMPANY_NAME", "ENTITY_NAME",
            "RECIPIENT_NAME", "AWARDEE_NAME", "EMPLOYER_NAME", "ESTABLISHMENT_NAME",
            "MINE_NAME", "PWS_NAME", "PRIMARY_NAME", "FAC_NAME", "NAME",
            "CMTE_NM", "CAND_NAME", "SPONSOR_NAME", "DOING_BUSINESS_AS_NAME"]
LAST_COLS = ["PROVIDER_LAST_NAME", "LAST_NAME", "LASTNAME", "PRVDR_LAST_NAME",
             "RNDRNG_PRVDR_LAST_ORG_NAME", "PRSCRBR_LAST_ORG_NAME",
             "COVERED_RECIPIENT_LAST_NAME"]
FIRST_COLS = ["PROVIDER_FIRST_NAME", "FIRST_NAME", "FIRSTNAME", "PRVDR_FIRST_NAME",
              "RNDRNG_PRVDR_FIRST_NAME", "PRSCRBR_FIRST_NAME",
              "COVERED_RECIPIENT_FIRST_NAME"]
CITY_COLS = ["CITY", "CITY_TOWN", "CITY_NAME", "PROVIDER_CITY", "RECIPIENT_CITY",
             "RNDRNG_PRVDR_CITY", "PRSCRBR_CITY", "MAILING_CITY", "CMTE_CITY",
             "ESTABLISHMENT_CITY", "FAC_CITY"]
STATE_COLS = ["STATE", "STATE_CD", "STATE_ABBR", "STATE_CODE", "PROVIDER_STATE",
              "RECIPIENT_STATE", "RNDRNG_PRVDR_STATE_ABRVTN", "PRSCRBR_STATE_ABRVTN",
              "MAILING_STATE", "CMTE_ST", "ESTABLISHMENT_STATE", "FAC_STATE"]
ZIP_COLS = ["ZIP", "ZIP_CODE", "ZIP_CD", "ZIPCODE", "ZIP5", "POSTAL_CODE",
            "PROVIDER_ZIP", "RECIPIENT_ZIP", "RNDRNG_PRVDR_ZIP5", "MAILING_ZIP",
            "CMTE_ZIP", "ESTABLISHMENT_ZIP"]

# Survivorship authority: LOWER wins the golden name. Mirrors the tiers already in
# DISPLAY_SPECS -- 1 is reserved for NPPES (the provider registry of record), 2 for a
# source that IS the registry for its own key, 3-4 for enrollment/administrative
# files, 6 for everything downstream. A generated spec never claims 1 or 2 unless the
# table is named below, because taking the golden name away from an existing
# authoritative source is a decision, not a default.
AUTHORITY_BY_TABLE = {
    "FED_EPA_FRS_FULL": 2,        # IS the EPA facility registry
    "FED_EPA_SDWA_SDWA_FACILITIES": 2,   # IS the water-system inventory
    "FED_MSHA_VIOLATIONS": 3,
    "FED_MSHA_ACCIDENTS": 4,
}
DEFAULT_AUTHORITY = 6

# --------------------------------------------------------------------------- #
# extra_keys safety. A spec's extra_keys share the row's org/person/address for name
# survivorship, so an extra key is only safe when it identifies the SAME real-world
# thing the row is about. entity_index_specs.py's docstring is explicit about this and
# names ARCOS's buyer_dea_no as an accepted-but-known mislabeling not to repeat.
#
# The failure this guard exists to stop, caught while generating wave 2: both
# FED_FEC_COMMITTEE_TO_CANDIDATE and FED_FEC_BULK_COMMITTEES carry a committee ID AND
# a candidate ID. Those are TWO PARTIES TO A RELATIONSHIP, not one thing with two IDs
# -- wiring the candidate as an extra_key would have given every candidate (a person)
# the canonical name of a PAC ("FRIENDS OF ..."), silently, on 20,007 rows.
#
# Rule: an extra key whose entity TYPE differs from the primary's is REJECTED unless
# the table is listed below as a genuine one-thing-many-IDs case. Same-type extras
# (e.g. an auditee's EIN alongside its UEI, both 'organization') are allowed.
SAME_THING_MULTI_ID = {
    # A Medicare-enrolled facility legitimately holds BOTH an NPI (as a billing
    # provider) and a CCN (as a certified facility). One hospital, two identifier
    # systems, and ORGANIZATION_NAME is the correct name for both.
    "FED_CMS_HOSPITAL_ENROLLMENTS",
    "FED_CMS_HOSPICE_ENROLLMENTS",
    "FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS",
    "FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS",
    "FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS",
    "FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS",
    "FED_CMS_MEDICARE_DIALYSIS_FACILITIES",
}

# A key must clear ALL of these to be wired.
MIN_DISTINCT = 2          # one distinct value is a constant, not an identifier
MIN_SURVIVING_PCT = 0.5   # under this % of rows normalizing to non-NULL, it's noise


def pick(cols_upper, preference):
    """First preference present in the table, else None. cols_upper maps UPPER -> real."""
    for want in preference:
        if want in cols_upper:
            return cols_upper[want]
    return None


def verify_key(cur, table, key, key_col, total_rows):
    """Measure the key with the SPINE'S OWN normalizer, not a hand-rolled TRIM.

    Returns an evidence dict. This is the whole point of the script: the number that
    decides whether to wire is COUNT(DISTINCT normalized), never COUNT(col).
    """
    norm = normalize_sql(key, quote_ident(key_col))
    cur.execute(f'''
        select count(*),
               count({norm}),
               count(distinct {norm}),
               min(length({norm})),
               max(length({norm}))
        from LIBRARY_RAW.LANDING."{table}"
    ''')
    n, survive, distinct, minl, maxl = cur.fetchone()
    cur.execute(f'''
        select distinct {norm} from LIBRARY_RAW.LANDING."{table}"
        where {norm} is not null limit 5
    ''')
    sample = [r[0] for r in cur.fetchall()]
    # New-to-spine: the number that actually says whether this is worth the rebuild.
    # A 6M-row table adding 2,288 entities is an attribute table, not a population.
    cur.execute(f'''
        select count(*) from (
          select distinct {norm} as v from LIBRARY_RAW.LANDING."{table}"
          where {norm} is not null
        ) s
        where not exists (
          select 1 from LIBRARY_META."CONNECT".ENTITY_MAP e
          where e.KEY_TYPE = %s and e.KEY_VALUE = s.v)
    ''', (key,))
    new_to_spine = cur.fetchone()[0] or 0

    ev = {
        "table": table, "key": key, "key_col": key_col,
        "rows": n or 0, "surviving": survive or 0, "distinct": distinct or 0,
        "min_len": minl, "max_len": maxl,
        "sample": " | ".join(str(s) for s in sample),
        "new_to_spine": new_to_spine,
        "surviving_pct": round(100.0 * (survive or 0) / (n or 1), 2),
    }
    reasons = []
    if ev["distinct"] < MIN_DISTINCT:
        reasons.append(f"only {ev['distinct']} distinct value(s) after normalization")
    if ev["surviving_pct"] < MIN_SURVIVING_PCT:
        reasons.append(f"only {ev['surviving_pct']}% of rows survive normalization")
    if ev["surviving"] == 0:
        reasons.append("normalizes to NULL on every row (sentinel or wrong column)")
    ev["reject_reason"] = "; ".join(reasons)
    return ev


def candidates(cur, only_tables=None):
    """Modeled sources with a claimed hard key that are NOT yet in the spine.

    Matched on LANDING_FQN, not SOURCE_ID: the registry holds duplicate rows whose
    SOURCE_ID differs but whose landing table is one the spine already covers (e.g.
    'fed_dea_arcos' vs 'fed_dea_arcos_full' -- same 178.6M-row table, and the first
    one's landing pointer is dangling entirely).
    """
    cur.execute("""
        select SOURCE_ID, upper(split_part(LANDING_FQN, '.', 3)) as LAND_TBL,
               JOIN_KEY_TIER, JOIN_KEYS_STD, MART_ROW_COUNT
        from LIBRARY_META.REGISTRY.CATALOG
        where LIFECYCLE = 'modeled'
          and JOIN_KEY_TIER in ('STEEL', 'STRONG')
          and array_size(JOIN_KEYS_STD) > 0
    """)
    rows = cur.fetchall()
    cur.execute("""select distinct upper(TABLE_NAME) from LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
                   where TABLE_SCHEMA = 'LANDING'""")
    live = {r[0] for r in cur.fetchall()}
    already = {t.upper() for t in DISPLAY_SPECS}

    out, skipped = {}, []
    for sid, land, tier, keys_json, mart_rows in rows:
        if not land:
            skipped.append((sid, "no LANDING_FQN"))
            continue
        if land not in live:
            skipped.append((sid, f"landing table {land} does not exist (ghost registry row)"))
            continue
        if land in already:
            skipped.append((sid, f"{land} already in DISPLAY_SPECS"))
            continue
        if only_tables and land not in only_tables:
            continue
        import json as _json
        keys = _json.loads(keys_json) if isinstance(keys_json, str) else list(keys_json or [])
        # Dedup: several SOURCE_IDs can point at one landing table. Keep the biggest.
        prev = out.get(land)
        if prev and (prev["mart_rows"] or 0) >= (mart_rows or 0):
            continue
        out[land] = {"source_id": sid, "table": land, "tier": tier,
                     "claimed_keys": keys, "mart_rows": mart_rows or 0}
    return out, skipped


def build_spec(cur, cand):
    """Verify every claimed spine-eligible key on a table; return (spec, evidence)."""
    table = cand["table"]
    cols = sc.columns_of(table, conn=cur.connection)
    cols_upper = {c.upper(): c for c in cols}

    # Only claimed keys that connect/ can actually normalize AND that name a THING.
    # ACCESSION_NUMBER/CUSIP are filtered out here: a filing is not an entity and a
    # security is not an organization (2026-07-30 call) -- they belong as edges off
    # the CIK axis. Geo keys (STATE/ZIP/COUNTY/FIPS) are not identities either.
    usable = [k for k in cand["claimed_keys"]
              if k in KEY_COL_PREFERENCE and k in NORM_RULES]
    # FEC_ID in the registry means "one of CMTE_ID / CAND_ID"; connect/ splits them.
    if "FEC_ID" in cand["claimed_keys"]:
        usable += [k for k in ("FEC_CMTE_ID", "FEC_CAND_ID") if k not in usable]

    verified, rejected = [], []
    for key in usable:
        key_col = pick(cols_upper, KEY_COL_PREFERENCE[key])
        if not key_col:
            rejected.append({"table": table, "key": key, "key_col": "",
                             "reject_reason": "claimed by the registry but no known "
                                              "column name for it in this table",
                             "rows": cand["mart_rows"], "surviving": 0, "distinct": 0,
                             "min_len": None, "max_len": None, "sample": "",
                             "new_to_spine": 0, "surviving_pct": 0.0})
            continue
        ev = verify_key(cur, table, key, key_col, cand["mart_rows"])
        (rejected if ev["reject_reason"] else verified).append(ev)

    if not verified:
        return None, rejected

    # Primary key = the verified key with the most distinct values; it's the grain the
    # table is really about. Ties broken by KEY_COL_PREFERENCE order for stability.
    verified.sort(key=lambda e: (-e["distinct"], list(KEY_COL_PREFERENCE).index(e["key"])))
    primary, extras = verified[0], verified[1:]

    # Drop any extra that identifies a DIFFERENT KIND of thing than the primary --
    # it would inherit this row's name and address (see SAME_THING_MULTI_ID above).
    kept_extras = []
    for e in extras:
        same_type = (ENTITY_TYPE_BY_KEY.get(e["key"]) ==
                     ENTITY_TYPE_BY_KEY.get(primary["key"]))
        if same_type or table in SAME_THING_MULTI_ID:
            kept_extras.append(e)
        else:
            e = dict(e)
            e["reject_reason"] = (
                f"extra_key rejected: {e['key']} is a "
                f"'{ENTITY_TYPE_BY_KEY.get(e['key'])}' but the row's primary "
                f"{primary['key']} is a '{ENTITY_TYPE_BY_KEY.get(primary['key'])}' -- "
                f"two parties to a relationship, not one thing with two IDs. Wiring it "
                f"would give the {ENTITY_TYPE_BY_KEY.get(e['key'])} this row's name. "
                f"Add {table} to SAME_THING_MULTI_ID only if that is genuinely wrong.")
            rejected.append(e)
    extras = kept_extras
    verified = [primary] + extras

    spec = {
        "key": primary["key"], "key_col": primary["key_col"],
        "org": pick(cols_upper, ORG_COLS),
        "person": None, "city": pick(cols_upper, CITY_COLS),
        "state": pick(cols_upper, STATE_COLS), "zip": pick(cols_upper, ZIP_COLS),
        "authority": AUTHORITY_BY_TABLE.get(table, DEFAULT_AUTHORITY),
        "extra_keys": [{"key": e["key"], "key_col": e["key_col"]} for e in extras],
    }
    last, first = pick(cols_upper, LAST_COLS), pick(cols_upper, FIRST_COLS)
    if last and first:
        spec["person"] = [last, first]
    return spec, rejected, verified


def render(table, spec, verified):
    """Emit a DISPLAY_SPECS entry with its evidence inline as a comment, so the diff
    reviewer sees WHY it was wired without re-running anything."""
    p = verified[0]
    lines = [f'    "{table}": {{']
    lines.append(f'        # {p["key"]} -- {p["distinct"]:,} distinct / {p["surviving"]:,} '
                 f'rows ({p["surviving_pct"]}% survive norm), +{p["new_to_spine"]:,} new '
                 f'to spine. len {p["min_len"]}-{p["max_len"]}. e.g. {p["sample"].split(" | ")[0]}')
    lines.append(f'        "key": "{spec["key"]}", "key_col": "{spec["key_col"]}",')
    if spec["person"]:
        lines.append(f'        "person": ["{spec["person"][0]}", "{spec["person"][1]}"],')
    if spec["org"]:
        lines.append(f'        "org": "{spec["org"]}",')
    addr = [f'"{k}": "{spec[k]}"' for k in ("city", "state", "zip") if spec.get(k)]
    if addr:
        lines.append(f'        {", ".join(addr)},')
    if spec["extra_keys"]:
        for e, ev in zip(spec["extra_keys"], verified[1:]):
            lines.append(f'        # extra: {ev["key"]} -- {ev["distinct"]:,} distinct, '
                         f'+{ev["new_to_spine"]:,} new to spine')
        inner = ", ".join(f'{{"key": "{e["key"]}", "key_col": "{e["key_col"]}"}}'
                          for e in spec["extra_keys"])
        lines.append(f'        "extra_keys": [{inner}],')
    lines.append(f'        "authority": {spec["authority"]},')
    lines.append("    },")
    return "\n".join(lines)


# Waves from the 2026-07-30 plan, ordered by NEW ENTITIES not row count -- the
# handoff ranked by rows, which pointed at a 6.3M-row table that adds 2,288 entities
# while burying a table that adds 175,699.
WAVES = {
    1: [  # new populations the spine has never seen
        "FED_USASPENDING_ASSISTANCE_FULL",
        "FED_OSHA_ITA_300A_SUMMARY_2023", "FED_OSHA_ITA_300A_SUMMARY_2024",
        "FED_OSHA_ITA_300A_SUMMARY_2025", "FED_OSHA_ITA_CASE_DETAIL_2023",
        "FED_OSHA_ITA_CASE_DETAIL_2024", "FED_OSHA_ITA_CASE_DETAIL_2025",
        "FED_IRS_PUB78_ELIGIBLE_DONEES", "FED_IRS_AUTO_REVOCATIONS",
        "FED_IRS_SOI_CHARITIES",
        "FED_CMS_HOSPITAL_ENROLLMENTS", "FED_CMS_HOSPICE_ENROLLMENTS",
        "FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS",
        "FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS",
        "FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS",
        "FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS",
    ],
    2: [  # new key axes -- MSHA first because it's smallest and proves the path
        "FED_MSHA_VIOLATIONS", "FED_MSHA_ACCIDENTS",
        "FED_EPA_FRS_FULL", "FED_EPA_ECHO",
        "FED_EPA_SDWA_SDWA_FACILITIES", "FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT",
        "FED_EPA_SDWA_SDWA_SITE_VISITS", "FED_EPA_SDWA_SDWA_LCR_SAMPLES",
        "FED_EPA_FRS_FRS_NAICS_CODES", "FED_EPA_FRS_FRS_SIC_CODES",
        "FED_EPA_FRS_FRS_PROGRAM_LINKS",
        "FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS",
        "FED_EPA_NPDES_NPDES_INSPECTIONS",
        "FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS",
        "FED_FEC_INDIV_CONTRIBUTIONS", "FED_FEC_COMMITTEE_TO_CANDIDATE",
        "FED_FEC_BULK_CANDIDATES", "FED_FEC_BULK_COMMITTEES", "FED_FEC_BULK_SUMMARY",
    ],
    3: None,   # everything else that verifies -- breadth pass
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wave", type=int, choices=[1, 2, 3])
    ap.add_argument("--tables", help="comma-separated landing table names")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--out", help="write the spec block here instead of stdout")
    args = ap.parse_args()

    only = None
    if args.tables:
        only = {t.strip().upper() for t in args.tables.split(",") if t.strip()}
    elif args.wave in (1, 2):
        only = set(WAVES[args.wave])
    elif not (args.all or args.wave == 3):
        ap.error("pass --wave N, --tables A,B or --all")

    conn = sc.connect()
    cur = conn.cursor()
    cands, skipped = candidates(cur, only)

    print(f"candidates: {len(cands)}   skipped: {len(skipped)}")
    for sid, why in skipped:
        if "already in DISPLAY_SPECS" not in why:
            print(f"   SKIP  {sid:55} {why}")

    if only:
        missing = only - set(cands)
        for m in sorted(missing):
            print(f"   MISS  {m:55} not a live unwired candidate (already wired, or no key)")

    blocks, all_ev, all_rej = [], [], []
    for table in sorted(cands, key=lambda t: -cands[t]["mart_rows"]):
        try:
            result = build_spec(cur, cands[table])
        except Exception as exc:
            print(f"   ERR   {table:55} {type(exc).__name__}: {str(exc)[:90]}")
            continue
        if result[0] is None:
            _, rej = result
            all_rej.extend(rej)
            for r in rej:
                print(f"   REJECT {table:54} {r['key']}: {r['reject_reason']}")
            continue
        spec, rej, verified = result
        all_rej.extend(rej)
        all_ev.extend(verified)
        blocks.append(render(table, spec, verified))
        v = verified[0]
        print(f"   WIRE  {table:55} {v['key']:12} {v['distinct']:>10,} distinct  "
              f"+{v['new_to_spine']:>9,} new")

    os.makedirs(OUT_DIR, exist_ok=True)
    ev_path = os.path.join(OUT_DIR, "spine_wiring_evidence.csv")
    rj_path = os.path.join(OUT_DIR, "spine_wiring_rejects.csv")
    cols = ["table", "key", "key_col", "rows", "surviving", "surviving_pct",
            "distinct", "min_len", "max_len", "new_to_spine", "sample", "reject_reason"]
    for path, data in ((ev_path, all_ev), (rj_path, all_rej)):
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            for r in data:
                w.writerow(r)

    body = "\n".join(blocks)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(body + "\n")
        print(f"\nspec block -> {args.out}")
    else:
        print("\n" + "=" * 78 + "\npaste into connect/entity_index_specs.py DISPLAY_SPECS:\n"
              + "=" * 78)
        print(body)

    tot_new = sum(e["new_to_spine"] for e in all_ev)
    print(f"\nwired {len(blocks)} tables, {len(all_ev)} keys, "
          f"{tot_new:,} new entity values; {len(all_rej)} rejected")
    print(f"evidence -> {ev_path}\nrejects  -> {rj_path}")
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
