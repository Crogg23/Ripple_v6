| 1 | Hotspot analysis (Getis-Ord Gi*) | GIS | ✅ Ready | county and tract centroids plus population give both the neighbour rule and the rate denominator |
| 2 | Kernel Density Estimation (KDE) | GIS | ✅ Ready | the only technique here that needs nothing built first — check row grain before plotting |
| 3 | Spatial autocorrelation (Moran's I) | GIS | ✅ Ready | distance-band weights from existing centroids; the shuffle-test code is already running elsewhere |
| 4 | Voronoi diagrams | GIS | ✅ Ready | not the dud the catalog assumes — bank branches and water systems genuinely own their ground |
| 5 | Aggregate first (histograms/heatmaps/hexbins) | Scatter readability | ✅ Ready | 252 tables over 1M rows with real groupers and real numeric measures; 14 rollups already exist |
| 6 | Encode density not position | Scatter readability | ✅ Ready | 122 tables have genuinely numeric coordinates; the biggest is 58.1M points |
| 7 | Dimension reduction (PCA/t-SNE) | Scatter readability | ✅ Ready | 10 tables carry a 20+ measure vector on 50k+ rows — but watch the exact duplicate twin |
| 8 | Epidemiology → contact tracing graphs | Raided | ✅ Ready | one table already IS contact tracing — 2.57M person-stints with book-in and book-out times |
| 9 | Astronomy → sky surveys / N-body clustering | Raided | ✅ Ready | 58M-point cloud is real, but it is one week of pings — a photograph, not a survey |
| 10 | Ecology → food web / trophic cascade | Raided | ✅ Ready | directed multi-hop chains exist in one ID namespace — shipments, ownership, mine controllers |
| 11 | Music/Audio → spectrograms | Raided | ✅ Ready | one pharmacy, drugs down the side, 84 months across the bottom — straight out of one table |
| 12 | Finance → correlation matrices / heatmap clustering | Raided | ✅ Ready | 403 sources already counted per day on one shared axis; the matrix input is prebuilt |
| 13 | Topological Data Analysis (TDA) | Physics | ✅ Ready | dense numeric point clouds exist; the distance rule is arithmetic you write, not a table you need |
| 14 | Network centrality | Physics | ✅ Ready | real entity-to-entity edge lists exist, and degree is already computed for 33.3M entities |
| 15 | Entropy / information density | Physics | ✅ Ready | 403 tables now share one clock column, so one query shape runs warehouse-wide |
| 16 | Mass (density/heatmaps/bubble/contour) | Organism | ✅ Ready | coordinates, place codes and 2020 population denominators all present at county and tract |
| 17 | Distance (clustering, dimension reduction over join-key relatedness) | Organism | ✅ Ready | cluster on the source registry's own feature columns, not on the 0.1%-sampled edge map |
| 18 | Circulation (network / force-directed graphs) | Organism | ✅ Ready | several real edge lists — but the two biggest are sealed islands with no way out |
| 19 | Flow maps | GIS | 🟡 Partial | drawable today at county resolution; ZIP resolution needs one small model, no new data |
| 20 | Sample or tier by zoom | Scatter readability | 🟡 Partial | every rung of the ladder exists, but no boundary shape exists, so zoom gives bigger dots not filled areas |
| 21 | Neuroscience → connectome mapping | Raided | 🟡 Partial | runs inside the opioid network today; cannot run across the warehouse, the islands don't touch |
| 22 | Percolation theory | Physics | 🟡 Partial | valid on the opioid shipment network; on the connection map it would measure the sampler |
| 23 | Ripples (diffusion/propagation animation) | Organism | 🟡 Partial | no spine edge carries a world clock; the dated graphs that exist are mostly sealed |
