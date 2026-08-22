"""Emit the summary table rows for Laboratory_Warehouse_Map.md."""
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
r = json.load(open(os.path.join(ROOT, "reports", "lab_map",
                                "_workflow_result.json"), encoding="utf-8"))

OVERRIDE_TIER = {"Percolation theory": "PARTIAL", "Flow maps": "PARTIAL"}
LABEL = {"READY": "✅ Ready", "PARTIAL": "🟡 Partial",
         "NEEDS_NEW_DATA": "🔴 Needs new data",
         "NEEDS_CLEANUP": "🛠️ Needs cleanup"}
SHORT = {"Making Massive Scatter Plots Readable": "Scatter readability",
         "The Organism Metaphor (Mass / Distance / Circulation / Ripples)": "Organism",
         "Physics-Derived Techniques": "Physics",
         "GIS / Geographic Techniques": "GIS",
         "Other Domains Raided for Ideas": "Raided"}

# One-line reasons, written for the table rather than lifted from the notes.
REASON = {
    "Aggregate first (histograms/heatmaps/hexbins)":
        "252 tables over 1M rows with real groupers and real numeric measures; 14 rollups already exist",
    "Encode density not position":
        "122 tables have genuinely numeric coordinates; the biggest is 58.1M points",
    "Dimension reduction (PCA/t-SNE)":
        "10 tables carry a 20+ measure vector on 50k+ rows — but watch the exact duplicate twin",
    "Sample or tier by zoom":
        "every rung of the ladder exists, but no boundary shape exists, so zoom gives bigger dots not filled areas",
    "Mass (density/heatmaps/bubble/contour)":
        "coordinates, place codes and 2020 population denominators all present at county and tract",
    "Distance (clustering, dimension reduction over join-key relatedness)":
        "cluster on the source registry's own feature columns, not on the 0.1%-sampled edge map",
    "Circulation (network / force-directed graphs)":
        "several real edge lists — but the two biggest are sealed islands with no way out",
    "Ripples (diffusion/propagation animation)":
        "no spine edge carries a world clock; the dated graphs that exist are mostly sealed",
    "Topological Data Analysis (TDA)":
        "dense numeric point clouds exist; the distance rule is arithmetic you write, not a table you need",
    "Percolation theory":
        "valid on the opioid shipment network; on the connection map it would measure the sampler",
    "Network centrality":
        "real entity-to-entity edge lists exist, and degree is already computed for 33.3M entities",
    "Entropy / information density":
        "403 tables now share one clock column, so one query shape runs warehouse-wide",
    "Hotspot analysis (Getis-Ord Gi*)":
        "county and tract centroids plus population give both the neighbour rule and the rate denominator",
    "Kernel Density Estimation (KDE)":
        "the only technique here that needs nothing built first — check row grain before plotting",
    "Spatial autocorrelation (Moran's I)":
        "distance-band weights from existing centroids; the shuffle-test code is already running elsewhere",
    "Voronoi diagrams":
        "not the dud the catalog assumes — bank branches and water systems genuinely own their ground",
    "Flow maps":
        "drawable today at county resolution; ZIP resolution needs one small model, no new data",
    "Epidemiology → contact tracing graphs":
        "one table already IS contact tracing — 2.57M person-stints with book-in and book-out times",
    "Astronomy → sky surveys / N-body clustering":
        "58M-point cloud is real, but it is one week of pings — a photograph, not a survey",
    "Neuroscience → connectome mapping":
        "runs inside the opioid network today; cannot run across the warehouse, the islands don't touch",
    "Ecology → food web / trophic cascade":
        "directed multi-hop chains exist in one ID namespace — shipments, ownership, mine controllers",
    "Music/Audio → spectrograms":
        "one pharmacy, drugs down the side, 84 months across the bottom — straight out of one table",
    "Finance → correlation matrices / heatmap clustering":
        "403 sources already counted per day on one shared axis; the matrix input is prebuilt",
}

out = io.open(os.path.join(ROOT, "reports", "lab_map", "_summary_rows.md"),
              "w", encoding="utf-8")
rows = []
for cat in r["categories"]:
    for t in cat["techniques"]:
        tier = OVERRIDE_TIER.get(t["technique"], t["tier"])
        rows.append((tier, cat["title"], t["technique"]))

order = {"READY": 0, "PARTIAL": 1, "NEEDS_CLEANUP": 2, "NEEDS_NEW_DATA": 3}
rows.sort(key=lambda x: (order[x[0]], x[1]))
for i, (tier, cat, tech) in enumerate(rows, 1):
    out.write("| %d | %s | %s | %s | %s |\n"
              % (i, tech, SHORT.get(cat, cat), LABEL[tier],
                 REASON.get(tech, "")))
out.close()
print("rows:", len(rows))
