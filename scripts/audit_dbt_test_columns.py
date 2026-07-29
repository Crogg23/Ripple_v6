"""Audit dbt column-level tests against the columns that actually exist.

Why: the mart generator wrote schema.yml tests for column names it invented --
VOYAGE_ID where the table has VOYAGEID, SETTLEMENT_SK / COMPANY_ID / PERSON_NAME
that exist nowhere. Those tests do not fail loudly as data problems; they error
with "invalid identifier", which is easy to wave off as noise. The effect is a
2,785-test suite that looks like coverage and isn't.

This compares every column-level test in the manifest against
INFORMATION_SCHEMA for the model's real relation, so phantom tests can be found
without running them.

Requires a parsed manifest (run `dbt parse` first) and a Snowflake connection via
the cortex CLI. Writes a CSV of phantom tests for triage.

Usage: python scripts/audit_dbt_test_columns.py [--out phantom_tests.csv]
"""
import argparse
import collections
import csv
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(REPO, "library-onboarding", "ripple_dbt", "target",
                        "manifest.json")


def load_manifest():
    with open(MANIFEST, encoding="utf-8") as fh:
        return json.load(fh)


def relation_of(node):
    return (node["database"].upper(), node["schema"].upper(),
            (node.get("alias") or node["name"]).upper())


def fetch_columns(databases):
    """Return {(db, schema, table): {COLUMN, ...}} for the given databases."""
    cols = collections.defaultdict(set)
    for db in sorted(databases):
        sql = (f"select table_schema, table_name, column_name "
               f"from {db}.information_schema.columns")
        proc = subprocess.run(
            ["cortex", "sql", "--query", sql, "--format", "json"],
            capture_output=True, text=True, shell=True,
        )
        if proc.returncode != 0:
            print(f"WARN could not read {db}: {proc.stderr.strip()[:160]}")
            continue
        try:
            rows = json.loads(proc.stdout)
        except json.JSONDecodeError:
            print(f"WARN unparseable response for {db}")
            continue
        if isinstance(rows, dict):
            rows = rows.get("rows") or rows.get("data") or []
        for r in rows:
            if isinstance(r, dict):
                sch = (r.get("TABLE_SCHEMA") or r.get("table_schema") or "").upper()
                tbl = (r.get("TABLE_NAME") or r.get("table_name") or "").upper()
                col = (r.get("COLUMN_NAME") or r.get("column_name") or "").upper()
            else:
                sch, tbl, col = (str(x).upper() for x in r[:3])
            cols[(db.upper(), sch, tbl)].add(col)
    return cols


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(REPO, "outputs",
                                                 "phantom_tests.csv"))
    args = ap.parse_args()

    man = load_manifest()
    nodes = man["nodes"]

    tests = []
    for uid, node in nodes.items():
        if node["resource_type"] != "test" or not node.get("column_name"):
            continue
        parents = [d for d in node["depends_on"]["nodes"] if d.startswith("model.")]
        if len(parents) != 1 or parents[0] not in nodes:
            continue
        tests.append((uid, node, nodes[parents[0]]))

    databases = {relation_of(m)[0] for _uid, _t, m in tests}
    print(f"{len(tests)} column-level tests across {len(databases)} databases: "
          f"{sorted(databases)}")
    cols = fetch_columns(databases)

    phantom, missing_rel, ok = [], [], 0
    for uid, test, model in tests:
        rel = relation_of(model)
        if rel not in cols:
            missing_rel.append((uid, test, model, rel))
            continue
        if test["column_name"].upper() in cols[rel]:
            ok += 1
        else:
            phantom.append((uid, test, model, rel))

    by_model = collections.Counter(m["name"] for _u, _t, m, _r in phantom)
    print(f"\nOK (column exists):        {ok}")
    print(f"PHANTOM (column missing):  {len(phantom)}")
    print(f"relation not built yet:    {len(missing_rel)}")
    if by_model:
        print("\nworst offenders:")
        for name, n in by_model.most_common(20):
            print(f"  {n:4}  {name}")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["model", "missing_column", "test", "defined_in"])
        for _uid, test, model, _rel in sorted(
                phantom, key=lambda x: (x[2]["name"], x[1]["column_name"])):
            w.writerow([model["name"], test["column_name"],
                        test.get("test_metadata", {}).get("name", ""),
                        test.get("original_file_path", "")])
    print(f"\nwrote {args.out}")
    return 1 if phantom else 0


if __name__ == "__main__":
    sys.exit(main())
