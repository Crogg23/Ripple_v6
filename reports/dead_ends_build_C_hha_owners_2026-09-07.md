# Dead ends, scope C build: home health agency owners (2026-09-07)

Docket E74 said "the ownership records don't exist for this type of agency." They do. CMS publishes
a quarterly Home Health Agency All Owners file. It is landed, marted, tested, and counted.
Python door only; the chat plug-in was not used.

## What was built

| piece | path |
|---|---|
| loader | `scripts/cms_hha_owners_load.py` (dry run by default, `--run` lands, `--append` to add on top of an existing load) |
| landing | `LIBRARY_RAW.LANDING.FED_CMS_HOME_HEALTH_OWNERS`, 38 columns as text + `INGESTED_AT` + `_SOURCE_RUN_ID` |
| staging | `ripple_dbt/models/staging/fed_cms_home_health_owners/stg_fed_cms_home_health_owners__records.sql` |
| mart | `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_OWNERS` from `models/marts/health/health__fed_cms_home_health_owners.sql` |
| source | added to `models/marts/health/_health__sources.yml` |
| tests | `models/marts/health/schema_fed_cms_home_health_owners.yml` |

Source: data.cms.gov dataset `fc009b2d-7846-44b1-b4a1-692f0c143879`, CSV
`HHA_All_Owners_2026.07.17.csv`, 18,527,284 bytes, sha256 `be8ae6de74be…`. Encoding is cp1252, not utf-8
(a 0x96 en-dash at byte 46,777); the loader falls back.

## Commands run, in order

```
python scripts/cms_hha_owners_load.py            # dry run: 38 columns, 101,188 rows, header printed
python scripts/cms_hha_owners_load.py --run      # landed 101,188; quality gate DQ OK, density 0.0769
cd library-onboarding/ripple_dbt
dbt parse                                        # 0 errors after moving test args under `arguments:`
dbt run  -s +health__fed_cms_home_health_owners  # 3 models, 3 success
dbt test -s +health__fed_cms_home_health_owners  # 10 tests, 10 pass
dbt run  -s  health__fed_cms_home_health_owners  # rebuild after the owner_name fix, 1 success
dbt test -s  health__fed_cms_home_health_owners  # 6 tests, 6 pass
```

No hook refused anything.

## The numbers (Python door, `connect/db.py`)

**Landing**

| check | result |
|---|---|
| rows | 101,188 (matches the data-api stats endpoint) |
| distinct ENROLLMENT_ID | 11,494, all 15 chars (`O` + YYYYMMDD + 6 digits) |
| distinct ASSOCIATE_ID (agency) | 10,203 |
| distinct ASSOCIATE_ID_OWNER | 31,847; lengths 10 (90,908 rows), 9 (9,381), 8 (899): leading zeros were stripped upstream, it is still an id |
| nulls in either id | 0 |
| dupes on (ENROLLMENT_ID, ASSOCIATE_ID_OWNER, ROLE_CODE_OWNER) | 0, so that triple is the grain |
| exact duplicate rows | 0 |
| TYPE_OWNER | I 79,880 / O 21,308 |
| ASSOCIATION_DATE_OWNER | parses MM/DD/YYYY on 101,188 of 101,188 |
| PERCENTAGE_OWNERSHIP | null on 36,330, parses as a number on every other row, range 0 to 100 |

**Join to CCN**

`FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS` has 11,508 rows, 11,508 distinct ENROLLMENT_ID, CCN blank on 0.
So the join on ENROLLMENT_ID cannot fan out and every hit carries a CCN.

| measure | result |
|---|---|
| mart rows | 101,188 (same as landing, no fan-out) |
| rows with a CCN | 99,287 (98.1%) |
| enrollment ids with a CCN | 11,224 of 11,494 (97.7%) |
| CCN length | 6 on 11,131 agencies, 7 on 93 (branch suffix, the 2026-09-05 trap) |
| unmatched sample | O20030422000042 LEGEND HOME HEALTHCARE, O20030103000023 CENTRAL HOME HEALTH CARE, O20030923000059 WESCARE: in the owners file, not in the current enrollment snapshot |

**Top 10 owners by agency count** (organization rows, keyed on ASSOCIATE_ID_OWNER, not name)

| owner | id | agencies | with CCN | chain home office | holding co |
|---|---|---|---|---|---|
| UNITEDHEALTH GROUP INCORPORATED | 749192441 | 461 | 456 | | |
| LHC GROUP INC | 6305754169 | 335 | 332 | Y | |
| HUMANA INC | 5294862660 | 253 | 247 | | Y |
| KENTUCKY HOMECARE HOLDINGS, INC. | 4789932682 | 249 | 244 | | Y |
| CENTERWELL HEALTH SERVICES INC | 6901714534 | 248 | 243 | Y | Y |
| KENTUCKY HOMECARE PARENT INC. | 2062745532 | 248 | 243 | | Y |
| CENTERWELL HEALTH SERVICES HOLDING CORP | 5092623629 | 191 | 186 | | Y |
| VANGUARD GROUP INC | 4284807678 | 163 | 163 | | Y |
| BLACKROCK INC | 2668509902 | 156 | 156 | | Y |
| AMEDISYS INC | 3072421957 | 153 | 149 | Y | |

Name-only grouping is close but not the same: UNITEDHEALTH GROUP INCORPORATED is 3 ids / 464 agencies,
BLACKROCK INC is 2 ids / 159. Key on the id. Vanguard and BlackRock are index-fund holders of the public
parents (Amedisys, Enhabit), not operators; the file lists indirect 5%+ interest.

**Flags**

| flag | true | false | null |
|---|---|---|---|
| is_private_equity | 744 rows, 231 agencies, 104 distinct owner ids | 20,564 | 79,880 |
| is_reit | 0 | 21,308 | 79,880 |

Every flag is null on individual (`I`) rows. Only org rows carry them. REIT is 'N' on all 21,308 org rows:
a constant in this vintage, not a signal. On org rows: for-profit 8,429, corporation 8,042, LLC 6,385,
holding company 4,851, created-for-acquisition 1,223, chain home office 789, investment firm 741.

**Roles** (ROLE_CODE_OWNER): 41 corporate director 20,942; 40 corporate officer 20,505;
35 indirect 5%+ 17,013; 42 W-2 managing employee 16,854; 34 direct 5%+ 15,526;
43 operational/managerial control 7,626; 25 contracted managing employee 760; 44 other 628.

**Dates**: ASSOCIATION_DATE_OWNER spans 1800-01-01 to 2026-10-31. 641 rows sit before 1990 and 3 are in
the future; treat both as sentinels. 4,120 agencies have at least one owner row dated 2024-01-01 or later,
which is the working set for "who is the new owner".

## Bug caught on the first build

`owner_name` came out null on 49,827 rows. Snowflake's `concat_ws` returns NULL when any argument is NULL,
and most individuals have no middle name. Fixed by coalescing each part to '' before the concat; rebuilt;
now 0 nulls, and landing confirms 0 rows with no name in any name column.

## What E74 can now do

The question was "is there a record of who the new owner is." Yes: name, id, role, percentage and the date
the owner arrived, per agency, joined to CCN so it reaches Care Compare stars and POS. What has NOT been
run is the analysis itself: which agencies changed hands, and what happened to them after. That is the
open piece.

## Skeptic pass

Fresh-context reviewer reran every number above through the Python door: all reproduced exactly,
verdict AGREE. It found four small things, all fixed the same hour: the docket coverage cell said
1990-2026 when the span is 1800-2026 (641 pre-1990 sentinels); EXPECTED_ROWS was printed but never
enforced, so the loader now stops when the row count moves more than 20% from the baseline
(`--expect-rows` resets it, checked by forcing a stop at 50,000); the docstring claimed the dry run
prints the landed count, it does not, docstring fixed; one unused CTE column in the mart, dropped.
The mart SQL edit is cosmetic and the table was not rebuilt for it. Blind spot the skeptic named:
every check compares the warehouse to a file the same script parsed; nothing independent confirms
CMS served the full file beyond the 101,188 the stats endpoint reports.

## Not done

- Historical vintages (catalog.data.gov has them back to 2023-04-01) were not landed; this is one snapshot,
  so "changed owner" reads off ASSOCIATION_DATE_OWNER, not off a diff between quarters.
- No timeline view or `ripple_time_registry` row for the new mart.
- `CSV_URL` is the dated July path, not resolved from the dataset id; a rerun next quarter lands the same vintage.
- Not committed. Nothing pushed.

parked: the same CMS "All Owners" family exists for hospice, SNF, hospitals, FQHC and RHC; the loader is a
URL and a table name away from each.
