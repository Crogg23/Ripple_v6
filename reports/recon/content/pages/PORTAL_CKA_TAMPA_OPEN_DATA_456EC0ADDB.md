# PORTAL_CKA_TAMPA_OPEN_DATA_456EC0ADDB

rows 829  columns 13  scan 4.3s

roles: amount 1, audit 2, category 2, date 2, other 2, who 5

## when

DATE
  2026       829  ##############################

INGESTED_AT
  2026       829  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 829 | 0 | 3 | 50.75M | 265.08M | 1.44B |

## who

C_ORGANIZATION by rows
       829  Economic Opportunity (Economic Opportunity Administrator)

C_ORGANIZATION by dollars
       1.44B      829 rows  Economic Opportunity (Economic Opportunity Administrator)

CATEGORY by rows
        24  Jobs Created/Retained
        24  Workshops
        15  Entrepreneur Training
        14  Number of Attendees
        14  Familiarization Tours
        14  Business Planning WS
        14  Production Expenditures
        14  Room Nights
        14  Business Plan in a Day
        14  Capital Investment
        14  Average Wages
        14  Media Placements
        14  Events
        14  Tampa Projects
        14  Production Permits
        14  Hillsborough County Projects
        14  Missions
        14  Marketing Toolbox
        11  Business Planning
        11  Financing Assistance

CATEGORY by dollars
     806.89M       10 rows  Capital Raised
     573.62M       14 rows  Capital Investment
      49.65M       14 rows  Production Expenditures
       8.73M        9 rows  Loans Received
       1.19M       14 rows  Average Wages
       18.0K       14 rows  Room Nights
        8.1K       10 rows  All Other Industry Jobs
        7.2K       10 rows  Film Jobs
        7.0K       24 rows  Jobs Created/Retained
        3.1K       10 rows  Consulting Hours
        2.8K       10 rows  Strategic Connections
        2.4K       10 rows  New Jobs
        2.1K       10 rows  Startup Applications
        1.6K       10 rows  Startup Counseling #
        1.2K       14 rows  Production Permits
        1.1K       14 rows  Number of Attendees
        1.0K       10 rows  Clients Consulted
        1.0K       11 rows  Clients
         732       14 rows  Media Placements
         564       24 rows  Workshops

TYPEDATA by rows
       829  Period

TYPEDATA by dollars
       1.44B      829 rows  Period

DESCRIPTION by rows
       829  Small Business Navigator

DESCRIPTION by dollars
       1.44B      829 rows  Small Business Navigator

## who x when

C_ORGANIZATION by DATE, dollars = VALUE
  Economic Opportunity (Economic Opportuni  2026:1.44B

CATEGORY by DATE, dollars = VALUE
  All Other Industry Jobs                   2026:8.1K
  Average Wages                             2026:1.19M
  Business Plan in a Day                    2026:7
  Business Planning                         2026:129
  Business Planning WS                      2026:7
  Capital Investment                        2026:573.62M
  Capital Raised                            2026:806.89M
  Clients Consulted                         2026:1.0K
  Consulting Hours                          2026:3.1K
  Entrepreneur Training                     2026:8
  Events                                    2026:65
  Familiarization Tours                     2026:5
  Film Jobs                                 2026:7.2K
  Financing Assistance                      2026:33
  Hillsborough County Projects              2026:22
  Jobs Created/Retained                     2026:7.0K
  Loans Received                            2026:8.73M
  Marketing Toolbox                         2026:145
  Media Placements                          2026:732
  Missions                                  2026:11
  New Jobs                                  2026:2.4K
  Number of Attendees                       2026:1.1K
  Production Expenditures                   2026:49.65M
  Production Permits                        2026:1.2K
  Room Nights                               2026:18.0K
  Startup Applications                      2026:2.1K
  Startup Counseling #                      2026:1.6K
  Strategic Connections                     2026:2.8K
  Tampa Projects                            2026:45
  Workshops                                 2026:564

## what

CHARTNAME: Economic Opportunity - Small B 32%, Economic Opportunity - Small B 17%, Economic Opportunity - Tampa B 12%, Economic Opportunity - Hillsbo 8%, Economic Opportunity - Tampa B 7%, Economic Opportunity - Small B 6%, Economic Opportunity - Prosper 5%, Economic Opportunity - Tampa B 4%, Economic Opportunity - Jobs Cr 3%, Economic Opportunity - Tampa B 2%, Economic Opportunity - Tampa B 2%, Economic Opportunity - Tampa B 2%

PERIOD: FY26-Q1 9%, FY24-Q4 9%, FY24-Q3 9%, FY24-Q1 9%, FY25-Q4 9%, FY25-Q1 9%, FY24-Q2 9%, FY25-Q3 9%, FY25-Q2 9%, FY23-Q4 7%, FY23-Q3 7%, FY26-Q2 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 799 | 0 | 21201 5; 21200 5; 21199 5; 21198 5 |
| C_ORGANIZATION | who | 1 | 0 | Economic Opportunity (Eco 829 |
| CHARTNAME | category | 24 | 0 | Economic Opportunity - Sm 220; Economic Opportunity - Sm 121; Economic Opportunity - Ta 80; Economic Opportunity - Hi 57 |
| DESCRIPTION | who | 1 | 0 | Small Business Navigator 829 |
| CATEGORY | who | 72 | 0 | Jobs Created/Retained 24; Workshops 24; Entrepreneur Training 15; Missions 14 |
| SUMMARY | other | 1 | 0 | Total 829 |
| TYPEDATA | who | 1 | 0 | Period 829 |
| DATE | date | 309 | 0 | 2026-04-15T00:00:00 39; 2026-05-20T00:00:00 28; 2026-04-17T00:00:00 26; 2026-05-11T00:00:00 12 |
| PERIOD | category | 22 | 0 | FY26-Q1 74; FY24-Q4 72; FY24-Q3 72; FY24-Q1 72 |
| VALUE | amount | 241 | 0 | 0.0 276; 1.0 85; 2.0 36; 4.0 30 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:23:30.03504 829 |
| SOURCE_RUN_ID | audit | 1 | 0 | 28b61dac-061a-4a7e-87c7-2 829 |
| SRC_SHA256 | who | 1 | 0 | aca5f25070b67dcc8cf170149 829 |
