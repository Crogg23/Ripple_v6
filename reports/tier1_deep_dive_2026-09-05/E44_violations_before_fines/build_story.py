"""Build story.html from results.json. No warehouse calls here.
Run from repo root: PYTHONPATH=reports/tier1_deep_dive_2026-09-05 python3 reports/tier1_deep_dive_2026-09-05/E44_violations_before_fines/build_story.py
"""
import json, statistics as st
import plotly.graph_objects as go
from _shared.viz import PAL, base_fig, bar_style, write_story

D = "reports/tier1_deep_dive_2026-09-05/E44_violations_before_fines"
R = json.load(open(f"{D}/results.json"))
BRIA, NAT = PAL[1], PAL[0]     # orange = Bria, blue = national, fixed everywhere

def series(key, grp):
    return [r for r in R[key] if r["GRP"] == grp]

def roll3(xs):
    out = []
    for i in range(len(xs)):
        w = xs[max(0, i - 2):i + 1]
        out.append(sum(w) / len(w))
    return out

months = [r["MO"][:7] for r in series("monthly", "bria")]

# ---------------- chart 1: deficiencies per home per month ----------------
fig1 = base_fig("Bria's homes get cited 2 to 3 times as often as the average home, every month",
                "Deficiencies per home per month, 3-month rolling mean. Denominator = homes whose retained record had started by that month.")
for grp, col, name in (("national", NAT, "National (all other homes)"), ("bria", BRIA, "Bria Health Services (15 homes)")):
    s = series("monthly", grp)
    raw = [r["DEFS"] / r["HOMES"] for r in s]
    fig1.add_trace(go.Scatter(x=months, y=roll3(raw), mode="lines", name=name, line=dict(color=col, width=3),
                              customdata=[[r["DEFS"], r["HOMES"], v] for r, v in zip(s, raw)],
                              hovertemplate="%{x}<br>%{y:.2f} per home (3-mo)<br>raw %{customdata[2]:.2f} = %{customdata[0]} citations / %{customdata[1]} homes<extra>" + name + "</extra>"))
fig1.update_layout(yaxis_title="citations per home per month", xaxis=dict(tickvals=[m for m in months if m.endswith("-01") or m.endswith("-07")]))
fig1.add_annotation(x="2025-10", y=0.2, text="Oct 2025: surveys nationally<br>drop to a quarter of normal", showarrow=True, arrowhead=0, ax=-80, ay=-60, font=dict(size=12))

# ---------------- chart 2: severity letters by year ----------------
order = [("B-C", ["B", "C"]), ("D", ["D"]), ("E", ["E"]), ("F", ["F"]), ("G-I", ["G", "H", "I"]), ("J-L", ["J", "K", "L"])]
cols = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", PAL[3], PAL[7]]
fig2 = base_fig("One in three Bria citations in 2025 was actual harm; nationally it is one in sixteen",
                "Share of citations by scope-severity letter. G and up = a resident was harmed. J-L = immediate jeopardy.")
labels = []
for grp, nm in (("national", "National"), ("bria", "Bria")):
    for yr in (2023, 2024, 2025):
        labels.append(f"{nm} {yr}")
for (lab, letters), col in zip(order, cols):
    ys, hov = [], []
    for grp in ("national", "bria"):
        for yr in (2023, 2024, 2025):
            rows = [r for r in R["sev_year"] if r["GRP"] == grp and r["YR"] == yr]
            tot = sum(r["N"] for r in rows)
            n = sum(r["N"] for r in rows if r["SEV"] in letters)
            ys.append(100 * n / tot); hov.append(f"{n:,} of {tot:,}")
    fig2.add_trace(go.Bar(x=labels, y=ys, name=lab, marker_color=col, customdata=hov,
                          text=[f"{y:.1f}%" if lab in ("G-I", "J-L") else "" for y in ys], textposition="inside",
                          hovertemplate="%{x}<br>" + lab + ": %{y:.1f}% (%{customdata})<extra></extra>"))
fig2.update_layout(barmode="stack", yaxis_title="% of citations", bargap=0.25)
bar_style(fig2)

# ---------------- chart 3: fines per home per month ----------------
fig3 = base_fig("Bria pays 8 to 15x the national fine rate per home, and that rate did not climb",
                "Fine dollars per home per month, 3-month rolling mean. CMS penalty file starts June 2023.")
fm = [m for m in months if m >= "2023-06"]
for grp, col, name in (("national", NAT, "National (all other homes)"), ("bria", BRIA, "Bria Health Services (15 homes)")):
    s = [r for r in series("fines_monthly", grp) if r["MO"][:7] >= "2023-06"]
    raw = [r["USD"] / r["HOMES"] for r in s]
    fig3.add_trace(go.Scatter(x=fm, y=roll3(raw), mode="lines", name=name, line=dict(color=col, width=3),
                              customdata=[[r["USD"], r["FINES"], r["HOMES"], v] for r, v in zip(s, raw)],
                              hovertemplate="%{x}<br>$%{y:,.0f} per home (3-mo)<br>raw $%{customdata[3]:,.0f} = $%{customdata[0]:,.0f} / %{customdata[2]} homes, %{customdata[1]} fines<extra>" + name + "</extra>"))
fig3.update_layout(yaxis_title="fine dollars per home per month", yaxis_tickprefix="$", xaxis=dict(tickvals=[m for m in fm if m.endswith("-01") or m.endswith("-07")]))

# ---------------- chart 4: does harm lead the fine? lag correlation ----------------
def corr(a, b):
    ma, mb = st.mean(a), st.mean(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** .5
    return num / den
LAGS = list(range(0, 7))
lagres = {}
for grp in ("bria", "national"):
    m = series("monthly", grp); f = series("fines_monthly", grp)
    g = [r["GPLUS"] / r["HOMES"] for r in m]; u = [r["USD"] / r["HOMES"] for r in f]
    s0 = 5  # 2023-06, first month the penalty file covers
    lagres[grp] = [corr(g[s0:36 - lag], u[s0 + lag:36]) for lag in LAGS]
fig4 = base_fig("Fines land in the same month as the harm citations, not months later",
                "Correlation between harm citations (G+) per home in month t and fine dollars per home in month t+lag, Jun 2023 to Dec 2025 (31 months).")
for grp, col, name in (("national", NAT, "National"), ("bria", BRIA, "Bria (15 homes, noisy)")):
    fig4.add_trace(go.Bar(x=[f"lag {l}" for l in LAGS], y=lagres[grp], name=name, marker_color=col,
                          text=[f"{v:.2f}" for v in lagres[grp]], textposition="outside",
                          hovertemplate="%{x} months<br>r = %{y:.2f}<extra>" + name + "</extra>"))
fig4.update_layout(barmode="group", yaxis_title="Pearson r", yaxis_range=[-0.5, 0.85])
bar_style(fig4)

# ---------------- numbers for prose ----------------
def yr_rates(grp, yr):
    m = [r for r in series("monthly", grp) if r["MO"].startswith(str(yr))]
    f = [r for r in series("fines_monthly", grp) if r["MO"].startswith(str(yr)) and r["MO"][:7] >= "2023-06"]  # penalty file starts Jun 2023
    hm = sum(r["HOMES"] for r in m); hf = sum(r["HOMES"] for r in f)
    return dict(defs=sum(r["DEFS"] for r in m) / hm, g=sum(r["GPLUS"] for r in m) / hm, ij=sum(r["IJ"] for r in m) / hm,
                share=100 * sum(r["GPLUS"] for r in m) / sum(r["DEFS"] for r in m),
                usd=sum(r["USD"] for r in f) / hf, fines=sum(r["FINES"] for r in f) / hf)
B = {y: yr_rates("bria", y) for y in (2023, 2024, 2025)}
_pm = [r for r in series("monthly", "bria") if r["MO"] < "2025"]
IJP = 0  # set below
N = {y: yr_rates("national", y) for y in (2023, 2024, 2025)}
IJP = B[2025]["ij"] / (sum(r["IJ"] for r in _pm) / sum(r["HOMES"] for r in _pm))
json.dump(dict(bria=B, national=N, lag=lagres), open(f"{D}/derived.json", "w"), indent=1)

lede = ("Bria Health Services runs 15 nursing homes in Illinois. The first pass said its harm-level citations climbed from 2023 to 2025 "
        "and the fines followed. Rebuilt as rates per home, the picture is sharper and less tidy: Bria has been cited two to three times "
        "as often as the average home all along, its <b>immediate-jeopardy</b> rate rose 2.4x in 2025, and the fines came with the citations, not after them. "
        "A CCN is the six-digit certification number CMS gives each nursing home; every join here is on it.")

sec1 = (f"<p>Every month from 2023 through 2025, Bria's homes drew more citations than the country. "
        f"<b>{B[2023]['defs']:.2f}</b>, <b>{B[2024]['defs']:.2f}</b> and <b>{B[2025]['defs']:.2f}</b> citations per home per month in 2023, 2024, 2025, "
        f"against a national <b>{N[2023]['defs']:.2f}</b>, <b>{N[2024]['defs']:.2f}</b>, <b>{N[2025]['defs']:.2f}</b>.</p>"
        f"<p>The rate did not march upward. It peaked in 2024, then fell back in 2025 to a bit under 2023. What the first pass read as "
        f"\"getting worse\" is the mix, not the volume: see the next chart.</p>"
        f"<p>Why rates and not counts: the deficiency file is a rolling three-cycle window, so 6,265 of 14,632 homes nationally (43%), and 6 of Bria's 15, "
        f"have no retained record before 2023. Each month's denominator is only the homes whose record had already started, on both sides.</p>")

sec2 = (f"<p>Harm citations (G and up) per home per month: Bria <b>{B[2023]['g']:.2f}</b>, <b>{B[2024]['g']:.2f}</b>, <b>{B[2025]['g']:.2f}</b>. "
        f"National: <b>{N[2023]['g']:.3f}</b>, <b>{N[2024]['g']:.3f}</b>, <b>{N[2025]['g']:.3f}</b>. Bria is roughly <b>10x</b> the country every year (7.8x, 8.8x, 11.2x).</p>"
        f"<p>The first-pass share (21.5% to 33.5%) reproduces to the digit. But the 2025 jump is mostly the denominator shrinking: total citations fell "
        f"from 345 to 227 while harm citations held (70 to 76). The harm <i>rate</i> per home rose only {100*(B[2025]['g']/B[2024]['g']-1):.0f}% from 2024.</p>"
        f"<p>What did move: immediate jeopardy (J-L), the letters that mean a resident is in danger now. Bria per home per month: "
        f"<b>{B[2023]['ij']:.3f}</b>, <b>{B[2024]['ij']:.3f}</b>, <b>{B[2025]['ij']:.3f}</b>. The counts are small: 7, 5, 17 events. "
        f"2025 is <b>2.4x</b> 2023, <b>{IJP:.1f}x</b> the pooled 2023-24 rate, and <b>{B[2025]['ij']/N[2025]['ij']:.0f}x</b> the 2025 national rate of {N[2025]['ij']:.3f}, which was flat all three years. "
        f"Twelve of the 17 came in the second half of 2025.</p>"
        f"<p>Attribution caveat: the chain roster is a 2025-12-01 snapshot with no history. The 12-month ownership-change flag says nothing about 2023, so pre-2025 citations are assumed to belong to Bria, not shown to.</p>")

sec3 = (f"<p>Fine dollars per home per month: Bria <b>${B[2023]['usd']:,.0f}</b> (Jun-Dec 2023), <b>${B[2024]['usd']:,.0f}</b>, <b>${B[2025]['usd']:,.0f}</b>. "
        f"National: <b>${N[2023]['usd']:,.0f}</b>, <b>${N[2024]['usd']:,.0f}</b>, <b>${N[2025]['usd']:,.0f}</b>.</p>"
        f"<p>So the money is <b>{B[2025]['usd']/N[2025]['usd']:.0f}x</b> the national rate in 2025, and it did not climb: the heaviest stretch was the second half of 2023, "
        f"2024 was half that, 2025 recovered to two-thirds. Fines per home per month were flat too, {B[2023]['fines']:.2f}, {B[2024]['fines']:.2f}, {B[2025]['fines']:.2f}. "
        f"Nationally both fell every year, so Bria's share of the country's enforcement grew while its own bill did not.</p>"
        f"<p>Only 'Fine' rows carry a dollar amount; 2,470 'Payment Denial' rows nationally (15%) carry none and are counted as penalties, not fines. "
        f"Fines are dated by penalty date, and the file starts 2023-06-17, so nothing before June 2023 is visible on either side.</p>")

sec4 = (f"<p>If violations got worse <i>before</i> fines hit, harm this month should predict fine dollars in later months. It does not. "
        f"Nationally the correlation is strongest at lag 0 (r = {lagres['national'][0]:.2f}) and decays from there; the penalty date tracks the survey date. "
        f"Bria's own series is too noisy to date the lag: r = {lagres['bria'][0]:.2f} at lag 0, {lagres['bria'][5]:.2f} at lag 5, and sign flips between. "
        f"Both series also carry a trend (the country's fines fell every year), so every lag here is inflated a little; the ranking of lags is the reading, not the size of r.</p>"
        f"<p>Read plainly: the fine is the same event as the citation, dated the same month. There is no window in this data where Bria's "
        f"record deteriorated and enforcement had not yet arrived.</p>")

footer = ("Tables: LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411 (chain roster, dated 2025-12-01), HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES "
          "(418,479 rows, surveys 2017-03 to 2026-05), HEALTH__FED_CMS_NURSING_HOME_PENALTIES (16,180 rows, 2023-06 to 2026-05). "
          "Bria = CHAIN_ID 88; the name filter '%bria%' also catches Briar Hill Management and was not used. "
          "COMPLAINT_DEFICIENCY is 'N' on every row before April 2023, so complaint-vs-standard splits for early 2023 are not usable. "
          "Every query is in <code>queries.py</code>, logged in <code>queries.log</code>.")

hero = [(f"{B[2025]['defs']/N[2025]['defs']:.1f}x", "citations per home vs national, 2025"),
        ("~10x", "harm citations per home vs national, every year"),
        ("2.4x", "Bria immediate-jeopardy rate, 2025 vs 2023"),
        ("lag 0", "where fines track harm, nationally")]

write_story(f"{D}/story.html", "Bria: worse than the country every month, fined in the same month",
            lede, [("Cited 2 to 3x as often, all three years", sec1, fig1),
                   ("Harm share up, harm rate up less, immediate jeopardy 2.4x", sec2, fig2),
                   ("Fines per home: 13x the country, and not rising", sec3, fig3),
                   ("Fines do not lag the violations", sec4, fig4)], footer, hero)
print("wrote story.html")
print(json.dumps(dict(bria=B, national=N), indent=1))
