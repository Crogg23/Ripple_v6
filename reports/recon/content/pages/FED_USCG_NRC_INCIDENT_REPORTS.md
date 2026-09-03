# FED_USCG_NRC_INCIDENT_REPORTS

rows 116.7K  columns 18  scan 3.1s

roles: audit 2, category 2, date 2, empty 5, id 1, other 4, who 2

## when

DATE_TIME_RECEIVED
  2020     22.5K  ############################
  2021     24.5K  ##############################
  2022     23.5K  #############################
  2023     23.1K  ############################
  2024     23.0K  ############################

DATE_TIME_COMPLETE
  2020     22.5K  ############################
  2021     24.5K  ##############################
  2022     23.5K  #############################
  2023     23.1K  ############################
  2024     23.0K  ############################

## who

RESPONSIBLE_COMPANY by rows
       456  TARGA RESOURCES
       441  CSX RAILROAD
       404  KINDER MORGAN
       381  COX OPERATING
       329  NORFOLK SOUTHERN
       261  ENERGY TRANSFER
       242  PHILLIPS 66
       237  REPUBLIC SERVICES
       200  CONSOLIDATED EDISON COMPANY OF NEW YORK
       197  TAYLOR ENERGY
       196  CANTIUM LLC
       195  TALOS ENERGY
       186  TARGA PIPELINE
       185  ENTERGY
       180  CHEVRON
       178  US NAVY
       174  WILLIAMS COMPANIES
       169  BP
       159  WEEKS MARINE
       159  TEXAS PETROLEUM INVESTMENT COMPANY

RESPONSIBLE_CITY by rows
      4.0K  HOUSTON
      1.0K  NEW ORLEANS
       790  JACKSONVILLE
       614  ATLANTA
       561  SEATTLE
       546  LAFAYETTE
       512  TULSA
       480  MIDLAND
       465  COVINGTON
       369  SAN DIEGO
       364  NORFOLK
       357  DALLAS
       347  PHOENIX
       330  CORPUS CHRISTI
       327  PORT ARTHUR
       323  THE WOODLANDS
       314  OMAHA
       298  WESTLAKE
       298  PORTLAND
       276  WILMINGTON

## who x when

RESPONSIBLE_COMPANY by DATE_TIME_RECEIVED
  BP                                        2020:37 2021:32 2022:26 2023:37 2024:37
  CANTIUM LLC                               2020:30 2021:36 2022:36 2023:51 2024:43
  CHEVRON                                   2020:43 2021:40 2022:35 2023:30 2024:32
  CONSOLIDATED EDISON COMPANY OF NEW YORK   2020:71 2021:46 2022:49 2023:18 2024:16
  COX OPERATING                             2020:81 2021:80 2022:97 2023:105 2024:18
  CSX RAILROAD                              2020:133 2021:100 2022:73 2023:53 2024:82
  ENERGY TRANSFER                           2020:23 2021:37 2022:64 2023:64 2024:73
  ENTERGY                                   2020:94 2021:30 2022:23 2023:12 2024:26
  KINDER MORGAN                             2020:74 2021:89 2022:77 2023:86 2024:78
  NORFOLK SOUTHERN                          2020:2 2021:58 2022:121 2023:84 2024:64
  PHILLIPS 66                               2020:26 2021:49 2022:36 2023:66 2024:65
  REPUBLIC SERVICES                         2020:76 2021:95 2022:25 2023:27 2024:14
  TALOS ENERGY                              2020:40 2021:21 2022:27 2023:53 2024:54
  TARGA PIPELINE                            2020:45 2021:15 2022:31 2023:76 2024:19
  TARGA RESOURCES                           2020:34 2021:42 2022:130 2023:120 2024:130
  TAYLOR ENERGY                             2020:111 2021:69 2022:15 2023:1 2024:1
  TEXAS PETROLEUM INVESTMENT COMPANY        2020:36 2021:42 2022:14 2023:29 2024:38
  US NAVY                                   2020:41 2021:40 2022:26 2023:30 2024:41
  WEEKS MARINE                              2020:28 2021:23 2022:19 2023:49 2024:40
  WILLIAMS COMPANIES                        2020:18 2021:19 2022:46 2023:50 2024:41

RESPONSIBLE_CITY by DATE_TIME_RECEIVED
  ATLANTA                                   2020:90 2021:115 2022:157 2023:129 2024:123
  CORPUS CHRISTI                            2020:70 2021:81 2022:62 2023:72 2024:45
  COVINGTON                                 2020:77 2021:94 2022:82 2023:105 2024:107
  DALLAS                                    2020:57 2021:62 2022:75 2023:94 2024:69
  HOUSTON                                   2020:643 2021:743 2022:797 2023:855 2024:1.0K
  JACKSONVILLE                              2020:206 2021:180 2022:133 2023:117 2024:154
  LAFAYETTE                                 2020:111 2021:160 2022:95 2023:94 2024:86
  MIDLAND                                   2020:159 2021:83 2022:103 2023:64 2024:71
  NEW ORLEANS                               2020:320 2021:328 2022:222 2023:99 2024:65
  NORFOLK                                   2020:71 2021:83 2022:69 2023:63 2024:78
  OMAHA                                     2020:44 2021:60 2022:82 2023:57 2024:71
  PHOENIX                                   2020:100 2021:124 2022:55 2023:25 2024:43
  PORT ARTHUR                               2020:33 2021:43 2022:103 2023:87 2024:61
  PORTLAND                                  2020:69 2021:83 2022:49 2023:51 2024:46
  SAN DIEGO                                 2020:59 2021:64 2022:81 2023:84 2024:81
  SEATTLE                                   2020:104 2021:116 2022:119 2023:115 2024:107
  THE WOODLANDS                             2020:28 2021:52 2022:51 2023:104 2024:88
  TULSA                                     2020:97 2021:98 2022:103 2023:105 2024:109
  WESTLAKE                                  2020:55 2021:67 2022:55 2023:63 2024:58
  WILMINGTON                                2020:63 2021:62 2022:55 2023:48 2024:48

## what

RESPONSIBLE_ORG_TYPE: PRIVATE ENTERPRISE 44%, UNKNOWN 41%, PRIVATE CITIZEN 9%, MILITARY 2%, PUBLIC UTILITY 2%, LOCAL GOVERNMENT 1%, FEDERAL GOVERNMENT 0%, STATE GOVERNMENT 0%, OTHER 0%, FIRE DEPARTMENT 0%, POLICE DEPARTMENT 0%, TRIBE 0%

SOURCE: TELEPHONE 98%, MESSAGE TRAFFIC 2%, NEWS 0%, OTHERS 0%, AWW HOTLINE 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SEQNOS | id | 114.0K | 0 | 1420229 584; 1420228 584; 1420227 584; 1420222 584 |
| DATE_TIME_RECEIVED | date | 115.3K | 0 | 2024-12-30 17:40:00 585; 2024-12-31 22:24:00 584; 2024-12-31 21:06:00 584; 2024-12-31 21:00:00 584 |
| DATE_TIME_COMPLETE | date | 113.2K | 0 | 2024-12-31 12:50:00 585; 2024-12-31 11:40:00 585; 2024-12-30 15:41:00 585; 2024-12-31 22:27:00 584 |
| CALLTYPE | other | 1 | 0 | INC 116.7K |
| RESPONSIBLE_COMPANY | who | 27.1K | 56.8K | TARGA RESOURCES 512; CSX RAILROAD 442; KINDER MORGAN 405; NORFOLK SOUTHERN 397 |
| RESPONSIBLE_ORG_TYPE | category | 14 | 207 | PRIVATE ENTERPRISE 51.8K; UNKNOWN 47.5K; PRIVATE CITIZEN 10.0K; MILITARY 2.5K |
| RESPONSIBLE_CITY | who | 8.8K | 55.3K | HOUSTON 4.0K; NEW ORLEANS 1.0K; JACKSONVILLE 790; ATLANTA 614 |
| RESPONSIBLE_STATE | other | 93 | 83 | XX 53.3K; TX 10.9K; LA 5.8K; CA 4.0K |
| RESPONSIBLE_ZIP | other | 9.6K | 77.5K | 77002 1.1K; 30308 375; 32202 361; 70508 309 |
| SOURCE | category | 5 | 1 | TELEPHONE 114.7K; MESSAGE TRAFFIC 1.9K; NEWS 6; OTHERS 4 |
| COLUMN1 | empty | 0 | 116.7K |  |
| COLUMN2 | empty | 0 | 116.7K |  |
| COLUMN3 | empty | 0 | 116.7K |  |
| COLUMN4 | empty | 0 | 116.7K |  |
| COLUMN5 | empty | 0 | 116.7K |  |
| INGESTED_AT | audit | 1 | 0 | 1786164136569826 116.7K |
| SOURCE_RUN_ID | audit | 1 | 0 | 1a914807-a170-46d4-8ecc-4 116.7K |
| SRC_SHA256 | other | 1 | 0 | 535020c6dadb74ecd51aab64d 116.7K |
