# PORTAL_CKA_TAMPA_OPEN_DATA_6C25EA91D4

rows 443  columns 10  scan 3.8s

roles: amount 3, audit 2, category 1, date 1, other 2, who 2

## when

INGESTED_AT
  2026       443  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AMOUNT | 443 | 1 | 122 | 37.6K | 117.3K | 997.2K |
| PERCENTAMOUNT | 443 | 0.01 | 99.43 | 100 | 100 | 27.4K |
| AVERAGEAMOUNT | 443 | 0 | 3.76 | 112.28 | 272 | 4.9K |

## who

SERVICENAME by rows
         2  Historic Preservation Commission
         2  Building / Structural Violation Complaint
         2  Parks and Recreation
         2  Water Color Concern (Cloudy, Discolored, Dirty)
         2  Street Marking Request (Repair)
         2  Curbside Special Solid Waste Pick-up Request
         2  Sewer Odor Complaint
         2  Foreclosed Property Registration Application
         2  Compactor Repair Request
         2  Transportation Executive - Operations Tasks (Dep't Use ONLY)
         2  Address Not Posted / Not Visible
         2  Picnic Shelter Requests
         2  Residential Service was Missed (Garbage, Recycling, Yard Waste, SWEEP)
         2  Solid Waste/EPM Personnel/Crew Compliment or Comments
         2  Request a Grant Letter of Support
         2  Code Enforcement General Inquiries
         2  Tree Removal Information
         2  Mayor Jane Castor's Office
         2  Mobile App Enhancement Request
         2  Construction Services - General Inquiries

SERVICENAME by dollars
      117.9K        2 rows  Utility Service Start Request
       79.2K        2 rows  Utility Bill Questions
       57.2K        2 rows  Utility Service Stop Request
       47.6K        2 rows  Code Enforcement General Inquiries
       41.6K        2 rows  Utility Information Service Request (internal Water Dep't Us
       32.2K        2 rows  Solid Waste General Correspondence
       31.4K        2 rows  Utility Service High Utility Bill Inquiry
       30.3K        2 rows  Mayor Jane Castor's Office
       25.9K        2 rows  Police
       24.0K        2 rows  Foreclosed Property Registration Application
       23.2K        2 rows  Residential Service was Missed (Garbage, Recycling, Yard Was
       22.3K        2 rows  Accumulated Junk, Trash or Debris on Private Property
       19.5K        2 rows  New Business Tax Receipt Application
       17.3K        2 rows  Pothole Repair ONLY (non Cave-In/Sinking Area Repair)
       15.7K        2 rows  Garbage (blue) or Recycling (green) Cart Request
       15.3K        2 rows  Water
       15.2K        2 rows  Police Personnel Bureau
       13.7K        2 rows  Overgrown Lot or Yard Complaint
       13.4K        2 rows  Picnic Shelter Requests
       11.7K        2 rows  Parks and Recreation

SRC_SHA256 by rows
       443  55da4550ea3a11a4b12a07d016412a309857b9bdca0507ed625d802a34fcccda

SRC_SHA256 by dollars
      997.2K      443 rows  55da4550ea3a11a4b12a07d016412a309857b9bdca0507ed625d802a34fc

## who x when

SERVICENAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = AMOUNT
  Accumulated Junk, Trash or Debris on Pri  2026:22.3K
  Address Not Posted / Not Visible          2026:195
  Building / Structural Violation Complain  2026:10.0K
  Code Enforcement General Inquiries        2026:47.6K
  Compactor Repair Request                  2026:341
  Construction Services - General Inquirie  2026:8.9K
  Curbside Special Solid Waste Pick-up Req  2026:7.8K
  Foreclosed Property Registration Applica  2026:24.0K
  Historic Preservation Commission          2026:78
  Mayor Jane Castor's Office                2026:30.3K
  Mobile App Enhancement Request            2026:205
  New Business Tax Receipt Application      2026:19.5K
  Parks and Recreation                      2026:11.7K
  Picnic Shelter Requests                   2026:13.4K
  Police                                    2026:25.9K
  Pothole Repair ONLY (non Cave-In/Sinking  2026:17.3K
  Request a Grant Letter of Support         2026:20
  Residential Service was Missed (Garbage,  2026:23.2K
  Sewer Odor Complaint                      2026:1.3K
  Solid Waste General Correspondence        2026:32.2K
  Solid Waste/EPM Personnel/Crew Complimen  2026:51
  Street Marking Request (Repair)           2026:444
  Transportation Executive - Operations Ta  2026:168
  Tree Removal Information                  2026:2.6K
  Utility Bill Questions                    2026:79.2K
  Utility Information Service Request (int  2026:41.6K
  Utility Service High Utility Bill Inquir  2026:31.4K
  Utility Service Start Request             2026:117.9K
  Utility Service Stop Request              2026:57.2K
  Water Color Concern (Cloudy, Discolored,  2026:1.3K

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = AMOUNT
  55da4550ea3a11a4b12a07d016412a309857b9bd  2026:997.2K

## what

STATUS: Closed 62%, Other 38%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 436 | 0 | 1352226 3; 1352225 3; 1352224 3; 1352223 3 |
| SERVICENAME | who | 272 | 0 | Zoning Violations 3; Zoning District Regulatio 3; Ybor City Development Cor 3; Wet Zoning Inquiries 3 |
| AMOUNT | amount | 274 | 0 | 1 40; 2 23; 5 21; 3 20 |
| PERCENTAMOUNT | amount | 181 | 0 | 100 105; 0.16 9; 99.84 9; 0.14 7 |
| AVERAGEAMOUNT | amount | 346 | 0 | 0 41; 0.04 6; 1.52 5; 0.17 4 |
| STATUS | category | 2 | 0 | Closed 274; Other 169 |
| DESCRIPTION | other | 276 | 0 | Customer Service Center M 3; Customer Service Center M 3; Customer Service Center M 3; Customer Service Center M 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:20:34.85651 443 |
| SOURCE_RUN_ID | audit | 1 | 0 | ce20197e-f9f8-4f7a-ae1d-6 443 |
| SRC_SHA256 | who | 1 | 0 | 55da4550ea3a11a4b12a07d01 443 |
