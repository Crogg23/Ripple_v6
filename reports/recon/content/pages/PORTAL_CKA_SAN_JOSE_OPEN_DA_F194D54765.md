# PORTAL_CKA_SAN_JOSE_OPEN_DA_F194D54765

rows 10.0K  columns 67  scan 5.8s

roles: amount 4, audit 2, category 36, date 2, empty 1, id 7, other 6, who 10

## when

DATEDIMID
  2020      4.3K  ############################
  2021      4.7K  ##############################
  2022       994  ######

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 10.0K | 6.12M | 6.16M | 6.19M | 6.22M | 61.64B |
| Y | 10.0K | 1.89M | 1.94M | 1.97M | 1.99M | 19.42B |
| LATITUDE | 10.0K | 37.17 | 37.32 | 37.41 | 37.45 | 373.2K |
| LONGITUDE | 10.0K | -122.03 | -121.87 | -121.77 | -121.68 | -1.22M |

## who

CRASHNAME by rows
         1  CR-0000080170
         1  CR-0000080153
         1  CR-0000093255
         1  CR-0000082602
         1  CR-0000082007
         1  CR-0000093242
         1  CR-0000082566
         1  CR-0000082511
         1  CR-0000082599
         1  CR-0000082523
         1  CR-0000093269
         1  CR-0000082545
         1  CR-0000080167
         1  CR-0000082338
         1  CR-0000080145
         1  CR-0000085198
         1  CR-0000082539
         1  CR-0000082501
         1  CR-0000080163
         1  CR-0000080151

CRASHNAME by dollars
       6.22M        1 rows  CR-0000090754
       6.22M        1 rows  CR-0000084330
       6.22M        1 rows  CR-0000084872
       6.21M        1 rows  CR-0000086545
       6.21M        1 rows  CR-0000082784
       6.21M        1 rows  CR-0000082402
       6.21M        1 rows  CR-0000091083
       6.21M        1 rows  CR-0000085103
       6.21M        1 rows  CR-0000082024
       6.21M        1 rows  CR-0000082365
       6.21M        1 rows  CR-0000086970
       6.21M        1 rows  CR-0000090667
       6.20M        1 rows  CR-0000086355
       6.20M        1 rows  CR-0000083443
       6.20M        1 rows  CR-0000088868
       6.20M        1 rows  CR-0000089210
       6.20M        1 rows  CR-0000088220
       6.20M        1 rows  CR-0000087716
       6.20M        1 rows  CR-0000084878
       6.20M        1 rows  CR-0000091097

INTASTREETNAME by rows
       365  CAPITOL EX
       225  KING RD
       215  BLOSSOM HILL RD
       191  FIRST ST
       166  ALUM ROCK AV
       154  ELEVENTH ST
       147  ALMADEN EX
       146  MONTEREY RD
       144  CAPITOL AV
       127  BRANHAM LN
       126  MCLAUGHLIN AV
       110  SANTA CLARA ST
       106  BASCOM AV
       103  BAYSHORE FR
        96  BERRYESSA RD
        86  CURTNER AV
        85  ALMA AV
        84  FOURTH ST
        83  JULIAN ST
        80  CAMDEN AV

INTASTREETNAME by dollars
       2.25B      365 rows  CAPITOL EX
       1.39B      225 rows  KING RD
       1.33B      215 rows  BLOSSOM HILL RD
       1.18B      191 rows  FIRST ST
       1.02B      166 rows  ALUM ROCK AV
     948.80M      154 rows  ELEVENTH ST
     905.77M      147 rows  ALMADEN EX
     900.98M      146 rows  MONTEREY RD
     888.28M      144 rows  CAPITOL AV
     783.09M      127 rows  BRANHAM LN
     777.43M      126 rows  MCLAUGHLIN AV
     677.79M      110 rows  SANTA CLARA ST
     651.29M      106 rows  BASCOM AV
     635.21M      103 rows  BAYSHORE FR
     591.75M       96 rows  BERRYESSA RD
     529.60M       86 rows  CURTNER AV
     523.75M       85 rows  ALMA AV
     517.24M       84 rows  FOURTH ST
     511.31M       83 rows  JULIAN ST
     492.09M       80 rows  CAMDEN AV

INTBSTREETNAME by rows
       353  STORY RD
       304  TULLY RD
       236  WHITE RD
       197  MONTEREY RD
       192  TENTH ST
       182  SENTER RD
       136  SNELL AV
       132  MCKEE RD
       114  SINCLAIR FR
       111  SANTA TERESA BL
       107  SAN CARLOS ST
        98  SANTA CLARA ST
        96  SEVENTH ST
        96  MERIDIAN AV
        93  SARATOGA AV
        89  WILLIAM ST
        88  MCLAUGHLIN AV
        85  OAKLAND RD
        83  STEVENS CREEK BL
        81  TAYLOR ST

INTBSTREETNAME by dollars
       2.18B      353 rows  STORY RD
       1.88B      304 rows  TULLY RD
       1.46B      236 rows  WHITE RD
       1.22B      197 rows  MONTEREY RD
       1.18B      192 rows  TENTH ST
       1.12B      182 rows  SENTER RD
     839.60M      136 rows  SNELL AV
     814.34M      132 rows  MCKEE RD
     703.13M      114 rows  SINCLAIR FR
     686.30M      111 rows  SANTA TERESA BL
     658.42M      107 rows  SAN CARLOS ST
     603.50M       98 rows  SANTA CLARA ST
     591.57M       96 rows  SEVENTH ST
     590.67M       96 rows  MERIDIAN AV
     570.26M       93 rows  SARATOGA AV
     548.46M       89 rows  WILLIAM ST
     543.30M       88 rows  MCLAUGHLIN AV
     523.31M       85 rows  OAKLAND RD
     509.40M       83 rows  STEVENS CREEK BL
     498.55M       81 rows  TAYLOR ST

VEHICLEDAMAGE by rows
      1.7K  Unknown, Unknown
       838  Major, Major
       751  Moderate, Moderate
       721  Minor, Minor
       603  Major
       456  Minor, Unknown
       294  Major, Moderate
       275  Moderate
       235  Moderate, Unknown
       222  Moderate, Major
       217  Not Applicable, Unknown
       216  Moderate, Minor
       170  Minor, Moderate
       158  Minor, Not Applicable
       155  Major, Minor
       154  Unknown
       150  Not Applicable, Minor
       146  Minor
       145  Unknown, Minor
       139  None, Not Applicable

VEHICLEDAMAGE by dollars
      10.50B     1.7K rows  Unknown, Unknown
       5.16B      838 rows  Major, Major
       4.63B      751 rows  Moderate, Moderate
       4.44B      721 rows  Minor, Minor
       3.72B      603 rows  Major
       2.81B      456 rows  Minor, Unknown
       1.81B      294 rows  Major, Moderate
       1.70B      275 rows  Moderate
       1.45B      235 rows  Moderate, Unknown
       1.37B      222 rows  Moderate, Major
       1.34B      217 rows  Not Applicable, Unknown
       1.33B      216 rows  Moderate, Minor
       1.05B      170 rows  Minor, Moderate
     973.59M      158 rows  Minor, Not Applicable
     955.23M      155 rows  Major, Minor
     949.34M      154 rows  Unknown
     924.63M      150 rows  Not Applicable, Minor
     899.99M      146 rows  Minor
     893.84M      145 rows  Unknown, Minor
     856.47M      139 rows  None, Not Applicable

## who x when

CRASHNAME by DATEDIMID, dollars = X
  CR-0000080145                             2020:6.16M
  CR-0000080151                             2020:6.18M
  CR-0000080153                             2020:6.18M
  CR-0000080163                             2020:6.16M
  CR-0000080167                             2020:6.16M
  CR-0000080170                             2020:6.18M
  CR-0000082007                             2020:6.16M
  CR-0000082024                             2020:6.21M
  CR-0000082338                             2020:6.15M
  CR-0000082365                             2020:6.21M
  CR-0000082402                             2020:6.21M
  CR-0000082501                             2020:6.17M
  CR-0000082511                             2020:6.16M
  CR-0000082523                             2020:6.18M
  CR-0000082539                             2020:6.15M
  CR-0000082545                             2020:6.15M
  CR-0000082566                             2020:6.19M
  CR-0000082599                             2020:6.16M
  CR-0000082602                             2020:6.15M
  CR-0000082784                             2020:6.21M
  CR-0000084330                             2020:6.22M
  CR-0000084872                             2020:6.22M
  CR-0000085103                             2020:6.21M
  CR-0000085198                             2020:6.16M
  CR-0000086545                             2021:6.21M
  CR-0000090754                             2022:6.22M
  CR-0000091083                             2022:6.21M
  CR-0000093242                             2020:6.13M
  CR-0000093255                             2020:6.13M
  CR-0000093269                             2020:6.15M

INTASTREETNAME by DATEDIMID, dollars = X
  ALMA AV                                   2020:252.63M 2021:252.64M 2022:18.48M
  ALMADEN EX                                2020:363.54M 2021:443.65M 2022:98.58M
  ALUM ROCK AV                              2020:512.20M 2021:394.94M 2022:117.24M
  BASCOM AV                                 2020:319.49M 2021:282.64M 2022:49.15M
  BAYSHORE FR                               2020:296.08M 2021:289.72M 2022:49.40M
  BERRYESSA RD                              2020:234.26M 2021:308.18M 2022:49.31M
  BLOSSOM HILL RD                           2020:567.74M 2021:629.41M 2022:129.59M
  BRANHAM LN                                2020:339.11M 2021:357.65M 2022:86.33M
  CAMDEN AV                                 2020:147.67M 2021:313.66M 2022:30.77M
  CAPITOL AV                                2020:339.31M 2021:444.13M 2022:104.84M
  CAPITOL EX                                2020:845.92M 2021:1.13B 2022:277.87M
  CURTNER AV                                2020:172.42M 2021:283.28M 2022:73.90M
  ELEVENTH ST                               2020:486.73M 2021:394.31M 2022:67.77M
  FIRST ST                                  2020:393.82M 2021:658.37M 2022:123.07M
  FOURTH ST                                 2020:209.35M 2021:227.85M 2022:80.03M
  JULIAN ST                                 2020:234.08M 2021:240.27M 2022:36.97M
  KING RD                                   2020:604.73M 2021:654.12M 2022:129.61M
  MCLAUGHLIN AV                             2020:345.50M 2021:327.04M 2022:104.89M
  MONTEREY RD                               2020:364.17M 2021:462.72M 2022:74.09M
  SANTA CLARA ST                            2020:289.60M 2021:326.58M 2022:61.61M

## what

INJURYSEVERITY: Minor 56%, Moderate 25%, Severe 7%, Moderate, Minor 7%, Fatal 2%, Severe, Minor 1%, Severe, Moderate 1%, Severe, Moderate, Minor 0%, Fatal, Severe 0%, Fatal, Minor 0%, Fatal, Moderate 0%

VEHICLECOUNT: 2 74%, 1 13%, 3 10%, 4 2%, 5 1%, 6 0%, 7 0%, 8 0%

VEHICLEDRIVERINTOXICATED: 1 100%

MINORINJURIES: 0 69%, 1 23%, 2 6%, 3 1%, 4 0%, 5 0%, 6 0%

MODERATEINJURIES: 0 84%, 1 14%, 2 1%, 3 0%, 4 0%, 5 0%

SEVEREINJURIES: 0 95%, 1 4%, 2 0%, 3 0%

FATALINJURIES: 0 99%, 1 1%, 2 0%

CITYDAMAGEFLAG: F 90%, T 10%

SHORTFORMFLAG: F 83%, T 17%

ROADWAYSURFACE: Dry 86%, Unknown 9%, Wet 5%, Slippery (Muddy Oily etc.) 0%, Snowy - Icy 0%

ROADWAYCONDITION: No Unusual Conditions 89%, Unknown 10%, Construction - Repair Zone 1%, Other 0%, Loose Material On Roadway 0%, Obstruction On Roadway 0%, Holes Deep Rut 0%, Reduced Roadway Width 0%, Flooded 0%

LIGHTING: Daylight 56%, Dark - Street Light 34%, Dusk - Dawn 5%, Unknown 4%, Dark - No Street Light 1%, Dark - Street Light Not Functi 0%

PRIMARYCOLLISIONFACTOR: Violation Driver 1 74%, Unknown 22%, Bike At Fault 2%, Pedestrian At Fault 1%, Other Than Driver 0%, Violation Driver 2 0%, Other Improper Driving 0%, Parked/Rolling 0%

WEATHER: Clear 84%, Unknown 9%, Cloudy 4%, Rain 3%, Other 0%, Fog 0%, Wind 0%, Snow 0%

COLLISIONTYPE: Rear End 25%, Sideswipe 21%, Broadside 21%, Hit Object 12%, Head On 7%, Vehicle/Pedestrian 6%, Vehicle/Bike 5%, Other 3%, Overturned 0%

VEHICLEINVOLVEDWITH: Other Vehicle 52%, Parked Vehicle 20%, Fixed Object 12%, Pedestrian 5%, Bike 5%, Motorcycle 3%, Motor Vehicle On Other Roadway 1%, Other Object 1%, Non-Collision 0%, Scooter Motorized 0%, Unknown 0%, Train 0%

PEDESTRIANACTION: No Pedestrians Involved 94%, Crossing In Crosswalk - At Int 2%, Crossing - Not In Crosswalk 2%, In Road - Includes Shoulder 1%, Not In Road 0%, Crossing In Crosswalk - Not At 0%, Unknown 0%, Walking 0%

PEDESTRIANDIRECTIONFROM: Not Applicable 94%, South 1%, North 1%, West 1%, East 1%, No Direction (Not Walking) 1%, Unknown 1%

PEDESTRIANDIRECTIONTO: Not Applicable 94%, North 1%, South 1%, East 1%, West 1%, No Direction (Not Walking) 1%, Unknown 1%

DIRECTIONFROMINTERSECTION: At 38%, South Of 16%, North Of 15%, East Of 15%, West Of 14%, Unknown 2%

PROXIMITYTOINTERSECTION: Non-Related 42%, Intersection 39%, Related 20%, Driveway 0%

TRAFFICCONTROL: Controls Functioning 49%, No Controls Present/Factor 40%, Unknown 10%, Controls Not Functioning 1%, Controls Obscured 0%

INTASTREETTYPE: Local (LO) 37%, Arterial (AR) 27%, Major Street (MA) 17%, Neighborhood Collector (NC) 11%, Freeway/Expressway (CA) 8%

INTBSTREETTYPE: Local (LO) 34%, Arterial (AR) 27%, Major Street (MA) 21%, Neighborhood Collector (NC) 14%, Freeway/Expressway (CA) 4%

INTERSECTIONTYPE: 4 Leg 58%, 3 Leg 41%, 2 Leg 1%

INTTRAFFICCONTROLTYPE: Signal 55%, 1 Way Stop 22%, 2 Way Stop 10%, No Control 9%, 4 Way Stop 3%, 3 Way Stop 1%, Yield Sign 0%

HOUR: 17 10%, 16 10%, 18 10%, 14 9%, 15 9%, 19 8%, 21 8%, 13 8%, 20 8%, 12 7%, 22 7%, 11 7%

DAYOFWEEKNAME: Saturday 16%, Friday 16%, Sunday 15%, Wednesday 14%, Monday 13%, Thursday 13%, Tuesday 13%

MONTHNAME: February 12%, January 12%, March 9%, October 9%, August 8%, July 8%, September 8%, November 7%, June 7%, December 7%, May 7%, April 6%

YEAR: 2021 47%, 2020 43%, 2022 10%

LASTUPDATE: 2025/01/25 00:17:39+00 58%, 2023/11/11 00:12:28+00 21%, 2025/01/25 00:13:51+00 16%, 2025/01/25 00:13:50+00 6%, 2024/09/27 23:07:38+00 0%, 2024/07/26 23:07:27+00 0%, 2024/11/01 23:08:39+00 0%, 2024/09/20 23:07:58+00 0%, 2024/06/21 23:07:55+00 0%, 2023/11/25 00:11:19+00 0%, 2025/03/14 23:09:49+00 0%, 2024/10/10 00:00:57+00 0%

DAYNUMBER: 13 9%, 2 9%, 3 9%, 5 9%, 15 8%, 12 8%, 8 8%, 4 8%, 16 8%, 27 8%, 6 8%, 10 8%

REPORTEDLOCATIONFOUND: No 69%, Yes 31%

SPEEDINGFLAG: False 96%, True 4%

HITANDRUNFLAG: False 97%, True 3%

KSIINJURIES: 0 94%, 1 5%, 2 0%, 3 0%, 4 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| X | amount | 6.5K | 0 | 6175956.327646 51; 6156347.29304525 51; 6156505.89016899 51; 6162115.88747916 51 |
| Y | amount | 6.3K | 0 | 1952947.93956581 51; 1948705.76169848 51; 1951582.47838598 51; 1946147.75041032 51 |
| INJURYSEVERITY | category | 16 | 5.2K | Minor 2.7K; Moderate 1.2K; Severe 351; Moderate, Minor 331 |
| OBJECTID | id | 10.1K | 0 | 15300 50; 15299 50; 15298 50; 15297 50 |
| GLOBALID | id | 9.9K | 0 | {8EDCE72A-26BC-4F00-9C71- 50; {3595C229-BD5C-4767-8CA7- 50; {9B1CFD7B-1767-4293-A823- 50; {A0C61A98-009E-4F8A-BFD7- 50 |
| FACILITYID | who | 10.1K | 0 | 588158 50; 587846 50; 587845 50; 588157 50 |
| INTID | id | 10.1K | 0 | 588158 50; 587846 50; 587845 50; 588157 50 |
| TCRNUMBER | id | 9.9K | 0 | 22-073-0671 50; 22-073-0649 50; 22-073-0640 50; 22-074-0202 50 |
| CRASHDATETIME | id | 9.8K | 0 | 2022/03/07 16:00:00+00 51; 2022/03/05 18:40:00+00 51; 2022/03/03 17:24:00+00 51; 2022/03/02 12:00:00+00 51 |
| CRASHDATETIMEUTC | id | 10.0K | 0 | 2022/03/08 00:00:00+00 51; 2022/03/06 02:40:00+00 51; 2022/03/04 01:24:00+00 51; 2022/03/02 20:00:00+00 51 |
| VEHICLECOUNT | category | 9 | 2 | 2 7.4K; 1 1.3K; 3 1.0K; 4 234 |
| VEHICLEPARTYCATEGORY | who | 103 | 2 | Driver, Driver 4.8K; Driver 1.2K; Driver, Parked 1.1K; Parked, Driver 431 |
| VEHICLEVIOLATIONCODEDESCRIPTION | who | 372 | 2 | Unknown, Unknown 1.6K; Speeding, Not Applicable 828; Not Applicable, Speeding 580; Speeding 526 |
| VEHICLEDAMAGE | who | 359 | 16 | Unknown, Unknown 1.7K; Major, Major 838; Moderate, Moderate 751; Minor, Minor 721 |
| VEHICLEDRIVERINTOXICATED | category | 2 | 9.8K | 1 196 |
| MINORINJURIES | category | 7 | 0 | 0 6.9K; 1 2.3K; 2 593; 3 127 |
| MODERATEINJURIES | category | 6 | 0 | 0 8.4K; 1 1.4K; 2 136; 3 9 |
| SEVEREINJURIES | category | 4 | 0 | 0 9.5K; 1 441; 2 19; 3 7 |
| FATALINJURIES | category | 3 | 0 | 0 9.9K; 1 120; 2 4 |
| CITYDAMAGEFLAG | category | 2 | 0 | F 9.0K; T 992 |
| SHORTFORMFLAG | category | 2 | 0 | F 8.3K; T 1.7K |
| ROADWAYSURFACE | category | 5 | 0 | Dry 8.6K; Unknown 875; Wet 466; Slippery (Muddy Oily etc. 14 |
| ROADWAYCONDITION | category | 9 | 0 | No Unusual Conditions 8.9K; Unknown 986; Construction - Repair Zon 61; Other 39 |
| LIGHTING | category | 6 | 0 | Daylight 5.6K; Dark - Street Light 3.4K; Dusk - Dawn 477; Unknown 353 |
| PRIMARYCOLLISIONFACTOR | category | 8 | 0 | Violation Driver 1 7.4K; Unknown 2.2K; Bike At Fault 183; Pedestrian At Fault 142 |
| WEATHER | category | 8 | 0 | Clear 8.4K; Unknown 858; Cloudy 450; Rain 288 |
| COLLISIONTYPE | category | 9 | 0 | Rear End 2.5K; Sideswipe 2.1K; Broadside 2.1K; Hit Object 1.2K |
| VEHICLEINVOLVEDWITH | category | 17 | 0 | Other Vehicle 5.2K; Parked Vehicle 2.0K; Fixed Object 1.2K; Pedestrian 538 |
| PEDESTRIANACTION | category | 8 | 0 | No Pedestrians Involved 9.4K; Crossing In Crosswalk - A 234; Crossing - Not In Crosswa 169; In Road - Includes Should 122 |
| PEDESTRIANDIRECTIONFROM | category | 7 | 0 | Not Applicable 9.4K; South 130; North 124; West 119 |
| PEDESTRIANDIRECTIONTO | category | 7 | 0 | Not Applicable 9.4K; North 136; South 120; East 118 |
| DISTANCE | other | 589 | 891 | 0 3.9K; 51 1.0K; 30 94; 20 93 |
| DIRECTIONFROMINTERSECTION | category | 6 | 0 | At 3.8K; South Of 1.6K; North Of 1.5K; East Of 1.5K |
| PROXIMITYTOINTERSECTION | category | 4 | 0 | Non-Related 4.2K; Intersection 3.9K; Related 2.0K; Driveway 6 |
| TRAFFICCONTROL | category | 5 | 0 | Controls Functioning 4.9K; No Controls Present/Facto 4.0K; Unknown 1.0K; Controls Not Functioning 67 |
| INTASTREETNAME | who | 1.7K | 0 | CAPITOL EX 365; KING RD 225; BLOSSOM HILL RD 215; FIRST ST 191 |
| INTBSTREETNAME | who | 1.7K | 0 | STORY RD 353; TULLY RD 304; WHITE RD 236; MONTEREY RD 197 |
| INTASTREETTYPE | category | 5 | 0 | Local (LO) 3.7K; Arterial (AR) 2.7K; Major Street (MA) 1.7K; Neighborhood Collector (N 1.1K |
| INTBSTREETTYPE | category | 5 | 0 | Local (LO) 3.4K; Arterial (AR) 2.7K; Major Street (MA) 2.1K; Neighborhood Collector (N 1.4K |
| INTERSECTIONTYPE | category | 4 | 2 | 4 Leg 5.8K; 3 Leg 4.1K; 2 Leg 117 |
| INTTRAFFICCONTROLTYPE | category | 7 | 0 | Signal 5.5K; 1 Way Stop 2.2K; 2 Way Stop 970; No Control 915 |
| INTERSECTIONNUMBER | other | 3.6K | 0 | 32999 57; 79617 57; 90045 55; 47497 53 |
| INTERSECTIONDIMID | other | 3.6K | 0 | 12474 57; 1583 57; 9065 55; 3689 53 |
| DATEDIMID | date | 787 | 0 | 20220303 68; 20220212 66; 20220305 62; 20220205 62 |
| HOUR | category | 24 | 0 | 17 688; 16 664; 18 639; 14 573 |
| DAYOFWEEKNAME | category | 7 | 0 | Saturday 1.6K; Friday 1.6K; Sunday 1.5K; Wednesday 1.4K |
| MONTHNAME | category | 12 | 0 | February 1.2K; January 1.2K; March 911; October 865 |
| YEAR | category | 3 | 0 | 2021 4.7K; 2020 4.3K; 2022 994 |
| LASTUPDATE | category | 25 | 0 | 2025/01/25 00:17:39+00 5.8K; 2023/11/11 00:12:28+00 2.1K; 2025/01/25 00:13:51+00 1.6K; 2025/01/25 00:13:50+00 560 |
| LASTEDITOR | other | 1 | 0 | FME 10.0K |
| NOTES | empty | 2 | 10.0K |  |
| ENTERPRISEID | id | 10.1K | 0 | DOT-VZCF-0000588158 50; DOT-VZCF-0000587846 50; DOT-VZCF-0000587845 50; DOT-VZCF-0000588157 50 |
| DAYNUMBER | category | 31 | 0 | 13 366; 2 365; 3 364; 5 360 |
| NARRATIVE | other | 6.0K | 2 | Unspecified driver vs par 603; Unspecified driver vs obj 301; Unspecified driver vs 2 p 155; Unspecified driver vs par 89 |
| AGERANGE | who | 161 | 1.6K | 30-49 1.6K; 16-29 1.6K; 50-64 743; 30-49, 30-49 554 |
| CRASHNAME | who | 9.8K | 0 | CR-0000091537 50; CR-0000091096 50; CR-0000091041 50; CR-0000091535 50 |
| LATITUDE | amount | 6.4K | 0 | 37.35083339 51; 37.33840063 51; 37.34630706 51; 37.33161023 51 |
| LONGITUDE | amount | 6.3K | 0 | -121.843109 52; -121.8270065 51; -121.8942427 51; -121.8938446 51 |
| INTERSECTIONNUMBERINT | other | 3.6K | 0 | 32999 57; 79617 57; 90045 55; 47497 53 |
| REPORTEDLOCATIONFOUND | category | 2 | 0 | No 6.9K; Yes 3.1K |
| SPEEDINGFLAG | category | 2 | 0 | False 9.6K; True 378 |
| HITANDRUNFLAG | category | 2 | 0 | False 9.7K; True 338 |
| KSIINJURIES | category | 5 | 0 | 0 9.4K; 1 534; 2 26; 3 10 |
| NEARBYSAFETYCORRIDORS | who | 92 | 5.5K | Monterey Road 222; First St 206; Story Rd 205; Capitol Expressway 184 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:44:27.48826 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 674bf428-dacc-48ed-84ef-0 10.0K |
| SRC_SHA256 | who | 1 | 0 | 2909e4d2c7565b6a9413c8c58 10.0K |
