"""Build story.html from results.json. No warehouse calls."""
import json, html
import plotly.graph_objects as go
from _shared.viz import PAL, base_fig, bar_style, write_story, TEXT2
D = "reports/tier1_deep_dive_2026-09-05/E68_nonprofit_charity_care"
R = json.load(open(f"{D}/results.json"))
OWN = ["nonprofit", "for-profit", "government"]
COL = {"nonprofit": PAL[0], "for-profit": PAL[1], "government": PAL[2]}
pct = lambda x: f"{x*100:.2f}%"
m = lambda x: f"${x/1e6:,.0f}M"

# ---- chart 1: histogram of charity share by owner ----
bins = ["0-0.5%", "0.5-1%", "1-2%", "2-3%", "3-5%", "5-10%", "10%+"]
tot = {o: sum(r["N"] for r in R["hist_by_owner"] if r["OWNER"] == o) for o in OWN}
f1 = base_fig("Half of nonprofit hospitals give under 1.6% of costs as charity care; for-profits that report it give more",
              "Share of hospitals in each charity-care band, by owner. Charity care = HCRIS S-10 cost of charity care / total costs. One report per hospital.")
for o in OWN:
    ys = []
    for b in bins:
        n = next((r["N"] for r in R["hist_by_owner"] if r["OWNER"] == o and r["BIN"].endswith(b)), 0)
        ys.append(n / tot[o] * 100)
    f1.add_bar(name=f"{o} (n={tot[o]:,})", x=bins, y=ys, marker_color=COL[o],
               hovertemplate="%{x}: %{y:.1f}% of " + o + " hospitals<extra></extra>",
               text=[f"{v:.0f}%" for v in ys], textposition="outside", textfont=dict(size=11, color=TEXT2))
f1.update_layout(barmode="group", yaxis_title="% of hospitals", xaxis_title="charity care as % of total costs")
bar_style(f1)

# ---- chart 2: scatter, profitable nonprofits ----
irs = {r["PROVIDER_CCN"] for r in R["irs_tail"]}
tail = {r["PROVIDER_CCN"] for r in R["tail_nonprofit_list"]}
pts = [r for r in R["scatter_nonprofit"] if r["OWNER"] == "nonprofit" and r["NET_INCOME"] > 0]
def grp(r):
    if r["PROVIDER_CCN"] in irs: return "tail, IRS name-matched (37)"
    if r["PROVIDER_CCN"] in tail: return "tail, CMS code only (52)"
    return "other profitable nonprofits"
f2 = base_fig("89 nonprofit hospitals clear $50M profit with under 1% charity care; the IRS name-join identifies 37 of them",
              "Nonprofit-control hospitals with positive net income. x = net income (log). Shaded box = both bars.", height=560)
for g, c, sz in [("other profitable nonprofits", "#c9c8c4", 6), ("tail, CMS code only (52)", PAL[1], 9), ("tail, IRS name-matched (37)", PAL[0], 9)]:
    s = [r for r in pts if grp(r) == g]
    f2.add_scatter(name=g, mode="markers", x=[r["NET_INCOME"] for r in s], y=[r["CHARITY_SHARE"] * 100 for r in s],
                   marker=dict(color=c, size=sz, opacity=0.85), customdata=[[r["HOSPITAL_NAME"], r["STATE_CODE"]] for r in s],
                   hovertemplate="%{customdata[0]} (%{customdata[1]})<br>net income $%{x:,.0f}<br>charity %{y:.2f}%<extra></extra>")
f2.add_shape(type="rect", x0=50e6, x1=1.3e9, y0=0, y1=1, fillcolor="rgba(227,73,72,0.07)", line=dict(color=PAL[7], width=1, dash="dot"))
labels = {"050441": "Stanford", "050625": "Cedars-Sinai", "050138": "Kaiser LA", "220110": "Brigham", "180067": "UK Lexington", "030103": "Mayo Phoenix"}
for r in pts:
    if r["PROVIDER_CCN"] in labels:
        f2.add_annotation(x=__import__("math").log10(r["NET_INCOME"]), y=r["CHARITY_SHARE"] * 100, text=labels[r["PROVIDER_CCN"]],
                          showarrow=True, arrowhead=0, ax=0, ay=-22, font=dict(size=11))
f2.update_layout(xaxis=dict(type="log", title="net income, FY ending 2023-2024 (log)", tickvals=[1e6, 1e7, 5e7, 1e8, 1e9], ticktext=["$1M", "$10M", "$50M", "$100M", "$1B"]),
                 yaxis=dict(title="charity care as % of total costs", range=[0, 8]))

# ---- chart 3: median share by profit bucket ----
bk = ["loss", "$0-10M", "$10-50M", "$50-100M", "$100M+"]
f3 = base_fig("Richer nonprofits barely give more: 1.8% median at $100M+ vs 1.5% for loss-makers, a quarter of the richest for-profits' 6.5%",
              "Median charity care share by net-income tier and owner. For-profit and government tiers over $50M hold 27 to 65 hospitals each.")
for o in OWN:
    rows = sorted([r for r in R["bucket_by_owner"] if r["OWNER"] == o], key=lambda r: r["PROFIT_BUCKET"])
    f3.add_bar(name=o, x=bk, y=[r["P50_SHARE"] * 100 for r in rows], marker_color=COL[o],
               customdata=[[r["N"], r["N_UNDER_1PCT"]] for r in rows],
               hovertemplate="%{x} " + o + ": median %{y:.2f}%<br>n=%{customdata[0]}, under 1%: %{customdata[1]}<extra></extra>",
               text=[f"{r['P50_SHARE']*100:.1f}" for r in rows], textposition="outside", textfont=dict(size=11, color=TEXT2))
f3.update_layout(barmode="group", yaxis_title="median charity share, %", xaxis_title="net income tier")
bar_style(f3)

# ---- chart 4: the 37 ----
t = R["irs_tail"]
f4 = base_fig("The 37: Stanford ($1.05B, 0.45%) and Cedars-Sinai ($825M, 0.80%) lead; 11 of 37 sit under 0.6%",
              "IRS name-matched nonprofit hospitals over $50M net income and under 1% charity care, ranked by net income. Bar color darkens as charity share falls.", height=900)
sh = [r["CHARITY_SHARE"] * 100 for r in t]
f4.add_bar(orientation="h", y=[f"{r['HOSPITAL_NAME'].title()} ({r['STATE_CODE']})" for r in t][::-1], x=[r["NET_INCOME"] / 1e6 for r in t][::-1],
           marker=dict(color=sh[::-1], colorscale=[[0, "#0d366b"], [1, "#9ec5f4"]], cmin=0, cmax=1, showscale=True,
                       colorbar=dict(title="charity %", thickness=10, len=0.5)),
           customdata=[[r["CHARITY_SHARE"] * 100, r["COST_OF_CHARITY_CARE"] / 1e6, str(r["FISCAL_YEAR_END_DATE"]), r["EIN"]] for r in t][::-1],
           hovertemplate="%{y}<br>net income $%{x:,.0f}M<br>charity %{customdata[0]:.2f}% ($%{customdata[1]:,.1f}M)<br>FYE %{customdata[2]}, EIN %{customdata[3]}<extra></extra>",
           text=[f"${r['NET_INCOME']/1e6:,.0f}M · {r['CHARITY_SHARE']*100:.2f}%" for r in t][::-1], textposition="outside", textfont=dict(size=11))
f4.update_layout(xaxis_title="net income, $M", margin=dict(l=300, r=120), bargap=0.25, yaxis=dict(tickfont=dict(size=11)))
bar_style(f4)

# ---- prose ----
P = R["pct_by_owner"]; po = {r["OWNER"]: r for r in P}
np_, fp, gv = po["nonprofit"], po["for-profit"], po["government"]
tl = {r["GRP"]: r for r in R["tail_vs_all_uncomp"]}
sel = {(r["OWNER"], r["FILL"]): r for r in R["fp_fill_selection"]}
t37_ni = sum(r["NET_INCOME"] for r in t); t37_ch = sum(r["COST_OF_CHARITY_CARE"] for r in t)

lede = ("Every US hospital files a Medicare cost report (HCRIS) that lists its profit and, on Worksheet S-10, what charity care cost it. "
        "Nonprofit hospitals pay no income tax on the theory they give some of that back. This is one cost-report year, fiscal years ending "
        "Nov 2022 to Sep 2024, checked against one snapshot of the IRS exempt-organization master file (BMF). No trend is claimed.")
hero = [("37", "IRS name-matched nonprofits: $50M+ profit, <1% charity"), ("89", "same bars, nonprofit by CMS control code"),
        (pct(np_["P50"]), "median charity share, all 2,583 nonprofits"), (m(t37_ni), "combined net income of the 37")]
sections = [
 ("Where nonprofits sit", f"""
<p>2,583 nonprofit hospitals have a clean full-year report with readable profit, costs and charity care. Their median charity share is <b>{pct(np_['P50'])}</b> of total costs; a quarter give under {pct(np_['P25'])}; 808 (31%) give under 1%.</p>
<p>The 635 for-profits that report charity care sit higher: median <b>{pct(fp['P50'])}</b>, dollar-weighted {pct(fp['DOLLAR_WEIGHTED_SHARE'])} vs {pct(np_['DOLLAR_WEIGHTED_SHARE'])} for nonprofits. Government hospitals split: many tiny ones near zero, big ones high.</p>
<p><b>Read the for-profit bar with care.</b> Only 672 of 1,792 for-profit reports with readable total costs (37.5%) carry a readable charity number; the 1,120 that do not are small (median $20M costs, 54 beds). Nonprofits report it 88% of the time. The comparison is nonprofits vs the larger for-profits that bothered to fill S-10.</p>""", f1),
 ("The tail, two ways", f"""
<p>The first pass said 37. It reproduces exactly: my own name normalizer, city + state + NTEE E20-E22 against the BMF, 1,476 pairs, 1,047 hospitals, 866 nonprofit-control, and <b>37</b> clear both bars.</p>
<p>Drop the IRS leg and count by the cost report's own control code (1-2 = voluntary nonprofit): <b>89</b> clear both bars. The 52 the name-join misses are not marginal: nine Kaiser Foundation hospitals in California (0.11% to 0.28% charity, $62M to $206M profit each), Brigham and Women's ($128M, 0.64%), Hospital of the University of Pennsylvania ($317M, 0.93%), Mayo Clinic Phoenix ($268M, 0.70%), UK Lexington ($554M, 0.92%), four Advocate hospitals. They miss because the BMF lists the parent under another city or NTEE code, not because they are not exempt.</p>
<p>So 37 is a floor set by the join, not the count. And 89 is a floor too: divide by operating expense instead of total costs and 124 clear both bars. The 89 hold {m(tl['tail']['TOTAL_NI'])} of net income against {m(tl['tail']['TOTAL_CHARITY'])} of charity care, 0.68% dollar-weighted; median bad debt among them is also half the rest (2.7% vs 4.3%), so the wider uncompensated-care measure does not rescue them.</p>""", f2),
 ("Does profit buy charity?", f"""
<p>Barely. Among nonprofits the median share runs 1.5% (loss-makers), 1.4% ($0-10M), 1.8% ($10-50M), 2.0% ($50-100M), 1.8% ($100M+). The richest tier gives 21% more than the loss-makers, a third of a point. Of the 399 nonprofits over $50M profit, 89 (22%) give under 1% and 209 (52%) under 2%.</p>
<p>For-profits climb with profit: 6.5% median in the $100M+ tier (65 hospitals), 4.4% at $50-100M. Government hospitals over $100M give 3.6%. The richest nonprofit tier gives less than a third of what the richest for-profit tier gives, on the reports that exist.</p>
<p>What a hit means: the tax exemption is not buying charity care at the top. What a miss would have meant: if share rose with profit, the exemption would look earned. It does not rise.</p>""", f3),
 ("Name them", f"""
<p>All 37, with the EIN the name-join landed on. The normalizer strips HOSPITAL, MEDICAL, CENTER, HEALTH and SYSTEM before matching, so about 5 of 37 EINs land on a parent or physician group rather than the hospital. Two named: Cedars-Sinai matched CEDARS-SINAI HEALTH SYSTEM (the hospital's own EIN sits in the BMF under W HOLLYWOOD), and The Queen's Medical Center matched QUEENS UNIVERSITY MEDICAL GROUP (its own EIN is NTEE E60). Corewell Grand Rapids pulled 37 EINs, Carilion 7; the join is a system-level match there.</p>
<p>Combined: {m(t37_ni)} net income, {m(t37_ch)} charity care, {pct(t37_ch/sum(r['TOTAL_COSTS'] for r in t))} of their costs. Fiscal years end between Sep 2023 and Aug 2024; 15 of 37 end in 2024.</p>""", f4),
]
foot = ("Sources: LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS (6,103 reports, 6,040 hospitals; one report per hospital, latest fiscal year end) and "
        "LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF (1,983,563 rows, NTEE E20-E22 filtered). Clean = net income, total costs and charity care all parse "
        "(the mart stores NaN, not null: 1,869 reports have no charity number), total costs > 0, net income <= total costs (31 broken rows, Holy Family Memorial WI among them), "
        "fiscal year 350-380 days. Charity share = COST_OF_CHARITY_CARE / TOTAL_COSTS. Every query in queries.py, logged in queries.log.")
write_story(f"{D}/story.html", "Fat margins, thin charity care", lede, sections, foot, hero)
print("ok")
