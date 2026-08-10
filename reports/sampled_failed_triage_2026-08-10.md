# Sampled + failed source triage — 2026-08-10

Recon over the 1,569 'sampled' and 268 'failed' catalog rows after the landed
backlog hit zero.

## The big picture
- **~98% of both piles is the portal crawl universe** (auto-probed ArcGIS/CKAN
  portal datasets, ids `portal_arc_*` / `portal_cka_*`): every sampled portal
  row is capped at exactly 10,000 rows by the probe design; the failed ones are
  dead dataset links (404s on data.gov.au / open.canada.ca / Finland), broken
  city GIS endpoints, and JSON parse errors. These were bulk reconnaissance,
  not curated sources. Whether to complete, re-probe, or drop this universe is
  a where-does-the-light-point call → Chris (RED lane), not a session default.

## The actionable non-portal remainder (18 sources)

Failed (12):
| source | state | next step |
|---|---|---|
| intl_uk_fcdo_sanctions_list | 58k landed, last run failed | diagnose loader; likely fixable |
| fed_hhs_taggs | 45 rows | REDUNDANT (decided 2026-08-10 evening): HHS grants are already held in full via the USASpending assistance corpus; no loader rebuild. Drop-list candidate. |
| fed_fda_device_classification / maude_device_events / caers_food_events / faers_drug_events / device_enforcement | 1 row each | five openFDA corpora; API loaders failed at first page — rewrite against bulk downloads |
| fed_dol_wage_hour | nothing landed | KEY-GATED — waiting on Chris's API signup |
| fed_fcc_broadband | nothing landed | big geodata; scope decision first |
| fed_phmsa_flagged_incidents | nothing landed | pipeline incidents; loader diagnose |
| xc_housestockwatcher | nothing landed | community House-trades mirror; check if site still exists |
| fed_dol_olms | nothing landed | union filings; loader diagnose |

Sampled (6):
| source | sample | full size |
|---|---|---|
| fed_fdic_sod_branch_deposits | 10k | millions — branch-level deposits, high value, bulk CSV exists |
| fed_usgs_3dep | 5k | elevation tiles — probably fine as sample; geo infra |
| fed_dol_ofccp_csal | 2k | small full file exists |
| fed_epa_superfund_site_boundaries | 2k | full GIS export exists |
| fed_atf_ffl_locations | 2k | full FFL list exists (also modeled separately) |
| intl_bd_datagov | 500 | portal-probe-like; low value |

## Also still open from this session
- DTCC participant directory: site 403-blocks scripted downloads; needs a
  manual browser download (tiny xlsx) or a header-spoofing retry.
- FinCEN BOI + CMS hospital-price 1-row tables: not re-ingestable
  (legally restricted / wrong-shaped source), stay on the drop list.
