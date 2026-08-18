"""Merge the census-grid fill: Tier A catalog metadata + the 2026-08-11
verification scan + Tier B new scans into one per-model fill table.

Produces reports/census_grid_2026-08-12/fill/fill_tables.csv -- one row per
mart-layer model in the grid, carrying:
  - measured row count, bytes (catalog), whether it's a table or a view
  - exact-dup signal (distinct full-row hashes vs rows)
  - freshness: min/max across all date columns, plus epoch-1970 and far-future
    counts (the known date traps)
  - best join key: the ID column with the highest distinct count, its fill
    rate, distinct count, and sentinel count
  - scan provenance (2026-08-11 scan / tier-b 2026-08-17 / unscanned)

Plus fill_summary counts printed for the report. Pure local merge, no warehouse.
"""
import csv
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GRID = os.path.join(REPO, "reports", "census_grid_2026-08-12")
FILL = os.path.join(GRID, "fill")


def load_scans():
    scans = {}
    for path, tag in [
        (os.path.join(REPO, "outputs", "_mart_key_date_dup_scan_2026-08-11.jsonl"), "scan-2026-08-11"),
        (os.path.join(REPO, "outputs", "_mart_key_date_dup_scan_rerun.jsonl"), "scan-2026-08-11"),
        (os.path.join(FILL, "tier_b_new_scans.jsonl"), "tier-b-2026-08-17"),
    ]:
        if not os.path.exists(path):
            continue
        for line in open(path, encoding="utf-8"):
            r = json.loads(line)
            tab = r["table"].split(".", 1)[1].upper()
            scans[tab] = (r, tag)  # later files win (rerun/tier-b fix earlier errors)
    return scans


def main():
    catalog = {}
    for r in csv.DictReader(open(os.path.join(FILL, "tier_a_tables.csv"), encoding="utf-8")):
        if r["database"] == "LIBRARY_MARTS":
            catalog[r["table"].upper()] = r

    scans = load_scans()
    models = list(csv.DictReader(open(os.path.join(GRID, "table_map.csv"), encoding="utf-8")))

    out_path = os.path.join(FILL, "fill_tables.csv")
    n_filled = n_unscanned = n_empty = n_dupheavy = n_stale = 0
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow([
            "model", "subject", "family", "class", "object_type", "n_rows", "bytes",
            "dup_ratio", "date_min", "date_max", "n_epoch1970", "n_far_future",
            "best_key", "best_key_fill_pct", "best_key_distinct", "best_key_sentinels",
            "scan_provenance",
        ])
        for m in models:
            if m["layer"] != "marts":
                continue
            name = m["model"].upper()
            cat = catalog.get(name, {})
            scan, tag = scans.get(name, (None, "unscanned"))
            n_rows = bytes_ = obj_type = ""
            if cat:
                obj_type = cat["table_type"]
                n_rows = cat["row_count"]
                bytes_ = cat["bytes"]
            dup_ratio = date_min = date_max = ""
            e1970 = far = ""
            bk = bk_fill = bk_dn = bk_sent = ""
            if scan and "error" not in scan:
                rows = scan.get("n_rows") or 0
                n_rows = rows
                if scan.get("distinct_row_hashes") and rows:
                    dup_ratio = round(1 - int(scan["distinct_row_hashes"]) / int(rows), 4)
                dates = scan.get("dates", {})
                mins = [d["min"] for d in dates.values() if d.get("min") not in (None, "None")]
                maxs = [d["max"] for d in dates.values() if d.get("max") not in (None, "None")]
                date_min = min(mins) if mins else ""
                date_max = max(maxs) if maxs else ""
                e1970 = sum(int(d.get("y1970") or 0) for d in dates.values())
                far = sum(int(d.get("future5y") or 0) for d in dates.values())
                best = None
                for c, s in scan.get("ids", {}).items():
                    dn = int(s.get("distinct") or 0)
                    if best is None or dn > best[1]:
                        best = (c, dn, s)
                if best and rows:
                    c, dn, s = best
                    bk = c
                    bk_fill = round(100 * int(s.get("nonnull") or 0) / int(rows), 1)
                    bk_dn = dn
                    bk_sent = s.get("sentinels")
                if rows == 0:
                    n_empty += 1
                if dup_ratio != "" and dup_ratio > 0.05:
                    n_dupheavy += 1
                if date_max and date_max < "2024-01-01":
                    n_stale += 1
                n_filled += 1
            else:
                n_unscanned += 1
            w.writerow([m["model"], m["subject"], m["family"], m["class"], obj_type,
                        n_rows, bytes_, dup_ratio, date_min, date_max, e1970, far,
                        bk, bk_fill, bk_dn, bk_sent, tag])

    print(f"mart models filled with scan data: {n_filled}")
    print(f"unscanned (catalog metadata only or nothing): {n_unscanned}")
    print(f"empty tables (0 rows): {n_empty}")
    print(f"dup-heavy (>5% duplicate full rows): {n_dupheavy}")
    print(f"stale (no date column value past 2024-01-01): {n_stale}")
    print("wrote", out_path)


if __name__ == "__main__":
    main()
