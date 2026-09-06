"""Build story.html from data.json. Run from repo root with PYTHONPATH=reports/tier1_deep_dive_2026-09-05."""
import json
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from _shared.viz import PAL, TEXT2, base_fig, bar_style, write_story

HERE = Path(__file__).resolve().parent
D = json.load(open(HERE / "data.json"))
OWN, IND = "hospital-owned", "independent"
C = {OWN: PAL[0], IND: PAL[1]}

def rows(key, **f):
    return [r for r in D[key] if all(r.get(k) == v for k, v in f.items())]

# ---------- chart 1: missingness by volume band
bands = ["0 none", "1 <100", "2 100-249", "3 250-499", "4 500+"]
labels = ["no episode count", "under 100", "100-249", "250-499", "500+"]
fig1 = base_fig("Blank stars are a volume story, not an ownership story",
                "Share of agencies with no quality star, by Medicare episodes in the year. Hover for counts.")
for grp in (OWN, IND):
    rr = {r["BAND"]: r for r in rows("by_band", GRP=grp)}
    fig1.add_bar(name=grp, x=labels, y=[rr[b]["PCT_STAR_MISSING"] for b in bands], marker_color=C[grp],
                 customdata=[rr[b]["N"] for b in bands],
                 hovertemplate="%{x}<br>" + grp + ": %{y}% blank of %{customdata} agencies<extra></extra>",
                 text=[f"{rr[b]['PCT_STAR_MISSING']:.0f}%" for b in bands], textposition="outside", textfont=dict(color=TEXT2, size=12))
fig1.update_layout(barmode="group", yaxis_title="% with no star", yaxis_range=[0, 70])
bar_style(fig1)

# ---------- chart 2: star distribution, share of rated
stars = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
fig2 = base_fig("Hospital-owned agencies pile up at 3 stars; independents spread to 4 and 5",
                "Share of RATED agencies at each quality-of-patient-care star. Blanks excluded from both groups.")
for grp in (OWN, IND):
    rr = {r["STAR"]: r["N"] for r in rows("star_dist", GRP=grp)}
    tot = sum(rr.values())
    y = [100 * rr.get(s, 0) / tot for s in stars]
    fig2.add_bar(name=f"{grp} ({tot:,} rated)", x=[str(s) for s in stars], y=y, marker_color=C[grp],
                 customdata=[rr.get(s, 0) for s in stars],
                 hovertemplate="%{x} stars<br>" + grp + ": %{y:.1f}% (%{customdata} agencies)<extra></extra>")
own3 = 100 * {r["STAR"]: r["N"] for r in rows("star_dist", GRP=OWN)}[3.0] / sum(r["N"] for r in rows("star_dist", GRP=OWN))
fig2.add_annotation(x="3", y=own3, text=f"{own3:.0f}% of owned sit at 3", showarrow=True, arrowhead=0, ax=60, ay=-30, font=dict(size=12))
fig2.update_layout(barmode="group", yaxis_title="% of rated agencies")
bar_style(fig2)

# ---------- chart 3: cohort, four measures side by side
co = {r["GRP"]: r for r in D["cohort"]}
panels = [("Quality star, 1-5", "MEAN_STAR", "SD_STAR", "N_STAR", ".2f"),
          ("Spend ratio, 1 = national", "MEAN_SPEND", "SD_SPEND", "N_SPEND", ".3f"),
          ("Sent home, % (up = good)", "DTC", "SD_DTC", "N_STAR", ".1f"),
          ("Prev. hosp., % (down = good)", "PPH", "SD_PPH", "N_STAR", ".2f")]
fig3 = make_subplots(rows=1, cols=4, subplot_titles=[p[0] for p in panels], horizontal_spacing=0.08)
for i, (ttl, m, sd, n, fmt) in enumerate(panels, start=1):
    for grp in (OWN, IND):
        v = co[grp][m]
        fig3.add_bar(x=["owned" if grp == OWN else "indep."], y=[v], marker_color=C[grp], name=grp, showlegend=(i == 1),
                     text=[format(v, fmt)], textposition="outside", textfont=dict(color=TEXT2, size=12),
                     hovertemplate=f"{grp}<br>{ttl}: %{{y:{fmt}}}<br>n={co[grp][n]:,}, sd={co[grp][sd]}<extra></extra>", row=1, col=i)
    lo = min(co[g][m] for g in (OWN, IND)); hi = max(co[g][m] for g in (OWN, IND))
    pad = (hi - lo) * 3 or hi * 0.1
    fig3.update_yaxes(range=[max(0, lo - pad), hi + pad], row=1, col=i)
fig3.update_layout(title=dict(text="<b>At 100+ episodes: 3% pricier per agency, tenth-star lower, more sent home</b>"
                              f"<br><span style='font-size:13px;color:{TEXT2}'>314 owned vs 4,452 independent with 100+ episodes (313 vs 4,158 rated). Y-axes zoomed to the gap; hover for n and spread.</span>"),
                   height=480, bargap=0.25)
fig3.update_annotations(font_size=11)
fig3.update_xaxes(tickangle=0)
bar_style(fig3)

# ---------- chart 4: states dumbbell
st = [r for r in D["states"] if r["OWNED_N"] >= 10 and r["OWNED_STAR"] is not None]
st.sort(key=lambda r: r["OWNED_STAR"] - r["IND_STAR"])
fig4 = base_fig("The star gap flips by state: owned wins in California, loses a full star in Alabama",
                "Mean quality star, states with 10+ hospital-owned agencies. Line = the gap. Hover for counts, blanks and spend.", height=620)
for r in st:
    fig4.add_scatter(x=[r["OWNED_STAR"], r["IND_STAR"]], y=[r["STATE"], r["STATE"]], mode="lines",
                     line=dict(color="#c9c8c4", width=2), showlegend=False, hoverinfo="skip")
for grp, col, sk, nk, mk, spk in ((OWN, "OWNED_STAR", "OWNED_STAR", "OWNED_N", "OWNED_MISS", "OWNED_SPEND"),
                                  (IND, "IND_STAR", "IND_STAR", "IND_N", "IND_MISS", "IND_SPEND")):
    fig4.add_scatter(name=grp, x=[r[sk] for r in st], y=[r["STATE"] for r in st], mode="markers",
                     marker=dict(color=C[grp], size=11, line=dict(color="#fcfcfb", width=2)),
                     customdata=[[r[nk], r[mk], r[spk]] for r in st],
                     hovertemplate="%{y} " + grp + "<br>mean star %{x:.2f}<br>%{customdata[0]} agencies, %{customdata[1]}% no star<br>spend vs national %{customdata[2]:.3f}<extra></extra>")
fig4.update_layout(xaxis_title="mean quality star", xaxis_range=[2.5, 4.2], yaxis=dict(showgrid=False))

# ---------- prose
bg = {r["GRP"]: r for r in D["by_group"]}
own_n, ind_n, np_n = bg[OWN]["N"], bg[IND]["N"], bg["not in PECOS"]["N"]
lede = ("Hospitals that run their own home health agency: do their agencies score worse and cost Medicare more? "
        "Two CMS files answer part of it. Care Compare rates every home health agency on a 1-to-5 quality star and a spend-per-episode ratio. "
        "PECOS, the Medicare enrollment roster, says which organisation enrolled each agency. Where that organisation also enrolled a hospital, the agency is hospital-owned. "
        f"That gives {own_n} hospital-owned agencies, {ind_n:,} independents, and {np_n:,} agencies with no enrollment row at all. "
        "A CCN is the Medicare certification number every facility carries; it is the key that joins the two files.")
hero = [(f"{own_n}", "hospital-owned agencies"), ("5.2% vs 32.6%", "blank stars, owned vs independent"),
        ("3.06 vs 3.17", "mean star, 100+ episode cohort"), ("3% / 1.9%", "spend gap per agency / per episode, same cohort")]

p1 = (f"<p>The first pass said 37% of independent agencies have no star against 5% of hospital-owned. That reproduces, but only if the {np_n:,} agencies with no PECOS row are counted as independent. Split out, they are 78% blank. True independents are 33% blank.</p>"
      "<p>Every blank star carries the same footnote: too few patient episodes to report. So the blank is small volume, and the chart shows it. Under 100 episodes, 29% of owned and 56% of independent are blank; at 250 and up, both sit under 5%.</p>"
      "<p>Hospital-owned agencies are older (median certification 41 years ago vs 16) and bigger (median 316 episodes vs 220). They have stars because they have patients. The missingness is not hiding bad owned agencies; it is hiding small independents, whose rated survivors skew high.</p>")
lh = {r["GRP"]: r for r in D["star_lowhigh"]}
p2 = (f"<p>Among rated agencies, {lh[OWN]['PCT_HIGH']}% of hospital-owned reach 4 stars or better against {lh[IND]['PCT_HIGH']}% of independents. But owned also has fewer at the bottom: {lh[OWN]['PCT_LOW']}% at 2 stars or under vs {lh[IND]['PCT_LOW']}%.</p>"
      "<p>Owned agencies are a narrow middle. Independents are wide at both ends. Mean star: 3.16 owned, 3.26 independent. Median: 3.0 vs 3.5.</p>"
      "<p>Read it as: the hospital agency is rarely great and rarely terrible.</p>")
p3 = ("<p>The fair test is agencies with at least 100 Medicare episodes. Blanks shrink but do not vanish: 1 owned and 294 independents in the cohort still have no star, and the blank independents are the worst ones (59.7% discharged to community vs 79.6% for the rated). So the independent star flatters, and the gap below is an upper bound.</p>"
      "<p><b>Cost:</b> per agency, owned spends 0.996 of the national per-episode figure, independent 0.965; a 3.1-point gap, about 4 standard errors. Weighted by episodes it is 0.9945 vs 0.9755, 1.9 points. The gap lives in the small agencies: 6.2 points at 100-249 episodes, 2.9 at 250-499, 0.7 at 500-998. The episode column tops out at 998, so that last band is capped.</p>"
      "<p><b>Star:</b> 3.06 vs 3.17 on 313 vs 4,158 rated, a tenth of a star, about 2 standard errors. Median 3.0 for both. Thin.</p>"
      "<p><b>Outcomes cut the other way.</b> Owned agencies discharge 83.7% of patients back to the community vs 78.6% (8 standard errors), and have a lower preventable-hospitalization rate, 10.6% vs 11.0%. The star is a composite of process and functional measures; the claims-based outcomes favour the hospital agency.</p>"
      "<p>Restricting to for-profit agencies only (78 owned vs 3,727 independent) gives the same numbers: 3.05 vs 3.17 stars, 0.996 vs 0.964 spend. Tax status is not the driver.</p>"
      "<p>Not in the warehouse: the patient survey star (HHCAHPS). Searched every table name for HHCAHPS, PATIENT_SURVEY and HOME_HEALTH. Only the two files above exist.</p>")
p4 = ("<p>The national tenth-of-a-star is an average of states pulling opposite ways.</p>"
      "<p>Alabama: owned 2.92 vs independent 4.01. Arkansas: 2.76 vs 3.62. Nebraska: 2.86 vs 3.56. Louisiana: 3.08 vs 3.76. In the rural South and Plains the hospital agency is the low scorer by a lot.</p>"
      "<p>California flips it: owned 3.37 vs 3.16, and owned spends 0.836 vs 0.943, the cheapest owned group anywhere. Indiana, Illinois, Michigan, Virginia, Missouri also favour owned.</p>"
      "<p>Small counts: most states have 10 to 43 owned agencies. Treat single-state gaps as leads.</p>")

owners = D["owners"][0]
footer = (f"Tables: LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH (12,392 rows, CCN unique), HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS (11,508), HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS (9,175). "
          f"Hospital-owned = HHA enrollment ASSOCIATE_ID also appears on a hospital enrollment: {owners['SYSTEMS']} organisations, {owners['HHA']} agencies, {D['owned_stripped'][0]['HHA']} after stripping the 95 branch suffixes, 519 of them in Care Compare. "
          "Second check: 140 of 519 owned carry HOSPITAL / MEDICAL CENTER / HEALTH SYSTEM in their name vs 77 of 10,694 independents, so the flag is real but may undercount owned agencies enrolled under a separate organisation. "
          "Snapshot, no time series. Every query in <code>queries.py</code>, log in <code>queries.log</code>. Python door only.")

write_story(HERE / "story.html", "Hospital-owned home health: a narrow middle that costs a little more",
            lede, [("The blanks are small agencies, not owned ones", p1, fig1),
                   ("Owned is the narrow middle of the star scale", p2, fig2),
                   ("On equal footing: pricier, a hair lower star, better outcomes", p3, fig3),
                   ("The states disagree with each other", p4, fig4)], footer, hero=hero)
print("wrote story.html")
