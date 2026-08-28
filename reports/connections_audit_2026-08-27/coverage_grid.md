# Connection-Layer Coverage Audit — 2026-08-27

Read-only audit of LIBRARY_MARTS via the guarded read lane (`viz.sqlrun`).
Key detection: `connect/keys.py` (`detect_key` + `TABLE_COLUMN_KEYS`), STEEL tier only,
applied to all 37,223 mart columns across 1,143 objects (32 domain schemas after
excluding CORE / REFERENCE / FINDINGS / REVIEW / PUBLIC / OPEN_DATA / TIMELINE /
INVESTIGATIONS / DBT_CROGERS / _RESTORE_* infrastructure schemas).

Note: the brief said "13 STEEL families"; the live tagger declares more — 24 distinct
STEEL families actually appear in mart columns (the FEC/FRS/MINE/spine-batch adds since
the original 13). All are shown.

## 1. Domain x STEEL-key-family grid (count = tables in the domain carrying that family; `.` = ZERO)

| DOMAIN | tables | keyed% | BIOGUIDE | CCN | CIK | CL_COURT | CL_PERSON | COMPANY_NO | DEA_NO | DUNS | EIN | FEC_CAND | FEC_CMTE | FRS_ID | ICE_FAC | ICPSR | IMO | LEI | MINE_ID | MMSI | NCUA | NPDES | NPI | PATENT | PWSID | UEI |
|---|---:|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MARITIME | 1 | 100.0 | . | . | . | . | . | . | . | . | . | . | . | . | . | . | 1 | . | . | 1 | . | . | . | . | . | . |
| CRIMINAL_JUSTICE | 1 | 100.0 | . | . | . | . | 1 | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . |
| LABOR | 12 | 91.7 | . | . | . | . | . | . | . | . | 8 | . | . | . | . | . | . | . | 3 | . | . | . | . | . | . | . |
| FINANCE | 57 | 66.7 | . | . | 20 | . | . | . | . | . | 11 | 7 | 6 | 3 | . | . | . | 2 | . | . | 4 | . | . | . | . | . |
| HEALTH | 100 | 55.0 | . | 27 | . | . | . | . | 2 | 1 | 1 | . | . | . | . | . | . | . | . | . | . | . | 34 | 1 | . | . |
| ECONOMICS | 47 | 51.1 | . | . | 3 | . | . | . | . | 5 | 17 | . | . | . | . | . | . | 2 | . | . | . | . | . | . | . | 6 |
| ENVIRONMENT | 75 | 42.7 | . | . | 1 | . | . | . | . | . | . | . | . | 16 | . | . | . | 1 | . | . | . | 10 | . | . | 8 | 1 |
| IMMIGRATION | 15 | 40.0 | . | 1 | . | . | . | . | . | . | . | . | . | . | 3 | . | . | . | . | . | . | . | 2 | . | 1 | . |
| PROCUREMENT | 5 | 40.0 | . | . | . | . | . | . | . | 1 | . | . | . | . | . | . | . | . | . | . | . | . | 1 | . | . | 2 |
| SCIENCE_RESEARCH | 6 | 33.3 | . | . | . | . | . | . | . | 2 | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | 2 |
| POLITICS | 79 | 32.9 | 15 | . | . | . | . | . | . | . | 5 | 4 | 4 | . | . | 6 | . | . | . | . | . | . | . | . | . | . |
| HOUSING | 18 | 27.8 | . | . | . | . | . | . | . | . | 1 | . | . | . | . | . | . | 4 | . | . | . | . | . | . | . | . |
| CORPORATE_REGISTRY | 11 | 27.3 | . | . | . | . | . | 2 | . | . | 1 | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . |
| SCIENCE | 5 | 20.0 | . | . | . | . | . | . | . | . | 1 | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . |
| JUSTICE | 67 | 19.4 | . | . | . | 3 | 7 | . | . | . | 2 | . | . | . | . | . | 3 | . | . | . | . | . | . | . | . | . |
| ENERGY | 29 | 0.0 | all ZERO |
| EDUCATION | 17 | 0.0 | all ZERO |
| TRANSPORT | 12 | 0.0 | all ZERO |
| HISTORY | 5 | 0.0 | all ZERO |
| CONSUMER_SAFETY | 4 | 0.0 | all ZERO |
| EPSTEIN | 3 | 0.0 | all ZERO |
| GOVERNMENT_RECORDS | 2 | 0.0 | all ZERO |
| CONSUMER_PROTECTION | 1 | 0.0 | all ZERO |
| CIVIL_RIGHTS | 1 | 0.0 | all ZERO |
| FOREIGN_INFLUENCE | 1 | 0.0 | all ZERO |
| GOVERNANCE | 1 | 0.0 | all ZERO |
| HISTORICAL_RECORDS | 1 | 0.0 | all ZERO |
| JUDICIARY | 1 | 0.0 | all ZERO |
| LAND_AND_TERRITORY | 1 | 0.0 | all ZERO |
| LEGAL_ENFORCEMENT | 1 | 0.0 | all ZERO |
| MONEY_FINANCE | 1 | 0.0 | all ZERO |
| REGULATORY | 1 | 0.0 | all ZERO |

Grid-wide: 32 domains x 24 families = 768 cells; 62 are non-zero (92% of cells empty).
17 of 32 domain schemas carry ZERO STEEL keys anywhere (most are 1-table stub schemas,
but ENERGY (29 tables), EDUCATION (17), TRANSPORT (12), CONSUMER_SAFETY (4) are real
whole-domain blind spots — consistent with the 2026-08-05 sweep finding).

## 2. Graph-connectedness ranking

% of a domain's tables carrying at least one STEEL key column (name-detected; presence,
not verified fill):

Top: MARITIME/CRIMINAL_JUSTICE 100% (1 table each), LABOR 91.7%, FINANCE 66.7%,
HEALTH 55.0%, ECONOMICS 51.1%.
Bottom (multi-table domains): JUSTICE 19.4%, SCIENCE 20.0%, CORPORATE_REGISTRY 27.3%,
HOUSING 27.8%, POLITICS 32.9%, and the four all-zero domains above.

### Politics verdict: the "zero" claim is PARTLY refuted, partly stale
- The claim "politics has zero verified cross-family joins" is **no longer literally true
  at the key layer**: 26 of 79 POLITICS mart tables carry STEEL keys — BIOGUIDE (15),
  ICPSR (6), FEC_CAND/CMTE (4+4), and crucially **EIN on 5 tables** (the IRS-527
  political-org tables + FCC licensing).
- Live overlap probe (cheap, distinct-EIN join): the 527 political orgs' 58,916 distinct
  EINs overlap the IRS exempt-org master (CORPORATE_REGISTRY) on only **260 EINs (0.4%)**.
  So the EIN bridge out of politics EXISTS but is nearly dry against the registry we have
  (527s are not exempt-org-BMF entities by nature; the real bridge would be against
  employer/filer EIN universes — SEC, Form 5500, OSHA — untested here).
- BIOGUIDE/ICPSR/FEC keys connect politics tables to EACH OTHER and to FINANCE's FEC
  money marts (FEC_CMTE_ID/FEC_CAND_ID appear in both schemas) — that IS a cross-schema
  join axis. What politics still lacks is any hard key into the corporate/health/labor
  entity world beyond the thin EIN thread. The **state lobbying/campaign layer is fully
  dark**: all CA_LOBBY_*, TX_LOBBY_*, NYC_CFB_* tables (≈2.7M rows combined) carry zero
  STEEL keys — name-only.

## 3. Missed-connection probe (name+zip recall estimate)

Method: 10k-row (or full, if smaller) sample from side A, matched to distinct side-B
pairs on `UPPER(alnum(name)) + ZIP5`. Rough lower bound — no suffix stripping or token
sort, so real fuzzy recall is higher.

| Pair | sample | matched | % |
|---|---:|---:|---:|
| FHLB membership (FINANCE, keyless) x FDIC bank data (LEI-keyed) | 6,327 | 3,076 | **48.6%** |
| OSHA ITA 300A 2024 (LABOR) x IRS exempt-org master (CORPORATE_REGISTRY) | 10,000 | 65 | 0.7% |
| SAM exclusions (PROCUREMENT) x OSHA ITA case detail 2024 (LABOR) | 10,000 | 1 | 0.01% |

Reading: when the two tables actually describe the same universe (banks x banks), plain
name+zip recovers **roughly half the rows** that the hard-key wiring currently leaves
unconnected — that's the recall on the table. When universes barely overlap (employers x
exempt orgs, debarred entities x injury-reporting establishments), name+zip confirms the
overlap really is tiny — the low numbers are population truth, not matcher failure. The
lever is pair SELECTION plus name+zip, not name+zip everywhere.

## 4. Biggest keyless islands (largest mart tables with ZERO STEEL keys)

| rows | table | has name col | has zip col |
|---:|---|---|---|
| 26,250,920 | HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | yes | yes |
| 19,136,434 | HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC | yes | no |
| 17,168,287 | CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS | yes | yes* |
| 12,646,465 | POLITICS.POLITICS__INTL_ELECTIONS_CANADA_CONTRIBUTIONS | yes | yes |
| 12,631,225 | IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA | no | no |
| 10,857,396 | JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL | no | no |
| 10,323,280 | JUSTICE.JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED | no | no |
| 10,070,727 | JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS | yes | no |
| 9,833,260 | HEALTH.HEALTH__FED_FDA_FAERS_INDI | no | no |
| 9,794,971 | CONSUMER_SAFETY.CONSUMER_SAFETY__FED_CPSC_NEISS | no | no |

\* CFPB complaint ZIP is the CONSUMER's zip, not the company's — name-only bridge there.

Caveats:
- "Keyless" = no STEEL-family column by NAME detection + the table-scoped overrides;
  a table can still join via docket/case-number keys the STEEL set doesn't cover
  (the FJC IDB / CourtListener trio likely links internally on docket IDs — CL tables
  outside the CL_*_ID columns read keyless here even when linked by construction).
- Row counts are INFORMATION_SCHEMA metadata (views count as NULL/0); presence of a key
  column says nothing about fill — the COUNT(DISTINCT) rule still applies before trusting
  any cell of this grid as a live join.

Probe scripts + raw grid JSON: scratchpad (session-local); regenerate from
INFORMATION_SCHEMA + connect/keys.py in ~1 min, <$0.10.
