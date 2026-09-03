# INTL_EUROSTAT

rows 450  columns 12  scan 2.2s

roles: amount 1, audit 2, category 3, empty 2, other 3, who 1

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| OBS_VALUE | 450 | 0 | 0.54 | 85.93 | 95.10 | 1.2K |

## who

_SRC_SHA256 by rows
       450  72a17cbe4e13738bbcf6651ba51c591cd32603a234c2532f19ac54033007dd14

_SRC_SHA256 by dollars
        1.2K      450 rows  72a17cbe4e13738bbcf6651ba51c591cd32603a234c2532f19ac54033007

## what

DATAFLOW_ID: TESPN070 96%, LFST_DPW_05 4%

GEO: EU_V_NO 12%, TR 8%, SK 8%, SI 8%, SE 8%, RS 8%, RO 8%, PT 8%, PL 8%, NO 8%, NL 8%, MK 8%

TIME: 2022 28%, 2020 25%, 2021 24%, 2023 23%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DATAFLOW_ID | category | 2 | 0 | TESPN070 432; LFST_DPW_05 18 |
| GEO | category | 37 | 0 | EU_V_NO 18; TR 12; SK 12; SI 12 |
| TIME | category | 4 | 0 | 2022 126; 2020 111; 2021 108; 2023 105 |
| OBS_VALUE | amount | 85 | 0 | 0.48 25; 0.57 23; 0.59 21; 0.53 17 |
| OBS_STATUS | empty | 1 | 450 |  |
| UNIT | other | 1 | 0 | PC 450 |
| FREQ | other | 1 | 0 | A 450 |
| INDICATOR | empty | 1 | 450 |  |
| RAW_XML_SERIES_KEY | other | 130 | 0 | geo=TR;unit=PC;sex=T;freq 4; geo=SK;unit=PC;sex=T;freq 4; geo=SI;unit=PC;sex=T;freq 4; geo=SE;unit=PC;sex=T;freq 4 |
| _INGESTED_AT | audit | 1 | 0 | 1783021725214893 450 |
| _SOURCE_RUN_ID | audit | 1 | 0 | a92a1d22-e586-4044-920c-4 450 |
| _SRC_SHA256 | who | 1 | 0 | 72a17cbe4e13738bbcf6651ba 450 |
