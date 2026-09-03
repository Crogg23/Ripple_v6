# FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS

rows 10.41M  columns 12  scan 5.5s

roles: amount 1, audit 2, category 5, other 3, who 1

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ANNUAL_EMISSION | 10.41M | -1.4K | 1.04 | 309.5K | 47.63B | 39974.94B |

## who

POLLUTANT_NAME by rows
    381.5K  Volatile organic compounds
    319.2K  Primary PM10 (filterables and condensibles)
    318.6K  Primary PM2.5 (filterables and condensibles)
    305.1K  Nitrogen oxides
    292.1K  Carbon monoxide
    284.6K  Benzene
    278.7K  Toluene
    276.1K  Sulfur dioxide
    245.4K  Xylene
    239.6K  Formaldehyde
    226.1K  Primary PM10, filterable portion only
    225.3K  Primary PM2.5, filterable portion only
    224.8K  Primary PM condensible portion,  less than 1 micron
    217.0K  Naphthalene
    211.7K  Lead
    210.7K  Hexane
    189.2K  Ethylbenzene
    183.7K  Acetaldehyde
    182.7K  Fluoranthene
    166.9K  Phenanthrene

POLLUTANT_NAME by dollars
   34621.24B    79.2K rows  Carbon dioxide
    5148.19B    20.6K rows  Carbon Dioxide
      67.92B   276.1K rows  Sulfur dioxide
      53.17B   305.1K rows  Nitrogen oxides
      30.17B   292.1K rows  Carbon monoxide
      10.96B    81.9K rows  Methane
      10.62B   381.5K rows  Volatile organic compounds
       7.04B   319.2K rows  Primary PM10 (filterables and condensibles)
       4.97B   318.6K rows  Primary PM2.5 (filterables and condensibles)
       4.61B   226.1K rows  Primary PM10, filterable portion only
       2.63B   225.3K rows  Primary PM2.5, filterable portion only
       2.26B    98.2K rows  Ammonia
       2.11B   224.8K rows  Primary PM condensible portion,  less than 1 micron
       1.53B   127.0K rows  Methanol
       1.07B    30.9K rows  Hydrochloric acid
     627.36M   210.7K rows  Hexane
     545.79M     6.2K rows  Sulfuric acid
     426.42M   125.1K rows  Styrene
     418.79M    63.8K rows  Remaining PMFINE portion of PM2.5-PRI
     342.27M   278.7K rows  Toluene

## what

REPORTING_YEAR: 2020 20%, 2017 19%, 2011 18%, 2014 17%, 2008 17%, 2015 1%, 2018 1%, 2016 1%, 2019 1%, 2022 1%, 2021 1%, 2023 1%

PGM_SYS_ACRNM: EIS 90%, TRIS 8%, E-GGRT 2%, CAMDBS 0%

UNIT_OF_MEASURE: Pounds 98%, MTCO2e 2%

NEI_TYPE: HAP 66%, CAP 30%, OTH 4%, GHG 0%, PFAS 0%

NEI_HAP_VOC_FLAG: VOC 66%, HAP-VOC 32%, EXEMPT-NONPHOTOCHEM 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| REPORTING_YEAR | category | 13 | 0 | 2020 2.09M; 2017 2.01M; 2011 1.89M; 2014 1.81M |
| REGISTRY_ID | other | 165.6K | 0 | 110041446753 14.2K; 110000424416 14.2K; 110071872465 14.2K; 110038080368 13.3K |
| PGM_SYS_ACRNM | category | 4 | 0 | EIS 9.38M; TRIS 798.6K; E-GGRT 196.1K; CAMDBS 34.0K |
| PGM_SYS_ID | other | 188.6K | 0 | 12142811 14.2K; 7147211 14.2K; 9442411 14.2K; 9581511 13.3K |
| POLLUTANT_NAME | who | 695 | 0 | Volatile organic compound 381.7K; Primary PM10 (filterables 319.3K; Primary PM2.5 (filterable 318.8K; Nitrogen oxides 305.2K |
| ANNUAL_EMISSION | amount | 4.27M | 572 | 0 531.6K; .01 31.3K; .000524054 19.5K; .00034937 19.3K |
| UNIT_OF_MEASURE | category | 2 | 0 | Pounds 10.22M; MTCO2e 196.1K |
| NEI_TYPE | category | 5 | 1.03M | HAP 6.21M; CAP 2.79M; OTH 331.7K; GHG 46.3K |
| NEI_HAP_VOC_FLAG | category | 4 | 4.58M | VOC 3.86M; HAP-VOC 1.89M; EXEMPT-NONPHOTOCHEM 78.0K |
| _INGESTED_AT | audit | 1 | 0 | 1786043749975236 10.41M |
| _SOURCE_RUN_ID | audit | 1 | 0 | a010fb6c-fe06-457c-98e2-3 10.41M |
| _SRC_SHA256 | other | 1 | 0 | d6ec1dbabae3ff473134f9031 10.41M |
