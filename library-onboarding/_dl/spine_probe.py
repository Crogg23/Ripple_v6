import sys, io, re
sys.path.insert(0, r"c:\Code\Ripple_v6\library-onboarding")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from snow import connect

names = [
    # CFPB top complained-about companies
    "TRANSUNION INTERMEDIATE HOLDINGS, INC.",
    "EQUIFAX, INC.",
    "Experian Information Solutions Inc.",
    "BANK OF AMERICA, NATIONAL ASSOCIATION",
    "JPMORGAN CHASE & CO.",
    "WELLS FARGO & COMPANY",
    "CAPITAL ONE FINANCIAL CORPORATION",
    "CITIBANK, N.A.",
    "SYNCHRONY FINANCIAL",
    "ENCORE CAPITAL GROUP INC.",
    # SBA PPP top borrowers
    "GARDEN FRESH RESTAURANTS LLC DBA SWEET TOMATOES  SOUPLANTATI",
    "NAVARRO RESEARCH & ENGINEERING INC",
    "GOODWILL INDUSTRIES OF SOUTHERN CALIF",
    "COMMUNITY BRIDGES INC",
    "HAZELDEN BETTY FORD FOUNDATION",
    "PIONEER HUMAN SERVICES",
    "ISAGENIX WORLDWIDE INC",
    "STAR TRIBUNE MEDIA COMPANY LLC",
    "AMYRIS, INC.",
    "ARCHDIOCESE OF GALVESTON-HOUSTON",
]

def norm(s):
    s = s.upper()
    s = re.sub(r"[.,]", "", s)
    s = re.sub(r"\b(INC|LLC|CORP|CORPORATION|COMPANY|CO|LTD|NATIONAL ASSOCIATION|N A|DBA.*)\b", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

conn = connect()
cur = conn.cursor()

results = []
for nm in names:
    key = norm(nm)
    hits = []
    # OpenSanctions
    cur.execute(
        "select name, c_schema, dataset from library_raw.landing.intl_opensanctions_default "
        "where upper(name) like %s limit 3",
        (f"%{key.split()[0]}%",) if key else ("%",)
    )
    os_rows = [r for r in cur.fetchall() if key == norm(r[0])]
    if os_rows:
        hits.append(("OpenSanctions", os_rows[:2]))
    # GLEIF
    cur.execute(
        'select "Entity.LegalName" from library_raw.landing.intl_gleif where upper("Entity.LegalName") like %s limit 20',
        (f"%{key[:20]}%",)
    )
    gleif_rows = [r for r in cur.fetchall() if key == norm(r[0])]
    if gleif_rows:
        hits.append(("GLEIF", gleif_rows[:2]))
    # ICIJ entities
    cur.execute(
        "select name from library_raw.landing.icij_offshore_leaks_entities where upper(name) like %s limit 20",
        (f"%{key.split()[0]}%",)
    )
    icij_rows = [r for r in cur.fetchall() if key == norm(r[0])]
    if icij_rows:
        hits.append(("ICIJ", icij_rows[:2]))
    results.append((nm, hits))

matched = 0
for nm, hits in results:
    if hits:
        matched += 1
        print("MATCH:", nm, "->", hits)
    else:
        print("no match:", nm)

print()
print(f"MATCH RATE: {matched}/{len(names)}")
