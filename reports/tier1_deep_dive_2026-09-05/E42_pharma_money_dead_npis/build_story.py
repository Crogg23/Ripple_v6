"""Build story.html from results.json / results2.json. No warehouse calls."""
import json, datetime as dt
import plotly.graph_objects as go
from _shared.viz import PAL, TEXT2, base_fig, bar_style, write_story
D = "reports/tier1_deep_dive_2026-09-05/E42_pharma_money_dead_npis"
R = json.load(open(f"{D}/results.json")); R2 = json.load(open(f"{D}/results2.json"))
q1 = R["q1_rebuild"][0]; top = R["q2_top"][:10]
top_ids = [r["NPI"] for r in top]
top_tot = sum(r["TOT"] for r in top)
money = lambda x: f"${x:,.0f}"

# ---- chart 1: top 10 stacked by nature
def nat(s):
    if s.startswith("Royalty"): return "Royalty or license"
    if s.startswith("Food"): return "Food and beverage"
    if s.startswith("Acquisitions"): return "Practice acquisition"
    return "Speaking or consulting"
names = {r["NPI"]: f"{r['LN'].title()} ({r['ST']}, {r['SPEC'].split('|')[-1]})" for r in top}
cats = ["Royalty or license", "Speaking or consulting", "Practice acquisition", "Food and beverage"]
agg = {}
for r in R["q5_top_detail"]:
    agg.setdefault(nat(r["NATURE"]), {}).setdefault(r["NPI"], 0.0); agg[nat(r["NATURE"])][r["NPI"]] += r["DOLLARS"]
order = top_ids[::-1]
f1 = base_fig("94% of the $4.19M is ten NPIs, and eight of the ten are device royalties",
              "Open Payments PY2024 dollars dated after the NPI's NPPES deactivation, top 10 recipients, by nature of payment", height=520)
for i, c in enumerate(cats):
    ys = [names[n] for n in order]; xs = [agg.get(c, {}).get(n, 0) for n in order]
    f1.add_bar(y=ys, x=xs, name=c, orientation="h", marker_color=PAL[i],
               hovertemplate="%{y}<br>" + c + ": $%{x:,.0f}<extra></extra>")
for n in order:
    r = next(t for t in top if t["NPI"] == n)
    f1.add_annotation(x=r["TOT"], y=names[n], text=f" {money(r['TOT'])} · {r['DAYS_TO_FIRST']//365}y after", showarrow=False, xanchor="left", font=dict(size=12, color=TEXT2))
f1.update_layout(barmode="stack", xaxis=dict(title="PY2024 dollars after deactivation", tickprefix="$", tickformat=",.0f", range=[0, 2.35e6]), yaxis=dict(title=""), margin=dict(l=300))
bar_style(f1)

# ---- chart 2: timeline per person
f2 = base_fig("The money did not start after deactivation. It never stopped.",
              "Each row is one of the ten. Red diamond = NPPES deactivation date. Dots = every Open Payments transfer, PY2022 to PY2024.", height=520)
ys = [names[n] for n in top_ids[::-1]]
f2.add_scatter(x=[next(t for t in top if t["NPI"] == n)["DEACT"] for n in top_ids[::-1]], y=ys, mode="markers", name="NPI deactivated (NPPES)",
               marker=dict(symbol="diamond", size=13, color=PAL[7]), hovertemplate="%{y}<br>deactivated %{x}<extra></extra>")
prior = {}
for r in R["q7_prior"]:
    prior.setdefault(r["NPI"], []).append(r)
px, py, pt = [], [], []
for n in top_ids:
    for r in prior.get(n, []):
        for d in (r["FIRST_PD"], r["LAST_PD"]):
            px.append(d); py.append(names[n]); pt.append(f"PY{r['PY']}: {r['PAYMENTS']} transfers, {money(r['DOLLARS'])}")
f2.add_scatter(x=px, y=py, mode="markers", name="PY2022-23 transfers (first and last of the year)", marker=dict(size=8, color=PAL[3]),
               text=pt, hovertemplate="%{y}<br>%{x}<br>%{text}<extra></extra>")
mx, my, mt = [], [], []
for r in R["q12_top_timeline"]:
    mx.append(r["M"]); my.append(names[r["NPI"]]); mt.append(f"{r['N']} transfer(s), {money(r['DOLLARS'])}")
f2.add_scatter(x=mx, y=my, mode="markers", name="PY2024 transfers after deactivation (by month)", marker=dict(size=9, color=PAL[0]),
               text=mt, hovertemplate="%{y}<br>%{x|%b %Y}<br>%{text}<extra></extra>")
f2.update_layout(xaxis=dict(title="", range=["2013-06-01", "2025-03-01"], showgrid=True, gridcolor="#e6e5e1"), yaxis=dict(title=""), margin=dict(l=300), legend=dict(y=-0.12))

# ---- chart 3: the long tail
lab = {"a <$25": "under $25", "b $25-100": "$25 to $100", "c $100-1k": "$100 to $1k", "d $1k-10k": "$1k to $10k", "e $10k-100k": "$10k to $100k", "f $100k+": "$100k and up"}
d3 = R["q3_dist"]; tn = sum(r["NPIS"] for r in d3); td = sum(r["DOLLARS"] for r in d3)
f3 = base_fig("1,078 of the 1,325 NPIs got under $100. Five got 86% of the money.",
              "Per-NPI total of PY2024 dollars after deactivation, bucketed. Share of NPIs vs share of dollars.")
f3.add_bar(x=[lab[r["BUCKET"]] for r in d3], y=[100 * r["NPIS"] / tn for r in d3], name="share of NPIs", marker_color=PAL[0],
           text=[f"{r['NPIS']:,}" for r in d3], textposition="outside", hovertemplate="%{x}<br>%{text} NPIs, %{y:.1f}% of NPIs<extra></extra>")
f3.add_bar(x=[lab[r["BUCKET"]] for r in d3], y=[100 * r["DOLLARS"] / td for r in d3], name="share of dollars", marker_color=PAL[1],
           text=[money(r["DOLLARS"]) for r in d3], textposition="outside", hovertemplate="%{x}<br>%{text}, %{y:.1f}% of dollars<extra></extra>")
f3.update_layout(barmode="group", yaxis=dict(title="percent", ticksuffix="%", range=[0, 100]), xaxis=dict(title="what the NPI received in PY2024 after deactivation"))
bar_style(f3)

# ---- chart 4: years since deactivation
g = R["q11_gap"]
f4 = base_fig("370 NPIs were paid within a year of deactivation. 116 were paid ten or more years after.",
              "1,325 NPIs by whole years between NPPES deactivation and their first PY2024 transfer. Hover for the dollars in each year.")
f4.add_bar(x=[("10+" if r["YRS"] >= 10 else str(int(r["YRS"]))) for r in g], y=[r["NPIS"] for r in g], name="NPIs", marker_color=PAL[0],
           text=[f"{r['NPIS']}" for r in g], textposition="outside",
           customdata=[money(r["DOLLARS"]) for r in g], hovertemplate="%{x} years after<br>%{y} NPIs<br>%{customdata} after-deactivation dollars<extra></extra>")
f4.update_layout(xaxis=dict(title="years from deactivation to first PY2024 transfer"), yaxis=dict(title="NPIs"), showlegend=False)
bar_style(f4)

# ---- prose
lede = ("The Open Payments file is where drug and device makers report every dollar they hand a doctor. NPPES is the federal registry that "
        "issues each provider a ten-digit National Provider Identifier (NPI) and records the day it is switched off. "
        "The first pass found $4.19M of PY2024 industry money booked to NPIs that NPPES had already deactivated. "
        "This pass rebuilt the number a second way, then took the ten people who hold 94% of it apart: when they were deactivated, "
        "how long after that the money arrived, what the money was for, and whether the NPI ever came back.")
hero = [(money(q1["DOLLARS_AFTER"]), "PY2024 dollars dated after deactivation"), (f"{q1['NPIS_PAID_AFTER']:,}", "deactivated NPIs paid after the date"),
        (f"{100*top_tot/q1['DOLLARS_AFTER']:.0f}%", "of the money to ten NPIs"), ("0 of 10", "reactivated, replaced, excluded or billing Part B")]
p1 = (f"<p>Rebuilt by rolling payments up per NPI per day before touching NPPES, the first pass reproduces to the cent: "
      f"{q1['NPIS_PAID_AFTER']:,} NPIs, {money(q1['DOLLARS_AFTER'])}, {q1['NPIS_PAID_90PLUS']:,} of them paid 90 or more days after deactivation.</p>"
      f"<p>The ten at the top hold {money(top_tot)}. Eight of them are pure royalty streams from device makers (Stryker three times, DePuy Synthes, Medtronic, Globus, Alphatec, KLS-Martin, Cook) to surgeons and a podiatrist. "
      f"A royalty is passive income on a patented implant; it keeps paying whether or not the surgeon still operates.</p>"
      f"<p>The one that is not a royalty is Geller, an optometrist, deactivated February 2023, paid $451,125 for speaking and $87,000 for consulting by Johnson &amp; Johnson Vision Care through November 2024. "
      f"Speaking and consulting are services performed, not passive income. Reddy is the ninth: a $50,000 practice buy-out from US Retina on top of $12,786 of Bausch &amp; Lomb royalty.</p>")
p2 = (f"<p>Every one of the ten was also paid in PY2023 or PY2022 by the same companies. Spetzler's Stryker royalty ran $1.97M in 2022, $1.80M in 2023, $1.79M in 2024, all after a November 2018 deactivation. "
      f"Fenlin's NPI was deactivated in June 2014; Stryker paid him $1.15M, $712k and $537k in the three years on file.</p>"
      f"<p>Gap from deactivation to the first 2024 dollar runs from 84 days (Ruiz, KLS-Martin royalty) to 3,520 days (Fenlin). Eight of the ten were deactivated more than a year before any 2024 payment; six more than four years before.</p>"
      f"<p>Reactivation: none. NPI_REACTIVATION_DATE is null on all ten, REPLACEMENT_NPI is blank on all ten, and a live type-1 NPI with the same first name, last name and state exists for only two of them, in the wrong specialties (Morrison: a dentist; Goldstein: a gastroenterologist, an obstetrician and a paediatric dentist). "
      f"Deactivation reason: NPPES publishes none, on these ten or on any of the 346,179 deactivated rows. None of the ten is on the OIG exclusion list or the SAM exclusion list, and none billed Medicare Part B in 2024.</p>")
p3 = (f"<p>Below the ten, the number is a different story. 584 NPIs got under $25, 494 got $25 to $100. Between them that is 1,078 NPIs and {money(10952.70+24019.58)}.</p>"
      f"<p>That tail is 2,503 food-and-beverage transfers to 1,246 NPIs, {money(82210.81)} in total, the sales-rep lunch. It is where the drug companies sit; the device makers own the head.</p>"
      f"<p>The median NPI in the whole 1,325 got $28. The five over $100k got {money(3587607.61)}, 86% of everything.</p>")
p4 = (f"<p>370 NPIs were paid inside the first year after deactivation, most of them lunches booked in the months around a retirement or a move. "
      f"The money is not there: year 0 holds {money(162858.76)}. Years 4, 5 and 9 hold {money(809214.58+1801832.58+585713.60)} between them, which is Mast, Morrison, Spetzler, Fenlin and Goldstein.</p>"
      f"<p>116 NPIs were paid ten or more years after deactivation, for {money(9190.48)}. A decade-dead NPI still gets a $79 lunch on average. That is the recipient-matching in Open Payments never being refreshed against NPPES, not a person.</p>"
      f"<p>The reactivated cohort is a separate, small check: 35 NPIs took 65 transfers worth {money(14666.30)} inside a deactivation window that later closed. Median window 25 days. Nothing there.</p>")
footer = ("Sources: LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS (PY2024, 15,385,047 rows), _2023, _2022; HEALTH__FED_CMS_NPPES (9,606,683 rows, snapshot to 2026-06-07); "
          "HEALTH__FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT; HEALTH__FED_HHS_OIG_LEIE; PROCUREMENT__FED_SAM_EXCLUSIONS; HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER. "
          "Test: payment date strictly after NPI_DEACTIVATION_DATE, NPI_REACTIVATION_DATE null. Queries in <code>queries.py</code>, <code>queries2.py</code>, log in <code>queries.log</code>. Built 2026-09-05.")
write_story(f"{D}/story.html", "Industry money to switched-off NPIs", lede,
            [("Ten NPIs: eight royalties, one acquisition, one speaker", p1, f1), ("Deactivation date against payment date", p2, f2),
             ("The tail is lunches", p3, f3), ("How long after", p4, f4)], footer, hero)
print("story written", top_tot)
