"""Fix part 2: CMS Open Payments + ensure source YAMLs reference correct tables."""
import snowflake.connector
import os
from pathlib import Path

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
SOURCES_DIR = Path(r'c:\Code\Ripple_v6\library-onboarding\ripple_dbt\models')

# === Fix CMS Open Payments ===
print("Fixing CMS Open Payments...")

# Select the most important columns (NPI is the key)
cms_op_sql = """{{ config(materialized='table', schema='HEALTH') }}
-- GRAIN: one row per payment record (RECORD_ID)
-- Key: NPI (National Provider Identifier)

with source as (
    select * from {{ source('ripple_raw', 'FED_CMS_OPEN_PAYMENTS') }}
)

select
    RECORD_ID,
    NPI,
    COVERED_RECIPIENT_TYPE,
    COVERED_RECIPIENT_PROFILE_ID,
    COVERED_RECIPIENT_FIRST_NAME,
    COVERED_RECIPIENT_LAST_NAME,
    RECIPIENT_CITY,
    RECIPIENT_STATE,
    RECIPIENT_ZIP_CODE,
    COVERED_RECIPIENT_PRIMARY_TYPE_1,
    COVERED_RECIPIENT_SPECIALTY_1,
    SUBMITTING_APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_NAME,
    APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME,
    APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_STATE,
    TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS,
    DATE_OF_PAYMENT,
    FORM_OF_PAYMENT_OR_TRANSFER_OF_VALUE,
    NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE,
    PHYSICIAN_OWNERSHIP_INDICATOR,
    PROGRAM_YEAR,
    TEACHING_HOSPITAL_NAME,
    CCN
from source
"""
(MODELS_DIR / 'health' / 'health__fed_cms_open_payments.sql').write_text(cms_op_sql, encoding='utf-8')
print("  Fixed: health__fed_cms_open_payments.sql")

cms_op_2022 = cms_op_sql.replace("'FED_CMS_OPEN_PAYMENTS'", "'FED_CMS_OPEN_PAYMENTS_2022'")
(MODELS_DIR / 'health' / 'health__fed_cms_open_payments_2022.sql').write_text(cms_op_2022, encoding='utf-8')
print("  Fixed: health__fed_cms_open_payments_2022.sql")

cms_op_2023 = cms_op_sql.replace("'FED_CMS_OPEN_PAYMENTS'", "'FED_CMS_OPEN_PAYMENTS_2023'")
(MODELS_DIR / 'health' / 'health__fed_cms_open_payments_2023.sql').write_text(cms_op_2023, encoding='utf-8')
print("  Fixed: health__fed_cms_open_payments_2023.sql")

# === Build comprehensive source YAML ===
print("\nBuilding comprehensive source YAML for all tables...")

# Get ALL tables in LANDING
cur = conn.cursor()
cur.execute("""SELECT table_name FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES 
               WHERE table_schema = 'LANDING' ORDER BY table_name""")
all_tables = [r[0] for r in cur.fetchall()]
print(f"  Found {len(all_tables)} tables in LANDING")

# Check which tables are already referenced in source YAMLs
existing_refs = set()
for yml_file in SOURCES_DIR.rglob('*sources*.yml'):
    content = yml_file.read_text(encoding='utf-8')
    for table in all_tables:
        if table in content:
            existing_refs.add(table)

print(f"  Already referenced in YAML: {len(existing_refs)}")
missing = [t for t in all_tables if t not in existing_refs]
print(f"  Missing from YAML: {len(missing)}")

# Write a catch-all source YAML for missing tables
if missing:
    yaml_lines = ['version: 2', '', 'sources:', '  - name: ripple_raw',
                  '    database: LIBRARY_RAW', '    schema: LANDING', '    tables:']
    for t in sorted(missing):
        yaml_lines.append(f'      - name: {t}')
    
    catchall_path = SOURCES_DIR / 'marts' / '_all_sources.yml'
    catchall_path.write_text('\n'.join(yaml_lines) + '\n', encoding='utf-8')
    print(f"  Wrote catch-all source YAML: {catchall_path.name} ({len(missing)} tables)")

print("\nDone!")
conn.close()
