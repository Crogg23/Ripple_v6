"""Build story.html from results.json. No warehouse calls."""
import json
import plotly.graph_objects as go
from _shared.viz import PAL, base_fig, bar_style, write_story
D = "reports/tier1_deep_dive_2026-09-05/E38_optout_doctors_paid/"
R = json.load(open(D + "results.json"))
M = lambda x: f"${x/1e6:,.1f}M"
YRS = [2022, 2023, 2024]

# --- chart 1: fixed cohort by year, stacked by kind of money
def bucket(n):
    if n.startswith("Royalty"): return "Royalties & licenses"
    if n == "Acquisitions": return "Acquisitions (buying their company/IP)"
    if n.startswith("Compensation") or n in ("Consulting Fee", "Honoraria"): return "Speaking, consulting, honoraria"
    return "Meals, travel, gifts, education, other"
order = ["Royalties & licenses", "Acquisitions (buying their company/IP)", "Speaking, consulting, honoraria", "Meals, travel, gifts, education, other"]
agg = {b: {y: 0.0 for y in YRS} for b in order}
for r in R["nature"]: agg[bucket(r["NATURE"])][int(r["PY"])] += r["USD"]
tot = {y: sum(agg[b][y] for b in order) for y in YRS}
f1 = base_fig("Money to the fixed cohort fell 13% on recurring money, 33% counting a one-time 2022 buyout",
              "27,547 clinicians who opted out of Medicare before 2023 - the same people in every bar. Open Payments PY2022-PY2024.", height=500)
for i, b in enumerate(order):
    f1.add_bar(name=b, x=[str(y) for y in YRS], y=[agg[b][y] for y in YRS], marker_color=PAL[i],
               hovertemplate=f"{b}<br>PY%{{x}}: $%{{y:,.0f}}<extra></extra>")
for y in YRS:
    f1.add_annotation(x=str(y), y=tot[y], text=f"<b>{M(tot[y])}</b>", showarrow=False, yshift=14)
f1.update_layout(barmode="stack", yaxis=dict(tickprefix="$", tickformat="~s", title=None), xaxis_title=None, legend=dict(y=-0.12))
bar_style(f1)

# --- chart 2: top 10 payers, royalty vs everything else
P = R["payers_norm"][:10]
nice = {"ABBVIE INC": "AbbVie", "ARTHREX INC": "Arthrex", "SMITHNEPHEW INC": "Smith+Nephew", "DEPUY SYNTHES PRODUCTS INC": "DePuy Synthes (J&J)",
        "STRYKER CORPORATION": "Stryker", "ZIMMER BIOMET HOLDINGS INC": "Zimmer Biomet", "MEDTRONIC INC": "Medtronic", "ZIMVIE INC": "ZimVie",
        "MERIT MEDICAL SYSTEMS INC": "Merit Medical", "AXSOME THERAPEUTICS INC": "Axsome", "OTSUKA AMERICA PHARMACEUTICAL INC": "Otsuka", "STRAUMANN USA LLC": "Straumann"}
names = [nice.get(p["PAYER"], p["PAYER"].title()) for p in P][::-1]
roy = [p["USD_ROYALTY"] for p in P][::-1]; oth = [p["USD"] - p["USD_ROYALTY"] for p in P][::-1]
npis = [p["NPIS"] for p in P][::-1]
f2 = base_fig("Seven of the ten biggest payers are orthopedic and device makers paying royalties to a handful of surgeons",
              "Top 10 payers to the fixed cohort, PY2022-2024 pooled. Payer names case-folded (AbbVie was two spellings).", height=520)
f2.add_bar(name="Royalties & licenses", y=names, x=roy, orientation="h", marker_color=PAL[0],
           customdata=npis, hovertemplate="%{y}<br>royalties: $%{x:,.0f}<br>practitioners paid (all kinds): %{customdata:,}<extra></extra>")
f2.add_bar(name="Everything else", y=names, x=oth, orientation="h", marker_color=PAL[3],
           customdata=npis, hovertemplate="%{y}<br>non-royalty: $%{x:,.0f}<br>practitioners paid (all kinds): %{customdata:,}<extra></extra>")
for n, a, b, k in zip(names, roy, oth, npis):
    f2.add_annotation(y=n, x=a + b, text=f"{M(a+b)} · {k:,} people", showarrow=False, xanchor="left", xshift=6, font=dict(size=12))
f2.update_layout(barmode="stack", xaxis=dict(tickprefix="$", tickformat="~s", range=[0, 66e6]), margin=dict(l=150), legend=dict(y=-0.1))
bar_style(f2)

# --- chart 3: specialty - dollars vs headcount
S = [s for s in R["specialty"] if s["USD"]][:8]
sn = [s["SPECIALTY"].replace("Plastic And Reconstructive Surgery", "Plastic surgery").replace("Cardiovascular Disease (Cardiology)", "Cardiology") for s in S][::-1]
su = [s["USD"] for s in S][::-1]; sc = [s["COHORT"] for s in S][::-1]; sp = [s["PAID_NPIS"] for s in S][::-1]
f3 = base_fig("242 orthopedic surgeons take $101M; 7,830 therapists in the same cohort take almost nothing",
              "Industry money PY2022-2024 by the specialty on the opt-out affidavit, fixed cohort. Label = cohort size and share paid at least once.", height=500)
f3.add_bar(y=sn, x=su, orientation="h", marker_color=[PAL[7] if n in ("Orthopedic Surgery", "Plastic surgery") else PAL[0] for n in sn],
           customdata=list(zip(sc, sp)), hovertemplate="%{y}<br>$%{x:,.0f}<br>in cohort: %{customdata[0]:,}<br>paid at least once: %{customdata[1]:,}<extra></extra>", showlegend=False)
for n, u, c, p in zip(sn, su, sc, sp):
    f3.add_annotation(y=n, x=u, text=f"{M(u)} · {c:,} in cohort, {p/c:.0%} paid", showarrow=False, xanchor="left", xshift=6, font=dict(size=12))
f3.update_layout(xaxis=dict(tickprefix="$", tickformat="~s", range=[0, 135e6]), margin=dict(l=150))
bar_style(f3)

# --- chart 4: concentration
C = R["concentration"][0]
T = R["top_npis"]
lab = ["Top 1 (TN plastic surgeon)", "Next 9", "Rank 11-100", "Other 11,163 paid"]
v = [T[0]["USD"], C["TOP10"] - T[0]["USD"], C["TOP100"] - C["TOP10"], C["TOT"] - C["TOP100"]]
f4 = base_fig("One plastic surgeon is 19% of the whole three-year total; the median paid opt-out doctor got $251",
              f"{C['PAID_NPIS']:,} cohort members received anything PY2022-2024; {M(C['TOT'])} in all.", height=380)
f4.add_bar(x=v, y=[""] * 4, orientation="h", marker_color=[PAL[7], PAL[1], PAL[3], PAL[0]], text=[f"{x/C['TOT']:.0%}" for x in v],
           textposition="inside", customdata=lab, hovertemplate="%{customdata}: $%{x:,.0f}<extra></extra>", showlegend=False)
for i, (l, x) in enumerate(zip(lab, v)):
    f4.add_trace(go.Bar(name=l, x=[0], y=[""], marker_color=[PAL[7], PAL[1], PAL[3], PAL[0]][i], orientation="h", hoverinfo="skip"))
f4.update_layout(barmode="stack", xaxis=dict(tickprefix="$", tickformat="~s"), yaxis=dict(showticklabels=False), legend=dict(y=-0.4))
bar_style(f4)

fp = R["fp_variants"][0]; fx = {int(r["PY"]): r for r in [R[f"fixed_py{y}"][0] for y in YRS]}
lede = ("An NPI is the ten-digit National Provider Identifier every U.S. clinician carries. Medicare 'opt-out' means a clinician filed an affidavit saying they will not bill Medicare at all, "
        "and patients pay them privately. Open Payments is the federal ledger where drug and device companies must report every dollar, meal and royalty they give a clinician. "
        "The first pass said $70.8M reached opted-out clinicians in 2023. That number reproduces exactly. What it hides: the money is falling, it is royalties to a few dozen surgeons, "
        "and the typical opted-out doctor gets a sandwich.")
hero = [(M(sum(tot.values())), "to the fixed cohort, PY2022-24"), ("27,547", "clinicians opted out before 2023 (fixed cohort)"), ("53%", "of it went to 10 people"),
        (f"{M(tot[2022])} → {M(tot[2024])}", "PY2022 to PY2024, same people")]
sections = [
    ("Fix the people, then watch the money", f"""
<p>The roster of opt-outs grows every year (15,966 new affidavits in 2024 alone, mostly therapists newly allowed into Medicare). Counting 'anyone on the roster' each year mixes roster growth with real change. So the cohort is frozen: the 27,547 clinicians whose opt-out took effect before 2023-01-01. (2,389 of them opted out during 2022, so $1.6M of the PY2022 bar predates the person's own opt-out; PY2023 and PY2024 are clean.)</p>
<p>Same people, three years: <b>{M(tot[2022])} → {M(tot[2023])} → {M(tot[2024])}</b>. Without the one-time Acquisitions line that is $67.6M → $67.0M → $58.9M, a 13% fall. The count of people paid barely moves ({fx[2022]['PAID_NPIS']:,} → {fx[2023]['PAID_NPIS']:,} → {fx[2024]['PAID_NPIS']:,}). What moves is royalties ({M(agg[order[0]][2022])} → {M(agg[order[0]][2024])}) and a {M(agg[order[1]][2022])} 'acquisition' year in 2022 that did not repeat. Speaking and consulting money is flat at about $17-19M a year.</p>
<p>'Is industry still paying them?' Yes, and it is not shrinking because they opted out; it is shrinking because two or three royalty streams shrank.</p>""", f1),
    ("Who pays", f"""
<p>AbbVie leads at $51.6M, but $41.1M of that is royalties to one Tennessee plastic surgeon (a breast-implant patent stream; the roster shows him opted out since 2017). Strip him and AbbVie is a $3.5M-a-year psychiatry speaker-and-meals operation across 2,600 opted-out psychiatrists and nurse practitioners.</p>
<p>Arthrex, Smith+Nephew, DePuy, Stryker, Zimmer Biomet, Medtronic: orthopedic and device royalties to 12 to 300 surgeons each. Axsome and Otsuka are the only pure drug-company entries and they pay meals and talks, not royalties.</p>
<p>Trap caught: 'ABBVIE INC.' and 'AbbVie Inc.' are separate strings in the payer column. Raw grouping splits the top payer in two.</p>""", f2),
    ("Who gets it", f"""
<p>The opt-out roster is mostly therapists (7,830 in the cohort), dentists and oral surgeons (7,798) and psychiatrists (4,014). Industry money does not care about them: therapists get essentially nothing and dentists get implant-company meals.</p>
<p>607 orthopedic, plastic and neurosurgeons - 2% of the cohort - take $149M, 69% of the money. 71% of the orthopedic surgeons were paid at least once. These are surgeons who invented a device and license it; opting out of Medicare is unrelated to that income.</p>
<p>The affidavit specialty label agrees with Open Payments' own taxonomy for the big names (checked PY2023: 'Orthopedic Surgery' maps to 'Orthopaedic Surgery' and its sub-specialties).</p>""", f3),
    ("How concentrated", f"""
<p>{C['PAID_NPIS']:,} of the 27,547 (41%) received at least one dollar in three years; 5,089 were paid in all three years. The median recipient got <b>${C['MED_PER_NPI']:,.0f}</b> over three years; {C['UNDER_100']:,} got under $100.</p>
<p>Top 10 people: {M(C['TOP10'])} (53%). Top 100: {M(C['TOP100'])} (84%). The headline dollar figure is a story about roughly 100 surgeons with patents, not about 27,000 clinicians who left Medicare.</p>""", f4),
]
footer = ("Sources: LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS (57,209 rows, 56,455 NPIs, current-snapshot roster; effective dates 1998-2026, every end date is 2026-06-30 or later); "
          "HEALTH__FED_CMS_OPEN_PAYMENTS_2022 (13.3M rows), _2023 (14.7M), HEALTH__FED_CMS_OPEN_PAYMENTS (15.4M, PROGRAM_YEAR 2024 only). Join on NPI, cohort = min(OPTOUT_EFFECTIVE_DATE) &lt; 2023-01-01. "
          f"First-pass $70.8M reproduced as 'opted out on or before the payment date' x PY2023 = ${fp['EFF_ON_OR_BEFORE_PAYMENT']:,.0f}. "
          "Caveat: the roster is a live snapshot, so anyone who opted out before 2023 and has since re-enrolled is missing; the cohort is survivors. All queries: queries.py, queries2.py, queries.log.")
write_story(D + "story.html", "Opted out of Medicare, still on industry payroll", lede, sections, footer, hero)
print("ok", sum(tot.values()), tot, {b: agg[b] for b in order})
