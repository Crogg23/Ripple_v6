# PORTAL_SOC_DELAWARE_OPEN_DA_D15606CF5C

rows 303  columns 10  scan 2.5s

roles: audit 2, category 4, date 1, other 2, who 2

## when

INGESTED_AT
  2026       303  ##############################

## who

SUBSECTOR by rows
         9  Merchant Wholesalers, Durable Goods
         9  Fabricated Metal Product Manufacturing
         9  Merchant Wholesalers, Nondurable Goods
         9  Food Manufacturing
         8  Administrative and Support Services
         7  Ambulatory Health Care Services
         7  Chemical Manufacturing
         7  Transportation Equipment Manufacturing
         7  Machinery Manufacturing
         6  Transit and Ground Passenger Transportation
         6  Support Activities for Transportation
         6  Animal Production
         6  Computer and Electronic Product Manufacturing
         5  Crop Production
         5  Primary Metal Manufacturing
         5  Performing Arts, Spectator Sports, and Related Industries
         5  Religious, Grantmaking, Civic, Professional, and Similar Organizations
         5  Nonmetallic Mineral Product Manufacturing
         4  Personal and Laundry Services
         4  Heavy and Civil Engineering Construction

SRC_SHA256 by rows
       303  596cbf6c83d2d3130a47442f0ad629d9300e60c9a3617fffbc068a11fa0d9d53

## who x when

SUBSECTOR by INGESTED_AT  LOAD STAMP, not an event date
  Administrative and Support Services       2026:8
  Ambulatory Health Care Services           2026:7
  Animal Production                         2026:6
  Chemical Manufacturing                    2026:7
  Computer and Electronic Product Manufact  2026:6
  Crop Production                           2026:5
  Fabricated Metal Product Manufacturing    2026:9
  Food Manufacturing                        2026:9
  Heavy and Civil Engineering Construction  2026:4
  Machinery Manufacturing                   2026:7
  Merchant Wholesalers, Durable Goods       2026:9
  Merchant Wholesalers, Nondurable Goods    2026:9
  Nonmetallic Mineral Product Manufacturin  2026:5
  Performing Arts, Spectator Sports, and R  2026:5
  Personal and Laundry Services             2026:4
  Primary Metal Manufacturing               2026:5
  Religious, Grantmaking, Civic, Professio  2026:5
  Support Activities for Transportation     2026:6
  Transit and Ground Passenger Transportat  2026:6
  Transportation Equipment Manufacturing    2026:7

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  596cbf6c83d2d3130a47442f0ad629d9300e60c9  2026:303

## what

INDUSTRY: Manufacturing 28%, Trade, Transportation, and Uti 25%, Education and Health Services 8%, Professional and Business Serv 7%, Financial Activities 6%, Natural Resources and Mining 6%, Leisure and Hospitality 5%, Other Services (except Public  5%, Information 4%, Construction 3%, Mining, Quarrying, and Oil and 2%, Utilities 1%

SECTOR: Manufacturing 33%, Transportation and Warehousing 11%, Retail Trade 10%, Wholesale Trade 7%, Agriculture, Forestry, Fishing 7%, Health Care and Social Assista 7%, Other Services (except Public  5%, Administration and Support and 4%, Finance and Insurance 4%, Information 4%, Construction 4%, Arts, Entertainment, and Recre 3%

BUSINESS_TO_REMAIN_OPEN: true 79%, false 21%

NOTES: null 86%, Permitted to work from home on 3%, Permitted to provide curbside  3%, Only personnel necessary to su 2%, Allowed to sell at showrooms b 2%, Permitted only to admit essent 1%, Permitted to work from home 1%, Permitted to work from home an 1%, Permitted to remain open but m 0%, With the exception of 812910 a 0%, Permitted to provide services  0%, Takeout and delivery only. 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY | category | 12 | 0 | Manufacturing 86; Trade, Transportation, an 75; Education and Health Serv 25; Professional and Business 21 |
| SECTOR | category | 19 | 0 | Manufacturing 86; Transportation and Wareho 29; Retail Trade 27; Wholesale Trade 19 |
| SUBSECTOR | who | 107 | 0 | Merchant Wholesalers, Non 9; Merchant Wholesalers, Dur 9; Fabricated Metal Product  9; Food Manufacturing 9 |
| INDUSTRY_GROUP | other | 266 | 0 | null 37; Business, Professional, L 2; Civic and Social Organiza 2; Social Advocacy Organizat 2 |
| C_4_DIGIT_NAICS | other | 304 | 0 | 8141 2; 8139 2; 8134 2; 8133 2 |
| BUSINESS_TO_REMAIN_OPEN | category | 2 | 0 | true 239; false 64 |
| NOTES | category | 18 | 0 | null 256; Permitted to work from ho 9; Permitted to provide curb 9; Only personnel necessary  7 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:42:40.30114 303 |
| SOURCE_RUN_ID | audit | 1 | 0 | 037c35ae-b6d6-4251-84b7-0 303 |
| SRC_SHA256 | who | 1 | 0 | 596cbf6c83d2d3130a47442f0 303 |
