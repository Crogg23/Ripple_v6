"""Fix URLs and retry failed datasets from tier1_bulk_batch_load.py run."""
import requests, re

UA = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}

# Check CourtListener
print("=== CourtListener ===")
r = requests.get("https://www.courtlistener.com/help/api/bulk-data/", timeout=15, headers=UA)
links = re.findall(r'href="([^"]+)"', r.text)
bulk_links = [l for l in links if "bulk" in l.lower() or "storage" in l.lower()]
for l in sorted(set(bulk_links))[:20]:
    print(l)

# Check Google polads ZIP contents
print("\n=== Google Political Ads ZIP structure ===")
import io, zipfile
r = requests.get("https://storage.googleapis.com/transparencyreport/google-political-ads-transparency-bundle.zip",
                 timeout=120, headers=UA, stream=True)
# Just get first 100KB to see structure
content = b""
for chunk in r.iter_content(chunk_size=65536):
    content += chunk
    if len(content) > 200_000_000:  # 200MB cap
        break
r.close()
print(f"Downloaded {len(content):,} bytes")
try:
    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        names = zf.namelist()
        print(f"Files in ZIP: {len(names)}")
        csv_files = [n for n in names if n.lower().endswith(".csv")]
        csv_files.sort(key=lambda n: zf.getinfo(n).file_size, reverse=True)
        for n in csv_files[:10]:
            print(f"  {zf.getinfo(n).file_size:>12,} {n}")
except Exception as e:
    print(f"ZIP error: {e}")
