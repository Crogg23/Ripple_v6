-- Scratch: renders every ripple_time macro against known-nasty values so the
-- standard is proven before it is applied to 67 live models. Not a model.
with v as (
    select * from values
        ('iso',        '2026-03-15'),
        ('iso_ts',     '2026-03-15T09:30:00'),
        ('us',         '3/15/2026'),
        ('us2_recent', '05/29/26'),
        ('us2_old',    '05/29/85'),
        ('dmon',       '15-MAR-2026'),
        ('dmon2_zero', '01-MAR-00'),
        ('dmon2_mid',  '02-JUN-16'),
        ('dmon2_now',  '25-SEP-25'),
        ('ymd',        '20260315'),
        ('blank_1900', '1900-01-01'),
        ('fiscal_year','2012'),
        ('prec_code',  '3'),
        ('empty',      ''),
        ('junk',       'SEE ADDTL INFO')
        as t(label, raw)
)
select
    label,
    raw,
    {{ ripple_ts_from_date('raw', 'auto', 2069, ['1900-01-01']) }}  as ts_auto,
    {{ ripple_ts_from_year('raw') }}                                as ts_year,
    {{ ripple_ts_from_yyyymm('raw') }}                              as ts_month,
    {{ ripple_ts_from_yearquarter('raw') }}                         as ts_quarter
from v
union all
select 'q_2004q1', '2004q1', null, null, null, {{ ripple_ts_from_yearquarter("'2004q1'") }}
union all
select 'q_2014Q2', '2014Q2', null, null, null, {{ ripple_ts_from_yearquarter("'2014Q2'") }}
union all
select 'm_202403', '202403', null, null, {{ ripple_ts_from_yyyymm("'202403'") }}, null
union all
select 'y_2024',   '2024',   null, {{ ripple_ts_from_year("'2024'") }}, null, null
