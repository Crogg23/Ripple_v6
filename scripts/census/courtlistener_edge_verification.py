"""CourtListener internal-ID edge verification — the registration evidence.

The 21 court tables join internally on CourtListener's own person/court IDs but
have zero edges in the connection map. Before those keys become spine key axes
(staged in connect/keys.py + entity_index_specs.py behind
ENABLE_COURTLISTENER_SPINE, flipped at the next full spine rebuild), every join
surface is measured here the same way the 2026-08-11 connection audit measured
the existing map: nonnull / distinct / match-rate against the authority table.

Read-only aggregates. Writes reports/census_grid_2026-08-12/fill/
courtlistener_edges.json.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _snowflake_conn import connect  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "reports", "census_grid_2026-08-12", "fill",
                   "courtlistener_edges.json")

L = 'LIBRARY_RAW."LANDING"'

# (carrier table, id column, authority table, authority id col, edge name)
PERSON_EDGES = [
    ("FED_COURTLISTENER_FINANCIAL_DISCLOSURES", "PERSON_ID", "judge -> financial disclosure"),
    ("FED_COURTLISTENER_POSITIONS", "PERSON_ID", "judge -> position/judgeship"),
    ("FED_COURTLISTENER_POSITIONS", "APPOINTER_ID", "appointing judge -> position"),
    ("FED_COURTLISTENER_JUDGE_EDUCATIONS", "PERSON_ID", "judge -> education"),
    ("FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS", "PERSON_ID", "judge -> political affiliation"),
    ("FED_COURTLISTENER_JUDGE_RACES", "PERSON_ID", "judge -> race record"),
    ("FED_COURTLISTENER_DOCKETS", "ASSIGNED_TO_ID", "judge -> assigned docket"),
    ("FED_COURTLISTENER_ORIGINATING_COURT_INFO", "ASSIGNED_TO_ID", "judge -> originating-court assignment"),
    ("FED_COURTLISTENER_ORIGINATING_COURT_INFO", "ORDERING_JUDGE_ID", "ordering judge -> originating-court info"),
]
COURT_EDGES = [
    ("FED_COURTLISTENER_DOCKETS", "COURT_ID", "court -> docket"),
    ("FED_COURTLISTENER_COURTHOUSES", "COURT_ID", "court -> courthouse"),
    ("FED_COURTLISTENER_POSITIONS", "COURT_ID", "court -> judgeship"),
    ("FED_COURTLISTENER_COURTS", "PARENT_COURT_ID", "court -> parent court"),
    ("FED_COURTLISTENER_COURT_APPEALS_TO", "FROM_COURT_ID", "court -> appeals-from"),
    ("FED_COURTLISTENER_COURT_APPEALS_TO", "TO_COURT_ID", "court -> appeals-to"),
]
CHAIN_EDGES = [  # the money chain: disclosure-line tables -> financial disclosure
    ("FED_COURTLISTENER_INVESTMENTS", "FINANCIAL_DISCLOSURE_ID", "investment line -> disclosure"),
    ("FED_COURTLISTENER_DISCLOSURE_DEBTS", "FINANCIAL_DISCLOSURE_ID", "debt line -> disclosure"),
    ("FED_COURTLISTENER_DISCLOSURE_GIFTS", "FINANCIAL_DISCLOSURE_ID", "gift line -> disclosure"),
    ("FED_COURTLISTENER_DISCLOSURE_SPOUSAL_INCOME", "FINANCIAL_DISCLOSURE_ID", "spousal-income line -> disclosure"),
    ("FED_COURTLISTENER_DISCLOSURE_POSITIONS", "FINANCIAL_DISCLOSURE_ID", "position line -> disclosure"),
]


def measure(cur, carrier, col, auth, auth_col, label):
    cur.execute(f"""
        select count(*), count(c."{col}"),
               approx_count_distinct(c."{col}"),
               count_if(a."{auth_col}" is not null),
               min(to_varchar(c."{col}")), max(to_varchar(c."{col}"))
        from {L}."{carrier}" c
        left join {L}."{auth}" a on to_varchar(a."{auth_col}") = to_varchar(c."{col}")
        """)
    n, nn, dn, matched, mn, mx = cur.fetchone()
    rec = {"edge": label, "carrier": carrier, "column": col, "authority": auth,
           "rows": n, "nonnull": nn, "distinct": dn, "matched_rows": matched,
           "match_pct_of_nonnull": round(100 * matched / nn, 2) if nn else None,
           "sample_range": [mn, mx]}
    print(f"  {label}: rows={n:,} nonnull={nn:,} distinct={dn:,} "
          f"matched={matched:,} ({rec['match_pct_of_nonnull']}%)", flush=True)
    return rec


def main():
    conn = connect(database="LIBRARY_RAW")
    cur = conn.cursor()
    out = {"authorities": {}, "person_edges": [], "court_edges": [], "chain_edges": []}

    cur.execute(f"""
        select count(*), approx_count_distinct("ID"), count_if("IS_ALIAS_OF_ID" is not null),
               count_if(nullif(trim("NAME_LAST"), '') is not null)
        from {L}."FED_COURTLISTENER_JUDGES" """)
    n, dn, alias, named = cur.fetchone()
    out["authorities"]["judges"] = {"rows": n, "distinct_id": dn, "alias_rows": alias,
                                    "named": named}
    print(f"judges: {n:,} rows, {dn:,} distinct ids, {alias:,} alias rows, {named:,} named", flush=True)

    cur.execute(f"""
        select count(*), approx_count_distinct("ID"),
               count_if(nullif(trim("FULL_NAME"), '') is not null),
               count_if("FJC_COURT_ID" is not null)
        from {L}."FED_COURTLISTENER_COURTS" """)
    n, dn, named, fjc = cur.fetchone()
    out["authorities"]["courts"] = {"rows": n, "distinct_id": dn, "named": named,
                                    "with_fjc_bridge_id": fjc}
    print(f"courts: {n:,} rows, {dn:,} distinct ids, {named:,} named, {fjc:,} with FJC bridge id", flush=True)

    print("person edges:", flush=True)
    for carrier, col, label in PERSON_EDGES:
        out["person_edges"].append(
            measure(cur, carrier, col, "FED_COURTLISTENER_JUDGES", "ID", label))
    print("court edges:", flush=True)
    for carrier, col, label in COURT_EDGES:
        out["court_edges"].append(
            measure(cur, carrier, col, "FED_COURTLISTENER_COURTS", "ID", label))
    print("disclosure-chain edges:", flush=True)
    for carrier, col, label in CHAIN_EDGES:
        out["chain_edges"].append(
            measure(cur, carrier, col, "FED_COURTLISTENER_FINANCIAL_DISCLOSURES", "ID", label))

    conn.close()
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1)
    print("wrote", OUT, flush=True)


if __name__ == "__main__":
    main()
