# PORTAL_ARC_HARRIS_COUNTY_OP_E68ADDC07C

rows 33  columns 122  scan 6.9s

roles: amount 11, audit 2, category 65, date 2, empty 24, other 15, who 4

## when

USER_UPDAT
  2023        33  ##############################

INGESTED_AT
  2026        33  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 33 | 95.47 | 100 | 100 | 100 | 3.3K |
| DISTANCE | 33 | 0 | 0 | 203.4K | 299.2K | 299.2K |
| X | 33 | -95.79 | -95.74 | -95.68 | -95.68 | -3.2K |
| Y | 33 | 29.74 | 29.80 | 29.83 | 29.83 | 983.35 |
| DISPLAYX | 33 | -95.79 | -95.74 | -95.68 | -95.68 | -3.2K |
| DISPLAYY | 33 | 29.74 | 29.80 | 29.83 | 29.83 | 983.34 |

## who

SUBREGION by rows
        33  Harris County

SUBREGION by dollars
        3.3K       33 rows  Harris County

USER_INSTR by rows
        33  REGULAR INSTRUCTIONAL

USER_INSTR by dollars
        3.3K       33 rows  REGULAR INSTRUCTIONAL

USER_SCH16 by rows
        33  Active

USER_SCH16 by dollars
        3.3K       33 rows  Active

SRC_SHA256 by rows
        33  e3c6519302382b54916f5ab77298abfa0fe597b21ebd112938fa8ca7aebe24c1

SRC_SHA256 by dollars
        3.3K       33 rows  e3c6519302382b54916f5ab77298abfa0fe597b21ebd112938fa8ca7aebe

## who x when

SUBREGION by USER_UPDAT, dollars = SCORE
  Harris County                             2023:3.3K

USER_INSTR by USER_UPDAT, dollars = SCORE
  REGULAR INSTRUCTIONAL                     2023:3.3K

## what

FID: 33 8%, 32 8%, 31 8%, 30 8%, 29 8%, 28 8%, 27 8%, 26 8%, 25 8%, 24 8%, 23 8%, 22 8%

OBJECTID: 5024 8%, 5000 8%, 4997 8%, 4994 8%, 4993 8%, 4992 8%, 4989 8%, 4987 8%, 4986 8%, 4984 8%, 4983 8%, 4982 8%

MATCH_ADDR: 20625 Clay Rd, Katy, Texas, 77 14%, 24406 Franz Rd, Katy, Texas, 7 14%, 2602 Winchester Ranch Trl, Kat 7%, 2502 N Mason Rd, Katy, Texas,  7%, 2715 Fry Rd, Katy, Texas, 7744 7%, 2751 N Westgreen Blvd, Katy, T 7%, 19711 Clay Rd, Katy, Texas, 77 7%, 18605 Green Land Way, Houston, 7%, 1901 Charlton House Ln, Katy,  7%, 19910 Stonelodge Dr, Katy, Tex 7%, 21203 Park Timbers Ln, Katy, T 7%, 3535 Fry Rd, Katy, Texas, 7744 7%

LONGLABEL: 20625 Clay Rd, Katy, TX, 77449 14%, 24406 Franz Rd, Katy, TX, 7749 14%, 2602 Winchester Ranch Trl, Kat 7%, 2502 N Mason Rd, Katy, TX, 774 7%, 2715 Fry Rd, Katy, TX, 77449,  7%, 2751 N Westgreen Blvd, Katy, T 7%, 19711 Clay Rd, Katy, TX, 77449 7%, 18605 Green Land Way, Houston, 7%, 1901 Charlton House Ln, Katy,  7%, 19910 Stonelodge Dr, Katy, TX, 7%, 21203 Park Timbers Ln, Katy, T 7%, 3535 Fry Rd, Katy, TX, 77449,  7%

SHORTLABEL: 20625 Clay Rd 14%, 24406 Franz Rd 14%, 2602 Winchester Ranch Trl 7%, 2502 N Mason Rd 7%, 2715 Fry Rd 7%, 2751 N Westgreen Blvd 7%, 19711 Clay Rd 7%, 18605 Green Land Way 7%, 1901 Charlton House Ln 7%, 19910 Stonelodge Dr 7%, 21203 Park Timbers Ln 7%, 3535 Fry Rd 7%

ADDR_TYPE: PointAddress 82%, StreetAddress 12%, StreetAddressExt 6%

PLACE_ADDR: 20625 Clay Rd, Katy, Texas, 77 14%, 24406 Franz Rd, Katy, Texas, 7 14%, 2602 Winchester Ranch Trl, Kat 7%, 2502 N Mason Rd, Katy, Texas,  7%, 2715 Fry Rd, Katy, Texas, 7744 7%, 2751 N Westgreen Blvd, Katy, T 7%, 19711 Clay Rd, Katy, Texas, 77 7%, 18605 Green Land Way, Houston, 7%, 1901 Charlton House Ln, Katy,  7%, 19910 Stonelodge Dr, Katy, Tex 7%, 21203 Park Timbers Ln, Katy, T 7%, 3535 Fry Rd, Katy, Texas, 7744 7%

ADDNUM: 21203 12%, 3535 12%, 20625 12%, 24406 12%, 2602 6%, 2502 6%, 2715 6%, 2751 6%, 19711 6%, 18605 6%, 1901 6%, 19910 6%

ADDNUMFROM: 24398 33%, 2500 17%, 20957 17%, 22499 17%, 19290 17%

ADDNUMTO: 24348 33%, 2572 17%, 21003 17%, 22301 17%, 19200 17%

ADDRANGE: 24348-24398 33%, 2500-2572 17%, 20957-21003 17%, 22301-22499 17%, 19200-19290 17%

SIDE: L 67%, R 33%

STPREDIR: N 75%, S 25%

STNAME: Clay 14%, Franz 14%, Mason 9%, Fry 9%, Lakes of Bridgewater 9%, Greenhouse 9%, Kingsland 9%, Provincial 9%, Winchester Ranch 5%, Westgreen 5%, Green Land 5%, Charlton House 5%

STTYPE: Rd 45%, Blvd 15%, Dr 15%, Ln 9%, Trl 3%, Way 3%, St 3%, Pkwy 3%, Fwy 3%

STADDR: 20625 Clay Rd 14%, 24406 Franz Rd 14%, 2602 Winchester Ranch Trl 7%, 2502 N Mason Rd 7%, 2715 Fry Rd 7%, 2751 N Westgreen Blvd 7%, 19711 Clay Rd 7%, 18605 Green Land Way 7%, 1901 Charlton House Ln 7%, 19910 Stonelodge Dr 7%, 21203 Park Timbers Ln 7%, 3535 Fry Rd 7%

NBRHD: West Memorial 100%

CITY: Katy 85%, Houston 15%

METROAREA: Houston-Galveston Metro Area 100%

POSTAL: 77449 42%, 77450 30%, 77493 12%, 77084 12%, 77094 3%

POSTALEXT: 5593 17%, 4179 8%, 3054 8%, 6380 8%, 5088 8%, 5740 8%, 3887 8%, 2669 8%, 5200 8%, 5372 8%, 8618 8%

EXINFO: DALLAS COUNTY 75%, 77494 25%

IN_ADDRESS: 20625 CLAY RD 14%, 24406 FRANZ RD 14%, 2602 WINCHESTER RANCH TRAIL 7%, 2502 MASON RD 7%, 2715 FRY RD 7%, 2751 N WESTGREEN BLVD 7%, 19711 CLAY RD 7%, 18605 GREEN LAND WAY 7%, 1901 CHARLTON HOUSE LN 7%, 19910 STONELODGE 7%, 21203 PARK TIMBERS 7%, 3535 N FRY RD 7%

IN_CITY: KATY 85%, HOUSTON 15%

IN_SUBREGI: HARRIS COUNTY 91%, DALLAS COUNTY 9%

IN_POSTAL: 77449 33%, 77493 17%, 77494 8%, 77449-3859 8%, 77084 4%, 77450-5200 4%, 77450-5372 4%, 77449-9999 4%, 77449-2898 4%, 77084-4408 4%, 77449-3398 4%, 77450-2797 4%

USER_COUNT: 101 91%, 57 9%

USER_COU_1: HARRIS COUNTY 91%, DALLAS COUNTY 9%

USER_ESC_R: 4 91%, 10 9%

USER_ESC_1: 4 91%, 10 9%

USER_ESC_2: 4 91%, 10 9%

USER_DISTR: 101914 85%, 57848 9%, 101837 6%

USER_DIS_1: KATY ISD 85%, INTERNATIONAL LEADERSHIP OF TE 9%, CALVIN NELMS CHARTER SCHOOLS 6%

USER_DIS_2: INDEPENDENT 85%, CHARTER 15%

USER_NCES: 4825170 85%, 4801440 9%, 4800124 6%

USER_DIS_3: P O BOX 159 85%, 2021 LAKESIDE BLVD 9%, 20625 CLAY RD 6%

USER_DIS_4: KATY 91%, RICHARDSON 9%

USER_DIS_6: 77492-0159 85%, 75082 9%, 77449 6%

USER_DIS_7: 6301 S STADIUM LN 85%, 2021 LAKESIDE BLVD 9%, 20625 CLAY RD 6%

USER_DIS_8: KATY 91%, RICHARDSON 9%

USER_DIS10: 77494-1057 85%, 75082 9%, 77449 6%

USER_DIS11: (281) 396-6000 85%, (972) 479-9078 9%, (281) 398-8031 6%

USER_DIS12: (281) 644-1800 85%, (972) 479-9129 9%, (281) 398-8032 6%

USER_DIS13: kennethgregorski@katyisd.org 85%, econger@iltexas.org 9%, MDean@cnchs.net 6%

USER_DIS14: www.katyisd.org/ 85%, www.iltexas.org/ 9%, WWW.cnchs.net 6%

USER_DIS15: DR KENNETH GREGORSKI 85%, MR EDWARD CONGER 9%, MR MICHAEL DEAN 6%

USER_DIS16: 92667 85%, 22139 9%, 313 6%

USER_SCHOO: 101914144 8%, 101914130 8%, 101914128 8%, 101914126 8%, 101914125 8%, 101914121 8%, 101914120 8%, 101914112 8%, 101914115 8%, 101914116 8%, 101914113 8%, 101914108 8%

USER_SCH_1: LEONARD EL 8%, MORTON RANCH EL 8%, URSULA STEPHENS EL 8%, FRANZ EL 8%, JACK & SHARON RHOADS EL 8%, JEAN & BETTY SCHMALZ EL 8%, ROBERT KING EL 8%, HAZEL S PATTISON EL 8%, JEANETTE HAYES EL 8%, MCROBERTS EL 8%, LORAINE T GOLBOW EL 8%, DIANE WINBORN EL 8%

USER_CHART: OPEN ENROLLMENT CHARTER 100%

USER_NCE_1: 482517013805 8%, 482517011835 8%, 482517010769 8%, 482517010767 8%, 482517010766 8%, 482517008628 8%, 482517008627 8%, 482517006724 8%, 482517007336 8%, 482517007641 8%, 482517006725 8%, 482517005753 8%

USER_SCH_2: 20625 CLAY RD 14%, 24406 FRANZ RD 14%, 6301 S STADIUM LN 7%, 2502 MASON RD 7%, 2715 FRY RD 7%, 2751 N WESTGREEN BLVD 7%, 19711 CLAY RD 7%, 18605 GREEN LAND WAY 7%, 1901 CHARLTON HOUSE LN 7%, 19910 STONELODGE 7%, 21203 PARK TIMBERS 7%, 3535 N FRY RD 7%

USER_SCH_3: KATY 85%, HOUSTON 15%

USER_SCH_5: 77449 38%, 77493 12%, 77494 8%, 77449-3859 8%, 77494-1057 4%, 77084 4%, 77450-5200 4%, 77450-5372 4%, 77449-2898 4%, 77084-4408 4%, 77449-3398 4%, 77450-2797 4%

USER_SCH_6: 20625 CLAY RD 14%, 24406 FRANZ RD 14%, 2602 WINCHESTER RANCH TRAIL 7%, 2502 MASON RD 7%, 2715 FRY RD 7%, 2751 N WESTGREEN BLVD 7%, 19711 CLAY RD 7%, 18605 GREEN LAND WAY 7%, 1901 CHARLTON HOUSE LN 7%, 19910 STONELODGE 7%, 21203 PARK TIMBERS 7%, 3535 N FRY RD 7%

USER_SCH_7: KATY 85%, HOUSTON 15%

USER_SCH_9: 77449 33%, 77493 17%, 77494 8%, 77449-3859 8%, 77084 4%, 77450-5200 4%, 77450-5372 4%, 77449-9999 4%, 77449-2898 4%, 77084-4408 4%, 77449-3398 4%, 77450-2797 4%

USER_SCH10: (281) 398-8031 ext:101 14%, (281) 394-9417 14%, (281) 396-6000 7%, (281) 234-0300 7%, (281) 234-0200 7%, (281) 237-8600 7%, (281) 237-8500 7%, (281) 237-4500 7%, (281) 237-6850 7%, (281) 237-5456 7%, (281) 237-3200 7%, (281) 237-2000 7%

USER_SCH11: (281) 398-8032 14%, (346) 387-7044 14%, (281) 396-6000 7%, (281) 644-1685 7%, (281) 644-1680 7%, (281) 644-1520 7%, (281) 644-1590 7%, (281) 644-1615 7%, (281) 644-1595 7%, (281) 644-1575 7%, (281) 644-1541 7%, (281) 644-1580 7%

USER_SCH12: Mpeper@cnchs.net 14%, scamarilloarroyo@iltexas.org 14%, stephanielvaughan@katyisd.org 7%, deborahshubble@katyisd.org 7%, michaeleschwartz@katyisd.org 7%, YvetteGSylvan@katyisd.org 7%, timothydwolff@katyisd.org 7%, charlotteygilder@katyisd.org 7%, tammirwilhelm@katyisd.org 7%, debrabarker@katyisd.org 7%, HeatherAMulcahy@KATYISD.ORG 7%, rahsanjsmith@katyisd.org 7%

USER_SCH13: www.katyisd.org/ 84%, www.cnchs.net 6%, katyk8.iltexas.org 6%, westparkk8.iltexas.org 3%

USER_SCH14: MINDY PEPER 15%, MS STEPHANIE VAUGHAN 8%, DEBORAH HUBBLE 8%, MICHAEL SCHWARTZ 8%, YVETTE SYLVAN 8%, MR TIMOTHY WOLFF 8%, CHARLOTTE GILDER 8%, MRS TAMMI WILHELM 8%, MS DEBRA BARKER 8%, HEATHER MULCAHY 8%, MR RAHSAN SMITH 8%, MS JESSICA HALE 8%

USER_GRADE: EE-05 55%, 06-08 27%, 09-12 12%, KG-05 6%

USER_SCH15: 796 15%, 1190 8%, 1130 8%, 618 8%, 1000 8%, 1311 8%, 981 8%, 1228 8%, 610 8%, 708 8%, 959 8%, 737 8%

GEOMETRY: {"type": "Point", "coordinates 14%, {"type": "Point", "coordinates 14%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FID | category | 33 | 0 | 33 1; 32 1; 31 1; 30 1 |
| OBJECTID | category | 33 | 0 | 5024 1; 5000 1; 4997 1; 4994 1 |
| STATUS | other | 1 | 0 | M 33 |
| SCORE | amount | 10 | 0 | 100.0 20; 99.0 4; 95.47 2; 99.62 1 |
| MATCH_TYPE | other | 1 | 0 | A 33 |
| MATCH_ADDR | category | 31 | 0 | 20625 Clay Rd, Katy, Texa 2; 24406 Franz Rd, Katy, Tex 2; 2602 Winchester Ranch Trl 1; 2502 N Mason Rd, Katy, Te 1 |
| LONGLABEL | category | 31 | 0 | 20625 Clay Rd, Katy, TX,  2; 24406 Franz Rd, Katy, TX, 2; 2602 Winchester Ranch Trl 1; 2502 N Mason Rd, Katy, TX 1 |
| SHORTLABEL | category | 31 | 0 | 20625 Clay Rd 2; 24406 Franz Rd 2; 2602 Winchester Ranch Trl 1; 2502 N Mason Rd 1 |
| ADDR_TYPE | category | 3 | 0 | PointAddress 27; StreetAddress 4; StreetAddressExt 2 |
| TYPE | empty | 1 | 33 |  |
| PLACENAME | empty | 1 | 33 |  |
| PLACE_ADDR | category | 31 | 0 | 20625 Clay Rd, Katy, Texa 2; 24406 Franz Rd, Katy, Tex 2; 2602 Winchester Ranch Trl 1; 2502 N Mason Rd, Katy, Te 1 |
| PHONE | empty | 1 | 33 |  |
| URL | empty | 1 | 33 |  |
| RANK | other | 1 | 0 | 20 33 |
| ADDBLDG | empty | 1 | 33 |  |
| ADDNUM | category | 29 | 0 | 21203 2; 3535 2; 20625 2; 24406 2 |
| ADDNUMFROM | category | 6 | 27 | 24398 2; 2500 1; 20957 1; 22499 1 |
| ADDNUMTO | category | 6 | 27 | 24348 2; 2572 1; 21003 1; 22301 1 |
| ADDRANGE | category | 6 | 27 | 24348-24398 2; 2500-2572 1; 20957-21003 1; 22301-22499 1 |
| SIDE | category | 3 | 27 | L 4; R 2 |
| STPREDIR | category | 3 | 29 | N 3; S 1 |
| STPRETYPE | empty | 1 | 33 |  |
| STNAME | category | 23 | 0 | Clay 3; Franz 3; Mason 2; Fry 2 |
| STTYPE | category | 9 | 0 | Rd 15; Blvd 5; Dr 5; Ln 3 |
| STDIR | empty | 1 | 33 |  |
| BLDGTYPE | empty | 1 | 33 |  |
| BLDGNAME | empty | 1 | 33 |  |
| LEVELTYPE | empty | 1 | 33 |  |
| LEVELNAME | empty | 1 | 33 |  |
| UNITTYPE | empty | 1 | 33 |  |
| UNITNAME | empty | 1 | 33 |  |
| SUBADDR | empty | 1 | 33 |  |
| STADDR | category | 31 | 0 | 20625 Clay Rd 2; 24406 Franz Rd 2; 2602 Winchester Ranch Trl 1; 2502 N Mason Rd 1 |
| BLOCK | empty | 1 | 33 |  |
| SECTOR | empty | 1 | 33 |  |
| NBRHD | category | 2 | 32 | West Memorial 1 |
| DISTRICT | empty | 1 | 33 |  |
| CITY | category | 2 | 0 | Katy 28; Houston 5 |
| METROAREA | category | 2 | 27 | Houston-Galveston Metro A 6 |
| SUBREGION | who | 1 | 0 | Harris County 33 |
| REGION | other | 1 | 0 | Texas 33 |
| REGIONABBR | other | 1 | 0 | TX 33 |
| TERRITORY | empty | 1 | 33 |  |
| ZONE | empty | 1 | 33 |  |
| POSTAL | category | 5 | 0 | 77449 14; 77450 10; 77493 4; 77084 4 |
| POSTALEXT | category | 24 | 9 | 5593 2; 4179 1; 3054 1; 6380 1 |
| COUNTRY | other | 1 | 0 | USA 33 |
| LANGCODE | other | 1 | 0 | ENG 33 |
| DISTANCE | amount | 2 | 0 | 0.0 32; 299151.115512 1 |
| X | amount | 31 | 0 | -95.7361153861746 2; -95.7929341079374 2; -95.7815758398649 1; -95.7520146795882 1 |
| Y | amount | 31 | 0 | 29.8295800338165 2; 29.8019116116657 2; 29.8129998519148 1; 29.8131046228751 1 |
| DISPLAYX | amount | 31 | 0 | -95.734323 2; -95.7929341079374 2; -95.7820289655505 1; -95.7520146795882 1 |
| DISPLAYY | amount | 31 | 0 | 29.829114 2; 29.8019116116657 2; 29.8138859867183 1; 29.8131046228751 1 |
| XMIN | amount | 31 | 0 | -95.735323 2; -95.7939341079374 2; -95.7830289655505 1; -95.7530146795882 1 |
| XMAX | amount | 31 | 0 | -95.733323 2; -95.7919341079374 2; -95.7810289655505 1; -95.7510146795882 1 |
| YMIN | amount | 31 | 0 | 29.828114 2; 29.8009116116657 2; 29.8128859867183 1; 29.8121046228751 1 |
| YMAX | amount | 31 | 0 | 29.830114 2; 29.8029116116657 2; 29.8148859867183 1; 29.8141046228751 1 |
| EXINFO | category | 3 | 29 | DALLAS COUNTY 3; 77494 1 |
| IN_ADDRESS | category | 31 | 0 | 20625 CLAY RD 2; 24406 FRANZ RD 2; 2602 WINCHESTER RANCH TRA 1; 2502 MASON RD 1 |
| IN_ADDRE_1 | empty | 1 | 33 |  |
| IN_ADDRE_2 | empty | 1 | 33 |  |
| IN_NEIGHBO | empty | 1 | 33 |  |
| IN_CITY | category | 2 | 0 | KATY 28; HOUSTON 5 |
| IN_SUBREGI | category | 2 | 0 | HARRIS COUNTY 30; DALLAS COUNTY 3 |
| IN_REGION | other | 1 | 0 | TX 33 |
| IN_POSTAL | category | 21 | 0 | 77449 8; 77493 4; 77494 2; 77449-3859 2 |
| IN_POSTALE | empty | 1 | 33 |  |
| IN_COUNTRY | empty | 1 | 33 |  |
| USER_COUNT | category | 2 | 0 | 101 30; 57 3 |
| USER_COU_1 | category | 2 | 0 | HARRIS COUNTY 30; DALLAS COUNTY 3 |
| USER_ESC_R | category | 2 | 0 | 4 30; 10 3 |
| USER_ESC_1 | category | 2 | 0 | 4 30; 10 3 |
| USER_ESC_2 | category | 2 | 0 | 4 30; 10 3 |
| USER_DISTR | category | 3 | 0 | 101914 28; 57848 3; 101837 2 |
| USER_DIS_1 | category | 3 | 0 | KATY ISD 28; INTERNATIONAL LEADERSHIP  3; CALVIN NELMS CHARTER SCHO 2 |
| USER_DIS_2 | category | 2 | 0 | INDEPENDENT 28; CHARTER 5 |
| USER_NCES | category | 3 | 0 | 4825170 28; 4801440 3; 4800124 2 |
| USER_DIS_3 | category | 3 | 0 | P O BOX 159 28; 2021 LAKESIDE BLVD 3; 20625 CLAY RD 2 |
| USER_DIS_4 | category | 2 | 0 | KATY 30; RICHARDSON 3 |
| USER_DIS_5 | other | 1 | 0 | TX 33 |
| USER_DIS_6 | category | 3 | 0 | 77492-0159 28; 75082 3; 77449 2 |
| USER_DIS_7 | category | 3 | 0 | 6301 S STADIUM LN 28; 2021 LAKESIDE BLVD 3; 20625 CLAY RD 2 |
| USER_DIS_8 | category | 2 | 0 | KATY 30; RICHARDSON 3 |
| USER_DIS_9 | other | 1 | 0 | TX 33 |
| USER_DIS10 | category | 3 | 0 | 77494-1057 28; 75082 3; 77449 2 |
| USER_DIS11 | category | 3 | 0 | (281) 396-6000 28; (972) 479-9078 3; (281) 398-8031 2 |
| USER_DIS12 | category | 3 | 0 | (281) 644-1800 28; (972) 479-9129 3; (281) 398-8032 2 |
| USER_DIS13 | category | 3 | 0 | kennethgregorski@katyisd. 28; econger@iltexas.org 3; MDean@cnchs.net 2 |
| USER_DIS14 | category | 3 | 0 | www.katyisd.org/ 28; www.iltexas.org/ 3; WWW.cnchs.net 2 |
| USER_DIS15 | category | 3 | 0 | DR KENNETH GREGORSKI 28; MR EDWARD CONGER 3; MR MICHAEL DEAN 2 |
| USER_DIS16 | category | 3 | 0 | 92667 28; 22139 3; 313 2 |
| USER_SCHOO | category | 33 | 0 | 101914144 1; 101914130 1; 101914128 1; 101914126 1 |
| USER_SCH_1 | category | 33 | 0 | LEONARD EL 1; MORTON RANCH EL 1; URSULA STEPHENS EL 1; FRANZ EL 1 |
| USER_INSTR | who | 1 | 0 | REGULAR INSTRUCTIONAL 33 |
| USER_CHART | category | 2 | 28 | OPEN ENROLLMENT CHARTER 5 |
| USER_AEA | other | 1 | 0 | N 33 |
| USER_MAGNE | other | 1 | 0 | N 33 |
| USER_RESID | other | 1 | 0 | N 33 |
| USER_NCE_1 | category | 33 | 0 | 482517013805 1; 482517011835 1; 482517010769 1; 482517010767 1 |
| USER_SCH_2 | category | 31 | 0 | 20625 CLAY RD 2; 24406 FRANZ RD 2; 6301 S STADIUM LN 1; 2502 MASON RD 1 |
| USER_SCH_3 | category | 2 | 0 | KATY 28; HOUSTON 5 |
| USER_SCH_4 | other | 1 | 0 | TX 33 |
| USER_SCH_5 | category | 21 | 0 | 77449 9; 77493 3; 77494 2; 77449-3859 2 |
| USER_SCH_6 | category | 31 | 0 | 20625 CLAY RD 2; 24406 FRANZ RD 2; 2602 WINCHESTER RANCH TRA 1; 2502 MASON RD 1 |
| USER_SCH_7 | category | 2 | 0 | KATY 28; HOUSTON 5 |
| USER_SCH_8 | other | 1 | 0 | TX 33 |
| USER_SCH_9 | category | 21 | 0 | 77449 8; 77493 4; 77494 2; 77449-3859 2 |
| USER_SCH10 | category | 31 | 0 | (281) 398-8031 ext:101 2; (281) 394-9417 2; (281) 396-6000 1; (281) 234-0300 1 |
| USER_SCH11 | category | 31 | 0 | (281) 398-8032 2; (346) 387-7044 2; (281) 396-6000 1; (281) 644-1685 1 |
| USER_SCH12 | category | 31 | 0 | Mpeper@cnchs.net 2; scamarilloarroyo@iltexas. 2; stephanielvaughan@katyisd 1; deborahshubble@katyisd.or 1 |
| USER_SCH13 | category | 5 | 2 | www.katyisd.org/ 26; www.cnchs.net 2; katyk8.iltexas.org 2; westparkk8.iltexas.org 1 |
| USER_SCH14 | category | 31 | 0 | MINDY PEPER 2; MS STEPHANIE VAUGHAN 1; DEBORAH HUBBLE 1; MICHAEL SCHWARTZ 1 |
| USER_GRADE | category | 4 | 0 | EE-05 18; 06-08 9; 09-12 4; KG-05 2 |
| USER_SCH15 | category | 32 | 0 | 796 2; 1190 1; 1130 1; 618 1 |
| USER_SCH16 | who | 1 | 0 | Active 33 |
| USER_SCH17 | amount | 17 | 0 | nan 9; 1086134400000.0 3; 1471824000000.0 3; 1217376000000.0 2 |
| USER_UPDAT | date | 4 | 0 | 4/20/2023 5:41:31 AM 18; 4/20/2023 5:41:30 AM 10; 4/20/2023 5:41:20 AM 3; 4/20/2023 5:41:27 AM 2 |
| GEOMETRY | category | 31 | 0 | {"type": "Point", "coordi 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:16:00.11162 33 |
| SOURCE_RUN_ID | audit | 1 | 0 | fe0a327e-1d61-49d9-ba0c-0 33 |
| SRC_SHA256 | who | 1 | 0 | e3c6519302382b54916f5ab77 33 |
