{{ config(materialized='table', schema='JUSTICE') }}

-- Source: FDIC Enforcement Decisions and Orders, orders.fdic.gov (10,838 rows,
-- 1975-06-11 to 2026-07-31, 23 undated). Landed 2026-09-07 by
-- scripts/fdic_enforcement_load.py over the site's Salesforce Aura endpoint;
-- see the staging model for the grain and the cert caveats.
--
-- Docket 118 join: cert_number -> FED_FDIC_BANK_DATA.CERT (27,836 institutions,
-- CERT unique). Measured 2026-09-07: 10,565 of 10,838 orders attach (97.5%);
-- 10,565 of the 10,606 with a numeric cert (99.6%). The misses are 183 'N/A'
-- certs (bank redacted on adjudicated decisions), 49 blanks (Section 19
-- letters about a person, no bank), and 41 numeric certs the directory does
-- not carry. bank_* columns below come from the directory and are null on the
-- 273 unattached rows.

with orders as (
    select * from {{ ref('stg_fed_fdic_enforcement_orders__orders') }}
),

banks as (
    select
        try_to_number(cert) as cert,
        name                as bank_name,
        city                as bank_city,
        stalp               as bank_state,
        bkclass             as bank_class,
        active              as bank_active,
        endefymd            as bank_end_date,
        rssdid              as bank_rssd_id,
        holding_company_name as bank_holding_company
    from {{ ref('stg_fed_fdic_bank_data__institutions') }}
)

select
    o.order_id,
    o.order_date,
    year(o.order_date)                                 as order_year,
    o.order_title,
    o.docket_number,
    o.order_category,
    o.order_type,
    o.institution_name,
    o.city,
    o.state,
    o.cert_number,
    o.bank_count,
    o.banks_all,
    o.respondents,
    o.respondent_count,
    o.cmp_amount_total,
    o.restitution_amount_total,
    o.nmls_ids,
    o.termination_date,
    o.termination_comments,
    o.public_order_action,
    o.status,
    o.document_url,
    b.cert is not null                                 as cert_attached,
    b.bank_name,
    b.bank_city,
    b.bank_state,
    b.bank_class,
    b.bank_active,
    b.bank_end_date,
    b.bank_rssd_id,
    b.bank_holding_company,
    'fed_fdic_enforcement_orders'                      as source_id,
    o._ingested_at,
    o._source_run_id
from orders o
left join banks b
    on o.cert_number = b.cert
