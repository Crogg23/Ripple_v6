# PORTAL_CKA_SAN_JOSE_OPEN_DA_5B443A0101

rows 18  columns 17  scan 2.8s

roles: amount 3, audit 2, category 10, date 1, empty 1, who 1

## when

INGESTED_AT
  2026        18  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCHOOLDISTAREA | 18 | 0.27 | 17.54 | 256.91 | 287.31 | 742.60 |
| SHAPE_LENGTH | 18 | 19.8K | 136.5K | 509.6K | 539.6K | 3.32M |
| SHAPE_AREA | 18 | 7.46M | 488.70M | 7.16B | 8.01B | 20.70B |

## who

SRC_SHA256 by rows
        18  363a4be55e5fe46fa51d4baff93c6af1eab5d4e8820cea84e6f3e0b6ab8d7dc7

SRC_SHA256 by dollars
      742.60       18 rows  363a4be55e5fe46fa51d4baff93c6af1eab5d4e8820cea84e6f3e0b6ab8d

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCHOOLDISTAREA
  363a4be55e5fe46fa51d4baff93c6af1eab5d4e8  2026:742.60

## what

OBJECTID: 162 8%, 161 8%, 160 8%, 159 8%, 158 8%, 157 8%, 156 8%, 155 8%, 154 8%, 153 8%, 152 8%, 151 8%

FACILITYID: 127 8%, 110 8%, 105 8%, 100 8%, 96 8%, 60 8%, 84 8%, 79 8%, 75 8%, 63 8%, 69 8%, 61 8%

INTID: 127 8%, 110 8%, 105 8%, 100 8%, 96 8%, 60 8%, 84 8%, 79 8%, 75 8%, 63 8%, 69 8%, 61 8%

SCHOOLDISTRICTID: 22 8%, 19 8%, 18 8%, 17 8%, 15 8%, 12 8%, 11 8%, 9 8%, 8 8%, 4 8%, 6 8%, 3 8%

SCHOOLDISTRICTNAME: Union Elementary School Distri 8%, Orchard Elementary School Dist 8%, Oak Grove Elementary School Di 8%, Mount Pleasant Elementary Scho 8%, Moreland Elementary School Dis 8%, Luther Burbank Elementary Scho 8%, Los Gatos Union Elementary Sch 8%, Franklin-McKinley Elementary S 8%, Evergreen Elementary School Di 8%, Campbell Union Elementary Scho 8%, Cupertino Union Elementary Sch 8%, Cambrian Elementary School Dis 8%

DISTRICTTYPE: Elementary 78%, Unified 22%

AGENCYURL: www.unionsd.org 8%, www.orchardsd.org 8%, www.ogsd.net 8%, www.mpesd.org 8%, www.moreland.org 8%, www.lbsd.k12.ca.us 8%, www.lgusd.org 8%, www.fmsd.org 8%, www.eesd.org 8%, www.campbellusd.org 8%, www.cusdk8.org 8%, www.cambriansd.org 8%

PHONE: 408-377-8010 8%, 408-944-0397 8%, 408-227-8300 8%, 408-223-3710 8%, 408-874-2901 8%, 408-295-2450 8%, 408-335-2000 8%, 408-283-6006 8%, 408-270-6800 8%, 408-364-4200 8%, 408-252-3000 8%, 408-377-2103 8%

EMAIL: martinezp@unionsd.org 8%, wgudalewicz@orchardsd.org 8%, jmanzo@oakgrovesd.net 8%, emacarthur@mpesd.org 8%, mkgoing@moreland.org 8%, emourtos@lbsdk8.org 8%, pjohnson@lgusd.org 8%, otilia.enriquez@fmsd.org 8%, ashaffer@eesd.org 8%, contact@campbellusd.org 8%, smith_renee@cusdk8.org 8%, grandeyc@cambriansd.com 8%

LASTUPDATE: 2024/12/26 18:06:00+00 19%, 2022/05/04 17:50:05+00 12%, 2024/12/26 18:10:42+00 12%, 2024/12/30 23:23:29+00 6%, 2024/12/26 18:19:16+00 6%, 2025/01/02 19:56:36+00 6%, 2024/12/30 23:28:25+00 6%, 2024/12/30 22:59:00+00 6%, 2024/12/26 18:21:31+00 6%, 2024/12/20 18:54:01+00 6%, 2022/05/04 17:50:04+00 6%, 2024/12/30 23:32:16+00 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 18 | 0 | 162 1; 161 1; 160 1; 159 1 |
| FACILITYID | category | 18 | 0 | 127 1; 110 1; 105 1; 100 1 |
| INTID | category | 18 | 0 | 127 1; 110 1; 105 1; 100 1 |
| SCHOOLDISTRICTID | category | 18 | 0 | 22 1; 19 1; 18 1; 17 1 |
| SCHOOLDISTRICTNAME | category | 18 | 0 | Union Elementary School D 1; Orchard Elementary School 1; Oak Grove Elementary Scho 1; Mount Pleasant Elementary 1 |
| DISTRICTTYPE | category | 2 | 0 | Elementary 14; Unified 4 |
| SCHOOLDISTAREA | amount | 18 | 0 | 7.39 1; 5.83 1; 21.34 1; 6.11 1 |
| AGENCYURL | category | 18 | 0 | www.unionsd.org 1; www.orchardsd.org 1; www.ogsd.net 1; www.mpesd.org 1 |
| PHONE | category | 18 | 0 | 408-377-8010 1; 408-944-0397 1; 408-227-8300 1; 408-223-3710 1 |
| EMAIL | category | 18 | 0 | martinezp@unionsd.org 1; wgudalewicz@orchardsd.org 1; jmanzo@oakgrovesd.net 1; emacarthur@mpesd.org 1 |
| LASTUPDATE | category | 14 | 0 | 2024/12/26 18:06:00+00 3; 2022/05/04 17:50:05+00 2; 2024/12/26 18:10:42+00 2; 2024/12/30 23:23:29+00 1 |
| NOTES | empty | 1 | 18 |  |
| SHAPE_LENGTH | amount | 18 | 0 | 74206.0713958697 1; 97356.9073011311 1; 142048.109269163 1; 62547.0564989853 1 |
| SHAPE_AREA | amount | 18 | 0 | 206043864.876715 1; 164487113.868264 1; 594877835.045154 1; 170395297.159211 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:15:57.32720 18 |
| SOURCE_RUN_ID | audit | 1 | 0 | 170e7fcb-ab6a-423a-944b-b 18 |
| SRC_SHA256 | who | 1 | 0 | 363a4be55e5fe46fa51d4baff 18 |
