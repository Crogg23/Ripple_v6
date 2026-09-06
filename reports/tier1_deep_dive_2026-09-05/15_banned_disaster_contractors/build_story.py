"""Build story.html from the saved query results. No warehouse calls."""
import json, datetime as dt
import plotly.graph_objects as go
from _shared.viz import PAL, base_fig, bar_style, write_story
D = "reports/tier1_deep_dive_2026-09-05/15_banned_disaster_contractors"
L = lambda n: json.load(open(f"{D}/{n}.json"))
f = lambda x: float(x or 0)
tl = L("company_timeline"); ws = L("window_summary"); rows = L("in_window_rows"); m = L("matches")

# ---- chart 1: the number shrinks as the question gets honest
inwin_pos = sum(f(r["OBLIG_POS"]) for r in ws if r["IN_WINDOW"] == 1)
inwin_net = sum(f(r["OBLIG"]) for r in ws if r["IN_WINDOW"] == 1)
labels = ["First pass: award ceilings,\nFEMA, untimed", "Money actually obligated,\nall disaster work, untimed", "Obligated INSIDE\nthe ban window (gross)", "Obligated inside the\nban window (net of clawbacks)"]
vals = [169_247_002.55, 41_062_973.47, inwin_pos, inwin_net]
fig1 = base_fig("The $169M is $15K once you ask when", "Same 26-to-56 companies; each bar asks a stricter question of the same rows")
fig1.add_trace(go.Bar(x=[l.replace("\n", "<br>") for l in labels], y=vals, marker_color=[PAL[0], PAL[0], PAL[7], PAL[7]],
    text=[f"${v/1e6:,.1f}M" if abs(v) >= 1e6 else f"${v:,.0f}" for v in vals], textposition="outside",
    hovertemplate="%{x}<br>$%{y:,.0f}<extra></extra>"))
fig1.update_yaxes(title="dollars (federal action obligation)", tickprefix="$", tickformat="~s")
bar_style(fig1)

# ---- chart 2: award span vs ban start, one line per company
tl2 = sorted([r for r in tl if r["FIRST_ACT_ON"]], key=lambda r: r["FIRST_ACT_ON"])
fig2 = base_fig("Almost every award came BEFORE the ban started", "One row per banned company: blue span = disaster awards, red diamond = exclusion start; " + str(sum(1 for r in tl if r["ANY_AFTER"]==1)) + " rows have anything after the diamond", height=max(600, 16 * len(tl2) + 160))
ys = [f"{r['RN'][:34]}" for r in tl2]
for i, r in enumerate(tl2):
    fig2.add_trace(go.Scatter(x=[r["FIRST_AWARD"], r["LAST_AWARD"]], y=[ys[i], ys[i]], mode="lines+markers", line=dict(color=PAL[0], width=3), marker=dict(size=6),
        showlegend=(i == 0), name="disaster awards (first to last)", hovertemplate=f"{r['RN']}<br>awards {r['FIRST_AWARD']} to {r['LAST_AWARD']}<br>${f(r['OBLIG']):,.0f} obligated<extra></extra>"))
fig2.add_trace(go.Scatter(x=[r["FIRST_ACT_ON"] for r in tl2], y=ys, mode="markers", marker=dict(color=PAL[7], size=9, symbol="diamond"), name="exclusion starts",
    hovertemplate="%{y}<br>banned from %{x}<extra></extra>"))
fig2.update_xaxes(range=["2006-06-01", "2027-01-01"], title="year")
fig2.update_yaxes(autorange="reversed", tickfont=dict(size=10))
fig2.update_layout(margin=dict(l=240))

# ---- chart 3: Tribute Contracting, the one big number, obligated then clawed back
tr = sorted([r for r in m if r["RN"] == "TRIBUTE CONTRACTING, LLC" and r["HOW"] == "UEI"], key=lambda r: r["ACT"])
cum, xs, ysum = 0, [], []
for r in tr:
    cum += f(r["OBLIG"]); xs.append(r["ACT"]); ysum.append(cum)
fig3 = base_fig("Tribute Contracting: $156M obligated for Puerto Rico meals, $155.7M taken back, banned 7 years later",
                "Running total of FEMA obligations on the Hurricane Maria meals contract; the exclusion did not start until 2025")
fig3.add_trace(go.Scatter(x=xs, y=ysum, mode="lines+markers", line=dict(color=PAL[0], shape="hv"), name="cumulative obligation",
    hovertemplate="%{x}<br>running total $%{y:,.0f}<extra></extra>"))
fig3.add_vline(x=dt.datetime(2025, 3, 26).timestamp() * 1000, line_color=PAL[7], line_dash="dash")
fig3.add_annotation(x="2025-03-26", y=max(ysum) * 0.6, text="excluded 2025-03-26", showarrow=False, font=dict(color=PAL[7]), xanchor="right")
fig3.update_yaxes(tickprefix="$", tickformat="~s", title="running obligation")
fig3.update_xaxes(range=["2017-06-01", "2026-09-01"])

# ---- prose
ncos = len({r["UEI"] for r in tl})
after = [r for r in tl if r["ANY_AFTER"] == 1]
hero = [("$169M", "first-pass number (award ceilings, FEMA only, untimed)"), ("$41M", "actually obligated, untimed, 56 companies"),
        (f"${inwin_pos:,.0f}", "obligated inside a ban window"), (f"-${abs(inwin_net):,.0f}", "net inside ban windows (clawbacks)")]
lede = ("Are companies banned from federal contracting still getting disaster-relief money? The first pass said 26 companies and $169 million. "
        "That number is real but it answers a different question: it sums award ceilings for companies that were banned <i>at some point</i>, with no check "
        "on whether the ban had started when the money moved. Put the dates side by side and the answer is: no, not in any amount that matters.")
s1 = (f"<p>A SAM exclusion is the government's do-not-hire list: a company on it cannot get new federal contracts from the day the exclusion starts until it ends. "
      f"We took every contract transaction in USAspending that was awarded by FEMA or carried a disaster keyword (hurricane, wildfire, debris removal, and so on), "
      f"and matched the recipient to the exclusion list by its UEI (the government's company ID), its CAGE code, or its exact name. That gives {ncos} recipients: 56 by ID, 5 more by exact name only.</p>"
      f"<p>The first pass reproduces exactly: 26 companies, $169,247,003, if you take FEMA only, join on UEI, and sum each award's <i>current total value</i> once per award. "
      f"Current total value is a ceiling, not money spent. Sum what was actually obligated and it is $41M across all disaster agencies, $22M for FEMA alone.</p>"
      f"<p>Then ask when. Only 20 transactions out of 349 fall on or after the company's exclusion start. They net to <b>-${abs(inwin_net):,.0f}</b>: the government was pulling money back, not paying. "
      f"Gross positive money inside a ban window is <b>${inwin_pos:,.0f}</b>, and $3,096 of that is a 2007 VA apron purchase matched to a 1998 HHS exclusion on a same-named firm with a different ID, so it does not count.</p>")
s2 = (f"<p>Each row is one company. The blue span runs from its first disaster award to its last. The red diamond is the day its exclusion started. "
      f"For {ncos - len(after)} of {ncos} companies the diamond sits to the right of the span: the awards ended, then years later the company got banned.</p>"
      f"<p>The typical gap is years. Blackhawk Ventures' last award was 2012; banned 2021. Odyssey International's last was 2020; banned 2023. Intellipeak and Worldwide Equipment were banned in August 2026, weeks before this data was pulled.</p>"
      f"<p>The {len(after)} rows with activity after the diamond are closeouts and de-obligations, plus one real exception: Anderson Court Reporting, banned by the Department of Labor on 2024-07-19, got one FEMA purchase order for court transcripts (70FA4024P00000053, awarded 2024-08-29, modified 2024-09-25) totalling $12,232. That is the whole finding, and it is a transcription vendor, not disaster relief in any meaningful sense.</p>")
s3 = ("<p>The company behind most of the first-pass dollars is Tribute Contracting, the one-person firm FEMA hired in October 2017 to deliver 30 million meals to Puerto Rico after Hurricane Maria. "
      "USAspending shows $155,982,000 obligated on 2017-10-03, then -$85,982,000 in March 2018, -$64,745,000 in October 2018, and -$5,000,000 at closeout in 2019. Net obligation on the award: $255,000, which is what FEMA says it paid for the roughly 50,000 meals delivered.</p>"
      "<p>The 'current total value' the first pass summed on this award is $155,982,000 (award key CONT_AWD_70FB7018C00000001; the five rows carry $255K, $155.98M, $70M, $5.255M, $255K), which is 92% of the $169M scare number. And the exclusion did not start until 2025-03-26, more than seven years after the award. "
      "This is the shape of every big row here: the ban came after the failure, not before the money.</p>")
foot = ("Sources: LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FULL_R2 (93.2M contract transactions, 2006-10-01 to 2026-08-22) and "
        "LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS (168,328 exclusion records, 35,197 firms). Disaster slice = awarding sub-agency FEMA, or a disaster keyword in the transaction description "
        "(210,751 FEMA rows plus ~110K keyword rows). Match on UEI, CAGE, or exact upper-cased name; individuals excluded. In-window = action date between exclusion activation and termination (open-ended when 'Indefinite'). "
        "Every query is in <code>queries.py</code>, results in <code>queries.log</code>.")
write_story(f"{D}/story.html", "Banned contractors and disaster money", lede,
            [("Ask when, and $169M becomes $15K", s1, fig1), ("Banned after the work, not before", s2, fig2), ("The Puerto Rico meals contract", s3, fig3)], foot, hero=hero)
print("wrote story.html")
