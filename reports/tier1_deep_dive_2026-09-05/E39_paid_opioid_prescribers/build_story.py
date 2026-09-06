"""Build story.html for E39 from the query results saved in the scratchpad by queries.py.
Run from repo root: PYTHONPATH=reports/tier1_deep_dive_2026-09-05 python3 reports/tier1_deep_dive_2026-09-05/E39_paid_opioid_prescribers/build_story.py
"""
import json
import plotly.graph_objects as go
from _shared.viz import PAL, TEXT2, base_fig, bar_style, write_story

SCRATCH = "/private/tmp/claude-501/-Users-chrisr--Desktop-The-Ripple-Portfolio-Ripple-v6/8b65fde3-6771-4850-89e5-068eb53d8a29/scratchpad"
OUT = "reports/tier1_deep_dive_2026-09-05/E39_paid_opioid_prescribers/story.html"
m7 = json.load(open(f"{SCRATCH}/e39_main7.json"))   # PY2024, aligned year
m3 = json.load(open(f"{SCRATCH}/e39_main3.json"))   # PY2022 payments vs DY2024 prescribing
m4 = json.load(open(f"{SCRATCH}/e39_main4.json"))   # PY2023 payments vs DY2024 prescribing
fx = json.load(open(f"{SCRATCH}/e39_fix.json"))     # skeptic fixes: standardised comparators, matched specialties, bounds
f = lambda x: float(x)

# ---------- chart 1: deciles of all-industry money ----------
dec = m7["deciles"]
labels = ["unpaid"] + [f"D{r['DEC']}<br>${f(r['USD_MED']):,.0f}" for r in dec[1:]]
fig1 = base_fig("Industry money in general barely moves opioid prescribing",
                "Opioid share of Part D claims by decile of total 2024 industry payments per prescriber (label = median $ in the decile)")
fig1.add_trace(go.Bar(x=labels, y=[f(r["AGG_RATE"]) for r in dec], name="opioid share of claims, %",
                      marker_color=[PAL[1]] + [PAL[0]] * 10,
                      text=[f"{f(r['AGG_RATE']):.1f}%" for r in dec], textposition="outside",
                      customdata=[[r["N"], f(r["MEAN_RATE"]), f(r["SHARE_GE10"]) * 100] for r in dec],
                      hovertemplate="%{x}<br>opioid share of claims: %{y:.2f}%<br>prescribers: %{customdata[0]:,}<br>mean of per-prescriber rates: %{customdata[1]:.1f}%<br>share of prescribers at 10%+ opioid: %{customdata[2]:.1f}%<extra></extra>"))
fig1.update_layout(yaxis_title="opioid claims as % of all Part D claims", yaxis_range=[0, 5], showlegend=False)
bar_style(fig1)

# ---------- chart 2: within specialty, three groups ----------
tg = fx["matched"]
specs = ["Nurse Practitioner", "Physician Assistant", "Family Practice", "Internal Medicine", "Physical Medicine and Rehabilitation", "Anesthesiology", "Pain Management", "Interventional Pain Management"]
short = {"Physical Medicine and Rehabilitation": "PM&R", "Interventional Pain Management": "Interventional Pain", "Nurse Practitioner": "Nurse Practitioner", "Physician Assistant": "Physician Assistant", "Family Practice": "Family Practice", "Internal Medicine": "Internal Medicine", "Anesthesiology": "Anesthesiology", "Pain Management": "Pain Management"}
groups = [("0 unpaid", "unpaid", PAL[0]), ("1 paid, no opioid brand", "paid, but not by an opioid maker", PAL[2]), ("2 paid by opioid maker", "paid by an opioid maker", PAL[7])]
fig2 = base_fig("The gap is nurse practitioners and physician assistants; pain doctors on the list write 1.2x their peers",
                "Opioid share of Part D claims, 2024, by who paid the prescriber, within matched specialties. Dentists left out: only 2 took opioid-brand money.")
for key, name, col in groups:
    rows = {r["PRSCRBR_TYPE"]: r for r in tg if r["GRP"] == key}
    ys = [f(rows[s]["AGG_RATE"]) for s in specs]
    fig2.add_trace(go.Bar(x=[short[s] for s in specs], y=ys, name=name, marker_color=col,
                          text=[f"{y:.0f}" for y in ys], textposition="outside", textfont=dict(size=11),
                          customdata=[[rows[s]["N"]] for s in specs],
                          hovertemplate="%{x} - " + name + "<br>opioid share of claims: %{y:.1f}%<br>prescribers: %{customdata[0]:,}<extra></extra>"))
fig2.update_layout(barmode="group", yaxis_title="opioid claims as % of all Part D claims", yaxis_range=[0, 68], height=540)
bar_style(fig2)

# ---------- chart 3: dose response inside the opioid-paid group ----------
dose = m7["dose"]
xl = [f"Q{r['Q']}<br>median ${f(r['MED_USD']):,.0f}<br>{f(r['MED_NPAY']):.0f} payment{'s' if f(r['MED_NPAY'])>1 else ''}" for r in dose]
fig3 = base_fig("The more lunches a prescriber gets, the more opioids they already write",
                "The 6,477 prescribers paid by an opioid maker in 2024, split into fifths by opioid-brand dollars received")
fig3.add_trace(go.Bar(x=xl, y=[f(r["AGG_RATE"]) for r in dose], name="opioid share of claims, %", marker_color=PAL[7],
                      text=[f"{f(r['AGG_RATE']):.1f}%" for r in dose], textposition="outside",
                      customdata=[[r["N"], f(r["LO"]), f(r["HI"]), f(r["MED_TOT"]), f(r["SHARE_GE10"]) * 100] for r in dose],
                      hovertemplate="%{x}<br>opioid share of claims: %{y:.1f}%<br>prescribers: %{customdata[0]:,}<br>opioid-brand $ range: $%{customdata[1]:,.0f} to $%{customdata[2]:,.0f}<br>median claims: %{customdata[3]:,.0f}<br>at 10%+ opioid: %{customdata[4]:.0f}%<extra></extra>"))
fig3.add_hline(y=3.09, line_dash="dot", line_color=TEXT2, annotation_text="unpaid prescribers: 3.1%", annotation_position="top right")
fig3.update_layout(yaxis_title="opioid claims as % of all Part D claims", yaxis_range=[0, 62], showlegend=False)
bar_style(fig3)

# ---------- chart 4: share of prescribers vs share of opioid claims ----------
tot = [r for r in m7["targeting"] if r["SPEC"] is None]
n_all = sum(r["N"] for r in tot); op_all = sum(r["OPIOID_CLMS"] for r in tot)
bd = fx["bound"][0]; share_lo, share_hi = f(bd["SHARE_LO"]), f(bd["SHARE_HI"])
fig4 = base_fig("0.46% of prescribers, 14% to 15% of Medicare's opioid prescriptions",
                "Each group's share of Part D prescribers vs its share of unsuppressed Part D opioid claims, 2024. Filling CMS-suppressed blanks with 10 lowers the red bar to 14.1%.")
gl = [name for _, name, _ in groups]
fig4.add_trace(go.Bar(x=gl, y=[r["N"] / n_all * 100 for r in tot], name="share of prescribers", marker_color=PAL[0],
                      text=[f"{r['N']/n_all*100:.1f}%" if r["N"]/n_all > 0.01 else f"{r['N']/n_all*100:.2f}%" for r in tot], textposition="outside",
                      customdata=[[r["N"]] for r in tot], hovertemplate="%{x}<br>%{y:.2f}% of prescribers (%{customdata[0]:,})<extra></extra>"))
fig4.add_trace(go.Bar(x=gl, y=[r["OPIOID_CLMS"] / op_all * 100 for r in tot], name="share of opioid claims", marker_color=PAL[1],
                      text=[f"{r['OPIOID_CLMS']/op_all*100:.1f}%" for r in tot], textposition="outside",
                      customdata=[[r["OPIOID_CLMS"]] for r in tot], hovertemplate="%{x}<br>%{y:.1f}% of opioid claims (%{customdata[0]:,})<extra></extra>"))
fig4.update_layout(barmode="group", yaxis_title="% of total", yaxis_range=[0, 70])
bar_style(fig4)

# ---------- prose ----------
pv = {r["PAID"]: r for r in m7["paid_vs_unpaid"]}
st = m7["standardised"][0]
t22 = {r["GRP"]: r for r in m3["targeting"] if r["SPEC"] is None}
t23 = {r["GRP"]: r for r in m4["targeting_2023"]}
opg = [r for r in tot if r["GRP"].startswith("2")][0]

lede = ("Open Payments is the federal ledger of every meal, fee and gift a drug or device company gives a clinician, keyed by NPI, the 10-digit national provider ID. "
        "Medicare Part D is the drug benefit; CMS publishes one row per prescriber with their opioid claims as a share of all claims. "
        "Both are data year 2024. The first pass said paid prescribers write far more opioids. They do not, in general. "
        "The ones paid <i>by an opioid maker</i> do — 2.4x their specialty-matched peers, almost all of it nurse practitioners and physician assistants — and that is targeting, not a purchase.")
std = {r["GRP"]: f(r["AGG_AT_OPIOID_MIX"]) for r in fx["std"]}
hero = [(f"{opg['N']:,}", "prescribers paid by an opioid maker in 2024"),
        (f"{f(opg['AGG_RATE']):.1f}%", f"of their Part D claims are opioids (unpaid: 3.1% raw, {std['0 unpaid']:.1f}% at the same specialty mix)"),
        (f"{share_lo:.1f}-{share_hi:.1f}%", "of all Medicare opioid claims come from that 0.46%"),
        ("$55", "median opioid-brand money received, almost all lunches")]

s1 = (f"<p>Every Part D prescriber ({n_all:,}, NPI unique) was matched to their total 2024 industry payments. {pv[True]['N']:,} took something; {pv[False]['N']:,} took nothing.</p>"
      f"<p>Paid prescribers' opioid share of claims is <b>{f(pv[True]['AGG_RATE']):.2f}%</b> vs <b>{f(pv[False]['AGG_RATE']):.2f}%</b> unpaid. The mean of per-prescriber rates reads {f(pv[True]['MEAN_RATE']):.1f} vs {f(pv[False]['MEAN_RATE']):.1f}, which is probably the first pass's 'much higher'. Half of it is specialty mix: give the unpaid the paid group's specialty mix and their mean rises to {f(st['UNPAID_AT_PAID_MIX']):.1f} against {f(st['PAID_ACTUAL']):.1f}.</p>"
      f"<p>Across deciles of money it is flat. $17 a year and $1,400 a year look the same. Only the top decile ($2,091+) ticks up, and inside it the story is surgeons and pain doctors, not the money.</p>")
s2 = (f"<p>The landing table of Open Payments names the product behind each payment. Filtering to opioid painkiller brands (Belbuca, Xtampza, RoxyBond, Nucynta, Dsuvia, Olinvyk and the rest; addiction-treatment products left out) finds {opg['N']:,} prescribers. {6454:,} of them were paid by one company, Collegium Pharmaceutical, which sells Belbuca and Xtampza. Median payment: $17. 99.98% food and beverage.</p>"
      f"<p>Nurse practitioners on that list write <b>41.4%</b> opioids; nurse practitioners paid by any other company write 2.6%; unpaid ones 3.2%. Physician assistants: 44.5% vs 4.4% vs 5.1%. Family practice 9.9% vs 2.7% vs 2.7%. Internal medicine 6.2% vs 2.1% vs 2.3%.</p>"
      f"<p>Pain specialists are the check. Pain management on the list writes 56.5% vs 46.5% unpaid; interventional pain 59.5% vs 48.3%; anesthesiology 56.1% vs 39.8%. About 1.2x. Their unpaid peers already write half their scripts as opioids, so the lunch marks little there.</p>"
      f"<p>Put together: give the unpaid the opioid-maker group's specialty mix and they write {std['0 unpaid']:.1f}%, not 3.1%; the paid-by-others {std['1 paid, no opioid brand']:.1f}%. The honest gap is 2.4x, and it is carried by NPs (13x) and PAs (8.7x), not by pain doctors.</p>")
s3 = (f"<p>Split the {opg['N']:,} into fifths by opioid-brand dollars. The bottom fifth got one $17 lunch and writes 24.8% opioids. The top fifth got a median 14 payments, $219, and writes 52.7%.</p>"
      f"<p>Read that as a rep's call sheet. Nobody's prescribing habit is bought for $219 of sandwiches; reps visit the offices that already write the most of their drug, and visit the biggest ones most often. Payments from 2022 (a different company, Kowa, then dominated) and 2023 mark the same kind of prescriber in 2024: {f(t22['2 paid by opioid maker']['AGG_RATE']):.1f}% and {f(t23['2 paid by opioid maker']['AGG_RATE']):.1f}% opioid share vs ~3% for everyone else. The list is stable because the prescribing is.</p>"
      f"<p>Part D here is a single year, so before-and-after is not testable in this warehouse. What is shown is who the money finds, not what it does.</p>")
s4 = (f"<p>The opioid-maker group is {opg['N']:,} of {n_all:,} prescribers, 0.46%, and writes {opg['OPIOID_CLMS']:,} of {op_all:,} unsuppressed Medicare opioid claims, {share_hi:.1f}%. CMS blanks counts of 1 to 10; fill every blank with 10 and the share is {share_lo:.1f}%. So: {share_lo:.1f}% to {share_hi:.1f}%. Median 2,267 claims each vs 136 for the unpaid.</p>"
      f"<p>Who they are: 2,142 nurse practitioners, 1,240 physician assistants, then pain management (625), anesthesiology (559), physical medicine (518), interventional pain (430). The pain specialists write 55 to 59% opioids; the NPs and PAs on the list write 41 to 44%, ten times their peers.</p>"
      f"<p>Suppression check: CMS blanks opioid counts of 1 to 10. Filling the blanks with 1 or with 10 moves this group's rate from 38.72% to 38.73%. It moves the unpaid from 3.12% to 3.41%. Nothing here rides the blanks.</p>")

footer = ("Sources: LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS (Medicare Part D Prescribers by Provider, data year 2024, 1,416,883 rows, NPI unique); "
          "LIBRARY_RAW.LANDING.FED_CMS_OPEN_PAYMENTS (Open Payments program year 2024, 15,385,047 rows; landing used because the mart drops the drug-name columns); "
          "FED_CMS_OPEN_PAYMENTS_2022 and _2023 for the prior-year checks. Teaching-hospital payment rows excluded. "
          "Opioid share = OPIOID_TOT_CLMS / TOT_CLMS summed over the group; blanks are CMS-suppressed counts of 1 to 10 and are excluded unless stated. Opioid-brand match is a brand-name list only (no bare generics; addiction-treatment products excluded). "
          "Queries: <code>queries.py</code>, log: <code>queries.log</code>. Built 2026-09-05.")

write_story(OUT, "Who gets the opioid maker's lunch", lede,
            [("Industry money in general: almost nothing", s1, fig1),
             ("Opioid-maker money: a different population", s2, fig2),
             ("More lunches, more opioids, already", s3, fig3),
             ("The call list, sized", s4, fig4)], footer, hero=hero)
print("wrote", OUT)
