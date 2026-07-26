"""Find actual OSHA download mechanism."""
import requests, re

UA = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}

# Get the OSHA catalog page
r = requests.get("https://enforcedata.dol.gov/views/data_catalogs/osha/", timeout=15, headers=UA)
print(f"Catalog page: {r.status_code}, {len(r.content)} bytes")

# Find all links
links = re.findall(r'href="([^"]+)"', r.text)
data_links = [l for l in links if "csv" in l.lower() or "download" in l.lower() or "zip" in l.lower() or "data" in l.lower()]
print(f"\nData-related links ({len(data_links)}):")
for l in data_links[:20]:
    print(f"  {l}")

# Also show all links
print(f"\nAll links ({len(links)}):")
for l in links[:30]:
    print(f"  {l}")

# Try with a session (cookie-based)
print("\n=== Session-based approach ===")
s = requests.Session()
s.headers.update(UA)
r1 = s.get("https://enforcedata.dol.gov/views/data_catalogs/osha/", timeout=15)
print(f"Session cookies: {dict(s.cookies)}")

# Now try the download with cookies
url = "https://enforcedata.dol.gov/views/data_catalogs/osha/osha_inspection_20250701.csv.zip"
r2 = s.get(url, timeout=30)
print(f"\nDownload attempt: {r2.status_code}, {len(r2.content)} bytes")
print(f"Content-Type: {r2.headers.get('content-type')}")
if r2.content[:4] == b"PK\x03\x04":
    print("  -> Valid ZIP!")
elif r2.content[:2] == b"\x1f\x8b":
    print("  -> GZIP!")
else:
    print(f"  -> First 100: {r2.content[:100].decode('utf-8', errors='replace')[:100]}")
