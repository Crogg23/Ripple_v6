"""Try OSHA API and check if OSHA data is available via other portals."""
import requests, re

UA = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}

# OSHA has an API for inspections - try direct DOL API paths
# The old DOL developer API had specific datasets
print("=== DOL API prod (various paths) ===")
tests = [
    # Old patterns that used to work
    "https://apiprod.dol.gov/v4/DOL_OSHA_Inspection?$limit=5&$format=csv",
    "https://apiprod.dol.gov/v4/osha-enforcement?$limit=5&$format=csv",
    # Try without $
    "https://apiprod.dol.gov/v4/DOL_OSHA_Inspection",
]
for u in tests:
    try:
        r = requests.get(u, timeout=10, headers=UA)
        ct = r.headers.get("content-type", "?")
        print(f"  {r.status_code} {ct[:30]} {u.split('/')[-1][:50]}")
        if r.status_code == 200 and not r.text.startswith("<"):
            print(f"    {r.text[:150]}")
    except Exception as e:
        print(f"  ERR {str(e)[:50]}")

# Try Socrata dataset on data.gov for OSHA
print("\n=== data.gov OSHA datasets ===")
r = requests.get(
    "https://catalog.data.gov/api/3/action/package_search?q=OSHA+inspection&rows=5",
    timeout=15, headers=UA
)
if r.status_code == 200:
    import json
    data = r.json()
    results = data.get("result", {}).get("results", [])
    for res in results:
        title = res.get("title", "?")
        resources = res.get("resources", [])
        csv_res = [rr for rr in resources if "csv" in rr.get("format", "").lower()]
        if csv_res:
            print(f"  {title}")
            print(f"    {csv_res[0].get('url', '?')[:120]}")

# Also try the DOL enforcement with a Selenium-like cookie approach
# Actually let's check if enforcedata has a JSON API behind the scenes
print("\n=== enforcedata.dol.gov JSON API ===")
api_tests = [
    "https://enforcedata.dol.gov/api/osha/inspection?limit=5",
    "https://enforcedata.dol.gov/views/data_catalogs/osha/osha_inspection.json",
    "https://enforcedata.dol.gov/api/v1/osha_inspection?limit=5",
]
for u in api_tests:
    try:
        r = requests.get(u, timeout=10, headers=UA)
        ct = r.headers.get("content-type", "?")
        print(f"  {r.status_code} {ct[:30]} {u.split('/')[-1][:50]}")
        if r.status_code == 200 and not r.text.startswith("<"):
            print(f"    {r.text[:150]}")
    except Exception as e:
        print(f"  ERR {str(e)[:50]}")
