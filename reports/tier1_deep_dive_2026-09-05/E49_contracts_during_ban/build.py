"""Build story.html from results*.json (no warehouse calls)."""
import json, html
import plotly.graph_objects as go
from _shared.viz import PAL, base_fig, bar_style, write_story
D = "reports/tier1_deep_dive_2026-09-05/E49_contracts_during_ban"
r1 = json.load(open(f"{D}/results.json")); r2 = json.load(open(f"{D}/results2.json")); r3 = json.load(open(f"{D}/results3.json"))
M = lambda x: f"${x/1e6:,.1f}M"

# 1. money in vs money out
t = r1["hit_total"][0]
f1 = base_fig("Inside a ban, the government mostly takes money back", "Every contract action dated inside a SAM exclusion window, 136 banned companies, 2007-2026")
f1.add_bar(x=["New money obligated", "Money pulled back"], y=[float(t["OBL_POS"]), -float(t["OBL_NEG"])],
           marker_color=[PAL[0], PAL[7]], text=[M(float(t["OBL_POS"])), M(-float(t["OBL_NEG"]))], textposition="outside",
           hovertemplate="%{x}: %{y:$,.0f}<extra></extra>")
f1.add_annotation(x=1, y=-float(t["OBL_NEG"]), text=f"{t['ZERO_ACTIONS']} more actions moved $0", showarrow=False, yshift=-40, font=dict(color="#52514e"))
f1.update_layout(yaxis_title="dollars", showlegend=False, height=440); bar_style(f1)

# 2. positive awards by size, split by started during / before ban
order = ["under $1k", "$1k-10k", "$10k-100k", "$100k-1M", "$1M+"]
pb = r3["pos_award_buckets"]
def series(kind): 
    d = {x["BUCKET"]: x for x in pb if x["KIND"] == kind}
    return [d.get(b, {}).get("AWARDS", 0) for b in order], [float(d.get(b, {}).get("OBL", 0)) for b in order]
c_new, m_new = series("started during ban"); c_old, m_old = series("started before ban")
f2 = base_fig("120 of the 172 awards that started inside a ban are under $10k", "Awards with positive new money inside the window, by award size (sum of in-ban obligations per award)")
f2.add_bar(name="award started during ban", x=order, y=c_new, marker_color=PAL[0], customdata=m_new, text=c_new, textposition="outside",
           hovertemplate="%{x}: %{y} awards, %{customdata:$,.0f}<extra>started during ban</extra>")
f2.add_bar(name="award started before ban (a modification)", x=order, y=c_old, marker_color=PAL[1], customdata=m_old, text=c_old, textposition="outside",
           hovertemplate="%{x}: %{y} awards, %{customdata:$,.0f}<extra>started before ban</extra>")
f2.update_layout(barmode="group", yaxis_title="awards", height=460); bar_style(f2)

# 3. who got the money
u = r3["uei_pos_new"][:10]; tot = sum(float(x["OBL"]) for x in r3["uei_pos_new"])
names = [x["RECIPIENT"].title() for x in u][::-1]; vals = [float(x["OBL"]) for x in u][::-1]
f3 = base_fig("Nova Datacom holds 67% of the money on awards that began inside a ban", f"Top 10 of 37 companies, {M(tot)} over 172 awards that started during the ban")
f3.add_bar(x=vals, y=names, orientation="h", marker_color=[PAL[7] if v > 1e6 else PAL[0] for v in vals],
           text=[M(v) for v in vals], textposition="outside",
           customdata=[[x["EXCL_BY"] or "?", x["EXCL_TYPE"], x["AWARDS"], x["BAN_START"]] for x in u][::-1],
           hovertemplate="%{y}<br>%{x:$,.0f} over %{customdata[2]} awards<br>excluded by %{customdata[0]}: %{customdata[1]}<br>ban began %{customdata[3]}<extra></extra>")
f3.update_layout(xaxis_title="dollars", yaxis=dict(automargin=True), height=520, margin=dict(l=260, r=90)); bar_style(f3)

# 4. when in the ban
lag_order = ["0-7 days", "8-30 days", "31-90 days", "91-365 days", "over a year"]
lg = {x["LAG"]: x for x in r3["lag_new"]}
f4 = base_fig("83 of the 172 awards began more than a year into the ban - not paperwork lag", "Awards that started during the ban, each counted once at its first in-ban action")
f4.add_bar(x=lag_order, y=[lg[k]["AWARDS"] for k in lag_order], marker_color=PAL[0], text=[lg[k]["AWARDS"] for k in lag_order], textposition="outside",
           customdata=[float(lg[k]["OBL"]) for k in lag_order], hovertemplate="%{x}: %{y} awards, %{customdata:$,.0f}<extra></extra>")
f4.update_layout(yaxis_title="awards", showlegend=False, height=440); bar_style(f4)

pk = {x["KIND"]: x for x in r2["pos_kind"]}
lede = ("SAM is the federal do-not-do-business list; USAspending is the ledger of every federal contract action. Matching the two by company id "
        "(the 12-character UEI) finds 1,762 contract actions dated inside a ban across 136 banned companies. But 9 in 10 of those actions "
        "put in zero dollars or took dollars out. The new money is <b>$16.0M on 197 awards to 45 companies</b>. The sharp version: <b>172 awards worth $8.35M began while the company was already on the list</b>, and one company, Nova Datacom, holds 67% of that.")
sections = [
 ("The join, and what it caught",
  f"<p>168,328 exclusion rows in the SAM mart; only 47,686 carry a UEI. That gives 40,680 ban windows (start date to end date, or to today when the ban is open) across 32,998 company ids. 382 of those ids ever appear in the 93M-row USAspending contracts table.</p>"
  f"<p>1,762 actions on 1,390 awards fall inside a window (each action counted once; a company with several overlapping listings is matched to its earliest covering window). Net obligation: <b>{M(float(t['OBL']))}</b>. That negative sign is the finding: {t['ZERO_ACTIONS']} actions are $0 admin entries and most of the rest are de-obligations, terminations, and settlements. ATI Government Solutions alone gave back $52M to the IRS after its October 2025 exclusion.</p>", f1),
 ("The new money is small, and mostly small awards",
  f"<p>Positive money: $16.0M over 218 actions, 197 awards, 45 companies. Median award: $4,725.</p>"
  f"<p>Split it by whether the award's period of performance began after the ban started. <b>{pk['started during ban']['AWARDS']} awards ({M(float(pk['started during ban']['OBL']))}) to {pk['started during ban']['UEIS']} companies started inside the ban</b>: brand-new work handed to a listed company. The other {pk['started before ban']['AWARDS']} awards ({M(float(pk['started before ban']['OBL']))}) are modifications to contracts that existed before the ban, which the rules allow.</p>"
  f"<p>120 of the 172 new-during-ban awards are under $10k: purchase-card-sized buys, not procurements someone vetted.</p>""<p>Eleven awards straddle the line: some of their actions report a period-of-performance start before the ban and some after (USAspending restates the start date on modifications). All eleven are classed 'started before ban' here using the earliest date; only one carries positive money ($100k, Consummate Computer Consultants).</p>", f2),
 ("Who, and under what kind of ban",
  "<p>Inside the 172: Nova Datacom $5.59M on 4 awards, then Bonus Environmental $839k on 14. Take Nova out and $2.76M is spread over 168 awards and 36 companies.</p>""<p>On the wider all-positive set ($16.0M, 197 awards) ATI Government Solutions adds $6.8M, all of it on contracts that predate its October 2025 listing, so it does not appear in this chart. ATI and Nova were both SBA 'Proceedings Pending' listings, meaning a proposed debarment; contracting officers may not award to those either, but it is a softer listing than a completed debarment.</p>"
  "<p>ATI's biggest positive line is a $4.6M 'contract termination settlement': money paid to shut the contract down, not new work. Nova Datacom's $5.1M was 'Option II on IT support' for a DoD counterintelligence agency, on a contract that began six months after its exclusion.</p>"
  "<p>Below the top two: Bonus Environmental got 14 Army awards ($839k) eight to eleven years into an open EPA listing. EPA 'Prohibition/Restriction' listings are often tied to one facility under the Clean Air or Clean Water Act rather than a government-wide ban, so treat those with care.</p>", f3),
 ("Timing rules out the lag excuse",
  "<p>If these were paperwork overlap, the awards would cluster in the first week or month after the ban. 26 awards ($270k) start within 7 days. But 83 of the 172 (48%) begin over a year into the ban, worth $1.45M, and the 91-365 day bucket holds $5.8M, almost all of it Nova Datacom.</p>"
  "<p>Rebuilt a different way, joining on CAGE code instead of UEI (only 435 SAM rows carry one): 540 awards, 74 companies, net -$23.3M, +$1.7M new money. Same shape, smaller lens. The first-pass figure of '17 awards, $43k plus one big one' does not reproduce under any UEI or CAGE cut tried here; the closest match is the 2008 slice alone (48 awards, $42,941), so the first pass likely used a narrower join.</p>", f4),
]
footer = ("Tables: LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS (168,328 rows, all RECORD_STATUS='Active', so past bans already purged from SAM are invisible) and "
          "LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FULL_R2 (93,153,424 rows, columns UPPERCASE in this R2 copy). Window = ACTIVATION_DATE to TERMINATION_DATE, open bans end today; activation dates outside 2000..today dropped. "
          "Money = FEDERAL_ACTION_OBLIGATION per action, each landing row counted once even when a company carries several overlapping listings; 'started during ban' = PERIOD_OF_PERFORMANCE_START_DATE on or after ban start. Every query in <code>queries.py</code>, <code>queries2.py</code>, <code>queries3.py</code>; log in <code>queries.log</code>.")
hero = [("172", "awards began inside a ban"), ("$8.35M", "on those 172, to 37 companies"), ("67%", "of that is one company, Nova Datacom"), ("-$102.0M", "net of all in-ban actions: bans mostly pull money back")]
write_story(f"{D}/story.html", "Contracts during the ban", lede, sections, footer, hero)
print("ok")
