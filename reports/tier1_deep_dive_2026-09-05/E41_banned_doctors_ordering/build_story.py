"""Build story.html for E41 from results.json (written by queries.py). No warehouse calls."""
from __future__ import annotations
import json
from pathlib import Path
import plotly.graph_objects as go
from _shared.viz import PAL, STATUS, TEXT2, base_fig, bar_style, write_story

HERE = Path(__file__).resolve().parent
R = json.loads((HERE / "results.json").read_text())
LOAD = "2026-08-05"
LEIE_LOAD = "2026-08-27"

TYPE_LABEL = {
    "1128a1": "1128(a)(1) program crime, mandatory",
    "1128a2": "1128(a)(2) patient abuse, mandatory",
    "1128a3": "1128(a)(3) felony fraud, mandatory",
    "1128a4": "1128(a)(4) felony drugs, mandatory",
    "1128b1": "1128(b)(1) misdemeanor fraud",
    "1128b4": "1128(b)(4) license revoked",
    "1128b7": "1128(b)(7) kickbacks / fraud",
    "1128b14": "1128(b)(14) loan default",
}

m = R["matches"]
by = R["by_year"]
n_match = len(m)
old = [x for x in m if x["EXCLUSION_DATE"] < "2025-01-01"]
before_load = [x for x in m if x["EXCLUSION_DATE"] < LOAD]
after_load = [x for x in m if x["EXCLUSION_DATE"] >= LOAD]
waived = [x for x in m if x["WVRSTATE"]]
dme = R["dme_refer"]
dme_paid = sum(float(x["PAID"]) for x in dme)

# --- chart 1: rate by exclusion year -----------------------------------------
y25 = next(x for x in by if x["Y"] == 2025)
y26 = next(x for x in by if x["Y"] == 2026)
fig1 = base_fig(
    f"CMS scrubs the file: 0 of {y25['EXCLUDED_NPIS']} doctors banned in 2025 remain, {y26['IN_ORDERING']} of {y26['EXCLUDED_NPIS']} banned in 2026 do",
    "Excluded NPIs still on the Order and Referring file, by year of first exclusion. Hover for the denominator.")
fig1.add_trace(go.Bar(
    x=[str(x["Y"]) for x in by], y=[x["IN_ORDERING"] for x in by], name="still on the ordering file",
    marker_color=[STATUS["critical"] if x["Y"] < 2025 else PAL[0] for x in by],
    customdata=[[x["EXCLUDED_NPIS"], x["NPPES_ACTIVE"]] for x in by],
    hovertemplate="%{x}: %{y} still listed<br>%{customdata[0]} excluded NPIs, %{customdata[1]} still active in NPPES<extra></extra>",
    text=[x["IN_ORDERING"] if x["IN_ORDERING"] else "" for x in by], textposition="outside"))
fig1.update_layout(yaxis_title="excluded NPIs still on the file", xaxis_title="year of first exclusion", showlegend=False)
fig1.add_annotation(x="2015", y=1, text="red = banned before 2025, the 7 that should not be there", showarrow=True, ay=-60, ax=60,
                    font=dict(size=12, color=TEXT2))
bar_style(fig1)

# --- chart 2: the 38 on a timeline -------------------------------------------
fig2 = base_fig(
    f"{len(old)} of {n_match} were banned before 2025 — the other {n_match - len(old)} are file lag",
    f"Each dot is one excluded clinician on the ordering file. Dashed lines: ordering file landed {LOAD}, exclusion list landed {LEIE_LOAD}.",
    height=420)
groups = [
    ("banned before 2025", old, STATUS["critical"]),
    ("banned 2026, before the ordering file landed", [x for x in before_load if x not in old], PAL[3]),
    ("banned after the ordering file landed", after_load, PAL[0]),
]
import collections
for name, rows, color in groups:
    cnt = collections.Counter(x["EXCLUSION_DATE"] for x in rows)
    seen = collections.Counter()
    ys = []
    for x in rows:
        seen[x["EXCLUSION_DATE"]] += 1
        ys.append(seen[x["EXCLUSION_DATE"]])
    fig2.add_trace(go.Scatter(
        x=[x["EXCLUSION_DATE"] for x in rows], y=ys, mode="markers", name=name,
        marker=dict(size=12, color=color, line=dict(width=0)),
        customdata=[[x["LAST_NAME"], x["SPECIALTY"].strip().rstrip(" ("), x["LEIE_STATE"], TYPE_LABEL.get(x["EXCLUSION_TYPE"], x["EXCLUSION_TYPE"]),
                     x["WVRSTATE"] or "none"] for x in rows],
        hovertemplate="%{customdata[0]} — %{customdata[1]}, %{customdata[2]}<br>excluded %{x}<br>%{customdata[3]}<br>waiver: %{customdata[4]}<extra></extra>"))
for d, lbl in [(LOAD, "ordering file landed"), (LEIE_LOAD, "exclusion list landed")]:
    fig2.add_vline(x=d, line_dash="dash", line_color=TEXT2)
    fig2.add_annotation(x=d, y=13, text=lbl, showarrow=False, font=dict(size=11, color=TEXT2), xanchor="right" if d == LOAD else "left")
fig2.update_layout(yaxis=dict(title="clinicians on that date", range=[0, 14]), xaxis_title="exclusion date")
for x in old:
    fig2.add_annotation(x=x["EXCLUSION_DATE"], y=1, text=x["LAST_NAME"].title() + (" (waiver)" if x["WVRSTATE"] else ""),
                        showarrow=False, yshift=16, font=dict(size=11))

# --- chart 3: exclusion type mix ---------------------------------------------
tm = [x for x in R["type_mix"] if x["ALL_REAL_NPIS"] >= 40]
tot_all = R["leie_profile"][0]["DISTINCT_NPI"]  # 8,660 distinct; summing across types double-counts NPIs with two exclusions
b4 = next(x for x in R["type_mix"] if x["EXCLUSION_TYPE"] == "1128b4")
fig3 = base_fig(
    f"License revocations are {b4['IN_ORDERING']} of the {n_match} matches ({b4['IN_ORDERING']/n_match:.0%}) but {b4['ALL_REAL_NPIS']/tot_all:.0%} of the whole list",
    "Share of NPIs by exclusion reason: the full exclusion list vs the ones still on the ordering file.")
labels = [TYPE_LABEL.get(x["EXCLUSION_TYPE"], x["EXCLUSION_TYPE"]) for x in tm]
fig3.add_trace(go.Bar(name=f"whole exclusion list ({tot_all:,} real NPIs)", x=labels, y=[x["ALL_REAL_NPIS"] / tot_all for x in tm],
                      marker_color=PAL[0], customdata=[x["ALL_REAL_NPIS"] for x in tm],
                      hovertemplate="%{x}<br>%{y:.1%} of the list (%{customdata:,} NPIs)<extra></extra>"))
fig3.add_trace(go.Bar(name=f"still on the ordering file ({n_match})", x=labels, y=[x["IN_ORDERING"] / n_match for x in tm],
                      marker_color=PAL[1], customdata=[x["IN_ORDERING"] for x in tm],
                      hovertemplate="%{x}<br>%{y:.1%} of the matches (%{customdata} NPIs)<extra></extra>"))
fig3.update_layout(barmode="group", yaxis=dict(tickformat=".0%", title="share of NPIs"), xaxis=dict(tickangle=-20))
bar_style(fig3)

# --- chart 4: what they can order --------------------------------------------
cats = [("DME", "medical equipment (DME)"), ("PMD", "power wheelchairs (PMD)"), ("PARTB", "Part B tests and visits"),
        ("HHA", "home health"), ("HOSPICE", "hospice")]
cnt = {c: sum(1 for x in m if x[c] == "Y") for c, _ in cats}
cnt_old = {c: sum(1 for x in old if x[c] == "Y") for c, _ in cats}
fig4 = base_fig(
    f"All {n_match} can order medical equipment; {cnt['HOSPICE']} can certify hospice",
    "How many of the matched clinicians the file marks eligible, per ordering category.", height=400)
fig4.add_trace(go.Bar(name=f"all {n_match} matches", y=[l for _, l in cats], x=[cnt[c] for c, _ in cats], orientation="h",
                      marker_color=PAL[0], text=[cnt[c] for c, _ in cats], textposition="outside",
                      hovertemplate="%{y}: %{x} of " + str(n_match) + "<extra></extra>"))
fig4.add_trace(go.Bar(name=f"the {len(old)} banned before 2025", y=[l for _, l in cats], x=[cnt_old[c] for c, _ in cats], orientation="h",
                      marker_color=STATUS["critical"], text=[cnt_old[c] for c, _ in cats], textposition="outside",
                      hovertemplate="%{y}: %{x} of " + str(len(old)) + "<extra></extra>"))
fig4.update_layout(barmode="group", xaxis=dict(range=[0, n_match + 6], title="clinicians marked eligible"), yaxis=dict(autorange="reversed"))
bar_style(fig4)

# --- prose ---------------------------------------------------------------------
def row_table(rows):
    h = "<table style='font-size:13px;border-collapse:collapse'><tr><th align=left>who</th><th align=left>banned</th><th align=left>why</th><th align=left>waiver</th><th align=left>can order</th></tr>"
    for x in rows:
        can = ", ".join(k for k in ["PARTB", "DME", "HHA", "PMD", "HOSPICE"] if x[k] == "Y")
        h += (f"<tr><td>{x['LAST_NAME'].title()}, {x['SPECIALTY'].strip().rstrip(' (').title()}, {x['LEIE_STATE']}</td>"
              f"<td>{x['EXCLUSION_DATE']}</td><td>{TYPE_LABEL.get(x['EXCLUSION_TYPE'], x['EXCLUSION_TYPE'])}</td>"
              f"<td>{x['WVRSTATE'] or '—'}</td><td>{can}</td></tr>")
    return h + "</table>"

lede = ("An NPI is the ten-digit number every clinician bills Medicare under. The OIG exclusion list (LEIE) names people banned from federal health programs; "
        "CMS's Order and Referring file names every NPI allowed to order tests, equipment, home health and hospice for Medicare patients. "
        "A name on both is a banned clinician the system still lets order. "
        f"There are {n_match}. Most are file lag. Seven are not.")

s1 = (f"<p>The exclusion list holds 83,747 rows but only 8,660 real NPIs — 74,908 rows carry the sentinel <code>0000000000</code>, which the mart blanks out. "
      f"Those 8,660 were joined to the 2,018,350 distinct NPIs on the ordering file. <b>{n_match} match</b>, both on the marts and again on the raw landing tables.</p><p><b>Limit:</b> only 8,839 of 83,747 exclusion rows (10.6%) carry a usable NPI. Everything below is about NPI-bearing exclusions; every count is a floor.</p>"
      f"<p>By year of exclusion the picture is flat zero from 2010 through 2024 — one or three a year at most — then <b>0 of {y25['EXCLUDED_NPIS']}</b> for 2025 and "
      f"<b>{y26['IN_ORDERING']} of {y26['EXCLUDED_NPIS']}</b> for 2026. The denominator is not deactivated NPIs: {y25['NPPES_ACTIVE']} of the 2025 cohort are still live in NPPES and none are on the file. "
      f"A hit here means CMS has not yet pulled the name; a miss means it has. The 2025 zero says CMS does pull them, within months.</p>")

s2 = (f"<p>The ordering file landed {LOAD}; it carries no date of its own, no year column, empty registry row, so the load stamp is the only clock. "
      f"The exclusion list landed {LEIE_LOAD} with exclusions through 2026-08-20.</p>"
      f"<p><b>{len(after_load)}</b> of the {n_match} were excluded 2026-08-20, after the ordering file was cut — they cannot be a finding. "
      f"<b>{len(before_load) - len(old)}</b> were excluded February to July 2026, one to six months before the load — consistent with the lag the 2025 zero implies. "
      f"<b>{len(old)}</b> were excluded before 2025, oldest 2015; the lag story does not cover them.</p>"
      f"<p>Reinstatement check: <code>REINDATE</code> is <code>00000000</code> on all 83,842 landing rows. OIG drops reinstated people from the file rather than dating them, so anyone on the list is still excluded as of the file. "
      f"Waiver check: <code>WAIVERDATE</code>/<code>WVRSTATE</code> carries a dated waiver on 3 rows in the whole list (a fourth has a state and no date) and <b>{len(waived)} of the 3 are among the 7</b> — "
      + ", ".join(f"{x['LAST_NAME'].title()} ({x['WVRSTATE']}, waiver dated {x['WAIVERDATE'][:4]}-{x['WAIVERDATE'][4:6]}-{x['WAIVERDATE'][6:]})" for x in waived)
      + ". A waiver lets an excluded clinician keep serving a state's program; those two are legal, not a loophole.</p>"
      + "<p>The seven:</p>" + row_table(old))

s3 = (f"<p>Exclusion type is the OIG statute. The (a) codes are mandatory bans for convictions; (b) codes are discretionary — (b)(4) is a state license revocation. "
      f"On the whole list (b)(4) is {b4['ALL_REAL_NPIS']/tot_all:.0%} of real NPIs; among the {n_match} matches it is {b4['IN_ORDERING']/n_match:.0%}. "
      f"That fits the lag story: license-based exclusions are the fastest-growing type in 2026 and the newest names are the ones not yet pulled.</p>"
      f"<p>Among the 7 old ones the mix flips: 2 program-crime convictions (Miranda 2015, Sicuro 2024), 2 felony drug convictions (Patel 2020, Fraser 2021), 3 kickback/fraud (b)(7). All seven are mandatory-ban or fraud codes, none is license paperwork.</p>"
      f"<p>State: the 7 sit in TX, OR, NE, IL, MO, CA, CT — no cluster. Across all 38, FL leads with 8 (834 excluded NPIs in FL on the list), then TX and CA with 4 each. "
      f"10 of the 38 do not match state between the exclusion record and NPPES — 9 practise elsewhere, 1 (Adams, NC) has a blank NPPES record because the NPI was deactivated 2025-07-29, and it is still on the ordering file.</p>")

s4 = (f"<p>The file has five yes/no columns. <code>DME</code> is Y on 2,018,350 of 2,018,354 rows — a constant, it means nothing on its own. "
      f"Hospice (1,140,374 Y) and home health (1,689,678 Y) are the selective ones. "
      f"{cnt['HOSPICE']} of the {n_match} can certify hospice; {cnt_old['HOSPICE']} of the 7 old ones can, including Miranda (2015) and Fraser (2021).</p>"
      f"<p>Did they order? The Medicare DME-by-referrer file (381,228 referrers, one data year, no year column, vintage unproven) lists <b>{len(dme)} of the {n_match}</b> as paid referrers, "
      f"${dme_paid:,.0f} in Medicare payments on their orders combined. Miranda is one: 1,343 supplier services, ${float(dme[0]['PAID']):,.0f} paid, eight years after his exclusion — and he holds a Texas waiver dated the same day as the ban, so that money is likely legal. "
      f"The other 8 paid referrers were all excluded in 2026, so their payments predate the ban.</p>")

footer = (f"Tables: <code>{'LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE'}</code> (83,747 rows, landed {LEIE_LOAD}), "
          f"<code>HEALTH__FED_CMS_ORDER_AND_REFERRING</code> (2,018,354 rows, landed {LOAD}), <code>HEALTH__FED_CMS_NPPES</code>, "
          f"<code>HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER</code>. Every query in <code>queries.py</code>, log in <code>queries.log</code>. "
          "Traps hit: LEIE mart <code>_INGESTED_AT</code> is epoch microseconds cast as a timestamp (year 56,656,460) — use the landing column; "
          "LEIE mart blanks the sentinel NPI (0 rows read '0000000000', 74,908 read empty); ordering-file DME flag is a constant.")

write_story(HERE / "story.html", "Banned doctors still allowed to order", lede,
            sections=[
                ("CMS pulls banned doctors — 2025's cohort is gone", s1, fig1),
                ("Lag explains 31; 7 are real", s2, fig2),
                ("Why they were banned", s3, fig3),
                ("What they can order, and what they did", s4, fig4),
            ],
            footer=footer,
            hero=[(n_match, "banned clinicians on the ordering file"), (len(old), "banned before 2025"),
                  (len(waived), "of those 7 hold an OIG waiver"), (len(dme), "show up as paid DME referrers")])
print("wrote", HERE / "story.html")
