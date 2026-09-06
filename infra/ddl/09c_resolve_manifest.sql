CREATE OR REPLACE PROCEDURE LIBRARY_META.REGISTRY.RIPPLE_RESOLVE_MANIFEST("MANIFEST" VARIANT)
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('snowflake-snowpark-python','requests')
HANDLER = 'resolve'
EXTERNAL_ACCESS_INTEGRATIONS = (RIPPLE_BULK_ACCESS)
COMMENT='Turn a manifest spec into the list of files to load. Static list, JSON index, or regex over a listing, with optional S3 paging, newest-stamp picking and an expected file count. A frozen list of dated URLs is a photograph of a directory and 404s the month the publisher sweeps it.'
EXECUTE AS OWNER
AS '
import json
import re
import requests


def _pages(url, paginate):
    """One page, or every page of an S3 bucket listing.

    A public S3 listing caps at 1000 keys and sets IsTruncated; the next page is
    the same URL with ?marker=<last key>. USAspending holds 4,597 keys and the 20
    files wanted sit between position 302 and 4,596, so one fetch misses most.
    """
    import urllib.parse as up
    out, marker, seen = [], "", 0
    while True:
        u = url
        if marker:
            u = url + ("&" if "?" in url else "?") + "marker=" + up.quote(marker, safe="")
        r = requests.get(u, timeout=180, allow_redirects=True,
                         headers={"User-Agent": "Ripple manifest",
                                  "Accept": "application/json"})
        r.raise_for_status()
        out.append(r.text)
        if paginate != "s3" or "<IsTruncated>true" not in r.text:
            break
        keys = re.findall(r"<Key>([^<]+)</Key>", r.text)
        if not keys:
            break
        marker = keys[-1]
        seen += len(keys)
        if seen > 100000:
            raise RuntimeError("manifest listing exceeded 100k keys: " + url)
    return out


def _keep_latest(urls, latest_re):
    """Keep only the files carrying the newest version stamp.

    A publisher that rotates monthly leaves one live snapshot and deletes the
    rest, so newest stamp and still exists are the same set. Stamps compare as
    strings, so they must be zero padded.
    """
    stamped = []
    for u in urls:
        m = re.search(latest_re, u)
        if m:
            stamped.append((m.group(1), u))
    if not stamped:
        return urls, None
    newest = max(s for s, _ in stamped)
    return [u for s, u in stamped if s == newest], newest


def resolve(session, manifest):
    m = manifest
    if isinstance(m, str):
        m = json.loads(m)
    if isinstance(m, list):
        return {"urls": list(m), "stamp": None}

    base = m.get("base", "")
    kind = m.get("type", "json")
    if kind == "json":
        r = requests.get(m["url"], timeout=180, allow_redirects=True,
                         headers={"User-Agent": "Ripple manifest",
                                  "Accept": "application/json"})
        r.raise_for_status()
        val = r.json()
        for key in (str(m["path"]).split(".") if m.get("path") else []):
            val = val[int(key)] if isinstance(val, list) else val[key]
        item = m.get("item")
        found = []
        for v in val:
            u = v.get(item) if (item and isinstance(v, dict)) else v
            if isinstance(u, str):
                found.append(u)
    else:
        found = []
        for page in _pages(m["url"], m.get("paginate")):
            found += re.findall(m["path"], page)

    urls, seen = [], set()
    for u in found:
        full = base + u if (base and not u.startswith("http")) else u
        if full not in seen:
            seen.add(full)
            urls.append(full)

    stamp = None
    if m.get("latest_re"):
        urls, stamp = _keep_latest(urls, m["latest_re"])

    want = m.get("expect_files")
    if want and len(urls) != int(want):
        raise RuntimeError(
            f"manifest resolved {len(urls)} files, spec expects {want}. "
            "A publisher mid-sweep looks exactly like this; re-run once it settles.")
    return {"urls": urls, "stamp": stamp, "count": len(urls)}
';
