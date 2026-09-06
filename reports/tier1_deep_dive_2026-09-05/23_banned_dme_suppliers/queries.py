"""Hunch 23 - money collected by LEIE-excluded DME suppliers. Every query that feeds findings.md and story.html.
Run from repo root: PYTHONPATH=reports/tier1_deep_dive_2026-09-05 python3 reports/tier1_deep_dive_2026-09-05/23_banned_dme_suppliers/queries.py
"""
import json, datetime
import plotly.graph_objects as go
from _shared.q import run, open_log
from _shared.viz import PAL, base_fig, bar_style, write_story

D = "reports/tier1_deep_dive_2026-09-05/23_banned_dme_suppliers"
open_log(f"{D}/queries.log")
S = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL"
L = "LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE"
LS = "LIBRARY_RAW.LANDING.FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL"
LL = "LIBRARY_RAW.LANDING.FED_HHS_OIG_LEIE"
PAID = "try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_PYMT_AMT"   # the file carries an AVERAGE per service, not a total

# 1. vintage + shape
shape = run(f"select count(*) n, count(distinct SUPLR_NPI) npis, sum({PAID}) paid, sum(try_to_number(TOT_SUPLR_SRVCS)*AVG_SUPLR_MDCR_ALOWD_AMT) allowed from {S}", "supplier file shape + money")[0]
ing = run(f"select to_varchar(min(_INGESTED_AT)) mi, to_varchar(max(_INGESTED_AT)) ma from {LS}", "supplier landing ingest date")[0]
leie = run(f"""select count(*) n, count(distinct NPI) npis, sum(iff(NPI='0000000000',1,0)) sentinel,
  sum(iff(nullif(trim(NPI),'') is null,1,0)) blank_npi, sum(iff(nullif(trim(UPIN),'') is null,1,0)) blank_upin,
  max(try_to_date(EXCLDATE, 'YYYYMMDD')) max_excl, min(INGESTED_AT) raw_ingest
  from {LL}""", "LEIE landing shape, sentinel, blanks")[0]
leie_mart = run(f"select count(*) n, sum(iff(NPI='0000000000',1,0)) sentinel, count(distinct iff(NPI_IS_REAL, NPI, null)) real_npis, sum(iff(WAS_REINSTATED,1,0)) reinstated from {L}", "LEIE mart shape")[0]

# 2. the join, on NPI only - real NPIs, no sentinel, no blank
hits = run(f"""
with m as (select SUPLR_NPI, max(SUPLR_PRVDR_LAST_NAME_ORG) org, max(SUPLR_PRVDR_STATE_ABRVTN) st,
             sum({PAID}) paid, sum(try_to_number(TOT_SUPLR_SRVCS)) srvcs, count(*) hcpcs_rows from {S} group by 1),
     e as (select NPI, min(EXCLUSION_DATE) excl, count(*) excl_rows, max(EXCLUSION_TYPE) etype, max(BUSINESS_NAME) bname, max(STATE) lstate
             from {L} where NPI_IS_REAL and nullif(trim(NPI),'') is not null and NPI<>'0000000000' group by 1)
select m.SUPLR_NPI npi, m.org, m.st, round(m.paid) paid, m.srvcs, m.hcpcs_rows, e.excl, e.excl_rows, e.etype, e.bname, e.lstate
from m join e on m.SUPLR_NPI=e.NPI order by m.paid desc""", "excluded suppliers matched on NPI")
EX = "(" + ",".join(f"'{h['NPI']}'" for h in hits) + ")"
split = run(f"""with m as (select SUPLR_NPI, sum({PAID}) paid from {S} group by 1)
select iff(SUPLR_NPI in {EX},'excluded','other') grp, count(*) n, round(sum(paid)) paid, round(median(paid)) med from m group by 1""", "file money split excluded vs other")

# 3. rebuild a different way: business-name match instead of NPI
name = run(f"""with m as (select SUPLR_NPI, upper(max(SUPLR_PRVDR_LAST_NAME_ORG)) org, max(SUPLR_PRVDR_STATE_ABRVTN) st, sum({PAID}) paid from {S} group by 1),
 e as (select distinct upper(regexp_replace(BUSINESS_NAME,'[^A-Z0-9 ]','')) bn, NPI, STATE, EXCLUSION_DATE from {L} where nullif(trim(BUSINESS_NAME),'') is not null)
select m.SUPLR_NPI npi, m.org, m.st, round(m.paid) paid, e.NPI leie_npi, e.STATE leie_st, e.EXCLUSION_DATE excl, iff(m.SUPLR_NPI=e.NPI,'npi','name only') how
from m join e on regexp_replace(m.org,'[^A-Z0-9 ]','')=e.bn order by paid desc""", "name-only match as the cross-check")

# 4. rank of the hits in the whole file
top = run(f"""with m as (select SUPLR_NPI, max(SUPLR_PRVDR_LAST_NAME_ORG) org, max(SUPLR_PRVDR_STATE_ABRVTN) st, sum({PAID}) paid from {S} group by 1)
select SUPLR_NPI npi, org, st, round(paid) paid, iff(SUPLR_NPI in {EX},1,0) excluded, rank() over (order by paid desc) rk from m qualify rk<=12 order by rk""", "top 12 suppliers in the file")

# 5. what they billed, and their share of each code
codes = run(f"""select HCPCS_CD, max(HCPCS_DESC) d, count(distinct SUPLR_NPI) npis, round(sum({PAID})) paid,
  round(sum(iff(SUPLR_NPI in {EX}, {PAID}, 0))) paid_excl,
  sum(try_to_number(TOT_SUPLR_BENES)) benes, sum(iff(SUPLR_NPI in {EX}, try_to_number(TOT_SUPLR_BENES), 0)) benes_excl
  from {S} group by 1 order by paid desc limit 8""", "top 8 HCPCS with the excluded share")
hit_codes = run(f"""select SUPLR_NPI npi, HCPCS_CD, try_to_number(TOT_SUPLR_BENES) benes, try_to_number(TOT_SUPLR_SRVCS) srvcs, round({PAID}) paid
  from {S} where SUPLR_NPI in {EX} order by paid desc""", "the hits by HCPCS")
cath = run(f"""select iff(SUPLR_NPI in {EX},'excluded','other') grp, count(*) suppliers,
  round(median(try_to_number(TOT_SUPLR_SRVCS)/nullif(try_to_number(TOT_SUPLR_BENES),0)),0) med_per_bene,
  sum(try_to_number(TOT_SUPLR_BENES)) benes, round(sum({PAID})) paid from {S} where HCPCS_CD='A4353' group by 1""", "A4353 catheters: excluded vs other")

# 6. exclusion timing
pre = run(f"""select count(distinct NPI) npis, count(distinct iff(IS_ENTITY_NOT_INDIVIDUAL, NPI, null)) orgs,
 count(distinct iff(IS_ENTITY_NOT_INDIVIDUAL and (upper(SPECIALTY) like '%DME%' or upper(SPECIALTY) like '%DURABLE%' or upper(SPECIALTY) like '%MEDICAL EQUIP%' or upper(SPECIALTY) like '%SUPPL%'), NPI, null)) dme_orgs
 from {L} where NPI_IS_REAL and NPI<>'0000000000' and nullif(trim(NPI),'') is not null and EXCLUSION_DATE < '2026-01-01'""", "pre-2026 real-NPI exclusions: orgs, DME orgs")[0]
aa = run(f"""select count(*) n, sum(iff(year(EXCLUSION_DATE)=2026,1,0)) y2026, sum(iff(EXCLUSION_DATE between '2026-06-19' and '2026-06-28',1,0)) june_window,
 sum(iff(EXCLUSION_DATE between '2026-06-19' and '2026-06-28' and upper(SPECIALTY) like 'DME%',1,0)) june_dme from {L} where EXCLUSION_TYPE='1128Aa'""", "1128Aa shape")[0]
unb = run(f"""select SUPLR_NPI npi, max(SUPLR_PRVDR_LAST_NAME_ORG) org, max(SUPLR_PRVDR_STATE_ABRVTN) st, sum(try_to_number(TOT_SUPLR_BENES)) benes, sum(try_to_number(TOT_SUPLR_SRVCS)) srvcs, round(sum({PAID})) paid
 from {S} where HCPCS_CD='A4353' and SUPLR_NPI not in {EX} group by 1 order by paid desc limit 3""", "biggest unbanned A4353 billers")
yrs = run(f"select year(EXCLUSION_DATE) y, count(distinct iff(NPI_IS_REAL, NPI, null)) npis from {L} where EXCLUSION_DATE>='2016-01-01' group by 1 order by 1", "LEIE real-NPI exclusions by year")

json.dump(dict(shape=shape, ing=ing, leie=leie, leie_mart=leie_mart, hits=hits, split=split, name=name, top=top, codes=codes,
               hit_codes=hit_codes, cath=cath, yrs=yrs, pre=pre, aa=aa, unb=unb), open(f"{D}/results.json", "w"), indent=1, default=str)

# ---------- charts ----------
M = lambda v: v / 1e6
# chart 1: top 12 suppliers, excluded in red
f1 = base_fig("One banned supplier out-billed every DME supplier in America: $860M",
              "Medicare paid, top 12 of 55,598 suppliers. Red = on the OIG exclusion list by NPI. File ingested 2026-07-26, no year column.", 520)
labels = [f"{t['ORG'][:28]} ({t['ST']})" for t in top][::-1]
vals = [M(t['PAID']) for t in top][::-1]
cols = [PAL[7] if t['EXCLUDED'] else PAL[0] for t in top][::-1]
f1.add_bar(x=vals, y=labels, orientation="h", marker_color=cols, name="Medicare paid",
           text=[f"${v:,.0f}M" if v > 300 else "" for v in vals], textposition="outside",
           hovertemplate="%{y}<br>$%{x:,.1f}M<extra></extra>")
f1.add_bar(x=[None], y=[None], marker_color=PAL[7], name="excluded (LEIE, NPI match)")
f1.add_bar(x=[None], y=[None], marker_color=PAL[0], name="not excluded")
almaz = [t for t in top if t['NPI']=='1487343505'][0]
f1.add_annotation(x=M(almaz['PAID']), y=f"{almaz['ORG'][:28]} ({almaz['ST']})", text=f"not excluded - ${unb[0]['PAID']/1e6:,.0f}M of it catheters, {unb[0]['SRVCS']/unb[0]['BENES']:,.0f} per patient", showarrow=True, ax=120, ay=0, font=dict(size=12, color=PAL[0]), xanchor="left")
f1.update_layout(xaxis_title="Medicare paid, $ millions", margin=dict(l=240), showlegend=True, barmode="overlay")
bar_style(f1)

# chart 2: exclusion date vs the data
f2 = base_fig("All eight were banned in one ten-day window - June 2026, after the money moved",
              "Exclusion date per matched supplier vs. the day the payment file landed. Bubble = Medicare paid.", 420)
f2.add_scatter(x=[h['EXCL'] for h in hits], y=[h['ORG'][:26] for h in hits], mode="markers",
               marker=dict(size=[max(10, (h['PAID'] / 1e6) ** 0.5 * 2.2) for h in hits], color=PAL[7], opacity=.85),
               name="exclusion date", hovertemplate="%{y}<br>excluded %{x}<br>$%{customdata:,.0f}M<extra></extra>",
               customdata=[M(h['PAID']) for h in hits])
f2.add_vline(x=datetime.date(2026, 7, 26), line_dash="dot", line_color=PAL[0])
f2.add_annotation(x=datetime.date(2026, 7, 26), y=1.02, yref="paper", text="payment file ingested 2026-07-26", showarrow=False, font=dict(color=PAL[0], size=12), xanchor="right")
f2.update_layout(xaxis=dict(range=[datetime.date(2026, 6, 10), datetime.date(2026, 8, 5)], title="2026"), margin=dict(l=220), showlegend=False)

# chart 3: share of each product code
f3 = base_fig("The eight took 64% of every catheter dollar and 62% of every wound-dressing dollar",
              "Medicare paid by product code, split by whether the supplier is now excluded. Top 8 codes in the file.", 480)
cx = [c['HCPCS_CD'] for c in codes]
f3.add_bar(x=cx, y=[M(c['PAID_EXCL']) for c in codes], name="excluded suppliers", marker_color=PAL[7],
           hovertemplate="%{x}<br>excluded: $%{y:,.0f}M<extra></extra>")
f3.add_bar(x=cx, y=[M(c['PAID'] - c['PAID_EXCL']) for c in codes], name="everyone else", marker_color=PAL[0],
           hovertemplate="%{x}<br>others: $%{y:,.0f}M<extra></extra>")
for c in codes:
    if c['PAID_EXCL']:
        f3.add_annotation(x=c['HCPCS_CD'], y=M(c['PAID']), text=f"{c['PAID_EXCL']/c['PAID']:.0%}", showarrow=False, yshift=12, font=dict(color=PAL[7]))
f3.update_layout(barmode="stack", yaxis_title="Medicare paid, $ millions", xaxis_title="HCPCS product code")
bar_style(f3)

# ---------- story ----------
tot = shape['PAID']; ex = [s for s in split if s['GRP'] == 'excluded'][0]; oth = [s for s in split if s['GRP'] == 'other'][0]
a4353 = [c for c in codes if c['HCPCS_CD'] == 'A4353'][0]; a6197 = [c for c in codes if c['HCPCS_CD'] == 'A6197'][0]
cx_ex = [c for c in cath if c['GRP'] == 'excluded'][0]; cx_ot = [c for c in cath if c['GRP'] == 'other'][0]
twin = [n for n in name if n['HOW'] == 'name only' and n['PAID'] > 1e7]
lede = (f"Medicare's public file of durable medical equipment suppliers (one row per supplier and product code, {shape['N']:,} rows, "
        f"ingested 2026-07-26, no year column) was matched against the HHS Inspector General's exclusion list on NPI, the ten-digit "
        f"National Provider Identifier. Eight suppliers match. Together they were paid <b>${ex['PAID']/1e9:.2f} billion</b> - "
        f"{ex['PAID']/tot:.1%} of every DME dollar in the file - and every one of them was excluded in June 2026, after the billing.")
sections = [
    ("$860M, one company", 
     f"<p>Sunshine Senior Solutions LLC of Florida, NPI 1811518392, was paid <b>${hits[0]['PAID']/1e6:,.0f} million</b> across "
     f"{hits[0]['HCPCS_ROWS']} product codes. That is rank 1 of {shape['NPIS']:,} suppliers, nearly twice the next one. "
     f"The match is on NPI and the business name agrees on both sides ({hits[0]['BNAME']}, {hits[0]['LSTATE']}).</p>"
     f"<p>Seven more excluded suppliers were paid between $9M and $116M each. Median paid for the eight: ${ex['MED']/1e6:,.0f}M. Median for the other {oth['N']:,}: ${oth['MED']:,.0f}.</p>",
     f1),
    ("Banned after, not before",
     f"<p>Every one of the eight carries exclusion type 1128Aa, dated between "
     f"{min(h['EXCL'] for h in hits)} and {max(h['EXCL'] for h in hits)}. The payment file landed 2026-07-26 and covers an earlier "
     f"calendar year (CMS publishes it a year or more in arrears; the file itself carries no year). So the money was collected "
     f"<b>before</b> the ban. None of the {pre['NPIS']:,} suppliers excluded before 2026 appears in the file - expected, since only {pre['DME_ORGS']} of them are DME organizations.</p>"
     f"<p>1128Aa is a rare code with one shape: {aa['N']} rows in the whole list, {aa['JUNE_WINDOW']} of them in this ten-day window, all {aa['JUNE_DME']} DME businesses. The eight are part of one batch.</p>"
     f"<p>The hunch as written - 'banned suppliers still collected' - is backwards. And <b>the pattern is wider than the ban</b>: at least three unbanned suppliers bill the same way. "
     f"{unb[0]['ORG']} ({unb[0]['ST']}) is rank 2 in the whole file with ${unb[0]['PAID']/1e6:,.0f}M in catheters at {unb[0]['SRVCS']/unb[0]['BENES']:,.0f} per patient; {unb[1]['ORG']} ({unb[1]['ST']}) ${unb[1]['PAID']/1e6:,.0f}M; {unb[2]['ORG']} ({unb[2]['ST']}) ${unb[2]['PAID']/1e6:,.0f}M. ${sum(u['PAID'] for u in unb)/1e6:,.0f}M of catheter money sits outside the eight.</p>",
     f2),
    ("What they sold",
     f"<p>Two product codes carry the story. A4353 is an intermittent urinary catheter with insertion supplies; A6197 is a large alginate wound dressing. "
     f"The eight took ${a4353['PAID_EXCL']/1e6:,.0f}M of ${a4353['PAID']/1e6:,.0f}M in catheter payments and "
     f"${a6197['PAID_EXCL']/1e6:,.0f}M of ${a6197['PAID']/1e6:,.0f}M in dressings.</p>"
     f"<p>On catheters, six excluded suppliers billed for {cx_ex['BENES']:,} patients. The other {cx_ot['SUPPLIERS']} suppliers combined billed for {cx_ot['BENES']:,}. "
     f"Per-patient volume does not separate them (median {cx_ex['MED_PER_BENE']:,.0f} vs {cx_ot['MED_PER_BENE']:,.0f} catheters a year); the patient count does.</p>",
     f3),
]
twin_txt = '; '.join(f"{t['ORG']} ({t['ST']}, NPI {t['NPI']}, ${t['PAID']/1e6:,.0f}M)" for t in twin)
footer = (f"Tables: {S} ({shape['N']:,} rows, landing ingested {ing['MI'][:10]}); {L} ({leie_mart['N']:,} rows, {leie_mart['REAL_NPIS']:,} real NPIs; "
          f"landing holds {leie['SENTINEL']:,} '0000000000' NPI sentinels and {leie['BLANK_UPIN']:,} blank UPINs, both excluded from the match). "
          f"Money = TOT_SUPLR_SRVCS x AVG_SUPLR_MDCR_PYMT_AMT summed per supplier; the file carries averages, not totals. "
          f"Cross-check by business name instead of NPI: {sum(1 for n in name if n['HOW']=='npi')} of the 8 re-found, ${sum(n['PAID'] for n in name if n['HOW']=='npi')/1e9:.2f}B ({sum(n['PAID'] for n in name if n['HOW']=='npi')/ex['PAID']:.0%}); the two misses are a 30-char name truncation and an INC suffix. Plus "
          f"{twin_txt} matching by name and state but under a different NPI. "
          f"Python door, SELECT only. Queries in queries.py, log in queries.log.")
hero = [(f"${ex['PAID']/1e9:.2f}B", "paid to 8 now-excluded suppliers"), (f"{ex['PAID']/tot:.1%}", "of all DME dollars in the file"),
        (f"${hits[0]['PAID']/1e6:,.0f}M", "Sunshine Senior Solutions alone"), ("June 2026", "when all 8 were excluded")]
write_story(f"{D}/story.html", "Banned DME suppliers: $1.43 billion, collected first, banned after", lede, sections, footer, hero)
print("story written")
