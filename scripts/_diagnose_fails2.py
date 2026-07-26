"""Check OSHA CSV direct download and Google polads alternatives."""
import requests

UA = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}

# OSHA - try direct CSV (no zip)
print("=== OSHA Direct CSV ===")
url = "https://enforcedata.dol.gov/views/data_catalogs/osha/osha_inspection_20250701.csv"
r = requests.get(url, timeout=60, headers=UA, stream=True)
print(f"Status: {r.status_code}")
ct = r.headers.get("content-type", "?")
cl = r.headers.get("content-length", "?")
print(f"Content-Type: {ct}, Content-Length: {cl}")
chunk = next(r.iter_content(500))
first_line = chunk.decode("utf-8", errors="replace").split("\n")[0]
print(f"Header: {first_line[:200]}")
r.close()

# Also check WHD
print("\n=== WHD Direct CSV ===")
url = "https://enforcedata.dol.gov/views/data_catalogs/whd/whd_whisard_20250701.csv"
r = requests.get(url, timeout=60, headers=UA, stream=True)
print(f"Status: {r.status_code}, CT: {r.headers.get('content-type','?')}, CL: {r.headers.get('content-length','?')}")
chunk = next(r.iter_content(500))
first_line = chunk.decode("utf-8", errors="replace").split("\n")[0]
print(f"Header: {first_line[:200]}")
r.close()

# Google Political Ads - check README for new instructions
print("\n=== Google Polads README ===")
import io, zipfile
r = requests.get("https://storage.googleapis.com/transparencyreport/google-political-ads-transparency-bundle.zip", timeout=30, headers=UA)
with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
    with zf.open("google-political-ads-transparency-bundle/README.txt") as f:
        print(f.read().decode("utf-8"))

# Try individual country files
print("\n=== Google Polads US Creative Stats ===")
for suffix in ["creative-stats", "advertiser-stats", "advertiser-weekly-spend"]:
    url = f"https://storage.googleapis.com/transparencyreport/google-political-ads-transparency-bundle/google-political-ads-{suffix}.csv"
    r = requests.head(url, timeout=10, headers=UA, allow_redirects=True)
    print(f"  {r.status_code} {suffix}")
