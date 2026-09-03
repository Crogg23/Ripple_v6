"""Gen 3 content recon: fold cross-table entity names from the gen-1 json pages.

Reads reports/recon/content/json/*.json (already on disk, zero warehouse cost),
pulls every "who"-tagged column's top-20 names, filters out place/address noise,
folds punctuation/legal-suffix variants into tier-1 clusters, and links tier-1
clusters that look like parent/subsidiary spellings into tier-2 groups for a
human or verifier agent to confirm.

Output: reports/recon/gen3/clusters.csv, reports/recon/gen3/parent_groups.csv
"""
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

JSON_DIR = Path("reports/recon/content/json")
OUT_DIR = Path("reports/recon/gen3")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# who-columns that are actually address/place components, not entities.
# Found by inspecting FED_ATF_FFL: CITY, REGION, SUBREGION, PLACENAME, STNAME,
# SUBADDR all got tagged "who" by the gen-1 classifier. This is the exact hole
# gen 1 section 9 flagged: "9.2% of who picks are city, state, or street
# columns; the exclusion list only sorts, never filters." Gen 3 filters it.
PLACE_COL_PATTERN = re.compile(
    r"CITY|STATE|REGION|COUNTY|DISTRICT|PLACENAME|STNAME|STREET|ADDR|ZIP|"
    r"POSTAL|NBRHD|SECTOR|TOWN|MUNICIP|LOCALE|NEIGHBORHOOD|SUBADDR|BLOCK|"
    r"^X$|^Y$|LONGLABEL|SHORTLABEL"
)
# who-columns holding one FRAGMENT of a person's name, not an entity name.
# Found by tracing "JOHNSON" (46 tables, 664K rows in NPPES alone) back to
# PROVIDER_LAST_NAME_LEGAL_NAME / AUTHORIZED_OFFICIAL_LAST_NAME: a surname
# column, not an org. Thousands of unrelated Dr. Johnsons, not one entity.
PERSON_FRAGMENT_COL_PATTERN = re.compile(
    r"LAST_?NAME|FIRST_?NAME|MIDDLE_?NAME|SURNAME|GIVEN_?NAME|_LNAME|_FNAME|"
    r"_MI$|MIDDLE_INIT|"
    # round 2: the verify-agent pass (2026-09-03) found the same surname leak
    # riding columns the round-1 pattern above doesn't catch — NAME_LAST is
    # LAST-then-NAME reversed, a bare "LAST"/"FIRST" column, lobbyist filer
    # name fields, a name+org field mashed into one, and court party fields.
    r"^LAST$|^FIRST$|^PLT$|^DEF$|"
    r"NAME_LAST|NAME_FIRST|NAME_MIDDLE|NAME_SURNAME|NAME_FORENAME|"
    r"FAMILY_NAME|FILER_NAML|FILER_NAMF|FILERNAMELAST|FILERNAMEFIRST|"
    r"PRVDR_LAST_ORG_NAME|CASE_NAME_SHORT|SIGNERPRINTEDNAME|"
    r"RECIPIENTNAMELAST|RECIPIENTNAMEFIRST"
)
# who-columns holding a county name, not an entity — found via JOHNSON/JACKSON
# leaking through NOAA/HUD/Census fields that don't end in the literal word
# "COUNTY" (the PLACE_COL_PATTERN regex above only catches that suffix).
COUNTY_COL_PATTERN = re.compile(r"^CZ_NAME$|^CNTY_NM2KX$|^CURCNTY_NM$")
# a THIRD noise type, found in phase-A round 2 verification (54 of 169 hits):
# category/classification fields, not names at all. OSHA injury narratives,
# job titles, political party, pollutant names, medical diagnoses all get
# tagged "who" the same as a real name column. Traced by looking up which
# column actually held STRAIN/ATTORNEY/DEMOCRAT/KITCHEN in each source table.
CATEGORY_COL_PATTERN = re.compile(
    r"^PARTY$|PARTY_DETAILED|OCCUPATION|POLLUTANT|DIAGNOSIS|"
    r"INJURY|ILLNESS|INCIDENT_LOCATION|JOB_TITLE|^POSITION$|ENTY_TITLE|"
    r"TITLEOFCLASS|SUBGROUP|STUB_LABEL|OTHER_TYPE_TEXT"
)
# a handful of (table, column) exceptions too specific to generalize into a
# regex: XC_CENSUS_CB_COUNTY's own NAME column holds bare county names
# ("Jackson", not "Jackson County") — but "NAME" is too generic a column
# name to blacklist everywhere without killing real entity-name columns.
TABLE_COL_EXCEPTIONS = {
    ("XC_CENSUS_CB_COUNTY", "NAME"),
}

LEGAL_SUFFIXES = {
    "INC", "LLC", "LP", "LLP", "CO", "CORP", "CORPORATION", "LTD", "COMPANY",
    "PLC", "PC", "PA", "THE", "LC", "LTDA", "COS", "CO INC",
}

# noise values seen in gen-1's residue note plus obvious placeholders.
STOPLIST = {
    "SELF EMPLOYED", "NOT EMPLOYED", "UNEMPLOYED", "RETIRED",
    "HOMEMAKER", "NONE", "N A", "NA", "UNKNOWN", "INFORMATION REQUESTED",
    "INFORMATION REQUESTED PER BEST EFFORTS", "REQUESTED", "N/A",
    "OTHER", "MISC", "MISCELLANEOUS", "VARIOUS", "MULTIPLE", "TBD", "PENDING",
    "UNAVAILABLE", "NOT APPLICABLE", "NOT AVAILABLE", "NOT REPORTED",
    "SELF", "SELF EMPLOYED", "PRESIDENT", "VICE PRESIDENT", "GOVERNMENT",
    "OWNER", "MANAGER", "EMPLOYEE", "CEO", "DIRECTOR", "RESIDENCE",
    "RESIDENTIAL", "COMMERCIAL", "INDUSTRIAL", "AGRICULTURAL", "VACANT",
}
# a top-60 major US city — bare city names leak through non-place-tagged
# columns (FEC candidate mailing city, EIA utility city) same as countries.
US_CITIES = {
    "NEW YORK", "LOS ANGELES", "CHICAGO", "HOUSTON", "PHOENIX",
    "PHILADELPHIA", "SAN ANTONIO", "SAN DIEGO", "DALLAS", "AUSTIN",
    "JACKSONVILLE", "FORT WORTH", "COLUMBUS", "CHARLOTTE", "SAN FRANCISCO",
    "INDIANAPOLIS", "SEATTLE", "DENVER", "WASHINGTON", "BOSTON",
    "NASHVILLE", "OKLAHOMA CITY", "EL PASO", "PORTLAND", "LAS VEGAS",
    "DETROIT", "MEMPHIS", "LOUISVILLE", "BALTIMORE", "MILWAUKEE",
    "ALBUQUERQUE", "TUCSON", "FRESNO", "SACRAMENTO", "MESA", "KANSAS CITY",
    "ATLANTA", "OMAHA", "COLORADO SPRINGS", "RALEIGH", "MIAMI",
    "LONG BEACH", "VIRGINIA BEACH", "OAKLAND", "MINNEAPOLIS", "TULSA",
    "TAMPA", "ARLINGTON", "NEW ORLEANS", "WICHITA", "CLEVELAND",
    "BAKERSFIELD", "AURORA", "ANAHEIM", "HONOLULU", "SANTA ANA",
    "RIVERSIDE", "CORPUS CHRISTI", "LEXINGTON", "STOCKTON", "ST LOUIS",
}
# a bare hex-looking string is a hash (e.g. _SRC_SHA256), not a name.
HEX_RE = re.compile(r"^[0-9A-F]{20,}$")
# ISO-ish common-English short names, uppercase — countries are places, not
# entities, and slip past the who-column filter because country fields get
# tagged "who" (e.g. FATCA jurisdiction, FAERS reporter country).
COUNTRIES = {
    "AFGHANISTAN", "ALBANIA", "ALGERIA", "ANDORRA", "ANGOLA", "ARGENTINA",
    "ARMENIA", "AUSTRALIA", "AUSTRIA", "AZERBAIJAN", "BAHAMAS", "BAHRAIN",
    "BANGLADESH", "BARBADOS", "BELARUS", "BELGIUM", "BELIZE", "BENIN",
    "BHUTAN", "BOLIVIA", "BOSNIA", "BOTSWANA", "BRAZIL", "BRUNEI",
    "BULGARIA", "BURKINA FASO", "BURUNDI", "CAMBODIA", "CAMEROON", "CANADA",
    "CHAD", "CHILE", "CHINA", "COLOMBIA", "COMOROS", "CONGO", "COSTA RICA",
    "CROATIA", "CUBA", "CYPRUS", "CZECHIA", "CZECH REPUBLIC", "DENMARK",
    "DJIBOUTI", "DOMINICA", "ECUADOR", "EGYPT", "EL SALVADOR", "ERITREA",
    "ESTONIA", "ESWATINI", "ETHIOPIA", "FIJI", "FINLAND", "FRANCE", "GABON",
    "GAMBIA", "GEORGIA", "GERMANY", "GHANA", "GREECE", "GRENADA",
    "GUATEMALA", "GUINEA", "GUYANA", "HAITI", "HONDURAS", "HONG KONG",
    "HUNGARY", "ICELAND", "INDIA", "INDONESIA", "IRAN", "IRAQ", "IRELAND",
    "ISRAEL", "ITALY", "JAMAICA", "JAPAN", "JORDAN", "KAZAKHSTAN", "KENYA",
    "KIRIBATI", "KOSOVO", "KUWAIT", "KYRGYZSTAN", "LAOS", "LATVIA",
    "LEBANON", "LESOTHO", "LIBERIA", "LIBYA", "LIECHTENSTEIN", "LITHUANIA",
    "LUXEMBOURG", "MACAU", "MADAGASCAR", "MALAWI", "MALAYSIA", "MALDIVES",
    "MALI", "MALTA", "MAURITANIA", "MAURITIUS", "MEXICO", "MOLDOVA",
    "MONACO", "MONGOLIA", "MONTENEGRO", "MOROCCO", "MOZAMBIQUE", "MYANMAR",
    "NAMIBIA", "NEPAL", "NETHERLANDS", "NEW ZEALAND", "NICARAGUA", "NIGER",
    "NIGERIA", "NORWAY", "OMAN", "PAKISTAN", "PALAU", "PANAMA",
    "PAPUA NEW GUINEA", "PARAGUAY", "PERU", "PHILIPPINES", "POLAND",
    "PORTUGAL", "QATAR", "ROMANIA", "RUSSIA", "RWANDA", "SAMOA",
    "SAN MARINO", "SAUDI ARABIA", "SENEGAL", "SERBIA", "SEYCHELLES",
    "SIERRA LEONE", "SINGAPORE", "SLOVAKIA", "SLOVENIA", "SOMALIA",
    "SOUTH AFRICA", "SOUTH KOREA", "SOUTH SUDAN", "SPAIN", "SRI LANKA",
    "SUDAN", "SURINAME", "SWEDEN", "SWITZERLAND", "SYRIA", "TAIWAN",
    "TAJIKISTAN", "TANZANIA", "THAILAND", "TOGO", "TONGA",
    "TRINIDAD AND TOBAGO", "TUNISIA", "TURKEY", "TURKMENISTAN", "TUVALU",
    "UGANDA", "UKRAINE", "UNITED ARAB EMIRATES", "UNITED KINGDOM",
    "UNITED STATES", "UNITED STATES OF AMERICA", "USA", "URUGUAY",
    "UZBEKISTAN", "VANUATU", "VATICAN CITY", "VENEZUELA", "VIETNAM",
    "YEMEN", "ZAMBIA", "ZIMBABWE",
}
US_STATES = {
    "ALABAMA", "ALASKA", "ARIZONA", "ARKANSAS", "CALIFORNIA", "COLORADO",
    "CONNECTICUT", "DELAWARE", "FLORIDA", "GEORGIA", "HAWAII", "IDAHO",
    "ILLINOIS", "INDIANA", "IOWA", "KANSAS", "KENTUCKY", "LOUISIANA",
    "MAINE", "MARYLAND", "MASSACHUSETTS", "MICHIGAN", "MINNESOTA",
    "MISSISSIPPI", "MISSOURI", "MONTANA", "NEBRASKA", "NEVADA",
    "NEW HAMPSHIRE", "NEW JERSEY", "NEW MEXICO", "NEW YORK",
    "NORTH CAROLINA", "NORTH DAKOTA", "OHIO", "OKLAHOMA", "OREGON",
    "PENNSYLVANIA", "RHODE ISLAND", "SOUTH CAROLINA", "SOUTH DAKOTA",
    "TENNESSEE", "TEXAS", "UTAH", "VERMONT", "VIRGINIA", "WASHINGTON",
    "WEST VIRGINIA", "WISCONSIN", "WYOMING", "DISTRICT OF COLUMBIA",
}
COUNTY_RE = re.compile(r"^[A-Z .]+ COUNTY$")
FLOOR_RE = re.compile(r"^\d+(ST|ND|RD|TH)\s+FLOOR$")
SUITE_RE = re.compile(r"^(SUITE|STE|UNIT|APT|FL)\s*#?\s*\d*[A-Z]?$")
PUNCT_RE = re.compile(r"[^A-Z0-9 ]")
WS_RE = re.compile(r"\s+")


def is_noise(raw_upper):
    # punctuation-normalized form so "SELF-EMPLOYED" matches "SELF EMPLOYED"
    norm = WS_RE.sub(" ", PUNCT_RE.sub(" ", raw_upper)).strip()
    if norm in STOPLIST or norm in US_STATES or norm in COUNTRIES or norm in US_CITIES:
        return True
    if COUNTY_RE.match(raw_upper) or FLOOR_RE.match(raw_upper) or SUITE_RE.match(raw_upper):
        return True
    if raw_upper.replace(" ", "").isdigit():
        return True
    if HEX_RE.match(raw_upper.replace(" ", "").replace("-", "")):
        return True
    if len(raw_upper) < 3:
        return True
    return False


def normalize_key(raw_upper):
    cleaned = PUNCT_RE.sub(" ", raw_upper)
    cleaned = WS_RE.sub(" ", cleaned).strip()
    tokens = cleaned.split(" ")
    while tokens and tokens[-1] in LEGAL_SUFFIXES:
        tokens.pop()
    if not tokens:
        return None
    return "".join(tokens)


def main():
    files = sorted(JSON_DIR.glob("*.json"))
    clusters = defaultdict(lambda: {
        "display": None, "display_count": -1,
        "variants": defaultdict(int),   # raw string -> total row count
        "tables": defaultdict(set),     # table -> set of columns
    })
    skipped_place_cols = 0
    seen_cols = set()
    n_tables_scanned = 0

    for fp in files:
        table = fp.stem
        if table.startswith("PORTAL_"):
            continue
        n_tables_scanned += 1
        data = json.loads(fp.read_text(encoding="utf-8"))
        who = data.get("who", {})
        for col, payload in who.items():
            col_u = col.upper()
            if (table, col_u) in TABLE_COL_EXCEPTIONS:
                skipped_place_cols += 1
                continue
            if (PLACE_COL_PATTERN.search(col_u) or PERSON_FRAGMENT_COL_PATTERN.search(col_u)
                    or COUNTY_COL_PATTERN.search(col_u) or CATEGORY_COL_PATTERN.search(col_u)):
                skipped_place_cols += 1
                continue
            seen_cols.add(f"{table}.{col}")
            rows = payload.get("by_rows", []) or []
            for entry in rows:
                if len(entry) < 2:
                    continue
                raw, cnt = entry[0], entry[1]
                if raw is None:
                    continue
                raw_upper = str(raw).strip().upper()
                if not raw_upper or raw_upper == "NONE":
                    continue
                if is_noise(raw_upper):
                    continue
                key = normalize_key(raw_upper)
                if not key or len(key) < 3:
                    continue
                c = clusters[key]
                c["variants"][raw_upper] += cnt
                c["tables"][table].add(col)
                if cnt > c["display_count"]:
                    c["display_count"] = cnt
                    c["display"] = raw_upper

    # tier-1 output, ranked by distinct non-portal table count.
    # Split by token count: a single leftover token (WALMART, SMITH) is
    # ambiguous between "one distinctive brand" and "common surname shared
    # by many unrelated people" and needs a verifier; 2+ tokens (TENNESSEE
    # VALLEY AUTHORITY, MARTIN MARIETTA MATERIALS) is safe by construction —
    # coincidental collision across independent tables is far less likely.
    tier1 = []
    for key, c in clusters.items():
        n_tables = len(c["tables"])
        if n_tables < 3:
            continue
        display = c["display"]
        n_tokens = len(PUNCT_RE.sub(" ", display).split())
        table_cols = [f"{t}:{','.join(sorted(cols))}" for t, cols in sorted(c["tables"].items())]
        tier1.append({
            "key": key,
            "display": display,
            "n_tables": n_tables,
            "n_tokens": n_tokens,
            "n_variants": len(c["variants"]),
            "tables": sorted(c["tables"].keys()),
            "table_cols": table_cols,
            "variants": sorted(c["variants"].items(), key=lambda x: -x[1]),
        })
    tier1.sort(key=lambda r: -r["n_tables"])
    multi = [r for r in tier1 if r["n_tokens"] >= 2]
    single = [r for r in tier1 if r["n_tokens"] == 1]

    def write_csv(rows, path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["key", "display", "n_tables", "n_variants", "tables", "variants"])
            for r in rows:
                w.writerow([
                    r["key"], r["display"], r["n_tables"], r["n_variants"],
                    "; ".join(r["tables"]),
                    "; ".join(f"{v}({n})" for v, n in r["variants"][:8]),
                ])

    write_csv(multi, OUT_DIR / "clusters_multiword.csv")
    write_csv(single, OUT_DIR / "clusters_singleword.csv")

    # tier-2: prefix-link tier-1 keys (min shared length 5), union-find
    keys_sorted = sorted((r["key"] for r in tier1), key=len)
    parent = {k: k for k in keys_sorted}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for i, short in enumerate(keys_sorted):
        if len(short) < 5:
            continue
        for long in keys_sorted[i + 1:]:
            if len(long) <= len(short):
                continue
            if long.startswith(short):
                union(short, long)

    groups = defaultdict(list)
    by_key = {r["key"]: r for r in tier1}
    for k in keys_sorted:
        groups[find(k)].append(k)

    parent_rows = []
    for root, members in groups.items():
        if len(members) < 2:
            continue
        combined_tables = set()
        for m in members:
            combined_tables.update(by_key[m]["tables"])
        parent_rows.append({
            "root": root,
            "members": members,
            "member_displays": [by_key[m]["display"] for m in members],
            "n_tables_union": len(combined_tables),
        })
    parent_rows.sort(key=lambda r: -r["n_tables_union"])

    with open(OUT_DIR / "parent_groups.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["root", "n_members", "n_tables_union", "member_displays"])
        for r in parent_rows:
            w.writerow([r["root"], len(r["members"]), r["n_tables_union"],
                        "; ".join(r["member_displays"])])

    print(f"tables scanned (non-portal): {n_tables_scanned}")
    print(f"who-columns kept: {len(seen_cols)}; place-pattern who-columns skipped: {skipped_place_cols}")
    print(f"raw clusters (any table count): {len(clusters)}")
    print(f"tier-1 clusters (>=3 tables): {len(tier1)}  multi-word: {len(multi)}  single-word: {len(single)}")
    print(f"tier-2 parent-groups (>=2 members): {len(parent_rows)}")
    print("top 20 MULTI-WORD (safer) by table count:")
    for r in multi[:20]:
        print(f"  {r['n_tables']:3d}  {r['display']}")
    print("top 20 SINGLE-WORD (needs verify) by table count:")
    for r in single[:20]:
        print(f"  {r['n_tables']:3d}  {r['display']}")


if __name__ == "__main__":
    main()
