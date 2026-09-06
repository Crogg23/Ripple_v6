"""Build story.html from results.json. Run from repo root with PYTHONPATH=reports/tier1_deep_dive_2026-09-05."""
import json
import plotly.graph_objects as go
from _shared.viz import PAL, TEXT2, GRID, base_fig, bar_style, write_story

D = "reports/tier1_deep_dive_2026-09-05/02_owner_fines_per_home"
R = json.load(open(f"{D}/results.json"))
f = float
chains = [r for r in R["chains"] if r["CHAIN_ID"] != "(none)"]
none = [r for r in R["chains"] if r["CHAIN_ID"] == "(none)"][0]
big = [r for r in chains if r["HOMES"] >= 10]
rep = {r["CHAIN_ID"]: r for r in R["repeat"]}
allrows = R["chains"]
nat_fph = sum(r["FINES"] for r in allrows) / sum(r["HOMES"] for r in allrows)
nat_dpb = sum(f(r["DOLLARS"]) for r in allrows) / sum(r["BEDS"] for r in allrows)
nat_f100 = 100 * sum(r["FINES"] for r in allrows) / sum(r["BEDS"] for r in allrows)
rep_pw_all = 100 * sum(r["REPEAT_PAIRS_PW"] for r in R["repeat"]) / sum(r["PAIRS_PW"] for r in R["repeat"])
bria = next(r for r in chains if r["CHAIN_NAME"] == "BRIA HEALTH SERVICES")
sv = {r["CHAIN_ID"]: r for r in R["surveys"]}
il = [r for r in R["il_chains"] if r["CHAIN_ID"] != "(none)"]
il_none = [r for r in R["il_chains"] if r["CHAIN_ID"] == "(none)"][0]
st = {r["GRP"]: r for r in R["state_bed"]}
IL_FPH, IL_DPB, US_DPB, US_FPH = f(st["IL"]["FINES_PER_HOME"]), f(st["IL"]["DOLLARS_PER_BED"]), f(st["rest of US"]["DOLLARS_PER_BED"]), f(st["rest of US"]["FINES_PER_HOME"])
tot_dates = sum(r["SURVEY_DATES"] for r in R["surveys"]); tot_rp = sum(r["REPEAT_PAIRS"] for r in R["surveys"]); tot_h = sum(r["HOMES"] for r in R["surveys"])
rps_all = tot_rp / tot_dates
dph_else = (tot_dates - sv["88"]["SURVEY_DATES"]) / (tot_h - 15)
rps = lambda cid: sv[cid]["REPEAT_PAIRS"] / sv[cid]["SURVEY_DATES"]
rps_rank = sorted([rps(r["CHAIN_ID"]) for r in big if sv[r["CHAIN_ID"]]["SURVEY_DATES"]], reverse=True)
bria_rps_rank = rps_rank.index(rps("88")) + 1
gen = next(r for r in chains if r["CHAIN_NAME"] == "GENESIS HEALTHCARE")
short = lambda s: s if len(s) < 34 else s[:31] + "..."
HOT, BLUE, GRAY = PAL[7], PAL[0], "#b8b6b0"

# --- chart 1: top 10 fines per home, 10+ homes ---
top = sorted(big, key=lambda r: -f(r["FINES_PER_HOME"]))[:10]
rows1 = top + [gen, none]
fig1 = base_fig(f"Bria draws 5.9 fines per home, 2.8x the Illinois rate of {IL_FPH:.2f} (all US: {nat_fph:.2f})",
                "Chains with 10 or more homes, fines dated 2023-06-17 to 2026-05-13, ranked by fines per home", height=520)
fig1.add_trace(go.Bar(
    y=[short(r["CHAIN_NAME"]) for r in rows1][::-1], x=[f(r["FINES_PER_HOME"]) for r in rows1][::-1], orientation="h",
    marker_color=[HOT if r is bria else (GRAY if r in (gen, none) else BLUE) for r in rows1][::-1],
    text=[f"{f(r['FINES_PER_HOME']):.2f}" if r in (bria, gen, none) else "" for r in rows1][::-1], textposition="outside",
    customdata=[[r["HOMES"], r["BEDS"], r["FINES"], f(r["DOLLARS"]) / 1e6, r["HOMES_FINED"]] for r in rows1][::-1],
    hovertemplate="%{y}<br>%{x:.2f} fines per home<br>%{customdata[0]} homes, %{customdata[1]:,} beds<br>%{customdata[2]} fines, $%{customdata[3]:.2f}M<br>%{customdata[4]} of %{customdata[0]} homes fined<extra></extra>",
    name="fines per home", showlegend=False))
fig1.add_vline(x=nat_fph, line_dash="dot", line_color=TEXT2, annotation_text=f"all US {nat_fph:.2f}", annotation_position="top")
fig1.add_vline(x=IL_FPH, line_dash="dash", line_color=PAL[3], annotation_text=f"Illinois {IL_FPH:.2f}", annotation_position="top")
fig1.update_layout(xaxis_title="fines per home", margin=dict(l=240), bargap=0.3)
bar_style(fig1)

# --- chart 2: per-bed scatter, all 301 chains ---
fig2 = base_fig(f"Per bed, Bria is $2,172, 2.6x its own state (Illinois ${IL_DPB:,.0f}, rest of US ${US_DPB:,.0f})",
                "Every chain with 10+ homes (301). x = fines per 100 certified beds, y = fine dollars per bed", height=520)
others = [r for r in big if r not in (bria, gen)]
fig2.add_trace(go.Scatter(x=[f(r["FINES_PER_100_BEDS"]) for r in others], y=[f(r["DOLLARS_PER_BED"]) for r in others], mode="markers",
    marker=dict(color=BLUE, size=[6 + min(r["HOMES"], 300) / 15 for r in others], opacity=0.55, line=dict(width=0)),
    customdata=[[r["CHAIN_NAME"], r["HOMES"], r["BEDS"], r["FINES"]] for r in others],
    hovertemplate="%{customdata[0]}<br>%{x:.2f} fines per 100 beds<br>$%{y:,.0f} per bed<br>%{customdata[1]} homes, %{customdata[2]:,} beds, %{customdata[3]} fines<extra></extra>",
    name="other chains (dot size = homes)"))
for r, c, nm in ((bria, HOT, "Bria Health Services"), (gen, PAL[3], "Genesis Healthcare")):
    fig2.add_trace(go.Scatter(x=[f(r["FINES_PER_100_BEDS"])], y=[f(r["DOLLARS_PER_BED"])], mode="markers+text", text=[nm], textposition="middle left" if r is bria else "middle right",
        marker=dict(color=c, size=14, line=dict(width=0)), customdata=[[r["HOMES"], r["BEDS"], r["FINES"]]],
        hovertemplate=nm + "<br>%{x:.2f} fines per 100 beds<br>$%{y:,.0f} per bed<br>%{customdata[0]} homes, %{customdata[1]:,} beds, %{customdata[2]} fines<extra></extra>", name=nm))
fig2.add_hline(y=nat_dpb, line_dash="dot", line_color=TEXT2, annotation_text=f"all US ${nat_dpb:,.0f}/bed", annotation_position="bottom right")
fig2.add_hline(y=IL_DPB, line_dash="dash", line_color=PAL[3], annotation_text=f"Illinois ${IL_DPB:,.0f}/bed", annotation_position="top right")
fig2.add_vline(x=nat_f100, line_dash="dot", line_color=TEXT2, annotation_text=f"all homes {nat_f100:.2f}/100 beds", annotation_position="top")
fig2.update_layout(xaxis_title="fines per 100 beds", yaxis_title="fine dollars per bed", xaxis=dict(showgrid=True, gridcolor=GRID))

# --- chart 3: repeats per survey visit ---
rows3 = top + [gen]
fig3 = base_fig("Repeats track how often inspectors visit: per visit, Bria repeats less than Genesis",
                "Repeat (home, tag) pairs divided by survey dates since 2023-06-17. Same ten chains as the first chart plus Genesis. Hover for visits per home", height=520)
vals = [(short(r["CHAIN_NAME"]), rps(r["CHAIN_ID"]), sv[r["CHAIN_ID"]], rep[r["CHAIN_ID"]], r) for r in rows3]
fig3.add_trace(go.Bar(y=[v[0] for v in vals][::-1], x=[v[1] for v in vals][::-1], orientation="h",
    marker_color=[HOT if v[4] is bria else (GRAY if v[4] is gen else BLUE) for v in vals][::-1],
    text=[f"{v[1]:.2f}" if v[4] in (bria, gen) else "" for v in vals][::-1], textposition="outside",
    customdata=[[v[2]["SURVEY_DATES"], v[2]["REPEAT_PAIRS"], f(v[2]["DATES_PER_HOME"]), f(v[3]["REPEAT_PCT_PW"])] for v in vals][::-1],
    hovertemplate="%{y}<br>%{x:.2f} repeat pairs per survey date<br>%{customdata[1]} repeats over %{customdata[0]} survey dates<br>%{customdata[2]:.1f} survey dates per home, raw repeat share %{customdata[3]:.1f}%<extra></extra>", showlegend=False))
fig3.add_vline(x=rps_all, line_dash="dot", line_color=TEXT2, annotation_text=f"all homes {rps_all:.2f}", annotation_position="top")
fig3.update_layout(xaxis_title="repeat home-tag pairs per survey date", margin=dict(l=240), bargap=0.3)
bar_style(fig3)

# --- chart 4: Bria home by home, two ways ---
bh = sorted(R["bria_homes"], key=lambda r: -(f(r["DOLLARS"] or 0)))
fig4 = base_fig("Bria home by home: 14 of 15 fined, 12 of 15 rated one star",
                "Fine dollars per home. Blue = penalties file, 2023-06-17 on. Orange = CMS's own three-year rollup column in the provider file", height=520)
lbl = [f"{r['PROVIDER_NAME']} ({r['STATE']})" for r in bh]
fig4.add_trace(go.Bar(x=lbl, y=[f(r["DOLLARS"] or 0) for r in bh], name="penalties file (rebuilt)", marker_color=BLUE,
    customdata=[[r["FINES"], r["BEDS"], r["OVERALL_RATING"], r["ABUSE_ICON"], r["SPECIAL_FOCUS_STATUS"] or "-"] for r in bh],
    hovertemplate="%{x}<br>$%{y:,.0f}, %{customdata[0]} fines<br>%{customdata[1]} beds, %{customdata[2]}-star, abuse icon %{customdata[3]}, %{customdata[4]}<extra></extra>"))
fig4.add_trace(go.Bar(x=lbl, y=[f(r["CMS_DOLLARS"] or 0) for r in bh], name="CMS rollup column", marker_color=PAL[1],
    customdata=[[r["CMS_FINES"]] for r in bh], hovertemplate="%{x}<br>$%{y:,.0f}, %{customdata[0]} fines (CMS column)<extra></extra>"))
fig4.update_layout(barmode="group", yaxis_title="fine dollars", xaxis=dict(tickangle=-40), legend=dict(y=-0.55), margin=dict(b=200))
bar_style(fig4)

# --- prose ---
nchain = len(chains)
lede = (f"CMS tags every certified nursing home with a chain id. {nchain} chains own {sum(r['HOMES'] for r in chains):,} of 14,713 homes; "
        f"{none['HOMES']:,} homes carry no chain. Since the penalty file opens on 2023-06-17, the biggest chains pay about one fine per home. "
        f"Bria Health Services, 15 homes, all in Illinois, pays {f(bria['FINES_PER_HOME']):.1f} fines per home and "
        f"${f(bria['DOLLARS_PER_BED']):,.0f} per bed, first on both among the {len(big)} chains with ten or more homes. "
        f"Illinois fines hard (${IL_DPB:,.0f} a bed against ${US_DPB:,.0f} elsewhere), so the fair yardstick is Illinois: Bria is 2.6x its own state and first of the {len(il)} Illinois chains with ten or more homes there.")
hero = [(f"{f(bria['FINES_PER_HOME']):.1f}", "fines per Bria home (all homes: 0.93)"),
        (f"${f(bria['DOLLARS_PER_BED']):,.0f}", "fine dollars per Bria bed (all homes: $292)"),
        (f"{IL_DPB/US_DPB:.1f}x", "Illinois fines per bed vs the rest of the US"),
        (f"1st of {len(il)}", "Illinois chains with 10+ homes, on fines per home, per bed, and dollars per bed")]
s1 = (f"<p>A CCN is the CMS Certification Number, one per certified nursing home. The provider file gives each home a chain id; the penalties file lists every fine and payment denial by CCN. "
      f"We counted distinct fine ids per home from 2023-06-17 (the first date in the file) to 2026-05-13 (the last), then rolled up by chain. Only chains with ten or more homes are ranked, so a two-home owner with one bad year cannot top the list.</p>"
      f"<p>Bria: {bria['FINES']} fines on {bria['HOMES']} homes, ${f(bria['DOLLARS'])/1e6:.2f}M. Genesis: {gen['FINES']} fines on {gen['HOMES']} homes, ${f(gen['DOLLARS'])/1e6:.1f}M, {f(gen['FINES_PER_HOME']):.2f} per home. "
      f"The first pass said 5.4 vs 1.1; that came from the provider file's own fine-count column. The penalty file, counted from scratch, says {f(bria['FINES_PER_HOME']):.2f} vs {f(gen['FINES_PER_HOME']):.2f}. Same story, second source.</p>"
      f"<p>Chain size itself is not the signal: chains with 10+ homes average 0.96 fines per home, smaller chains 0.94, no-chain homes 0.87. Ownership matters only when you name the owner.</p>")
s2 = (f"<p>Fines per home rewards a chain of small homes. Beds fix that. Bria's homes average {bria['BEDS']//bria['HOMES']} certified beds, above Genesis at {gen['BEDS']/gen['HOMES']:.1f}, so the per-bed view is the fair one.</p>"
      f"<p>On fines per 100 beds Bria drops to third ({f(bria['FINES_PER_100_BEDS']):.2f}) behind Bayshire ({[f(r['FINES_PER_100_BEDS']) for r in big if r['CHAIN_NAME']=='BAYSHIRE SENIOR COMMUNITIES'][0]:.2f}, tiny 68-bed homes) and the Bello/Maze/Swain family group. "
      f"On dollars per bed Bria stays first at ${f(bria['DOLLARS_PER_BED']):,.0f}; second is Goldwater Care at $1,874. Genesis sits at ${f(gen['DOLLARS_PER_BED']):,.0f}, near the all-homes line of ${nat_dpb:,.0f}. Bria's fines are not just frequent, they are large: ${f(bria['DOLLARS'])/bria['FINES']:,.0f} each against ${f(gen['DOLLARS'])/gen['FINES']:,.0f} at Genesis.</p>"
      f"<p>The catch: Illinois is a hard state. Its 669 homes draw {IL_FPH:.2f} fines per home and ${IL_DPB:,.0f} per bed; the other 14,044 homes draw {US_FPH:.2f} and ${US_DPB:,.0f}. So national multiples flatter the finding. Ranked only against Illinois chains with ten or more Illinois homes, Bria is still first on all three measures:</p>"
      + "<table style='font-size:13px;border-collapse:collapse'><tr><th align=left>Illinois chain</th><th>homes</th><th>fines/home</th><th>fines/100 beds</th><th>$/bed</th></tr>"
      + "".join(f"<tr><td>{short(r['CHAIN_NAME'])}</td><td align=right>{r['HOMES']}</td><td align=right>{f(r['FINES_PER_HOME']):.2f}</td><td align=right>{f(r['FINES_PER_100_BEDS']):.2f}</td><td align=right>{f(r['DOLLARS_PER_BED']):,.0f}</td></tr>" for r in il[:8])
      + f"<tr><td>Illinois, no chain</td><td align=right>{il_none['HOMES']}</td><td align=right>{f(il_none['FINES_PER_HOME']):.2f}</td><td align=right>{f(il_none['FINES_PER_100_BEDS']):.2f}</td><td align=right>{f(il_none['DOLLARS_PER_BED']):,.0f}</td></tr></table>")
s3 = (f"<p>Does it repeat? The deficiencies file lists every survey citation by home and tag (a tag is the CMS rule number, e.g. F0689 accident hazards). "
      f"A (home, tag) pair cited on two or more different survey dates is a repeat: the inspector came back and found the same problem. We cut this to surveys since 2023-06-17 so the window matches the fines.</p>"
      f"<p>Raw, Bria repeats {f(rep[bria['CHAIN_ID']]['REPEAT_PCT_PW']):.0f}% of its pairs ({rep[bria['CHAIN_ID']]['REPEAT_PAIRS_PW']} of {rep[bria['CHAIN_ID']]['PAIRS_PW']}), third of the 301 big chains, against {rep_pw_all:.1f}% for all homes. "
      f"But the raw share tracks how often inspectors show up: Bria homes were surveyed {f(sv['88']['DATES_PER_HOME']):.1f} times each in the window, everyone else {dph_else:.1f}. More visits, more chances to re-find a tag. "
      f"Divide repeats by survey dates and Bria drops to {rps('88'):.2f} repeat pairs per visit, rank {bria_rps_rank} of 301, below Genesis at {rps('237'):.2f} and below all homes at {rps_all:.2f}.</p>"
      f"<p>So the honest reading: Bria is not a chain that repeats more per inspection. It is a chain inspectors keep coming back to, four times as often as the rest, and every visit finds something. F0689 (accident hazards, supervision) was cited at all 15 homes and repeated at all 15; abuse (F0600) at 13 homes, repeated at 12.</p>")
s4 = (f"<p>Home by home, so nobody can say one outlier carries the chain: {bria['HOMES_FINED']} of 15 Bria homes were fined; 12 of 15 hold a one-star overall rating; 11 carry CMS's abuse icon; two are Special Focus Facility candidates. "
      f"Nexus Pavilion at Belleville alone drew $821,641 across 7 fines. The two bars per home show the penalties file rebuilt from scratch beside CMS's own rollup column; they differ home by home (different three-year windows) and agree at the chain level within 4%.</p>"
      f"<p>The clean home is Bria of Geneva: five stars, zero fines. One of fifteen.</p>"
      f"<p>One caveat on the roster: the chain tag is a single snapshot dated 2025-12-01, applied to fines back to 2023-06-17. A home that joined Bria late carries its prior owner's fines under Bria's name. Five of the 15 still carry Nexus names, the pre-rebrand or pre-transfer label; the ownership-change file, not this one, settles who owned what when.</p>")
footer = ("Tables: LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411 (14,713 homes, processing date 2025-12-01), HEALTH__FED_CMS_NURSING_HOME_PENALTIES (16,180 rows: 13,710 fines with unique FINE_ID, 2,470 payment denials with no id, 2023-06-17 to 2026-05-13), "
          "HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES (418,479 rows, 2017-03-23 to 2026-05-20; only 40 homes have 2017 rows and complaint citations start in 2023, so it is a rolling window with a thin tail, not a nine-year series). "
          "Fines counted on distinct FINE_ID; 255 same-home same-day same-amount fine pairs have distinct ids and are kept as separate fines. CHAIN_ID: 617 real values plus a blank string on 4,551 homes; the first pass's 618 counted the blank. "
          "Queries: <code>queries.py</code>, log in <code>queries.log</code>.")
write_story(f"{D}/story.html", "Owner fines per home", lede,
            [("One fine per home is normal. Bria pays six.", s1, fig1),
             ("Per bed, and against Illinois, still first", s2, fig2),
             ("The same problem, found again, because inspectors keep coming", s3, fig3),
             ("Fifteen homes, one clean", s4, fig4)], footer, hero=hero)
print("wrote story.html")
