# PORTAL_CKA_SAN_JOSE_OPEN_DA_D4BF270A36

rows 92  columns 24  scan 3.7s

roles: amount 2, audit 2, category 8, date 1, empty 2, other 7, who 3

## when

INGESTED_AT
  2026        92  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 92 | 6.13M | 6.15M | 6.19M | 6.19M | 566.29M |
| Y | 92 | 1.91M | 1.95M | 1.98M | 1.98M | 179.30M |

## who

NAME by rows
         4  Extended Stay America
         3  Holiday Inn
         3  Motel 6
         2  Aloft Hotel
         2  Residence Inn
         2  Four Points by Sheraton Hotel
         1  DoubleTree Hotel
         1  Hotel Rose Garden
         1  Hotel Elan
         1  Valley Inn
         1  Hotel De Anza
         1  Hampton Inn
         1  Travelers Rest Motel
         1  Plaza Hotel
         1  Whitehouse Inn
         1  Hotel Clariana
         1  Americas Best Value Inn
         1  Hyatt Place San Jose Airport
         1  The Alameda Motel
         1  Lanai Garden Inn & Suites

NAME by dollars
      24.63M        4 rows  Extended Stay America
      18.48M        3 rows  Motel 6
      18.45M        3 rows  Holiday Inn
      12.33M        2 rows  Residence Inn
      12.31M        2 rows  Four Points by Sheraton Hotel
      12.27M        2 rows  Aloft Hotel
       6.19M        1 rows  Wynham Garden Hotel
       6.18M        1 rows  Hayes Mansion
       6.18M        1 rows  Fontaine Inn
       6.17M        1 rows  Lanai Garden Inn & Suites
       6.17M        1 rows  Mission Motel
       6.17M        1 rows  Days Inn
       6.17M        1 rows  Capitol Hill Inn
       6.17M        1 rows  Clarion Inn
       6.17M        1 rows  Whitehouse Inn
       6.17M        1 rows  Palm Tree Inn Motel
       6.17M        1 rows  Holiday Inn Express & Suites
       6.17M        1 rows  SureStay Plus Hotel
       6.17M        1 rows  Tully Inn & Suites
       6.16M        1 rows  California Motel

FACILITYID by rows
         1  75
         1  13
         1  48
         1  64
         1  114
         1  1279
         1  37
         1  73
         1  106
         1  1
         1  28
         1  8
         1  108
         1  50
         1  15
         1  9
         1  27
         1  32
         1  115
         1  23

FACILITYID by dollars
       6.19M        1 rows  36
       6.19M        1 rows  60
       6.19M        1 rows  25
       6.18M        1 rows  21
       6.18M        1 rows  54
       6.18M        1 rows  19
       6.17M        1 rows  49
       6.17M        1 rows  51
       6.17M        1 rows  18
       6.17M        1 rows  6
       6.17M        1 rows  12
       6.17M        1 rows  105
       6.17M        1 rows  57
       6.17M        1 rows  116
       6.17M        1 rows  115
       6.17M        1 rows  33
       6.16M        1 rows  5
       6.16M        1 rows  64
       6.16M        1 rows  8
       6.16M        1 rows  106

SRC_SHA256 by rows
        92  fe9db28a16d52786de9f7eed29d104ec7b732ef4832f5c1c36464653c6cf22c5

SRC_SHA256 by dollars
     566.29M       92 rows  fe9db28a16d52786de9f7eed29d104ec7b732ef4832f5c1c36464653c6cf

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  Aloft Hotel                               2026:12.27M
  Americas Best Value Inn                   2026:6.16M
  Capitol Hill Inn                          2026:6.17M
  Clarion Inn                               2026:6.17M
  Days Inn                                  2026:6.17M
  DoubleTree Hotel                          2026:6.15M
  Extended Stay America                     2026:24.63M
  Fontaine Inn                              2026:6.18M
  Four Points by Sheraton Hotel             2026:12.31M
  Hampton Inn                               2026:6.15M
  Hayes Mansion                             2026:6.18M
  Holiday Inn                               2026:18.45M
  Holiday Inn Express & Suites              2026:6.17M
  Hotel Clariana                            2026:6.16M
  Hotel De Anza                             2026:6.16M
  Hotel Elan                                2026:6.16M
  Hotel Rose Garden                         2026:6.15M
  Hyatt Place San Jose Airport              2026:6.15M
  Lanai Garden Inn & Suites                 2026:6.17M
  Mission Motel                             2026:6.17M
  Motel 6                                   2026:18.48M
  Palm Tree Inn Motel                       2026:6.17M
  Plaza Hotel                               2026:6.16M
  Residence Inn                             2026:12.33M
  SureStay Plus Hotel                       2026:6.17M
  The Alameda Motel                         2026:6.15M
  Travelers Rest Motel                      2026:6.16M
  Valley Inn                                2026:6.15M
  Whitehouse Inn                            2026:6.17M
  Wynham Garden Hotel                       2026:6.19M

FACILITYID by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  1                                         2026:6.13M
  106                                       2026:6.16M
  108                                       2026:6.13M
  114                                       2026:6.16M
  115                                       2026:6.17M
  1279                                      2026:6.14M
  13                                        2026:6.15M
  15                                        2026:6.15M
  18                                        2026:6.17M
  19                                        2026:6.18M
  21                                        2026:6.18M
  23                                        2026:6.15M
  25                                        2026:6.19M
  27                                        2026:6.13M
  28                                        2026:6.15M
  32                                        2026:6.15M
  36                                        2026:6.19M
  37                                        2026:6.15M
  48                                        2026:6.14M
  49                                        2026:6.17M
  50                                        2026:6.16M
  51                                        2026:6.17M
  54                                        2026:6.18M
  6                                         2026:6.17M
  60                                        2026:6.19M
  64                                        2026:6.16M
  73                                        2026:6.16M
  75                                        2026:6.15M
  8                                         2026:6.16M
  9                                         2026:6.15M

## what

STATUS: closed 100%

STREETPREFIX: N 51%, S 29%, E 12%, W 7%

STREETNAME: 1st St 29%, Monterey Rd 21%, The Alameda 13%, 4th St 8%, Santa Clara St 5%, Market St 5%, America Center Ct 3%, Bascom Ave 3%, Oakland Rd 3%, 2nd St 3%, San Ignacio Ave 3%, Fontaine Rd 3%

ZIPCODE: 95112 27%, 95113 13%, 95110 12%, 95131 12%, 95111 10%, 95126 9%, 95128 3%, 95134 3%, 95002 3%, 95008 2%, 95119 2%, 95121 2%

AGENCYURL: http://studiosinn.com/ 33%, https://www.ihg.com/holidayinn 33%, https://www.bestwestern.com/en 33%

LASTUPDATE: 2021/05/07 19:00:09+00 11%, 2021/05/07 19:00:08+00 11%, 2021/05/07 19:00:06+00 11%, 2021/05/07 19:00:07+00 9%, 2021/05/07 19:00:01+00 9%, 2021/05/07 19:00:11+00 8%, 2021/05/07 19:00:10+00 8%, 2021/05/07 19:00:05+00 8%, 2021/05/07 19:00:03+00 8%, 2021/05/07 19:00:00+00 8%, 2021/05/07 19:00:12+00 6%, 2021/05/07 19:00:04+00 6%

LASTEDITOR: PLN 79%, MICHAEL.FUNG 21%

NOTES: added 5/6/2021 50%, opens April 2022 6%, added 5/6/2021 204 rooms, 6 su 6%, added 5/6/2021. Fairfield: 80  6%, homeless shelter 6%, this converted 27 units to per 6%, converted to low income studio 6%, County of Santa Cara submit pr 6%, bay 101 casino, No hotel 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| X | amount | 91 | 0 | 6141728.22713909 1; 6168093.37453991 1; 6158107.686178 1; 6146941.34138475 1 |
| Y | amount | 91 | 0 | 1943117.70922631 1; 1933258.11870931 1; 1948208.70987107 1; 1953649.83383131 1 |
| INTID | other | 92 | 0 | 1279 1; 116 1; 884 1; 883 1 |
| OBJECTID | other | 92 | 0 | 1279 1; 1278 1; 884 1; 883 1 |
| FACILITYID | who | 92 | 0 | 1279 1; 116 1; 884 1; 883 1 |
| NAME | who | 83 | 0 | Extended Stay America 4; Holiday Inn 3; Motel 6 3; Residence Inn 2 |
| STATUS | category | 2 | 86 | closed 6 |
| GUESTROOMS | other | 74 | 1 | 21 4; 26 3; 61 2; 81 2 |
| ADDRNUM | other | 86 | 0 | 10 2; 1350 2; 55 2; 2050 2 |
| STREETPREFIX | category | 5 | 51 | N 21; S 12; E 5; W 3 |
| STREETNAME | category | 41 | 0 | 1st St 18; Monterey Rd 13; The Alameda 8; 4th St 5 |
| STREETTYPE | empty | 1 | 92 |  |
| STREETPOSTDIR | empty | 1 | 92 |  |
| FULLADDR | other | 93 | 0 | 348 S. Clover Ave 1; 2660 Monterey Rd 1; 100 E Santa Clara St 1; 1130 Wondo Wy 1 |
| ZIPCODE | category | 18 | 0 | 95112 23; 95113 11; 95110 10; 95131 10 |
| AGENCYURL | category | 4 | 89 | http://studiosinn.com/ 1; https://www.ihg.com/holid 1; https://www.bestwestern.c 1 |
| LASTUPDATE | category | 33 | 0 | 2021/05/07 19:00:09+00 7; 2021/05/07 19:00:08+00 7; 2021/05/07 19:00:06+00 7; 2021/05/07 19:00:07+00 6 |
| LASTEDITOR | category | 2 | 0 | PLN 73; MICHAEL.FUNG 19 |
| NOTES | category | 10 | 76 | added 5/6/2021 8; opens April 2022 1; added 5/6/2021 204 rooms, 1; added 5/6/2021. Fairfield 1 |
| GLOBALID | other | 91 | 0 | {66A33E6E-FC17-4170-A657- 1; {70796F93-01AC-4CFB-B88D- 1; {EA761485-C0BC-4452-8302- 1; {BC840C68-84F5-4382-8BE1- 1 |
| ENTERPRISEID | other | 93 | 0 | PLN-HOTE-0000001279 1; PLN-HOTE-0000000116 1; PLN-HOTE-0000000884 1; PLN-HOTE-0000000883 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:31:19.18949 92 |
| SOURCE_RUN_ID | audit | 1 | 0 | 3d5583ad-a6ef-401e-a94f-0 92 |
| SRC_SHA256 | who | 1 | 0 | fe9db28a16d52786de9f7eed2 92 |
