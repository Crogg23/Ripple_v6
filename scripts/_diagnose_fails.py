"""Quick diagnostic for failed downloads."""
import requests, io, zipfile

UA = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}

# --- OSHA ---
print("=== OSHA Inspection ===")
url = "https://enforcedata.dol.gov/views/data_catalogs/osha/osha_inspection_20250701.csv.zip"
r = requests.get(url, timeout=60, headers=UA, stream=True)
print(f"Status: {r.status_code}")
ct = r.headers.get("content-type", "?")
cl = r.headers.get("content-length", "?")
print(f"Content-Type: {ct}")
print(f"Content-Length: {cl}")
chunk = next(r.iter_content(500))
print(f"Magic bytes: {chunk[:4].hex()}")
# ZIP magic = 504b0304, GZIP = 1f8b
if chunk[:2] == b"\x1f\x8b":
    print("  -> GZIP detected (not ZIP)")
elif chunk[:4] == b"PK\x03\x04":
    print("  -> Valid ZIP")
else:
    print(f"  -> Raw text? First line: {chunk[:200].decode('utf-8', errors='replace')[:200]}")
r.close()

# Try without .zip extension
print("\n=== OSHA without .zip ===")
url2 = "https://enforcedata.dol.gov/views/data_catalogs/osha/osha_inspection_20250701.csv"
r2 = requests.head(url2, timeout=15, headers=UA, allow_redirects=True)
print(f"Status: {r2.status_code}")

# Try the catalog page to find real links
print("\n=== DOL Data Catalog Page ===")
r3 = requests.get("https://enforcedata.dol.gov/views/data_summary.php", timeout=15, headers=UA)
import re
links = re.findall(r'href="([^"]*osha[^"]*)"', r3.text, re.IGNORECASE)
for l in sorted(set(links))[:10]:
    print(f"  {l}")

print("\n=== Google Political Ads ===")
url = "https://storage.googleapis.com/transparencyreport/google-political-ads-transparency-bundle.zip"
r = requests.get(url, timeout=120, headers=UA)
print(f"Status: {r.status_code}, Size: {len(r.content):,}")
ct = r.headers.get("content-type", "?")
print(f"Content-Type: {ct}")
try:
    with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
        names = zf.namelist()
        print(f"Files: {len(names)}")
        for n in names[:20]:
            size = zf.getinfo(n).file_size
            print(f"  {size:>12,} {n}")
except Exception as e:
    print(f"Not a ZIP: {e}")
    print(f"First 200 chars: {r.content[:200].decode('utf-8', errors='replace')}")
