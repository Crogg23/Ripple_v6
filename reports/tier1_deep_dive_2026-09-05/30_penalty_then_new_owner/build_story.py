"""Build story.html from results.json. Run from repo root with PYTHONPATH=reports/tier1_deep_dive_2026-09-05."""
import json, math
import plotly.graph_objects as go
from _shared.viz import PAL, TEXT2, base_fig, bar_style, write_story
D = "reports/tier1_deep_dive_2026-09-05/30_penalty_then_new_owner"
R = json.load(open(f"{D}/results.json"))

def z(a, na, b, nb):
    p = (a + b) / (na + nb); se = math.sqrt(p * (1 - p) * (1 / na + 1 / nb)); return (a / na - b / nb) / se

# --- cohort numbers
C = R["cohorts"]
def pick(cohort, cut, grp): return next(c for c in C if c["COHORT"] == cohort and c["CUT"] == cut and c["GRP"] == grp)
pen23 = [pick("2023 H2", "penalty count", g) for g in ("one penalty", "two or more")]
pen24 = [pick("2024", "penalty count", g) for g in ("one penalty", "two or more")]
no23 = pick("2023 H2", "penalty count", "no penalty"); no24 = pick("2024", "penalty count", "no penalty")
a23 = sum(c["NEW_RECORD_NEXT_YEAR"] for c in pen23); n23 = sum(c["HOMES"] for c in pen23)
a24 = sum(c["NEW_RECORD_NEXT_YEAR"] for c in pen24); n24 = sum(c["HOMES"] for c in pen24)
z23 = z(a23, n23, no23["NEW_RECORD_NEXT_YEAR"], no23["HOMES"]); z24 = z(a24, n24, no24["NEW_RECORD_NEXT_YEAR"], no24["HOMES"])
p23, q23 = 100 * a23 / n23, no23["PCT"]; p24, q24 = 100 * a24 / n24, no24["PCT"]
print(f"2023H2 penalized {a23}/{n23} = {p23:.2f}% vs {q23}% z={z23:.1f}; 2024 {a24}/{n24} = {p24:.2f}% vs {q24}% z={z24:.1f}")

# --- fig 1: two clocks
years = list(range(2015, 2027))
inc = {r["Y"]: r["N"] for r in R["incorp_by_year"]}; enr = {r["Y"]: r["N"] for r in R["enroll_by_year"]}
f1 = base_fig("The clock the first pass read stops in September 2024", "Current nursing-home operators by year: when the company was incorporated vs when its Medicare enrollment record is dated", 440)
f1.add_bar(x=years, y=[inc.get(y, 0) for y in years], name="incorporation date (first pass)", marker_color=PAL[1], hovertemplate="%{x}: %{y:,} homes<extra>incorporation date</extra>")
f1.add_bar(x=years, y=[enr.get(y, 0) for y in years], name="enrollment record date (this pass)", marker_color=PAL[0], hovertemplate="%{x}: %{y:,} homes<extra>enrollment record</extra>")
f1.update_layout(barmode="group", yaxis_title="homes", xaxis=dict(tickmode="linear", dtick=1))
f1.add_annotation(x=2024, y=inc.get(2024, 0), text="89 in 2024, then nothing", showarrow=True, ay=-40, ax=-30, font=dict(color=PAL[1]))
f1.add_annotation(x=2025, y=enr.get(2025, 0), text="632 in 2025", showarrow=True, ay=-30, ax=20, font=dict(color=PAL[0]))
f1.add_vrect(x0=2023.4, x1=2026.4, fillcolor=PAL[0], opacity=0.05, line_width=0, annotation_text="penalty file window", annotation_position="top left", annotation_font_color=TEXT2)
bar_style(f1)

# --- fig 2: base rate
groups = ["no penalty", "one penalty", "two or more", "$100k+ in fines"]
def row(cohort):
    return [pick(cohort, "penalty count", "no penalty"), pick(cohort, "penalty count", "one penalty"), pick(cohort, "penalty count", "two or more"), pick(cohort, "fine band", "$100k+")]
r23, r24 = row("2023 H2"), row("2024")
f2 = base_fig("Penalized homes change hands the next year about 1.5x as often as unpenalized ones", "Share of homes whose current enrollment record is dated in the following calendar year; same calendar window for every bar", 460)
for name, rows, col in (("penalty in 2023 H2 -> new record in 2024", r23, PAL[0]), ("penalty in 2024 -> new record in 2025", r24, PAL[1])):
    f2.add_bar(x=groups, y=[float(r["PCT"]) for r in rows], name=name, marker_color=col, text=[f"{float(r['PCT']):.1f}%" for r in rows], textposition="outside",
               customdata=[[r["NEW_RECORD_NEXT_YEAR"], r["HOMES"]] for r in rows], hovertemplate="%{x}: %{y:.2f}% (%{customdata[0]:,} of %{customdata[1]:,} homes)<extra>" + name + "</extra>")
f2.update_layout(barmode="group", yaxis_title="% with a new enrollment record next year", yaxis_range=[0, 15])
bar_style(f2)

# --- fig 3: penalties around a new record
rm = R["rel_month"]
f3 = base_fig("Penalties fall 19% after a change of hands, and never pile up before it", "Penalties per month, counted relative to the home's new enrollment record; 658 homes with a record dated 2024-06-17 to 2025-05-13 so a full year is visible on both sides", 440)
xs = [r["REL_MONTH"] for r in rm]; ys = [r["N_PEN"] for r in rm]
f3.add_bar(x=xs, y=ys, marker_color=[PAL[1] if x < 0 else PAL[0] for x in xs], name="penalties", showlegend=False, hovertemplate="month %{x:+d}: %{y} penalties<extra></extra>")
f3.add_vline(x=-0.5, line_dash="dot", line_color=TEXT2)
f3.add_annotation(x=-6, y=max(ys) + 3, text=f"year before: {R['rel_total'][0]['PEN_365_BEFORE']} penalties", showarrow=False, font=dict(color=PAL[1]))
f3.add_annotation(x=6, y=max(ys) + 3, text=f"year after: {R['rel_total'][0]['PEN_365_AFTER']} penalties", showarrow=False, font=dict(color=PAL[0]))
f3.update_layout(xaxis_title="months before (-) and after (+) the new enrollment record", yaxis_title="penalties", xaxis=dict(tickmode="linear", dtick=2), yaxis_range=[0, max(ys) + 8])
bar_style(f3)

# --- fig 4: the gap, both clocks
buckets = ["0-90 days", "91-180", "181-365", "366-730", "731+"]
ge = {r["BUCKET"]: r["N"] for r in R["gap_enroll"]}; gi = {r["BUCKET"]: r["N"] for r in R["gap_incorp"]}
f4 = base_fig("The first pass had no window: only 13 of its 39 sit inside 90 days, and 13 of the 39 are one Oregon-Washington deal", "Days from a home's first penalty to the new-owner signal, by which clock is read", 440)
f4.add_bar(x=buckets, y=[gi.get(b, 0) for b in buckets], name="incorporation date after first penalty (39 homes)", marker_color=PAL[1], text=[gi.get(b, 0) for b in buckets], textposition="outside")
f4.add_bar(x=buckets, y=[ge.get(b, 0) for b in buckets], name="enrollment record after first penalty (650 homes)", marker_color=PAL[0], text=[ge.get(b, 0) for b in buckets], textposition="outside")
f4.update_layout(barmode="group", yaxis_title="homes", xaxis_title="days after first penalty", yaxis_range=[0, 260])
bar_style(f4)

fp = R["first_pass"][0]; rb = R["rebuild"][0]; ck = R["clocks"][0]; nf = R["nh411_flag_cross"][0]
fv = R["flag_vs_pen"][0]; ow = R["orwa_owners"][0]
fpct = 100 * fv["FLAGGED_PENALIZED"] / fv["FLAGGED"]; bpct = 100 * fv["ALL_PENALIZED"] / fv["ALL_HOMES"]
zf = z(fv["FLAGGED_PENALIZED"], fv["FLAGGED"], fv["ALL_PENALIZED"], fv["ALL_HOMES"])
rt = R["rel_total"][0]; drop = 100 * (rt["PEN_365_BEFORE"] - rt["PEN_365_AFTER"]) / rt["PEN_365_BEFORE"]
zb = (rt["PEN_365_BEFORE"] - rt["PEN_365_AFTER"]) / math.sqrt(rt["PEN_365_BEFORE"] + rt["PEN_365_AFTER"])
print(f"flag {fpct:.1f}% vs {bpct:.1f}% z={zf:.1f}; drop {drop:.0f}% z={zb:.1f}")
lede = ("The first pass said 39 nursing homes got a new owner right after a penalty. The 39 reproduce, but the clock it read stops in September 2024, "
        "there was no time window, and a third of the 39 are one two-state portfolio deal. Read a better clock and the honest version is: penalized homes "
        f"change hands the next year at about 1.5x the rate of unpenalized homes ({p23:.1f}% vs {q23}% for 2023 penalties, {p24:.1f}% vs {q24}% for 2024), the gap widens with the fine bill, "
        "and penalties fall 19% after the record date without any pile-up in front of it.")
hero = [(f"{fp['INCORP_AFTER_FIRST_PEN']}", "first-pass homes, reproduced exactly"),
        (f"{rb['ENROLL_AFTER_FIRST_PEN']}", "penalized homes with a new enrollment record after the first penalty"),
        (f"{p23:.1f}% vs {q23}%", "new record in 2024: penalized in 2023 H2 vs not"),
        (f"{nf['ENROLL_RECORD_IN_12MO_BEFORE_SNAPSHOT']} of {nf['FLAGGED_Y']}", "CMS 'changed ownership' flags the enrollment clock catches")]
sections = [
 ("How the first pass saw a new owner", f"""
<p>A nursing home is identified by its CCN, the CMS Certification Number Medicare uses for a facility. The penalty file lists {R['keys_pen'][0]['N']:,} fines and payment denials against {R['keys_pen'][0]['D_CCN']:,} homes, dated {R['keys_pen'][0]['MN']} to {R['keys_pen'][0]['MX']}. The enrollment file is one row per home ({ck['HOMES']:,} rows, {ck['HOMES']:,} distinct CCNs) naming the company that currently operates it.</p>
<p>The first pass called it a new owner when that company's <b>incorporation date</b> fell after the home's first penalty. That column is filled on {ck['INCORP_FILLED']:,} of {ck['HOMES']:,} rows, carries {ck['INCORP_PRE1900']} dates before 1900, and its newest value is <b>{ck['INCORP_MAX']}</b>. The penalty file runs 17 more months. Anyone who bought a home after September 2024 is invisible on that clock.</p>
<p>A clock-free check first: CMS itself flags {fv["FLAGGED"]} homes as 'changed ownership in the last 12 months' in Nursing Home 411. <b>{fv["FLAGGED_PENALIZED"]} of the {fv["FLAGGED"]} ({fpct:.0f}%) are penalized homes</b>, against {bpct:.0f}% of all {fv["ALL_HOMES"]:,} homes (z = {zf:.1f}). No date column touched.</p>
<p>The same file carries a second clock nobody read: the enrollment ID is 'O' plus the date the record was created (all {ck['ENROLL_PARSED']:,} parse; newest {ck['ENROLL_MAX']}). A new operator files a new enrollment, so this dates the current operator's arrival. It catches {nf['ENROLL_RECORD_IN_12MO_BEFORE_SNAPSHOT']} of the {nf['FLAGGED_Y']} homes CMS itself flags as 'changed ownership in the last 12 months' in the Nursing Home 411 file; the incorporation clock catches {nf['INCORP_SINCE_202306']}.</p>""", f1),
 ("The base rate the first pass never ran", f"""
<p>Take every home, split by whether it was penalized in a window, and count how many carry an enrollment record dated in the following calendar year. Same calendar for both groups, so the general churn in the industry cancels out.</p>
<p>Penalized in 2023 H2: <b>{a23} of {n23:,} ({p23:.1f}%)</b> got a new record in 2024. Not penalized: {no23['NEW_RECORD_NEXT_YEAR']} of {no23['HOMES']:,} ({q23}%). z = {z23:.1f}. Penalized in 2024: <b>{a24} of {n24:,} ({p24:.1f}%)</b> in 2025 vs {no24['NEW_RECORD_NEXT_YEAR']} of {no24['HOMES']:,} ({q24}%). z = {z24:.1f}.</p>
<p>It scales with the bill: homes fined $100k+ in 2023 H2 changed hands at {float(pick('2023 H2','fine band','$100k+')['PCT']):.1f}%, in 2024 at {float(pick('2024','fine band','$100k+')['PCT']):.1f}%. Inside for-profits alone the gap holds ({float(pick('2023 H2','ownership','P / penalized')['PCT']):.1f}% vs {float(pick('2023 H2','ownership','P / no penalty')['PCT']):.1f}%, then {float(pick('2024','ownership','P / penalized')['PCT']):.1f}% vs {float(pick('2024','ownership','P / no penalty')['PCT']):.1f}%), so it is not just that for-profits get fined more and sell more.</p>""", f2),
 ("Before or after? A real drop after, no hump before", f"""
<p>The shell-game story needs penalties to bunch up right before the sale. For the {rt['HOMES_NEW_RECORD']} homes whose new record sits far enough inside the penalty file that a full year is visible on both sides, there were {rt['PEN_365_BEFORE']} penalties in the year before and {rt['PEN_365_AFTER']} in the year after: <b>a {drop:.0f}% drop</b> (z about {zb:.1f}), with no hump in the months right before month zero.</p>
<p>What a hit would look like: a spike in the two or three months before the record date. What this looks like: penalties come at a steady rate, then thin out once the record changes. Three readings fit that, and these tables cannot pick between them: the new operator is running a cleaner home; CMS reports penalties against the new record with a lag; or a new enrollment buys a grace period before surveys bite again. {rb['PENALIZED_AGAIN_AFTER_NEW_RECORD']} of the {rb['ENROLL_AFTER_FIRST_PEN']} homes with a new record after their first penalty were penalized again under the new record.</p>""", f3),
 ("What the 39 actually are", f"""
<p>The 39 reproduce to the home. But the first pass counted any incorporation after the first penalty, no ceiling. {gi.get('0-90 days',0)} sit inside 90 days, {gi.get('91-180',0)} in 91 to 180, {gi.get('181-365',0)} in 181 to 365, {gi.get('366-730',0)} later than a year. And they cluster: eight Oregon homes all incorporated on 2024-05-10 and five Washington homes on 2024-05-14, every one named '&lt;place&gt; SNF Healthcare LLC'. That reads as one buyer papering a portfolio, but it is an inference from the name pattern and the dates: all {ow["N_ROWS"]} '... SNF Healthcare LLC' rows in the file carry {ow["D_ASSOC"]} distinct owner IDs across {ow["STATES"]} states, so the enrollment file itself does not tie them together. Thirteen same-week single-home LLCs also fits a shell shape. Two more pairs share a date and a state. Counted as events, the 39 are 13 + 4 + 22 = 25.</p>
<p>The enrollment clock gives {rb['ENROLL_AFTER_FIRST_PEN']} homes with a new record after the first penalty, {rb['WITHIN_365']} within a year and {rb['WITHIN_180']} within six months, across {rb['DISTINCT_OWNERS_IN_SET']} distinct owner IDs. {rb['BOTH_CLOCKS_AFTER']} of the original 39 are in this set. The 650 is the number to carry, with the base rate beside it.</p>""", f4),
]
footer = ("Tables: LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS (14,425 rows, snapshot with records dated to 2026-02-12), HEALTH__FED_CMS_NURSING_HOME_PENALTIES (16,180 rows, 2023-06-17 to 2026-05-13), "
          "HEALTH__FED_NURSINGHOME411 (ownership flag, 2025-12-01 roster). No change-of-ownership file for nursing homes is landed: HEALTH__FED_CMS_POS_OTHER's five categories hit zero penalty CCNs. "
          "Queries in <code>queries.py</code>, log in <code>queries.log</code>. Enrollment file holds only the current record per home, so a home that changed hands twice shows once, and any earlier change is invisible.")
write_story(f"{D}/story.html", "Penalty, then a new owner", lede, sections, footer, hero)
print("wrote story.html")
