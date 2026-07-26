"""Check OSHA establishment injury data page for CSVs."""
import requests, re

UA = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}

r = requests.get("https://www.osha.gov/Establishment-Specific-Injury-and-Illness-Data", timeout=15, headers=UA)
links = re.findall(r'href="([^"]+)"', r.text)
csv_links = [l for l in links if ".csv" in l.lower() or ".zip" in l.lower() or ".xlsx" in l.lower()]
print(f"Found {len(csv_links)} data links:")
for l in csv_links[:15]:
    print(f"  {l}")

# Check if any of these are full URLs
for l in csv_links[:5]:
    full = l if l.startswith("http") else f"https://www.osha.gov{l}"
    r2 = requests.head(full, timeout=10, headers=UA, allow_redirects=True)
    ct = r2.headers.get("content-type", "?")
    cl = r2.headers.get("content-length", "?")
    print(f"  {r2.status_code} {ct[:30]} {cl} {full[:80]}")
