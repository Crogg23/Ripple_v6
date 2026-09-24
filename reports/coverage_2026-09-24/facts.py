"""Turn battery.jsonl into one plain fact line per table, plus the data traps it caught.

Newest line per table wins. Writes facts.tsv and traps.tsv beside this file.
The score column is sort order only, never a filter: every table stays on the menu.
"""
import csv
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import ledger as L  # noqa: E402


def num(x):
    try:
        v = float(x)
        return None if math.isnan(v) else v
    except (TypeError, ValueError):
        return None


def big(v):
    if v is None:
        return "?"
    a = abs(v)
    for d, s in ((1e12, "T"), (1e9, "B"), (1e6, "M"), (1e3, "K")):
        if a >= d:
            return f"{v / d:.1f}{s}"
    return f"{v:.0f}" if a >= 10 else f"{v:.2g}"


def sentinel(v):
    if v is None:
        return False
    s = str(int(abs(v))) if abs(v) >= 999 and float(v).is_integer() else ""
    return bool(s) and len(set(s)) == 1 and s[0] == "9"


def load():
    last = {}
    for line in (HERE / "battery.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            last[r["table"]] = r
    return last


def facts(r, plain):
    out, traps = [], []
    if r.get("fatal"):
        return dict(line=f"FAILED: {r['fatal'][:120]}", score=-9), [("fatal", r["fatal"][:200])]
    prof = (r["q"].get("profile") or {})
    if prof.get("err"):
        return dict(line=f"FAILED profile: {prof['err'][:120]}", score=-9), [("query error", prof["err"][:200])]
    p = prof.get("row") or {}
    n = num(p.get("N")) or 0
    out.append(f"{big(n)} rows")
    if r.get("date") and p.get("D_MIN"):
        out.append(f"{r['date']} {str(p['D_MIN'])[:10]} to {str(p['D_MAX'])[:10]}")
    s = dict(conc=0, tail=0, mass=math.log10(max(n, 1)), money=0)
    for i, m in enumerate(r["metrics"]):
        nn, nd = num(p.get(f"NN{i}")) or 0, num(p.get(f"ND{i}")) or 0
        mx, sm, p50 = num(p.get(f"MX{i}")), num(p.get(f"SM{i}")), num(p.get(f"P50_{i}"))
        if n and nn == 0:
            traps.append(("empty column", f"{m} is null on all {int(n):,} rows"))
            continue
        if n > 100 and nd == 1:
            traps.append(("constant column", f"{m} holds one value, {p.get(f'MN{i}')}, on {int(nn):,} rows"))
            continue
        if sentinel(mx):
            traps.append(("ceiling value", f"{m} max is {mx:,.0f}, a 9s sentinel"))
        fill = f", {nn / n:.0%} filled" if n and nn / n < 0.9 else ""
        out.append(f"{m}: sum {big(sm)}, median {big(p50)}, max {big(mx)}{fill}")
        if i == 0 and r["metrics"][0] in (r.get("money_cols") or r["metrics"]) and sm and sm > 0:
            s["money"] = math.log10(sm)
    tail = ((r["q"].get("tail") or {}).get("row") or {})
    t1 = num(tail.get("TOP1_SHARE"))
    if t1 is not None and n >= 1000 and 0 <= t1 <= 1:
        out.append(f"top 1% of rows hold {t1:.0%} of {r['metrics'][0]}; {int(num(tail.get('OVER10X')) or 0):,} rows over 10x median")
        s["tail"] = t1
    act = r["q"].get("actors") or {}
    if act.get("err"):
        traps.append(("query error", f"actor rollup on {r['actor']}: {act['err'][:150]}"))
    rows = act.get("rows") or []
    if rows:
        tc, ts, nk = num(rows[0]["TC"]) or 0, num(rows[0]["TS"]), num(rows[0]["NK"]) or 0
        top = rows[0]
        byS = ts not in (None, 0) and num(top["S"]) is not None
        share = (num(top["S"]) / ts) if byS else (num(top["C"]) / tc if tc else 0)
        what = r["metrics"][0] if byS else "rows"
        names = "; ".join(f"{str(x['K'])[:40]} {big(num(x['S']) if byS else num(x['C']))}" for x in rows[:3])
        out.append(f"{int(nk):,} distinct {r['actor']}; top holds {share:.0%} of {what}: {names}")
        a_nn = num(p.get("A_NN")) or 0
        if n and a_nn == 0:
            traps.append(("empty column", f"{r['actor']} is null on all {int(n):,} rows"))
        if nk >= 20:
            s["conc"] = share
    cats = ((r["q"].get("cats") or {}).get("row") or {})
    for i, c in enumerate(r.get("cats") or []):
        try:
            tk = json.loads(cats.get(f"TK{i}") or "[]")
        except ValueError:
            tk = []
        if tk:
            out.append(f"{c} top: " + ", ".join(f"{str(v)[:30]} {big(num(k))}" for v, k in tk[:3]))
    score = round(s["mass"] / 2 + s["money"] / 3 + 3 * s["conc"] + 2 * s["tail"], 2)
    return dict(line=" | ".join(out), score=score), traps


def main():
    T = L.load_catalog()
    B = load()
    rows, traps = [], []
    for name, r in B.items():
        t = T.get(name, {})
        r["money_cols"] = t.get("money", [])
        f, tr = facts(r, t)
        rows.append(dict(table=name, schema=r.get("schema", ""), tags=" ".join(t.get("tags", [])), score=f["score"],
                         summary=re.sub(r"\s+", " ", t.get("summary", ""))[:300], facts=f["line"]))
        traps += [dict(table=name, kind=k, detail=d) for k, d in tr]
    rows.sort(key=lambda x: -x["score"])
    for fn, data, cols in (("facts.tsv", rows, ["table", "schema", "tags", "score", "summary", "facts"]),
                           ("traps.tsv", traps, ["table", "kind", "detail"])):
        with (HERE / fn).open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, cols, delimiter="\t")
            w.writeheader()
            w.writerows(data)
    print(f"{len(rows)} tables, {len(traps)} traps, {sum(1 for x in rows if x['score'] == -9)} failed")


if __name__ == "__main__":
    main()
