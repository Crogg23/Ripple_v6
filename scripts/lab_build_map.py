"""Assemble Laboratory_Warehouse_Map.md from the workflow's structured scoring.

Reads reports/lab_map/_workflow_result.json (the technique scoring, already
adversarially verified) plus a small set of editorial overrides applied here
after the completeness critic overturned some tiers. Writes the technique
sections; the front matter, corrections, summary and opportunity sections are
appended from _MAP_PROSE.md so the prose stays hand-written.
"""
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "reports", "lab_map", "_workflow_result.json")
OUT = os.path.join(ROOT, "Laboratory_Warehouse_Map.md")

TIER_LABEL = {
    "READY": "✅ **Ready**",
    "PARTIAL": "🟡 **Partial**",
    "NEEDS_NEW_DATA": "🔴 **Needs new data**",
    "NEEDS_CLEANUP": "🛠️ **Needs cleanup**",
}

# Tier corrections forced by the completeness critic, with the reason shown in
# the document so nothing is changed silently.
OVERRIDE = {
    "Percolation theory": {
        "tier": "PARTIAL",
        "blocker": (
            "Downgraded after review. The threshold dial on the connection map "
            "is measuring the sampler, not the warehouse: 4,910 measured table "
            "pairs out of roughly 4.6 million possible pairs across 3,033 base "
            "tables is about 0.1% coverage, and a missing pair there means "
            "\"never measured\", not \"no overlap\". Percolation's entire output "
            "is the threshold where islands snap into one blob — on a 0.1% "
            "sample that number is an artifact. `MATCH_PAIRS` does not rescue "
            "it either: a row says one key value appeared in two TABLES, not "
            "that two entities are linked."
        ),
        "distance_to_ready": (
            "Run it on a real physical network instead of on the warehouse's "
            "own wiring. The opioid shipment table is a genuine directed "
            "weighted network with 178.6M edges in one identifier namespace and "
            "a FLOAT quantity to threshold on — percolation there is valid "
            "today with no repair. To make the connection-map lane valid you "
            "would have to measure a far larger share of table pairs first."
        ),
        "note": (
            "Valid today on the opioid shipment network; invalid on the "
            "connection map, because 0.1% of the possible table pairs have "
            "ever been measured."
        ),
    },
    "Flow maps": {
        "tier": "PARTIAL",
        "what_exists": (
            "The shape index's 558 origin-and-destination tables is close to "
            "worthless and the review debunked it: the top \"origin\" column "
            "names are loader bookkeeping — SOURCE_RUN_ID (1,884), _SOURCE_URL "
            "(1,100), _SOURCE_RUN_ID (948) — and only 32 columns in the whole "
            "warehouse are literally named ORIGIN. About six genuine same-row "
            "flow families survive, and they are strong on the from-and-to and "
            "weak on the coordinates.\n\n"
            "`LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS` carries reporter "
            "city/state/zip to buyer city/state/zip across 178,598,026 shipment "
            "rows with DOSAGE_UNITS and TOTAL_MME as FLOAT. **A mid-sweep claim "
            "that its date and county columns are bad casts was read off the "
            "backup copy of the table, not the live one** — in the live mart "
            "BUYER_COUNTY is TEXT and the clock index rates TRANSACTION_DATE as "
            "happened / day / high confidence, calling it the cleanest big "
            "event clock in its batch. The real limit on it is span: coverage "
            "is 2006–2012, not 2006–2026.\n\n"
            "`LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS` "
            "genuinely pairs damaged ZIP/city/state with rental-resource "
            "ZIP/city/state plus a rental assistance amount — and its origin end "
            "needs no crosswalk at all, because it carries a census tract id "
            "that joins straight to the tract centroid table. Its 3,080,000 "
            "rows is an exactly round count, the shape confirmed as a load cap "
            "in 18 other tables.\n\n"
            "`LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL` "
            "holds recipient county FIPS and place-of-performance county FIPS on "
            "the same row across 19,902,879 rows — the only county-to-county "
            "lane there is. **The bad-cast warning previously attached to those "
            "two columns is stale**: that defect was repaired on 2026-08-10 and "
            "both columns land as TEXT today, leading zeros intact. The real "
            "problem with that table is different and worse — all 112 of its "
            "columns are TEXT, including every obligation amount and the action "
            "date, so a weighted or dated flow needs a cast first. Its contracts "
            "twin has the identically-named money columns as FLOAT, so this is a "
            "per-table modelling miss, not a source limitation.\n\n"
            "`LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CRIMINAL` already holds "
            "district and transfer-district on the same row across 6.3M cases — "
            "but court districts have no geography anywhere in the warehouse, "
            "which kills the map and not the flow. The transport equivalent is a "
            "confirmed 21-row stub."
        ),
        "candidate_fixes": {
            "LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS": (
                "reporter city/state/zip to buyer city/state/zip on 178.6M rows "
                "with DOSAGE_UNITS and TOTAL_MME as FLOAT and the cleanest big "
                "event clock in the warehouse — the ZIP ends are clean and "
                "drawable at county resolution today; coverage stops at 2012"
            ),
            "LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL": (
                "place-of-performance and recipient county FIPS on the same row "
                "— the only county-to-county lane, and the FIPS columns are TEXT "
                "and intact after the August repair. Every amount and date on "
                "this table is TEXT though, so weighting a flow needs a cast"
            ),
        },
        "blocker": (
            "Corrected after review — the original blocker (\"nothing can place "
            "a ZIP on a map\") was wrong. ZIP → county → centroid is a two-hop "
            "join over two tables that both exist today: "
            "`LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY` (46,960 rows) maps every ZIP "
            "to a county, and `LIBRARY_MARTS.CORE.DIM_COUNTY` (3,222) carries "
            "POP_CENTER_LAT/LON as FLOAT. So flows are drawable **today at "
            "county resolution with no ingest**. What is genuinely missing is a "
            "ZIP-level centroid, so the flagship ZIP-to-ZIP flows collapse from "
            "roughly 33,000 endpoints to 3,222 — a real loss of resolution, not "
            "a blocked technique. Separately: the recipient and place-of-"
            "performance county FIPS columns on the USAspending assistance "
            "table land as TEXT in the mart, so the leading zeros are probably "
            "intact — unverified, check the values before trusting them."
        ),
        "distance_to_ready": (
            "One dbt model, hours not days: DIM_ZIP_POINT — ZCTA5 from "
            "XWALK_ZCTA_COUNTY joined to DIM_COUNTY's population-weighted "
            "centroid, with a tie-break for the ZIPs that span counties (46,960 "
            "rows cover roughly 33,000 ZIPs, so some span). Optional follow-on "
            "of about a day for true per-ZIP centroids: average the coordinates "
            "on the ~12.9M already-geocoded ZIP-stamped facility and branch "
            "rows — finer, but facility-weighted and with holes where no "
            "regulated site exists."
        ),
        "note": (
            "Not blocked — just coarse. Every ZIP-to-ZIP flow in the building "
            "can be drawn today at county resolution; one small model takes it "
            "down to ZIP."
        ),
    },
}

# Extra candidates the completeness critic surfaced that the scoring missed.
EXTRA_CANDIDATES = {
    "Ripples (diffusion/propagation animation)": [
        ("LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK",
         "5300149",
         "found by the completeness critic — a pre-built bridge from the "
         "corporate-identifier namespace onto 5.3M geocoded, FIPS-stamped "
         "facilities, and onward to the SEC family and to 40M federal award "
         "rows. It breaks the \"nowhere to propagate to\" half of the blocker. "
         "Marked as a fuzzy name match by its own confidence and review "
         "columns — check the fill rate before trusting it."),
    ],
    "Neuroscience → connectome mapping": [
        ("LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK",
         "5300149",
         "found by the completeness critic — one of the \"build a crosswalk per "
         "island\" bridges is already built. There is live proof the chain "
         "traverses: a FINDINGS view already joins EPA facility violations to "
         "federal award dollars on the corporate parent key."),
    ],
    "Circulation (network / force-directed graphs)": [
        ("LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK",
         "12794",
         "found by the completeness critic — the identifier Rosetta stone for "
         "the one domain prior sessions recorded as having zero verified "
         "cross-family joins. Carries fifteen parallel member identifiers plus "
         "a campaign-finance id array. The tables that should consume it are "
         "starved at roughly a tenth of its coverage."),
    ],
}


def esc(s):
    return (s or "").strip()


def main():
    r = json.load(open(RES, encoding="utf-8"))
    out = io.open(OUT, "w", encoding="utf-8")
    w = out.write

    counts = {}
    lines_by_cat = []

    for cat in r["categories"]:
        buf = []
        buf.append("\n---\n\n## " + cat["title"] + "\n")
        for t in cat["techniques"]:
            ov = OVERRIDE.get(t["technique"], {})
            tier = ov.get("tier", t["tier"])
            counts[tier] = counts.get(tier, 0) + 1
            buf.append("\n### " + t["technique"] + "\n")
            buf.append("\n**Readiness:** " + TIER_LABEL[tier])
            if t["technique"] in OVERRIDE:
                if tier != t["tier"]:
                    buf.append("  *(changed from "
                               + TIER_LABEL[t["tier"]].replace("**", "")
                               + " during the completeness review — reason below)*")
                else:
                    buf.append("  *(tier held, but the stated gap was corrected"
                               " during the completeness review — see below)*")
            buf.append("\n\n**Needs.** " + esc(t["needs"]) + "\n")
            buf.append("\n**What exists.** "
                       + esc(ov.get("what_exists", t["what_exists"])) + "\n")
            blocker = esc(ov.get("blocker", t.get("blocker")))
            dist = esc(ov.get("distance_to_ready", t.get("distance_to_ready")))
            if blocker:
                buf.append("\n**The gap.** " + blocker + "\n")
            if dist:
                buf.append("\n**Distance to ready.** " + dist + "\n")
            buf.append("\n**Candidate tables.**\n\n")
            cands = list(t["candidates"])
            fixes = ov.get("candidate_fixes", {})
            for c in cands:
                if c["table"] in fixes:
                    c = dict(c, why=fixes[c["table"]])
                rows = c.get("rows") or ""
                try:
                    rows = "{:,}".format(int(rows)) + " rows"
                except (TypeError, ValueError):
                    rows = "view" if not rows else rows
                buf.append("- `" + c["table"] + "` — " + rows + ". "
                           + esc(c["why"]) + "\n")
            for tbl, rows, why in EXTRA_CANDIDATES.get(t["technique"], []):
                buf.append("- `" + tbl + "` — {:,} rows. ".format(int(rows))
                           + why + "\n")
            buf.append("\n> " + esc(ov.get("note", t.get("note"))) + "\n")
        lines_by_cat.append("".join(buf))

    w("".join(lines_by_cat))
    out.close()

    print(json.dumps(counts, indent=2))
    print("technique sections written to", OUT)


if __name__ == "__main__":
    main()
