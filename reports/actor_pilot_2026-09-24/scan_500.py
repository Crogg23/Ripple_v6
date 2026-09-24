"""Scan every party-name column for the ~500 seed companies.

Scales past the pilot's 25 by joining on words, not by trying every pattern on every row:
distinct names -> split into words -> equal-join each word to a company's rarest word -> confirm the full pattern.
Read-only. Writes hits_500.csv and log_500.txt next to this file.
"""
import csv
import queue
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).parent))
import ledger as L  # noqa: E402
from connect import db  # noqa: E402
from pilot import DOMAIN, SKIP_TOKENS, ONLY_COLS  # noqa: E402

OUT = Path(__file__).parent
SKIP = SKIP_TOKENS | {"ADDR", "ADDRESS", "ADDRESS1", "ADDRESS2", "ADDR1", "ADDR2", "APT", "DAM", "DEVICE", "STREET"}
GENERIC = set("""AMERICAN NATIONAL UNITED GENERAL FIRST INTERNATIONAL GLOBAL STATE CITY COUNTY FEDERAL
    HEALTH MEDICAL CARE BANK CAPITAL ENERGY POWER SYSTEMS SOLUTIONS TECHNOLOGIES PARTNERS ASSOCIATES
    SERVICES INDUSTRIES MANAGEMENT RESOURCES ENTERPRISES TECHNOLOGY PRODUCTS INSURANCE FINANCIAL
    TRUST SECURITIES PHARMACEUTICALS LABORATORIES HOSPITAL HEALTHCARE ELECTRIC GAS OIL COMMUNICATIONS
    NORTH SOUTH EAST WEST NEW OF AND THE""".split())
lock = __import__("threading").Lock()
log = open(OUT / "log_500.txt", "a", encoding="utf-8")


def say(m):
    with lock:
        log.write(time.strftime("%H:%M:%S ") + m + "\n")
        log.flush()
        print(m, flush=True)


# Plain words that start many company names. Claude's hand list; the surname test below is data-driven.
PLAIN_WORDS = set("""SOUTHERN NORTHERN EASTERN WESTERN CENTRAL PACIFIC ATLANTIC CONTINENTAL NATIONWIDE PROGRESSIVE
    LIBERTY FIDELITY GUARDIAN ALLIED PIONEER DELTA SUMMIT PREMIER SUPERIOR UNIVERSAL STANDARD SOVEREIGN
    AMERICA FRONTIER HERITAGE MERIDIAN EMPIRE CAPITOL PATRIOT EAGLE VICTORY SENTINEL ADVANCED INTEGRATED""".split())


def surnames(words):
    """One-word company names that are also common surnames, counted in the national provider registry."""
    cache = OUT / "surnames.json"
    if cache.exists():
        return set(__import__("json").loads(cache.read_text()))
    c = db.connect()
    lst = ",".join("'" + w.replace("'", "''") + "'" for w in words)
    got = {w for w, n in db.rows(c, f"""SELECT UPPER(PROVIDER_LAST_NAME_LEGAL_NAME), COUNT(*)
        FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES WHERE UPPER(PROVIDER_LAST_NAME_LEGAL_NAME) IN ({lst})
        GROUP BY 1 HAVING COUNT(*) >= 25""")}
    cache.write_text(__import__("json").dumps(sorted(got)))
    return got


def full_name_pattern(r):
    """The shortest raw legal name, as words, e.g. KELLY SERVICES INC. None if it is still one word."""
    import re
    names = sorted({re.sub(r"\s+", " ", re.sub(r"[^A-Z0-9& ]", " ", n.upper())).strip() for n in r["raw_names"].split(" | ")}, key=len)
    names = [n for n in names if len(n.split()) > 1]
    return r"\s+".join(re.escape(w).replace("\\&", "&") for w in names[0].split()) if names else None


def load_seeds():
    rows = list(csv.DictReader(open(OUT / "seeds.csv", encoding="utf-8")))
    single = [r["core"] for r in rows if r["pattern"] and r"\s" not in r["pattern"]]
    risky = surnames(single) | PLAIN_WORDS
    pats = []
    for i, r in enumerate(rows):
        if not r["pattern"]:
            continue
        if r"\s" not in r["pattern"] and r["core"] in risky:
            r["pattern"] = full_name_pattern(r)  # a surname or plain word needs its full legal name
            if not r["pattern"]:
                continue
        words = [w for w in r["core"].split() if w not in GENERIC and len(w) > 2] or r["core"].split()
        anchor = max(words, key=len)
        pats.append((i, anchor, r["pattern"], r["core"]))
    return rows, pats


def cols_for(t):
    if t["table"] in ONLY_COLS:
        return ONLY_COLS[t["table"]]
    return [c for c in t["names"] if not set(L.toks(c)) & SKIP
            and not ("LAST" in L.toks(c) and "ORG" not in L.toks(c))][:6]


def rx(p):
    """Multi-word names match anywhere. A one-word name must open the party name or follow V in a case name:
    HYATT alone matched the Brownstein Hyatt law firm, SOUTHERN matched Norfolk Southern."""
    if r"\s" in p:
        return r"(^|[^A-Z0-9])(" + p + r")([^A-Z0-9]|$)"
    # One word: the whole party name must be that word plus legal endings. PFIZER INC yes, ASHLAND COUNTY no.
    # In a case name the party may sit either side of V, so the name may also end at V or ET AL.
    legal = r"(\s(INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|LLC|L\s?L\s?C|LP|LTD|LIMITED|PLC|HOLDINGS?|GROUP|USA|US|N\s?A|THE))*"
    return r"(^|\sVS?\s)(" + p + r")" + legal + r"($|\sVS?\s|\sET\s)"


def sql_for(t, cols, pats):
    fq = f'LIBRARY_MARTS."{t["schema"]}"."{t["table"]}"'
    union = " UNION ALL ".join(
        f"SELECT '{c}' col, UPPER(\"{c}\"::varchar) v, COUNT(*) n FROM {fq} WHERE \"{c}\" IS NOT NULL GROUP BY 1, 2" for c in cols)
    vals = ",\n".join("({}, '{}', '{}')".format(i, a.replace("'", "''"), rx(p).replace("\\", "\\\\").replace("'", "''"))
                      for i, a, p, _ in pats)
    return f"""
WITH pats(id, anchor, rx) AS (SELECT * FROM VALUES {vals}),
vals AS ({union}),
norm AS (SELECT col, v, n, TRIM(REGEXP_REPLACE(v, '[^A-Z0-9&]+', ' ')) nv FROM vals),
words AS (SELECT DISTINCT col, v, nv, n, w.value::string tok
          FROM norm, LATERAL SPLIT_TO_TABLE(nv, ' ') w)
SELECT p.id, words.col, SUM(words.n) n, COUNT(DISTINCT words.v) nd,
       ARRAY_TO_STRING(ARRAY_SLICE(ARRAY_AGG(DISTINCT LEFT(words.v, 120)), 0, 6), ' | ') samp
FROM words JOIN pats p ON words.tok = p.anchor
WHERE REGEXP_INSTR(words.nv, p.rx) > 0
GROUP BY 1, 2"""


def main():
    rows, pats = load_seeds()
    T = L.load_catalog()
    ts = [t for t in T.values() if t["names"] and not t["derived"] and not t["reference"]
          and t["table"] not in L.DUPLICATE_OF and t["rows"] and cols_for(t)]
    ts.sort(key=lambda t: t["rows"])
    pool = queue.Queue()
    for _ in range(4):
        c = db.connect()
        db.rows(c, "ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 600")
        pool.put(c)
    say(f"start: {len(ts)} tables, {len(pats)} companies")
    out, errs = [], []

    def run(t):
        c = pool.get()
        try:
            t0 = time.time()
            res = db.rows(c, sql_for(t, cols_for(t), pats))
            say(f"ok {time.time() - t0:6.1f}s {t['table']} hits={len(res)}")
            return [dict(company=rows[i]["core"], lists=rows[i]["lists"], domain=DOMAIN.get(t["schema"], t["schema"].lower()),
                         schema=t["schema"], table=t["table"], col=col, rows=n, distinct=nd, sample=s) for i, col, n, nd, s in res]
        except Exception as e:
            errs.append(t["table"])
            say(f"ERR {t['table']}: {str(e)[:150]}")
            return []
        finally:
            pool.put(c)

    with ThreadPoolExecutor(4) as ex:
        for r in ex.map(run, ts):
            out += r
    with (OUT / "hits_500.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["company", "lists", "domain", "schema", "table", "col", "rows", "distinct", "sample"])
        w.writeheader()
        w.writerows(sorted(out, key=lambda r: (r["company"], r["domain"])))
    say(f"done: {len(out)} hits, {len(errs)} errors: {errs}")


if __name__ == "__main__":
    main()
