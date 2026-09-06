"""Hunch 5 - math and story. Reads the three aggregate CSVs written by queries.py. No warehouse calls.
Run from repo root: PYTHONPATH=reports/tier1_deep_dive_2026-09-05 python3 reports/tier1_deep_dive_2026-09-05/05_disaster_loan_terms/analysis.py"""
import os, json
import pandas as pd
import plotly.graph_objects as go
from _shared.viz import PAL, TEXT2, base_fig, bar_style, write_story

HERE = os.path.dirname(os.path.abspath(__file__))
fe = pd.read_csv(f"{HERE}/fema_county_disaster.csv", dtype={"FIPS5": str, "DN": str}); fe["Y"] = pd.to_datetime(fe.DECL).dt.year
hm = pd.read_csv(f"{HERE}/hmda_county_year.csv", dtype={"FIPS5": str}).dropna(subset=["FIPS5"])
dr = pd.read_csv(f"{HERE}/denial_reasons_county_year.csv", dtype={"FIPS5": str, "REASON": str}).dropna(subset=["FIPS5"])

c15, c16, c17 = (set(fe[fe.Y == y].FIPS5) for y in (2015, 2016, 2017))
anyd = set(fe.FIPS5)
treat = c16 - (c15 | c17)                      # hit in 2016 only: 2015 is a clean before, 2017 a clean after
states = sorted(set(fe[fe.Y == 2016].ST))
h = hm[hm.ST.isin(states)]
tr = h[h.FIPS5.isin(treat)]; co = h[~h.FIPS5.isin(anyd)]
YRS = (2015, 2016, 2017)
n_ctrl = len(set(co[co.YR == 2015].FIPS5) & set(co[co.YR == 2017].FIPS5))  # 896 with activity in both years

def m(df, y):
    d = df[df.YR == y]
    return dict(apps=int(d.APPS.sum()), orig=int(d.ORIG.sum()),
                deny=d.DENIED.sum() / d.APPS.sum() * 100, deny_wide=d.DENIED.sum() / d.APPS_WIDE.sum() * 100, wd=(d.APPS_WIDE.sum()-d.APPS.sum())/d.APPS_WIDE.sum()*100,
                rs=d.ORIG_RS.sum() / d.ORIG.sum() * 100,
                hoepa=d.ORIG_HOEPA.sum() / d.ORIG.sum() * 1e4, hoepa_n=int(d.ORIG_HOEPA.sum()))
T = {y: m(tr, y) for y in YRS}; C = {y: m(co, y) for y in YRS}
did = {k: (T[2017][k] - T[2015][k]) - (C[2017][k] - C[2015][k]) for k in ("deny", "deny_wide", "wd", "rs", "hoepa")}

# per state denial DiD
rows = []
for st in states:
    t, c = tr[tr.ST == st], co[co.ST == st]
    if t.empty or c.empty: continue
    a, b = {y: m(t, y) for y in (2015, 2017)}, {y: m(c, y) for y in (2015, 2017)}
    rows.append(dict(st=st, n=t.FIPS5.nunique(), apps=a[2017]["apps"],
                     deny=(a[2017]["deny"] - a[2015]["deny"]) - (b[2017]["deny"] - b[2015]["deny"]),
                     rs=(a[2017]["rs"] - a[2015]["rs"]) - (b[2017]["rs"] - b[2015]["rs"])))
ps = pd.DataFrame(rows).sort_values("deny")

# county sign test
p = h.pivot_table(index=["ST", "FIPS5"], columns="YR", values=["APPS", "DENIED"], aggfunc="sum").fillna(0)
p["chg"] = p[("DENIED", 2017)] / p[("APPS", 2017)] * 100 - p[("DENIED", 2015)] / p[("APPS", 2015)] * 100
ctrl = p[~p.index.get_level_values(1).isin(anyd)]
sc = ctrl.groupby(level=0).apply(lambda g: (g[("DENIED", 2017)].sum() / g[("APPS", 2017)].sum() - g[("DENIED", 2015)].sum() / g[("APPS", 2015)].sum()) * 100)
tc = p[p.index.get_level_values(1).isin(treat)].copy(); tc = tc[tc[("APPS", 2015)] >= 200]
tc["excess"] = tc.chg - tc.index.get_level_values(0).map(sc)
sign = dict(n=len(tc), beat=int((tc.excess > 0).sum()), med=float(tc.excess.median()))

# placebo: counties hit only in 2017, 2015->2016 change vs their states' controls (nothing should show)
pl = c17 - (c15 | c16); st17 = set(fe[fe.Y == 2017].ST); h2 = hm[hm.ST.isin(st17)]
tp, cp = h2[h2.FIPS5.isin(pl)], h2[~h2.FIPS5.isin(anyd)]
placebo = (m(tp, 2016)["deny"] - m(tp, 2015)["deny"]) - (m(cp, 2016)["deny"] - m(cp, 2015)["deny"])
# dose: declared Jan-Jun 2016 (2016 mostly 'after') vs Jul-Dec
early = set(fe[(fe.Y == 2016) & (pd.to_datetime(fe.DECL).dt.month <= 6)].FIPS5) & treat; late = treat - early
def dd(s, y):
    x = h[h.FIPS5.isin(s)]; return (m(x, y)["deny"] - m(x, 2015)["deny"]) - (C[y]["deny"] - C[2015]["deny"])
dose = dict(early_n=len(early), early16=dd(early, 2016), early17=dd(early, 2017), late_n=len(late), late16=dd(late, 2016), late17=dd(late, 2017))

# denial reasons per 100 applications
dr["cls"] = ["treat" if f in treat else ("ctrl" if f not in anyd else "other") for f in dr.FIPS5]
g = dr[dr.cls.isin(["treat", "ctrl"])].groupby(["cls", "YR", "REASON"]).N.sum().unstack("REASON").fillna(0)
apps = {("treat", y): T[y]["apps"] for y in YRS} | {("ctrl", y): C[y]["apps"] for y in YRS}
NAMES = {"1": "Debt-to-income", "2": "Employment", "3": "Credit history", "4": "Collateral", "5": "Cash", "6": "Unverifiable", "7": "Incomplete", "8": "MI denied", "9": "Other", "none": "No reason given"}
rdid = {}
for r in g.columns:
    rt = {k: g.loc[k, r] / apps[k] * 100 for k in apps}
    rdid[NAMES[r]] = (rt[("treat", 2017)] - rt[("treat", 2015)]) - (rt[("ctrl", 2017)] - rt[("ctrl", 2015)])

stats = dict(treat_counties=len(treat), ctrl_counties=n_ctrl, states=states, T=T, C=C, did=did,
             per_state=ps.to_dict("records"), sign=sign, placebo=placebo, dose=dose, reason_did=rdid,
             c16=len(c16), c16_overlap=len(c16 & (c15 | c17)))
json.dump(stats, open(f"{HERE}/stats.json", "w"), indent=1, default=float)
print(json.dumps(stats, indent=1, default=float))

# ---------------- charts ----------------
def line(fig, name, ys, color, dash=None):
    fig.add_trace(go.Scatter(x=list(YRS), y=ys, name=name, mode="lines+markers+text", text=[f"{v:.1f}" for v in ys],
                             textposition="top center", line=dict(color=color, width=3, dash=dash), marker=dict(size=9),
                             hovertemplate="%{x}: %{y:.2f}<extra>" + name + "</extra>"))

f1 = base_fig("Denials fell everywhere after 2016 - 1.1 points less in the disaster counties",
              "Share of home-loan applications denied, %. Applications = originated + approved-not-accepted + denied.")
line(f1, f"Hit in 2016 ({len(treat)} counties)", [T[y]["deny"] for y in YRS], PAL[1])
line(f1, f"Same-state control ({n_ctrl} counties)", [C[y]["deny"] for y in YRS], PAL[0])
f1.update_layout(xaxis=dict(tickvals=list(YRS)), yaxis=dict(title="denied, % of applications", range=[19, 26]))

f2 = base_fig("Pricing did not move: higher-priced loan share tracks the control within 0.2 points",
              "Share of originated loans reported with a rate spread, %. HOEPA flags are shown in the text, not here.")
line(f2, "Hit in 2016", [T[y]["rs"] for y in YRS], PAL[1])
line(f2, "Same-state control", [C[y]["rs"] for y in YRS], PAL[0])
f2.update_layout(xaxis=dict(tickvals=list(YRS)), yaxis=dict(title="rate-spread loans, % of originations", range=[5.5, 8.5]))

f3 = base_fig("10 of 13 states lean the same way - but no state carries the story alone",
              "Denial-rate change 2015 to 2017, hit counties minus same-state control counties, percentage points.")
cols = [PAL[1] if v > 0 else PAL[0] for v in ps.deny]
f3.add_trace(go.Bar(x=[f"{r.st} ({r.n})" for r in ps.itertuples()], y=ps.deny, marker_color=cols,
                    text=[f"{v:+.1f}" for v in ps.deny], textposition="outside",
                    customdata=ps.apps, hovertemplate="%{x}<br>DiD %{y:+.2f} pts<br>%{customdata:,} applications in 2017<extra></extra>", showlegend=False))
f3.update_layout(yaxis=dict(title="denial DiD, pts"), xaxis=dict(title="state (hit counties in cohort)"), height=460); bar_style(f3)

f4 = base_fig("The whole gap sits in denials with no reason given",
              "Denial DiD by lender-stated reason, per 100 applications, 2015 to 2017. Reason-coded denials net to about zero.")
rd = pd.Series(rdid).sort_values()
f4.add_trace(go.Bar(x=rd.values, y=rd.index, orientation="h", marker_color=[PAL[7] if k == "No reason given" else PAL[0] for k in rd.index],
                    text=[f"{v:+.2f}" for v in rd.values], textposition="outside",
                    hovertemplate="%{y}: %{x:+.3f} per 100 apps<extra></extra>", showlegend=False))
f4.update_layout(xaxis=dict(title="DiD, denials per 100 applications", range=[-0.4, 1.3]), height=460); bar_style(f4)

lede = ("FEMA registrations mark which counties a declared disaster hit. HMDA is the federal file where every mortgage lender reports "
        "each application, what happened to it, and how it was priced. A rate spread is the loan's APR minus the prime benchmark, reported only when it is 1.5+ points, so 'rate-spread share' is the share of loans that were higher-priced. HOEPA is the stricter federal flag for a high-cost loan. Question: after a 2016 hurricane or flood, did "
        "people in hit counties get worse mortgage terms than people in the rest of their state?")
sections = [
    ("Denials: a small, consistent gap", f"""
<p>Hit counties: denial rate {T[2015]['deny']:.1f}% in 2015, {T[2017]['deny']:.1f}% in 2017. Control: {C[2015]['deny']:.1f}% to {C[2017]['deny']:.1f}%.</p>
<p>Control improved 2.3 points; hit counties improved 1.2. Difference-in-differences: <b>+{did['deny']:.2f} points</b> more denial in hit counties.</p>
<p>County by county: {sign['beat']} of {sign['n']} hit counties with 200+ applications fell behind their state's control (median +{sign['med']:.1f} pts).</p>
<p>Robustness: count withdrawn and incomplete files in the denominator too and the gap is <b>{did['deny_wide']:+.2f}</b>; withdrawals rose less in hit counties (DiD {did['wd']:+.2f} pts of files).</p>
<p>Placebo: counties hit only in 2017, checked 2015 to 2016 when nothing had happened yet, show {placebo:+.2f}. Clean.</p>""", f1),
    ("Pricing: nothing", f"""
<p>Higher-priced (rate-spread) share: hit {T[2015]['rs']:.2f}% to {T[2017]['rs']:.2f}%, control {C[2015]['rs']:.2f}% to {C[2017]['rs']:.2f}%. DiD <b>{did['rs']:+.2f}</b> - if anything hit counties priced slightly better.</p>
<p>HOEPA, stated separately: {T[2015]['hoepa_n']} loans in hit counties in 2015, {T[2017]['hoepa_n']} in 2017; control {C[2015]['hoepa_n']} to {C[2017]['hoepa_n']}. DiD +{did['hoepa']:.1f} per 10,000 loans. Both roughly tripled - a nationwide 2017 jump (1,464 to 3,603 flagged loans across all states), not a disaster effect. Counts this small do not support a claim either way.</p>""", f2),
    ("Where the denial gap lives", f"""
<p>Positive in 10 of 13 states. Louisiana (49 counties, Aug 2016 flood) +{ps[ps.st=='LA'].deny.iloc[0]:.1f}; North Carolina (44, Hurricane Matthew) +{ps[ps.st=='NC'].deny.iloc[0]:.1f}; Texas (12) +{ps[ps.st=='TX'].deny.iloc[0]:.1f}.</p>
<p>Arkansas is one county with 99 applications; ignore the bar height.</p>
<p>Dose check: counties declared January to June 2016 (most of 2016 already 'after') read +{dose['early16']:.1f} in 2016 and +{dose['early17']:.1f} in 2017; July to December declarations read +{dose['late16']:.1f} then +{dose['late17']:.1f}. Earlier hit, bigger gap - the direction a real effect should run.</p>""", f3),
    ("What kind of denial", f"""
<p>Split the DiD by the reason the lender reported. Collateral (a damaged house appraising badly) is the obvious suspect. It reads {rdid['Collateral']:+.2f} - nothing. Credit history {rdid['Credit history']:+.2f}, debt-to-income {rdid['Debt-to-income']:+.2f}.</p>
<p>'No reason given' carries <b>{rdid['No reason given']:+.2f}</b> of the {did['deny']:.2f} total. Reporting a reason is optional for most lenders in this era, so this is either lenders declining to say why, or a shift in which lenders were writing loans in hit counties. The data cannot split those two.</p>""", f4),
]
footer = ("Sources: LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS (declarations 2016, county = padded FIPS) and "
          "HOUSING__FED_CFPB_HMDA_HISTORIC 2015-2017 (45M rows, aggregated by county-year in SQL). Cohort = counties hit in 2016 and not in 2015 or 2017; "
          "control = counties in the same 13 states with no 2015-2017 declaration. HMDA has no application date, so 'before' is calendar 2015 and 'after' is calendar 2017. "
          "Queries in queries.py, numbers in stats.json.")
hero = [(f"{did['deny']:+.1f} pts", "denial gap, hit vs control"), (f"{did['rs']:+.2f} pts", "higher-priced loan share gap"),
        (f"{sign['beat']}/{sign['n']}", "hit counties behind their state"), (f"{len(treat)}", "counties in the 2016 cohort")]
write_story(f"{HERE}/story.html", "After the flood, more 'no' - not more expensive", lede, sections, footer, hero)
print("story written")
