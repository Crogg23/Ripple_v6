# PORTAL_CKA_SAN_JOSE_OPEN_DA_E55BABFE84

rows 31  columns 17  scan 2.6s

roles: amount 1, audit 2, category 13, date 1, who 1

## when

INGESTED_AT
  2026        31  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 31 | 3.9K | 23.5K | 52.4K | 53.2K | 792.8K |

## who

SRC_SHA256 by rows
        31  c52b192a137e1675bd8436d1f62e93eac749e4a08c8cbd6a2dd8113b079851fb

SRC_SHA256 by dollars
      792.8K       31 rows  c52b192a137e1675bd8436d1f62e93eac749e4a08c8cbd6a2dd8113b0798

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  c52b192a137e1675bd8436d1f62e93eac749e4a0  2026:792.8K

## what

OBJECTID: 39 8%, 38 8%, 37 8%, 36 8%, 35 8%, 34 8%, 33 8%, 32 8%, 31 8%, 30 8%, 29 8%, 28 8%

FACILITYID: 40 8%, 39 8%, 38 8%, 37 8%, 36 8%, 35 8%, 34 8%, 33 8%, 32 8%, 31 8%, 30 8%, 29 8%

INTID: 40 8%, 39 8%, 38 8%, 37 8%, 36 8%, 35 8%, 34 8%, 33 8%, 32 8%, 31 8%, 30 8%, 29 8%

PROJECTLIMITS: Monterey Rd to Ruby Ave 8%, Penitencia Creek Rd to Aborn R 8%, Meadowbrook Dr to Route 101/Co 8%, Sally Dr/City Limit to Montere 8%, Alma Ave to Harry Rd/City Limi 8%, E Willliam St/William Ct to Tu 8%, Senter Rd to Fleming Ave 8%, Liberty St to Alma Ave 8%, Tully Rd to Rural Access 8%, Trimble Rd/City Limit to Alum  8%, Hillsdale Ave to end of Snell  8%, Hwy 85 to Bayliss Dr 8%

SAFETYPRIORITYSTREET: Tully Rd 8%, White Rd 8%, Blossom Hill Rd 8%, Branham Ln 8%, Almaden Exp 8%, McLaughlin Ave 8%, Story Rd 8%, First St 8%, Quimby Rd 8%, Capitol Ave 8%, Snell Ave 8%, Santa Teresa Blvd 8%

GRANTFUNDING: Applied for STP 57%, HSIP 14%, TDA-3 14%, OBAG 14%

FUNDINGAGENCY: Caltrans 86%, State of California 14%

GRANTAMOUNT: Requesting $500,000 for planni 43%, Grant ($2,513,970) + 10% Match 14%, $300,000 (no match required) 14%, Requesting $500,000 for planni 14%, Grant ($1,500,000) + Local Mat 14%

VOLUME: 0 65%, 1 23%, 2 13%

JURISDICTION: San Jose 94%, County 6%

CREATIONDATE: 2023/05/03 01:58:45+00 9%, 2023/05/03 01:58:11+00 9%, 2023/05/03 01:57:28+00 9%, 2023/05/03 01:56:50+00 9%, 2023/05/03 01:56:27+00 9%, 2023/05/03 01:55:35+00 9%, 2023/05/03 01:54:40+00 9%, 2023/05/03 01:52:29+00 9%, 2023/05/03 01:49:40+00 9%, 2023/05/03 01:49:25+00 9%, 2023/05/03 01:48:57+00 9%

LASTUPDATE: 2023/05/06 01:34:53+00 87%, 2023/05/03 01:56:27+00 3%, 2023/10/18 02:06:12+00 3%, 2023/10/18 02:07:32+00 3%, 2020/02/07 00:00:00+00 3%

NOTES: New PSC in 2023 46%, Added to Priority Safety Corri 14%, Evaluate safety issues and det 7%, Before 2023, Tully PSC was fro 4%, Before 2023, White PSC was fro 4%, Before 2023, Branham PSC was f 4%, Coordinate with County to eval 4%, Before 2023, McLaughlin PSC wa 4%, Before 2023, Story PSC was fro 4%, Added to Priority Safety Corri 4%, A traffic signal modification  4%, Buffered bike lanes were insta 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 31 | 0 | 39 1; 38 1; 37 1; 36 1 |
| FACILITYID | category | 31 | 0 | 40 1; 39 1; 38 1; 37 1 |
| INTID | category | 31 | 0 | 40 1; 39 1; 38 1; 37 1 |
| PROJECTLIMITS | category | 31 | 0 | Monterey Rd to Ruby Ave 1; Penitencia Creek Rd to Ab 1; Meadowbrook Dr to Route 1 1; Sally Dr/City Limit to Mo 1 |
| SAFETYPRIORITYSTREET | category | 31 | 0 | Tully Rd 1; White Rd 1; Blossom Hill Rd 1; Branham Ln 1 |
| GRANTFUNDING | category | 5 | 24 | Applied for STP 4; HSIP 1; TDA-3 1; OBAG 1 |
| FUNDINGAGENCY | category | 3 | 24 | Caltrans 6; State of California 1 |
| GRANTAMOUNT | category | 6 | 24 | Requesting $500,000 for p 3; Grant ($2,513,970) + 10%  1; $300,000 (no match requir 1; Requesting $500,000 for p 1 |
| VOLUME | category | 3 | 0 | 0 20; 1 7; 2 4 |
| JURISDICTION | category | 2 | 0 | San Jose 29; County 2 |
| CREATIONDATE | category | 21 | 11 | 2023/05/03 01:58:45+00 1; 2023/05/03 01:58:11+00 1; 2023/05/03 01:57:28+00 1; 2023/05/03 01:56:50+00 1 |
| LASTUPDATE | category | 5 | 0 | 2023/05/06 01:34:53+00 27; 2023/05/03 01:56:27+00 1; 2023/10/18 02:06:12+00 1; 2023/10/18 02:07:32+00 1 |
| NOTES | category | 15 | 0 | New PSC in 2023 13; Added to Priority Safety  4; Evaluate safety issues an 2; Before 2023, Tully PSC wa 1 |
| SHAPE_LENGTH | amount | 31 | 0 | 26519.9574470475 1; 32363.1816343203 1; 41223.2242679713 1; 29316.0679496279 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:19:24.44365 31 |
| SOURCE_RUN_ID | audit | 1 | 0 | e5b7173f-6caa-4936-a5f0-b 31 |
| SRC_SHA256 | who | 1 | 0 | c52b192a137e1675bd8436d1f 31 |
