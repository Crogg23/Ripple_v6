# PORTAL_CKA_TAMPA_OPEN_DATA_485B900D71

rows 604  columns 13  scan 3.4s

roles: amount 1, audit 2, category 7, date 2, other 1, who 1

## when

DATE
  2015         1  
  2016         1  
  2017         1  
  2018         1  
  2019         1  
  2020         1  
  2021        48  ###########
  2022        66  ###############
  2023       121  ###########################
  2024        96  #####################
  2025       136  ##############################
  2026       131  #############################

INGESTED_AT
  2026       604  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 604 | 0 | 99.87 | 761.6K | 813.0K | 8.94M |

## who

SRC_SHA256 by rows
       604  648d36f9c39f65ba688ea21de80922ff6c105a3a441d14d2b736cf3ffd763e5b

SRC_SHA256 by dollars
       8.94M      604 rows  648d36f9c39f65ba688ea21de80922ff6c105a3a441d14d2b736cf3ffd76

## who x when

SRC_SHA256 by DATE, dollars = VALUE
  648d36f9c39f65ba688ea21de80922ff6c105a3a  2015:720.0K 2016:740.0K 2017:745.0K 2018:760.0K 2019:784.5K 2020:761.7K 2021:919.5K 2022:798.7K 2023:830.2K 2024:896.8K 2025:921.6K 2026:57.9K

## what

C_ORGANIZATION: Technology & Innovation 85%, Logistics & Asset Management ( 9%, Neighborhood Empowerment 2%, Development & Growth Mgmt 2%, City of Tampa 1%, Planning & Development (Develo 1%

CHARTNAME: Major System Uptime 37%, Technology and Innovation Serv 24%, Percent of Vehicles Available  9%, Technology and Innovation Proj 9%, Technology and Innovation Tick 8%, Major System Uptime - OLD 4%, Budget Book Estimates 4%, Mayor's Strategic Initiatives  2%, Mayor's Strategic Initiatives  2%, Mayor's Strategic Initiatives  1%, Mayor's Strategic Initiatives  0%, Mayor's Strategic Initiatives  0%

DESCRIPTION: Major System Uptime 54%, FootPrints 11%, FootPrints Projects 11%, FootPrints Tickets 11%, Workforce Development; T3 Init 6%, Development and Growth Mgmt; H 5%, T3 Initiative 2%

CATEGORY: Percent of Vehicles 14%, TPDNET 12%, TampaGOV 12%, Percentage of Calls Answered w 11%, Percentage of Tickets Complete 11%, Calls to the T&I Service Desk 11%, SIRE Council Agendas 9%, Percentage of Calls Answered 7%, Overdue Projects by Month 4%, Oracle Fusion 3%, Tickets Overdue by Month 3%, Projects Closed by Month 3%

SUMMARY: Percent 67%, Total 33%

TYPEDATA: Date 92%, Period 8%

PERIOD: 7/2026 9%, 6/2026 9%, 5/2026 9%, 4/2026 9%, 3/2026 9%, 2/2026 9%, 1/2026 9%, 12/2025 9%, 11/2025 9%, 10/2025 9%, 9/2025 9%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 604 | 0 | 162683 4; 162682 4; 162681 4; 162680 4 |
| C_ORGANIZATION | category | 6 | 0 | Technology & Innovation 516; Logistics & Asset Managem 53; Neighborhood Empowerment 14; Development & Growth Mgmt 11 |
| CHARTNAME | category | 12 | 0 | Major System Uptime 221; Technology and Innovation 147; Percent of Vehicles Avail 53; Technology and Innovation 52 |
| DESCRIPTION | category | 8 | 381 | Major System Uptime 121; FootPrints 25; FootPrints Projects 24; FootPrints Tickets 24 |
| CATEGORY | category | 37 | 0 | Percent of Vehicles 53; TPDNET 45; TampaGOV 45; Percentage of Calls Answe 41 |
| SUMMARY | category | 2 | 0 | Percent 406; Total 198 |
| TYPEDATA | category | 2 | 0 | Date 557; Period 47 |
| DATE | date | 153 | 0 | 10/01/2025 00:00:00 19; 09/01/2025 00:00:00 19; 08/01/2025 00:00:00 19; 06/01/2026 00:00:00 18 |
| PERIOD | category | 36 | 395 | 7/2026 14; 6/2026 14; 5/2026 14; 4/2026 14 |
| VALUE | amount | 355 | 0 | 100.000 126; 99.990 16; 0.000 11; 33.000 10 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:22:18.89763 604 |
| SOURCE_RUN_ID | audit | 1 | 0 | e67c819b-d8f1-4f06-8fb2-1 604 |
| SRC_SHA256 | who | 1 | 0 | 648d36f9c39f65ba688ea21de 604 |
