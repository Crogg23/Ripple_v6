# PORTAL_SOC_TEXAS_OPEN_DATA_24C81C0C8A

rows 2.0K  columns 17  scan 2.4s

roles: audit 2, category 8, date 2, id 1, other 4, who 1

## when

WST_STATUS_CD_DT
  2011         3  #
  2012        82  ##############################
  2013        52  ###################
  2014        50  ##################
  2015        70  ##########################
  2016        53  ###################
  2017        56  ####################
  2018        58  #####################
  2019        52  ###################
  2020        58  #####################
  2021        52  ###################
  2022        62  #######################
  2023        59  ######################
  2024        48  ##################
  2025        47  #################
  2026         1  

INGESTED_AT
  2026      2.0K  ##############################

## who

SRC_SHA256 by rows
      2.0K  79b6e13eee4e5275595b57cb358ee49b659f354a5d79cc18265eef6ee528ba86

## who x when

SRC_SHA256 by WST_STATUS_CD_DT
  79b6e13eee4e5275595b57cb358ee49b659f354a  2011:3 2012:82 2013:52 2014:50 2015:70 2016:53 2017:56 2018:58 2019:52 2020:58 2021:52 2022:62 2023:59 2024:48 2025:47 2026:1

## what

EPA_FORM_CD: nan 60%, W219 8%, W001 7%, W319 4%, W409 4%, W203 4%, W801 3%, W211 3%, W110 2%, W209 2%, W119 2%, W310 2%

WST_STATUS_CD: INACTIVE 58%, ACTIVE 36%, nan 6%

ORIGIN_CD: 1 86%, 2 8%, 7 2%, 3 1%, 5 1%, 4 1%, nan 1%, 6 0%

WST_SOURCE_CD: nan 56%, G11 18%, G09 8%, G19 4%, G06 3%, G32 3%, G22 2%, G13 1%, G16 1%, G02 1%, G01 1%, G07 1%

WST_RADIOACT_FLG: False 100%, True 0%

NEW_CHEM_SUBST_FLG: False 91%, True 9%

WST_MGMT_LOC_CD: True 100%

SYS_TYP_CD: nan 99%, H14 1%, H02 0%, H03 0%, H10 0%, H06 0%, H12 0%, H13 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SWR_NUM_TXT | other | 1.6K | 0 | 30694 12; 30137 12; 34240 11; 31547 11 |
| TX_WST_CD | other | 1.7K | 0 | 0501203H 20; 0001203H 13; 0001801H 12; 0015001H 12 |
| EPA_FORM_CD | category | 45 | 0 | nan 1.0K; W219 130; W001 124; W319 69 |
| WST_STATUS_CD | category | 3 | 0 | INACTIVE 1.2K; ACTIVE 714; nan 121 |
| WST_STATUS_CD_DT | date | 616 | 0 | nan 1.2K; 2019-03-18T00:00:00.000 7; 2020-10-14T00:00:00.000 6; 2022-05-25T00:00:00.000 6 |
| WST_DESC_TXT | other | 1.7K | 0 | nan 172; UNSTRIPPER RAFFINATE; A n 10; Paint booth filters/Paint 10; Toxic solids, organic, n. 10 |
| ORIGIN_CD | category | 8 | 0 | 1 1.7K; 2 166; 7 31; 3 29 |
| WST_SOURCE_CD | category | 29 | 0 | nan 1.0K; G11 345; G09 146; G19 84 |
| NAICS_CD | other | 220 | 0 | nan 1.1K; 444110 155; 325199 56; 446110 52 |
| WST_RADIOACT_FLG | category | 2 | 0 | False 2.0K; True 3 |
| NEW_CHEM_SUBST_FLG | category | 3 | 20 | False 1.8K; True 175 |
| TWC_ID | id | 2.0K | 0 | 211132 10; 136865 10; 350304 10; 151342 10 |
| WST_MGMT_LOC_CD | category | 2 | 1.7K | True 334 |
| SYS_TYP_CD | category | 8 | 0 | nan 2.0K; H14 11; H02 2; H03 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:46:25.43714 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | def1a96e-80ac-4e62-af7d-b 2.0K |
| SRC_SHA256 | who | 1 | 0 | 79b6e13eee4e5275595b57cb3 2.0K |
