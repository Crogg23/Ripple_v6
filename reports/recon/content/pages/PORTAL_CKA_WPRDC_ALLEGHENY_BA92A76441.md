# PORTAL_CKA_WPRDC_ALLEGHENY_BA92A76441

rows 9  columns 7  scan 2.2s

roles: audit 2, category 4, date 1, who 1

## when

INGESTED_AT
  2026         9  ##############################

## who

SRC_SHA256 by rows
         9  9bd0a60766d107860ddf79f524d00ccd92da19a12cf6417f7220ea67fb0db706

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  9bd0a60766d107860ddf79f524d00ccd92da19a1  2026:9

## what

FIELD_NAME: purchase_type 11%, payment_type 11%, amount 11%, date_recorded_utc 11%, purchase_date_utc 11%, payment_end_utc 11%, payment_start_utc 11%, zone 11%, meter_id 11%

TYPE: text 78%, float 22%

DESCRIPTION: Indicates whether the purchase 11%, Means of payment ("Cash" = cas 11%, The amount paid in dollars in  11%, When the purchase was recorded 11%, When the purchase took place ( 11%, Datetime through which parking 11%, Datetime that the parking sess 11%, Identifier for the chief repor 11%, Human-readable ID of the meter 11%

EXAMPLE: New 11%, Mobile 11%, 13.25 11%, 2018-10-01T09:53:47 11%, 2018-10-01T09:53:21 11%, 2018-10-02T01:03:03 11%, 2018-10-01T04:03:03 11%, 341 - 18th & Sidney Lot 11%, PBP341 11%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FIELD_NAME | category | 9 | 0 | purchase_type 1; payment_type 1; amount 1; date_recorded_utc 1 |
| TYPE | category | 2 | 0 | text 7; float 2 |
| DESCRIPTION | category | 9 | 0 | Indicates whether the pur 1; Means of payment ("Cash"  1; The amount paid in dollar 1; When the purchase was rec 1 |
| EXAMPLE | category | 9 | 0 | New 1; Mobile 1; 13.25 1; 2018-10-01T09:53:47 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:06:37.46104 9 |
| SOURCE_RUN_ID | audit | 1 | 0 | 92c5219c-3437-4d68-a5b2-a 9 |
| SRC_SHA256 | who | 1 | 0 | 9bd0a60766d107860ddf79f52 9 |
