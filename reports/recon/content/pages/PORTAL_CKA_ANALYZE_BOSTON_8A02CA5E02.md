# PORTAL_CKA_ANALYZE_BOSTON_8A02CA5E02

rows 1.4K  columns 20  scan 4.2s

roles: amount 2, audit 2, category 7, date 2, id 6, who 2

## when

PLANNED_INSTALL_DATE
  2008         1  
  2017        28  ##
  2018       434  ##############################
  2019       215  ###############
  2020       206  ##############
  2021       259  ##################
  2022       127  #########
  2023        58  ####
  2024        24  ##
  2025        27  ##
  2026         3  

INGESTED_AT
  2026      1.4K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| POINT_X | 1.4K | -71.17 | -71.08 | -71.01 | -71 | -98.2K |
| POINT_Y | 1.4K | 42.24 | 42.34 | 42.39 | 42.39 | 58.5K |

## who

NEW_POLE_TYPE by rows
       186  Wood Utility Pole Antenna Top Mount (Verizon Exhibit X-4)
       173  Wood Utility Pole Antenna Side Mount (Verizon Exhibit X-5)
       172  Aeriata Light Pole with Side Mount (Extenet X-13)
        89  Double Acorn Light Pole with Side Mount & Whip Antenna (Extenet Exhibi
        73  Standard Concrete Light Pole (Lightower Exhibit X-1)
        63  Standard Concrete Light Pole (Verizon Exhibit X-1)
        44  Pendant Light Pole (Lightower Exhibit X-3)
        43  Pendant Light Pole with Side Mount (Extenet X-16)
        36  Aeriata Light Pole ( Verizon Exhibit X-2)
        36  Standard Concrete Light Pole (Extenet Exhibit X-1)
        35  Pendant Light Pole (Verizon Exhibit X-3)
        34  Standard Concrete Light Pole with Side Mount (Extenet X-18A)
        33  Double Acorn Light Pole with Base & Whip Antenna (Lightower Exhibit X-
        32  Double Acorn Light Pole with Side Mount & Whip Antenna (Lightower Exhi
        27  Aeriata Light Pole (Lightower Exhibit X-2)
        25  Pendant Light Pole (Extenet Exhibit X-3)
        23  Standard Concrete Light Pole (Verizon Exhibit X-1A)
        23  Aeriata Light Pole (Extenet Exhibit X-2)
        22  Wood Utility Pole Antenna Top Mount (Extenet Exhibit X-4)
        22  Double Acorn Light Pole with Base & Whip Antenna (Extenet Exhibit X-8)

NEW_POLE_TYPE by dollars
      -71.05        1 rows  Convention Center Round Tapered Pole with Side Mount (Crown 
      -71.06        1 rows  Convention Center Round Tapered Pole (Crown Castle Exhibit X
      -71.06        1 rows  Pendant Light Pole (Crown Castle Exhibit X-3)
      -71.07        1 rows  Wood Utility Pole Antenna Side Mount (Crown Castle Exhibit X
      -71.08        1 rows  Contemporary Square Aluminum Light Pole with Side Mount (Ext
      -71.09        1 rows  Double Acorn Light Pole with Base & Whip Antenna & 5G (Exten
      -71.10        1 rows  Wood Utility Pole Antenna Top Mount (Crown Castle Exhibit X-
      -71.15        1 rows  Double Pendant Light Pole with Side Mount (Extenet X-15)
     -142.11        2 rows  Quad Acorn Light Pole with Base & Whip Antenna (Lightower Ex
     -142.12        2 rows  Double Straight Light Pole (Lightower Exhibit X-11)
     -142.12        2 rows  Double Cobra Light Pole (Lightower Exhibit X-12)
     -142.13        2 rows  Pendant Light Pole with Side Mount (Crown Castle X-16A)
     -142.15        2 rows  Wood Utility Pole Antenna Top Mount (Extenet Exhibit X-4A)
     -142.17        2 rows  Contemporary Square Aluminum Light Pole with Side Mount (Cro
     -142.20        2 rows  Standard Concrete Light Pole (Crown Castle Exhibit X-1A)
     -213.13        3 rows  Double Nautical Light Pole with Base & Whip Antenna (Crown C
     -213.18        3 rows  Pendant Light Pole (Crown Castle Exhibit X-3A)
     -213.18        3 rows  Double Acorn Light Pole with Base & Whip Antenna (Crown Cast
     -213.20        3 rows  Double Pendant Light Pole (Extenet X-14)
     -213.27        3 rows  Contemporary Square Aluminum Light Pole with Side Mount (Cro

SRC_SHA256 by rows
      1.4K  5733c10c30de9838936ae2d44e3ec5716a210b69105d9dd164cfe88c957d8a49

SRC_SHA256 by dollars
      -98.2K     1.4K rows  5733c10c30de9838936ae2d44e3ec5716a210b69105d9dd164cfe88c957d

## who x when

NEW_POLE_TYPE by PLANNED_INSTALL_DATE, dollars = POINT_X
  Aeriata Light Pole ( Verizon Exhibit X-2  2018:-2.6K
  Aeriata Light Pole (Extenet Exhibit X-2)  2018:-1.3K 2019:-142.17 2020:-213.26
  Aeriata Light Pole (Lightower Exhibit X-  2017:-710.84 2018:-1.2K
  Aeriata Light Pole with Side Mount (Exte  2018:-2.1K 2019:-213.18 2020:-213.30 2021:-3.6K 2022:-5.0K 2023:-995.37
  Contemporary Square Aluminum Light Pole   2023:-71.08
  Convention Center Round Tapered Pole (Cr  2021:-71.06
  Convention Center Round Tapered Pole wit  2018:-71.05
  Double Acorn Light Pole with Base & Whip  2023:-71.09
  Double Acorn Light Pole with Base & Whip  2018:-1.4K 2020:-71.08 2022:-71.08
  Double Acorn Light Pole with Base & Whip  2018:-1.7K 2019:-355.41 2020:-284.24
  Double Acorn Light Pole with Side Mount   2018:-1.4K 2019:-710.65 2020:-142.12 2021:-1.5K 2022:-1.1K 2023:-710.72 2024:-781.66 2025:-71.07
  Double Acorn Light Pole with Side Mount   2017:-71.04 2018:-2.0K 2019:-142.11 2021:-71.06
  Double Pendant Light Pole with Side Moun  2018:-71.15
  Double Straight Light Pole (Lightower Ex  2018:-142.12
  Pendant Light Pole (Crown Castle Exhibit  2017:-71.06
  Pendant Light Pole (Extenet Exhibit X-3)  2018:-1.2K 2019:-426.45 2021:-142.17
  Pendant Light Pole (Lightower Exhibit X-  2017:-284.34 2018:-2.1K 2019:-639.68 2020:-71.10
  Pendant Light Pole (Verizon Exhibit X-3)  2018:-2.1K 2019:-284.33 2022:-71.07
  Pendant Light Pole with Side Mount (Exte  2018:-355.43 2021:-781.79 2022:-853.02 2023:-852.89 2024:-142.12 2025:-71.07
  Quad Acorn Light Pole with Base & Whip A  2018:-71.06 2019:-71.05
  Standard Concrete Light Pole (Extenet Ex  2018:-1.5K 2019:-213.25 2020:-213.24 2021:-284.30 2022:-213.30 2023:-142.20
  Standard Concrete Light Pole (Lightower   2017:-284.12 2018:-1.7K 2019:-2.8K 2020:-355.35 2021:-71.06
  Standard Concrete Light Pole (Verizon Ex  2017:-213.26 2018:-2.8K 2019:-995.16 2020:-284.38 2021:-142.13
  Standard Concrete Light Pole (Verizon Ex  2018:-142.18 2019:-710.79 2020:-284.25 2021:-426.39 2022:-71.15
  Standard Concrete Light Pole with Side M  2021:-710.88 2022:-71.09 2023:-1.1K 2024:-568.62
  Wood Utility Pole Antenna Side Mount (Cr  2019:-71.07
  Wood Utility Pole Antenna Side Mount (Ve  2018:-71.17 2019:-1.1K 2020:-5.5K 2021:-4.6K 2022:-853.52 2025:-213.35
  Wood Utility Pole Antenna Top Mount (Cro  2018:-71.10
  Wood Utility Pole Antenna Top Mount (Ext  2018:-639.96 2019:-426.59 2020:-213.31 2021:-142.21 2022:-142.17
  Wood Utility Pole Antenna Top Mount (Ver  2017:-213.17 2018:-1.1K 2019:-2.9K 2020:-4.5K 2021:-4.2K 2024:-71.11 2025:-213.18

SRC_SHA256 by PLANNED_INSTALL_DATE, dollars = POINT_X
  5733c10c30de9838936ae2d44e3ec5716a210b69  2008:-71.07 2017:-2.0K 2018:-30.8K 2019:-15.3K 2020:-14.6K 2021:-18.4K 2022:-9.0K 2023:-4.1K 2024:-1.7K 2025:-1.9K 2026:-213.29

## what

VENDOR: ExteNet Systems 40%, Verizon Wireless 39%, Lightower 16%, Crown Castle 6%

NEIGHBORHOOD: Downtown / Financial District 14%, Dorchester 14%, Fenway / Kenmore 12%, Allston / Brighton 9%, Roxbury 8%, Hyde Park 8%, West Roxbury 8%, South Boston 7%, North End 6%, Greater Mattapan 5%, South End 5%, Back Bay 5%

ORIGINAL_POLE_TYPE: Wood Utility Pole (Not City Ow 30%, Standard Concrete - Aeriata 21%, Pendant 13%, Acorn - Double 10%, Standard Concrete - Cobra 9%, Aeriata Light Pole 5%, Standard Concrete 4%, Acorn - Single 4%, Contemporary Square Aluminium  1%, Pendant - Double 1%, Standard Concrete - Double Cob 0%, Nautical - Double 0%

ATTACHMENT_OR_REPLACEMENT: Replacement 70%, Attachment 29%, Upgrade to Pre-2017 PIC approv 1%

INTENDED_COMMERCIAL_USE: Single Carrier 57%, Neutral Host 43%

SPECTRUM: Licensed 98%, Both 2%

REQUESTER_EMAIL_ADDRESS: vzwexhibitx1@gmail.com 32%, ExteNetER@gmail.com 20%, mconstantino@lightower.com 16%, exteneter@gmail.com 11%, rsousa@princelobel.com 8%, VZWExhibitX1@gmail.com 6%, amanda.cornwall@crowncastle.co 2%, ucsdoit@gmail.com 2%, ccf-ne-district-permitting@cro 1%, CCF-NE-District-Permitting@cro 1%, MGiaimo@rc.com 1%, joseph.shannon@crowncastle.com 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| VENDOR | category | 4 | 0 | ExteNet Systems 548; Verizon Wireless 536; Lightower 218; Crown Castle 80 |
| NEIGHBORHOOD | category | 19 | 0 | Downtown / Financial Dist 156; Dorchester 154; Fenway / Kenmore 128; Allston / Brighton 99 |
| ADDRESS | id | 1.4K | 0 | 33 Roseberry Rd 7; 59 Oakcrest Rd 7; 41 Chestnut Hill Ave, pol 7; Intersection of Gordon St 7 |
| LAT | id | 1.4K | 0 | 42.267575999999998 7; 42.265278000000002 7; 42.347088999999997 7; 42.350563999999999 7 |
| LONG | id | 1.4K | 0 | -71.000000000000000 10; -71.103707999999997 7; -71.103545999999994 7; -71.153852999999998 7 |
| PLANNED_INSTALL_DATE | date | 514 | 0 | 7/1/2018 0:00:00.000 58; 8/1/2018 0:00:00.000 36; 6/1/2018 0:00:00.000 31; 3/31/2023 0:00:00.000 22 |
| ORIGINAL_POLE_TYPE | category | 14 | 0 | Wood Utility Pole (Not Ci 417; Standard Concrete - Aeria 294; Pendant 179; Acorn - Double 138 |
| ATTACHMENT_OR_REPLACEMENT | category | 3 | 0 | Replacement 970; Attachment 399; Upgrade to Pre-2017 PIC a 13 |
| NEW_POLE_TYPE | who | 56 | 0 | Wood Utility Pole Antenna 186; Wood Utility Pole Antenna 173; Aeriata Light Pole with S 172; Double Acorn Light Pole w 89 |
| POLE_IDENTIFYING_NUMBER | id | 1.4K | 0 | 553349 7; 553348 7; 531735 7; 531731 7 |
| INTENDED_COMMERCIAL_USE | category | 2 | 0 | Single Carrier 786; Neutral Host 596 |
| SPECTRUM | category | 2 | 0 | Licensed 1.4K; Both 24 |
| CITY_REFERENCE | id | 1.4K | 0 | Ver2322 7; Ver2321 7; Ver2320 7; Ver2319 7 |
| REQUESTER_EMAIL_ADDRESS | category | 42 | 0 | vzwexhibitx1@gmail.com 422; ExteNetER@gmail.com 268; mconstantino@lightower.co 216; exteneter@gmail.com 144 |
| SHAPE_WKT | id | 1.4K | 0 | POINT (-71.10370799999998 7; POINT (-71.10354599999993 7; POINT (-71.15385299999997 7; POINT (-71.14002599999997 7 |
| POINT_X | amount | 1.4K | 0 | -70.999999999999943 10; -71.103707999999983 7; -71.103545999999938 7; -71.153852999999970 7 |
| POINT_Y | amount | 1.4K | 0 | 42.267576000000076 7; 42.265278000000080 7; 42.347089000000040 7; 42.350564000000077 7 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:53:47.11644 1.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | 5eef6111-6c65-4bff-b3e0-a 1.4K |
| SRC_SHA256 | who | 1 | 0 | 5733c10c30de9838936ae2d44 1.4K |
