# PORTAL_CKA_SAN_JOSE_OPEN_DA_00B8041D47

rows 10.0K  columns 13  scan 3.2s

roles: amount 2, audit 2, category 5, date 3, id 1, who 1

## when

DATE_CREATED
  2017     10.0K  ##############################

DATE_LAST_UPDATED
  2017      7.7K  ##############################
  2018        61  
  2019       524  ##
  2020        35  
  2021      1.6K  ######
  2023         1  
  2024         1  

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 10.0K | 0 | 37.30 | 37.41 | 54.19 | 283.0K |
| LONGITUDE | 10.0K | -122.25 | -121.84 | 0 | 0 | -923.7K |

## who

SRC_SHA256 by rows
     10.0K  2f8845fb9e95711bb4e08b2f89fe8dfc2f9cc806f029fc61d93509f95ac49776

SRC_SHA256 by dollars
      283.0K    10.0K rows  2f8845fb9e95711bb4e08b2f89fe8dfc2f9cc806f029fc61d93509f95ac4

## who x when

SRC_SHA256 by DATE_LAST_UPDATED, dollars = LATITUDE
  2f8845fb9e95711bb4e08b2f89fe8dfc2f9cc806  2017:199.1K 2018:2.2K 2019:19.5K 2020:1.2K 2021:60.9K 2023:37.34 2024:37.37

## what

STATUS: Closed 100%, In Progress 0%, Open 0%

SOURCE: Public API 54%, CX Console 35%, End-User pages 7%, Web Console 4%, End-User Pages 0%, SFDC-DOT 0%

CATEGORY: Other 42%, Utility 20%, City 11%, Water 9%, Painted Wall 5%, Light Pole 4%, Utility Box 3%, Payment 2%, No Value 2%, Wood Fence 1%, Sidewalk 1%

SERVICE_TYPE: Graffiti 39%, Other Issues 33%, Illegal Dumping 11%, Abandoned Vehicle 9%, Streetlight Outage 4%, Pothole 2%

DEPARTMENT: Parks and Recreation 41%, ESD 35%, DOT 18%, Finance 2%, External 1%, Planning Building 1%, Code Enforcement 1%, Housing 0%, Human Resources 0%, Police 0%, Public Works 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INCIDENT_ID | id | 10.1K | 0 | 20720 50; 20719 50; 20718 50; 20717 50 |
| STATUS | category | 3 | 0 | Closed 10.0K; In Progress 23; Open 14 |
| SOURCE | category | 6 | 0 | Public API 5.4K; CX Console 3.5K; End-User pages 734; Web Console 361 |
| CATEGORY | category | 18 | 2.7K | Other 3.0K; Utility 1.5K; City 787; Water 677 |
| SERVICE_TYPE | category | 7 | 6 | Graffiti 3.9K; Other Issues 3.3K; Illegal Dumping 1.1K; Abandoned Vehicle 920 |
| LATITUDE | amount | 7.1K | 0 | 0 2.4K; 37.3176466 42; 37.2743545 42; 37.37178 39 |
| LONGITUDE | amount | 7.3K | 0 | 0 2.4K; -121.8456362 42; -121.9034899 42; -121.867857 39 |
| DATE_CREATED | date | 8.0K | 0 | 7/17/2017 4:04:00 PM 119; 7/18/2017 5:01:00 PM 113; 7/18/2017 5:00:00 PM 108; 7/17/2017 4:27:00 PM 84 |
| DATE_LAST_UPDATED | date | 4.5K | 0 | 3/24/2021 1:30:01 AM 1.6K; 7/18/2017 5:01:00 PM 102; 7/17/2017 4:04:00 PM 96; 7/18/2017 5:00:00 PM 92 |
| DEPARTMENT | category | 27 | 180 | Parks and Recreation 4.0K; ESD 3.4K; DOT 1.8K; Finance 149 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:03:50.69289 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | cb9c507d-48ab-41d9-aa15-6 10.0K |
| SRC_SHA256 | who | 1 | 0 | 2f8845fb9e95711bb4e08b2f8 10.0K |
