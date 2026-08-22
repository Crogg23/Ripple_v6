# Visualization Ideas Inventory

*What CAN be visualized from data that is verified clean and usable — running list,
compiled in batches. Started 2026-08-22 (viz sprint session). Each idea names its
exact data substrate and its trust level so a design template can be built against
it without re-verifying. "BUILT" = a working prototype page already exists from the
2026-08-22 sprint.*

**Trust legend:**
- ✅ CLEAN — table/columns verified this month (live queries or the Laboratory map's refute pass)
- ⚠️ CAVEAT — usable, but with a named limit that must appear on the visual
- 🚫 excluded entirely: contract trends (truncated sample), FAERS (column-shift), MSHA deaths,
  EPA penalty dollars (phantom-fines stamping), SEC 13F dollars (scale split), NHTSA (dup risk),
  UK ownership timelines (fixed 8/22 but PSC edge dates unverified since), debarment list.

---

## Batch 1 — compiled 2026-08-22

### A. Opioid shipments (178.6M rows, dated, weighted, from→to; public window 2006–2012) ✅

1. **County dose map** — every county colored by morphine-equivalent dose per resident per year. BUILT (The Rate Map).
2. **Distributor→pharmacy flow arcs** — ZIP-to-ZIP shipment routes over time. BUILT (Pill Rivers).
3. **The firehose finder** — rank pharmacies by dose received vs. their county's population; a scatter of "pharmacy size vs. town size" where the outliers ARE the story (the famous 9M-pill town in WV is findable this way).
4. **Distributor market share river** — stacked share of national dose by distributor company per quarter; shows consolidation and who owned the peak years.
5. **Drug mix shift** — oxycodone vs hydrocodone vs the rest, share per year per state; small-multiple states, spotting states whose mix flips.
6. **The one-pharmacy spectrogram** — pick any pharmacy: drugs down the side, 84 months across, cell = dose. The Laboratory's own "music" technique; substrate confirmed.
7. **Percolation dial** — drop weak shipment routes one threshold at a time and watch the national network shatter into regional islands; the snap threshold is the finding.
8. **Network centrality leaderboard** — which distributors bridge the most pharmacy communities (betweenness on the real shipment graph).

### B. Immigration detention stints (2.57M, real book-in/book-out timestamps) ✅

9. **Survival curves** — % still detained at day 7/30/90/180/365, by year booked in. BUILT (The Waiting Room).
10. **Country → state → outcome Sankey** — where people are from, who held them, how it ended. BUILT (Detention Rivers).
11. **Facility league table with funnel plot** — median stay per facility plotted against facility volume, with uncertainty bands so tiny facilities can't top the chart on noise. Uses the same stint table's facility field.
12. **Bond ladder** — distribution of bond amounts set vs posted; where the "can't afford $5,000" wall sits. Bond columns are typed numbers on the same table (fill rate unverified — check first).
13. **The revolving door** — people with multiple stints (person-hash repeats): gap between release and re-booking as a histogram.

### C. Mortgage applications, 2007–2017 (19.1M rows, race/income/outcome on one row) ✅

14. **Denial gap dot plot** — denial rate by race across income bands. BUILT (The Denial Gap).
15. **Redline echo map** — tract-level denial rate for Black applicants vs the 1930s redlining grades (the redlining polygon mart holds only a 1,155-row sample ⚠️ — works as a city case study, not national).
16. **The gap by lender** — respondent-level: which lenders show the widest same-income racial gap; funnel-plot guard for small lenders.
17. **Denial reason fingerprints** — reason mix by race per state; "collateral" vs "credit history" split reads very differently.
18. **Crash timeline** — application volume + denial rate through 2007–2012, national; the mortgage market's heartbeat through the crash.

### D. Bank branches (76k branches, deposits, coordinates; latest survey) ✅

19. **Deposit glow / density / desert map** — three views. BUILT (Bank Deserts).
20. **Branch catchment population** — assign every census tract to its nearest branch; rank catchments by people-per-branch (Voronoi stats without drawing a polygon). Tract centroids + populations verified.
21. **Bank exit timeline** — the survey is annual back years; branches that vanish year-over-year, mapped as departures per county per year (⚠️ verify all survey years are loaded before designing around it).
22. **HQ vault effect** — deposits booked to headquarters vs street branches; a log-scale strip plot that makes the accounting artifact itself the story.

### E. Corporate ownership, global LEI registry (484k dated edges, typed dates since 8/22) ✅

23. **Ownership switch-on/off clock + growing web**. BUILT (The Ownership Clock).
24. **Chain-length census** — how deep do ownership chains go (parent-of-parent-of-parent); histogram + longest-chain gallery with names.
25. **Cross-border ownership matrix** — country-of-child × country-of-parent heatmap; the offshore corridors light up.
26. **Orphaned subsidiaries** — links that switched OFF with no replacement parent; a timeline of corporate abandonment events.

### F. Consumer complaints (17.2M, product/issue/company/state/date, all verified) ✅

27. **Complaint entropy map** — which states' complaint mix is unusual vs the national mix (the entropy technique's textbook table).
28. **Company response fingerprint** — response type mix per company for the top 100 companies; who closes with relief vs without.
29. **Issue emergence tracker** — new issue-categories appearing and exploding month over month (changepoint detection on category series).
30. **Narrative volume vs outcome** — do complaints with written narratives get different responses; two-rate comparison, no NLP needed.

### G. Warehouse-wide clocks (403 sources on one shared time axis) ✅

31. **Heartbeat wall** — every source's monthly pulse. BUILT.
32. **Pulse correlation grid** — which sources beat together. BUILT (The Pulse Grid).
33. **Calendar-effect scanner** — September fiscal-year-end spikes, election-cycle money wobble, weekend gaps; the 155k-row calendar dimension joins to everything with a clock ⚠️ (calendar table verified present, join untested).
34. **Changepoint gallery** — for each source, the single month its line snapped hardest; a wall of before/after breaks (collection-artifact x-ray, honesty tool for everything else).

### H. Political money (84M itemized contributions, typed amounts + dates) ✅

35. **Money shape** — Benford digits, magnet amounts, threshold bunching, election river. BUILT (The Shape of Money).
36. **The $23 cluster hunt** — recurring-amount donor clusters (the July sweep found one generating a fifth of rows); a treemap of exact-amount "colonies."
37. **Distance-from-limit creep** — how the just-under-the-limit spike migrated as limits rose era over era; animated histogram.
38. **ZIP money vs ZIP denial** — 🅿️ PARKED: needs the mortgage table joined to contributions by geography — cross-table, design later.

### I. Health provider clouds (verified wide numeric tables) ✅

39. **Provider PCA/t-SNE atlas** — 1.3M providers, 49 real measures each, projected to 2D; clusters = practice styles, outliers = billing anomalies. ⚠️ The identical twin table must be excluded or every point doubles.
40. **Hospital funnel plots** — 6,103 hospitals × 107 cost-report measures with volume-based uncertainty bands; the honest "worst in America" guard.
41. **Chronic-condition geography** — the provider table's ~35 condition percentages averaged by county (providers have states/ZIPs); disease-burden maps with no new data.

---

## Parked — worked through 2026-08-22 (this session)

- **UNPARKED: Politics money ↔ votes.** Measured live: 1,530 of 12,794 members carry
  campaign-finance ids — and that matches the SOURCE file exactly (1,530 of 12,768 upstream),
  so nothing was lost in ingest; the ids cover the modern era, which is what the donations
  table covers. End-to-end chain verified: member → committee linkage → 16,451,066 individual
  contributions ($2.14B) reachable. Buildable today; caveat "modern members only" on the visual.
- **UNPARKED: Opioid flows ↔ overdose deaths.** NCHS county drug-poisoning mortality
  (1999–2015, 53,387 rows, 3,141 counties) ingested to landing 2026-08-22 and verified against
  source count. Joins to the county spine by FIPS; joins to opioid shipments by county name
  (same path the Rate Map uses). Caveat: death rate is a BANDED estimate ("12.1–14 per 100k"),
  not an exact count.
- **MEASURED, decision pending: EPA facility ↔ corporate parent bridge.** Fill rate is 1.4% —
  73,948 of 5,300,149 facilities carry a matched corporate id (22,736 distinct companies;
  10,297 with ultimate parent; 8,442 with SEC id; avg match confidence 0.96, zero review flags).
  The map's "fuses the whole 5.3M-facility island" claim is oversold ~70×. Whether a 74k-facility
  bridge justifies the $10–15 spine rebuild is Chris's call.
- Anything on federal contract TRENDS (🚫 truncated sample until re-pull — off-limits list).

---

*Batch 2 candidates (not yet compiled): environment/EPA facility families, water-system
violations spans (14.4M, survival), storm events, workplace injuries with hours-worked
denominators, ER injury narratives (text), court case durations, maritime AIS point cloud,
FracFocus chemicals, GLEIF×SEC overlap. Say "next batch" to continue.*
