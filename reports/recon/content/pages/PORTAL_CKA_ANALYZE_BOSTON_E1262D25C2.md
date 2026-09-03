# PORTAL_CKA_ANALYZE_BOSTON_E1262D25C2

rows 35  columns 31  scan 3.7s

roles: amount 5, audit 2, category 21, date 1, empty 2, who 1

## when

INGESTED_AT
  2026        35  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CT90 | 33 | 3 | 709 | 1.4K | 1.4K | 23.2K |
| XCOORD | 34 | 0 | 71.08M | 71.16M | 71.17M | 2.35B |
| YCOORD | 34 | 0 | 42.34M | 42.39M | 42.39M | 1.40B |
| POINT_X | 35 | -71.17 | -71.07 | -71.01 | -71 | -2.5K |
| POINT_Y | 35 | 42.24 | 42.34 | 42.39 | 42.39 | 1.5K |

## who

SRC_SHA256 by rows
        35  6c56f0f41aee768e197431275ff5fb8131c1f2a33230985b9b2064c1fabe8f86

SRC_SHA256 by dollars
       -2.5K       35 rows  6c56f0f41aee768e197431275ff5fb8131c1f2a33230985b9b2064c1fabe

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = POINT_X
  6c56f0f41aee768e197431275ff5fb8131c1f2a3  2026:-2.5K

## what

BFD_ID: 47.000000000000000 8%, 0.000000000000000 8%, 10.000000000000000 8%, 28.000000000000000 8%, 56.000000000000000 8%, 55.000000000000000 8%, 53.000000000000000 8%, 52.000000000000000 8%, 51.000000000000000 8%, 50.000000000000000 8%, 49.000000000000000 8%, 48.000000000000000 8%

MAP_ID: 043 10%, 060 10%, 055 10%, 074 10%, 063 10%, 062 10%, 035 10%, 045 10%, 059 10%, 058 10%

MAPCODE: 2 100%

LOCCODE: 043 10%, 042 10%, 033 10%, 032 10%, 031 10%, 030 10%, 029 10%, 028 10%, 027 10%, 026 10%

LOCDEPT: BFD 100%

LOCNAME: AIR SUPPLY UNIT 9%, Engine CO. 10 9%, Engine CO. 28, 10 (Division 2  9%, Engine CO. 56, 21 9%, Engine CO. 55 9%, Engine CO. 53, 16 9%, Engine CO. 52, 29 9%, Engine CO. 51 9%, Engine CO. 50 9%, Engine CO. 49 9%, Engine CO. 48, 28 9%

LOCCONTACT: Cptn O'Donnell 10%, Cptn. James Famolare 10%, Cptn. George Cohen 10%, Cptn. Sullivan 10%, Frftr Bowden, Cptn Noonan 10%, Cptn. Mozocca 10%, Cptn. John Varner 10%, Cptn. Tom Mortell 10%, Cptn. Porter, Ltnt Rushton 10%, Officer O'Brien 10%

LOCPHONE: 725-2810 10%, 725-2856 10%, 725-2855 10%, 725-2853 10%, 725-2852 10%, 725-2851 10%, 725-2850 10%, 725-2849 10%, 725-2848 10%, 725-2842 10%

LOCSTNO: 700 15%, 200 15%, 115 8%, 125 8%, 746 8%, 1 8%, 5115 8%, 945 8%, 975 8%, 425 8%, 34 8%

LOCADDR: Centre St 13%, Columbus Ave 13%, Cambridge St 13%, 50 Battery Wharf 7%, SOUTHAMPTON ST 7%, Purchase St 7%, Ashley St 7%, Washington St 7%, Canterbury St 7%, Blue Hill Ave 7%, Faneuil St, Oak Sq 7%, Winthrop St 7%

LOCOWNER: BFD 97%, PRI 3%

LOCWARD: 03 12%, 01 12%, 18 12%, 20 8%, 14 8%, 22 8%, 02 8%, 06 8%, 05 8%, 16 8%, 08 8%

LOCPARCL: 00000 71%, 00603 3%, 03006 3%, 05003 3%, 06009 3%, 07000 3%, 09003 3%, 02502 3%, 00500 3%, 01003 3%

LOCPLAN: F 100%

STUDY: T 94%, F 6%

ABOVE: 0 53%, 1 26%, 2 9%, 3 9%, 4 3%

ABOVE_DESC: (2)275g FO 25%, (1)1000g FO in bsment 8%, (1) 500g Diesel 8%, (1)1000g  diesel rear of bldg 8%, (1)1000g FO Basement 8%, (1)1000g  FO in basement 8%, (1)500g diesel,(2)330g FO 8%, (3)275g FO, (1)275 Diesel 8%, (1)275g Diesel 8%, (3)250g Diesel 8%

SOURCE: FP 39%, FPA 23%, P 10%, PD 6%, PF 6%, OF 3%, FPI 3%, DP 3%, FAP 3%, FD 3%

GEOADDRESS: 50 Battery Wharf 9%, 125 Purchase St 9%, 746 Centre St 9%, 1 Ashley St

 9%, 5115 Washington St 9%, 945 Canterbury St 9%, 975 Blue Hill Ave 9%, 425 Faneuil St, Oak Sq 9%, 34 Winthrop St 9%, 205 Neponset Valley Pkwy 9%, 60 Fairmount Ave 9%

PD: Boston 13%, Dorchester 13%, East Boston 10%, Allston/Brighton 10%, Roxbury 10%, West Roxbury 6%, Mattapan 6%, Charlestown 6%, Hyde Park 6%, South Boston 6%, Back Bay/Beacon Hill 6%, South End 6%

SHAPE_WKT: POINT (-71.04966350899997 42.3 8%, POINT (-71.069633657999987 42. 8%, POINT (-71.052996958999984 42. 8%, POINT (-71.114399582999965 42. 8%, POINT (-71.00418549799997 42.3 8%, POINT (-71.154852234999964 42. 8%, POINT (-71.117495638999969 42. 8%, POINT (-71.089696120999974 42. 8%, POINT (-71.168162183999982 42. 8%, POINT (-71.061126545999969 42. 8%, POINT (-71.131241127999942 42. 8%, POINT (-71.119847859999936 42. 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | empty | 1 | 35 |  |
| BFD_ID | category | 35 | 0 | 47.000000000000000 1; 0.000000000000000 1; 10.000000000000000 1; 28.000000000000000 1 |
| MAP_ID | category | 35 | 2 | 043 1; 060 1; 055 1; 074 1 |
| MAPCODE | category | 3 | 2 | 2 33 |
| LOCCODE | category | 35 | 2 | 043 1; 042 1; 033 1; 032 1 |
| LOCDEPT | category | 2 | 1 | BFD 34 |
| LOCNAME | category | 35 | 1 | AIR SUPPLY UNIT 1; Engine CO. 10 1; Engine CO. 28, 10 (Divisi 1; Engine CO. 56, 21 1 |
| LOCCONTACT | category | 34 | 3 | Cptn O'Donnell 1; Cptn. James Famolare 1; Cptn. George Cohen 1; Cptn. Sullivan 1 |
| LOCPHONE | category | 34 | 3 | 725-2810 1; 725-2856 1; 725-2855 1; 725-2853 1 |
| LOCSTNO | category | 33 | 1 | 700 2; 200 2; 115 1; 125 1 |
| LOCADDR | category | 32 | 0 | Centre St 2; Columbus Ave 2; Cambridge St 2; 50 Battery Wharf 1 |
| LOCOWNER | category | 4 | 2 | BFD 32; PRI 1 |
| LOCWARD | category | 21 | 2 | 03 3; 01 3; 18 3; 20 2 |
| LOCPARCL | category | 14 | 2 | 00000 22; 00603 1; 03006 1; 05003 1 |
| LOCPRECT | empty | 2 | 35 |  |
| LOCPLAN | category | 3 | 2 | F 33 |
| STUDY | category | 4 | 2 | T 31; F 2 |
| ABOVE | category | 6 | 1 | 0 18; 1 9; 2 3; 3 3 |
| ABOVE_DESC | category | 16 | 19 | (2)275g FO 3; (1)1000g FO in bsment 1; (1) 500g Diesel 1; (1)1000g  diesel rear of  1 |
| SOURCE | category | 12 | 4 | FP 12; FPA 7; P 3; PD 2 |
| GEOADDRESS | category | 34 | 1 | 50 Battery Wharf 1; 125 Purchase St 1; 746 Centre St 1; 1 Ashley St

 1 |
| PD | category | 16 | 1 | Boston 4; Dorchester 4; East Boston 3; Allston/Brighton 3 |
| CT90 | amount | 35 | 2 | 701 1; 1204 1; 511 1; 1304.01 1 |
| XCOORD | amount | 35 | 1 | 0.000000000000000 1; 71053770.000000000000000 1; 71115365.000000000000000 1; 71004487.000000000000000 1 |
| YCOORD | amount | 35 | 1 | 0.000000000000000 1; 42354808.000000000000000 1; 42310280.000000000000000 1; 42387724.000000000000000 1 |
| SHAPE_WKT | category | 35 | 0 | POINT (-71.04966350899997 1; POINT (-71.06963365799998 1; POINT (-71.05299695899998 1; POINT (-71.11439958299996 1 |
| POINT_X | amount | 35 | 0 | -71.049663508999970 1; -71.069633657999987 1; -71.052996958999984 1; -71.114399582999965 1 |
| POINT_Y | amount | 35 | 0 | 42.366634545000068 1; 42.331310567000060 1; 42.355083048000040 1; 42.310566613000049 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:20:16.15356 35 |
| SOURCE_RUN_ID | audit | 1 | 0 | f688d923-2d31-4896-86cd-f 35 |
| SRC_SHA256 | who | 1 | 0 | 6c56f0f41aee768e197431275 35 |
