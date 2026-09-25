"""Fetch every source page and check the searcher's quote is really on it.

exact   = every word of the quote appears on the page, in order, back to back
near    = the longest back-to-back run covers 80%+ of the quote's words
missing = the page loaded but the quote isn't there
blocked = the page wouldn't load: paywall, bot wall, 403, timeout

Punctuation, case, curly quotes and letter-digit spacing are ignored; words and numbers must match.
Pages are cached in pages/ so a re-run doesn't refetch.
Usage: python quotecheck.py [S001 S002 ...]   (no args = every file in search/)
"""
import csv, hashlib, io, json, re, subprocess, sys, unicodedata
from difflib import SequenceMatcher
from pathlib import Path

import requests
from bs4 import BeautifulSoup

HERE = Path(__file__).parent
CACHE = HERE / "pages"
CACHE.mkdir(exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"}

def words(s):
    s = unicodedata.normalize("NFKC", s).lower()
    s = s.replace("’", "'").replace("‘", "'").replace("'", "")
    # letters and digits split apart, so "PM2.5" and "PM 2.5" both read pm 2 5
    return re.findall(r"[a-z]+|[0-9]+", s)

def page_text(url):
    key = CACHE / (hashlib.sha1(url.encode()).hexdigest()[:16] + ".txt")
    if key.exists():
        return key.read_text(encoding="utf-8"), "cached"
    try:
        r = requests.get(url, headers=UA, timeout=30)
        status, content, ctype = r.status_code, r.content, r.headers.get("content-type", "")
    except Exception as e:
        status, content, ctype = f"error {type(e).__name__}", b"", ""
    if status != 200:
        # some sites refuse python's TLS fingerprint but serve curl
        p = subprocess.run(["curl", "-s", "-L", "--max-time", "30", "-A", UA["User-Agent"],
                            "-w", "\n%{http_code}", url], capture_output=True)
        body, _, code = p.stdout.rpartition(b"\n")
        fetched = f"curl {code.decode(errors='ignore').strip()}"
        if code.strip() != b"200":
            # bot walls: fall back to the Internet Archive's copy of the same URL
            body, snap = archived(url)
            if body is None:
                return None, f"http {status} / {fetched} / archive none"
            fetched = f"archive {snap}"
        content, ctype = body, ("pdf" if body[:4] == b"%PDF" else "html")
        status = fetched
    if "pdf" in ctype or url.lower().endswith(".pdf"):
        from pypdf import PdfReader
        try:
            text = "\n".join(p.extract_text() or "" for p in PdfReader(io.BytesIO(content)).pages)
        except Exception as e:
            return None, f"pdf {type(e).__name__}"
    else:
        soup = BeautifulSoup(content, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = soup.get_text(" ")
        # many news sites also carry the article body inside JSON-LD
        for js in BeautifulSoup(content, "html.parser").find_all("script", type="application/ld+json"):
            text += " " + (js.string or "")
    key.write_text(text, encoding="utf-8")
    return text, "http 200" if status == 200 else str(status)

def archived(url):
    try:
        a = requests.get("https://archive.org/wayback/available", params={"url": url}, timeout=30).json()
        snap = a.get("archived_snapshots", {}).get("closest") or {}
        if snap.get("status") != "200":
            return None, None
        # the id_ form serves the page as captured, without the archive's toolbar
        r = requests.get(f"https://web.archive.org/web/{snap['timestamp']}id_/{url}", headers=UA, timeout=60)
        return (r.content, snap["timestamp"]) if r.status_code == 200 else (None, None)
    except Exception:
        return None, None

def check(quote, text):
    q, p = words(quote), words(text)
    if not q:
        return "missing", 0.0
    qs, ps = " ".join(q), " ".join(p)
    if f" {qs} " in f" {ps} ":
        return "exact", 1.0
    m = SequenceMatcher(None, q, p, autojunk=False).find_longest_match(0, len(q), 0, len(p))
    ratio = m.size / len(q)
    return ("near" if ratio >= 0.8 else "missing"), round(ratio, 2)

def main(ids):
    files = sorted((HERE / "search").glob("S*.json"))
    if ids:
        files = [f for f in files if f.stem in ids]
    out = HERE / "quotecheck.tsv"
    old = {}
    if out.exists():
        for r in csv.DictReader(open(out, encoding="utf-8"), delimiter="\t"):
            old[(r["story_id"], r["idx"])] = r
    for f in files:
        d = json.loads(f.read_text(encoding="utf-8"))
        for k in [k for k in old if k[0] == d["story_id"]]:
            del old[k]
        for i, s in enumerate(d.get("sources", [])):
            text, fetch = page_text(s["url"])
            status, ratio = ("blocked", 0.0) if text is None else check(s.get("quote", ""), text)
            old[(d["story_id"], str(i))] = dict(story_id=d["story_id"], idx=str(i), status=status,
                                                ratio=ratio, fetch=fetch, paywalled=s.get("paywalled", False),
                                                url=s["url"])
            print(d["story_id"], i, status, ratio, fetch, s["url"][:90])
    cols = ["story_id", "idx", "status", "ratio", "fetch", "paywalled", "url"]
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        for k in sorted(old, key=lambda k: (k[0], int(k[1]))):
            w.writerow(old[k])

if __name__ == "__main__":
    main(set(sys.argv[1:]))
