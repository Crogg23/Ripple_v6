"""Build story.html from results.json (no warehouse calls)."""
import json
import plotly.graph_objects as go
from _shared.viz import PAL, base_fig, bar_style, write_story
D = "reports/tier1_deep_dive_2026-09-05/E48_closures_predicted/"
R = json.load(open(D + "results.json"))
LBL = {"a <-30%":"< -30%","b -30..-20":"-30 to -20","c -20..-10":"-20 to -10","d -10..-5":"-10 to -5","e -5..0":"-5 to 0","f 0..5":"0 to 5","g 5..10":"5 to 10","h 10..20":"10 to 20","i >20%":"> 20%"}

# 1 margin distribution, share of each group per bin
rows = R["C_margin_bins"]; ta = sum(r["ACTIVE"] for r in rows); tt = sum(r["TERM"] for r in rows)
x = [LBL[r["BIN"]] for r in rows]
f1 = base_fig("Terminated hospitals sit two bins left of everyone else", f"Latest 12-month cost report, net income as % of total cost. {tt} terminated 2024-26 vs {ta:,} still active.")
f1.add_bar(name=f"Terminated 2024-26 (n={tt})", x=x, y=[round(100*r["TERM"]/tt,1) for r in rows], marker_color=PAL[1], text=[f'{100*r["TERM"]/tt:.0f}%' for r in rows], textposition="outside", hovertemplate="%{x}: %{y}% of terminated (%{customdata} hospitals)<extra></extra>", customdata=[r["TERM"] for r in rows])
f1.add_bar(name=f"Still active (n={ta:,})", x=x, y=[round(100*r["ACTIVE"]/ta,1) for r in rows], marker_color=PAL[0], hovertemplate="%{x}: %{y}% of active (%{customdata} hospitals)<extra></extra>", customdata=[r["ACTIVE"] for r in rows])
f1.update_layout(barmode="group", yaxis_title="share of group (%)", xaxis_title="net income / total cost, latest report")
bar_style(f1)

# 2 threshold test: termination rate by bin
rows = R["D_threshold_by_bin"]
f2 = base_fig("The -30 to -20 bin terminated most, 10.1%; below -30 it eases to 7.6%", "Of every hospital in the bin, the share whose Medicare participation ended 2024-26. Closures exclude code 07 status changes.")
f2.add_bar(name="Any termination", x=[LBL[r["BIN"]] for r in rows], y=[float(r["PCT_TERM"]) for r in rows], marker_color=PAL[1], text=[f'{float(r["PCT_TERM"]):.1f}%' for r in rows], textposition="outside", hovertemplate="%{x}: %{y}% terminated, %{customdata[0]} of %{customdata[1]}<extra></extra>", customdata=[[r["TERM"], r["N"]] for r in rows])
f2.add_bar(name="Closure-type only (codes 01/03/04/05)", x=[LBL[r["BIN"]] for r in rows], y=[float(r["PCT_CLOSURE"]) for r in rows], marker_color=PAL[7], hovertemplate="%{x}: %{y}% closure-type, %{customdata[0]} of %{customdata[1]}<extra></extra>", customdata=[[r["CLOSURE"], r["N"]] for r in rows])
f2.update_layout(barmode="group", yaxis_title="% terminated 2024-26", xaxis_title="net income / total cost, latest report")
bar_style(f2)

# 3 stacked signals
rows = R["D_stacked_signals"]
f3 = base_fig("Four red flags at once: 8.5% terminated, eight times the clean group", "Flags: net loss, operating loss, negative fund balance (equity), current ratio under 1. Hospitals with all four fields filled.")
f3.add_bar(name="Any termination", x=[str(r["SIGNALS"]) for r in rows], y=[float(r["PCT_TERM"]) for r in rows], marker_color=PAL[1], text=[f'{float(r["PCT_TERM"]):.1f}%' for r in rows], textposition="outside", hovertemplate="%{x} flags: %{y}% terminated, %{customdata[0]} of %{customdata[1]}<extra></extra>", customdata=[[r["TERM"], r["N"]] for r in rows])
f3.add_bar(name="Closure-type only", x=[str(r["SIGNALS"]) for r in rows], y=[float(r["PCT_CLOSURE"]) for r in rows], marker_color=PAL[7], hovertemplate="%{x} flags: %{y}% closure-type, %{customdata[0]} of %{customdata[1]}<extra></extra>", customdata=[[r["CLOSURE"], r["N"]] for r in rows])
f3.update_layout(barmode="group", yaxis_title="% terminated 2024-26", xaxis_title="number of red flags on the latest report")
bar_style(f3)

# 4 by termination code
rows = [r for r in R["B_by_term_code"]]
order = ["01 voluntary merger/closure","07 status change","05 involuntary","active"]
rows.sort(key=lambda r: order.index(r["TGRP"]))
names = {"01 voluntary merger/closure":"01 closure/merger","07 status change":"07 status change","05 involuntary":"05 involuntary","active":"still active"}
f4 = base_fig("Sales and status changes look just as broke as closures", "Share with a net loss on the latest 12-month report, by the POS termination code.")
f4.add_bar(x=[names[r["TGRP"]] for r in rows], y=[float(r["PCT_NEG"]) for r in rows], marker_color=[PAL[7],PAL[1],PAL[3],PAL[0]], text=[f'{float(r["PCT_NEG"]):.0f}% (n={r["N"]})' for r in rows], textposition="outside", hovertemplate="%{x}: %{y}% losing money, %{customdata[0]} of %{customdata[1]}, median margin %{customdata[2]}%<extra></extra>", customdata=[[r["NEG"], r["N"], r["MED_M_COST"]] for r in rows])
f4.update_layout(yaxis_title="% with net loss", yaxis_range=[0,90], showlegend=False)
bar_style(f4)

b = {r["GRP"]: r for r in R["B_rebuild_68"]}
t = b["term_2024_26"]; a = b["active"]
lede = ("A CCN is the Medicare certification number that identifies one hospital. CMS's Provider of Services file (POS) records when a CCN's Medicare participation ended and a code for why; "
        "the hospital cost report (HCRIS) records its income statement and balance sheet. Match the two and ask: did the last cost report already show a loss?")
hero = [(f"{t['PCT_NEG']}%", f"of {t['N']} hospitals terminated 2024-26 lost money on their last full-year report"),
        (f"{a['PCT_NEG']}%", f"of {a['N']:,} still-active hospitals lost money on theirs"),
        (f"{t['MED_M_COST']}%", "median margin (net income / total cost), terminated"),
        ("0 hospitals", "have two 350-380 day reports in this file: a loss streak cannot be measured")]
S = []
S.append(("The whole shape moves, not just the sign",
 f"<p>The first pass said 68% of terminated hospitals were losing money. Rebuilt with a different selection rule (latest 12-month report ending on or before the termination date, NaN-guarded): <b>{t['NEG']} of {t['N']} = {t['PCT_NEG']}%</b>, against {a['PCT_NEG']}% of active hospitals. Reproduces within one hospital of the first pass (142 vs 141; the one dropped filed its report after its termination date).</p>"
 f"<p>The distribution is shifted, not just tipped. Terminated hospitals: 10th percentile -33.6%, median -8.1%, 75th percentile +3.3%. Active: -14.6%, +5.3%, +17.0%. A quarter of the terminated group was still profitable.</p>", f1))
S.append(("Closures and sales are the same story",
 "<p>POS code 01 is voluntary merger or closure, 07 is a provider status change (renumbered, converted, absorbed; 50 of 58 list a successor CCN), 05 is involuntary. "
 "The hunch's worry was that sales dilute the failure story. They do not: <b>code 01 was 68% in the red, code 07 was 69%</b>, medians -8.5% and -8.3%. The four involuntary terminations were mostly profitable, which is what a safety-rule shutdown looks like. "
 "Of the 192 hospitals terminated 2024-26 in POS, 141 have a 12-month report; 16 have no report at all and 32 only a stub shorter than 350 days, and those are likely the ones that fell apart mid-year.</p>", f4))
S.append(("The threshold test, cross-section version",
 "<p>The ask was: of hospitals with three straight loss years, how many closed? <b>Not testable here.</b> HCRIS in this warehouse is one vintage: 5,812 hospitals carry exactly one 350-380 day report and no hospital has two. So the test runs on the one report each hospital has: for every margin bin, what share was terminated within the window.</p>"
 "<p>Below zero, 4.8% terminated (2.8% closure-type). Below -10%, 6.8%. Below -20%, 8.4% (5.5% closure-type). Above +10%, 1.0%. A loss roughly quadruples the odds; a deep loss is about 7x the profitable group (8.4% over the 1.2% base). The curve reverses at the bottom: -30 to -20 terminates 10.1%, below -30 only 7.6% (23 of 301). And 92% of hospitals under -20% did not terminate, so this is a watch list, not a prediction.</p>", f2))
S.append(("Stacking flags is the closest thing to a loss streak",
 "<p>A negative fund balance means accumulated losses have eaten the equity, which is the balance-sheet trace of years of losses. Combine four flags from the same report: net loss, operating loss, negative fund balance, current ratio under 1. "
 "Zero flags: 1.1% terminated. Two: 3.8%. All four: <b>8.5% terminated, 6.5% closure-type</b> (29 of 341). Terminated hospitals carry negative equity at 32% (45 of 138) against 13.6% of active ones. Still: 312 of 341 four-flag hospitals are open.</p>", f3))
foot = ("Sources: LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS (6,103 rows, FY ends 2022-11 to 2024-09, one ingest) and HEALTH__FED_CMS_POS_OTHER category 01 (13,540 hospitals, latest termination 2026-03-05). "
        "Margin = NET_INCOME / TOTAL_COSTS on the latest report of 350-380 days ending on or before the termination date; NaN floats excluded. Queries: <code>queries.py</code>, log in <code>queries.log</code>. "
        "Trap: NET_MARGIN_RATIO in the mart is net income over gross patient charges, not net revenue; it is 2-3x smaller than either conventional margin and was not used.")
write_story(D + "story.html", "Broke Before They Closed", lede, S, foot, hero)
print("ok")
