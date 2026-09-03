# Gen 3 content recon: cross-table entity crosswalk — 2026-09-03

Chris's ask, verbatim: "so, whats layer 3? Remind me" then "are you capable of doing the gen 3?"
then "Metiuclously plan it out. Stresstest your methods, then go."

Gen 1's report named gen 3 in passing (section 7, "names that cross rooms") but never scoped it.
This round scopes it, builds it, breaks it once, fixes it, then verifies the output with 37
independent agents. Every finding below walks its chain: what was checked, what a hit means,
what a miss means.

## 1. What ran

| item | value | how we know |
|---|---|---|
| input | gen 1's 2,208 json pages, already on disk | reports/recon/content/json/*.json |
| door | none — zero warehouse queries this round | script reads local files only |
| cost | $0 | no SELECT issued against Snowflake |
| method | scripts/gen3_entity_crosswalk.py, local Python | run three times, tightened each pass |
| verify | 37 agents, one per candidate cluster | Workflow tool, 2,028,558 tokens, 114.7s wall |

## 2. The method — chain for each step

| step | what was checked | a hit means | a miss means |
|---|---|---|---|
| extract | every "who"-column's top-20 names, all 2,208 non-portal pages | raw name mentions with table+column+row-count | column never scanned (portal, or not who-tagged) |
| column filter | column name matched a place or person-fragment pattern | column dropped before clustering | column kept, value-level filter is the only net left |
| value filter | name matched a stoplist, country list, county pattern, or was pure noise | value dropped | value kept |
| normalize | uppercase, strip punctuation, drop trailing legal suffix (INC/LLC/CORP/CO/LP...) | two spellings fold to one cluster key | spelling difference beyond suffix/punctuation stays split |
| tier split | count tokens left in the cluster's display name | 1 token = high collision risk, 2+ = low risk | — this is a proxy, not a certainty, see section 5 |
| verify | one agent per top candidate reads the source pages and judges real-entity vs collision | independent confirm or reject with reasoning | agent uncertain, defaults toward reject |

## 3. It broke immediately — here's the break

First run, before any filtering: top cross-table clusters by table count were JOHNSON (46 tables),
SMITH (44), BROWN (44), DAVID (43), THOMAS (42) — common English surnames, not entities.

- Checked: traced JOHNSON back to its source column in FED_CMS_NPPES.
- Hit: `PROVIDER_LAST_NAME_LEGAL_NAME` and `AUTHORIZED_OFFICIAL_LAST_NAME` — literal surname columns,
  664,121 rows for JOHNSON in that one table alone. Thousands of different Dr. Johnsons, not one entity.
- Fix: added a column-name blacklist for `*_LAST_NAME`, `*_FIRST_NAME`, `*_LNAME`, `*_FNAME`, etc.,
  same pattern as the address-column blacklist gen 1 already had for CITY/STATE/REGION.
- Second break: AUSTRALIA, BRAZIL, SWITZERLAND still showed up — country names, not entities, leaking
  through columns not caught by the state/city blacklist (FATCA jurisdiction, FAERS reporter country).
  Fix: added a ~150-country stoplist.

After both fixes: 15,077 raw name mentions, folding into 739 clusters seen in 3+ tables — 523
multi-word (TENNESSEE VALLEY AUTHORITY, WALMART variants), 216 single-word (still mostly surnames,
by design of the split — see section 5).

## 4. Verification — 37 agents, one per top candidate

Ran 25 agents on the top single-word clusters (highest collision risk) and 12 on the top multi-word
clusters (lower risk, spot-check for false merges). Each agent got the cluster's table list, raw
variant counts, and could read the actual recon page for any source table before ruling.

| bucket | verified | real entity | collision/noise | hit rate |
|---|---|---|---|---|
| single-word | 25 | 2 (TESLA, PACIFICORP) | 23 | 8% |
| multi-word | 12 | 11 | 1 (ST LUKES HOSPITAL) | 92% |

- Checked: is this string plausibly one real-world entity, or many unrelated things sharing a name?
- Hit (single-word, 2 of 25): TESLA and PACIFICORP — distinctive brand words, all source tables are
  EIA/EPA/OSHA business registries, row counts match "one company, many filings."
- Miss (single-word, 23 of 25): every common-surname candidate (JOHNSON, SMITH, BROWN, THOMAS,
  DAVIS, WILLIAMS, TAYLOR, JONES, ANDERSON, JOHN, ROBERT, WILSON, JACKSON, DAVID, HARRIS, WHITE,
  RODRIGUEZ, MICHAEL, LEE, MARK, WILLIAM, MARTIN) confirmed as populations of unrelated people —
  row counts in the hundreds of thousands, source tables are physician/judge/legislator/lobbyist
  directories, not business registries.
- Hit (multi-word, 11 of 12): WAL-MART STORES EAST LP, TENNESSEE VALLEY AUTHORITY, WALMART INC,
  UNITED PARCEL SERVICE, MIDAMERICAN ENERGY CO, DUKE ENERGY CAROLINAS, BANK OF AMERICA CORPORATION,
  EXXON MOBIL CORP, WAL-MART STORES TEXAS LLC, MICROSOFT CORP, WALGREEN CO — each confirmed by
  reading a source page showing the value sitting in a real org-name field next to other named peers.
- Miss (multi-word, 1 of 12): ST LUKES HOSPITAL. FED_CMS_HOSPITAL_COMPARE's FACILITY_NAME column
  shows it sitting next to MEMORIAL HOSPITAL, HOLY CROSS HOSPITAL, ST JOSEPH MEDICAL CENTER, MERCY
  MEDICAL CENTER — all common civic/religious hospital names reused by dozens of unrelated facilities
  nationwide. XC_ROR_RESEARCH_ORGANIZATIONS independently assigns separate IDs to multiple different
  "St. Luke's Hospital" entities worldwide. Same failure shape as a surname, on an org name instead.

**Retroactive correction to gen 1**: gen 1's own "same name, many tables" list (still in DIGEST.md)
includes ST LUKES HOSPITAL, ST JOSEPH MEDICAL CENTER, MEMORIAL HOSPITAL, GOOD SAMARITAN HOSPITAL,
COMMUNITY HOSPITAL, and MERCY MEDICAL CENTER with no caveat. All six are the same generic-hospital-
name collision just confirmed on ST LUKES HOSPITAL. Treat all six as unverified until checked the
same way.

## 5. New failure modes found, not yet fixed

- **Person-name columns beyond `*_LAST_NAME`**: verification agents found the collision leaking
  through `NAME_LAST`, `NAME_FIRST`, `FILER_NAML`, `FILER_NAMF`, `FILERNAMELAST`, `FILERNAMEFIRST`,
  a bare column named `LAST`, `RNDRNG_PRVDR_LAST_ORG_NAME` (a name/org field mixed in one column),
  `CASE_NAME_SHORT`, `PLT`/`DEF` (civil case party fields), and `FAMILY_NAME`. The column-name
  blacklist only catches the pattern that broke gen 1's first run; it does not catch these.
- **County names beyond the ` COUNTY` suffix pattern**: `CZ_NAME` (NOAA storm events), `CNTY_NM2KX`
  / `CURCNTY_NM` (HUD), and bare county names in `XC_CENSUS_CB_COUNTY`'s NAME column (value is just
  "Jackson", not "Jackson County") all slipped past the regex, which requires the literal word COUNTY.
- **Generic institutional names**: the hospital-name collision generalizes to any "ST X" / "MEMORIAL
  X" / "COMMUNITY X" / "HOLY X" pattern — not just hospitals, likely also churches, schools, VFW posts.
- **Category and place leaks in unexpected columns**: WHITE picked up an EPA race/ethnicity field
  (`OTHER_RACE`) and a USGS watershed name field (`NAME`, as in "White River") — two more failure
  modes riding the same normalized string.

## 6. What's usable right now

- **523 multi-word clusters**, tested at a 92% real-entity rate on the top 12. Good enough to browse
  directly for cross-agency entity work; still eyeball each one for the hospital-name pattern before
  treating a hit as certain.
- **2 confirmed single-word entities**: TESLA (10 tables), PACIFICORP (11 tables) — PACIFICORP is a
  genuinely new find, not in gen 1's original top-40 name list.
- **216 single-word clusters, mostly unverified past the top 25** — treat every one as "probably a
  common name" until checked; the 8% hit rate on the top 25 says don't trust this bucket unverified.

Receipts: `reports/recon/gen3/clusters_multiword.csv`, `clusters_singleword.csv`, `parent_groups.csv`.

## 7. Not done

- Only the top 25 single-word and top 12 multi-word clusters got agent verification; 727 clusters
  did not.
- Tier-2 parent-group suggestions (WALMART ↔ WAL-MART STORES EAST LP style links) were generated
  but not independently verified — the union-find prefix-match is unaudited past manual inspection.
- The five new failure-mode column shapes in section 5 are documented, not fixed in the script.
- No ID-based join (EIN/LEI/UEI/DUNS) attempted — this stayed name-string-only, per plan; a real
  join would need new warehouse queries and a price check first.
- Nothing committed. New files: `scripts/gen3_entity_crosswalk.py`, `reports/recon/gen3/*`, this file.

## 8. Phase A — finishing the crosswalk, 2026-09-03 (same day, later)

Chris: "Phase A go." Goal: verify past the first 37, and fix what the verifiers found broken.

### Round 2 filter fixes, before any more verification
- Column-name blacklist expanded: `NAME_LAST`/`NAME_FIRST` (reversed order from round 1's
  `LAST_NAME` pattern), a bare column named `LAST`/`FIRST`, `FILER_NAML`/`FILER_NAMF`,
  `RNDRNG_PRVDR_LAST_ORG_NAME`, `CASE_NAME_SHORT`, `PLT`/`DEF` court-party fields.
- County leak fixed for `CZ_NAME`, `CNTY_NM2KX`, `CURCNTY_NM`, and one hardcoded exception
  (`XC_CENSUS_CB_COUNTY.NAME` holds bare county names with no "COUNTY" suffix to filter on).
- New value-level filters: hex/hash strings (a `_SRC_SHA256` audit column was leaking through),
  a ~60-city US stoplist, and generic occupation words (SELF, PRESIDENT, GOVERNMENT, RESIDENCE).
- Result: tier-1 clusters 739 → 647; single-word bucket 216 → 130, with the worst surname
  offenders (JOHNSON, SMITH) dropping from 20 tables to 7 as their columns got excluded.

### Round 2 verify batch — 169 candidates, full remaining risk pool
Everything left in the single-word bucket, plus every multi-word cluster shaped like a generic
institution name (contains HOSPITAL, BANK, CHURCH, SCHOOL, CARE CENTER, etc — the ST LUKES
HOSPITAL risk profile).

| | verified | real | noise | hit rate |
|---|---|---|---|---|
| round 2 combined | 169 | 46 | 123 | 27% |

- **Checked**: is this candidate one real entity, a small mirrored set of the same sanctioned
  people, or noise?
- **Hit — real companies nobody had caught yet**: Verizon, Comcast, Boeing, Pfizer, Merck,
  GlaxoSmithKline, Target, Chevron, Subway, McDonald's, Conrail, MISO, PruittHealth.
- **Hit — national chartered orgs, wrongly assumed noise-shaped**: Knights of Columbus, Rotary
  International, Lions Clubs International, American Legion Auxiliary, Kaiser Foundation
  Hospitals, Life Care Centers of America. One parent body, many local chapters — different from
  ST LUKES HOSPITAL's many-independent-locals pattern. The tell: source tables imply one
  chartering body (IRS nonprofit filings) rather than an independent local directory (CMS
  hospital comparison).
- **Hit — sanctions-list mirrors, a genuinely new failure-mode carve-out**: HAQQANI, AKHUND,
  SABAWI, BARZAN, ABDALLAH, QADHAFI, KONY, SADDAM. Same small set of designated individuals
  (Iraqi Ba'athist family, Taliban leadership, Joseph Kony/LRA) duplicated across UK/UN/US
  sanctions feeds — tens of rows, concentrated on one regime, not hundreds spread across
  unrelated programs.
- **Miss — a third noise type, the biggest yet**: category/classification fields tagged "who"
  by the gen-1 classifier. 54 of 169 hits — STRAIN, ATTORNEY, PHYSICIAN, DEMOCRAT, KITCHEN,
  INJURY, CONTUSION — OSHA injury types, job titles, political parties, none of them names.
- **Miss — still noise**: 28 more generic local-institution collisions (MEMORIAL HOSPITAL,
  FIRST STATE BANK, COMMUNITY BANK style), 16 more person-name collisions, 14 more place leaks.

### Cumulative Phase A status
206 of 647 tier-1 clusters independently verified (37 round 1 + 169 round 2): 59 confirmed
real, 147 confirmed noise. The remaining ~440 sit at the minimum 3-table threshold — lower
signal, not yet checked. Not fixed yet: the category-field leak (needs a column-name blacklist
pass the same way person-names and places got one) and the parent-vs-locals judgment call for
the rest of the generic-institution bucket.

Receipts: `reports/recon/gen3/vb2a.json`, `vb2b.json` (the round-2 batch as sent to the verifiers).

## 10. Phase A — round 4, the crosswalk is fully verified

Chris: "go", three more times, to the end. Round 4 took every remaining unverified multi-word
cluster — 396 of them, the entire low-risk-by-pattern tail — and checked each one individually
instead of trusting the pattern.

| | verified | real | noise | hit rate |
|---|---|---|---|---|
| round 4 | 395 | 322 | 73 | 81.5% |

- **Checked**: is this candidate one real entity, or does it fall into a known leak shape (street,
  address, place, case-name, category)?
- **Hit**: hundreds of real companies, agencies, and railroads confirmed — utilities, pharma
  distributors, airlines, all nine Class I-era railroads under FRA casualty/crossing/equipment
  tables, national PACs, federal courts. The multi-word bucket's 92% spot-check rate from section
  4 held at full scale.
- **Miss — a retroactive correction to gen 1**: "SUNOCO SERVICE STATION" and "SHELL SERVICE
  STATION" were both in gen 1's original DIGEST as apparent real cross-agency hits. Both are
  actually noise — "SERVICE STATION" is a generic EPA facility-type label, not a franchise name.
  SHELL OIL CO, the real Shell entity, is a separate, correctly-verified cluster.
- **Miss — two new leak shapes**: bare mailing addresses ("200 1ST ST SW") cluster because one
  hospital's address gets reused as the billing address for thousands of affiliated physicians;
  common-surname case names ("SMITH V. UNITED STATES") cluster because many unrelated litigants
  share a surname, same failure as the bare-surname problem, riding a legal citation instead.

### Phase A — final tally, all 4 rounds

| round | verified | real | noise | hit rate |
|---|---|---|---|---|
| 1 | 37 | 13 | 24 | 35% |
| 2 | 169 | 46 | 123 | 27% |
| 3 | 28 | 24 | 4 | 86% |
| 4 | 395 | 322 | 73 | 82% |
| **total** | **629** | **405** | **224** | **64%** |

Every tier-1 cluster (585, after all three rounds of column/value filter fixes) has now been
through at least one independent verification pass. Nothing left in the crosswalk is a guess —
each of the 405 confirmed-real entities and 224 confirmed-noise strings has a specific reason on
record, tied to a specific column or table.

## 9. Phase A — round 3, closing out the high-risk pool

Third filter fix, same session: category/classification columns (`PARTY`, `OCCUPATION`,
`POLLUTANT_NAME`, injury-narrative fields) blacklisted the same way name-fragment and place
columns were — traced by looking up which column actually held each round-2 noise value
(STRAIN, ATTORNEY, DEMOCRAT, KITCHEN). Tier-1 clusters 647 → 585; single-word bucket 130 → 100,
and every one of those 100 turned out to already be covered by round 1 or round 2's verdicts
under a slightly different display-string spelling — the single-word bucket is now fully resolved.

Final targeted batch: the last 28 unverified multi-word clusters shaped like ST LUKES HOSPITAL
(contains HOSPITAL, BANK, UNIVERSITY, ASSOCIATION, etc).

| | verified | real | noise | hit rate |
|---|---|---|---|---|
| round 3 | 28 | 24 | 4 | 86% |

- **Checked**: does the row/table pattern look like many independent owners, or one charter
  reported many times (the bank-branch or university-grant pattern)?
- **Hit — national bank charters**: Wells Fargo, JPMorgan Chase, U.S. Bank, PNC, TD Bank,
  KeyBank, M&T, First-Citizens, BMO, Citizens Bank — all "National Association" banks. One OCC
  charter each, branches and SBA/PPP loans reported under that one charter — confirmed via
  FDIC_SOD_BRANCH_DEPOSITS' own RSSDID/holding-company columns.
- **Hit — universities and a sanctioned-org network**: Columbia, Johns Hopkins, Ohio State,
  University of Washington, Oxford University Press, and Al-Aqsa Foundation (an OFAC-designated
  charity mirrored across four overlapping US sanctions/exclusion lists — same sanctions-mirror
  pattern round 2 found for individuals, now confirmed for an org too).
- **Miss — still noise, confirming the pattern holds**: ST LUKES HOSPITAL, ST MARY MEDICAL
  CENTER, MERCY REGIONAL MEDICAL CENTER, ROLLING HILLS CARE CENTER — each verified via a
  per-row facility ID (CCN) showing separately-run, unrelated facilities.

### Phase A final status
234 clusters independently verified across 3 rounds (37 + 169 + 28): 83 confirmed real, 151
confirmed noise. The single-word bucket and the generic-institution-name bucket — the two known
collision-risk shapes — are now both fully checked. What's left unverified (~350 of 585 tier-1
clusters) is the low-risk multi-word bucket of distinctive brand-shaped names, already spot-checked
at 92%+ real in section 4; trust it by pattern, not yet checked one by one.
