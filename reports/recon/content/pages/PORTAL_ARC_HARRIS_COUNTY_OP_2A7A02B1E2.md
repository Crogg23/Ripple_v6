# PORTAL_ARC_HARRIS_COUNTY_OP_2A7A02B1E2

rows 14  columns 124  scan 6.5s

roles: amount 9, audit 2, category 66, date 3, empty 27, other 14, who 4

## when

USER_SCH17
  1993         1  ###############
  1994         1  ###############
  2005         1  ###############
  2007         1  ###############
  2009         1  ###############
  2013         1  ###############
  2015         1  ###############
  2016         2  ##############################
  2018         1  ###############
  2022         1  ###############

USER_UPDAT
  2025        14  ##############################

INGESTED_AT
  2026        14  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 14 | 98.82 | 100 | 100 | 100 | 1.4K |
| X | 14 | -95.91 | -95.61 | -95.50 | -95.50 | -1.3K |
| Y | 14 | 29.66 | 29.75 | 30.08 | 30.08 | 417.02 |
| DISPLAYX | 14 | -95.91 | -95.61 | -95.50 | -95.50 | -1.3K |
| DISPLAYY | 14 | 29.66 | 29.75 | 30.08 | 30.08 | 417.02 |
| XMIN | 14 | -95.91 | -95.61 | -95.50 | -95.50 | -1.3K |

## who

CNTRYNAME by rows
        14  United States

CNTRYNAME by dollars
        1.4K       14 rows  United States

SUBREGION by rows
        14  Harris County

SUBREGION by dollars
        1.4K       14 rows  Harris County

USER_SCH16 by rows
        14  Active

USER_SCH16 by dollars
        1.4K       14 rows  Active

SRC_SHA256 by rows
        14  f74cfd9607574718b2718a4e652e04acb4086e4fcf6279f6be07cae416f5698c

SRC_SHA256 by dollars
        1.4K       14 rows  f74cfd9607574718b2718a4e652e04acb4086e4fcf6279f6be07cae416f5

## who x when

CNTRYNAME by USER_UPDAT, dollars = SCORE
  United States                             2025:1.4K

SUBREGION by USER_UPDAT, dollars = SCORE
  Harris County                             2025:1.4K

## what

OBJECTID: 14 8%, 13 8%, 12 8%, 11 8%, 10 8%, 9 8%, 8 8%, 7 8%, 6 8%, 5 8%, 4 8%, 3 8%

OBJECTID_1: 9220 8%, 5283 8%, 5252 8%, 5045 8%, 5016 8%, 4771 8%, 4519 8%, 4461 8%, 4285 8%, 4261 8%, 3557 8%, 2162 8%

MATCH_ADDR: 14400 Fern Dr, Houston, Texas, 14%, 15300 Bellaire Blvd, Houston,  14%, 19455 Stokes Rd, Waller, Texas 7%, 2715 Fry Rd, Katy, Texas, 7744 7%, 22605 Provincial Blvd, Katy, T 7%, 8405 Bonhomme Rd, Houston, Tex 7%, 16212 W Little York Rd, Housto 7%, 11100 Stancliff Rd, Houston, T 7%, 9305 W Sam Houston Pkwy S, Hou 7%, 10535 Harwin Dr, Houston, Texa 7%, 6615 Rookin St, Houston, Texas 7%, 27708 Tomball Pkwy, Tomball, T 7%

LONGLABEL: 14400 Fern Dr, Houston, TX, 77 14%, 15300 Bellaire Blvd, Houston,  14%, 19455 Stokes Rd, Waller, TX, 7 7%, 2715 Fry Rd, Katy, TX, 77449,  7%, 22605 Provincial Blvd, Katy, T 7%, 8405 Bonhomme Rd, Houston, TX, 7%, 16212 W Little York Rd, Housto 7%, 11100 Stancliff Rd, Houston, T 7%, 9305 W Sam Houston Pkwy S, Hou 7%, 10535 Harwin Dr, Houston, TX,  7%, 6615 Rookin St, Houston, TX, 7 7%, 27708 Tomball Pkwy, Tomball, T 7%

SHORTLABEL: 14400 Fern Dr 14%, 15300 Bellaire Blvd 14%, 19455 Stokes Rd 7%, 2715 Fry Rd 7%, 22605 Provincial Blvd 7%, 8405 Bonhomme Rd 7%, 16212 W Little York Rd 7%, 11100 Stancliff Rd 7%, 9305 W Sam Houston Pkwy S 7%, 10535 Harwin Dr 7%, 6615 Rookin St 7%, 27708 Tomball Pkwy 7%

ADDR_TYPE: PointAddress 79%, StreetAddress 21%

PLACE_ADDR: 14400 Fern Dr, Houston, Texas, 14%, 15300 Bellaire Blvd, Houston,  14%, 19455 Stokes Rd, Waller, Texas 7%, 2715 Fry Rd, Katy, Texas, 7744 7%, 22605 Provincial Blvd, Katy, T 7%, 8405 Bonhomme Rd, Houston, Tex 7%, 16212 W Little York Rd, Housto 7%, 11100 Stancliff Rd, Houston, T 7%, 9305 W Sam Houston Pkwy S, Hou 7%, 10535 Harwin Dr, Houston, Texa 7%, 6615 Rookin St, Houston, Texas 7%, 27708 Tomball Pkwy, Tomball, T 7%

ADDNUM: 14400 14%, 15300 14%, 19455 7%, 2715 7%, 22605 7%, 8405 7%, 16212 7%, 11100 7%, 9305 7%, 10535 7%, 6615 7%, 27708 7%

ADDNUMFROM: 19401 33%, 2653 33%, 27700 33%

ADDNUMTO: 19467 33%, 3473 33%, 27716 33%

ADDRANGE: 19401-19467 33%, 2653-3473 33%, 27700-27716 33%

SIDE: L 67%, R 33%

STPREDIR: W 100%

STNAME: Fern 14%, Bellaire 14%, Stokes 7%, Fry 7%, Provincial 7%, Bonhomme 7%, Little York 7%, Stancliff 7%, Sam Houston 7%, Harwin 7%, Rookin 7%, Tomball 7%

STTYPE: Rd 36%, Dr 21%, Blvd 21%, Pkwy 14%, St 7%

STDIR: S 100%

STADDR: 14400 Fern Dr 14%, 15300 Bellaire Blvd 14%, 19455 Stokes Rd 7%, 2715 Fry Rd 7%, 22605 Provincial Blvd 7%, 8405 Bonhomme Rd 7%, 16212 W Little York Rd 7%, 11100 Stancliff Rd 7%, 9305 W Sam Houston Pkwy S 7%, 10535 Harwin Dr 7%, 6615 Rookin St 7%, 27708 Tomball Pkwy 7%

CITY: Houston 71%, Katy 14%, Waller 7%, Tomball 7%

POSTAL: 77079 14%, 77074 14%, 77099 14%, 77083 14%, 77484 7%, 77449 7%, 77450 7%, 77084 7%, 77036 7%, 77375 7%

POSTALEXT: 5508 17%, 3109 17%, 7310 8%, 1627 8%, 5609 8%, 6509 8%, 4212 8%, 5204 8%, 1505 8%, 5015 8%

IN_ADDRESS: 14400 FERN 14%, 15300 BELLAIRE BLVD 14%, 19455 STOKES RD 7%, 2715 FRY RD 7%, 22605 PROVINCIAL BLVD 7%, 8405 BONHOMME 7%, 16212 W LITTLE YORK 7%, 11100 STANCLIFF 7%, 9305 W SAM HOUSTON PKWY S 7%, 10535 HARWIN DR 7%, 6615 ROOKIN ST 7%, 27708 TOMBALL PKWY 7%

IN_CITY: HOUSTON 71%, KATY 14%, WALLER 7%, TOMBALL 7%

IN_POSTAL: 77099 14%, 77083 14%, 77484-2200 7%, 77079-5599 7%, 77079 7%, 77494 7%, 77450-1698 7%, 77074-5609 7%, 77084 7%, 77036 7%, 77074 7%, 77375 7%

USER_COUNT: '101 64%, '057 14%, '237 7%, '072 7%, '046 7%

USER_COU_1: HARRIS COUNTY 64%, DALLAS COUNTY 14%, WALLER COUNTY 7%, ERATH COUNTY 7%, COMAL COUNTY 7%

USER_ESC_R: '04 71%, '10 14%, '11 7%, '20 7%

USER_ESC_1: '04 71%, '10 14%, '11 7%, '20 7%

USER_ESC_2: '04 71%, '10 14%, '11 7%, '13 7%

USER_DISTR: '101920 14%, '101914 14%, '057848 14%, '237904 7%, '101912 7%, '101907 7%, '101903 7%, '101846 7%, '101845 7%, '072801 7%, '046802 7%

USER_DIS_1: SPRING BRANCH ISD 14%, KATY ISD 14%, INTERNATIONAL LEADERSHIP OF TE 14%, WALLER ISD 7%, HOUSTON ISD 7%, CYPRESS-FAIRBANKS ISD 7%, ALIEF ISD 7%, HARMONY PUBLIC SCHOOLS - HOUST 7%, YES PREP PUBLIC SCHOOLS INC 7%, PREMIER HIGH SCHOOLS 7%, TRINITY CHARTER SCHOOL 7%

USER_DIS_2: INDEPENDENT 57%, CHARTER 43%

USER_NCES: '4841100 14%, '4825170 14%, '4801440 14%, '4844430 7%, '4823640 7%, '4816110 7%, '4807830 7%, '4800210 7%, '4800209 7%, '4800207 7%, '4800259 7%

USER_DIS_3: 955 CAMPBELL RD 14%, P O BOX 159 14%, 2021 LAKESIDE BLVD 14%, 2214 WALLER ST 7%, 4400 W 18TH ST 7%, P O BOX 692003 7%, P O BOX 68 7%, 9321 W SAM HOUSTON PKWY S 7%, 5455 S LOOP E FWY 7%, P O BOX 292730 7%, 8305 CROSS PARK DR 7%

USER_DIS_4: HOUSTON 43%, KATY 14%, RICHARDSON 14%, WALLER 7%, ALIEF 7%, LEWISVILLE 7%, AUSTIN 7%

USER_DIS_6: 77024-2803 14%, 77492-0159 14%, 75082 14%, 77484 7%, 77092-8501 7%, 77269-2003 7%, 77411-0068 7%, 77099 7%, 77033 7%, 75029 7%, 78714 7%

USER_DIS_7: 955 CAMPBELL RD 14%, 6301 S STADIUM LN 14%, 2021 LAKESIDE BLVD 14%, 2214 WALLER ST 7%, 4400 W 18TH ST 7%, 11440 MATZKE RD 7%, 4250 COOK RD 7%, 13522 W AIRPORT BLVD 7%, 5455 S LOOP E FWY 7%, 1301 WATERS RIDGE DR 7%, 8305 CROSS PARK DR 7%

USER_DIS_8: HOUSTON 36%, KATY 14%, RICHARDSON 14%, WALLER 7%, CYPRESS 7%, SUGAR LAND 7%, LEWISVILLE 7%, AUSTIN 7%

USER_DIS10: 77024-2803 14%, 77494-1057 14%, 75082 14%, 77484 7%, 77092-8501 7%, 77429 7%, 77072-1115 7%, 77478 7%, 77033 7%, 75057 7%, 78754 7%

USER_DIS11: (713) 464-1511 14%, (281) 396-6000 14%, (972) 479-9078 14%, (936) 931-3685 7%, (713) 556-6005 7%, (281) 897-4000 7%, (281) 498-8110 7%, (832) 831-9174 7%, (713) 967-9000 7%, (972) 316-3663 7%, (512) 778-6363 7%

USER_DIS12: (713) 251-9186 14%, (281) 644-1800 14%, (972) 479-9129 14%, (936) 310-6589 7%, (713) 556-6006 7%, (281) 897-4125 7%, (281) 988-3037 7%, (713) 777-8555 7%, (713) 589-2502 7%, (972) 315-9506 7%, (877) 705-2477 7%

USER_DIS13: jennifer.jones@springbranchisd 14%, kennethgregorski@katyisd.org 14%, econger@iltexas.org 14%, kmoran@wallerisd.net 7%, HISDSuperintendent@houstonisd. 7%, superintendent@cfisd.net 7%, rachel.delafuente@aliefisd.net 7%, superintendent.office@harmonyt 7%, mark.dibella@yesprep.org 7%, ccook@responsiveed.com 7%, Info@Trinitycharterschools.org 7%

USER_DIS14: www.springbranchisd.com 14%, www.katyisd.org/ 14%, www.iltexas.org/ 14%, www.wallerisd.net 7%, www.houstonisd.org 7%, www.cfisd.net 7%, www.aliefisd.net 7%, hva.harmonytx.org 7%, www.yesprep.org 7%, www.responsiveed.com/premier 7%, www.trinitycharterschools.org 7%

USER_DIS15: DR JENNIFER BLAINE 14%, DR KENNETH GREGORSKI 14%, MR EDWARD CONGER 14%, KEVIN MORAN 7%, MR MIKE MILES 7%, DR DOUGLAS KILLIAN 7%, DR ANTHONY MAYS 7%, MR FATIH AY 7%, MR MARK DIBELLA 7%, MR CHARLES COOK 7%, KEELY REYNOLDS 7%

USER_DIS16: 32668 14%, 96111 14%, 25497 14%, 9905 7%, 176727 7%, 117927 7%, 38610 7%, 3663 7%, 19573 7%, 7948 7%, 315 7%

USER_SCHOO: '237904102 8%, '101920123 8%, '101920018 8%, '101914128 8%, '101914103 8%, '101912163 8%, '101907053 8%, '101903141 8%, '101846102 8%, '101845005 8%, '072801161 8%, '057848017 8%

USER_SCH_1: I T HOLLEMAN EL 8%, THORNWOOD EL 8%, SPRING BRANCH ACADEMIC INSTITU 8%, URSULA STEPHENS EL 8%, WEST MEMORIAL EL 8%, SUGAR GROVE ACADEMY 8%, KAHLA MIDDLE 8%, KLENTZMAN INT 8%, HARMONY SCHOOL OF EXPLORATION- 8%, YES PREP - WEST 8%, PREMIER H S - HOUSTON (SHARPST 8%, ILTEXAS WESTPARK MIDDLE 8%

USER_INSTR: REGULAR INSTRUCTIONAL 86%, ALTERNATIVE INSTRUCTIONAL 14%

USER_CHART: OPEN ENROLLMENT CHARTER 100%

USER_AEA: N 93%, Y 7%

USER_RESID: N 93%, Y 7%

USER_NCE_1: '484443005072 8%, '484110004700 8%, '484110013209 8%, '482517010769 8%, '482517002812 8%, '482364006983 8%, '481611010728 8%, '480783007016 8%, '480021012974 8%, '480020912401 8%, '480020722832 8%, '480144013267 8%

USER_SCH_2: 14400 FERN 14%, 15300 BELLAIRE BLVD 14%, 19455 STOKES RD 7%, 2715 FRY RD 7%, 22605 PROVINCIAL BLVD 7%, 8405 BONHOMME 7%, 16212 W LITTLE YORK 7%, 11100 STANCLIFF 7%, 9305 W SAM HOUSTON PKWY S 7%, 10535 HARWIN DR 7%, P O BOX 292730 7%, 8305 CROSSPARK DR 7%

USER_SCH_3: HOUSTON 64%, KATY 14%, WALLER 7%, LEWISVILLE 7%, AUSTIN 7%

USER_SCH_5: 77099 14%, 77083 14%, 77484-2200 7%, 77079-5599 7%, 77079 7%, 77494 7%, 77450-1698 7%, 77074-5609 7%, 77084 7%, 77036 7%, 75029 7%, 78754 7%

USER_SCH_6: 14400 FERN 14%, 15300 BELLAIRE BLVD 14%, 19455 STOKES RD 7%, 2715 FRY RD 7%, 22605 PROVINCIAL BLVD 7%, 8405 BONHOMME 7%, 16212 W LITTLE YORK 7%, 11100 STANCLIFF 7%, 9305 W SAM HOUSTON PKWY S 7%, 10535 HARWIN DR 7%, 6615 ROOKIN ST 7%, 27708 TOMBALL PKWY 7%

USER_SCH_7: HOUSTON 71%, KATY 14%, WALLER 7%, TOMBALL 7%

USER_SCH_9: 77099 14%, 77083 14%, 77484-2200 7%, 77079-5599 7%, 77079 7%, 77494 7%, 77450-1698 7%, 77074-5609 7%, 77084 7%, 77036 7%, 77074 7%, 77375 7%

USER_SCH10: (346) 203-4126 15%, (936) 372-9196 8%, (713) 251-7300 8%, (713) 251-2277 8%, (281) 234-0200 8%, (281) 237-6600 8%, (713) 271-0214 8%, (281) 345-3260 8%, (281) 983-8477 8%, (832) 831-7406 8%, (713) 967-8200 8%, (713) 347-1002 8%

USER_SCH11: (281) 933-8129 15%, (936) 372-4023 8%, (713) 251-9765 8%, (713) 251-9190 8%, (281) 644-1680 8%, (281) 644-1625 8%, (713) 771-9342 8%, (281) 345-5275 8%, (281) 983-8373 8%, (713) 541-3032 8%, (713) 969-4863 8%, (972) 315-9506 8%

USER_SCH12: ahilaire@iltexas.org 15%, mrsciba@wallerisd.net 8%, TWE@springbranchisd.com 8%, patricia.kassir@springbranchis 8%, caroledlangley@katyisd.org 8%, rebeccammarron@katyisd.org 8%, nortega1@houstonisd.org 8%, joshua.carroll@cfisd.net 8%, amelia.tukes@aliefisd.net 8%, superintendent.office@harmonyt 8%, publicinfo@yesprep.org 8%, clbailey@responsiveedtx.com 8%

USER_SCH13: www.katyisd.org/ 14%, westparkk8.iltexas.org 14%, www.wallerisd.net 7%, twe.springbranchis.com 7%, sbai.springbranchisd.com 7%, www.houstonisd.org 7%, www.cfisd.net 7%, www.aliefisd.net 7%, hehouston.harmonytx.org/ 7%, west.yesprep.org 7%, www.responsiveed.com/premier 7%, trinitycharterschools.org 7%

USER_SCH14: MICHELLE SCIBA 8%, SANDRA HOUSTON 8%, MS PATRICIA KASSIR 8%, MS CAROLE LANGLEY 8%, MS REBECCA MARRON 8%, NOE ORTEGA 8%, JOSHUA CARROLL 8%, MS AMELIA TUKES 8%, GEMMA OLSON 8%, NATALIE GARCIA 8%, CURTIS BAILEY 8%, MS ARELIS CARDONA-HILAIRE 8%

USER_GRADE: 'EE-05 29%, '06-08 21%, '06-12 14%, '01-12 7%, '05-06 7%, 'PK-05 7%, '09-12 7%, 'KG-05 7%

USER_SCH15: 753 8%, 391 8%, 174 8%, 578 8%, 970 8%, 777 8%, 1126 8%, 833 8%, 687 8%, 990 8%, 91 8%, 440 8%

SCHOOL_TYP: Elementary School 43%, Middle School 29%, Elementary/Secondary 21%, High School 7%

GEOMETRY: {"type": "Point", "coordinates 14%, {"type": "Point", "coordinates 14%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 14 | 0 | 14 1; 13 1; 12 1; 11 1 |
| OBJECTID_1 | category | 14 | 0 | 9220 1; 5283 1; 5252 1; 5045 1 |
| STATUS | other | 1 | 0 | M 14 |
| SCORE | amount | 4 | 0 | 100.0 8; 98.82 4; 99.51 1; 98.84 1 |
| MATCH_TYPE | other | 1 | 0 | A 14 |
| MATCH_ADDR | category | 12 | 0 | 14400 Fern Dr, Houston, T 2; 15300 Bellaire Blvd, Hous 2; 19455 Stokes Rd, Waller,  1; 2715 Fry Rd, Katy, Texas, 1 |
| LONGLABEL | category | 12 | 0 | 14400 Fern Dr, Houston, T 2; 15300 Bellaire Blvd, Hous 2; 19455 Stokes Rd, Waller,  1; 2715 Fry Rd, Katy, TX, 77 1 |
| SHORTLABEL | category | 12 | 0 | 14400 Fern Dr 2; 15300 Bellaire Blvd 2; 19455 Stokes Rd 1; 2715 Fry Rd 1 |
| ADDR_TYPE | category | 2 | 0 | PointAddress 11; StreetAddress 3 |
| TYPE | empty | 1 | 14 |  |
| PLACENAME | empty | 1 | 14 |  |
| PLACE_ADDR | category | 12 | 0 | 14400 Fern Dr, Houston, T 2; 15300 Bellaire Blvd, Hous 2; 19455 Stokes Rd, Waller,  1; 2715 Fry Rd, Katy, Texas, 1 |
| PHONE | empty | 1 | 14 |  |
| URL | empty | 1 | 14 |  |
| RANK | other | 1 | 0 | 20 14 |
| ADDBLDG | empty | 1 | 14 |  |
| ADDNUM | category | 12 | 0 | 14400 2; 15300 2; 19455 1; 2715 1 |
| ADDNUMFROM | category | 4 | 11 | 19401 1; 2653 1; 27700 1 |
| ADDNUMTO | category | 4 | 11 | 19467 1; 3473 1; 27716 1 |
| ADDRANGE | category | 4 | 11 | 19401-19467 1; 2653-3473 1; 27700-27716 1 |
| SIDE | category | 3 | 11 | L 2; R 1 |
| STPREDIR | category | 2 | 12 | W 2 |
| STPRETYPE | empty | 1 | 14 |  |
| STNAME | category | 12 | 0 | Fern 2; Bellaire 2; Stokes 1; Fry 1 |
| STTYPE | category | 5 | 0 | Rd 5; Dr 3; Blvd 3; Pkwy 2 |
| STDIR | category | 2 | 13 | S 1 |
| BLDGTYPE | empty | 1 | 14 |  |
| BLDGNAME | empty | 1 | 14 |  |
| LEVELTYPE | empty | 1 | 14 |  |
| LEVELNAME | empty | 1 | 14 |  |
| UNITTYPE | empty | 1 | 14 |  |
| UNITNAME | empty | 1 | 14 |  |
| SUBADDR | empty | 1 | 14 |  |
| STADDR | category | 12 | 0 | 14400 Fern Dr 2; 15300 Bellaire Blvd 2; 19455 Stokes Rd 1; 2715 Fry Rd 1 |
| BLOCK | empty | 1 | 14 |  |
| SECTOR | empty | 1 | 14 |  |
| NBRHD | empty | 1 | 14 |  |
| DISTRICT | empty | 1 | 14 |  |
| CITY | category | 4 | 0 | Houston 10; Katy 2; Waller 1; Tomball 1 |
| METROAREA | empty | 1 | 14 |  |
| SUBREGION | who | 1 | 0 | Harris County 14 |
| REGION | other | 1 | 0 | Texas 14 |
| REGIONABBR | other | 1 | 0 | TX 14 |
| TERRITORY | empty | 1 | 14 |  |
| ZONE | empty | 1 | 14 |  |
| POSTAL | category | 10 | 0 | 77079 2; 77074 2; 77099 2; 77083 2 |
| POSTALEXT | category | 11 | 2 | 5508 2; 3109 2; 7310 1; 1627 1 |
| COUNTRY | other | 1 | 0 | USA 14 |
| CNTRYNAME | who | 1 | 0 | United States 14 |
| LANGCODE | other | 1 | 0 | ENG 14 |
| DISTANCE | other | 1 | 0 | 0 14 |
| X | amount | 12 | 0 | -95.60038333608418 2; -95.65705316307908 2; -95.90880961201152 1; -95.72062424350631 1 |
| Y | amount | 12 | 0 | 29.775450201280687 2; 29.700025265681333 2; 30.05834654689768 1; 29.80910174453211 1 |
| DISPLAYX | amount | 12 | 0 | -95.600124 2; -95.6572695 2; -95.90880961201152 1; -95.72062424350631 1 |
| DISPLAYY | amount | 12 | 0 | 29.776077 2; 29.700756 2; 30.05834654689768 1; 29.80910174453211 1 |
| XMIN | amount | 12 | 0 | -95.601124 2; -95.6582695 2; -95.90980961201153 1; -95.72162424350631 1 |
| XMAX | amount | 12 | 0 | -95.59912399999999 2; -95.6562695 2; -95.90780961201152 1; -95.7196242435063 1 |
| YMIN | amount | 12 | 0 | 29.775077 2; 29.699755999999997 2; 30.05734654689768 1; 29.80810174453211 1 |
| YMAX | amount | 12 | 0 | 29.777077000000002 2; 29.701756 2; 30.059346546897682 1; 29.810101744532112 1 |
| EXINFO | empty | 1 | 14 |  |
| IN_ADDRESS | category | 12 | 0 | 14400 FERN 2; 15300 BELLAIRE BLVD 2; 19455 STOKES RD 1; 2715 FRY RD 1 |
| IN_ADDRE_1 | empty | 1 | 14 |  |
| IN_ADDRE_2 | empty | 1 | 14 |  |
| IN_NEIGHBO | empty | 1 | 14 |  |
| IN_CITY | category | 4 | 0 | HOUSTON 10; KATY 2; WALLER 1; TOMBALL 1 |
| IN_SUBREGI | empty | 1 | 14 |  |
| IN_REGION | other | 1 | 0 | TX 14 |
| IN_POSTAL | category | 12 | 0 | 77099 2; 77083 2; 77484-2200 1; 77079-5599 1 |
| IN_POSTALE | empty | 1 | 14 |  |
| IN_COUNTRY | empty | 1 | 14 |  |
| USER_COUNT | category | 5 | 0 | '101 9; '057 2; '237 1; '072 1 |
| USER_COU_1 | category | 5 | 0 | HARRIS COUNTY 9; DALLAS COUNTY 2; WALLER COUNTY 1; ERATH COUNTY 1 |
| USER_ESC_R | category | 4 | 0 | '04 10; '10 2; '11 1; '20 1 |
| USER_ESC_1 | category | 4 | 0 | '04 10; '10 2; '11 1; '20 1 |
| USER_ESC_2 | category | 4 | 0 | '04 10; '10 2; '11 1; '13 1 |
| USER_DISTR | category | 11 | 0 | '101920 2; '101914 2; '057848 2; '237904 1 |
| USER_DIS_1 | category | 11 | 0 | SPRING BRANCH ISD 2; KATY ISD 2; INTERNATIONAL LEADERSHIP  2; WALLER ISD 1 |
| USER_DIS_2 | category | 2 | 0 | INDEPENDENT 8; CHARTER 6 |
| USER_NCES | category | 10 | 0 | '4841100 2; '4825170 2; '4801440 2; '4844430 1 |
| USER_DIS_3 | category | 10 | 0 | 955 CAMPBELL RD 2; P O BOX 159 2; 2021 LAKESIDE BLVD 2; 2214 WALLER ST 1 |
| USER_DIS_4 | category | 7 | 0 | HOUSTON 6; KATY 2; RICHARDSON 2; WALLER 1 |
| USER_DIS_5 | other | 1 | 0 | TX 14 |
| USER_DIS_6 | category | 11 | 0 | 77024-2803 2; 77492-0159 2; 75082 2; 77484 1 |
| USER_DIS_7 | category | 11 | 0 | 955 CAMPBELL RD 2; 6301 S STADIUM LN 2; 2021 LAKESIDE BLVD 2; 2214 WALLER ST 1 |
| USER_DIS_8 | category | 8 | 0 | HOUSTON 5; KATY 2; RICHARDSON 2; WALLER 1 |
| USER_DIS_9 | other | 1 | 0 | TX 14 |
| USER_DIS10 | category | 11 | 0 | 77024-2803 2; 77494-1057 2; 75082 2; 77484 1 |
| USER_DIS11 | category | 11 | 0 | (713) 464-1511 2; (281) 396-6000 2; (972) 479-9078 2; (936) 931-3685 1 |
| USER_DIS12 | category | 11 | 0 | (713) 251-9186 2; (281) 644-1800 2; (972) 479-9129 2; (936) 310-6589 1 |
| USER_DIS13 | category | 11 | 0 | jennifer.jones@springbran 2; kennethgregorski@katyisd. 2; econger@iltexas.org 2; kmoran@wallerisd.net 1 |
| USER_DIS14 | category | 11 | 0 | www.springbranchisd.com 2; www.katyisd.org/ 2; www.iltexas.org/ 2; www.wallerisd.net 1 |
| USER_DIS15 | category | 11 | 0 | DR JENNIFER BLAINE 2; DR KENNETH GREGORSKI 2; MR EDWARD CONGER 2; KEVIN MORAN 1 |
| USER_DIS16 | category | 11 | 0 | 32668 2; 96111 2; 25497 2; 9905 1 |
| USER_SCHOO | category | 14 | 0 | '237904102 1; '101920123 1; '101920018 1; '101914128 1 |
| USER_SCH_1 | category | 14 | 0 | I T HOLLEMAN EL 1; THORNWOOD EL 1; SPRING BRANCH ACADEMIC IN 1; URSULA STEPHENS EL 1 |
| USER_INSTR | category | 2 | 0 | REGULAR INSTRUCTIONAL 12; ALTERNATIVE INSTRUCTIONAL 2 |
| USER_CHART | category | 2 | 8 | OPEN ENROLLMENT CHARTER 6 |
| USER_AEA | category | 2 | 0 | N 13; Y 1 |
| USER_MAGNE | other | 1 | 0 | N 14 |
| USER_RESID | category | 2 | 0 | N 13; Y 1 |
| USER_NCE_1 | category | 14 | 0 | '484443005072 1; '484110004700 1; '484110013209 1; '482517010769 1 |
| USER_SCH_2 | category | 12 | 0 | 14400 FERN 2; 15300 BELLAIRE BLVD 2; 19455 STOKES RD 1; 2715 FRY RD 1 |
| USER_SCH_3 | category | 5 | 0 | HOUSTON 9; KATY 2; WALLER 1; LEWISVILLE 1 |
| USER_SCH_4 | other | 1 | 0 | TX 14 |
| USER_SCH_5 | category | 12 | 0 | 77099 2; 77083 2; 77484-2200 1; 77079-5599 1 |
| USER_SCH_6 | category | 12 | 0 | 14400 FERN 2; 15300 BELLAIRE BLVD 2; 19455 STOKES RD 1; 2715 FRY RD 1 |
| USER_SCH_7 | category | 4 | 0 | HOUSTON 10; KATY 2; WALLER 1; TOMBALL 1 |
| USER_SCH_8 | other | 1 | 0 | TX 14 |
| USER_SCH_9 | category | 12 | 0 | 77099 2; 77083 2; 77484-2200 1; 77079-5599 1 |
| USER_SCH10 | category | 13 | 0 | (346) 203-4126 2; (936) 372-9196 1; (713) 251-7300 1; (713) 251-2277 1 |
| USER_SCH11 | category | 13 | 0 | (281) 933-8129 2; (936) 372-4023 1; (713) 251-9765 1; (713) 251-9190 1 |
| USER_SCH12 | category | 13 | 0 | ahilaire@iltexas.org 2; mrsciba@wallerisd.net 1; TWE@springbranchisd.com 1; patricia.kassir@springbra 1 |
| USER_SCH13 | category | 12 | 0 | www.katyisd.org/ 2; westparkk8.iltexas.org 2; www.wallerisd.net 1; twe.springbranchis.com 1 |
| USER_SCH14 | category | 14 | 0 | MICHELLE SCIBA 1; SANDRA HOUSTON 1; MS PATRICIA KASSIR 1; MS CAROLE LANGLEY 1 |
| USER_GRADE | category | 8 | 0 | 'EE-05 4; '06-08 3; '06-12 2; '01-12 1 |
| USER_SCH15 | category | 14 | 0 | 753 1; 391 1; 174 1; 578 1 |
| USER_SCH16 | who | 1 | 0 | Active 14 |
| USER_SCH17 | date | 11 | 3 | 08/22/2016 2; 06/08/2015 1; 08/10/2007 1; 07/01/1993 1 |
| USER_UPDAT | date | 7 | 0 | 3/11/2025 5:38:01 AM 4; 3/11/2025 5:38:00 AM 3; 3/11/2025 5:37:59 AM 2; 3/11/2025 5:37:56 AM 2 |
| SCHOOL_TYP | category | 4 | 0 | Elementary School 6; Middle School 4; Elementary/Secondary 3; High School 1 |
| GEOMETRY | category | 12 | 0 | {"type": "Point", "coordi 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:13:59.43700 14 |
| SOURCE_RUN_ID | audit | 1 | 0 | a9a1bb27-6ca5-4083-b250-7 14 |
| SRC_SHA256 | who | 1 | 0 | f74cfd9607574718b2718a4e6 14 |
