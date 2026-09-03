# FED_CMS_MEDICARE_DIABETES_PREVENTION_PROGRAM

rows 1.0K  columns 15  scan 2.7s

roles: audit 2, category 1, date 1, id 3, other 6, state 1, who 3

## when

_INGESTED_AT
  2026      1.0K  ##############################

## who

LOCATION_NAME by rows
        64  Southern California Permanente Medical Group
        53  Uho - Ymca Of Metropolitan Milwaukee
        51  Providence Health & Services Oregon
        27  The Granite Ymca
        23  Prana Diabetes Inc
        23  Hockomock Young Mens Christian Asso
        16  Calvert County Health Department
        15  Kaiser Fndt Health Plan Of Colorado
        15  Uho - Ymca Metro Milwaukee
        15  Tampa Metropolitan Area Young Men'S Christian Association Inc
        14  St Mary Mercy Hospital
        13  Ihc Health Services Inc
        13  St Vincent Medical Group Inc
        12  Health Promotion Council Of Southeastern Pennsylvania, Inc.
        11  Johns Hopkins University
        11  Young Men'S Christian Association Of The Suncoast, Inc.
        11  Western New York Integrated Care Collaborative Inc
        11  Young Mens Christian Association Of Silicon Valley
        10  District Health Department #10
         9  Centro De Salud De La Comunidad De San Ysidro, Inc.

ORGANIZATION_NAME by rows
        69  Uho - Ymca Of Metropolitan Milwaukee
        64  Southern California Permanente Medical Group
        51  Providence Health & Services Oregon
        39  The Granite Ymca
        25  The Young Mens Christian Association Of Greater Seattle
        23  Hockomock Young Men'S Christian Association Inc.
        23  Prana Diabetes Inc
        21  The Young Men'S Christian Association Of Metropolitan Denver
        16  Calvert County Health Department
        15  Tampa Metropolitan Area Young Men'S Christian Association Inc
        15  Kaiser Foundation Health Plan Of Colorado
        14  St Mary Mercy Hospital
        13  Health Promotion Council Of Southeastern Pennsylvania, Inc.
        13  St Vincent Medical Group Inc
        13  Ihc Health Services Inc
        12  Network Health Ventures Llc
        12  Johns Hopkins University
        11  Young Mens Christian Association Of Silicon Valley
        11  Young Men'S Christian Association Of Delaware
        11  Henry Ford Macomb Hospital Corporation

NAME_OF_INITIATIVE by rows
      1.0K  Medicare Diabetes Prevention Program (MDPP) Expanded Model

## who x when

LOCATION_NAME by _INGESTED_AT  LOAD STAMP, not an event date
  Calvert County Health Department          2026:16
  Centro De Salud De La Comunidad De San Y  2026:9
  District Health Department #10            2026:10
  Health Promotion Council Of Southeastern  2026:12
  Hockomock Young Mens Christian Asso       2026:23
  Ihc Health Services Inc                   2026:13
  Johns Hopkins University                  2026:11
  Kaiser Fndt Health Plan Of Colorado       2026:15
  Prana Diabetes Inc                        2026:23
  Providence Health & Services Oregon       2026:51
  Southern California Permanente Medical G  2026:64
  St Mary Mercy Hospital                    2026:14
  St Vincent Medical Group Inc              2026:13
  Tampa Metropolitan Area Young Men'S Chri  2026:15
  The Granite Ymca                          2026:27
  Uho - Ymca Metro Milwaukee                2026:15
  Uho - Ymca Of Metropolitan Milwaukee      2026:53
  Western New York Integrated Care Collabo  2026:11
  Young Men'S Christian Association Of The  2026:11
  Young Mens Christian Association Of Sili  2026:11

ORGANIZATION_NAME by _INGESTED_AT  LOAD STAMP, not an event date
  Calvert County Health Department          2026:16
  Health Promotion Council Of Southeastern  2026:13
  Henry Ford Macomb Hospital Corporation    2026:11
  Hockomock Young Men'S Christian Associat  2026:23
  Ihc Health Services Inc                   2026:13
  Johns Hopkins University                  2026:12
  Kaiser Foundation Health Plan Of Colorad  2026:15
  Network Health Ventures Llc               2026:12
  Prana Diabetes Inc                        2026:23
  Providence Health & Services Oregon       2026:51
  Southern California Permanente Medical G  2026:64
  St Mary Mercy Hospital                    2026:14
  St Vincent Medical Group Inc              2026:13
  Tampa Metropolitan Area Young Men'S Chri  2026:15
  The Granite Ymca                          2026:39
  The Young Men'S Christian Association Of  2026:21
  The Young Mens Christian Association Of   2026:25
  Uho - Ymca Of Metropolitan Milwaukee      2026:69
  Young Men'S Christian Association Of Del  2026:11
  Young Mens Christian Association Of Sili  2026:11

## where

STATE: CA 122, OR 71, FL 67, NY 59, MD 51, MI 46, CO 45, WI 42, IN 42, OH 36, PA 35, WA 34

## what

CATEGORY: Administrative Location 65%, Community Setting 35%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NAME_OF_INITIATIVE | who | 1 | 0 | Medicare Diabetes Prevent 1.0K |
| ORGANIZATION_NAME | who | 300 | 0 | Uho - Ymca Of Metropolita 69; Southern California Perma 65; Providence Health & Servi 51; The Granite Ymca 39 |
| LOCATION_NAME | who | 439 | 0 | Southern California Perma 66; Uho - Ymca Of Metropolita 54; Providence Health & Servi 51; The Granite Ymca 28 |
| LOCATION_1 | id | 1.0K | 0 | 121 Dekalb Ave  Brooklyn  6; 129 W Kemper Rd  Springda 6; 26a Picotte Dr  Albany NY 6; 2206 Mitchell Park Dr Ste 6 |
| STREET_ADDRESS_LINE_1 | other | 974 | 0 | 121 Dekalb Ave 6; 129 W Kemper Rd 6; 26a Picotte Dr 6; 2206 Mitchell Park Dr 6 |
| STREET_ADDRESS_LINE_2 | other | 239 | 724 | Ste 200 9; Ste 300 7; Ste A 7; Ste 102 5 |
| CITY | other | 639 | 0 | Indianapolis 24; Portland 18; Baltimore 15; San Diego 12 |
| STATE | state | 51 | 0 | CA 122; OR 71; FL 67; NY 59 |
| ZIP_CODE | other | 870 | 0 | 20678 8; 91402 7; 11201 6; 45246 6 |
| TELEPHONE_NUMBER | other | 673 | 0 | (503) 215-1290 51; (714) 748-2654 18; (440) 574-0580 16; (904) 265-1777 16 |
| NPI | other | 313 | 0 | 1508523770 70; 1952333478 65; 1003319724 51; 1699377119 39 |
| CATEGORY | category | 2 | 0 | Administrative Location 669; Community Setting 368 |
| UNIQUE_ID | id | 1.0K | 0 | 1037 6; 1036 6; 1035 6; 1034 6 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-07-26 11:45:49.418 1.0K |
| _SOURCE_RUN_ID | audit id | 1.0K | 0 | 00ac44b7-b407-4513-93f7-a 6; ebe147da-c66c-497e-ac5b-4 6; de6363dc-1add-4294-b08b-9 6; 0aa855b3-55a8-4548-b0fd-d 6 |
