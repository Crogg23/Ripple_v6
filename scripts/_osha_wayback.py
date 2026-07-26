"""Find OSHA data via Wayback Machine or alternative paths."""
import requests, re

UA = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}

# Check Wayback Machine for cached OSHA CSV
print("=== Wayback Machine ===")
targets = [
    "https://enforcedata.dol.gov/views/data_catalogs/osha/osha_inspection_20250701.csv.zip",
    "https://enforcedata.dol.gov/views/data_catalogs/osha/osha_inspection_20250401.csv.zip",
    "https://enforcedata.dol.gov/views/data_catalogs/osha/osha_inspection_20250101.csv.zip",
    "https://enforcedata.dol.gov/views/data_catalogs/osha/osha_inspection_20241001.csv.zip",
]
for t in targets:
    url = f"https://web.archive.org/web/2/{t}"
    try:
        r = requests.head(url, timeout=15, headers=UA, allow_redirects=True)
        print(f"  {r.status_code} {t.split('/')[-1]} -> {r.url[:100]}")
        if r.status_code == 200:
            # Check if it's actually a zip
            r2 = requests.get(r.url, timeout=15, headers=UA, stream=True)
            chunk = next(r2.iter_content(10))
            r2.close()
            if chunk[:4] == b"PK\x03\x04":
                print(f"    VALID ZIP at: {r.url}")
            else:
                print(f"    Not a zip (magic: {chunk[:4].hex()})")
    except Exception as e:
        print(f"  ERR: {str(e)[:60]}")

# OSHA Severe Violator data (direct from OSHA site)
print("\n=== OSHA Direct Site ===")
osha_tests = [
    "https://www.osha.gov/enforcement/data",
    "https://www.osha.gov/data/commonstats",
]
for u in osha_tests:
    r = requests.get(u, timeout=15, headers=UA)
    links = re.findall(r'href="([^"]+)"', r.text)
    data_links = [l for l in links if "csv" in l.lower() or "download" in l.lower() or "data" in l.lower()]
    if data_links:
        print(f"\n{u}:")
        for l in data_links[:10]:
            print(f"  {l}")

# Check OSHA ITA (Injury Tracking Application)
print("\n=== OSHA ITA ===")
r = requests.get("https://www.osha.gov/injuryreporting", timeout=15, headers=UA)
links = re.findall(r'href="([^"]+)"', r.text)
data_links = [l for l in links if "csv" in l.lower() or "data" in l.lower() or "download" in l.lower() or "ita" in l.lower()]
for l in data_links[:10]:
    print(f"  {l}")
