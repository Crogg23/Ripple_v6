# PORTAL_SOC_UTAH_OPEN_DATA_P_2853122765

rows 5.0K  columns 23  scan 3.6s

roles: amount 17, audit 2, category 2, date 1, other 1, who 1

## when

INGESTED_AT
  2026      5.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CY1998 | 5.0K | -690.0K | 15.0K | 50.45M | 326.66M | 11.21B |
| CY1999 | 5.0K | -49.82M | 20.0K | 49.08M | 332.09M | 11.50B |
| CY2000 | 5.0K | -9.30M | 20.0K | 52.64M | 342.76M | 12.30B |
| CY2001 | 5.0K | -12.02M | 20.0K | 52.48M | 601.22M | 12.89B |
| CY2002 | 5.0K | -4.18M | 20.0K | 55.05M | 498.85M | 12.92B |
| CY2003 | 5.0K | -4.81M | 25.0K | 53.30M | 445.42M | 13.10B |

## who

SRC_SHA256 by rows
      5.0K  90925b7508701a3989c0860a3df9074944f2dbcfff87b73cbddae9cca1067274

SRC_SHA256 by dollars
      12.92B     5.0K rows  90925b7508701a3989c0860a3df9074944f2dbcfff87b73cbddae9cca106

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = CY2002
  90925b7508701a3989c0860a3df9074944f2dbcf  2026:12.92B

## what

COUNTY: Salt Lake 14%, Utah 14%, Weber 10%, Cache 10%, Washington 8%, Sanpete 7%, Box Elder 7%, Emery 6%, Davis 6%, Millard 6%, Iron 6%, Summit 5%

NAICS_MAJOR_SECTOR: PRIOR-PERIOD PAYMENTS & REFUND 11%, INFORMATION(510000-519999) 10%, MANUFACTURING(310000-339999) 9%, RETAIL-MISCELLANEOUS RETAIL TR 9%, OTHER SERVICES-EXECPT PUBLIC A 9%, FOOD SERVICES & DRINKING PLACE 8%, NONSTORE RETAILERS(454000-4549 8%, RETAIL-FOOD & BEVERAGE STORES( 8%, RETAIL-ELECTRONICS & APPLIANCE 8%, CONSTRUCTION(230000-239999) 7%, PROFESSIONAL, SCIENTIFIC, & TE 7%, RETAIL-GASOLINE STATIONS(44700 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ESTIMATED_POPULATION | other | 172 | 386 | 83793 129; 90749 122; 34017 81; 17791 74 |
| COUNTY | category | 34 | 1 | Salt Lake 475; Utah 448; Weber 332; Cache 316 |
| NAICS_MAJOR_SECTOR | category | 37 | 0 | PRIOR-PERIOD PAYMENTS & R 240; INFORMATION(510000-519999 209; MANUFACTURING(310000-3399 201; RETAIL-MISCELLANEOUS RETA 198 |
| CY1998 | amount | 926 | 0 |  .  1.7K; 1,000 238; 150,000 154; 200,000 106 |
| CY1999 | amount | 931 | 0 |  .  1.7K; 1,000 225; 150,000 142; 2,000 115 |
| CY2000 | amount | 963 | 0 |  .  1.7K; 1,000 233; 150,000 140; 200,000 108 |
| CY2001 | amount | 984 | 0 |  .  1.7K; 1,000 192; 150,000 144; 2,000 117 |
| CY2002 | amount | 968 | 0 |  .  1.7K; 1,000 188; 150,000 149; 15,000 112 |
| CY2003 | amount | 1.0K | 0 |  .  1.6K; 1,000 201; 150,000 150; 2,000 111 |
| CY2004 | amount | 1.1K | 0 |  .  1.5K; 1,000 247; 150,000 139; 2,000 110 |
| CY2005 | amount | 1.1K | 0 |  .  1.5K; 1,000 224; 150,000 127; 2,000 126 |
| CY2006 | amount | 1.1K | 0 |  .  1.6K; 1,000 193; 150,000 135; 200,000 109 |
| CY2007 | amount | 1.1K | 0 |  .  1.5K; 1,000 201; 150,000 139; 2,000 108 |
| CY2008 | amount | 1.1K | 0 |  .  1.5K; 1,000 224; 150,000 128; 2,000 104 |
| CY2009 | amount | 1.1K | 0 |  .  1.5K; 1,000 215; 150,000 126; 15,000 124 |
| CY2010 | amount | 1.2K | 0 |  .  1.5K; 1,000 199; 15,000 121; 150,000 115 |
| CY2011 | amount | 1.1K | 0 |  .  1.5K; 1,000 184; 150,000 141; 15,000 108 |
| CY2012 | amount | 1.1K | 0 |  .  1.5K; 1,000 186; 150,000 133; 200,000 121 |
| CY2013 | amount | 1.1K | 0 |  .  1.5K; 1,000 186; 150,000 131; 15,000 114 |
| CY2014 | amount | 1.1K | 0 |  .  1.6K; 1,000 174; 150,000 126; 200,000 110 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:44:52.19612 5.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 4493851f-139a-45b5-a179-e 5.0K |
| SRC_SHA256 | who | 1 | 0 | 90925b7508701a3989c0860a3 5.0K |
