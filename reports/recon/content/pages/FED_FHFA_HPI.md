# FED_FHFA_HPI

rows 184.8K  columns 15  scan 3.0s

roles: amount 3, audit 2, category 6, other 3, who 1

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| INDEX_NSA | 184.8K | 18.62 | 171.51 | 622.68 | 1.3K | 36.68M |
| INDEX_SA | 95.4K | 74.48 | 186.53 | 633.34 | 1.0K | 20.53M |
| RSTDERR | 57.8K | 0 | 2.06 | 10.61 | 15.76 | 154.7K |

## who

PLACE_NAME by rows
      1.1K  United States
       910  South Atlantic Division
       910  West South Central Division
       910  West North Central Division
       910  East South Central Division
       910  New England Division
       910  Middle Atlantic Division
       910  Pacific Division
       910  Mountain Division
       910  East North Central Division
       628  Los Angeles-Long Beach-Glendale, CA (MSAD)
       627  Anaheim-Santa Ana-Irvine, CA (MSAD)
       627  Oakland-Fremont-Berkeley, CA (MSAD)
       626  San Francisco-San Mateo-Redwood City, CA (MSAD)
       626  Chicago-Naperville-Schaumburg, IL (MSAD)
       626  Warren-Troy-Farmington Hills, MI (MSAD)
       625  Miami-Miami Beach-Kendall, FL (MSAD)
       625  San Diego-Chula Vista-Carlsbad, CA
       624  Atlanta-Sandy Springs-Roswell, GA (MSAD)
       623  Riverside-San Bernardino-Ontario, CA

PLACE_NAME by dollars
      246.9K      910 rows  Mountain Division
      238.6K     1.1K rows  United States
      235.4K      910 rows  Pacific Division
      227.3K      910 rows  New England Division
      211.8K      910 rows  Middle Atlantic Division
      208.5K      910 rows  South Atlantic Division
      197.1K      612 rows  Massachusetts
      196.4K      910 rows  West North Central Division
      189.6K      910 rows  West South Central Division
      187.1K      910 rows  East South Central Division
      181.5K      612 rows  Colorado
      179.4K      910 rows  East North Central Division
      178.9K      612 rows  Oregon
      175.6K      612 rows  Utah
      174.3K      612 rows  Washington
      172.9K      612 rows  Montana
      170.8K      487 rows  District of Columbia
      168.3K      612 rows  Hawaii
      167.3K      612 rows  New York
      166.3K      625 rows  Miami-Miami Beach-Kendall, FL (MSAD)

## what

HPI_TYPE: traditional 96%, non-metro 3%, distress-free 1%, developmental 0%, manufactured 0%

HPI_FLAVOR: all-transactions 48%, expanded-data 36%, purchase-only 16%

FREQUENCY: quarterly 98%, monthly 2%

LEVEL: MSA 78%, State 17%, USA or Census Division 5%, Puerto Rico 0%

PERIOD: 1 25%, 4 25%, 3 25%, 2 24%, 12 0%, 11 0%, 10 0%, 9 0%, 8 0%, 7 0%, 6 0%, 5 0%

NOTE: Note: Fewer than 1,000 repeat- 100%, Note: Index value suppressed d 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| HPI_TYPE | category | 5 | 0 | traditional 176.5K; non-metro 5.9K; distress-free 2.0K; developmental 245 |
| HPI_FLAVOR | category | 3 | 0 | all-transactions 89.3K; expanded-data 66.4K; purchase-only 29.1K |
| FREQUENCY | category | 2 | 0 | quarterly 180.6K; monthly 4.2K |
| LEVEL | category | 4 | 0 | MSA 144.5K; State 30.7K; USA or Census Division 9.3K; Puerto Rico 245 |
| PLACE_NAME | who | 478 | 0 | United States 1.2K; Wyoming 1.1K; West Virginia 1.1K; Wisconsin 1.1K |
| PLACE_ID | other | 467 | 0 | USA 1.2K; WY 1.1K; WV 1.1K; WI 1.1K |
| YR | other | 52 | 0 | 2025 4.8K; 2024 4.8K; 2023 4.8K; 2021 4.8K |
| PERIOD | category | 12 | 0 | 1 46.2K; 4 45.3K; 3 45.3K; 2 45.2K |
| INDEX_NSA | amount | 42.5K | 2 | 100.00 1.2K; 170.79 924; 270.34 923; 247.97 923 |
| INDEX_SA | amount | 31.5K | 89.4K | 100.00 685; 271.30 479; 253.44 479; 238.63 479 |
| RSTDERR | amount | 1.3K | 127.0K | 0.00 410; 0.47 340; 0.46 320; 0.45 320 |
| NOTE | category | 4 | 127.0K | Note: Fewer than 1,000 re 452; Note: Index value suppres 2 |
| INGESTED_AT | audit | 1 | 0 | 1782615445917690 184.8K |
| SOURCE_RUN_ID | audit | 1 | 0 | 78fe144c-944c-4143-8170-1 184.8K |
| SRC_SHA256 | other | 1 | 0 | a21426a1798ec61d79804d911 184.8K |
