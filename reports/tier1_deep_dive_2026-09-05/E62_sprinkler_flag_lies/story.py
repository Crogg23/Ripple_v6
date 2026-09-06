"""Build story.html from results.json (written by queries.py). No warehouse calls."""
import json, html
import plotly.graph_objects as go
from _shared.viz import PAL, STATUS, base_fig, bar_style, write_story
D="reports/tier1_deep_dive_2026-09-05/E62_sprinkler_flag_lies/"
R=json.load(open(D+"results.json"))
def g(k): return [v for kk,v in R.items() if kk.startswith(k)][0]

# chart 1: the sprinkler tag family, lifetime vs open at Yes homes
fam=g("13 ")
fam=[r for r in fam if r['CITES']>=10]
short={'0353':'K0353 inspect/test/maintain','0351':'K0351 install approved system','0354':'K0354 out of service >10h','0342':'K0342 alarm tied to sprinkler','0352':'K0352 supervisory attachments','0400':'K0400 tall-building sprinklers'}
f1=base_fig("K0351 is the only tag that says 'no approved system' - 3,764 lifetime cites at Yes homes, 68 open",
            "Sprinkler-family K-tags at homes flagged Yes, all surveys 2016-07 to 2026-05")
f1.add_bar(name="All cites, lifetime", x=[short[r['TAG']] for r in fam], y=[r['CITES'] for r in fam], marker_color=PAL[0],
           text=[f"{r['CITES']:,}" for r in fam], textposition="outside", hovertemplate="%{x}<br>%{y:,} cites<extra></extra>")
f1.add_bar(name="Still open on 2026-05-01", x=[short[r['TAG']] for r in fam], y=[r['OPEN_CITES'] for r in fam], marker_color=PAL[1],
           text=[str(r['OPEN_CITES']) for r in fam], textposition="outside", hovertemplate="%{x}<br>%{y} open<extra></extra>")
f1.update_layout(barmode="group", yaxis_title="citations", height=500); bar_style(f1)

# chart 2: the 68 open by status
st=g("11 ")
lab={'Deficient, Provider has date of correction':'Date promised (after the flag date)','Deficient, Provider has plan of correction':'Plan filed, mostly no date',
     'Deficient, Provider has no plan of correction':'No plan of correction','Waiver has been granted':'Waiver granted (CMS says OK)','No revisit needed':'No revisit needed'}
col={'Deficient, Provider has date of correction':STATUS['warning'],'Deficient, Provider has plan of correction':STATUS['warning'],
     'Deficient, Provider has no plan of correction':STATUS['critical'],'Waiver has been granted':PAL[0],'No revisit needed':PAL[2]}
f2=base_fig("Of the 68 open, only 14 have no plan at all; 11 are CMS-granted waivers",
            "K0351 citations open on 2026-05-01 at homes flagged Yes, by CMS correction status")
f2.add_bar(x=[r['CITES'] for r in st], y=[lab[r['STATUS']] for r in st], orientation='h', marker_color=[col[r['STATUS']] for r in st],
           text=[f"{r['CITES']}  (avg {r['AVG_DAYS']} days open)" for r in st], textposition="outside",
           hovertemplate="%{y}<br>%{x} cites<extra></extra>")
f2.update_layout(yaxis=dict(autorange="reversed"), xaxis=dict(range=[0,32], title="open citations"), height=420, showlegend=False); bar_style(f2)

# chart 3: by state, waiver vs not
sts=g("14 ")
f3=base_fig("Indiana leads with 15 open; Missouri's 7 are all waivers",
            "Homes flagged Yes with an open K0351 on 2026-05-01, by state")
xs=[r['STATE'] for r in sts]
f3.add_bar(name="Open, not waived", x=xs, y=[r['OPEN_CITES']-r['WAIVER'] for r in sts], marker_color=PAL[1],
           customdata=[[r['YES_HOMES'],r['AVG_DAYS'],r['MAX_DAYS']] for r in sts],
           hovertemplate="%{x}: %{y} not waived<br>%{customdata[0]:,} Yes homes in state<br>avg %{customdata[1]} days open, max %{customdata[2]}<extra></extra>")
f3.add_bar(name="Waiver granted", x=xs, y=[r['WAIVER'] for r in sts], marker_color=PAL[0], hovertemplate="%{x}: %{y} waived<extra></extra>")
f3.update_layout(barmode="stack", yaxis_title="open citations", height=460); bar_style(f3)

# chart 4: age buckets stacked by status
ag=g("15 ")
names=[r['BUCKET'][3:] for r in ag]
f4=base_fig("45 of 68 are under 90 days old; everything over a year is a waiver or a no-plan home",
            "Days between the K0351 survey and the 2026-05-01 flag date")
for key,label,c in [('HAS_DATE','Date promised',STATUS['warning']),('HAS_PLAN','Plan filed',PAL[3]),('NO_REVISIT','No revisit needed',PAL[2]),
                    ('NO_PLAN','No plan',STATUS['critical']),('WAIVER','Waiver',PAL[0])]:
    f4.add_bar(name=label, x=names, y=[r[key] for r in ag], marker_color=c, hovertemplate="%{x}<br>"+label+": %{y}<extra></extra>")
f4.update_layout(barmode="stack", yaxis_title="open citations", height=460); bar_style(f4)

lst=g("18 ")
rows="".join(f"<tr><td>{html.escape(r['PROVIDER_NAME'])}</td><td>{r['STATE']}</td><td>{r['SURVEY_DATE']}</td><td>{r['SS']}</td><td>{html.escape(r['STATUS'])}</td><td>{r['DAYS_OPEN']}</td></tr>" for r in lst[:15])
table=f"<div style='overflow-x:auto'><table style='border-collapse:collapse;font-size:13px'><tr><th align=left>Home</th><th>St</th><th>Survey</th><th>Scope</th><th align=left>Status</th><th>Days open</th></tr>{rows}</table></div>"

lede=("CMS's nursing-home directory has a checkbox, 'automatic sprinkler systems in all required areas'. It reads Yes on 14,638 of 14,700 homes and has "
      "no No value at all. The fire-safety inspection file has a tag, K0351, that means 'install an approved automatic sprinkler system'. "
      "On the day the Yes flag was published (2026-05-01), 67 Yes-flagged homes were carrying an open K0351. Half of those were less than 50 days old. "
      "The ones that have sat for years are mostly waivers CMS itself granted.")
sections=[
 ("Which tags mean 'sprinkler'", "<p>Eight K-tags mention sprinklers. Six matter. K0353 (inspect, test, maintain) is 4x bigger than K0351 and is about upkeep, not absence. "
  "A LIKE '%sprinkler%' filter blends them and inflates the story 4x. This hunch is K0351 only.</p><p>The CCN (CMS Certification Number, the home's federal ID) joins the two files clean: 14,700 rows, 14,700 distinct, zero orphans from the fire file.</p>", f1),
 ("What 'open' means here", "<p>Open = cited on or before 2026-05-01 and no correction date, or a correction date after 2026-05-01. That gives 68 citations at 67 homes (one home holds two).</p>"
  "<p>Thirty have no date at all. But status splits them: 22 have a promised date that simply falls after the flag date, 19 filed a plan, 14 filed nothing, 11 hold a CMS waiver, 2 need no revisit.</p>"
  "<p>The 22 'date of correction' rows are a promise, not a revisit. Four of those dates are past 2026-06-01, the fire file's own publication date, so nobody had checked them yet.</p><p>The durable set is the 11 waivers plus 14 no-plan homes, minus 3 whose later survey never re-cited K0351: <b>22 homes</b>.</p>", f2),
 ("Where they are", "<p>23 states. Indiana has 15, all cited in 2026, average 35 days old. Missouri has 7, every one a waiver, average 717 days old. Texas 7, Minnesota 5, Hawaii 4 of only 42 Yes homes in the state.</p>"
  "<p>State counts scale with how many surveys landed right before the snapshot, not with anything about the flag.</p>", f3),
 ("How long they've been open", "<p>Median 49.5 days. 45 of 68 are under 90 days, which is just the normal gap between a citation and a revisit. 15 are over a year: 11 waivers, 3 no-plan homes, 1 with a date that never came.</p>"
  "<p>The oldest row is Eddy Village Green, NY, waived since 2019-10-09, 2,396 days - but a 2025-04-03 survey did not re-cite it, so it reads stale. The oldest that holds is Vermont Veterans' Home, no plan on file since 2023-10-25, 919 days.</p>"+table, f4),
]
footer=("Sources: LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME (flag, LANDING PROCESSING_DATE 2026-05-01) and HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES "
        "(K-tags, PROCESSING_DATE 2026-06-01). Every query in <code>queries.py</code>, results in <code>results.json</code>. Python door, SELECT only. "
        "The hunch's listed tables (NURSINGHOME411, NURSING_HOME_DEFICIENCIES) hold neither the flag nor any K-tag.")
write_story(D+"story.html","The sprinkler checkbox that can't say No",lede,sections,footer,
            hero=[("14,638 / 14,700","homes flagged Yes; no No value exists"),("67","Yes homes with an open K0351 on flag day"),("22","hold up after a stale-row check: 14 no plan + 8 waiver"),("3","looked open but a later survey did not re-cite")])
print("wrote story.html")
