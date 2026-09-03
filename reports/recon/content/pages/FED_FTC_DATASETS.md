# FED_FTC_DATASETS

rows 1.2K  columns 11  scan 2.7s

roles: audit 2, date 1, empty 5, other 1, who 2

## when

DATE_FILED
  2021       120  ##############
  2022       197  ########################
  2023       166  ####################
  2024       225  ###########################
  2025       241  #############################
  2026       251  ##############################

## who

ACTION_NAME by rows
        50  The FTC Is on the Front Lines of Tech Innovation & Regulation
        50  How Loyalty Discounts Between Firms Harm Competition When There Are  N
        50  Military Consumer Protection in Action: Tools and Tactics for Service 
        50  FTC Seeks Public Comment on Policy Statement Addressing AI Accuracy
         2  NewsGuard/World Federation of Advertising
         2  Hargrove & Associates, Inc.’s Petition to Quash or Limit Civil Investi
         2  Statement of Chair Lina M. Khan Regarding the Advance Notice of Propos
         1  Touchtunes Music Company, FTC v.
         1  Growthmind/Wisey
         1  Air.ai
         1  Edwards Lifesciences Corporation and JenaValve Technology, Inc., FTC v
         1  World Professional Association for Transgender Health (WPATH)
         1  William E. March, In the Matter of
         1  Wellington, FTC v.
         1  Dissenting Statement of Commissioner Rebecca Kelly Slaughter Regarding
         1  Edwards Lifesciences Corp. and JenaValve Technology, Inc., In the Matt
         1  Eras/KIG
         1  Model Letter sent to Tech Companies from Chairman Andrew N. Ferguson
         1  Amazon.com, Inc. (ROSCA), FTC v.
         1  Statement of Commissioner Mark R. Meador In the Matter of Providence E

_SRC_SHA256 by rows
      1.2K  d4a557e19afd391f232c998f2b8e919900fc9d49660488dddbdd88829032b13e

## who x when

ACTION_NAME by DATE_FILED
  Air.ai                                    2026:1
  Amazon.com, Inc. (ROSCA), FTC v.          2025:1
  Dissenting Statement of Commissioner Reb  2025:1
  Edwards Lifesciences Corp. and JenaValve  2026:1
  Edwards Lifesciences Corporation and Jen  2026:1
  Eras/KIG                                  2025:1
  FTC Seeks Public Comment on Policy State  2026:50
  Growthmind/Wisey                          2026:1
  Hargrove & Associates, Inc.’s Petition t  2024:2
  How Loyalty Discounts Between Firms Harm  2026:50
  Military Consumer Protection in Action:   2026:50
  Model Letter sent to Tech Companies from  2025:1
  NewsGuard/World Federation of Advertisin  2025:1 2026:1
  Statement of Chair Lina M. Khan Regardin  2022:2
  Statement of Commissioner Mark R. Meador  2026:1
  The FTC Is on the Front Lines of Tech In  2025:50
  Touchtunes Music Company, FTC v.          2026:1
  Wellington, FTC v.                        2026:1
  William E. March, In the Matter of        2026:1
  World Professional Association for Trans  2026:1

_SRC_SHA256 by DATE_FILED
  d4a557e19afd391f232c998f2b8e919900fc9d49  2021:120 2022:197 2023:166 2024:225 2025:241 2026:251

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ACTION_NAME | who | 1.0K | 0 | Military Consumer Protect 50; FTC Seeks Public Comment  50; The FTC Is on the Front L 50; How Loyalty Discounts Bet 50 |
| RESPONDENT | empty | 1 | 1.2K |  |
| DATE_FILED | date | 541 | 0 | 2026-07-07T15:00:00Z 50; 2026-07-01T12:00:00Z 50; 2025-01-17T21:30:00Z 50; 2026-02-13T22:00:00Z 50 |
| CASE_TYPE | empty | 1 | 1.2K |  |
| STATUS | empty | 1 | 1.2K |  |
| TOPIC | empty | 1 | 1.2K |  |
| DOCUMENT_URL | other | 996 | 0 | https://www.ftc.gov/news- 50; https://www.ftc.gov/news- 50; https://www.ftc.gov/polic 50; https://www.ftc.gov/enfor 50 |
| EIN | empty | 1 | 1.2K |  |
| _INGESTED_AT | audit | 1 | 0 | 1782954371105196 1.2K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 5443253f-5e6f-4705-a6ae-3 1.2K |
| _SRC_SHA256 | who | 1 | 0 | d4a557e19afd391f232c998f2 1.2K |
