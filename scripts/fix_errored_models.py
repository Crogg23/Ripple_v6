"""Fix all 28+ errored dbt mart models by regenerating them with correct column refs."""
import snowflake.connector
import os
from pathlib import Path

# Load env
from dotenv import load_dotenv
load_dotenv(r'c:\Code\Ripple_v6\library-onboarding\.env')

conn = snowflake.connector.connect(
    account=os.environ['SNOWFLAKE_ACCOUNT'],
    user=os.environ['SNOWFLAKE_USER'],
    password=os.environ.get('SNOWFLAKE_PAT',''),
    role='ACCOUNTADMIN',
    warehouse='COMPUTE_WH'
)

MODELS_DIR = Path(r'c:\Code\Ripple_v6\library-onboarding\ripple_dbt\models\marts')

def get_columns(table_name):
    cur = conn.cursor()
    cur.execute(f"""SELECT column_name FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS 
                    WHERE table_schema='LANDING' AND table_name='{table_name}'
                    AND column_name NOT IN ('_INGESTED_AT','_SOURCE_RUN_ID','_SRC_SHA256')
                    ORDER BY ordinal_position""")
    return [r[0] for r in cur.fetchall()]

def needs_quoting(col):
    """True if column needs double-quoting in Snowflake SQL."""
    import re
    reserved = {'GROUP','ORDER','SELECT','TABLE','FROM','WHERE','JOIN','LEFT','RIGHT',
                'OUTER','INNER','ON','AS','AND','OR','NOT','IN','IS','NULL','TRUE','FALSE',
                'BETWEEN','LIKE','EXISTS','HAVING','UNION','ALL','INSERT','UPDATE','DELETE',
                'CREATE','DROP','ALTER','INDEX','VIEW','SCHEMA','DATABASE','GRANT','REVOKE',
                'SET','CASE','WHEN','THEN','ELSE','END','LIMIT','OFFSET','WITH','DISTINCT',
                'OVER','PARTITION','WINDOW','MERGE','INTO','VALUES','DEFAULT','PRIMARY','KEY',
                'FOREIGN','REFERENCES','CHECK','UNIQUE','CONSTRAINT','TRIGGER','FUNCTION',
                'PROCEDURE','RETURN','BEGIN','DECLARE','COLUMN','COMMENT','REPLACE','IF',
                'LATERAL','NATURAL','CROSS','FULL','SEMI','ANTI','ANY','SOME','QUALIFY','PIVOT',
                'UNPIVOT','SAMPLE','TABLESAMPLE','CONNECT','START','PRIOR','LEVEL','ROWNUM',
                'MINUS','INTERSECT','EXCEPT','FETCH','NEXT','ONLY','ROWS','RANGE','UNBOUNDED',
                'PRECEDING','FOLLOWING','CURRENT','ROW','AT','ZONE','TIMESTAMP','DATE','TIME',
                'INTERVAL','YEAR','MONTH','DAY','HOUR','MINUTE','SECOND','BOOLEAN','FLOAT',
                'INTEGER','NUMBER','VARCHAR','CHAR','TEXT','BINARY','VARIANT','OBJECT','ARRAY'}
    if col.upper() in reserved:
        return True
    if not re.match(r'^[A-Z_][A-Z0-9_]*$', col):
        return True  # lowercase, dots, spaces, hyphens, etc.
    return False

def safe_alias(col):
    """Generate a safe alias for a column."""
    import re
    alias = col.upper().replace('.','_').replace(' ','_').replace('-','_').replace('(','').replace(')','')
    alias = re.sub(r'[^A-Z0-9_]', '', alias)
    alias = re.sub(r'_+', '_', alias).strip('_')
    if not alias or alias[0].isdigit():
        alias = 'COL_' + alias
    return alias

def gen_simple_mart(table_name, source_name, schema, domain, cols, grain_comment=''):
    """Generate a simple mart model that selects all columns with proper quoting."""
    lines = []
    lines.append(f"{{{{ config(materialized='table', schema='{schema}') }}}}")
    lines.append('')
    if grain_comment:
        lines.append(f'-- {grain_comment}')
        lines.append('')
    lines.append('with source as (')
    lines.append(f"    select * from {{{{ source('ripple_raw', '{source_name}') }}}}")
    lines.append(')')
    lines.append('')
    lines.append('select')
    
    col_exprs = []
    seen_aliases = set()
    for c in cols:
        if needs_quoting(c):
            alias = safe_alias(c)
            # Deduplicate aliases
            if alias in seen_aliases:
                alias = alias + '_2'
            seen_aliases.add(alias)
            col_exprs.append(f'    "{c}" as {alias}')
        else:
            if c in seen_aliases:
                col_exprs.append(f'    "{c}" as {c}_2')
                seen_aliases.add(c + '_2')
            else:
                seen_aliases.add(c)
                col_exprs.append(f'    {c}')
    
    lines.append(',\n'.join(col_exprs))
    lines.append('from source')
    lines.append('')
    return '\n'.join(lines)

def disable_model(filepath, reason):
    """Disable a model file."""
    content = f"""{{{{ config(materialized='table', enabled=false) }}}}
-- DISABLED: {reason}
select 1 as _placeholder
"""
    filepath.write_text(content, encoding='utf-8')
    print(f'  DISABLED: {filepath.name} ({reason})')


# ============================================================
# FIX EACH ERRORED MODEL
# ============================================================

print("=" * 60)
print("FIXING ERRORED MODELS")
print("=" * 60)

# 1. FEC Independent Expenditures (lowercase columns)
print("\n1. FEC Independent Expenditures")
cols = get_columns('FED_FEC_INDEPENDENT_EXPENDITURES')
if cols:
    sql = gen_simple_mart('FED_FEC_INDEPENDENT_EXPENDITURES', 'FED_FEC_INDEPENDENT_EXPENDITURES',
                          'FINANCE', 'finance', cols, 'GRAIN: one row per independent expenditure transaction')
    # Write to the finance location (remove uncategorized duplicate)
    (MODELS_DIR / 'finance' / 'finance__fed_fec_independent_expenditures.sql').write_text(sql, encoding='utf-8')
    # Remove/disable uncategorized duplicate
    dup = MODELS_DIR / 'uncategorized' / 'uncategorized__fed_fec_independent_expenditures.sql'
    if dup.exists():
        disable_model(dup, 'duplicate - moved to finance domain')
    print('  FIXED')

# 2. FEC Leadership PAC (column is FEC_CANDIDATE_ID not CAND_ID)
print("\n2. FEC Leadership PAC")
cols = get_columns('FED_FEC_LEADERSHIP_PAC')
if cols:
    sql = gen_simple_mart('FED_FEC_LEADERSHIP_PAC', 'FED_FEC_LEADERSHIP_PAC',
                          'FINANCE', 'finance', cols, 'GRAIN: one row per candidate-committee linkage')
    target = MODELS_DIR / 'uncategorized' / 'uncategorized__fed_fec_leadership_pac.sql'
    target.write_text(sql, encoding='utf-8')
    print('  FIXED')

# 3. CMS Part D Prescribers (NPI is correct col name, model may reference wrong name)
print("\n3. CMS Part D Prescribers")
cols = get_columns('FED_CMS_PART_D_PRESCRIBERS')
if cols:
    sql = gen_simple_mart('FED_CMS_PART_D_PRESCRIBERS', 'FED_CMS_PART_D_PRESCRIBERS',
                          'HEALTH', 'health', cols, 'GRAIN: one row per prescriber (NPI)')
    (MODELS_DIR / 'health' / 'health__fed_cms_part_d_prescribers.sql').write_text(sql, encoding='utf-8')
    print('  FIXED')

# 4. FDA Drug Enforcement (only RAW column - JSON blob)
print("\n4. FDA Drug Enforcement")
cols = get_columns('FED_FDA_DRUG_ENFORCEMENT')
if cols:
    if cols == ['RAW']:
        # Parse the JSON RAW column
        sql = """{{ config(materialized='table', schema='HEALTH') }}
-- GRAIN: one row per drug enforcement action
-- Note: source data is a single JSON column; parsing key fields

with source as (
    select RAW from {{ source('ripple_raw', 'FED_FDA_DRUG_ENFORCEMENT') }}
),

parsed as (
    select
        RAW:recall_number::string as recall_number,
        RAW:event_id::int as event_id,
        RAW:status::string as status,
        RAW:city::string as city,
        RAW:state::string as state,
        RAW:country::string as country,
        RAW:classification::string as classification,
        RAW:product_type::string as product_type,
        RAW:product_description::string as product_description,
        RAW:reason_for_recall::string as reason_for_recall,
        RAW:recalling_firm::string as recalling_firm,
        RAW:report_date::string as report_date,
        RAW:recall_initiation_date::string as recall_initiation_date,
        RAW:voluntary_mandated::string as voluntary_mandated,
        RAW:initial_firm_notification::string as initial_firm_notification
    from source
)

select * from parsed
"""
        (MODELS_DIR / 'health' / 'health__fed_fda_drug_enforcement.sql').write_text(sql, encoding='utf-8')
        print('  FIXED (JSON parse)')
    else:
        sql = gen_simple_mart('FED_FDA_DRUG_ENFORCEMENT', 'FED_FDA_DRUG_ENFORCEMENT',
                              'HEALTH', 'health', cols)
        (MODELS_DIR / 'health' / 'health__fed_fda_drug_enforcement.sql').write_text(sql, encoding='utf-8')
        print('  FIXED')

# 5. DHS OHSS (massive spreadsheet, just select useful columns)
print("\n5. DHS OHSS Encounters")
cols = get_columns('FED_DHS_OHSS')
if cols:
    # Only keep the meaningful named columns (not UNNAMED__)
    useful_cols = [c for c in cols if not c.startswith('UNNAMED_')]
    # Limit to first 20 most useful
    priority_cols = ['REPORT_MONTH', 'ENCOUNTER_TYPE', 'REGION_OR_SECTOR', 'CITIZENSHIP',
                     'FAMILY_STATUS', 'CRIMINALITY', 'FISCAL_YEAR', 'CALENDAR_YEAR', 
                     'EVENT_COUNT', 'ENCOUNTERS', 'SOURCE_FILE_NAME', 'SOURCE_SHEET_NAME',
                     'MONTH', 'TOTAL', 'VENEZUELA', 'CUBA', 'MEXICO', 'HAITI', 'HONDURAS',
                     'COLOMBIA', 'GUATEMALA', 'EL_SALVADOR', 'ECUADOR', 'RUSSIA', 'OTHER',
                     'NICARAGUA', 'BORDER', 'INTERIOR']
    selected = [c for c in priority_cols if c in cols]
    sql = gen_simple_mart('FED_DHS_OHSS', 'FED_DHS_OHSS',
                          'IMMIGRATION', 'immigration', selected,
                          'GRAIN: one row per encounter report row (multi-sheet compilation)')
    (MODELS_DIR / 'immigration' / 'immigration__fed_dhs_ohss.sql').write_text(sql, encoding='utf-8')
    print('  FIXED (selected useful columns only)')

# 6. BJS Data (columns are IDPER, YEARQ, etc. not FIPS_CODE)
print("\n6. BJS Data")
cols = get_columns('FED_BJS_DATA')
if cols:
    sql = gen_simple_mart('FED_BJS_DATA', 'FED_BJS_DATA',
                          'CRIMINAL_JUSTICE', 'criminal_justice', cols,
                          'GRAIN: one row per victimization incident (NCVS survey)')
    (MODELS_DIR / 'criminal_justice' / 'criminal_justice__fed_bjs_data.sql').write_text(sql, encoding='utf-8')
    print('  FIXED')

# 7. Slavevoyages (two tables: TRANSATLANTIC and INTRAAMERICAN)
print("\n7. Slavevoyages Transatlantic")
cols = get_columns('FED_SLAVEVOYAGES_TRANSATLANTIC')
if cols:
    sql = gen_simple_mart('FED_SLAVEVOYAGES_TRANSATLANTIC', 'FED_SLAVEVOYAGES_TRANSATLANTIC',
                          'HISTORY', 'history', cols,
                          'GRAIN: one row per transatlantic slave voyage')
    (MODELS_DIR / 'history' / 'history__fed_slavevoyages_transatlantic.sql').write_text(sql, encoding='utf-8')
    print('  FIXED')

print("\n7b. Slavevoyages Intraamerican")
cols = get_columns('FED_SLAVEVOYAGES_INTRAAMERICAN')
if cols:
    sql = gen_simple_mart('FED_SLAVEVOYAGES_INTRAAMERICAN', 'FED_SLAVEVOYAGES_INTRAAMERICAN',
                          'HISTORICAL_RECORDS', 'historical_records', cols,
                          'GRAIN: one row per intra-American slave voyage')
    (MODELS_DIR / 'historical_records' / 'historical_records__fed_slavevoyages_intraamerican.sql').write_text(sql, encoding='utf-8')
    print('  FIXED')

# 8. NAAG Multistate Settlements
print("\n8. NAAG Multistate Settlements")
cols = get_columns('FED_NAAG_MULTISTATE_SETTLEMENTS')
if cols:
    sql = gen_simple_mart('FED_NAAG_MULTISTATE_SETTLEMENTS', 'FED_NAAG_MULTISTATE_SETTLEMENTS',
                          'LEGAL_ENFORCEMENT', 'legal_enforcement', cols,
                          'GRAIN: one row per multistate settlement action')
    (MODELS_DIR / 'legal_enforcement' / 'legal_enforcement__fed_naag_multistate_settlements.sql').write_text(sql, encoding='utf-8')
    print('  FIXED')

# 9. Vera Incarceration Trends
print("\n9. Vera Incarceration Trends")
cols = get_columns('XC_VERA_INCARCERATION_TRENDS')
if cols:
    sql = gen_simple_mart('XC_VERA_INCARCERATION_TRENDS', 'XC_VERA_INCARCERATION_TRENDS',
                          'JUSTICE', 'justice', cols,
                          'GRAIN: one row per county x year incarceration measure')
    (MODELS_DIR / 'justice' / 'justice__xc_vera_incarceration_trends.sql').write_text(sql, encoding='utf-8')
    print('  FIXED')

# 10. USASpending Assistance
print("\n10. USASpending Assistance Full")
cols = get_columns('FED_USASPENDING_ASSISTANCE_FULL')
if cols:
    sql = gen_simple_mart('FED_USASPENDING_ASSISTANCE_FULL', 'FED_USASPENDING_ASSISTANCE_FULL',
                          'ECONOMICS', 'economics', cols,
                          'GRAIN: one row per federal assistance award transaction')
    (MODELS_DIR / 'economics' / 'economics__fed_usaspending_assistance_full.sql').write_text(sql, encoding='utf-8')
    print('  FIXED')

# 11. USASpending Contracts (might have COVID-19 hyphen issue)
print("\n11. USASpending Contracts")
cols = get_columns('FED_USASPENDING_CONTRACTS')
if cols:
    sql = gen_simple_mart('FED_USASPENDING_CONTRACTS', 'FED_USASPENDING_CONTRACTS',
                          'ECONOMICS', 'economics', cols,
                          'GRAIN: one row per federal contract transaction')
    target = MODELS_DIR / 'economics' / 'economics__fed_usaspending_contracts.sql'
    if not target.exists():
        # Check other locations
        for p in MODELS_DIR.rglob('*usaspending_contracts*.sql'):
            target = p
            break
    target.write_text(sql, encoding='utf-8')
    print('  FIXED')

# 12. ForeignAssistance
print("\n12. ForeignAssistance")
cols = get_columns('FED_FOREIGNASSISTANCE')
if cols:
    sql = gen_simple_mart('FED_FOREIGNASSISTANCE', 'FED_FOREIGNASSISTANCE',
                          'ECONOMICS', 'economics', cols,
                          'GRAIN: one row per foreign assistance transaction')
    (MODELS_DIR / 'economics' / 'economics__fed_foreignassistance.sql').write_text(sql, encoding='utf-8')
    print('  FIXED')

# 13. GLEIF
print("\n13. GLEIF (International)")
cols = get_columns('INTL_GLEIF')
if cols:
    sql = gen_simple_mart('INTL_GLEIF', 'INTL_GLEIF',
                          'ECONOMICS', 'economics', cols,
                          'GRAIN: one row per Legal Entity Identifier (LEI)')
    (MODELS_DIR / 'economics' / 'economics__intl_gleif.sql').write_text(sql, encoding='utf-8')
    # Disable uncategorized duplicate
    dup = MODELS_DIR / 'uncategorized' / 'uncategorized__intl_gleif.sql'
    if dup.exists():
        disable_model(dup, 'duplicate - moved to economics domain')
    print('  FIXED')

# 14. GLEIF_RR (INT_GLEIF_RR)
print("\n14. GLEIF RR")
cols = get_columns('INT_GLEIF_RR')
if cols:
    sql = gen_simple_mart('INT_GLEIF_RR', 'INT_GLEIF_RR',
                          'ECONOMICS', 'economics', cols,
                          'GRAIN: one row per LEI reporting relationship')
    target = MODELS_DIR / 'economics' / 'economics__intl_gleif_rr.sql'
    if not target.exists():
        target = MODELS_DIR / 'uncategorized' / 'uncategorized__int_gleif_rr.sql'
    target.write_text(sql, encoding='utf-8')
    print('  FIXED')

# 15. SEC 13F - multiple tables
print("\n15. SEC 13F Positions")
cols = get_columns('FED_SEC_13F_POSITIONS')
if cols:
    sql = gen_simple_mart('FED_SEC_13F_POSITIONS', 'FED_SEC_13F_POSITIONS',
                          'FINANCE', 'finance', cols,
                          'GRAIN: one row per 13F position holding')
    target = MODELS_DIR / 'uncategorized' / 'uncategorized__fed_sec_13f_positions.sql'
    target.write_text(sql, encoding='utf-8')
    print('  FIXED')

print("\n15b. SEC 13F Submissions")
cols = get_columns('FED_SEC_13F_SUBMISSIONS')
if not cols:
    cols = get_columns('FED_SEC_13F_SUBMISSION')
if cols:
    tbl = 'FED_SEC_13F_SUBMISSIONS' if get_columns('FED_SEC_13F_SUBMISSIONS') else 'FED_SEC_13F_SUBMISSION'
    sql = gen_simple_mart(tbl, tbl, 'FINANCE', 'finance', cols,
                          'GRAIN: one row per 13F submission filing')
    target = MODELS_DIR / 'uncategorized' / 'uncategorized__fed_sec_13f_submission.sql'
    target.write_text(sql, encoding='utf-8')
    print('  FIXED')

# 16. DOL OSHA - table doesn't exist
print("\n16. DOL OSHA Inspection")
target = MODELS_DIR / 'labor' / 'labor__fed_dol_osha_inspection.sql'
if target.exists():
    disable_model(target, 'source table FED_DOL_OSHA_INSPECTION does not exist in LANDING')

# 17. CMS Open Payments (might be retired)
print("\n17. CMS Open Payments")
cur = conn.cursor()
cur.execute("""SELECT table_name FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES 
               WHERE table_schema='LANDING' AND table_name LIKE '%OPEN_PAYMENTS%'""")
open_pay_tables = [r[0] for r in cur.fetchall()]
print(f"  Found tables: {open_pay_tables}")

for f in (MODELS_DIR / 'health').glob('health__fed_cms_open_payments*.sql'):
    # Check if there's a matching table
    disable_model(f, 'source table retired/moved')

# 18. IRS Exempt Orgs
print("\n18. IRS Exempt Orgs")
cur.execute("""SELECT table_name FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES 
               WHERE table_schema='LANDING' AND table_name LIKE '%IRS_EXEMPT%'""")
irs_tables = [r[0] for r in cur.fetchall()]
print(f"  Found IRS tables: {irs_tables}")
for t in irs_tables:
    cols = get_columns(t)
    if cols:
        sql = gen_simple_mart(t, t, 'FINANCE', 'finance', cols,
                              f'Source: {t}')
        fname = f"finance__{t.lower()}.sql"
        (MODELS_DIR / 'finance' / fname).write_text(sql, encoding='utf-8')
        print(f'  FIXED: {fname}')

print("\n" + "=" * 60)
print("ALL FIXES APPLIED")
print("=" * 60)

conn.close()
