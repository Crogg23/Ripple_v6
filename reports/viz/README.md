# Standalone visualization pages

Self-contained HTML — open any file directly in a browser, no server, no internet
required (Google Fonts degrade to system monospace offline; everything else is inline).
Data is baked in at build time; each page's footnote states its data window and caveats.

Built 2026-08-22 from live warehouse extracts. The matching Claude-artifact copies are
convenience mirrors; **these files are the durable originals.**

| file | what it shows |
|---|---|
| ratemap.html | every county colored by opioid dose/resident or EPA facilities/1k |
| pillrivers.html | top 3,532 distributor→pharmacy opioid routes, animated 2006–2012 |
| heartbeat.html | all 342 sources' monthly pulse + live freshness states (the monitor) |
| denialgap.html | mortgage denial rates by race × income, 2007–2017 |
| waitingroom.html | immigration-detention survival curves, 2.6M stints |
| detrivers.html | detention Sankey: country → state → outcome |
| ownclock.html | corporate ownership links switching on/off + growing network |
| pulsegrid.html | 80×80 source correlation heatmap on the shared clock |
| bankdeserts.html | 76k bank branches: deposit glow / density / desert distance |
| moneyshape.html | 84M donations: Benford, magnet amounts, limit bunching |

Rebuild path: extraction scripts + templates live in the session scratchpad pattern —
data extracts (`extract_viz_data.py`, `extract_wave2.py`, `extract_wave3.py`) produce
JSONs, templates hold a `__PLACEHOLDER__` per dataset, injection = string replace.
Freshness states come from `LIBRARY_META.REGISTRY.SOURCE_FRESHNESS_TIMELINE`.
