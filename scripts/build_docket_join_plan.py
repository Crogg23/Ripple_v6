"""Map every docket question to its join columns, using THE_CATALOG plus live columns.

Reads  reports/THE_CATALOG.csv, reports/_live_cols_extra_<date>.json, docket/docket.csv,
       docket/docket_catalog_map_<date>.csv
Writes docket/docket_join_plan_<date>.csv

Grade per question:
  A measured   the catalog counted shared values for the join
  B hard ID    both tables carry the same ID family, never counted
  C geo        only county, zip or state in common
  D name match only a name column in common
  E no key     nothing shared, no one-hop bridge found
"""
import csv, json, collections, re, itertools, sys

DATE = sys.argv[1] if len(sys.argv) > 1 else '2026-09-22'
cat = list(csv.DictReader(open('reports/THE_CATALOG.csv', encoding='utf-8')))
realm = {x['table']: x['realm'] for x in cat}
cols = collections.defaultdict(list)
for x in cat:
    cols[x['table']].append(x['column'])
for t, c in json.load(open(f'reports/_live_cols_extra_{DATE}.json')).items():
    cols[t] = list(c)
m = {x['id']: x for x in csv.DictReader(open(f'docket/docket_catalog_map_{DATE}.csv', encoding='utf-8'))}
dk = list(csv.DictReader(open('docket/docket.csv', encoding='utf-8')))

FAM = [
 ('NPI', r'^(NPI|PRSCRBR_NPI|RFRG_NPI|RNDRNG_NPI|SUPLR_NPI|COVERED_RECIPIENT_NPI|PROVIDER_NPI|[A-Z0-9_]*_NPI)$'),
 ('CCN', r'^(CCN|PROVIDER_CCN|PRVDR_NUM|PROVIDER_NUMBER|FEDERAL_PROVIDER_NUMBER|CMS_CERTIFICATION_NUMBER_CCN|CMS_CERTIFICATION_NUMBER|[A-Z0-9_]*_CCN|RNDRNG_PRVDR_CCN)$'),
 ('EIN', r'^(EIN|AUDITEE_EIN|SPONS_DFE_EIN|EMPLOYER_IDENTIFICATION_NUMBER_EIN|TAX_ID|[A-Z0-9_]*_EIN)$'),
 ('UEI/DUNS', r'^(UEI|AUDITEE_UEI|RECIPIENT_UEI|AWARDEE_OR_RECIPIENT_UEI|ORG_DUNS|RECIPIENT_DUNS|DUNS|PARENT_UEI|[A-Z0-9_]*_UEI|[A-Z0-9_]*DUNS[A-Z0-9_]*)$'),
 ('CIK', r'^(CIK|ISSUER_CIK|PARENT_CIK|[A-Z0-9_]*_CIK)$'),
 ('ACCESSION', r'^(ACCESSION_NUMBER|ACCESSION_NO|ADSH)$'),
 ('LEI', r'^(LEI|MATCHED_LEI|ULTIMATE_PARENT_LEI|LEI_20\d\d|[A-Z0-9_]*_LEI)$'),
 ('FDIC_CERT', r'^(FDIC_CERT|CERT|RSSD_ID|HOLDING_COMPANY_RSSD|[A-Z0-9_]*RSSD[A-Z0-9_]*)$'),
 ('FEC_ID', r'^(CMTE_ID|CAND_ID|FILER_ID|COMMITTEE_ID|CANDIDATE_ID|OTHER_ID)$'),
 ('BIOGUIDE', r'^(BIOGUIDE_ID|BIOGUIDE|ICPSR|MEMBER_ID)$'),
 ('PERSON_ID', r'^(PERSON_ID|FINANCIAL_DISCLOSURE_ID|COVERED_RECIPIENT_PROFILE_ID)$'),
 ('FRS_ID', r'^(REGISTRY_ID|EPA_REGISTRY_ID|FRS_ID|FACILITY_REGISTRY_ID)$'),
 ('PWSID', r'^(PWSID)$'),
 ('NPDES_ID', r'^(NPDES_ID|NPDES_PERMIT_ID|EXTERNAL_PERMIT_NMBR)$'),
 ('RCRA_ID', r'^(HANDLER_ID|GENERATOR_ID|ID_NUMBER)$'),
 ('TRI_ID', r'^(TRI_FACILITY_ID|TRIFID)$'),
 ('ORIS', r'^(ORIS_CODE|PLANT_ID|FACILITY_ID)$'),
 ('MINE_ID', r'^(MINE_ID)$'),
 ('PHMSA_ID', r'^(PHMSA_OPERATOR_ID|OPERATOR_ID)$'),
 ('HRSA_ID', r'^(BHCMISID|BHCMIS_ORGANIZATION_ID)$'),
 ('VESSEL', r'^(IMO|IMO_NUMBER|MMSI)$'),
 ('DEVICE', r'^(K_NUMBER|BASELINE_510K_NUMBER|PRODUCT_CODE|DEVICE_REPORT_PRODUCT_CODE)$'),
 ('VEHICLE', r'^(MAKE|MODEL|MODEL_YEAR)$'),
 ('DOCKET', r'^(DOCKET|MDL_DOCKET|TRANSFER_DOCKET|DOCKET_IDS|DOCKET_NUMBER)$'),
 ('COUNTY_FIPS', r'^(COUNTY_FIPS|FIPS|STATE_COUNTY_FIPS_CODE|COUNTY_FIPS_CODE|GEOID|CENSUS_GEOID|CNTY_FIPS|FIPS_CODE|COUNTYFIPS|BUYER_COUNTY_FIPS|BRANCH_COUNTY_FIPS|BRANCH_STATE_COUNTY_FIPS|CZ_FIPS|FIPS_STATE|COUNTY_CODE)$'),
 ('COUNTY_NAME', r'^(COUNTY|COUNTY_NAME|COUNTY_PARISH|BUYER_COUNTY|REPORTER_COUNTY|BRANCH_COUNTY_NAME|CZ_NAME|[A-Z0-9_]*_COUNTY(_NAME)?)$'),
 ('ZIP', r'^(ZIP|ZIP_CODE|ZIP5|ZIPCODE|ZIP_CD|STD_ZIP5|[A-Z0-9_]*_ZIP|[A-Z0-9_]*_ZIP_CODE|[A-Z0-9_]*_ZIP_4_CODE|[A-Z0-9_]*ZIPCODE|POSTAL_CODE)$'),
 ('STATE', r'^(STATE|STATE_CODE|STATE_ABBR|ST|STATE_FIPS|STATE_FIPS_CODE|STATE_ABBREVIATION|STATEFP|STATE_NAME|[A-Z0-9_]*_STATE|[A-Z0-9_]*_STATE_CODE|[A-Z0-9_]*_STATE_ABBR(EV|EVIATION)?|[A-Z0-9_]*_STATE_FIPS|CMTE_ST)$'),
 ('ORG_NAME', r'^([A-Z0-9_]*(ORG|ORGANIZATION|COMPANY|EMPLOYER|FACILITY|RECIPIENT|VENDOR|OWNER|BUSINESS|LEGAL|SPONSOR|CONTRACTOR|MANUFACTURER|MFR|MFG|INSTITUTION|BANK|FIRM|ISSUER|ENTITY|OPERATOR|CHAIN|CLIENT|REGISTRANT|ADVERTISER|COMMITTEE|CMTE|AUDITEE|AUDITOR|HOSPITAL|PROVIDER|BUYER|REPORTER|SDN|TEACHING_HOSPITAL|AGENCY|HEALTHCENTER)[A-Z0-9_]*(NAME|NM)|NAME|DBA_NAME|VESSELNAME|WELL_NAME|PROPERTY_NAME)$'),
 ('PERSON_NAME', r'^([A-Z0-9_]*(LAST|FIRST|FULL|PERSON|CANDIDATE|MEMBER|PHYSICIAN|PRSCRBR|RNDRNG|RFRG|LEGISLATOR|DEFENDANT|DONOR|VICTIM|OFFICER|PARTNER)[A-Z0-9_]*(NAME|NM)[A-Z0-9_]*|LASTNAME|FIRSTNAME)$'),
 ('DRUG', r'^(NDC|DRUG_NAME|BRND_NAME|GNRC_NAME|BRAND_NAME|GENERIC_NAME|PRODUCT_NAME|INGREDIENT_NAME|SETID|NAME_OF_ASSOCIATED_COVERED_DRUG_OR_BIOLOGICAL1)$'),
 ('CVE', r'^(CVE_ID|CVE)$'),
 ('DATE', r'^([A-Z0-9_]*DATE[A-Z0-9_]*|[A-Z0-9_]*_YEAR|YEAR|FY|FISCAL_YEAR|[A-Z0-9_]*_DT|[A-Z0-9_]*_YR)$'),
]
RANK = {f: i for i, (f, _) in enumerate(FAM)}
HARD, GEO, NAME = RANK['DOCKET'], RANK['ZIP'], RANK['CVE']
NO_BRIDGE = {'DOCKET', 'PERSON_ID', 'ORIS', 'RCRA_ID'}  # ids that are only unique inside one source
_fc = {}


def fams(t):
    if t in _fc:
        return _fc[t]
    out = collections.defaultdict(list)
    for c in cols.get(t, []):
        for f, rx in FAM:
            if re.match(rx, c.upper()):
                out[f].append(c)
                break
    _fc[t] = out
    return out


famtab = collections.defaultdict(set)
for t in cols:
    for f in fams(t):
        if f not in ('DATE', 'STATE', 'ORG_NAME', 'PERSON_NAME'):
            famtab[f].add(t)


def pair_key(a, b, maxrank=99):
    A, B = fams(a), fams(b)
    for f, _ in FAM:
        if f == 'DATE' or RANK[f] > maxrank:
            continue
        if A.get(f) and B.get(f):
            return f, A[f][0], B[f][0]
    return None


def src(t):
    """Source family of a table name: FED_EPA_RCRA from ENVIRONMENT__FED_EPA_RCRA_VIOLATIONS."""
    n = t.split('__')[-1]
    parts = n.split('_')
    return '_'.join(parts[:3]) if len(parts) > 3 else n


def _bridge_dir(a, b):
    best = None
    for f1 in fams(a):
        if RANK.get(f1, 99) > HARD:
            continue
        for x in famtab[f1]:
            if x in (a, b) or '__PREV_' in x:
                continue
            if f1 in NO_BRIDGE and src(x) != src(a):
                continue
            k2 = pair_key(x, b, GEO)
            if k2 and k2[0] != 'STATE' and k2[0] not in NO_BRIDGE:
                same_src = x.split('__')[0] in (a.split('__')[0], b.split('__')[0])
                score = (RANK[f1] + RANK[k2[0]], 0 if same_src else 1)
                if best is None or score < best[0]:
                    best = (score, x, f1, fams(a)[f1][0], fams(x)[f1][0], k2)
    return best


def bridge(a, b):
    """One hop through a table x: hard ID from a to x, then any key from x to b. Tries both directions."""
    r1 = _bridge_dir(a, b)
    r2 = _bridge_dir(b, a)
    if r2 and (r1 is None or r2[0] < r1[0]):
        score, x, f1, cb, cx, k2 = r2
        return (score, x, f1, cb, cx, k2, True)
    return r1 + (False,) if r1 else None


MANUAL = {
 '83': 'text join: LDA GOVERNMENT_ENTITIES and SPECIFIC_ISSUES vs Federal Register AGENCY_NAMES, window on PUBLICATION_DATE',
 '90': 'name join: REVOLVINGDOOR AGENCY vs AWARDING_AGENCY_NAME, then SECTOR vs NAICS_DESCRIPTION',
 '92': 'name join: VENDOR_NAME vs DONOR_NAME or EMPLOYER, both cleaned',
 '94': 'CourtListener PERSON_ID to its people table for the judge name, then name vs FJC FILING_JUDGE',
 '107': 'name join: ARCOS REPORTER_NAME vs NAAG DEFENDANTS text',
 '113': 'name join: JPML LITIGATION text vs Open Payments manufacturer name',
 '130': 'bridge HUD MF properties by PROPERTY_ID for zip, then zip vs HPI PLACE_ID where LEVEL is ZIP5',
 '136': 'name join: CISA VENDOR_PROJECT vs RECIPIENT_NAME',
 'A35': 'name join: FD_PTR LAST plus FIRST plus STATEDST vs MEMBER_NAME, or bridge on bioguide via a legislators table',
 'E34': 'RCRA_VIOLATIONS ID_NUMBER to RCRA_FACILITIES for zip, then zip to county needs a zip-county crosswalk, none in the catalog',
 'E60': 'two hops: dialysis CCN to POS_OTHER for zip, POS zip to SDWA_PUB_WATER_SYSTEMS zip, then PWSID to violations',
}
out = csv.writer(open(f'docket/docket_join_plan_{DATE}.csv', 'w', encoding='utf-8', newline=''))
out.writerow(['id', 'family', 'status', 'question', 'tables', 'join_grade', 'join_plan', 'bridge_needed', 'filter_columns', 'no_key_pairs', 'manual_note'])
gc = collections.Counter()
for r in dk:
    tabs = [t.strip().split('.')[-1] for t in r['tables'].split('|') if t.strip()]
    rs = sorted(set(realm.get(t, 'RAW') for t in tabs))
    family = '+'.join(rs) if len(rs) <= 2 else 'CROSS 3+'
    plan, br, nokey, best, mp = [], [], [], 99, set()
    for j in m[r['id']]['measured_joins_between_tables'].split(' ; '):
        mm = re.match(r'(\S+)\.(\w+) = (\S+)\.(\w+) \[(\S+)\]', j)
        if mm:
            plan.append(f"{mm.group(1)}.{mm.group(2)} = {mm.group(3)}.{mm.group(4)} [measured {mm.group(5)} shared]")
            mp.add(frozenset([mm.group(1), mm.group(3)]))
            best = -1
    for a, b in itertools.combinations(tabs, 2):
        if frozenset([a, b]) in mp:
            continue
        k = pair_key(a, b)
        if k:
            plan.append(f"{a}.{k[1]} = {b}.{k[2]} [{k[0]}]")
            best = min(best, RANK[k[0]])
        else:
            bb = bridge(a, b)
            if bb:
                _, x, f1, ca, cx, k2, flipped = bb
                s1, s2 = (b, a) if flipped else (a, b)
                br.append(f"{s1}.{ca} = {x}.{cx} [{f1}] then {x}.{k2[1]} = {s2}.{k2[2]} [{k2[0]}]")
                best = min(best, max(RANK[f1], RANK[k2[0]]))
            else:
                nokey.append(f"{a} x {b}")
    if len(tabs) == 1:
        grade = 'single table'
    elif best == -1:
        grade = 'A measured'
    elif best <= HARD:
        grade = 'B hard ID'
    elif best <= GEO:
        grade = 'C geo'
    elif best <= NAME:
        grade = 'D name match'
    else:
        grade = 'E no shared key'
    if nokey and not grade.startswith('E'):
        grade += ' +gap'
    gc[grade] += 1
    filt = sorted(set(f"{t}.{c}" for t in tabs for c in fams(t).get('DATE', [])[:2]))
    out.writerow([r['id'], family, r['where_it_stands'], r['question'], ' | '.join(tabs), grade,
                  ' ; '.join(plan), ' ; '.join(br), ' | '.join(filt), ' ; '.join(nokey), MANUAL.get(r['id'], '')])
print(gc)
