# PORTAL_ARC_HARRIS_COUNTY_OP_41FBA6BF22

rows 15  columns 124  scan 6.0s

roles: amount 9, audit 2, category 55, date 3, empty 29, other 20, who 7

## when

USER_SCH17
  1979         2  ####################
  1987         1  ##########
  1990         1  ##########
  1992         3  ##############################
  2000         1  ##########
  2004         2  ####################
  2007         1  ##########
  2008         2  ####################

USER_UPDAT
  2025        15  ##############################

INGESTED_AT
  2026        15  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 15 | 98.82 | 100 | 100 | 100 | 1.5K |
| X | 15 | -95.75 | -95.70 | -95.63 | -95.63 | -1.4K |
| Y | 15 | 29.71 | 29.81 | 29.87 | 29.87 | 447.25 |
| DISPLAYX | 15 | -95.75 | -95.70 | -95.63 | -95.63 | -1.4K |
| DISPLAYY | 15 | 29.71 | 29.81 | 29.87 | 29.87 | 447.26 |
| XMIN | 15 | -95.75 | -95.70 | -95.63 | -95.63 | -1.4K |

## who

CNTRYNAME by rows
        15  United States

CNTRYNAME by dollars
        1.5K       15 rows  United States

SUBREGION by rows
        15  Harris County

SUBREGION by dollars
        1.5K       15 rows  Harris County

USER_COU_1 by rows
        15  HARRIS COUNTY

USER_COU_1 by dollars
        1.5K       15 rows  HARRIS COUNTY

USER_DIS_2 by rows
        15  INDEPENDENT

USER_DIS_2 by dollars
        1.5K       15 rows  INDEPENDENT

## who x when

CNTRYNAME by USER_UPDAT, dollars = SCORE
  United States                             2025:1.5K

SUBREGION by USER_UPDAT, dollars = SCORE
  Harris County                             2025:1.5K

## what

OBJECTID: 15 8%, 14 8%, 13 8%, 12 8%, 11 8%, 10 8%, 9 8%, 8 8%, 7 8%, 6 8%, 5 8%, 4 8%

OBJECTID_1: 5044 8%, 5039 8%, 5027 8%, 5008 8%, 5001 8%, 4990 8%, 4989 8%, 4570 8%, 4549 8%, 4535 8%, 4512 8%, 4510 8%

MATCH_ADDR: 2502 N Mason Rd, Katy, Texas,  8%, 19711 Clay Rd, Katy, Texas, 77 8%, 2698 Greenhouse Rd, Houston, T 8%, 2498 N Mason Rd, Katy, Texas,  8%, 2700 Greenhouse Rd, Houston, T 8%, 21000 Franz Rd, Katy, Texas, 7 8%, 19202 Groschke Rd, Houston, Te 8%, 19315 Plantation Cove Ln, Katy 8%, 19790 Kieth Harrow Blvd, Katy, 8%, 14950 W Little York Rd, Housto 8%, 19802 Kieth Harrow Blvd, Katy, 8%, 6600 Addicks Satsuma Rd, Houst 8%

LONGLABEL: 2502 N Mason Rd, Katy, TX, 774 8%, 19711 Clay Rd, Katy, TX, 77449 8%, 2698 Greenhouse Rd, Houston, T 8%, 2498 N Mason Rd, Katy, TX, 774 8%, 2700 Greenhouse Rd, Houston, T 8%, 21000 Franz Rd, Katy, TX, 7744 8%, 19202 Groschke Rd, Houston, TX 8%, 19315 Plantation Cove Ln, Katy 8%, 19790 Kieth Harrow Blvd, Katy, 8%, 14950 W Little York Rd, Housto 8%, 19802 Kieth Harrow Blvd, Katy, 8%, 6600 Addicks Satsuma Rd, Houst 8%

SHORTLABEL: 2502 N Mason Rd 8%, 19711 Clay Rd 8%, 2698 Greenhouse Rd 8%, 2498 N Mason Rd 8%, 2700 Greenhouse Rd 8%, 21000 Franz Rd 8%, 19202 Groschke Rd 8%, 19315 Plantation Cove Ln 8%, 19790 Kieth Harrow Blvd 8%, 14950 W Little York Rd 8%, 19802 Kieth Harrow Blvd 8%, 6600 Addicks Satsuma Rd 8%

ADDR_TYPE: PointAddress 87%, StreetAddress 13%

PLACE_ADDR: 2502 N Mason Rd, Katy, Texas,  8%, 19711 Clay Rd, Katy, Texas, 77 8%, 2698 Greenhouse Rd, Houston, T 8%, 2498 N Mason Rd, Katy, Texas,  8%, 2700 Greenhouse Rd, Houston, T 8%, 21000 Franz Rd, Katy, Texas, 7 8%, 19202 Groschke Rd, Houston, Te 8%, 19315 Plantation Cove Ln, Katy 8%, 19790 Kieth Harrow Blvd, Katy, 8%, 14950 W Little York Rd, Housto 8%, 19802 Kieth Harrow Blvd, Katy, 8%, 6600 Addicks Satsuma Rd, Houst 8%

ADDNUM: 2502 8%, 19711 8%, 2698 8%, 2498 8%, 2700 8%, 21000 8%, 19202 8%, 19315 8%, 19790 8%, 14950 8%, 19802 8%, 6600 8%

ADDNUMFROM: 2560 50%, 14946 50%

ADDNUMTO: 2500 50%, 14956 50%

ADDRANGE: 2500-2560 50%, 14946-14956 50%

SIDE: L 50%, R 50%

STPREDIR: N 67%, W 33%

STNAME: Greenhouse 20%, Mason 13%, Kieth Harrow 13%, Clay 7%, Franz 7%, Groschke 7%, Plantation Cove 7%, Little York 7%, Addicks Satsuma 7%, Rio Bonito 7%, Alief Clodine 7%

STTYPE: Rd 80%, Blvd 13%, Ln 7%

STADDR: 2502 N Mason Rd 8%, 19711 Clay Rd 8%, 2698 Greenhouse Rd 8%, 2498 N Mason Rd 8%, 2700 Greenhouse Rd 8%, 21000 Franz Rd 8%, 19202 Groschke Rd 8%, 19315 Plantation Cove Ln 8%, 19790 Kieth Harrow Blvd 8%, 14950 W Little York Rd 8%, 19802 Kieth Harrow Blvd 8%, 6600 Addicks Satsuma Rd 8%

CITY: Katy 53%, Houston 47%

POSTAL: 77449 53%, 77084 33%, 77083 7%, 77082 7%

POSTALEXT: 3054 8%, 5740 8%, 4408 8%, 4079 8%, 4410 8%, 5729 8%, 5600 8%, 4842 8%, 7003 8%, 1523 8%, 7004 8%, 1520 8%

IN_ADDRESS: 2502 MASON RD 8%, 19711 CLAY RD 8%, 2698 GREENHOUSE RD 8%, 2498 N MASON RD 8%, 2700 GREENHOUSE RD 8%, 21000 FRANZ RD 8%, 19202 GROSCHKE RD 8%, 19315 PLANTATION COVE LN 8%, 19790 KIETH HARROW BLVD 8%, 14950 W LITTLE YORK RD 8%, 19802 KIETH HARROW BLVD 8%, 6600 ADDICKS SATSUMA RD 8%

IN_CITY: KATY 53%, HOUSTON 47%

IN_POSTAL: 77449 40%, 77084-4408 7%, 77084-4410 7%, 77084-5627 7%, 77449-7003 7%, 77084-1523 7%, 77449-7004 7%, 77084-1520 7%, 77083-1531 7%, 77082-4607 7%

USER_DISTR: '101914 47%, '101907 40%, '101903 13%

USER_DIS_1: KATY ISD 47%, CYPRESS-FAIRBANKS ISD 40%, ALIEF ISD 13%

USER_NCES: '4825170 47%, '4816110 40%, '4807830 13%

USER_DIS_3: P O BOX 159 47%, P O BOX 692003 40%, P O BOX 68 13%

USER_DIS_4: KATY 47%, HOUSTON 40%, ALIEF 13%

USER_DIS_6: 77492-0159 47%, 77269-2003 40%, 77411-0068 13%

USER_DIS_7: 6301 S STADIUM LN 47%, 11440 MATZKE RD 40%, 4250 COOK RD 13%

USER_DIS_8: KATY 47%, CYPRESS 40%, HOUSTON 13%

USER_DIS10: 77494-1057 47%, 77429 40%, 77072-1115 13%

USER_DIS11: (281) 396-6000 47%, (281) 897-4000 40%, (281) 498-8110 13%

USER_DIS12: (281) 644-1800 47%, (281) 897-4125 40%, (281) 988-3037 13%

USER_DIS13: kennethgregorski@katyisd.org 47%, superintendent@cfisd.net 40%, rachel.delafuente@aliefisd.net 13%

USER_DIS14: www.katyisd.org/ 47%, www.cfisd.net 40%, www.aliefisd.net 13%

USER_DIS15: DR KENNETH GREGORSKI 47%, DR DOUGLAS KILLIAN 40%, DR ANTHONY MAYS 13%

USER_DIS16: 96111 47%, 117927 40%, 38610 13%

USER_SCHOO: '101914130 8%, '101914125 8%, '101914111 8%, '101914049 8%, '101914043 8%, '101914009 8%, '101914005 8%, '101907150 8%, '101907132 8%, '101907113 8%, '101907050 8%, '101907048 8%

USER_SCH_1: MORTON RANCH EL 8%, JACK & SHARON RHOADS EL 8%, MAYDE CREEK EL 8%, MORTON RANCH J H 8%, MAYDE CREEK J H 8%, MORTON RANCH H S 8%, MAYDE CREEK H S 8%, MCFEE EL 8%, SHERIDAN EL 8%, HORNE EL 8%, THORNTON MIDDLE 8%, TRUITT MIDDLE 8%

USER_NCE_1: '482517011835 8%, '482517010766 8%, '482517005879 8%, '482517009613 8%, '482517005517 8%, '482517010759 8%, '482517006001 8%, '481611011260 8%, '481611001253 8%, '481611005437 8%, '481611004206 8%, '481611006843 8%

USER_SCH_2: 2502 MASON RD 8%, 19711 CLAY RD 8%, 2698 GREENHOUSE RD 8%, 2498 N MASON RD 8%, 2700 GREENHOUSE RD 8%, 21000 FRANZ RD 8%, 19202 GROSCHKE RD 8%, 19315 PLANTATION COVE LN 8%, 19790 KIETH HARROW BLVD 8%, 14950 W LITTLE YORK RD 8%, 19802 KIETH HARROW BLVD 8%, 6600 ADDICKS SATSUMA RD 8%

USER_SCH_3: KATY 53%, HOUSTON 47%

USER_SCH_5: 77449 40%, 77084-4408 7%, 77084-4410 7%, 77084-5627 7%, 77449-7003 7%, 77084-1523 7%, 77449-7004 7%, 77084-1520 7%, 77083-1531 7%, 77082-4607 7%

USER_SCH_6: 2502 MASON RD 8%, 19711 CLAY RD 8%, 2698 GREENHOUSE RD 8%, 2498 N MASON RD 8%, 2700 GREENHOUSE RD 8%, 21000 FRANZ RD 8%, 19202 GROSCHKE RD 8%, 19315 PLANTATION COVE LN 8%, 19790 KIETH HARROW BLVD 8%, 14950 W LITTLE YORK RD 8%, 19802 KIETH HARROW BLVD 8%, 6600 ADDICKS SATSUMA RD 8%

USER_SCH_7: KATY 53%, HOUSTON 47%

USER_SCH_9: 77449 40%, 77084-4408 7%, 77084-4410 7%, 77084-5627 7%, 77449-7003 7%, 77084-1523 7%, 77449-7004 7%, 77084-1520 7%, 77083-1531 7%, 77082-4607 7%

USER_SCH10: (281) 234-0300 8%, (281) 237-8500 8%, (281) 237-3950 8%, (281) 237-7400 8%, (281) 237-3900 8%, (281) 237-7800 8%, (281) 237-3063 8%, (281) 463-5380 8%, (281) 856-1420 8%, (281) 463-5954 8%, (281) 856-1500 8%, (281) 856-1100 8%

USER_SCH11: (281) 644-1685 8%, (281) 644-1590 8%, (281) 644-1555 8%, (281) 644-1670 8%, (281) 644-1650 8%, (281) 644-1746 8%, (281) 644-1718 8%, (281) 463-5680 8%, (281) 856-1461 8%, (281) 856-1451 8%, (281) 345-3160 8%, (281) 856-1104 8%

USER_SCH12: LORIAMAURER@katyisd.org 8%, timothydwolff@katyisd.org 8%, FeliciaAAshabranner@KATYISD.OR 8%, frederickjblack@katyisd.org 8%, amandasweaver@KATYISD.ORG 8%, julieahinson@katyisd.org 8%, elizabethlherring@katyisd.org 8%, sharon.whitfield@cfisd.net 8%, rene.mcintyre@cfisd.net 8%, tracey.bennett@cfisd.net 8%, reginal2.mitchell@cfisd.net 8%, plas.williams@cfisd.net 8%

USER_SCH13: www.katyisd.org/ 43%, www.cfisd.net 43%, www.aliefisd.net 14%

USER_SCH14: LORI MAURER 8%, MR TIMOTHY WOLFF 8%, MRS FELICIA ASHABRANNER 8%, DR FREDERICK BLACK 8%, MS AMANDA WEAVER 8%, JULIE HINSON 8%, MS ELIZABETH HERRING 8%, MS SHARON WHITFIELD 8%, MS RENE MCINTYRE 8%, MS TRACEY BENNETT 8%, REGINALD MITCHELL 8%, DR PLAS WILLIAMS 8%

USER_GRADE: 'EE-05 33%, '06-08 27%, '09-12 20%, 'PK-05 7%, 'EE-04 7%, '07-08 7%

USER_SCH15: 1214 15%, 969 8%, 703 8%, 816 8%, 1205 8%, 2944 8%, 3036 8%, 961 8%, 919 8%, 908 8%, 1424 8%, 1353 8%

SCHOOL_TYP: Elementary School 47%, Middle School 27%, High School 20%, Junior High School 7%

GEOMETRY: {"type": "Point", "coordinates 20%, {"type": "Point", "coordinates 13%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 15 | 0 | 15 1; 14 1; 13 1; 12 1 |
| OBJECTID_1 | category | 15 | 0 | 5044 1; 5039 1; 5027 1; 5008 1 |
| STATUS | other | 1 | 0 | M 15 |
| SCORE | amount | 3 | 0 | 100.0 12; 98.82 2; 99.55 1 |
| MATCH_TYPE | other | 1 | 0 | A 15 |
| MATCH_ADDR | category | 15 | 0 | 2502 N Mason Rd, Katy, Te 1; 19711 Clay Rd, Katy, Texa 1; 2698 Greenhouse Rd, Houst 1; 2498 N Mason Rd, Katy, Te 1 |
| LONGLABEL | category | 15 | 0 | 2502 N Mason Rd, Katy, TX 1; 19711 Clay Rd, Katy, TX,  1; 2698 Greenhouse Rd, Houst 1; 2498 N Mason Rd, Katy, TX 1 |
| SHORTLABEL | category | 15 | 0 | 2502 N Mason Rd 1; 19711 Clay Rd 1; 2698 Greenhouse Rd 1; 2498 N Mason Rd 1 |
| ADDR_TYPE | category | 2 | 0 | PointAddress 13; StreetAddress 2 |
| TYPE | empty | 1 | 15 |  |
| PLACENAME | empty | 1 | 15 |  |
| PLACE_ADDR | category | 15 | 0 | 2502 N Mason Rd, Katy, Te 1; 19711 Clay Rd, Katy, Texa 1; 2698 Greenhouse Rd, Houst 1; 2498 N Mason Rd, Katy, Te 1 |
| PHONE | empty | 1 | 15 |  |
| URL | empty | 1 | 15 |  |
| RANK | other | 1 | 0 | 20 15 |
| ADDBLDG | empty | 1 | 15 |  |
| ADDNUM | category | 15 | 0 | 2502 1; 19711 1; 2698 1; 2498 1 |
| ADDNUMFROM | category | 3 | 13 | 2560 1; 14946 1 |
| ADDNUMTO | category | 3 | 13 | 2500 1; 14956 1 |
| ADDRANGE | category | 3 | 13 | 2500-2560 1; 14946-14956 1 |
| SIDE | category | 3 | 13 | L 1; R 1 |
| STPREDIR | category | 3 | 12 | N 2; W 1 |
| STPRETYPE | empty | 1 | 15 |  |
| STNAME | category | 11 | 0 | Greenhouse 3; Mason 2; Kieth Harrow 2; Clay 1 |
| STTYPE | category | 3 | 0 | Rd 12; Blvd 2; Ln 1 |
| STDIR | empty | 1 | 15 |  |
| BLDGTYPE | empty | 1 | 15 |  |
| BLDGNAME | empty | 1 | 15 |  |
| LEVELTYPE | empty | 1 | 15 |  |
| LEVELNAME | empty | 1 | 15 |  |
| UNITTYPE | empty | 1 | 15 |  |
| UNITNAME | empty | 1 | 15 |  |
| SUBADDR | empty | 1 | 15 |  |
| STADDR | category | 15 | 0 | 2502 N Mason Rd 1; 19711 Clay Rd 1; 2698 Greenhouse Rd 1; 2498 N Mason Rd 1 |
| BLOCK | empty | 1 | 15 |  |
| SECTOR | empty | 1 | 15 |  |
| NBRHD | empty | 1 | 15 |  |
| DISTRICT | empty | 1 | 15 |  |
| CITY | category | 2 | 0 | Katy 8; Houston 7 |
| METROAREA | empty | 1 | 15 |  |
| SUBREGION | who | 1 | 0 | Harris County 15 |
| REGION | other | 1 | 0 | Texas 15 |
| REGIONABBR | other | 1 | 0 | TX 15 |
| TERRITORY | empty | 1 | 15 |  |
| ZONE | empty | 1 | 15 |  |
| POSTAL | category | 4 | 0 | 77449 8; 77084 5; 77083 1; 77082 1 |
| POSTALEXT | category | 15 | 0 | 3054 1; 5740 1; 4408 1; 4079 1 |
| COUNTRY | other | 1 | 0 | USA 15 |
| CNTRYNAME | who | 1 | 0 | United States 15 |
| LANGCODE | other | 1 | 0 | ENG 15 |
| DISTANCE | other | 1 | 0 | 0 15 |
| X | amount | 13 | 0 | -95.70390929324046 2; -95.71565247945644 2; -95.75194669256044 1; -95.71610697377228 1 |
| Y | amount | 13 | 0 | 29.80702563197529 2; 29.84722407972141 2; 29.809636473293963 1; 29.831094875584792 1 |
| DISPLAYX | amount | 12 | 0 | -95.6981925 3; -95.7155985 2; -95.75194669256044 1; -95.7161115 1 |
| DISPLAYY | amount | 12 | 0 | 29.807046 3; 29.847915 2; 29.809636473293963 1; 29.83031100000001 1 |
| XMIN | amount | 12 | 0 | -95.69919250000001 3; -95.7165985 2; -95.75294669256044 1; -95.7171115 1 |
| XMAX | amount | 12 | 0 | -95.6971925 3; -95.7145985 2; -95.75094669256043 1; -95.71511149999999 1 |
| YMIN | amount | 12 | 0 | 29.806046 3; 29.846915 2; 29.808636473293962 1; 29.829311000000008 1 |
| YMAX | amount | 12 | 0 | 29.808046 3; 29.848915 2; 29.810636473293965 1; 29.83131100000001 1 |
| EXINFO | empty | 1 | 15 |  |
| IN_ADDRESS | category | 15 | 0 | 2502 MASON RD 1; 19711 CLAY RD 1; 2698 GREENHOUSE RD 1; 2498 N MASON RD 1 |
| IN_ADDRE_1 | empty | 1 | 15 |  |
| IN_ADDRE_2 | empty | 1 | 15 |  |
| IN_NEIGHBO | empty | 1 | 15 |  |
| IN_CITY | category | 2 | 0 | KATY 8; HOUSTON 7 |
| IN_SUBREGI | empty | 1 | 15 |  |
| IN_REGION | other | 1 | 0 | TX 15 |
| IN_POSTAL | category | 10 | 0 | 77449 6; 77084-4408 1; 77084-4410 1; 77084-5627 1 |
| IN_POSTALE | empty | 1 | 15 |  |
| IN_COUNTRY | empty | 1 | 15 |  |
| USER_COUNT | other | 1 | 0 | '101 15 |
| USER_COU_1 | who | 1 | 0 | HARRIS COUNTY 15 |
| USER_ESC_R | other | 1 | 0 | '04 15 |
| USER_ESC_1 | other | 1 | 0 | '04 15 |
| USER_ESC_2 | other | 1 | 0 | '04 15 |
| USER_DISTR | category | 3 | 0 | '101914 7; '101907 6; '101903 2 |
| USER_DIS_1 | category | 3 | 0 | KATY ISD 7; CYPRESS-FAIRBANKS ISD 6; ALIEF ISD 2 |
| USER_DIS_2 | who | 1 | 0 | INDEPENDENT 15 |
| USER_NCES | category | 3 | 0 | '4825170 7; '4816110 6; '4807830 2 |
| USER_DIS_3 | category | 3 | 0 | P O BOX 159 7; P O BOX 692003 6; P O BOX 68 2 |
| USER_DIS_4 | category | 3 | 0 | KATY 7; HOUSTON 6; ALIEF 2 |
| USER_DIS_5 | other | 1 | 0 | TX 15 |
| USER_DIS_6 | category | 3 | 0 | 77492-0159 7; 77269-2003 6; 77411-0068 2 |
| USER_DIS_7 | category | 3 | 0 | 6301 S STADIUM LN 7; 11440 MATZKE RD 6; 4250 COOK RD 2 |
| USER_DIS_8 | category | 3 | 0 | KATY 7; CYPRESS 6; HOUSTON 2 |
| USER_DIS_9 | other | 1 | 0 | TX 15 |
| USER_DIS10 | category | 3 | 0 | 77494-1057 7; 77429 6; 77072-1115 2 |
| USER_DIS11 | category | 3 | 0 | (281) 396-6000 7; (281) 897-4000 6; (281) 498-8110 2 |
| USER_DIS12 | category | 3 | 0 | (281) 644-1800 7; (281) 897-4125 6; (281) 988-3037 2 |
| USER_DIS13 | category | 3 | 0 | kennethgregorski@katyisd. 7; superintendent@cfisd.net 6; rachel.delafuente@aliefis 2 |
| USER_DIS14 | category | 3 | 0 | www.katyisd.org/ 7; www.cfisd.net 6; www.aliefisd.net 2 |
| USER_DIS15 | category | 3 | 0 | DR KENNETH GREGORSKI 7; DR DOUGLAS KILLIAN 6; DR ANTHONY MAYS 2 |
| USER_DIS16 | category | 3 | 0 | 96111 7; 117927 6; 38610 2 |
| USER_SCHOO | category | 15 | 0 | '101914130 1; '101914125 1; '101914111 1; '101914049 1 |
| USER_SCH_1 | category | 15 | 0 | MORTON RANCH EL 1; JACK & SHARON RHOADS EL 1; MAYDE CREEK EL 1; MORTON RANCH J H 1 |
| USER_INSTR | who | 1 | 0 | REGULAR INSTRUCTIONAL 15 |
| USER_CHART | empty | 1 | 15 |  |
| USER_AEA | other | 1 | 0 | N 15 |
| USER_MAGNE | other | 1 | 0 | N 15 |
| USER_RESID | other | 1 | 0 | N 15 |
| USER_NCE_1 | category | 15 | 0 | '482517011835 1; '482517010766 1; '482517005879 1; '482517009613 1 |
| USER_SCH_2 | category | 15 | 0 | 2502 MASON RD 1; 19711 CLAY RD 1; 2698 GREENHOUSE RD 1; 2498 N MASON RD 1 |
| USER_SCH_3 | category | 2 | 0 | KATY 8; HOUSTON 7 |
| USER_SCH_4 | other | 1 | 0 | TX 15 |
| USER_SCH_5 | category | 10 | 0 | 77449 6; 77084-4408 1; 77084-4410 1; 77084-5627 1 |
| USER_SCH_6 | category | 15 | 0 | 2502 MASON RD 1; 19711 CLAY RD 1; 2698 GREENHOUSE RD 1; 2498 N MASON RD 1 |
| USER_SCH_7 | category | 2 | 0 | KATY 8; HOUSTON 7 |
| USER_SCH_8 | other | 1 | 0 | TX 15 |
| USER_SCH_9 | category | 10 | 0 | 77449 6; 77084-4408 1; 77084-4410 1; 77084-5627 1 |
| USER_SCH10 | category | 15 | 0 | (281) 234-0300 1; (281) 237-8500 1; (281) 237-3950 1; (281) 237-7400 1 |
| USER_SCH11 | category | 15 | 0 | (281) 644-1685 1; (281) 644-1590 1; (281) 644-1555 1; (281) 644-1670 1 |
| USER_SCH12 | category | 15 | 0 | LORIAMAURER@katyisd.org 1; timothydwolff@katyisd.org 1; FeliciaAAshabranner@KATYI 1; frederickjblack@katyisd.o 1 |
| USER_SCH13 | category | 4 | 1 | www.katyisd.org/ 6; www.cfisd.net 6; www.aliefisd.net 2 |
| USER_SCH14 | category | 15 | 0 | LORI MAURER 1; MR TIMOTHY WOLFF 1; MRS FELICIA ASHABRANNER 1; DR FREDERICK BLACK 1 |
| USER_GRADE | category | 6 | 0 | 'EE-05 5; '06-08 4; '09-12 3; 'PK-05 1 |
| USER_SCH15 | category | 14 | 0 | 1214 2; 969 1; 703 1; 816 1 |
| USER_SCH16 | who | 1 | 0 | Active 15 |
| USER_SCH17 | date | 12 | 2 | 06/02/2004 2; 07/01/1992 2; 07/30/2008 1; 01/29/2000 1 |
| USER_UPDAT | date | 3 | 0 | 3/11/2025 5:38:01 AM 7; 3/11/2025 5:38:00 AM 7; 3/11/2025 5:37:59 AM 1 |
| SCHOOL_TYP | category | 4 | 0 | Elementary School 7; Middle School 4; High School 3; Junior High School 1 |
| GEOMETRY | category | 12 | 0 | {"type": "Point", "coordi 3; {"type": "Point", "coordi 2; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:14:11.47357 15 |
| SOURCE_RUN_ID | audit | 1 | 0 | 743af858-241c-46b4-bf1f-f 15 |
| SRC_SHA256 | who | 1 | 0 | 1f7f3d391e968eb09d25d5649 15 |
