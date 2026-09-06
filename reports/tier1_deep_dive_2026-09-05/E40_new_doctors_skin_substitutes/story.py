"""Build story.html from results.json. No warehouse calls here."""
import json, sys
sys.path.insert(0, "reports/tier1_deep_dive_2026-09-05")
import plotly.graph_objects as go
from _shared.viz import PAL, TEXT2, base_fig, bar_style, write_story

D = "reports/tier1_deep_dive_2026-09-05/E40_new_doctors_skin_substitutes"
R = json.load(open(f"{D}/results.json"))
M = lambda x: f"${x/1e6:,.0f}M"
K = lambda x: f"${x/1e3:,.1f}k"

top1 = {r["GRP"]: r for r in R["top1"]}
top1s = {r["GRP"]: r for r in R["top1_skin"]}
allskin = {r["GRP"]: r for r in R["all_skin"]}
new_all = R["all_new_skin"][0]
pb = {r["GRP"]: r for r in R["per_bene"]}
pbn = {r["GRP"]: r for r in R["per_bene_np_pa"]}
base = {r["GRP"]: r for r in R["all_base"]}
npb = {(r["PTYPE"], r["GRP"]): r for r in R["np_pa_base"]}
conc = R["conc"][0]
pba = {r["GRP"]: r for r in R["per_bene_all_nppa"]}

loose = top1["new"]["ALLOWED"]; strict_top1 = top1s["new"]["SKIN_ALLOWED"]; strict_all = new_all["SKIN_ALLOWED"]

# ---- chart 1: strict vs loose ------------------------------------------------------------------
f1 = base_fig("The headline is $452M, not $1.35B",
              "DY2024 Medicare Part B allowed charges, NPIs enumerated 2022 or later", height=420)
labels = ["Loose: all Part B billing<br>by the 354 new top-1% NPIs",
          "Strict: skin-substitute lines only,<br>same 354 (first pass)",
          "Strict: skin-substitute lines,<br>every new NPI (114)"]
vals = [loose, strict_top1, strict_all]
f1.add_trace(go.Bar(x=labels, y=vals, marker_color=[PAL[0], PAL[1], PAL[1]],
                    text=[M(v) for v in vals], textposition="outside",
                    hovertemplate="%{x}<br>%{text}<extra></extra>"))
f1.update_yaxes(title="allowed charges", tickprefix="$", range=[0, loose * 1.15])
bar_style(f1)

# ---- chart 2: enumeration year -----------------------------------------------------------------
yr = {r["ENUM_YEAR"]: r for r in R["by_year"]}
den = {r["ENUM_YEAR"]: r["PARTB_BILLERS"] for r in R["by_year_denom"]}
years = sorted(yr)
per_biller = [yr[y]["SKIN_ALLOWED"] / den[y] for y in years]
f2 = base_fig("NPIs born 2022-23 bill skin substitutes at the same rate as NPIs born 2018-20",
              "skin-substitute allowed dollars per individual Part B biller, by the year the NPI was created", height=460)
cols = [PAL[1] if y >= 2022 else PAL[0] for y in years]
f2.add_trace(go.Bar(x=[str(y) for y in years], y=per_biller, marker_color=cols,
                    customdata=[[yr[y]["SKIN_BILLERS"], den[y], yr[y]["SKIN_ALLOWED"]] for y in years],
                    hovertemplate="NPIs created %{x}<br>$%{y:,.0f} skin dollars per Part B biller<br>"
                                  "%{customdata[0]} skin billers of %{customdata[1]:,} billers<br>"
                                  "$%{customdata[2]:,.0f} total skin allowed<extra></extra>"))
f2.add_annotation(x="2024", y=per_biller[-1], text="2024: NPIs created mid-year,<br>billed a partial year",
                  showarrow=True, arrowhead=0, ax=-60, ay=-60, font=dict(size=12, color=TEXT2))
f2.add_annotation(x="2006", y=per_biller[1], text="2006: the year NPIs were<br>issued to everyone at once",
                  showarrow=True, arrowhead=0, ax=60, ay=-50, font=dict(size=12, color=TEXT2))
f2.update_yaxes(title="skin $ per Part B biller", tickprefix="$")
f2.update_xaxes(title="year the NPI was created")
bar_style(f2)

# ---- chart 3: top 10 ---------------------------------------------------------------------------
t10 = R["top10"]
f3 = base_fig("Ten new NPIs took $191M of the $452M; one Arizona nurse practitioner took $47M",
              "skin-substitute allowed dollars, DY2024, ten largest NPIs enumerated 2022 or later", height=520)
names = [f"{r['FIRST_NAME']} {r['LAST_NAME']} ({r['ST']})" for r in t10][::-1]
f3.add_trace(go.Bar(y=names, x=[r["SKIN_ALLOWED"] for r in t10][::-1], orientation="h", marker_color=PAL[1],
                    text=[M(r["SKIN_ALLOWED"]) for r in t10][::-1], textposition="outside",
                    customdata=[[r["PTYPE"], r["CITY"], r["ENUM_DT"], r["BENES"], r["TOTAL_ALLOWED"], r["UNITS"], r["NPI"]] for r in t10][::-1],
                    hovertemplate="<b>%{y}</b><br>%{customdata[0]}, %{customdata[1]}<br>NPI %{customdata[6]} created %{customdata[2]}<br>"
                                  "skin allowed $%{x:,.0f} on %{customdata[3]} beneficiaries<br>"
                                  "all Part B allowed $%{customdata[4]:,.0f}<br>%{customdata[5]:,.0f} square centimeters billed<extra></extra>"))
f3.update_xaxes(title="skin-substitute allowed", tickprefix="$", range=[0, t10[0]["SKIN_ALLOWED"] * 1.2])
f3.update_layout(margin=dict(l=200))
bar_style(f3)

# ---- chart 4: per beneficiary ------------------------------------------------------------------
f4 = base_fig("Per patient, new graft billers look like old graft billers; the gap is the trade, not the birth year",
              "median Part B allowed dollars per beneficiary, among NPIs that billed any skin substitute", height=440)
cats = ["Nurse practitioners and physician assistants", "All skin billers, every specialty"]
f4.add_trace(go.Bar(name="NPIs created 2022 or later", x=cats,
                    y=[pbn["new"]["MED_ALLOWED_PER_BENE"], pb["new"]["MED_ALLOWED_PER_BENE"]], marker_color=PAL[1],
                    text=[K(pbn["new"]["MED_ALLOWED_PER_BENE"]), K(pb["new"]["MED_ALLOWED_PER_BENE"])], textposition="outside",
                    customdata=[pbn["new"]["NPIS"], pb["new"]["NPIS"]],
                    hovertemplate="%{x}<br>new NPIs: $%{y:,.0f} per beneficiary (median of %{customdata} NPIs)<extra></extra>"))
f4.add_trace(go.Bar(name="NPIs created before 2022", x=cats,
                    y=[pbn["veteran"]["MED_ALLOWED_PER_BENE"], pb["veteran"]["MED_ALLOWED_PER_BENE"]], marker_color=PAL[0],
                    text=[K(pbn["veteran"]["MED_ALLOWED_PER_BENE"]), K(pb["veteran"]["MED_ALLOWED_PER_BENE"])], textposition="outside",
                    customdata=[pbn["veteran"]["NPIS"], pb["veteran"]["NPIS"]],
                    hovertemplate="%{x}<br>veteran NPIs: $%{y:,.0f} per beneficiary (median of %{customdata} NPIs)<extra></extra>"))
f4.update_yaxes(title="allowed $ per beneficiary", tickprefix="$", range=[0, 40000])
f4.update_layout(barmode="group")
bar_style(f4)

# ---- states table --------------------------------------------------------------------------------
st = {}
for r in R["states"]:
    st.setdefault(r["ST"], {})[r["GRP"]] = r
rows = sorted(st.items(), key=lambda kv: -kv[1].get("new", {}).get("SKIN_ALLOWED", 0))[:10]
tbl = "<table style='border-collapse:collapse;font-size:14px'><tr><th align=left>State</th><th align=right>New NPIs</th><th align=right>New $</th><th align=right>Veteran NPIs</th><th align=right>Veteran $</th><th align=right>New share</th></tr>"
for s, g in rows:
    n = g.get("new", {"NPIS": 0, "SKIN_ALLOWED": 0}); v = g.get("veteran", {"NPIS": 0, "SKIN_ALLOWED": 0})
    share = n["SKIN_ALLOWED"] / (n["SKIN_ALLOWED"] + v["SKIN_ALLOWED"])
    tbl += f"<tr><td>{s}</td><td align=right>{n['NPIS']}</td><td align=right>{M(n['SKIN_ALLOWED'])}</td><td align=right>{v['NPIS']}</td><td align=right>{M(v['SKIN_ALLOWED'])}</td><td align=right>{share:.0%}</td></tr>"
tbl += "</table>"

new_np = npb[("Nurse Practitioner", "new")]; vet_np = npb[("Nurse Practitioner", "veteran")]
new_pa = npb[("Physician Assistant", "new")]; vet_pa = npb[("Physician Assistant", "veteran")]
np_pa_new_share = (new_np["PARTB_BILLERS"] + new_pa["PARTB_BILLERS"]) / (new_np["PARTB_BILLERS"] + vet_np["PARTB_BILLERS"] + new_pa["PARTB_BILLERS"] + vet_pa["PARTB_BILLERS"])
skin_new_share_npa = pbn["new"]["SKIN_ALLOWED"] / (pbn["new"]["SKIN_ALLOWED"] + pbn["veteran"]["SKIN_ALLOWED"])
addr = R["addr_summary"][0]; addrv = R["addr_vets"][0]

lede = ("An NPI is the ten-digit number Medicare uses to identify one clinician. A skin substitute is a lab-grown or donor-tissue graft laid on a wound and billed per square centimeter; "
        "the HCPCS codes Q4100 and up name them. The first pass said brand-new NPIs billed $1.35 billion in DY2024. "
        "Most of that is other services. The part that is provably skin substitutes is $452 million, across 114 NPIs that did not exist before 2022 - "
        "and once you compare them to the clinicians already in the graft business, they bill like everybody else in the wave.")

sections = [
    ("Strict beats loose",
     f"<p>The first pass took the 354 new NPIs inside Medicare's top 1% of individual Part B billers and summed <em>everything</em> they billed: {M(loose)}. Reproduced here to the dollar with a different ranking method.</p>"
     f"<p>Only skin-substitute service lines count as skin substitutes. For those 354, that is {M(strict_top1)} - also reproduced to the dollar.</p>"
     f"<p>Drop the top-1% filter and take every individual NPI created 2022 or later: {new_all['NPIS']} NPIs, {M(strict_all)}, {new_all['CODES']} graft codes, {new_all['SQ_CM_UNITS']:,.0f} square centimeters. "
     f"The top-1% cut hid only {M(strict_all - strict_top1)}: nearly every new NPI that touches a skin substitute is already a top-1% biller.</p>"
     f"<p>Headline number: <b>at least {M(strict_all)}</b>. It is a floor twice over: CMS deletes any service line under 11 beneficiaries, and the newer A2001-A2999 graft codes are left out (+{M(R['a2'][0]['ALLOWED'])} on 11 NPIs).</p>", f1),
    ("Birth year of the NPI does not predict it",
     f"<p>Take every NPI ever issued, sort by the year it was created, and ask how many skin-substitute dollars that cohort billed in DY2024 per Part B biller. "
     f"NPIs created in 2022 billed ${yr[2022]['SKIN_ALLOWED']/den[2022]:,.0f} per biller; 2023, ${yr[2023]['SKIN_ALLOWED']/den[2023]:,.0f}. NPIs created in 2020 billed ${yr[2020]['SKIN_ALLOWED']/den[2020]:,.0f}; 2018, ${yr[2018]['SKIN_ALLOWED']/den[2018]:,.0f}.</p>"
     f"<p>The 2022-23 cohorts are not an outlier; they sit at the top of the plateau that started in 2018 (2023 is the series high, by a hair). What changed is the product, not the people.</p>"
     f"<p>Base rate: new NPIs are {base['new']['PARTB_BILLERS']/(base['new']['PARTB_BILLERS']+base['veteran']['PARTB_BILLERS']):.1%} of all individual Part B billers and take {allskin['new']['SKIN_ALLOWED']/(allskin['new']['SKIN_ALLOWED']+allskin['veteran']['SKIN_ALLOWED']):.1%} of skin dollars - over-represented, but by half again, not by an order of magnitude.</p>", f2),
    ("Where the new money sits",
     f"<p>Ten states by new-NPI skin dollars, with the veteran billers beside them. Arizona and Illinois are where new NPIs carry a real share; Florida is the veteran capital.</p>{tbl}"
     f"<p style='margin-top:12px'>Address check: the {new_all['NPIS']} new billers sit at {addr['ADDRESSES']} practice addresses; {addr['NPIS_AT_SHARED_ADDR']} of them share one with another new biller ({M(addr['DOLLARS_AT_SHARED_ADDR'])}), "
     f"and {addrv['VETERAN_SKIN_NPIS_SAME_ADDR']} veteran skin billers ({M(addrv['THEIR_SKIN_DOLLARS'])}) sit at those same addresses. These are wound-care clinics adding staff, not 114 lone operators.</p>", None),
    ("The ten biggest new billers",
     f"<p>{conc['OVER_1M']} of the {conc['NPIS']} new NPIs cleared $1 million in skin substitutes in one year. The top ten hold {M(conc['TOP10'])} ({conc['TOP10']/conc['TOTAL']:.0%}); the top fifty {M(conc['TOP50'])} ({conc['TOP50']/conc['TOTAL']:.0%}).</p>"
     f"<p>Allison Charles, a Sun City, Arizona nurse practitioner whose NPI dates from April 2022, billed {M(t10[0]['SKIN_ALLOWED'])} of one product (Q4271, Complete FT) on {t10[0]['BENES']} beneficiaries - {t10[0]['UNITS']:,.0f} square centimeters. Gina Palacios and Elisabeth Balken, both Arizona NPs enumerated June 2023, billed $23M and $18M on 33 and 25 patients.</p>"
     f"<p>Eight of the ten are nurse practitioners or physician assistants. That is the pattern across the 114: {R['ptype'][0]['NPIS']} NPs and {R['ptype'][1]['NPIS']} PAs.</p>", f3),
    ("Per patient, like for like",
     f"<p>The first pass compared new NPIs to veteran top-1% billers of every specialty and found $21,595 per beneficiary against $3,892 - a 5.5x gap. Among skin billers the same all-specialty comparison reads {K(pb['new']['MED_ALLOWED_PER_BENE'])} against {K(pb['veteran']['MED_ALLOWED_PER_BENE'])}.</p>"
     f"<p>Restrict veterans to the same job titles - nurse practitioners and physician assistants who also bill skin substitutes - and the gap closes: {K(pbn['new']['MED_ALLOWED_PER_BENE'])} against {K(pbn['veteran']['MED_ALLOWED_PER_BENE'])}. "
     f"New NP/PAs are {np_pa_new_share:.0%} of NP/PA Part B billers and take {skin_new_share_npa:.0%} of NP/PA skin dollars.</p>"
     f"<p>For scale: the median NP or PA of either vintage bills about $150 per patient ({K(pba['new']['MED_ALLOWED_PER_BENE'])} new, {K(pba['veteran']['MED_ALLOWED_PER_BENE'])} veteran, all {pba['new']['NPIS']+pba['veteran']['NPIS']:,} of them). The graft billers are 200x their trade whatever year their NPI was born.</p>"
     f"<p>What survives: {pb['new']['OVER_100K_PER_BENE']} new NPIs bill over $100,000 per beneficiary, and {pb['new']['MAJORITY_SKIN']} of 114 draw most of their money from grafts. The individuals are extraordinary. The cohort is ordinary for its trade.</p>", f4),
]
footer = ("Tables: LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER (1,296,739 rows = 1,296,739 distinct NPIs), "
          "..._BY_PROVIDER_AND_SERVI (9,781,673 rows), HEALTH__FED_CMS_NPPES (9,606,683 rows = distinct NPIs). Vintage DY2024 by carbon dating: newest NPIs in both Part B files are 2024, none from 2025. "
          "Line dollars = TOT_SRVCS x AVG_MDCR_ALOWD_AMT. Skin substitute = HCPCS Q4100+. Every query in queries.py, logged in queries.log.")
write_story(f"{D}/story.html", "New NPIs and the skin-substitute wave", lede, sections, footer,
            hero=[(M(strict_all), "skin-substitute allowed, 114 NPIs created 2022+"), (M(loose), "loose first-pass number (all their billing)"),
                  (K(pbn["new"]["MED_ALLOWED_PER_BENE"]) + " vs " + K(pbn["veteran"]["MED_ALLOWED_PER_BENE"]), "per patient, new vs veteran NP/PA")])
print("wrote story.html")
