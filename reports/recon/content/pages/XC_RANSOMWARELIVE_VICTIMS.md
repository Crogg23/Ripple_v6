# XC_RANSOMWARELIVE_VICTIMS

rows 31.1K  columns 12  scan 3.4s

roles: audit 2, category 1, date 2, id 2, other 3, who 2

## when

DISCOVERED
  2013         2  
  2014         2  
  2015         6  
  2016        16  
  2017        40  
  2018        21  
  2019        55  
  2020       247  #
  2021      1.8K  #######
  2022      2.8K  ##########
  2023      5.3K  ####################
  2024      6.1K  #######################
  2025      8.1K  ##############################
  2026      6.5K  ########################

PUBLISHED
  2013         2  
  2014         2  
  2015         7  
  2016        16  
  2017        40  
  2018        21  
  2019        55  
  2020       270  #
  2021      1.8K  #######
  2022      3.2K  ############
  2023      5.4K  ####################
  2024      6.1K  #######################
  2025      8.0K  ##############################
  2026      6.2K  #######################

## who

GROUP_NAME by rows
      2.2K  qilin
      2.0K  lockbit3
      1.6K  akira
      1.3K  clop
      1.3K  play
      1.0K  lockbit2
       913  incransom
       842  ransomhub
       778  thegentlemen
       731  alphv
       641  dragonforce
       552  bianlian
       547  safepay
       523  blackbasta
       517  medusa
       455  8base
       416  lynx
       392  everest
       351  conti
       344  dispossessor

SRC_SHA256 by rows
     31.1K  fef4b5e5eb2f507ad3f3843e9029d0b0fe4c268ce77480ba4218fe09474823e9

## who x when

GROUP_NAME by DISCOVERED
  8base                                     2023:278 2024:148 2025:29
  akira                                     2023:163 2024:317 2025:750 2026:342
  alphv                                     2021:14 2022:31 2023:627 2024:59
  bianlian                                  2022:90 2023:261 2024:169 2025:32
  blackbasta                                2022:156 2023:174 2024:185 2025:8
  clop                                      2020:4 2022:122 2023:388 2024:93 2025:518 2026:215
  conti                                     2020:11 2021:180 2022:160
  dispossessor                              2024:344
  dragonforce                               2023:21 2024:93 2025:221 2026:306
  everest                                   2021:35 2022:76 2023:22 2024:58 2025:107 2026:94
  incransom                                 2023:46 2024:165 2025:388 2026:314
  lockbit2                                  2021:429 2022:573
  lockbit3                                  2022:393 2023:1.0K 2024:537 2025:41
  lynx                                      2024:86 2025:270 2026:60
  medusa                                    2023:145 2024:213 2025:153 2026:6
  play                                      2022:36 2023:318 2024:367 2025:391 2026:192
  qilin                                     2022:1 2023:50 2024:186 2025:1.1K 2026:900
  ransomhub                                 2024:609 2025:233
  safepay                                   2024:46 2025:376 2026:125
  thegentlemen                              2025:80 2026:698

SRC_SHA256 by DISCOVERED
  fef4b5e5eb2f507ad3f3843e9029d0b0fe4c268c  2013:2 2014:2 2015:6 2016:16 2017:40 2018:21 2019:55 2020:247 2021:1.8K 2022:2.8K 2023:5.3K 2024:6.1K 2025:8.1K 2026:6.5K

## what

ACTIVITY: Professional Services 20%, Manufacturing 18%, Technology 13%, Healthcare 9%, Retail & E-Commerce 7%, Financial Services 6%, Transportation 5%, Not Found 5%, Education 5%, Government & Defense 5%, Agriculture and Food Productio 4%, Energy & Utilities 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| POST_TITLE | id | 30.2K | 0 | Swansea, Massachusetts Po 156; Greenland 156; Durham, N.H. police depar 156; Dickson County Sheriff’s  156 |
| GROUP_NAME | who | 360 | 0 | qilin 2.2K; lockbit3 2.0K; akira 1.6K; clop 1.3K |
| DISCOVERED | date | 30.6K | 0 | 2023-04-09T14:57:18+00:00 293; 2017-05-12T00:00:00+00:00 180; 2020-06-01T00:00:00+00:00 167; 2020-06-10T00:00:00+00:00 163 |
| PUBLISHED | date | 22.0K | 2 | 2023-04-09T14:57:18+00:00 292; 2017-05-12T00:00:00+00:00 180; 2020-06-01T00:00:00+00:00 167; 2020-06-10T00:00:00+00:00 163 |
| WEBSITE | id | 24.0K | 6.1K | fapsinc.com 127; maersk.com 126; fedex.com 126; renault.fr 126 |
| COUNTRY | other | 188 | 8.1K | US 10.2K; GB 1.1K; CA 1.1K; DE 1.0K |
| ACTIVITY | category | 15 | 2 | Professional Services 5.9K; Manufacturing 5.5K; Technology 3.9K; Healthcare 2.6K |
| DESCRIPTION | other | 20.7K | 6.5K | United States 865; [AI generated] N/A 569; N/A 450; using Zimbra vulnerabilit 276 |
| POST_URL | other | 19.0K | 10.5K | http://tezwsse5czllksjb7c 281; http://malas2urovbyyavjza 266; http://santat7kpllt6iyvqb 120; http://mblogci3rudehaagbr 103 |
| INGESTED_AT | audit | 1 | 0 | 1787444494054195 31.1K |
| SOURCE_RUN_ID | audit | 1 | 0 | 112b662a-9058-457d-b887-7 31.1K |
| SRC_SHA256 | who | 1 | 0 | fef4b5e5eb2f507ad3f3843e9 31.1K |
