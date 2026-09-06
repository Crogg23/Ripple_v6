"""Build story.html for hunch 27 from results*.json (no warehouse calls).
Run: PYTHONPATH=reports/tier1_deep_dive_2026-09-05 python3 reports/tier1_deep_dive_2026-09-05/27_pending_applicants_banned/build_story.py"""
import json, os
import plotly.graph_objects as go
from _shared.viz import PAL, TEXT2, base_fig, bar_style, write_story

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json")))
R2 = json.load(open(os.path.join(HERE, "results2.json")))
R3 = json.load(open(os.path.join(HERE, "results3.json")))
R4 = json.load(open(os.path.join(HERE, "results4.json")))  # state base rates for the 7 charted states, no limit

TYPE_WORDS = {
    "1128a1": "conviction: program-related crime",
    "1128a3": "felony: health care fraud",
    "1128a4": "felony: controlled substance",
    "1128b4": "license revoked or surrendered",
}
def mand(t): return "mandatory (1128a)" if t.lower().startswith("1128a") else "permissive (1128b)"

# ---- Chart 1: count ladder 12 -> 10 -> 9
rl = R["hits_rowlevel"][0]
f1 = base_fig("The answer is 9 people, not 12 rows", "same join, three ways of counting it")
labels = ["join rows (both files x every exclusion)", "distinct exclusions", "distinct people (NPI)"]
vals = [rl["N_JOIN_ROWS"], rl["N_EXCLUSIONS"], rl["N_NPI"]]
f1.add_bar(x=labels, y=vals, marker_color=[PAL[1], PAL[3], PAL[0]], text=vals, textposition="outside",
           hovertemplate="%{x}: %{y}<extra></extra>", showlegend=False)
f1.update_yaxes(title="count", range=[0, 14])
bar_style(f1)

# ---- Chart 2: timeline of the 10 exclusions
hits = R["hits"]
f2 = base_fig("All 10 exclusions are still active; the oldest is 13 years old",
              "one dot per exclusion row, 9 people; snapshot: pending list 2026-07-26, LEIE Aug 2026")
seen = set()
for grp, color in [("mandatory (1128a)", PAL[7]), ("permissive (1128b)", PAL[0])]:
    rows = [h for h in hits if mand(h["EXCLUSION_TYPE"]) == grp]
    f2.add_scatter(
        x=[h["EXCLUSION_DATE"] for h in rows],
        y=[f'{h["P_LAST"].title()} ({h["STATE"]})' for h in rows],
        mode="markers+text", name=grp, marker=dict(size=14, color=color),
        text=[f'{h["EXCLUSION_TYPE"]}' for h in rows], textposition="middle right",
        textfont=dict(size=11, color=TEXT2),
        customdata=[[h["EXCLUSION_TYPE"], TYPE_WORDS.get(h["EXCLUSION_TYPE"], ""), h["SPECIALTY"], h["CITY"], h["KIND"]] for h in rows],
        hovertemplate="%{y}<br>%{x}<br>%{customdata[0]} = %{customdata[1]}<br>%{customdata[2]}, %{customdata[3]}<br>pending file: %{customdata[4]}<extra></extra>",
    )
f2.update_yaxes(categoryorder="array", categoryarray=[f'{h["P_LAST"].title()} ({h["STATE"]})' for h in reversed(hits) if not (h["NPI"] in seen or seen.add(h["NPI"]))])
f2.update_xaxes(title="exclusion date", range=["2012-06-01", "2027-06-01"])
f2.update_layout(height=520)

# ---- Chart 3: mandatory vs permissive, hits vs LEIE base
base = {r["GRP"]: r["N"] for r in R2["leie_mand_perm"]}
base_tot = sum(base.values())
# hits by person, latest exclusion decides (Louisville: 2024 mandatory)
latest = {}
for h in hits:
    latest[h["NPI"]] = h
hp = {"mandatory (1128a)": 0, "permissive (1128b)": 0}
for h in latest.values(): hp[mand(h["EXCLUSION_TYPE"])] += 1
f3 = base_fig("7 of 9 are mandatory exclusions (felony or fraud conviction)",
              "share by exclusion class: the 9 applicants vs every real-NPI row in LEIE")
cats = ["mandatory (1128a)", "permissive (1128b)"]
f3.add_bar(name="the 9 pending applicants", x=cats, y=[100*hp[c]/9 for c in cats], marker_color=PAL[7],
           text=[f"{hp[c]} of 9" for c in cats], textposition="outside", hovertemplate="%{x}<br>%{y:.0f}% (%{text})<extra>the 9</extra>")
f3.add_bar(name=f"all LEIE rows with a real NPI (n={base_tot:,})", x=cats, y=[100*base.get(c,0)/base_tot for c in cats], marker_color=PAL[0],
           text=[f"{base.get(c,0):,}" for c in cats], textposition="outside", hovertemplate="%{x}<br>%{y:.1f}% (%{text} rows)<extra>LEIE base</extra>")
f3.update_yaxes(title="share, %", range=[0, 100])
f3.update_layout(barmode="group")
bar_style(f3)

# ---- Chart 4: state, hits vs pending list vs LEIE
hs = {}
for h in latest.values(): hs[h["STATE"]] = hs.get(h["STATE"], 0) + 1
pend = {r["ST"]: float(r["PCT"]) for r in R4["pending_state7"]}
leie = {r["STATE"]: float(r["PCT"]) for r in R4["leie_state7"]}
states = ["FL", "NC", "NV", "PA", "CA", "TX", "NY"]
f4 = base_fig("Florida is 6 of the 9; it is 12% of the pending list and 10% of LEIE",
              "share by state: the 9 vs all 14,103 pending applicants (NPPES practice state) vs real-NPI LEIE rows")
f4.add_bar(name="the 9 pending applicants", x=states, y=[100*hs.get(s,0)/9 for s in states], marker_color=PAL[7],
           text=[f"{hs.get(s,0)} of 9" if hs.get(s) else "" for s in states], textposition="outside", hovertemplate="%{x}: %{y:.0f}%<extra>the 9</extra>")
f4.add_bar(name="all pending applicants (13,290 with an NPPES state)", x=states, y=[pend.get(s,0) for s in states], marker_color=PAL[0],
           hovertemplate="%{x}: %{y:.1f}%<extra>pending list</extra>")
f4.add_bar(name="all LEIE rows with a real NPI", x=states, y=[leie.get(s,0) for s in states], marker_color=PAL[3],
           hovertemplate="%{x}: %{y:.1f}%<extra>LEIE base</extra>")
f4.update_yaxes(title="share, %", range=[0, 80])
f4.update_layout(barmode="group")
bar_style(f4)

lede = ("CMS publishes a monthly list of people whose first Medicare enrollment application is still being processed. "
        "The HHS Inspector General publishes the LEIE, the list of people currently banned from billing any federal health program. "
        "Both carry an NPI, the 10-digit National Provider Identifier every clinician gets once. "
        "Nine applicants on the July 2026 pending list sit on the August 2026 ban list under the same NPI and the same name. "
        "None has been reinstated. Two are applying on an NPI that CMS deactivated years ago. "
        "Nine is a floor: 89% of LEIE rows carry no NPI at all, and a first-plus-last name match against those finds 450 hits (37 with a matching state), both too noisy to count.")

sec1 = ("<p>The pending list is two files, physicians and non-physicians, 14,120 rows. Seventeen NPIs sit in both files under the same name, "
        "so the real list is 14,103 people. One of the nine, Tommy Louisville, is one of those seventeen and also carries two separate exclusions; "
        "a naive join returns him four times.</p>"
        "<p>Rebuilt two ways: a union-then-dedupe join, and an EXISTS check per file with no union. Both give 9. The first pass holds.</p>"
        "<p>The LEIE mart hides the sentinel: the landing file has 75,001 rows with NPI 0000000000, the mart turns them into blanks. "
        "Filtered either way, the join only touches the 8,660 rows with a real NPI.</p>")

sec2 = ("<p>Every one of the ten exclusion rows is still in force. The LEIE monthly file only lists people currently excluded; "
        "when OIG reinstates someone the row leaves the file. The REINDATE column is 00000000 on all 83,842 landing rows and the mart's "
        "WAS_REINSTATED is false on every row, so the reinstatement question answers itself by construction, not by a check.</p>"
        "<p>Mandatory exclusions (1128a) carry a five-year minimum and never end on their own; the person has to apply to come back. "
        "Hauser and Kushner were excluded in 2013 and are still listed 13 years later. Lewis was excluded in November 2025 and was already excluded when the July 2026 snapshot was taken.</p>"
        "<p>Louisville lost his license in 2020 (1128b4), then picked up a conviction-based exclusion in 2024 (1128a1) on top of it.</p>")

sec3 = ("<p>Seven of nine sit on a mandatory exclusion: a program-related crime conviction, a health care fraud felony, or a controlled-substance felony. "
        "Two are license revocations. Across all LEIE rows with a real NPI, mandatory is 63%. Nine people is too few to call the gap real; "
        "it says the nine are not softer cases than the list at large.</p>"
        "<p>Physician vs non-physician: 6 sit only in the physician file, 2 only in the non-physician file, 1 in both. "
        "The file label is loose. LEIE and NPPES both say Rodriguez is a chiropractor and Salazar-Vust a physician assistant, yet both are in the physician file.</p>")

sec4 = ("<p>Florida is 6 of the 9. Florida is 12% of the pending list and 10% of LEIE, so six of nine is far above either base, "
        "but the base rates say Florida would be the modal state either way. The six Florida cities: Miami twice, Pembroke Pines twice, Jacksonville, Coleman. "
        "The other three are Butner NC, Henderson NV, Leeper PA.</p>"
        "<p>Facility affiliation: none of the nine appears in CMS's physician-to-facility affiliation file. That is the expected miss, not a finding: "
        "only 152 of the 14,103 pending applicants (1.1%) appear there at all, because the file covers people already billing Medicare.</p>"
        "<p>NPPES adds the sharpest fact. Two of the nine NPIs are deactivated: Kushner's since 2015-08-31, Hauser's since 2018-06-19. "
        "NPPES has blanked the name and state on both. A pending Medicare application on a dead NPI is a data-entry error or a bad application; either way it should not be pending.</p>")

hero = [("9", "pending applicants on the ban list"), ("10", "active exclusions, 0 reinstated"), ("7 of 9", "mandatory: felony or fraud"),
        ("6 of 9", "Florida"), ("2 of 9", "NPI deactivated years ago")]

footer = ("Tables: LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS / _NON_PHYSICIANS (landed 2026-07-26), "
          "HEALTH__FED_HHS_OIG_LEIE (max exclusion date 2026-08-20; 83,747 rows, 8,660 real NPIs), HEALTH__FED_CMS_FACILITY_AFFILIATION (2.26M rows), "
          "HEALTH__FED_CMS_NPPES. Queries in <code>queries.py</code>, <code>queries2.py</code>, <code>queries3.py</code>; log in <code>queries.log</code>. "
          "Exclusion codes: 1128a1 program-related crime, 1128a3 health care fraud felony, 1128a4 controlled-substance felony, 1128b4 license revocation. "
          "Names are as published by OIG and CMS.")

write_story(os.path.join(HERE, "story.html"), "Nine pending Medicare applicants are already banned", lede,
            [("Dedupe first", sec1, f1), ("Still banned, all of them", sec2, f2), ("Felony and fraud, not paperwork", sec3, f3), ("Florida, and two dead NPIs", sec4, f4)],
            footer, hero)
print("wrote story.html")
