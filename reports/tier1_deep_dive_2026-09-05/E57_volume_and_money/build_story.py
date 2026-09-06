"""Build story.html for E57 from results.json. No warehouse calls."""
import json
from pathlib import Path
import plotly.graph_objects as go
from _shared.viz import PAL, TEXT2, base_fig, bar_style, write_story
HERE = Path(__file__).resolve().parent
R = json.load(open(HERE / "results.json"))
f = lambda x: float(x or 0)
M = lambda x: f"${f(x)/1e6:,.1f}M"

H = R["headline_ntile"][0]
top = int(H["TOP_BILLERS"]); both = int(H["BOTH_TOP_REAL_MONEY"]); peers = int(H["PEERS"])
rate = 100*both/top; peer_real = 100*int(R["bucket_split"][5]["PEOPLE"])/peers
B = {r["COHORT"]: r for r in R["bucket_split"]}
bt = B["both-top"]; roy_share = 100*f(bt["ROYALTY"])/f(bt["USD"]); svc_share = 100*f(bt["SERVICES"])/f(bt["USD"])

# --- chart 1: gradient by billing decile
D = R["by_bill_decile"]
fig1 = base_fig("Industry money climbs with every step up the billing ladder",
                "Share of each Part B billing decile (within specialty) that sits in the top industry-money decile, PY2024")
x = [f"D{r['BILL_DEC']}" for r in D]; y = [f(r["TOP_MONEY_PCT"]) for r in D]
fig1.add_trace(go.Bar(x=x, y=y, marker_color=[PAL[0]]*9 + [PAL[7]], text=[f"{v:.1f}%" if i in (0, 4, 9) else "" for i, v in enumerate(y)],
                      textposition="outside", hovertemplate="%{x}: %{y:.2f}% in top money decile<extra></extra>", name="top money decile"))
fig1.update_layout(yaxis_title="% in top money decile", xaxis_title="Part B allowed-charge decile (1 = lowest, 10 = highest)", showlegend=False)
bar_style(fig1)

# --- chart 2: what kind of money, by cohort (100% stacked)
cohorts = ["all OP NPIs", "lower-decile billers", "top-decile billers", "both-top"]
labels = {"all OP NPIs": "Every NPI in Open Payments", "lower-decile billers": "Part B billers, deciles 1-9",
          "top-decile billers": "Part B top-decile billers", "both-top": "Both-top (top biller AND top payee)"}
fig2 = base_fig("Royalties are a fifth of both-top money; consulting and speaking are half",
                "Share of PY2024 general-payment dollars by kind, per cohort. Research payments are not in the warehouse.")
for i, (k, nm) in enumerate([("ROYALTY", "Royalty or license"), ("SERVICES", "Consulting, speaking, honoraria"),
                             ("HOSPITALITY", "Food, travel, education, gifts"), ("OTHER", "Other (acquisitions, grants, debt forgiveness)")]):
    vals = [100*f(B[c][k])/f(B[c]["USD"]) for c in cohorts]
    fig2.add_trace(go.Bar(y=[labels[c] for c in cohorts], x=vals, orientation="h", name=nm, marker_color=PAL[i],
                          text=[f"{v:.0f}%" if (v >= 8 or k == "OTHER") else "" for v in vals], textposition="inside" if k != "OTHER" else "outside",
                          customdata=[M(B[c][k]) for c in cohorts], hovertemplate="%{y}<br>" + nm + ": %{x:.1f}% (%{customdata})<extra></extra>"))
fig2.update_layout(barmode="stack", xaxis_title="% of cohort dollars", height=420, margin=dict(l=260))
bar_style(fig2)

# --- chart 3: by specialty, overlap rate vs peer rate, bubble = both-top dollars
S = sorted([r for r in R["by_specialty"] if int(r["TOP_BILLERS"]) >= 200], key=lambda r: -int(r["BOTH_TOP"]))[:20]
S = sorted(S, key=lambda r: f(r["RATE_PCT"]))
fig3 = base_fig("Anesthesiology, PAs and internists overlap most; orthopedics holds the money",
                "Top 20 by both-top headcount of the 53 specialties with 200+ top-decile billers. Bar = % of top billers who are also top payees; dot = their lower-decile Medicare-billing peers.")
fig3.add_trace(go.Bar(y=[r["SPEC"] for r in S], x=[f(r["RATE_PCT"]) for r in S], orientation="h", name="top-decile billers", marker_color=PAL[0],
                      customdata=[[int(r["BOTH_TOP"]), M(r["BOTH_USD"]), 100*f(r["BOTH_ROYALTY"])/max(f(r["BOTH_USD"]), 1)] for r in S],
                      hovertemplate="%{y}<br>%{x:.1f}% of top billers are top payees<br>%{customdata[0]:,} people, %{customdata[1]} industry money, %{customdata[2]:.0f}% royalty<extra></extra>"))
fig3.add_trace(go.Scatter(y=[r["SPEC"] for r in S], x=[f(r["PEER_PCT"]) for r in S], mode="markers", name="lower-decile peers",
                          marker=dict(color=PAL[1], size=10), hovertemplate="%{y}<br>peers: %{x:.1f}%<extra></extra>"))
fig3.update_layout(xaxis_title="% in top industry-money decile", height=640, margin=dict(l=250), legend=dict(y=-0.1))
bar_style(fig3)

# --- chart 4: the named ten by industry money, stacked by kind
T = R["top10_money"][::-1]
fig4 = base_fig("The ten both-top clinicians industry paid most: nine surgeons on device royalties, one write-off",
                "Both-top cohort, PY2024 general payments. Debt forgiveness is a bad-debt write-off, not a cheque.")
names = [f"{r['FIRST_NAME']} {r['LAST_NAME']} ({r['SPEC'].replace('Orthopedic Surgery','Ortho')}, {r['ST']})" for r in T]
for i, (k, nm) in enumerate([("ROYALTY", "Royalty or license"), ("SERVICES", "Consulting, speaking"), ("HOSPITALITY", "Food, travel, education"), ("OTHER", "Other / debt forgiveness")]):
    fig4.add_trace(go.Bar(y=names, x=[f(r[k])/1e6 for r in T], orientation="h", name=nm, marker_color=PAL[i],
                          hovertemplate="%{y}<br>" + nm + ": $%{x:.2f}M<extra></extra>"))
fig4.update_layout(barmode="stack", xaxis_title="PY2024 industry money, $M", height=520, margin=dict(l=300))
bar_style(fig4)

conc = R["concentration"][0]
lede = (f"Part B is the Medicare program that pays clinicians for office visits, procedures and office-given drugs; Open Payments is the federal "
        f"register of what drug and device companies give clinicians. Rank every clinician inside their own specialty on both. "
        f"<b>{rate:.1f}%</b> of the top-decile billers are also top-decile industry payees; their lower-billing peers sit at <b>{peer_real:.1f}%</b>. "
        f"The overlap is real and it is not a royalty story: royalties are <b>{roy_share:.0f}%</b> of both-top money overall, {100*f([r for r in R['by_specialty'] if r['SPEC']=='Orthopedic Surgery'][0]['BOTH_ROYALTY'])/f([r for r in R['by_specialty'] if r['SPEC']=='Orthopedic Surgery'][0]['BOTH_USD']):.0f}% in orthopedics alone.")
hero = [(f"{rate:.1f}%", "of top billers are also top payees"), (f"{peer_real:.1f}%", "of their lower-billing peers"),
        (f"{both:,}", "both-top clinicians"), (M(bt["USD"]), "their PY2024 industry money"), (f"{roy_share:.0f}%", "of it is royalty")]

sec1 = (f"<p>1,235,757 individual clinicians in Part B DY2024, each given a decile for Medicare allowed charges and a decile for PY2024 industry money, "
        f"both inside their own specialty so a dermatologist is ranked against dermatologists. Decile 10 is the top.</p>"
        f"<p>The rise is monotonic: {y[0]:.1f}% at the bottom, {y[4]:.1f}% in the middle, {y[9]:.1f}% at the top. Any-money share climbs too, "
        f"{f(D[0]['ANY_MONEY_PCT']):.0f}% to {f(D[9]['ANY_MONEY_PCT']):.0f}%.</p>"
        f"<p>Take royalties out of the money measure entirely and the both-top count moves from {both:,} to {int(R['headline_no_royalty'][0]['BOTH_TOP']):,}. "
        f"Strip drug cost out of the billing measure and it is {int(R['headline_med_only'][0]['BOTH_TOP']):,}. The gradient survives both.</p>")
sec2 = (f"<p>Only general payments are in the warehouse. CMS publishes research payments and ownership interest as separate files; neither is landed, so 'research' is zero by absence, not by measurement.</p>"
        f"<p>Both-top money is {M(bt['USD'])}: {M(bt['SERVICES'])} consulting and speaking ({svc_share:.0f}%), {M(bt['HOSPITALITY'])} hospitality, "
        f"{M(bt['ROYALTY'])} royalty ({roy_share:.0f}%) to just {int(bt['ROYALTY_PEOPLE'])} people, {M(bt['OTHER'])} other.</p>"
        f"<p>The first pass reported 79% royalty. That number does not reproduce on this table and its method is not recorded. Across all specialties the royalty share is barely above the file-wide {100*f(B['all OP NPIs']['ROYALTY'])/f(B['all OP NPIs']['USD']):.0f}% for clinician-level dollars.</p>"
        f"<p>Skew: median both-top clinician got ${f(conc['MEDIAN_USD']):,.0f}; the top 100 hold {M(conc['TOP100'])}, the top 1,000 hold {M(conc['TOP1000'])} ({100*f(conc['TOP1000'])/f(conc['TOT']):.0f}%).</p>")
o = [r for r in R["by_specialty"] if r["SPEC"] == "Orthopedic Surgery"][0]
a = [r for r in R["by_specialty"] if r["SPEC"] == "Anesthesiology"][0]
sec3 = (f"<p>53 specialties have 200+ top billers. 45 show top billers ahead of peers. Seven are therapy and counseling fields where nobody gets paid (0.0% both sides). The one real reversal is Medical Oncology: 8.2% vs 10.2%, because its top billers are ranked on drug cost they pass through, not on anything a company courts. Widest: Anesthesiology {f(a['RATE_PCT']):.1f}% vs {f(a['PEER_PCT']):.1f}%, "
        f"{int(a['BOTH_TOP']):,} people but only {M(a['BOTH_USD'])}. Narrowest: Diagnostic Radiology 10.8% vs 9.9%.</p>"
        f"<p>Orthopedic Surgery is where the money is: {int(o['BOTH_TOP'])} both-top surgeons hold {M(o['BOTH_USD'])}, "
        f"{100*f(o['BOTH_ROYALTY'])/f(o['BOTH_USD']):.0f}% royalty. Neurosurgery is the only other specialty with a real royalty share ({100*f([r for r in R['by_specialty'] if r['SPEC']=='Neurosurgery'][0]['BOTH_ROYALTY'])/f([r for r in R['by_specialty'] if r['SPEC']=='Neurosurgery'][0]['BOTH_USD']):.0f}%).</p>"
        f"<p>Physician Assistants and Nurse Practitioners are the biggest groups by headcount (3,169 and 3,120) and their money is almost all consulting, speaking and meals.</p>")
sec4 = (f"<p>Each NPI is one Open Payments profile and one Part B row; no name collisions. Nine of the ten are surgeons paid royalties by one device maker each "
        f"(Encore Medical, Arthrex, Zimmer Biomet, DePuy Synthes, Medtronic). Mark Frankle, FL: $6.95M royalty from Encore Medical on $370,724 of Medicare billing.</p>"
        f"<p>Alexander Frank, OK, $3.08M, is a Skye Orthobiologics debt write-off already worked in reports/molina_debt_forgiveness_2026-09-05.md, not a payment. "
        f"Gary Gelbfish, NY, $1.93M, is a Stryker acquisition of his company.</p>"
        f"<p>Ranked the other way, by Medicare billing, the both-top list is drug buy-and-bill: Ravi Kapadia, CA, $97.1M allowed, 99.7% drug, $29,753 industry money, top payer Organogenesis (skin substitutes, hunch E40). "
        f"Both-top clinicians run 39.8% drug in their allowed charges against 10.2% for everyone else.</p>")

footer = ("Part B: LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER, 1,235,757 individuals (ENT_CD='I'), DY2024, one snapshot. "
          "Open Payments: LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS, PY2024 general payments, 15,385,047 rows, 48,059 blank NPIs dropped, $3.31B total, $2.64B to NPIs. "
          "Dropping blank-NPI rows removes $361.2M of royalty, 43% of all royalty dollars in the file, more than any other nature; every royalty share here is clinician-level only. Deciles: ntile(10) within RNDRNG_PRVDR_TYPE; top payee requires money > 0 (15,902 zero-dollar clinicians would otherwise land in the top money decile). "
          "Queries in queries.py, log in queries.log. Built 2026-09-05.")

write_story(HERE / "story.html", "Top billers, top payees", lede,
            [("The gradient", sec1, fig1), ("What kind of money", sec2, fig2), ("By specialty", sec3, fig3), ("The named ten", sec4, fig4)],
            footer, hero)
print("wrote", HERE / "story.html")
