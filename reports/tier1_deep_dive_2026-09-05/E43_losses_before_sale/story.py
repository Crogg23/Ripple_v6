"""Build story.html from results.json. Run from repo root with PYTHONPATH=reports/tier1_deep_dive_2026-09-05."""
import json, os
import plotly.graph_objects as go
from _shared.viz import PAL, TEXT2, base_fig, bar_style, write_story

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json")))
one = lambda k: R[k][0]

base = one("base_all"); fair = {r["GRP"]: r for r in R["fair_full_year"]}
before = one("before_cohort"); naive = one("repro_naive")
sold_full = fair["sold, full-year report before sale"]; not_sold_full = fair["not sold, full-year report"]

# ---- chart 1: the loss rate, four ways ----
labels = ["First pass (naive join,\n137 report rows)", "Last report before sale\n(88 hospitals)",
          "Full-year report only\n(62 hospitals)", "Not sold in the window,\nfull year (5,782)"]
vals = [naive["PCT"], before["PCT_LOSING"], sold_full["PCT"], not_sold_full["PCT"]]
cols = [PAL[1], PAL[1], PAL[1], PAL[0]]
f1 = base_fig("Sold hospitals lose money 1.6x as often as hospitals not sold in the window",
              "Share of hospitals with negative net income on their last cost report before the sale, FY2023-24")
f1.add_trace(go.Bar(x=[l.replace("\n", "<br>") for l in labels], y=vals, marker_color=cols,
                    text=[f"{v:.0f}%" for v in vals], textposition="outside",
                    hovertemplate="%{x}<br>%{y:.1f}% losing money<extra></extra>"))
f1.update_yaxes(title="losing money (%)", range=[0, 75], ticksuffix="%")
bar_style(f1)

# ---- chart 2: margin distribution, sold vs everyone else ----
mb = R["margin_buckets"]
buckets = sorted({r["BUCKET"] for r in mb})
nice = [b[3:] for b in buckets]
f2 = base_fig("Sold hospitals sit left of everyone else: median margin -1.6% vs +1.5%",
              "Net margin on the last report before the sale (88 sold) vs all other hospitals (6,015); share of each group")
for i, grp in enumerate(["sold, year before", "all other hospitals"]):
    rows = {r["BUCKET"]: r["N"] for r in mb if r["GRP"] == grp}
    tot = sum(rows.values())
    ys = [100 * rows.get(b, 0) / tot for b in buckets]
    f2.add_trace(go.Bar(name=f"{grp} (n={tot:,})", x=nice, y=ys, marker_color=PAL[1 - i],
                        text=[f"{y:.0f}%" for y in ys], textposition="outside",
                        hovertemplate="%{x}<br>%{y:.1f}% of " + grp + "<extra></extra>"))
f2.update_yaxes(title="share of group (%)", ticksuffix="%", range=[0, 55])
f2.update_xaxes(title="net margin bucket")
bar_style(f2)

# ---- chart 3: the stub trap ----
h = R["before_len_hist"]
f3 = base_fig("25 of the 88 'before' reports are the seller's stub, ending the day before the sale",
              "Each dot is one sold hospital: how long its last pre-sale cost report ran, and its margin. Red = short period")
full = [r for r in h if r["FY_LEN"] >= 300]; short = [r for r in h if r["FY_LEN"] < 300]
for name, rows, col in [("full year (300+ days)", full, PAL[0]), ("short period (<300 days)", short, PAL[7])]:
    f3.add_trace(go.Scatter(name=name, mode="markers", x=[r["FY_LEN"] for r in rows],
                            y=[100 * (r["NET_MARGIN_RATIO"] or 0) for r in rows],
                            marker=dict(color=col, size=9, opacity=0.8),
                            customdata=[[r["FAC_NAME"], r["DAYS_TO_SALE"]] for r in rows],
                            hovertemplate="%{customdata[0]}<br>report length %{x} days, ends %{customdata[1]} day(s) before sale<br>margin %{y:.1f}%<extra></extra>"))
f3.add_hline(y=0, line_color=TEXT2, line_width=1)
f3.update_xaxes(title="days covered by the report"); f3.update_yaxes(title="net margin (%)", ticksuffix="%")

# ---- chart 4: CHOW_DT is an effective date ----
dow = {r["DOW"]: r["N"] for r in R["chow_dow"]}
order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
f4 = base_fig("The sale date lands on weekends 25% of the time: it is the deal's effective date, not a filing date",
              "Day of week of CHOW_DT, all 1,248 provider ownership changes since 2015 in the POS file", height=380)
f4.add_trace(go.Bar(x=order, y=[dow.get(d, 0) for d in order], marker_color=[PAL[0]] * 5 + [PAL[1]] * 2,
                    text=[dow.get(d, 0) for d in order], textposition="outside",
                    hovertemplate="%{x}: %{y} ownership changes<extra></extra>"))
f4.update_yaxes(title="ownership changes")
bar_style(f4)

lede = ("CMS records when a hospital changes hands, and every hospital files a yearly cost report with its profit or loss. "
        "The first pass said 60% of hospitals sold in FY2022-24 were losing money the year before. "
        "That number is real, but a third of the losses behind it are the seller's final stub report, which almost always shows red. On full-year reports, mostly 2024 sales with a readable prior report, the honest number is 55% against a 34% base rate.")

s1 = ("<p>A CCN is the Medicare certification number that identifies one hospital across every CMS file. "
      "The Provider of Services file (POS_OTHER) keeps one row per CCN with the date of its most recent change of ownership, CHOW_DT. "
      "'Sold' here means a hospital-category CCN with a CHOW_DT in 2022-2024: 128 hospitals.</p>"
      "<p>The cost-report file (HCRIS) holds one report per hospital, fiscal years ending late 2022 through 2024. "
      "Net income below zero is 'losing money'.</p>"
      f"<p>The first pass joined the two and got {naive['LOSING_ROWS']} of {naive['ROWS_']} report rows losing, {naive['PCT']}%. "
      "That join fans out (some hospitals have two reports) and counts reports filed after the sale. "
      f"Fixed to one report per hospital, the last one ending before the sale: {before['LOSING']} of {before['HOSPITALS']}, {before['PCT_LOSING']}%. "
      f"Full-year reports only: {sold_full['LOSING']} of {sold_full['N']}, {sold_full['PCT']}%. "
      f"Hospitals not sold in the window, full-year report: {not_sold_full['PCT']}%. The 62 are mostly 2024 sales (55 of 62; 2024 alone 28 of 55, 50.9%). 40 of the 128 sold have no readable prior report and are out.</p>")

s2 = (f"<p>Rates hide how deep the hole is. Median net margin on the sold group's last pre-sale report is {100*before['MED_MARGIN']:.1f}%; "
      f"for every other hospital it is +{100*base['MED_MARGIN']:.1f}%.</p>"
      "<p>The sold group is not just tilted, it is bunched in the -10% to 0% band. Few of them were catastrophes; most were quietly bleeding.</p>"
      "<p>Mix does not explain it. Re-weighting the base rate by facility type (short-term, rehab, psych, long-term, critical access) gives an expected 36%. "
      "Re-weighting by ownership type gives 36% too. For-profit corporations are 39 of the 88 and their base rate is 33%.</p>")

s3 = ("<p>When a hospital is sold, the old owner closes its books and files a cost report that ends the day before the deal. "
      "Twenty-six of the 88 pre-sale reports are shorter than 300 days, and 25 of those end exactly one day before CHOW_DT.</p>"
      "<p>Short periods look worse everywhere: across all of HCRIS, 65% of sub-180-day reports show a loss versus 34% of full years. "
      "Five rehab hospitals sold on 2023-03-01 filed 58-day stubs, one at a -78% margin.</p>"
      "<p>So the fair test is full year against full year: 55% vs 34%. Still 1.6x, and with 62 hospitals it is about 3.4 standard deviations from chance.</p>")

s4 = ("<p>The hunch's watch-out was whether CHOW_DT is the transaction date or the date CMS processed the paperwork. "
      "Processing dates never fall on a Saturday or Sunday. These do, 318 of 1,248. And 75% land on the 1st of a month, which is how deals are dated. "
      "This is the effective date the parties put on the CMS-855A, the closest thing to a transaction date in any CMS file.</p>"
      "<p>Is a CHOW a sale at all, or paperwork inside one system? A name check says sale: 53 of the 88 hospitals carry a different name today than on their pre-sale report "
      "(Tenet's Orange County hospitals became UCI Health, Steward's St. Anne's became Brown University Health, Everest's rehab hospitals became Mercy and Liberty). "
      "Those 53 lose money 64% of the time; the 21 that kept their name exactly, 48%.</p>"
      "<p>It is still one date per hospital. A hospital sold twice keeps only the later date, so a 2023 sale that flipped again in 2025 is not in the 128.</p>")

hero = [(f"{sold_full['PCT']:.0f}%", "sold hospitals losing money, full-year report before sale"),
        (f"{not_sold_full['PCT']:.0f}%", "every other hospital, full-year report"),
        (f"{before['PCT_LOSING']:.0f}%", "the first pass's 60%, reproduced on 88 hospitals"),
        ("26", "of 88 pre-sale reports are short; 25 end the day before the sale")]

footer = ("Sources: LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER (44,429 rows, one per CCN; CHOW_DT) and HEALTH__FED_CMS_HCRIS (6,103 cost reports, 6,040 CCNs, FY ending 2022-11 to 2024-09; NET_INCOME, NET_MARGIN_RATIO). "
          "Sold = PRVDR_CTGRY_CD '01' and CHOW_DT in 2022-2024 (128 CCNs; 88 have a report ending before the sale, 40 do not: 33 only after, 7 none). "
          "Queries: <code>queries.py</code>, log in <code>queries.log</code>. Built 2026-09-05.")

write_story(os.path.join(HERE, "story.html"), "E43. Sold hospitals were already bleeding", lede,
            [("60% is real, 55% is fair", s1, f1),
             ("How deep the hole was", s2, f2),
             ("The stub-report trap", s3, f3),
             ("Is CHOW_DT the sale date?", s4, f4)], footer, hero)
print("wrote story.html")
