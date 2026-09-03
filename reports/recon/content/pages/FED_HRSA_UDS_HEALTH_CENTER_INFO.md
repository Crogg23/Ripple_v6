# FED_HRSA_UDS_HEALTH_CENTER_INFO

rows 1.4K  columns 22  scan 2.3s

roles: audit 2, category 6, id 6, other 4, state 1, who 3

## who

HEALTHCENTERNAME by rows
         3  FAMILY HEALTH CENTER, INC.
         3  COMMUNITY HEALTH CENTERS, INC.
         3  COMMUNITY HEALTH SYSTEMS, INC.
         2  TRI-STATE COMMUNITY HEALTH CENTER
         2  COMMUNITY HEALTH CARE, INC.
         2  RURAL HEALTH CARE, INC.
         1  OSBORN FAMILY HEALTH CENTER, INC., THE
         1  CENTRAL JERSEY MEDICAL CENTER INC.
         1  CENTRO DE SALUD FAMILIAR (PALMIERI)
         1  STAYWELL HEALTH CARE, INC.
         1  NORTH HUDSON COMMUNITY ACTION CORPORATION
         1  SOUTHERN JERSEY FAMILY
         1  MONTEFIORE MEDICAL CENTER
         1  UPSTATE FAMILY HEALTH CENTER, INC.
         1  SOUTHWEST COMMUNITY HEALTH CENTER
         1  EAST BAY COMMUNITY ACTION PROGRAM
         1  HOUSING WORKS HEALTH SERVICES III, INC.
         1  CENTRO DE SALUD DE LARES, INC.
         1  COMMUNITY HEALTH CENTER OF RICHMOND, INC.
         1  ISLAND HEALTH INC

PROJECTDIRECTORFAX by rows
       653  -
         1  (787)871-3960
         1  (724)632-6312
         1  (508)477-3909
         1  (718)686-2099
         1  (609)704-5511
         1  (787)739-8190
         1  (845)354-9448
         1  (757)223-0839
         1  (434)791-4126
         1  (973)789-8407
         1  (215)925-6166
         1  (304)354-9323
         1  (757)414-0569
         1  (401)285-5101
         1  (207)498-3947
         1  (276)398-3331
         1  (302)655-6606
         1  (207)794-0055
         1  (203)899-1769

_SRC_SHA256 by rows
      1.4K  1f8a7503f54892163a32083ec46c59f4695c9ad6c0e37a9c458fc88f7111fbfb

## where

HEALTHCENTERSTATE: CA 170, TX 71, NY 64, OH 51, FL 47, IL 45, PA 40, MI 39, NC 38, MA 37, LA 35, GA 35

## what

HEALTHCENTEROTHERADDRESS: - 100%, A 0%, 100 0%

FUNDINGCHC: True 95%, False 5%

FUNDINGMSAW: False 87%, True 13%

FUNDINGHP: False 78%, True 22%

FUNDINGRPH: False 92%, True 8%

URBANRURALFLAG: Urban 58%, Rural 42%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| BHCMISID | id | 1.3K | 0 | 11E01386 7; 11E01249 7; 10E01466 7; 10E01221 7 |
| GRANTNUMBER | id | 1.4K | 0 | H80CS35350 7; H80CS30720 7; H80CS47461 7; H80CS29030 7 |
| REPORTINGYEAR | other | 1 | 0 | 2025 1.4K |
| HEALTHCENTERNAME | who | 1.3K | 0 | KOSRAE COMMUNITY HEALTH C 7; CHUUK STATE DEPARTMENT OF 7; SEWARD COMMUNITY HEALTH C 7; MATTAWA COMMUNITY MEDICAL 7 |
| HEALTHCENTERSTREETADDRESS | id | 1.3K | 0 | Suite 101 KDC Building 7; NANTAKU, Weno Dhs Bldg 7; 417 1ST AVE 7; 210 GOVERNMENT RD 7 |
| HEALTHCENTEROTHERADDRESS | category | 3 | 0 | - 1.4K; A 1; 100 1 |
| HEALTHCENTERCITY | other | 946 | 0 | Los Angeles 29; Chicago 21; New York 15; Houston 13 |
| HEALTHCENTERSTATE | state | 59 | 0 | CA 170; TX 71; NY 64; OH 51 |
| HEALTHCENTERZIPCODE | other | 1.2K | 0 | 85012 9; - 8; 97470 8; 99615 8 |
| PROJECTDIRECTOR | id | 1.3K | 0 | Nena  Tolenoa 7; Inouefich  Shomour 7; Jilian  Chapman 7; Dana  Fox 7 |
| PROJECTDIRECTORPHONE | id | 1.4K | 0 | (691)370-2011 7; (691)330-7069 7; (907)224-8511 7; (509)932-4499 7 |
| PROJECTDIRECTORPHONEEXT | other | 203 | 0 | - 1.1K; 222 5; 1001 4; 102 3 |
| PROJECTDIRECTORFAX | who | 707 | 0 | - 653; (691)370-3000 4; (907)224-8501 4; (509)932-5363 4 |
| PROJECTDIRECTOREMAIL | id | 1.4K | 0 | ntolenoa@kosraechc.org 7; harushima81@gmail.com 7; jchapman@sewardhealthcent 7; dfox@mattwaclinic.net 7 |
| FUNDINGCHC | category | 2 | 0 | True 1.3K; False 66 |
| FUNDINGMSAW | category | 2 | 0 | False 1.2K; True 174 |
| FUNDINGHP | category | 2 | 0 | False 1.1K; True 298 |
| FUNDINGRPH | category | 2 | 0 | False 1.2K; True 106 |
| URBANRURALFLAG | category | 2 | 0 | Urban 787; Rural 569 |
| _INGESTED_AT | audit | 1 | 0 | 1785966223460403 1.4K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 0d132174-239a-41fd-a0f2-d 1.4K |
| _SRC_SHA256 | who | 1 | 0 | 1f8a7503f54892163a32083ec 1.4K |
