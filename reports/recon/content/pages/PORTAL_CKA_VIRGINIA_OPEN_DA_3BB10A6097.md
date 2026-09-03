# PORTAL_CKA_VIRGINIA_OPEN_DA_3BB10A6097

rows 263  columns 14  scan 4.4s

roles: amount 3, audit 2, category 2, date 1, other 4, who 3

## when

INGESTED_AT
  2026       263  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SITE_ACREAGE | 211 | 0.10 | 11.39 | 1.3K | 2.2K | 17.4K |
| SHAPE_LENGTH | 263 | 4.67 | 1.4K | 20.2K | 52.5K | 700.0K |
| SHAPE_AREA | 263 | 0.02 | 74.1K | 7.12M | 14.32M | 125.09M |

## who

APPLICANT by rows
         5  Joe Benton
         3  Robert Moses
         2  Thomas Quattlebaum
         2  Amherst EDA
         2  Randy Remillard
         2  Frank Fentress
         2  Marc Poulson
         2  City of Danville
         2  Scott Ashe
         2  River Mountain Solar 2, LLC
         2  City of Virginia Beach
         1  Isle of Wight County
         1  SunCap Property Group
         1  Milo Pfeffer
         1  Quick GK/FJ, LLC
         1  Dan Hotel River St LLC
         1  SOLIS ARX VA LLC
         1  Town of Blacksburg
         1  City of Norfolk
         1  Carlos Rengifo

APPLICANT by dollars
       52.5K        1 rows  Recurrent Energy
       37.6K        1 rows  Ramaco Resources Land Holdings LLC
       18.9K        2 rows  Frank Fentress
       11.5K        1 rows  Mitchell Conner
       11.2K        1 rows  Appomattox County
       10.1K        2 rows  River Mountain Solar 2, LLC
        9.9K        1 rows  Google, LLC
        8.8K        1 rows  Richard Curtis
        8.6K        1 rows  American Electric Power
        7.4K        1 rows  Fairwinds Landing, LLC
        6.8K        2 rows  Amherst EDA
        6.0K        1 rows  East Point Energy
        5.7K        1 rows  Amherst County EDA
        5.4K        2 rows  Marc Poulson
        5.1K        1 rows  William Darden
        5.1K        1 rows  CEP Solar, LLC
        4.9K        1 rows  Rogers Road Solar 1, LLC
        4.9K        1 rows  Reese Jones
        4.9K        1 rows  Clay Sawyer
        4.9K        2 rows  City of Danville

DELINEATION_AGENT by rows
        23  Rick Harris
        20  Matt Roth
        14  Julie Steele
         9  Brian Owen
         9  N/A
         8  Benjamin Rosner
         8  Sandra Brinson
         7  Hurt & Proffitt
         6  Matt Zubak
         6  Nikolai Karlov
         5  Balzer & Associates
         5  Nicholas Romano
         4  Avi Sareen
         4  Alexi Weber
         4  Benjamin Rosner VSWD0011
         3  Janelle Bernosky
         3  Dewberry
         3  VSWD0011
         3  Jamie Armentrout
         3  Robby Atwood, MSA

DELINEATION_AGENT by dollars
       52.5K        1 rows  Freese and Nichols
       44.7K        3 rows  Daniel Cox
       37.6K        1 rows  Artemis Consulting Services
       33.8K       23 rows  Rick Harris
       23.1K        7 rows  Hurt & Proffitt
       22.7K        6 rows  Nikolai Karlov
       19.2K        9 rows  N/A
       18.9K        2 rows  VSWD0034
       17.9K        5 rows  Nicholas Romano
       17.5K        8 rows  Benjamin Rosner
       16.3K        9 rows  Brian Owen
       15.2K       20 rows  Matt Roth
       15.2K        3 rows  Dewberry
       15.0K        2 rows  Timmons
       13.7K        5 rows  Balzer & Associates
       12.7K       14 rows  Julie Steele
       11.2K        4 rows  Avi Sareen
       11.2K        1 rows  Kimley-Horn
       10.1K        1 rows  Jennifer Feese
        9.2K        3 rows  VSWD0011

SRC_SHA256 by rows
       263  2e0383784307e87c1a78625f671bb7e069e316ca83b0ad920fbf3805ef04c081

SRC_SHA256 by dollars
      700.0K      263 rows  2e0383784307e87c1a78625f671bb7e069e316ca83b0ad920fbf3805ef04

## who x when

APPLICANT by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  American Electric Power                   2026:8.6K
  Amherst County EDA                        2026:5.7K
  Amherst EDA                               2026:6.8K
  Appomattox County                         2026:11.2K
  Carlos Rengifo                            2026:461.72
  City of Danville                          2026:4.9K
  City of Norfolk                           2026:3.9K
  City of Virginia Beach                    2026:2.6K
  Dan Hotel River St LLC                    2026:765.81
  East Point Energy                         2026:6.0K
  Fairwinds Landing, LLC                    2026:7.4K
  Frank Fentress                            2026:18.9K
  Google, LLC                               2026:9.9K
  Isle of Wight County                      2026:3.4K
  Joe Benton                                2026:1.7K
  Marc Poulson                              2026:5.4K
  Milo Pfeffer                              2026:586.97
  Mitchell Conner                           2026:11.5K
  Quick GK/FJ, LLC                          2026:454.63
  Ramaco Resources Land Holdings LLC        2026:37.6K
  Randy Remillard                           2026:485.38
  Recurrent Energy                          2026:52.5K
  Richard Curtis                            2026:8.8K
  River Mountain Solar 2, LLC               2026:10.1K
  Robert Moses                              2026:1.7K
  SOLIS ARX VA LLC                          2026:3.2K
  Scott Ashe                                2026:3.4K
  SunCap Property Group                     2026:1.3K
  Thomas Quattlebaum                        2026:743.45
  Town of Blacksburg                        2026:4.7K

DELINEATION_AGENT by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  Alexi Weber                               2026:6.6K
  Artemis Consulting Services               2026:37.6K
  Avi Sareen                                2026:11.2K
  Balzer & Associates                       2026:13.7K
  Benjamin Rosner                           2026:17.5K
  Benjamin Rosner VSWD0011                  2026:7.8K
  Brian Owen                                2026:16.3K
  Daniel Cox                                2026:44.7K
  Dewberry                                  2026:15.2K
  Freese and Nichols                        2026:52.5K
  Hurt & Proffitt                           2026:23.1K
  Jamie Armentrout                          2026:5.8K
  Janelle Bernosky                          2026:2.8K
  Jennifer Feese                            2026:10.1K
  Julie Steele                              2026:12.7K
  Kimley-Horn                               2026:11.2K
  Matt Roth                                 2026:15.2K
  Matt Zubak                                2026:8.1K
  N/A                                       2026:19.2K
  Nicholas Romano                           2026:17.9K
  Nikolai Karlov                            2026:22.7K
  Rick Harris                               2026:33.8K
  Robby Atwood, MSA                         2026:2.3K
  Sandra Brinson                            2026:6.2K
  Timmons                                   2026:15.0K
  VSWD0011                                  2026:9.2K
  VSWD0034                                  2026:18.9K

## what

REGION: TRO 56%, NRO 31%, BRRO 10%, SWRO 2%, BRRo 1%, Tidewater  0%

FIC_DESCRIPTION: Isle of Wight 28%, Chesapeake 21%, Virginia Beach 13%, Poquoson 7%, Suffolk 7%, York 5%, Amherst 5%, Hampton 4%, Williamsburg 4%, Norfolk 4%, Montgomery 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 262 | 0 | 263 2; 262 2; 261 2; 260 2 |
| SSWD_NUMBER | other | 256 | 7 | SSWD-000773 2; SSWD-000756 2; SSWD-000722 2; 000720 2 |
| PERMIT_NUMBER | other | 76 | 188 | WP4-05-2235 2; NA 1; Church Hill Drive 1; 819 James Madison Hwy 1 |
| DELINEATION_AGENT | who | 84 | 35 | Rick Harris 23; Matt Roth 20; Julie Steele 14; Brian Owen 9 |
| REGION | category | 7 | 18 | TRO 137; NRO 76; BRRO 24; SWRO 5 |
| APPLICANT | who | 153 | 98 | Joe Benton 5; Robert Moses 3; City of Danville 2; Marc Poulson 2 |
| FIC_DESCRIPTION | category | 38 | 109 | Isle of Wight 31; Chesapeake 23; Virginia Beach 14; Poquoson 8 |
| APPROVAL_DATE | other | 227 | 29 | 2025/02/05 00:00:00+00 3; 2025/01/16 00:00:00+00 3; 2026/05/04 13:34:54+00 2; 2026/04/10 16:40:57+00 2 |
| SITE_ACREAGE | amount | 185 | 52 | 5 6; 3 4; 1 3; 0.34 2 |
| SHAPE_LENGTH | amount | 256 | 0 | 4.67380399456672 4; 352.500707638717 3; 2526.46757402408 2; 203.929948347155 2 |
| SHAPE_AREA | amount | 254 | 0 | 0.0219224716641146 4; 6573.35291320773 3; 317031.037149669 2; 2488.75761680869 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:38:04.81838 263 |
| SOURCE_RUN_ID | audit | 1 | 0 | ae6225e8-09e3-42bb-ada5-a 263 |
| SRC_SHA256 | who | 1 | 0 | 2e0383784307e87c1a78625f6 263 |
