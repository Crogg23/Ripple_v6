# What the 2026-08-18 spine rebuild actually connected

Rebuild completed 10:57 PDT, exit 0. 33,283,474 entities (16,859,563 in 2+
sources) over 173 sources from 83,722,388 nodes.

## Headline finding: the spine has the new families; the connection map cannot see them

The spine build reads the live warehouse. The graph re-measure reads a cached
schema snapshot (outputs/connect_fingerprints.json), which was last built
2026-08-09 -- BEFORE the five new key axes were registered.

Result: all five new axes are tagged on ZERO tables in that snapshot, so they
produce ZERO edges in the map, while the spine resolved them fine.

    axis            tables tagged in map snapshot    entities in spine
    CL_PERSON_ID    0                                16,232
    CL_COURT_ID     0                                 3,361
    NPDES_ID        0                             1,213,740
    NCUA_CHARTER    0                                 4,339
    ICE_FACILITY    0                                 1,492

Secondary: the snapshot covers 1,273 of 2,212 live landing tables. 941 have
never been profiled and are structurally invisible to the map.

Fix for both: re-run `python -m connect fingerprint` (targeted or full), then
`python -m connect discover`. Not yet scoped for cost.

## Spine key axes, by multi-source rate

    key             entities    in 2+ sources     %     max sources
    FRS_ID          5,404,011   3,424,872       63.4    14
    NPI             9,608,798   3,212,841       33.4    19
    EIN             3,411,514   3,202,452       93.9    20
    LEI             3,384,590   3,140,917       92.8     3
    COMPANY_NO      8,506,743   2,335,951       27.5     2
    NPDES_ID        1,213,740     781,875       64.4     8
    PWSID             434,040     432,073       99.5     9
    UEI               685,266     149,850       21.9     6
    CCN                82,060      59,247       72.2     7
    MINE_ID            91,906      31,428       34.2     3
    FEC_CMTE_ID        26,842      23,272       86.7     6
    CL_PERSON_ID       16,232      15,674       96.6     8
    CIK               181,305      15,030        8.3    16
    BIOGUIDE           12,781      12,584       98.5     5
    DUNS               29,664       6,849       23.1     2
    FEC_CAND_ID        13,855       5,898       42.6     3
    NCUA_CHARTER        4,339       4,336       99.9     4
    CL_COURT_ID         3,361       2,767       82.3     3
    ICE_FACILITY        1,492         705       47.3     2
    ICPSR              12,677         639        5.0     2
    IMO                 9,014         303        3.4     2
    DEA_NO            149,244           0        0.0     1

DEA_NO is single-source: 149,244 entities, zero cross-source merges. It is a
dead axis today -- carried by exactly one table, so it connects nothing.

## The new families, table by table

CL_PERSON_ID (judges) -- 8 tables:
  JUDGES 16,191 / POSITIONS 15,613 / EDUCATIONS 7,398 /
  POLITICAL_AFFILIATIONS 7,226 / RACES 6,521 /
  FINANCIAL_DISCLOSURES 3,381 / DOCKETS 3,350 / ORIGINATING_COURT_INFO 1,520

CL_COURT_ID -- 3 tables: COURTS 3,361 / DOCKETS 2,199 / POSITIONS 1,033

NPDES_ID (water permits) -- 8 tables, a full enforcement chain:
  ICIS_FACILITIES 1,213,737 / QNCR_HISTORY 690,126 / INSPECTIONS 286,752 /
  INFORMAL_ENFORCEMENT 119,300 / SE_VIOLATIONS 76,438 /
  FORMAL_ENFORCEMENT 49,662 / PS_VIOLATIONS 44,872 / CS_VIOLATIONS 10,589

NCUA_CHARTER -- 4 tables: FS220 4,336 / FOICU 4,336 /
  FEDERALLY_INSURED_CU_LIST 4,250 / CHARTER_MERGER_EVENTS 53

ICE_FACILITY -- 2 tables: DETENTION_FACILITY_CODES 1,490 / DETENTION_STINTS 707

## Map as rebuilt (pre-fingerprint-refresh, so understated)

4,521 edges kept / 8,389 gated out, from 2,704,479 pairs tested.
By tier: CORROBORATED 2,576, STEEL 1,123, BRIDGE 482, GEO 334, STRONG 5,
PROBABILISTIC 1.

Cross-domain edge counts are dominated by health<->health (1,070) and
health<->other (1,015); justice appears in exactly 4 edges total.

## Repairs made this session

- Re-fingerprinted 5 tables whose columns had been renamed by a reload
  (EPA superfund boundaries lost its ATTRIBUTES_ prefix -- this was the
  crash that killed the graph step).
- Dropped 2 fingerprinted tables that no longer exist live.
- FED_FDA_DEVICE_CLASSIFICATION and FED_FDA_DEVICE_ENFORCEMENT were reloaded
  as raw JSON (a single RAW variant column). Data is complete inside
  (7,085 and 39,635 records, matching the source totals) but unflattened, so
  the map cannot read them. They silently left the graph.
