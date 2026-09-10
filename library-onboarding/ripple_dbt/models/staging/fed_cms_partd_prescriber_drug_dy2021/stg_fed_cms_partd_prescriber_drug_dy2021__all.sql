    with source as (
        select * from {{ source('ripple_raw', 'FED_CMS_PARTD_PRESCRIBER_DRUG_DY2021') }}
    )

    select
        "NPI",
"PRSCRBR_LAST_ORG_NAME",
"PRSCRBR_FIRST_NAME",
"PRSCRBR_CITY",
"PRSCRBR_STATE_ABRVTN",
"PRSCRBR_STATE_FIPS",
"PRSCRBR_TYPE",
"PRSCRBR_TYPE_SRC",
"BRND_NAME",
"GNRC_NAME",
"TOT_CLMS",
"TOT_30DAY_FILLS",
"TOT_DAY_SUPLY",
"TOT_DRUG_CST",
"TOT_BENES",
"GE65_SPRSN_FLAG",
"GE65_TOT_CLMS",
"GE65_TOT_30DAY_FILLS",
"GE65_TOT_DRUG_CST",
"GE65_TOT_DAY_SUPLY",
"GE65_BENE_SPRSN_FLAG",
"GE65_TOT_BENES",
_INGESTED_AT,
_SOURCE_RUN_ID
    from source
    qualify row_number() over (
        partition by "NPI"
        order by _INGESTED_AT desc
    ) = 1
