#!/usr/bin/env python3
"""C1b live proof -- same target, before vs after Playwright.

Target: BAILII UK Supreme Court judgments index (2024)
        https://www.bailii.org/uk/cases/UKSC/2024/

BAILII sits behind a JavaScript bot-challenge: a plain `requests` GET returns
HTTP 200 with a ~4 KB "checking your browser" interstitial and ZERO case links.
That is the documented C1-Phase-1 wall (static BeautifulSoup failed gracefully).

This script runs BOTH approaches through the *real* ingest executor
(`ingest._execute_fetch`), which is exactly what the agent runs at the LOAD
checkpoint -- it injects `context["render"]`, runs the generated `fetch_data`, and
applies the HTML-junk guard. The only thing it skips is the Snowflake write.

  BEFORE  access_pattern=scrape     (requests + BeautifulSoup) -> blocked, raises
  AFTER   access_pattern=scrape_js  (context["render"] + BS4)  -> N judgment rows

Run:
    PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python scripts/prove_c1b_bailii.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import ingest  # noqa: E402

URL = "https://www.bailii.org/uk/cases/UKSC/2024/"

CONFIG = {
    "source_id": "intl_bailii_uksc_judgments",
    "name": "BAILII UK Supreme Court judgments",
    "url": URL,
    "landing_table": "INTL_BAILII_UKSC_JUDGMENTS",
    "auth": {"type": "none"},
}

# --- BEFORE: the C1-Phase-1 static scrape the agent generates for access_pattern=scrape.
STATIC_CODE = '''
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch_data(context):
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    resp = requests.get(context["url"], headers={"User-Agent": ua}, timeout=30)
    resp.raise_for_status()
    context["source_bytes"] = resp.content
    soup = BeautifulSoup(resp.text, "html.parser")
    rows = []
    for a in soup.select("a[href$='.html']"):
        href = a.get("href", "")
        if re.search(r"/\\d+\\.html$", href):
            rows.append({"title": a.get_text(strip=True), "url": href})
    if not rows:
        raise RuntimeError(
            "No case links found -- the page is a bot-challenge / empty shell, "
            "not the judgments listing (this is the bot wall static scrape can't pass)."
        )
    return pd.DataFrame(rows)
'''

# --- AFTER: the C1b scrape_js code the agent generates -- identical parse, but it
#     fetches via the injected headless browser (context["render"]) instead of requests.
JS_CODE = '''
import re
import pandas as pd
from bs4 import BeautifulSoup

def fetch_data(context):
    html = context["render"](context["url"])   # runs JS, clears the bot challenge
    context["source_bytes"] = html.encode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    seen, rows = set(), []
    for a in soup.select("a[href$='.html']"):
        href = a.get("href", "")
        if re.search(r"/\\d+\\.html$", href) and href not in seen:
            seen.add(href)
            rows.append({"title": a.get_text(strip=True), "url": href})
    if not rows:
        raise RuntimeError("No case links found even after rendering.")
    return pd.DataFrame(rows)
'''


def _attempt(label: str, code: str):
    print(f"\n{'='*70}\n{label}\n{'='*70}")
    try:
        df, raw_bytes, _ = ingest._execute_fetch(CONFIG, code)
        print(f"RESULT: SUCCESS -- {len(df)} rows, {len(raw_bytes or b'')} source bytes")
        print(f"columns: {list(df.columns)}")
        print(df.head(5).to_string(index=False))
        return len(df)
    except Exception as exc:  # noqa: BLE001
        print(f"RESULT: BLOCKED -- {type(exc).__name__}: {exc}")
        return 0


def main() -> int:
    print(f"Target: {URL}")
    before = _attempt("BEFORE  -- access_pattern=scrape (requests + BeautifulSoup)", STATIC_CODE)
    after = _attempt("AFTER   -- access_pattern=scrape_js (context['render'] + BeautifulSoup)", JS_CODE)

    print(f"\n{'='*70}\nVERDICT\n{'='*70}")
    print(f"  static requests : {before} judgment rows")
    print(f"  headless browser: {after} judgment rows")
    ok = before == 0 and after > 0
    print("  -> " + ("PROVEN: blocked without Playwright, works with it."
                      if ok else "INCONCLUSIVE -- see output above."))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
