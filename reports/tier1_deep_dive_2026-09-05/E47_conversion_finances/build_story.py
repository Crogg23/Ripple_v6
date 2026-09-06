"""Builds story.html from results.json (no warehouse calls)."""
import json
import plotly.graph_objects as go
from _shared.viz import PAL, DIV, TEXT2, base_fig, bar_style, write_story
D = "reports/tier1_deep_dive_2026-09-05/E47_conversion_finances"
R = json.load(open(f"{D}/results.json"))
REH_C, BASE_C = PAL[1], PAL[0]

# --- chart 1: share losing money, REH vs comparison groups, raw counts on the bar
order = ["REH predecessors", "rural CAH+STH <=25 beds (not REH)", "rural CAH+STH (not REH)", "rural, all types", "all hospitals"]
labels = {"REH predecessors": "REH converters (last full year before switch)",
          "rural CAH+STH <=25 beds (not REH)": "Rural hospitals, 25 beds or fewer",
          "rural CAH+STH (not REH)": "Rural critical-access + short-term hospitals",
          "rural, all types": "Rural hospitals, every type", "all hospitals": "All US hospitals"}
g = {r["GRP"]: r for r in R["base_groups"]}
fig1 = base_fig("REH converters lose money at 2.5x the rural base rate",
                "Share with negative net income on the latest full-year cost report, FY ends 2023-2024")
fig1.add_trace(go.Bar(
    y=[labels[k] for k in order][::-1], x=[float(g[k]["PCT_NEG"]) for k in order][::-1], orientation="h",
    marker_color=[REH_C if k == "REH predecessors" else BASE_C for k in order][::-1],
    text=[f"{g[k]['NEG']} of {g[k]['N']:,}  ({float(g[k]['PCT_NEG'])}%)" for k in order][::-1],
    textposition="outside", cliponaxis=False,
    hovertemplate="%{y}<br>%{text}<br>median margin of cost: %{customdata}%<extra></extra>",
    customdata=[g[k]["MED_M_COST"] for k in order][::-1]))
fig1.update_layout(xaxis=dict(title="% of hospitals losing money", range=[0, 105]), showlegend=False, height=420)
bar_style(fig1)

# --- chart 2: margin distribution, REH vs rural base, share of group with n
bk = {}
for r in R["buckets"]: bk.setdefault(r["GRP"], {})[r["BUCKET"]] = r["N"]
buckets = ["a. under -20%", "b. -20% to -10%", "c. -10% to 0", "d. 0 to +5%", "e. +5% to +10%", "f. over +10%"]
bl = ["worse than -20%", "-20% to -10%", "-10% to 0", "0 to +5%", "+5% to +10%", "better than +10%"]
fig2 = base_fig("Where the money goes: half of REH converters sat below -10%, most rural hospitals sat above +5%",
                "Net income as % of total cost, latest full-year report; bars are share of each group, hover for counts")
for grp, col, name in [("REH predecessors", REH_C, "REH converters (n=23; Covington County MS excluded, flagged urban)"), ("rural CAH+STH (not REH)", BASE_C, "Rural CAH + short-term, not REH (n=2,418)")]:
    n = sum(bk[grp].values()); vals = [bk[grp].get(b, 0) for b in buckets]
    fig2.add_trace(go.Bar(name=name, x=bl, y=[100 * v / n for v in vals], marker_color=col,
                          text=[f"{v}" for v in vals], textposition="outside", cliponaxis=False,
                          hovertemplate="%{x}<br>" + name + ": %{text} hospitals (%{y:.1f}%)<extra></extra>"))
fig2.update_layout(barmode="group", yaxis=dict(title="% of group"), height=460)
bar_style(fig2)

# --- chart 3: every converter, last full year before switching
rows = sorted(R["reh_rows"], key=lambda r: r["M_COST"])
fig3 = base_fig("23 converters, one bar each: 19 in the red before the switch",
                "Net income as % of total cost on the last full-year report that closed before the conversion date")
fig3.add_trace(go.Bar(
    x=[r["M_COST"] * 100 for r in rows], y=[f"{r['HOSPITAL_NAME'].title()[:34]} ({r['STATE']})" for r in rows], orientation="h",
    marker_color=[DIV[2] if r["M_COST"] < 0 else DIV[0] for r in rows],
    customdata=[[r["FISCAL_YEAR_END_DATE"], r["REH_CONVERSION_DATE"], r["NUMBER_OF_BEDS"], r["CCN_FACILITY_TYPE"], f"{r['NET_INCOME']:,.0f}", r["PRED_CCN"]] for r in rows],
    hovertemplate="%{y}<br>margin of cost: %{x:.1f}%<br>net income: $%{customdata[4]}<br>FY end %{customdata[0]}, converted %{customdata[1]}<br>%{customdata[2]} beds, %{customdata[3]}, old CCN %{customdata[5]}<extra></extra>"))
fig3.add_vline(x=0, line_color=TEXT2, line_width=1)
fig3.add_vline(x=4.69, line_dash="dot", line_color=BASE_C, annotation_text="rural median +4.7%", annotation_position="top")
fig3.update_layout(xaxis=dict(title="net income as % of total cost"), yaxis=dict(tickfont=dict(size=11)), height=720, showlegend=False)
bar_style(fig3)

# --- chart 4: before/after pairs
pr = sorted(R["pairs_loose"], key=lambda r: r["PRE_PCT"])
fig4 = base_fig("After the switch: 4 of 7 with a report on both sides went from red to black",
                "Same hospital, last report under the old CCN vs first under the REH CCN; periods are mostly stubs, hover for lengths")
names = [f"{r['ORGANIZATION_NAME'].title()[:30]} ({r['STATE']})" for r in pr]
fig4.add_trace(go.Bar(name="before (old CCN)", x=names, y=[r["PRE_PCT"] for r in pr], marker_color=PAL[1],
                      customdata=[[r["PRE_FY"], r["PRE_LEN"]] for r in pr],
                      hovertemplate="%{x}<br>before: %{y}% of cost<br>FY end %{customdata[0]}, %{customdata[1]}-day period<extra></extra>"))
fig4.add_trace(go.Bar(name="after (REH CCN)", x=names, y=[r["POST_PCT"] for r in pr], marker_color=PAL[2],
                      customdata=[[r["POST_FY"], r["POST_LEN"]] for r in pr],
                      hovertemplate="%{x}<br>after: %{y}% of cost<br>FY end %{customdata[0]}, %{customdata[1]}-day period<extra></extra>"))
fig4.update_layout(barmode="group", yaxis=dict(title="net income as % of total cost"), xaxis=dict(tickfont=dict(size=11)), height=480)
bar_style(fig4)

lede = ("A Rural Emergency Hospital (REH) is a Medicare status created in 2023: a small rural hospital gives up its inpatient beds, keeps the ER and outpatient care, "
        "and gets a monthly federal payment in return. 48 hospitals have taken it. Their Medicare cost reports (HCRIS, one per hospital per fiscal year, filed under the "
        "hospital's CMS Certification Number, CCN) show that most were already losing money in their last full year before converting.")
hero = [("20 of 24", "converters with a readable report losing money (83%); 48 converters total"),
        ("807 of 2,418", "rural CAH + short-term hospitals losing money (33%)"),
        ("-9.5%", "converter median margin of cost, vs +4.7% rural")]
s1 = ("<p>Each converter's new REH CCN carries the old hospital's CCN in the enrollment file. Match that old CCN to the cost report file, keep reports that run a full year "
      "and have a readable revenue line, and take the latest one. 35 of 48 have any report, 25 a full-year one, 24 with revenue filled.</p>"
      "<p><b>20 of 24 were in the red.</b> If all 24 unmeasured converters were profitable the floor is 20 of 48 (42%). Strict before-conversion (drop Kiowa County OK, whose report closed 4 days after its date) is 19 of 23 (83%). The headline uses 20 of 24. The rural base rate on the same file and the same filters is 807 of 2,418 (33.4%). The gap is not a bed-size effect: rural hospitals of 25 beds or fewer run 404 of 1,257 (32.1%). Urban hospitals run 993 of 3,074 (32.3%), so this is converters against all hospitals, not rural against urban.</p>")
s2 = ("<p>The converters are not just slightly negative. 10 of 24 sat below -10% of cost, 4 below -20%. Rural hospitals as a whole put 271 of 2,418 (11.2%) below -10%, and 842 (34.8%) above +10%.</p>"
      "<p>Two converters were solidly profitable (Sharkey-Issaquena MS +30.8%, Parkland-Bonne Terre MO +60.4%) and two mildly so; the program is mostly a lifeline, not entirely.</p>")
s3 = ("<p>The same 24 with names, minus Kiowa County OK whose report closed 4 days after its conversion date. Worst are Westfield NY at -34% and Adair County OK at -32%. "
      "Five of the 23 also had negative net worth (total fund balance below zero), against 230 of 2,418 rural (9.5%).</p>"
      "<p>The gap between report and conversion runs from 23 days (Harper County OK) to 804 days (Garden County NE); the late 2025-2026 converters are measured on a 2023 report because the warehouse holds only one HCRIS vintage.</p>")
s4 = ("<p>14 of the 48 already filed a cost report under the new REH CCN. 7 of those also have a readable report under the old CCN. Every one of the 7 was a stub period on at least one side, so read the direction, not the size.</p>"
      "<p>4 of 7 flipped from negative to positive. Our Lady of the Lake Assumption LA was already +16.4% before and read +50.7% after. Sturgis MI (-55% to -38%) and Five Rivers AR (-16% to -16%) stayed negative. Too few and too short to call a trend; enough to say the after-picture exists in the warehouse.</p>")
footer = ("Tables: LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS (REH_CONVERSION_FLAG, CAH_OR_HOSPITAL_CCN pipe-separated, first piece = predecessor), "
          "HEALTH__FED_CMS_HCRIS (6,103 reports, one vintage, FY ends 2022-2024), HEALTH__FED_CMS_POS_OTHER (predecessor termination dates). "
          "Full-year = 350-380 days; revenue readable = NET_PATIENT_REVENUE not NaN (the mart keeps NaN as a FLOAT). Margin = NET_INCOME / TOTAL_COSTS. "
          "A 3-year pre-conversion trend was asked for and cannot be built: every CCN has exactly one clean report in the warehouse. Queries: queries.py, log: queries.log.")
write_story(f"{D}/story.html", "Broke before the switch: Rural Emergency Hospital converters", lede,
            [("83% were losing money; the rural base rate is 33%", s1, fig1),
             ("Not slightly negative, deeply negative", s2, fig2),
             ("Every converter, named", s3, fig3),
             ("What happens after", s4, fig4)], footer, hero)
print("wrote story.html")
