# PORTAL_CKA_WPRDC_ALLEGHENY_4597FBDFE3

rows 2.9K  columns 13  scan 3.8s

roles: audit 2, category 3, date 3, id 1, other 2, who 3

## when

STARTTIME
  2022      2.9K  ##############################

STOPTIME
  2022      2.9K  ##############################

INGESTED_AT
  2026      2.9K  ##############################

## who

TO_STATION_NAME by rows
       194  North Shore Trail & Fort Duquesne Bridge
       136  S 27th St & Sidney St. (Southside Works)
       136  Liberty Ave & Stanwix St
       135  S 18th St & Sidney St
       117  Schenley Dr & Forbes Ave (Schenley Plaza)
        93  Fifth Ave & S Bouquet St
        84  Microsoft
        82  S Negley Ave & Baum Blvd
        80  Forbes Ave & Market Square
        79  Isabella St & Federal St (PNC Park)
        77  Schenley Dr at Schenley Plaza (Carnegie Library Main)
        73  21st St & Penn Ave
        72  Glasshouse
        70  Hot Metal St & Tunnel Blvd
        54  33rd St & Penn Ave 
        51  Zulema St & Coltart Ave
        49  S Bouquet Ave & Sennott St
        48  Ivy St & Walnut St   
        47  Ellsworth Ave & N Neville St
        47  Burns White Center at 3 Crossings

FROM_STATION_NAME by rows
       178  North Shore Trail & Fort Duquesne Bridge
       137  Liberty Ave & Stanwix St
       126  Schenley Dr & Forbes Ave (Schenley Plaza)
       123  S 27th St & Sidney St. (Southside Works)
       118  Fifth Ave & S Bouquet St
       114  S 18th St & Sidney St
        96  Forbes Ave & Market Square
        95  Schenley Dr at Schenley Plaza (Carnegie Library Main)
        87  Microsoft
        82  Hot Metal St & Tunnel Blvd
        81  Isabella St & Federal St (PNC Park)
        77  Ivy St & Walnut St   
        76  S Bouquet Ave & Sennott St
        72  O'Hara St and University Place (Soldiers and Sailors Memorial)
        68  S Negley Ave & Baum Blvd
        63  Glasshouse
        62  Forbes Ave & Grant St
        54  First Ave & B St (T Station)
        53  South Side Trail & S 4th St
        51  21st St & Penn Ave

SRC_SHA256 by rows
      2.9K  b0f781e9ee48ad41667acf18ee6cd3a70dde44bb7524cb53019360b36b868ce9

## who x when

TO_STATION_NAME by STARTTIME
  21st St & Penn Ave                        2022:73
  33rd St & Penn Ave                        2022:54
  Burns White Center at 3 Crossings         2022:47
  Ellsworth Ave & N Neville St              2022:47
  Fifth Ave & S Bouquet St                  2022:93
  Forbes Ave & Market Square                2022:80
  Glasshouse                                2022:72
  Hot Metal St & Tunnel Blvd                2022:70
  Isabella St & Federal St (PNC Park)       2022:79
  Ivy St & Walnut St                        2022:48
  Liberty Ave & Stanwix St                  2022:136
  Microsoft                                 2022:84
  North Shore Trail & Fort Duquesne Bridge  2022:194
  S 18th St & Sidney St                     2022:135
  S 27th St & Sidney St. (Southside Works)  2022:136
  S Bouquet Ave & Sennott St                2022:49
  S Negley Ave & Baum Blvd                  2022:82
  Schenley Dr & Forbes Ave (Schenley Plaza  2022:117
  Schenley Dr at Schenley Plaza (Carnegie   2022:77
  Zulema St & Coltart Ave                   2022:51

FROM_STATION_NAME by STARTTIME
  21st St & Penn Ave                        2022:51
  Fifth Ave & S Bouquet St                  2022:118
  First Ave & B St (T Station)              2022:54
  Forbes Ave & Grant St                     2022:62
  Forbes Ave & Market Square                2022:96
  Glasshouse                                2022:63
  Hot Metal St & Tunnel Blvd                2022:82
  Isabella St & Federal St (PNC Park)       2022:81
  Ivy St & Walnut St                        2022:77
  Liberty Ave & Stanwix St                  2022:137
  Microsoft                                 2022:87
  North Shore Trail & Fort Duquesne Bridge  2022:178
  O'Hara St and University Place (Soldiers  2022:72
  S 18th St & Sidney St                     2022:114
  S 27th St & Sidney St. (Southside Works)  2022:123
  S Bouquet Ave & Sennott St                2022:76
  S Negley Ave & Baum Blvd                  2022:68
  Schenley Dr & Forbes Ave (Schenley Plaza  2022:126
  Schenley Dr at Schenley Plaza (Carnegie   2022:95
  South Side Trail & S 4th St               2022:53

## what

FROM_STATION_ID: 1000 12%, 1095 11%, 1045 11%, 1041 10%, 1048 10%, 1001 8%, 1036 8%, 49801 8%, 1084 7%, 1013 7%, 1033 7%

TO_STATION_ID: 1045 12%, 1000 12%, 1048 12%, 1095 11%, 1041 9%, 49801 8%, 1024 8%, 1001 7%, 1013 7%, 1036 7%, 1017 7%

USERTYPE: Customer 56%, Subscriber 44%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| TRIP_ID | id | 2.9K | 0 | 142255482 15; 142254319 15; 142254302 15; 142254301 15 |
| STARTTIME | date | 2.5K | 0 | 4/30/2022 21:37 17; 4/29/2022 14:51 16; 4/29/2022 11:41 16; 4/24/2022 22:23 16 |
| STOPTIME | date | 2.5K | 0 | 4/30/2022 20:15 17; 4/24/2022 19:22 17; 4/30/2022 22:10 16; 4/30/2022 16:46 16 |
| BIKEID | other | 172 | 0 | 70750 47; 70973 43; 70971 40; 70705 40 |
| TRIPDURATION | other | 2.1K | 0 | 506 16; 1607 15; 1979 15; 2023 15 |
| FROM_STATION_ID | category | 41 | 623 | 1000 137; 1095 126; 1045 123; 1041 118 |
| FROM_STATION_NAME | who | 152 | 0 | North Shore Trail & Fort  178; Liberty Ave & Stanwix St 137; Schenley Dr & Forbes Ave  126; S 27th St & Sidney St. (S 123 |
| TO_STATION_ID | category | 40 | 800 | 1045 136; 1000 136; 1048 135; 1095 117 |
| TO_STATION_NAME | who | 193 | 0 | North Shore Trail & Fort  194; S 27th St & Sidney St. (S 136; Liberty Ave & Stanwix St 136; S 18th St & Sidney St 135 |
| USERTYPE | category | 3 | 1 | Customer 1.6K; Subscriber 1.3K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:29:08.99098 2.9K |
| SOURCE_RUN_ID | audit | 1 | 0 | 23996c88-4a28-4b73-b1ff-4 2.9K |
| SRC_SHA256 | who | 1 | 0 | b0f781e9ee48ad41667acf18e 2.9K |
