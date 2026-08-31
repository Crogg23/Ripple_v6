# Ripple Library vs "World's Top 75 Issues (2026)" — Coverage + Onboarding Plan
*2026-06-27. Two independent passes reconciled: (A) 73/75 catalog-aware web-recon scout agents, (B) claude.ai Opus deep-research on the 29 gaps.*
*Full per-issue recon → `issue_scout_DETAIL_2026-06-27.md`. Deep-research prompt → `deep_research_prompt_GAPS_2026-06-27.md`.*

---

## Bottom line
- You're **not starting from zero on 49 of 75 issues.** 3 are already served by landed data, 5 partially, and **38 map to sources already sitting in the registry as `scouted` — those are "load it" jobs, not "find it" jobs.**
- Only **29 are true gaps**, and the two research passes **independently converged on the same flagship source for almost all of them** → high confidence. Where they differed, the in-house run usually found the *more onboardable* option because it knew the Snowflake/dbt stack and optimized for keyless+bulk.
- **26 of the 29 gaps are onboardable right now.** Only ~3 angles have no clean machine-readable source (live IAEA stockpile numbers, UN child grave-violations counts, military recruiting goals-vs-actuals) — proxies named below.

## Coverage at a glance
| Tier | Count | Meaning | Action |
|---|---|---|---|
| ✅ HAVE | 3 | Real data already serving it | Extend |
| 🟡 PARTIAL | 5 | Some data landed, incomplete | Top up |
| 📇 SCOUTED → LOAD | 38 | Source already in registry, not loaded | **Just run the loader** |
| ⬜ GAP | 29 | Nothing — needed fresh scouting (now done) | Onboard the new pick |

---

## Deep-research vs in-house: the verdict

**They AGREE on the flagship source (high confidence — onboard these without second-guessing):**

| Issue | Both passes landed on | Onboard as |
|---|---|---|
| #4 Russia-NATO hybrid war | Harvard Dataverse "Russian Operations Against Europe" (DOI 10.7910/DVN/TQ0FMQ) | `intl_leiden_russian_ops_europe` — bulk XLSX |
| #6 North Korea | CNS/NTI Missile Test DB (note: **frozen Apr 2026**) | `intl_nti_cns_dprk_missile_tests` — bulk XLSX |
| #8/#39/#43 Sahel / Extremism / Ethiopia | **UCDP GED** over ACLED (keyless, CC-BY, redistributable) | `intl_ucdp_ged` — bulk CSV |
| #15 Wealth inequality | WID.world + Fed Distributional Financial Accounts | `intl_wid` + `fed_frb_dfa_wealth` |
| #33 AI governance | AI Incident Database | `xc_aiid_incidents` — weekly snapshot |
| #34 Disinformation | EUvsDisinfo Zenodo CSV (record 10514307) | `intl_euvsdisinfo_zenodo` — CSV |
| #35 Cybersecurity | CISA KEV (CC0 / public domain) | `fed_cisa_kev` — JSON/CSV |
| #49 Human trafficking | CTDC Global Victim dataset | `xc_ctdc_global_victims` — CSV |
| #54 Abortion | Guttmacher + Society of Family Planning #WeCount | `xc_guttmacher_abortion` (+ `xc_wecount`) |
| #55/#56 LGBTQ+ / Trans | ACLU + Trans Legislation Tracker, **backed by LegiScan** | `fed_legiscan_bills` |
| #50 Child welfare (malnutrition) | UNICEF/WHO/WB Joint Malnutrition Estimates (CC-BY 3.0 IGO) | `intl_unicef_jme` (SDMX) |
| #73 Book bans | PEN America Index | `fed_pen_book_bans` — Google-Sheets CSV export |

**Where the IN-HOUSE run found a BETTER (more onboardable) source than deep-research:**

| Issue | Deep-research said | In-house found (better) | Why better |
|---|---|---|---|
| #18 AI bubble | IEA Energy&AI (free login, **projections**) | **PNNL IM3 Data Center Atlas** — open CSV+GeoPackage, real US datacenters w/ lat-lon+FIPS | actuals, keyless, has join keys |
| #36 Tech monopoly | StatCounter usage share | **2022 Economic Census concentration (HHI by NAICS)** + FTC merger data | measures actual market concentration |
| #29 AMR | ECDC EARS-Net (EU only) | **WHO GHO AMR OData API** (global, keyless) | global coverage, clean API |
| #74 Fed-vs-state | NCSL (scrape) | **Open States / Plural bulk** (keyless, public-domain) + Harvard cannabis dataset | bulk download, no scrape |
| #5 Iran | IAEA PDFs only | + IPFM facilities + GeoNuclearData + OWID warheads | structured proxies exist |

**Genuinely net-new from deep-research — worth folding in:**
- **#25/#70 Veteran suicide** → both passes agree: VA National Suicide Prevention **data appendices** (XLSX, public domain) `fed_va_veteran_suicide_appendix`, plus VA SAIL hospital performance
- **#26/#71 Military recruitment** → in-house found an open **DoD Accession ZIP-Code Profile** (recruits-by-ZIP CSV) `fed_dod_accession_zip_profile` — better than deep-research's "press-release only" read. DoD QMA youth-eligibility (deep-research) is still the best *propensity* angle. Only goals-vs-actuals-by-service remains press-release-only.
- **#29 AMR** → ECDC EARS-Net + CDC NARMS as the *EU + US complements* to WHO GHO
- **#35 Cyber** → VERIS VCDB (community breach incidents) as a backup to KEV
- **#21 Abortion** → #WeCount adds the telehealth/shield-law angle Guttmacher is thinner on

---

## Load-first queue (clean, keyless / public-domain — highest ROI)
*107 EASY+keyless candidates total; this is the first wave by impact × cleanliness.*

**New gaps, load now (CC0 / CC-BY / public domain, bulk or clean API):**
1. `fed_cisa_kev` — CISA Known Exploited Vulnerabilities (CC0, daily) — #35
2. `intl_ucdp_ged` — UCDP conflict events (CC-BY) — backbone for #1/#8/#39/#43
3. `xc_aiid_incidents` — AI Incident Database — #33
4. `intl_euvsdisinfo_zenodo` — disinformation cases — #34
5. `xc_ctdc_global_victims` — human-trafficking victims — #49
6. `intl_wid` + `fed_frb_dfa_wealth` — wealth inequality — #15
7. `fed_pnnl_datacenter_atlas` — AI datacenter buildout — #18
8. `fed_census_econ_concentration` — market concentration HHI — #36
9. `intl_nti_cns_dprk_missile_tests` — DPRK missile/nuclear tests — #6
10. `intl_leiden_russian_ops_europe` — Russia hybrid-war incidents — #4
11. `fed_pen_book_bans` — school book bans — #73
12. `fed_openstates_bills` — state legislation (also powers #55/#56) — #74
13. `xc_guttmacher_abortion` + `xc_wecount` — abortion provision — #54
14. `intl_ipc_food_insecurity_global` — famine/IPC — #3/#20
15. `intl_unhcr_refugee` — refugees/displacement — #7/#21/#44

**Already-scouted "just load it" wins (38 total — top accountability hits):**
`fed_atf_firearms_trace` (#51 guns) · `fed_dea_arcos` (#48 opioids) · `fed_bop_statistics` (#53 prisons) · `fed_eac_eavs` + `xc_medsl_mit` (#59 voting) · `fed_cfpb_hmda` (#61 lending bias) · `fed_fec_api` (#60 campaign finance) · `fed_nces_ccd`/`naep` (#46/#75 education) · `fed_hud_data` (#45/#72 housing/homelessness) · `fed_eia_api` (#28/#67 energy/grid) · `fed_usgs_water` (#25/#68 water) · `fed_nass_quickstats` (#69 ag) · `fed_ssa_statistics` (#65 social security) · `fed_samhsa_nsduh` (#31 mental health) · `intl_un_comtrade`/`intl_cepii_baci` (#10/#16 trade) · `intl_vdem`/`intl_freedomhouse` (#37 democracy)

**Extend what you HAVE:**
- #32 healthcare → add `fed_census_sahie` (uninsured rates) + `fed_hrsa_shortage_areas`
- #9 exec power → add `fed_opm_plum_positions` (the political-appointee "PLUM book")
- #57 SCOTUS → add `fed_courtlistener` opinions
- #60/#61 → add `xc_opensecrets_bulk`, `fed_eeoc_charges`

---

## Verify before you load (flags from the reconciliation)
- **ACLED is redistribution-restricted** — both passes flag it. Fine to ingest for analysis; you cannot re-share raw rows. **Add a `redistribution_restricted` boolean to the registry** and prefer **UCDP GED** anywhere output is public.
- **License copyleft:** EUvsDisinfo Zenodo is **CC BY-SA** (ShareAlike obligation). Cleanest licenses: UCDP GED, CISA KEV (CC0), UNICEF JME (CC-BY 3.0 IGO), all US-gov sources.
- **Frozen/stale (don't treat as live):** GTD terrorism (ends 2020, now gated → use UCDP/ACLED instead), CNS NK DB (frozen Apr 2026), X/Twitter influence-ops archive (~2021).
- **PDF/scrape-only — no clean feed (proxy or skip):** IAEA Iran stockpile numbers, UN MRM child grave-violations counts, military recruiting goals-vs-actuals, GERD/Nile, Lebanon parallel-currency rates.
- **WHO GHO AMR** carries only a thin AMR slice (MRSA/E.coli) via the keyless OData API — confirm indicator coverage; pair with ECDC EARS-Net (EU) for depth.
- **Projections ≠ actuals:** if you ever use IEA energy figures, store the scenario label. (The PNNL atlas avoids this — prefer it.)

## What's NOT worth chasing (honest stops)
Live foreign-conflict casualty feeds (#1/#2/#3/#5/#7) — there is no redistributable real-time casualty dataset; UCDP GED (annual + monthly candidate) + UNHCR displacement is the ceiling. Tech *antitrust actions* (#36) have no clean feed — concentration metrics are the proxy. Trans *health outcomes* (#56) — only the legislation side is onboardable. UN MRM child grave-violation counts (#50) and IAEA Iran stockpile numbers (#5) are PDF-only. Military recruiting *goals-vs-actuals by service* (#71) is press-release-only — but recruits-by-ZIP and youth-propensity data are onboardable.
