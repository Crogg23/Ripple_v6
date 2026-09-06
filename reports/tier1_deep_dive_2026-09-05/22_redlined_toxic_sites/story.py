"""Build story.html for hunch 22 from results.json (written by queries.py). No warehouse calls."""
import json, os
import plotly.graph_objects as go
from _shared.viz import PAL, base_fig, bar_style, write_story
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json")))

GR = ["A", "B", "C", "D", ""]
LBL = {"A": "A  best", "B": "B  still desirable", "C": "C  declining", "D": "D  hazardous (redlined)", "": "no grade"}
area = {r["G"]: float(r["KM2"]) for r in R["landing_area_by_grade"]}
j23 = {r["G"]: r for r in R["landing_join_by_grade"]}
jall = {r["G"]: r for r in R["landing_join_facility_table"]}
pw = {r["G"]: r for r in R["landing_polys_with_site"]}
for g in GR: j23.setdefault(g, {"SITES": 0, "LBS": 0})
x = [LBL[g] for g in GR]

# 1. density, two ways
d23 = [j23[g]["SITES"] / area[g] for g in GR]
dall = [jall[g]["SITES"] / area[g] for g in GR]
f1 = base_fig("Redlined land holds 10x to 180x the toxic-site density of the best-graded land",
              "Toxic Release Inventory sites per km² of 1930s HOLC polygon, 10,153 parsed polygons in 314 cities")
f1.add_bar(name="Reporting in 2023 (21,870 sites)", x=x, y=d23, marker_color=PAL[0],
           text=[f"{v:.4f}" for v in d23], textposition="outside",
           hovertemplate="%{x}<br>%{y:.4f} sites per km²<br>" + "<extra>2023 reporters</extra>")
f1.add_bar(name="Ever on the TRI facility list (48,193 with usable coordinates)", x=x, y=dall, marker_color=PAL[1],
           text=[f"{v:.2f}" for v in dall], textposition="outside",
           hovertemplate="%{x}<br>%{y:.4f} sites per km²<extra>all facilities</extra>")
f1.update_layout(barmode="group", yaxis_title="sites per km²", showlegend=True)
bar_style(f1)

# 2. share of polygons touched
pct = [float(pw[g]["PCT"]) for g in GR]
f2 = base_fig("1 in 7 redlined neighborhoods has a toxic site inside it; 1 in 1,000 A-graded ones does",
              "Share of HOLC polygons containing at least one 2023-reporting TRI site")
f2.add_bar(x=x, y=pct, marker_color=[PAL[0]] * 4 + [PAL[3]], text=[f"{v:.1f}%" for v in pct], textposition="outside",
           hovertemplate="%{x}<br>%{y:.1f}% of polygons<br>%{customdata[0]} of %{customdata[1]}<extra></extra>",
           customdata=[[pw[g]["POLYS_WITH_SITE"], pw[g]["POLYS"]] for g in GR])
f2.update_layout(yaxis_title="% of polygons with a site", yaxis_ticksuffix="%")
bar_style(f2)

# 3. pounds per km2, with the single biggest site split out
ex = {r["G"]: r for r in R["landing_lbs_excl_top1_per_grade"]}
base = []; top = []
for g in GR:
    tot = float(j23[g]["LBS"] or 0)
    rest = float(ex[g]["LBS_MINUS_BIGGEST"]) if g in ex else tot
    base.append(rest / area[g]); top.append((tot - rest) / area[g])
f3 = base_fig("Pounds released follow the same ladder: 6,900 lb per km² on redlined land, zero on A",
              "2023 total releases (pounds, grams converted) per km² of HOLC polygon; darker slice = the single biggest site in that grade")
f3.add_bar(name="all other sites", x=x, y=base, marker_color=PAL[0], hovertemplate="%{x}<br>%{y:,.0f} lb/km² from all other sites<extra></extra>")
f3.add_bar(name="biggest single site", x=x, y=top, marker_color=PAL[7], hovertemplate="%{x}<br>%{y:,.0f} lb/km² from the one biggest site<extra></extra>")
f3.add_scatter(x=x, y=[b + t for b, t in zip(base, top)], mode="text", text=[f"{b + t:,.0f}" for b, t in zip(base, top)],
               textposition="top center", showlegend=False, hoverinfo="skip")
f3.update_layout(barmode="stack", yaxis_title="pounds per km²", showlegend=True)
bar_style(f3)

# 4. top 10 cities, sites per km2 by grade
rows = R["landing_city_grade"]
cities = []
for r in rows:
    c = (r["CITY"], r["STATE"])
    if c not in cities: cities.append(c)
cities = cities[:10]
f4 = base_fig("In 9 of the 10 busiest cities D is the densest grade; A-graded land has zero sites in all 10",
              "2023-reporting TRI sites per km² by HOLC grade, cities ranked by sites inside graded polygons")
for i, g in enumerate("ABCD"):
    ys = []; cd = []
    for c in cities:
        r = next((r for r in rows if (r["CITY"], r["STATE"]) == c and r["G"] == g), None)
        ys.append(r["SITES"] / float(r["KM2"]) if r and float(r["KM2"]) > 0 else 0)
        cd.append([r["SITES"] if r else 0, r["KM2"] if r else 0])
    f4.add_bar(name=LBL[g], x=[f"{c[0]}, {c[1]}" for c in cities], y=ys, marker_color=PAL[i], customdata=cd,
               hovertemplate="%{x}<br>" + LBL[g] + ": %{y:.3f} sites/km² (%{customdata[0]} sites in %{customdata[1]} km²)<extra></extra>")
f4.update_layout(barmode="group", yaxis_title="sites per km²", showlegend=True, height=520)
bar_style(f4)

lede = ("In the 1930s the federal Home Owners' Loan Corporation (HOLC) drew maps of 300-odd cities and graded every neighborhood "
        "A (best) to D (hazardous) for mortgage risk, the D areas outlined in red: redlining. The EPA's Toxic Release Inventory (TRI) "
        "is the list of factories and plants that must report the pounds of listed chemicals they release each year. "
        "What follows is an association between a 1930s grade and today's plants, not a cause: HOLC graded land next to industry as hazardous partly because it was next to industry. "
        "We dropped every 2023-reporting TRI site onto every HOLC polygon and asked: does the 1930s grade still predict who lives next to a plant?")
hero = [("448 vs 1", "2023 TRI sites inside D polygons vs inside A polygons"),
        ("10x to 180x", "D over A, sites per km², depending on how you count"),
        ("17x", "D over A, 2023 release pounds per km² within 500 m")]
sections = [
    ("The gap, two ways", "<p>Blue counts the 21,870 facilities that filed a 2023 TRI report and sit inside a polygon. Orange counts every facility on "
     "the EPA's TRI list, open or closed, with a usable coordinate. Both divide by the land area of the polygons in that grade, so a grade with more "
     "or bigger neighborhoods gets no free lift.</p><p>Grade A is one site in 1,366 km², so the blue A bar is nearly a rounding error; the orange "
     "series (58 sites in A) gives the more stable ratio, <b>10.5x</b>. Strict 2023-only is 182x on one site.</p>"
     "<p>The tallest bar is land HOLC never graded: 817 polygons, mostly industrial, commercial and vacant land. That's where the plants "
     "were in 1935 and still are.</p>", f1),
    ("How many neighborhoods are touched", "<p>Density can be driven by a few busy polygons. This asks a blunter question: of all polygons in a grade, "
     "how many have a plant inside at all?</p><p>The ladder is monotone: A 0.1%, B 1.8%, C 6.5%, D 13.6%. One in seven redlined neighborhoods "
     "has a reporting plant inside its 1930s boundary; one in a thousand A neighborhoods does.</p>", f2),
    ("Pounds, not just sites", "<p>Site counts could hide a gradient in the other direction if D-area plants were smaller. They aren't. Total 2023 "
     "releases per km²: A 0, B 506, C 1,431, D 6,856. Per-site medians don't grade (B 255 lb, C 507, D 305), so the pounds gap is a count gap, "
     "not a bigger-plant gap.</p><p>A's zero is a single site; n=1. Widen to a 500 m ring around each polygon and every grade has real counts: A 1,137, B 2,981, C 10,601, D 19,670 lb/km², D over A <b>17x</b>.</p><p>The red slice is the single biggest site in each grade. D's is a Cleveland steelworks at 7.6M lb; strip it and D "
     "still sits at 4,600 lb/km², more than three times C.</p>", f3),
    ("City by city", "<p>The ten cities with the most sites inside graded polygons. In nine of them the D density beats A and B; Akron is the "
     "exception, where its C belt holds the plants. Grade A land has zero 2023 sites in every one of the ten.</p>"
     "<p>Cleveland is the starkest: 20 sites in 55 km² of D land, 8 in 143 km² of C, none in 103 km² of A and B.</p>", f4),
]
footer = ("Sources: LIBRARY_RAW.LANDING.FED_MAPPING_INEQUALITY (10,154 HOLC polygons, GeoJSON; TRY_TO_GEOGRAPHY parsed 10,153, all counts on those), "
          "ENVIRONMENT__FED_EPA_TRI_BASIC_2023 (78,647 chemical rows, 21,870 facilities, decimal lat/lon), "
          "ENVIRONMENT__FED_EPA_TRI_FACILITY (64,990 facilities; FAC_LATITUDE/LONGITUDE packed DDMMSS, converted; 48,193 usable). "
          "The HOUSING__FED_MAPPING_INEQUALITY mart keeps one polygon per (city, grade), 1,155 rows, an 11% slice; it was not used for the numbers. "
          "Point-in-polygon via ST_CONTAINS; area via ST_AREA. Grams converted at 453.592 g/lb. Queries in queries.py, log in queries.log.")
write_story(os.path.join(HERE, "story.html"), "Redlined in 1935, Toxic in 2023", lede, sections, footer, hero)
print("wrote story.html")
