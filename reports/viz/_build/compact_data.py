"""Compact the extracted JSON into small JS-ready blobs."""
import json, os
OUT = os.path.dirname(os.path.abspath(__file__))
def load(n): return json.load(open(os.path.join(OUT, n)))

def rnd(x, d=2): return round(x, d)

def compact_geom(geom, d=2):
    """GeoJSON Polygon/MultiPolygon -> list of rings [[x,y,...],...] rounded."""
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    out = []
    for poly in polys:
        ring = poly[0]  # outer ring only, holes negligible at this scale
        flat = []
        last = None
        for pt in ring:
            p = (rnd(pt[0], d), rnd(pt[1], d))
            if p != last:
                flat.extend(p)
                last = p
        if len(flat) >= 8:
            out.append(flat)
    return out

# counties
counties = load("counties.json")
arcos = {r["g"]: r for r in load("arcos_county.json")}
epa = {r["g"]: r["n"] for r in load("epa_county.json")}
cty = []
for c in counties:
    if c["s"] in ("PR", "VI", "GU", "MP", "AS"):
        continue
    a = arcos.get(c["g"])
    yrs = (a["y1"] - a["y0"] + 1) if a else None
    cty.append({
        "g": c["g"], "n": c["n"], "s": c["s"], "p": c["p"],
        "mme": rnd(a["mme"], 0) if a else None,
        "yrs": yrs,
        "epa": epa.get(c["g"]),
        "rings": compact_geom(c["geom"]),
    })
json.dump(cty, open(os.path.join(OUT, "c_counties.json"), "w"), separators=(",", ":"))

states = []
for s in load("states.json"):
    if s["s"] in ("PR", "VI", "GU", "MP", "AS"):
        continue
    states.append({"s": s["s"], "rings": compact_geom(s["geom"], 2)})
json.dump(states, open(os.path.join(OUT, "c_states.json"), "w"), separators=(",", ":"))

# flows: [rz,bz,yr,mme,rlat,rlon,blat,blon,rs,bs]
flows = load("flows.json")
out = [[f[0], f[1], f[2], rnd(f[3], 0), rnd(f[4], 3), rnd(f[5], 3), rnd(f[6], 3), rnd(f[7], 3), f[8], f[9]] for f in flows]
json.dump(out, open(os.path.join(OUT, "c_flows.json"), "w"), separators=(",", ":"))
yrs = sorted({f[2] for f in flows})
print("flow years", yrs[0], "-", yrs[-1], "pairs", len({(f[0], f[1]) for f in flows}))

# heartbeat: keep as-is but drop sources with <3 months
hb = load("heartbeat.json")
hb = {k: v for k, v in hb.items() if len(v) >= 3}
json.dump(hb, open(os.path.join(OUT, "c_heartbeat.json"), "w"), separators=(",", ":"))
print("hb sources", len(hb))
for n in ("c_counties.json", "c_states.json", "c_flows.json", "c_heartbeat.json"):
    print(n, os.path.getsize(os.path.join(OUT, n)) // 1024, "KB")
