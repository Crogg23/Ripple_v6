-- Scratch: renders every landing_date_casts macro so Jinja/SQL syntax is
-- proven before use. Not a model, not run against the warehouse.
select
    {{ landing_parse_date('"RPT_DATE"', 'us', 'TEXT') }} as t_us,
    {{ landing_parse_date('"HPSA_WITHDRAWN_DATE_STRING"', 'iso', 'TEXT') }} as t_iso,
    {{ landing_parse_date('"HUC8"', 'ymd8', 'TEXT') }} as t_ymd8,
    {{ landing_parse_date('"TRANSACTION_DT"', 'mdy8', 'TEXT') }} as t_mdy8,
    {{ landing_parse_date('"SOME_COL"', 'dmon', 'TEXT') }} as t_dmon,
    {{ landing_parse_date('"LOADDATE"', 'epochms', 'FLOAT') }} as t_epochms_num,
    {{ landing_parse_date('"SOME_TEXT_EPOCHMS"', 'epochms', 'TEXT') }} as t_epochms_text,
    {{ landing_parse_date('"SOME_COL"', 'epochs', 'TEXT') }} as t_epochs,
    {{ landing_parse_audit_epoch('"INGESTED_AT"') }} as t_audit_epoch,
    {{ landing_range_start('"ED30_DATE"', 'ddmonyyyy') }} as t_range_start_a,
    {{ landing_range_end('"ED30_DATE"', 'ddmonyyyy') }} as t_range_end_a,
    {{ landing_range_start('"TTM_DATE_RANGE"', 'monthyyyy') }} as t_range_start_b,
    {{ landing_range_end('"TTM_DATE_RANGE"', 'monthyyyy') }} as t_range_end_b,
    {{ landing_translate_granularity('"DATE_GRANULARITY_DOB"') }} as t_granularity,
    {{ landing_combine_time_date('"STOP_TIME"', landing_parse_date('"STOP_DATE"', 'epochms', 'FLOAT')) }} as t_combine
from (select 1) as dummy
