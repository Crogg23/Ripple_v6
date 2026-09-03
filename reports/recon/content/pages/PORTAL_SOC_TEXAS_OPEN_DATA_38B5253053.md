# PORTAL_SOC_TEXAS_OPEN_DATA_38B5253053

rows 2.0K  columns 16  scan 3.1s

roles: audit 2, category 7, date 2, other 2, who 4

## when

WST_STATUS_CD_DT
  2011         2  
  2013         3  
  2014         8  
  2015         4  
  2016         1  
  2017         9  
  2018        10  
  2019         6  
  2020         6  
  2021        11  
  2022         3  
  2023       133  #####
  2024       851  ##############################
  2025        48  ##
  2026         1  

INGESTED_AT
  2026      2.0K  ##############################

## who

WST_DESC_TXT by rows
       419  A mixed lab pack that consists of various spent and unspent chemicals 
        83  RCRA Hazardous Pharmaceuticals
        43  UNUSED CAUSTIC PRODUCT FOR DISPOSAL; EPISODIC GENERATION
        32  TOXIC SOLIDS
        31  SY Rags and Wipes Contaminated with Chlorinated Solvents
        30  TOXIC LIQUIDS
        28  FLAMMABLE SOLIDS
        26  Retail/clinical/hospital generated pharmaceutical products(includes sc
        24  Hazardous pharmaceutical waste.; The waste is exempted from regulation
        23  ITEMS CONTAINING ACIDIC/CORROSIVE LIQUIDS THAT ARE DAMAGED, RECALLED, 
        22  Waste Medicine Liquid Flamamble, Toxic
        20  Hazardous and universal waste generated during the course of day to da
        20  FLAMMABLE LIQUIDS
        20  Medicine Liquids
        20  Medicine Solids
        19  Old, outdated, expired, compounded pharmaceutical drugs, including tho
        18  P LISTED LAB PACKS
        17  LAB PACK LOOSE PACKED PHARMACEUTICALS
        16  Lab pack waste - stored and picked up by Stericycle
        15  HALOGENATED SOLVENTS FROM LAB PROCESSES

TX_WST_CD by rows
       426  0001003H
        83  0020005H
        47  0012409H
        44  0007119H
        32  0008409H
        31  1065407H
        31  0009219H
        26  7777005H
        25  0002801H
        24  0003004H
        23  0001105H
        22  0001201H
        22  0001409H
        21  0014219H
        20  0013009H
        20  0004211H
        18  0017004H
        18  0042004H
        17  0041004H
        17  0010004H

NAICS_CD by rows
       465  611310
       311  622110
       179  455211
       117  452112
        87  325199
        51  332721
        41  488999
        39  484122
        36  493110
        34  492110
        32  339999
        31  325211
        26  488210
        26  486910
        26  424210
        25  324110
        22  332813
        20  562111
        18  541380
        18  213112

SRC_SHA256 by rows
      2.0K  8608468cf33369c584e9d6ad11bf5602ca12c7bca95e51928d6efea43238bb04

## who x when

WST_DESC_TXT by WST_STATUS_CD_DT
  FLAMMABLE SOLIDS                          2025:6
  Hazardous and universal waste generated   2024:20
  Hazardous pharmaceutical waste.; The was  2024:24
  Medicine Liquids                          2024:20
  Medicine Solids                           2024:20
  Old, outdated, expired, compounded pharm  2024:19
  RCRA Hazardous Pharmaceuticals            2023:83
  Retail/clinical/hospital generated pharm  2024:26
  SY Rags and Wipes Contaminated with Chlo  2023:31
  UNUSED CAUSTIC PRODUCT FOR DISPOSAL; EPI  2024:43
  Waste Medicine Liquid Flamamble, Toxic    2024:22

TX_WST_CD by WST_STATUS_CD_DT
  0001003H                                  2024:1
  0001201H                                  2024:20
  0002801H                                  2024:25
  0003004H                                  2024:24
  0007119H                                  2024:44
  0009219H                                  2024:1
  0010004H                                  2024:17
  0012409H                                  2024:41 2025:6
  0013009H                                  2024:20
  0014219H                                  2024:21
  0017004H                                  2024:2
  0020005H                                  2023:83
  1065407H                                  2023:31
  7777005H                                  2024:26

## what

EPA_FORM_CD: W004 34%, W001 16%, W219 10%, W409 8%, W119 8%, W005 7%, W319 4%, W203 4%, W801 3%, W110 2%, W204 2%, W211 2%

WST_STATUS_CD: ACTIVE 71%, INACTIVE 29%

ORIGIN_CD: 1 93%, 2 5%, 4 1%, nan 0%, 5 0%, 6 0%, 7 0%

WST_SOURCE_CD: G22 30%, G11 26%, G09 14%, G19 9%, G41 4%, G13 4%, G32 3%, G01 3%, G16 2%, G06 2%, G76 1%, G07 1%

WST_RADIOACT_FLG: False 100%, True 0%

NEW_CHEM_SUBST_FLG: False 97%, True 3%

WST_MGMT_LOC_CD: True 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SWR_NUM_TXT | other | 208 | 0 | 74723 457; 90961 117; 97272 105; 89204 100 |
| TX_WST_CD | who | 463 | 0 | 0001003H 426; 0020005H 87; 0012409H 47; 0007119H 44 |
| EPA_WASTE_CODE | other | 438 | 0 | D001 278; D002 151; D008 69; D018 66 |
| EPA_FORM_CD | category | 39 | 0 | W004 559; W001 258; W219 171; W409 140 |
| WST_STATUS_CD | category | 2 | 0 | ACTIVE 1.4K; INACTIVE 587 |
| WST_STATUS_CD_DT | date | 75 | 0 | nan 904; 2024-08-19T00:00:00.000 131; 2024-08-22T00:00:00.000 123; 2024-08-08T00:00:00.000 96 |
| WST_DESC_TXT | who | 496 | 0 | A mixed lab pack that con 419; RCRA Hazardous Pharmaceut 87; UNUSED CAUSTIC PRODUCT FO 43; TOXIC SOLIDS 32 |
| ORIGIN_CD | category | 7 | 0 | 1 1.9K; 2 107; 4 26; nan 3 |
| WST_SOURCE_CD | category | 26 | 0 | G22 578; G11 497; G09 272; G19 176 |
| NAICS_CD | who | 105 | 0 | 611310 465; 622110 311; 455211 179; 452112 117 |
| WST_RADIOACT_FLG | category | 2 | 0 | False 2.0K; True 1 |
| NEW_CHEM_SUBST_FLG | category | 3 | 9 | False 1.9K; True 52 |
| WST_MGMT_LOC_CD | category | 2 | 1.6K | True 413 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:45:44.33720 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 3fa5d651-135a-4eca-a03d-b 2.0K |
| SRC_SHA256 | who | 1 | 0 | 8608468cf33369c584e9d6ad1 2.0K |
