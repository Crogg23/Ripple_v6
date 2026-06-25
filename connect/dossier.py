"""connect dossier — type a name or an ID, get every cross-domain row for that entity.

Resolution reuses the SAME normalizer the spine used (keys.normalize_sql), so a
pasted "1164-450-573" matches the stored "1164450573". A name query that hits more
than one entity prints a disambiguation list instead of silently guessing.

    python -m connect dossier --npi 1164450573
    python -m connect dossier --q "alexander frank"
    python -m connect dossier --id ENT_31f992d6d2c9d5b0 --html
"""

from __future__ import annotations

import html
import json
from pathlib import Path

from . import db, store
from .keys import normalize_sql, quote_ident

GOLD = store.cfqn("ENTITY_GOLDEN")
EMAP = store.cfqn("ENTITY_MAP")
INDEX = store.cfqn("ENTITY_INDEX")
AFFIL = db.fqn("FED_CMS_FACILITY_AFFILIATION")
OUT = Path(__file__).resolve().parents[1] / "outputs"


def _norm_input(conn, key: str, raw: str) -> str | None:
    """Canonicalize a user-typed value exactly as the spine stored it.

    normalize_sql inlines the column expression several times, so we bind the raw
    value ONCE as a subquery column (V) and normalize that — not a bare %s, which
    would need as many params as the column is repeated.
    """
    return db.scalar(conn, f"SELECT {normalize_sql(key, 'V')} FROM (SELECT %s AS V)", (raw,))


def _affiliations(conn, npi_value: str) -> list[dict]:
    """For a provider, the CMS facilities they're affiliated with (CCN -> facility)."""
    npi_n = normalize_sql("NPI", quote_ident("NPI"))
    ccn_n = normalize_sql("CCN", quote_ident("CCN"))
    return db.dicts(conn, f"""
        WITH ccns AS (SELECT DISTINCT {ccn_n} AS CCN FROM {AFFIL} WHERE {npi_n} = %s)
        SELECT x.CCN, g.CANONICAL_NAME, g.CANONICAL_ADDR
        FROM ccns x LEFT JOIN {GOLD} g ON g.KEY_TYPE = 'CCN' AND g.KEY_VALUE = x.CCN
        ORDER BY g.CANONICAL_NAME NULLS LAST LIMIT 100""", (npi_value,))


def _dossier(conn, eid: str) -> dict:
    g = db.dicts(conn, f"SELECT * FROM {GOLD} WHERE ENTITY_ID = %s", (eid,))
    m = db.dicts(conn, f"SELECT * FROM {EMAP} WHERE ENTITY_ID = %s", (eid,))
    sources = db.dicts(conn, f"""
        SELECT SOURCE_TABLE, DOMAIN, DISPLAY_LABEL, ROW_COUNT, PREVIEW
        FROM {INDEX} WHERE ENTITY_ID = %s ORDER BY DOMAIN, SOURCE_TABLE""", (eid,))
    golden = g[0] if g else {}
    emap = m[0] if m else {}
    affils = []
    if golden.get("KEY_TYPE") == "NPI":
        affils = _affiliations(conn, golden["KEY_VALUE"])
    return {"entity_id": eid, "golden": golden, "map": emap, "sources": sources, "affiliations": affils}


def _resolve(conn, npi, ccn, ein, entity_id, q):
    """Return (entity_id, candidates). candidates non-empty -> needs disambiguation."""
    if entity_id:
        return entity_id, []
    for key, raw in (("NPI", npi), ("CCN", ccn), ("EIN", ein)):
        if raw:
            nv = _norm_input(conn, key, raw)
            if not nv:
                return None, []
            return db.scalar(conn, f"SELECT ENTITY_ID FROM {EMAP} WHERE KEY_TYPE=%s AND KEY_VALUE=%s", (key, nv)), []
    if q:
        # NAME_NORM is token-SORTED, so a single substring of the sorted query would
        # miss non-contiguous tokens (e.g. "SMITH JOHN" inside "JOHN PAUL SMITH").
        # Require EACH query token to be present instead — order-/gap-insensitive.
        qn = _norm_input(conn, "NAME", q) or ""
        tokens = [t for t in qn.split(" ") if t]
        if not tokens:
            return None, []
        where = " AND ".join(["NAME_NORM LIKE %s"] * len(tokens))
        cands = db.dicts(conn, f"""
            SELECT ENTITY_ID, CANONICAL_NAME, ENTITY_TYPE FROM {GOLD}
            WHERE {where} ORDER BY LENGTH(CANONICAL_NAME), CANONICAL_NAME LIMIT 50""",
            tuple(f"%{t}%" for t in tokens))
        if len(cands) == 1:
            return cands[0]["ENTITY_ID"], []
        return None, cands
    return None, []


# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #
def _preview_str(preview) -> str:
    if not preview:
        return ""
    p = json.loads(preview) if isinstance(preview, str) else preview
    bits = [f"{k}={v}" for k, v in p.items() if v not in (None, "", "null")]
    return "; ".join(bits)


def _print(d: dict) -> None:
    g = d["golden"]
    print("\n" + "=" * 70)
    print(f"{g.get('CANONICAL_NAME', '(no name)')}   [{g.get('ENTITY_TYPE', '?')}]")
    print(f"{d['entity_id']}   {g.get('KEY_TYPE')}={g.get('KEY_VALUE')}", end="")
    if g.get("CANONICAL_ADDR"):
        print(f"   {g['CANONICAL_ADDR']}", end="")
    print("\n" + "=" * 70)
    print(f"appears across {d['map'].get('SOURCE_COUNT', len(d['sources']))} source(s):")
    last_dom = None
    for s in d["sources"]:
        if s["DOMAIN"] != last_dom:
            print(f"\n  [{s['DOMAIN']}]")
            last_dom = s["DOMAIN"]
        prev = _preview_str(s.get("PREVIEW"))
        cnt = f" ({s['ROW_COUNT']} rows)" if s["ROW_COUNT"] and s["ROW_COUNT"] > 1 else ""
        print(f"    {s['SOURCE_TABLE']}{cnt}: {s.get('DISPLAY_LABEL') or ''}"
              + (f"  — {prev}" if prev else ""))
    if d["affiliations"]:
        print(f"\n  [affiliations]  {len(d['affiliations'])} CMS facilit"
              f"{'y' if len(d['affiliations']) == 1 else 'ies'}:")
        for a in d["affiliations"][:25]:
            print(f"    CCN {a['CCN']}: {a.get('CANONICAL_NAME') or '(unnamed)'}"
                  + (f"  {a['CANONICAL_ADDR']}" if a.get("CANONICAL_ADDR") else ""))
    print()


def _disambiguate(q: str, cands: list) -> None:
    print(f"\n{len(cands)} entities match '{q}' — narrow with --id <ENTITY_ID>:")
    for x in cands[:30]:
        print(f"  {x['ENTITY_ID']}   {x['CANONICAL_NAME']}   ({x['ENTITY_TYPE']})")


def _write_json(d: dict) -> Path:
    OUT.mkdir(exist_ok=True)
    p = OUT / f"dossier_{d['entity_id']}.json"
    p.write_text(json.dumps(d, indent=2, default=str))
    print(f"wrote {p}")
    return p


def _write_html(d: dict) -> Path:
    OUT.mkdir(exist_ok=True)
    g = d["golden"]
    esc = html.escape

    def rows():
        out = []
        for s in d["sources"]:
            prev = esc(_preview_str(s.get("PREVIEW")))
            out.append(f"<tr><td class='dom'>{esc(s['DOMAIN'] or '')}</td>"
                       f"<td>{esc(s['SOURCE_TABLE'])}</td>"
                       f"<td>{esc(s.get('DISPLAY_LABEL') or '')}</td>"
                       f"<td class='num'>{s['ROW_COUNT']}</td>"
                       f"<td class='samp'>{prev}</td></tr>")
        return "\n".join(out)

    affils = ""
    if d["affiliations"]:
        items = "".join(f"<li>CCN {esc(a['CCN'])} — {esc(a.get('CANONICAL_NAME') or '(unnamed)')}</li>"
                        for a in d["affiliations"][:100])
        affils = f"<h2>Affiliated facilities ({len(d['affiliations'])})</h2><ul>{items}</ul>"

    page = f"""<!doctype html><html><head><meta charset="utf-8">
<title>Dossier — {esc(g.get('CANONICAL_NAME', ''))}</title>
<style>
 body{{background:#0d1117;color:#e6edf3;font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;margin:0;padding:32px}}
 h1{{margin:0 0 4px;font-size:24px}} .meta{{color:#9aa0a6;margin-bottom:24px}}
 h2{{font-size:16px;color:#c9d1d9;border-bottom:1px solid #30363d;padding-bottom:6px;margin-top:28px}}
 table{{border-collapse:collapse;width:100%}} td,th{{padding:6px 10px;border-bottom:1px solid #21262d;text-align:left}}
 th{{color:#9aa0a6;font-weight:600}} .num{{text-align:right}} .dom{{color:#36c98a}}
 .samp{{color:#9aa0a6;font-size:12px}} ul{{columns:2;color:#c9d1d9}} a{{color:#4da6ff}}
</style></head><body>
<h1>{esc(g.get('CANONICAL_NAME', '(no name)'))}</h1>
<div class="meta">{esc(g.get('ENTITY_TYPE', ''))} · {esc(g.get('KEY_TYPE', ''))}={esc(g.get('KEY_VALUE', ''))}
 · {esc(d['entity_id'])}{(' · ' + esc(g['CANONICAL_ADDR'])) if g.get('CANONICAL_ADDR') else ''}</div>
<h2>Appears across {d['map'].get('SOURCE_COUNT', len(d['sources']))} sources</h2>
<table><tr><th>domain</th><th>source</th><th>label</th><th>rows</th><th>detail</th></tr>
{rows()}</table>
{affils}
</body></html>"""
    p = OUT / f"dossier_{d['entity_id']}.html"
    p.write_text(page, encoding="utf-8")
    print(f"wrote {p}")
    return p


def run(npi=None, ccn=None, ein=None, entity_id=None, q=None, as_json=False, as_html=False) -> None:
    if not any((npi, ccn, ein, entity_id, q)):
        print("give one of --npi / --ccn / --ein / --id / --q")
        return
    if ein:
        # The v1 spine only resolves the health/provider slice (NPI, CCN). Be honest
        # rather than returning a misleading "not found" for an EIN that isn't indexed.
        print("Note: the v1 entity spine indexes NPI (providers) and CCN (facilities) only — "
              "EIN entities aren't in scope yet, so --ein won't resolve.")
        return
    conn = db.connect()
    try:
        eid, cands = _resolve(conn, npi, ccn, ein, entity_id, q)
        if cands:
            _disambiguate(q, cands)
            return
        if not eid:
            print("No matching entity found.")
            return
        d = _dossier(conn, eid)
        if not d["golden"]:
            print(f"No entity {eid} in the spine (run `connect spine` first).")
            return
        if as_json:
            _write_json(d)
        elif as_html:
            _write_html(d)
        else:
            _print(d)
    finally:
        conn.close()


if __name__ == "__main__":
    run()
