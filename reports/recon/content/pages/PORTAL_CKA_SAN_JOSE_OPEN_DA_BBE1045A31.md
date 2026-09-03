# PORTAL_CKA_SAN_JOSE_OPEN_DA_BBE1045A31

rows 56  columns 35  scan 5.3s

roles: amount 4, audit 2, category 16, date 1, empty 8, other 2, who 3

## when

INGESTED_AT
  2026        56  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 56 | 6.12M | 6.15M | 6.19M | 6.19M | 344.55M |
| Y | 56 | 1.91M | 1.95M | 1.98M | 1.98M | 109.26M |
| ELEVATION | 10 | 47.29 | 69.04 | 301.30 | 313 | 1.1K |
| NOMHP | 42 | 0 | 1 | 4.5K | 5.8K | 11.1K |

## who

FACILITYID by rows
         1  90004
         1  76390
         1  34563
         1  33275
         1  90009
         1  76389
         1  34561
         1  76900
         1  77754
         1  76906
         1  79831
         1  4015
         1  30115
         1  76905
         1  79813
         1  22749
         1  76899
         1  34571
         1  22564
         1  22566

FACILITYID by dollars
       6.19M        1 rows  90000
       6.18M        1 rows  32901
       6.18M        1 rows  79813
       6.18M        1 rows  90012
       6.18M        1 rows  77299
       6.17M        1 rows  34563
       6.17M        1 rows  30077
       6.17M        1 rows  90006
       6.17M        1 rows  79831
       6.16M        1 rows  31330
       6.16M        1 rows  76906
       6.16M        1 rows  2406
       6.16M        1 rows  22754
       6.16M        1 rows  34570
       6.16M        1 rows  22750
       6.16M        1 rows  33275
       6.16M        1 rows  22753
       6.16M        1 rows  76905
       6.16M        1 rows  34572
       6.16M        1 rows  22564

CREATIONDATE by rows
        56  1900/01/01 00:00:00+00

CREATIONDATE by dollars
     344.55M       56 rows  1900/01/01 00:00:00+00

SRC_SHA256 by rows
        56  d5e7c2c28567e91a85363759064102f6e5ddffb25a69c63ade23f3a0e8a3b3a0

SRC_SHA256 by dollars
     344.55M       56 rows  d5e7c2c28567e91a85363759064102f6e5ddffb25a69c63ade23f3a0e8a3

## who x when

FACILITYID by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  22564                                     2026:6.16M
  22566                                     2026:6.13M
  22749                                     2026:6.15M
  22754                                     2026:6.16M
  2406                                      2026:6.16M
  30077                                     2026:6.17M
  30115                                     2026:6.15M
  31330                                     2026:6.16M
  32901                                     2026:6.18M
  33275                                     2026:6.16M
  34561                                     2026:6.14M
  34563                                     2026:6.17M
  34570                                     2026:6.16M
  34571                                     2026:6.15M
  4015                                      2026:6.14M
  76389                                     2026:6.16M
  76390                                     2026:6.15M
  76899                                     2026:6.16M
  76900                                     2026:6.13M
  76905                                     2026:6.16M
  76906                                     2026:6.16M
  77299                                     2026:6.18M
  77754                                     2026:6.12M
  79813                                     2026:6.18M
  79831                                     2026:6.17M
  90000                                     2026:6.19M
  90004                                     2026:6.15M
  90006                                     2026:6.17M
  90009                                     2026:6.15M
  90012                                     2026:6.18M

CREATIONDATE by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  1900/01/01 00:00:00+00                    2026:344.55M

## what

PUMPTYPE: SUB 67%, UNK 17%, OTH 17%

NUMPUMP: 2 52%, 1 30%, 5 5%, 3 5%, 4 5%, 6 2%

INLETDIAM: 12 50%, 18 50%

DISCHDIAM: 3 50%, 8 50%

DYNHEAD: 2x20 29%, 2x5 29%, 2x30 14%, 2x10 14%, 2x15 14%

NAME: PVT Pumpstation 60%, CalTrans Pumpstation 7%, Lake Cunningham Pump Station 3%, Gold St PS (primary) 3%, Cahill PS (emergency) 3%, SJ Pumpstation 3%, Willow St PS 3%, Forest St PS 3%, Communication Hill PS 3%, Chynoweth PS 3%, Golden Wheel PS 3%, Bird Av PS 3%

DESIGNGPM: 2000 20%, 3200 13%, 10000 13%, 60 7%, 282 7%, 1400 7%, 229 7%, 15280 7%, 42000 7%, 6500 7%, 1740 7%

OWNEDBY: SJ 62%, PVT 34%, CDT 4%

UPGRADEYR: 2007 30%, 2018 10%, 1995 10%, 2005 10%, 2000 10%, 2013 10%, 2004 10%, 2003 10%

INSTALLYEAR: 2008 20%, 2015 15%, 2014 10%, 2017 10%, 2007 10%, 2009 10%, 2011 5%, 2004 5%, 2018 5%, 2013 5%, 1975 5%

SOURCEYEAR: MAGE 90%, ABPL 10%

PLANCRT: MGE 40%, 3-18493B 10%, UNK 5%, 18-111588 5%, CPMS7410 5%, CTR03023 5%, 3-18654D 5%, 3-14681 5%, 3-11445F 5%, CPMS3542 5%, AltinoBlvd_stormPS 5%, 3-01591 5%

PLANMOD: DD-3404 18%, HD87133 9%, DD-3184 9%, D-0018 9%, 1-9281 9%, DD-2233 9%, 4869-36 9%, DD-2905 9%, DD-2232 9%, DD-2276 9%

PLANREF: DD-202011 50%, DD-2132 50%

LASTUPDATE: 2021/04/30 21:16:34+00 63%, 2023/08/24 21:02:13+00 3%, 2020/10/01 18:51:12+00 3%, 2020/10/01 18:50:54+00 3%, 2021/04/30 21:16:58+00 3%, 2021/04/30 21:16:55+00 3%, 2020/10/01 18:50:39+00 3%, 2020/10/01 18:50:35+00 3%, 2020/10/01 18:50:34+00 3%, 2020/10/23 00:53:25+00 3%, 2020/10/01 18:50:18+00 3%, 2020/10/01 18:50:13+00 3%

NOTES: Edited Name per HD Ticket 1043 60%, Located inside IMH33710; Contr 4%, Edited Name per HD Ticket 1043 4%, Edited Name per HD Ticket 1043 4%, CALTRANS asset 4%, Non Automatic Model IX282, Sin 4%, Edited Name per HD Ticket 1043 4%, Crystal Ridge 4%, Edited Name per HD Ticket 1043 4%, San Carlos 4%, Edited Name per HD Ticket 1043 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| X | amount | 56 | 0 | 6180859.73975517 1; 6133192.36232108 1; 6153775.1220085 1; 6149431.40530224 1 |
| Y | amount | 56 | 0 | 1948725.81119907 1; 1981485.12691389 1; 1946328.65588839 1; 1952871.22777697 1 |
| OBJECTID | other | 56 | 0 | 2056 1; 1658 1; 1653 1; 1651 1 |
| FACILITYID | who | 55 | 0 | 90012 1; 1188899 1; 90009 1; 90007 1 |
| INTID | other | 55 | 0 | 90012 1; 1188899 1; 90009 1; 90007 1 |
| PUMPTYPE | category | 4 | 50 | SUB 4; UNK 1; OTH 1 |
| NUMPUMP | category | 7 | 16 | 2 21; 1 12; 5 2; 3 2 |
| ELEVATION | amount | 10 | 46 | 69.04 2; 112.93 1; 106.29 1; 47.29 1 |
| INLETDIAM | category | 3 | 54 | 12 1; 18 1 |
| DISCHDIAM | category | 3 | 54 | 3 1; 8 1 |
| IMPDIAM | empty | 1 | 56 |  |
| NOMHP | amount | 20 | 14 | 0 20; 1 4; 30 2; 1.8 1 |
| RATEDFLOW | empty | 1 | 56 |  |
| RATEDPRESS | empty | 1 | 56 |  |
| DYNHEAD | category | 6 | 49 | 2x20 2; 2x5 2; 2x30 1; 2x10 1 |
| SHUTHEAD | empty | 1 | 56 |  |
| DESHEAD | empty | 1 | 56 |  |
| MAXOPHEAD | empty | 1 | 56 |  |
| NAME | category | 38 | 0 | PVT Pumpstation 18; CalTrans Pumpstation 2; Lake Cunningham Pump Stat 1; Gold St PS (primary) 1 |
| STATIONID | empty | 1 | 56 |  |
| DESIGNGPM | category | 26 | 27 | 2000 3; 3200 2; 10000 2; 60 1 |
| MAXOPDISC | empty | 1 | 56 |  |
| OWNEDBY | category | 3 | 0 | SJ 35; PVT 19; CDT 2 |
| UPGRADEYR | category | 9 | 46 | 2007 3; 2018 1; 1995 1; 2005 1 |
| INSTALLYEAR | category | 15 | 33 | 2008 4; 2015 3; 2014 2; 2017 2 |
| SOURCEYEAR | category | 3 | 46 | MAGE 9; ABPL 1 |
| PLANCRT | category | 48 | 0 | MGE 8; 3-18493B 2; UNK 1; 18-111588 1 |
| PLANMOD | category | 11 | 45 | DD-3404 2; HD87133 1; DD-3184 1; D-0018 1 |
| PLANREF | category | 3 | 54 | DD-202011 1; DD-2132 1 |
| LASTUPDATE | category | 38 | 0 | 2021/04/30 21:16:34+00 19; 2023/08/24 21:02:13+00 1; 2020/10/01 18:51:12+00 1; 2020/10/01 18:50:54+00 1 |
| NOTES | category | 28 | 15 | Edited Name per HD Ticket 15; Located inside IMH33710;  1; Edited Name per HD Ticket 1; Edited Name per HD Ticket 1 |
| CREATIONDATE | who | 1 | 0 | 1900/01/01 00:00:00+00 56 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:12:57.42859 56 |
| SOURCE_RUN_ID | audit | 1 | 0 | 7d9fda40-bd69-4bf9-b427-b 56 |
| SRC_SHA256 | who | 1 | 0 | d5e7c2c28567e91a853637590 56 |
