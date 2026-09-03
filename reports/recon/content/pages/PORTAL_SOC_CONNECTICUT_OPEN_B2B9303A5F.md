# PORTAL_SOC_CONNECTICUT_OPEN_B2B9303A5F

rows 274  columns 10  scan 3.4s

roles: amount 2, audit 2, date 1, other 4, who 2

## when

INGESTED_AT
  2026       274  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SBE_SPENDING_ALLOCATION_GOAL | 274 | 0 | 0.04 | 0.32 | 0.32 | 14.35 |
| MBE_SPENDING_ALLOCATION_GOAL | 274 | 0 | 0.02 | 0.17 | 0.17 | 8.61 |

## who

NAICS_INDUSTRY_CATEGORY by rows
        37  Professional, Scientific, and Technical Services
        22  Gasoline Stations and Fuel Dealers
        19  Administrative and Support Services
        18  Repair and Maintenance
        17  Merchant Wholesalers, Durable Goods
        15  Rental and Leasing Services
        13  Computing Infrastructure Providers, Data Processing, Web Hosting, and 
         9  Utilities
         8  Sporting Goods, Hobby, Musical Instrument, Book, and Miscellaneous Ret
         6  Heavy and Civil Engineering Construction
         6  Telecommunications
         6  Ambulatory Health Care Services
         6  Insurance Carriers and Related Activities
         6  Real Estate
         5  Construction of Buildings
         5  Printing and Related Support Activities
         5  Specialty Trade Contractors
         5  Truck Transportation
         4  Waste Management and Remediation Services
         4  Miscellaneous Manufacturing

NAICS_INDUSTRY_CATEGORY by dollars
        2.59       37 rows  Professional, Scientific, and Technical Services
        1.60        5 rows  Printing and Related Support Activities
        1.53       17 rows  Merchant Wholesalers, Durable Goods
        1.20        6 rows  Heavy and Civil Engineering Construction
        1.15        5 rows  Truck Transportation
        1.05       15 rows  Rental and Leasing Services
        0.95       19 rows  Administrative and Support Services
        0.72       18 rows  Repair and Maintenance
        0.39       13 rows  Computing Infrastructure Providers, Data Processing, Web Hos
        0.36        4 rows  Waste Management and Remediation Services
        0.36        6 rows  Telecommunications
        0.35        5 rows  Specialty Trade Contractors
        0.30        2 rows  Mining (except Oil and Gas)
        0.24        3 rows  Building Material and Garden Equipment and Supplies Dealers
        0.16        4 rows  Miscellaneous Manufacturing
        0.16        8 rows  Sporting Goods, Hobby, Musical Instrument, Book, and Miscell
        0.10        2 rows  Couriers and Messengers
        0.10        5 rows  Construction of Buildings
        0.09        9 rows  Utilities
        0.09        3 rows  Transportation Equipment Manufacturing

SRC_SHA256 by rows
       274  7a692c4d3c40c6831f24d52fcf2bbe3509c6d161df10235a74df7d915aaeaecd

SRC_SHA256 by dollars
       14.35      274 rows  7a692c4d3c40c6831f24d52fcf2bbe3509c6d161df10235a74df7d915aae

## who x when

NAICS_INDUSTRY_CATEGORY by INGESTED_AT  LOAD STAMP, not an event date, dollars = SBE_SPENDING_ALLOCATION_GOAL
  Administrative and Support Services       2026:0.95
  Ambulatory Health Care Services           2026:0.06
  Building Material and Garden Equipment a  2026:0.24
  Computing Infrastructure Providers, Data  2026:0.39
  Construction of Buildings                 2026:0.10
  Couriers and Messengers                   2026:0.10
  Gasoline Stations and Fuel Dealers        2026:0
  Heavy and Civil Engineering Construction  2026:1.20
  Insurance Carriers and Related Activitie  2026:0.06
  Merchant Wholesalers, Durable Goods       2026:1.53
  Mining (except Oil and Gas)               2026:0.30
  Miscellaneous Manufacturing               2026:0.16
  Printing and Related Support Activities   2026:1.60
  Professional, Scientific, and Technical   2026:2.59
  Real Estate                               2026:0.06
  Rental and Leasing Services               2026:1.05
  Repair and Maintenance                    2026:0.72
  Specialty Trade Contractors               2026:0.35
  Sporting Goods, Hobby, Musical Instrumen  2026:0.16
  Telecommunications                        2026:0.36
  Transportation Equipment Manufacturing    2026:0.09
  Truck Transportation                      2026:1.15
  Utilities                                 2026:0.09
  Waste Management and Remediation Service  2026:0.36

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SBE_SPENDING_ALLOCATION_GOAL
  7a692c4d3c40c6831f24d52fcf2bbe3509c6d161  2026:14.35

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FISCAL_YEAR | other | 1 | 0 | 2027 274 |
| ACCOUNT_CODE | other | 273 | 0 | 56020 2; 56010 2; 55901 2; 55890 2 |
| ACCOUNT_CODE_DESCRIPTION | other | 275 | 0 | Rf-Direct Materials Used 2; Rf-Goods/Services-Resale/ 2; Capitalized SBITA 2; Other Structures 2 |
| THREE_DIGIT_NAICS_CODE | other | 52 | 0 | 541 37; 457 22; 561 19; 811 18 |
| NAICS_INDUSTRY_CATEGORY | who | 52 | 0 | Professional, Scientific, 37; Gasoline Stations and Fue 22; Administrative and Suppor 19; Repair and Maintenance 18 |
| SBE_SPENDING_ALLOCATION_GOAL | amount | 45 | 0 | 0.0712 37; 0.0025 22; 0.0529 19; 0.0411 18 |
| MBE_SPENDING_ALLOCATION_GOAL | amount | 42 | 0 | 0.0465 37; 0.0025 22; 0.0367 19; 0.019 18 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:47:51.17071 274 |
| SOURCE_RUN_ID | audit | 1 | 0 | 6377375c-2b95-4ab2-b712-5 274 |
| SRC_SHA256 | who | 1 | 0 | 7a692c4d3c40c6831f24d52fc 274 |
