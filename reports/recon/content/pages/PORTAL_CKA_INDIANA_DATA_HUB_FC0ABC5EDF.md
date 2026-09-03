# PORTAL_CKA_INDIANA_DATA_HUB_FC0ABC5EDF

rows 10.0K  columns 65  scan 3.7s

roles: audit 2, category 40, date 1, empty 6, other 12, who 5

## when

INGESTED_AT
  2026     10.0K  ##############################

## who

OFFENSE by rows
       269  failure to appear
       177  fail to appear initial warrant
       158  possession of paraphernalia
       156  mv owi c mis
       152  probation violation initial warrant
       145  failure to appear jail booking
       144  mv owi bac .15 con
       140  domestic battery
       136  criminal trespass
       132  warrant felony
       130  operating a vehicle while into
       122  poss mj hash salvia
       116  operating while intoxicated endangerment
       114  invasion of privacy
       104  mv owi bac+.08 less
       100  possession of cocaine or narcotic drug
        98  hold for outside agency
        96  operating while intoxicated
        96  warrant arrest bartholomew co issued
        92  intimidation

ARRESTING_AGENCY_COUNTY by rows
      2.8K  ALLEN
      1.8K  ST JOSEPH
      1.4K  PORTER
       638  DELAWARE
       449  HAMILTON
       414  VIGO
       341  MADISON
       304  CLARK
       292  BOONE
       200  MONTGOMERY
       194  DUBOIS
       182  BARTHOLOMEW
       140  JOHNSON
       116  TIPPECANOE
       110  LAKE
        72  ELKHART
        70  PUTNAM
        58  PERRY
        54  JASPER
        44  MORGAN

BOOKING_AGENCY_COUNTY by rows
      2.8K  ALLEN
      1.7K  ST JOSEPH
      1.5K  PORTER
       652  DELAWARE
       498  VIGO
       449  HAMILTON
       339  MADISON
       306  CLARK
       292  BOONE
       216  MONTGOMERY
       190  DUBOIS
       190  BARTHOLOMEW
       136  JOHNSON
        96  TIPPECANOE
        68  ELKHART
        62  PERRY
        58  LAKE
        56  JASPER
        54  MORGAN
        44  MARSHALL

OFFENSE_COUNTY by rows
      5.0K  IN
      1.4K  ALLEN
       875  ST JOSEPH
       742  PORTER
       327  DELAWARE
       249  VIGO
       224  HAMILTON
       170  MADISON
       153  CLARK
       146  BOONE
       108  MONTGOMERY
        95  DUBOIS
        95  BARTHOLOMEW
        68  JOHNSON
        48  TIPPECANOE
        34  ELKHART
        31  PERRY
        29  LAKE
        28  JASPER
        27  MORGAN

## who x when

OFFENSE by INGESTED_AT  LOAD STAMP, not an event date
  criminal trespass                         2026:136
  domestic battery                          2026:140
  fail to appear initial warrant            2026:177
  failure to appear                         2026:269
  failure to appear jail booking            2026:145
  hold for outside agency                   2026:98
  intimidation                              2026:92
  invasion of privacy                       2026:114
  mv owi bac .15 con                        2026:144
  mv owi bac+.08 less                       2026:104
  mv owi c mis                              2026:156
  operating a vehicle while into            2026:130
  operating while intoxicated               2026:96
  operating while intoxicated endangerment  2026:116
  poss mj hash salvia                       2026:122
  possession of cocaine or narcotic drug    2026:100
  possession of paraphernalia               2026:158
  probation violation initial warrant       2026:152
  warrant arrest bartholomew co issued      2026:96
  warrant felony                            2026:132

ARRESTING_AGENCY_COUNTY by INGESTED_AT  LOAD STAMP, not an event date
  ALLEN                                     2026:2.8K
  BARTHOLOMEW                               2026:182
  BOONE                                     2026:292
  CLARK                                     2026:304
  DELAWARE                                  2026:638
  DUBOIS                                    2026:194
  ELKHART                                   2026:72
  HAMILTON                                  2026:449
  JASPER                                    2026:54
  JOHNSON                                   2026:140
  LAKE                                      2026:110
  MADISON                                   2026:341
  MONTGOMERY                                2026:200
  MORGAN                                    2026:44
  PERRY                                     2026:58
  PORTER                                    2026:1.4K
  PUTNAM                                    2026:70
  ST JOSEPH                                 2026:1.8K
  TIPPECANOE                                2026:116
  VIGO                                      2026:414

## what

OFFENDER_AGE_GROUP: 25-34 Years 32%, 35-44 Years 29%, 15-24 Years 16%, 45-54 Years 15%, 55-64 Years 6%, 65+ Years 2%

OFFENDER_RACE: WHITE 68%, BLACK 30%, OTHER 1%, UNKNOWN 1%

OFFENDER_SEX: MALE 75%, FEMALE 25%

OFFENSE_YEAR: 2024 96%, 2023 2%, 2022 0%, 2013 0%, 2018 0%, 2016 0%, 2021 0%, 2017 0%, 2015 0%, 2011 0%, 2014 0%, 2020 0%

ARREST_MONTH: 10 40%, 11 35%, 12 25%

ARRESTING_AGENCY_TYPE: POLICE (LOCAL) 50%, SHERIFF 47%, ISP 2%, STATUTORY POLICE 0%, PROSECUTING ATTORNEY 0%, OTHERS 0%, ISEP 0%

BOOKING_AGENCY_TYPE: SHERIFF 91%, POLICE (LOCAL) 9%, ISP 0%, STATUTORY POLICE 0%, UNKNOWN 0%

BOOKING_AGENCY_STATE: IN 100%

CHARGE_NO: 1 60%, 0 29%, 2 5%, 3 3%, 4 1%, 5 1%, 6 0%, 7 0%, 8 0%, 9 0%, 10 0%, 14 0%

OFFENSE_STAGE: ORIGINAL 1 100%, FILED 0%

OFFENSE_STAGE_ORDER_IS_MAX: 1 84%, 0 16%

OFFENSE_CLASS: A 38%, 6 29%, C 14%, B 8%, 5 6%, 4 2%, 3 1%, 2 1%, 1 0%, D 0%, N 0%

OFFENSE_LEVEL: M 60%, F 39%, I 0%, C 0%

CHARGE_TYPE: Procedural 27%, Traffic 21%, Drug 17%, Violent 13%, Property 9%, Other 6%, Fraud 2%, Firearm 2%, Child 1%, Sex 1%, Alcohol 1%

DRUG_RELATED: Alcohol 47%, Paraphernalia 16%, Marijuana 13%, Meth 9%, Cocaine or Opioid 6%, Other 3%, Controlled Substance 3%, Cocaine 2%, Opioid 1%, Nuisance 0%

OFFENSE_CATEGORY_TYPE: primary 94%, secondary 6%

OFFENSE_CATEGORY_1: drug 19%, traffic 16%, Uncategorized 16%, court offenses 16%, crime-general 10%, property 8%, violence 8%, child 2%, weapon 1%, fraud 1%, sex 0%

OFFENSE_CATEGORY_2: Uncategorized 22%, traffic-impairment 14%, other 13%, failure to appear 9%, warrant 8%, paraphernalia 6%, alcohol 5%, theft/conversion 5%, domestic battery 5%, marijuana 4%, resisting law enforcement 4%, meth 4%

OFFENSE_CATEGORY_3: Uncategorized 69%, possession 12%, drug or alcohol OVWI 8%, traffic 3%, alcohol OVWI (DUI, OWI) 2%, DWS (driving while suspended) 2%, dealing 1%, syringe 1%, public intoxication 1%, ONL (operator never licensed) 1%, reckless driving 1%, minor 0%

FIREARM: 0 97%, 1 3%

FRAUD: 0 98%, 1 2%

CHILD: 0 96%, 1 4%

OTHER: 0 96%, 1 4%

HOLD: 0 97%, 1 3%

PROCEDURAL: 0 70%, 1 30%

PROPERTY: 0 91%, 1 9%

SEX: 0 98%, 1 2%

TRAFFIC: 0 78%, 1 22%

VIOLENT: 0 87%, 1 13%

ALCOHOL: 0 85%, 1 15%

COCAINE: 0 98%, 1 2%

COMMON_NUISANCE: 0 100%, 1 0%

CONTROLLED_SUBSTANCE: 0 99%, 1 1%

DRUG_GENERAL: 0 95%, 1 5%

HEROIN: 0 100%, 1 0%

MARIJUANA: 0 96%, 1 4%

METH: 0 97%, 1 3%

NARCOTIC: 0 98%, 1 2%

PARAPHERNALIA: 0 95%, 1 5%

DISMISSED_FLAG: 0 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OFFENDER_STATE_ID_HASHED | other | 3.5K | 0 | 4C0778ECDC091F0C2D8968B96 77; 2F2A12BF540A4B895776E41E2 61; 56A4169E45AFAC49417CC4E03 60; 64DD6FAE03D0741C9B5D09FC0 60 |
| OFFENDER_STATE | other | 1 | 0 | IN 10.0K |
| OFFENDER_AGE_GROUP | category | 6 | 0 | 25-34 Years 3.2K; 35-44 Years 2.9K; 15-24 Years 1.6K; 45-54 Years 1.5K |
| OFFENDER_RACE | category | 4 | 0 | WHITE 6.8K; BLACK 3.0K; OTHER 146; UNKNOWN 118 |
| OFFENDER_SEX | category | 2 | 0 | MALE 7.5K; FEMALE 2.5K |
| OFFENSE_YEAR | category | 18 | 0 | 2024 9.5K; 2023 236; 2022 46; 2013 32 |
| OFFENSE_COUNTY_FIPS | other | 53 | 0 | 0 5.0K; 3 1.4K; 141 875; 127 742 |
| OFFENSE_COUNTY | who | 52 | 0 | IN 5.0K; ALLEN 1.4K; ST JOSEPH 875; PORTER 742 |
| OFFENSE_STATE_FIPS | other | 1 | 0 | 18 10.0K |
| OFFENSE_STATE | other | 1 | 0 | IN 10.0K |
| ARREST_ID_HASHED | other | 3.8K | 0 | 605E77DDC8CA8D3CFC803DC2A 77; 26F61940A39600B2462D6CACC 61; 6FCC8203CA54E967D023FF2F2 60; 3EF7298F18DB5ABD96CC17FAF 59 |
| ARREST_YEAR | other | 1 | 0 | 2024 10.0K |
| ARREST_MONTH | category | 3 | 0 | 10 4.0K; 11 3.5K; 12 2.5K |
| ARRESTING_AGENCY_TYPE | category | 7 | 0 | POLICE (LOCAL) 5.0K; SHERIFF 4.7K; ISP 226; STATUTORY POLICE 44 |
| ARRESTING_AGENCY_COUNTY | who | 53 | 0 | ALLEN 2.8K; ST JOSEPH 1.8K; PORTER 1.4K; DELAWARE 638 |
| ARRESTING_AGENCY_STATE | other | 1 | 0 | IN 10.0K |
| BOOKING_AGENCY_TYPE | category | 5 | 0 | SHERIFF 9.1K; POLICE (LOCAL) 864; ISP 38; STATUTORY POLICE 14 |
| BOOKING_AGENCY_COUNTY | who | 52 | 6 | ALLEN 2.8K; ST JOSEPH 1.7K; PORTER 1.5K; DELAWARE 652 |
| BOOKING_AGENCY_STATE | category | 2 | 6 | IN 10.0K |
| CHARGE_NO | category | 23 | 0 | 1 6.0K; 0 2.9K; 2 477; 3 260 |
| OFFENSE_ID_HASHED | other | 4.8K | 0 | 85344F8F6E1CACD615F4B07E2 52; C0AC982C632792453B7BBF138 52; 651276DB794A8BD3C1D8754FF 51; CFFA467D0C6939D224FEE3DB1 51 |
| OFFENSE_STAGE | category | 2 | 0 | ORIGINAL 1 10.0K; FILED 8 |
| OFFENSE_STAGE_ORDER_IS_MAX | category | 2 | 0 | 1 8.4K; 0 1.6K |
| OFFENSE_CLASS | category | 12 | 2 | A 3.8K; 6 2.9K; C 1.4K; B 840 |
| OFFENSE_LEVEL | category | 5 | 2 | M 6.0K; F 3.9K; I 40; C 6 |
| OFFENSE_STATUTE | empty | 1 | 10.0K |  |
| OFFENSE_IC_TITLE_DESC | empty | 1 | 10.0K |  |
| OFFENSE_IC_ARTICLE_DESC | empty | 1 | 10.0K |  |
| OFFENSE_IC_CHAPTER_DESC | empty | 1 | 10.0K |  |
| OFFENSE_IC_SECTION_DESC | empty | 1 | 10.0K |  |
| OFFENSE | who | 933 | 0 | failure to appear 269; fail to appear initial wa 178; possession of paraphernal 163; mv owi c mis 160 |
| CHARGE_TYPE | category | 11 | 0 | Procedural 2.7K; Traffic 2.1K; Drug 1.7K; Violent 1.3K |
| DRUG_RELATED | category | 11 | 6.8K | Alcohol 1.5K; Paraphernalia 492; Marijuana 426; Meth 271 |
| OFFENSE_CATEGORY_TYPE | category | 2 | 0 | primary 9.4K; secondary 631 |
| OFFENSE_CATEGORY_1 | category | 11 | 0 | drug 1.9K; traffic 1.6K; Uncategorized 1.6K; court offenses 1.6K |
| OFFENSE_CATEGORY_2 | category | 46 | 0 | Uncategorized 1.6K; traffic-impairment 1.0K; other 976; failure to appear 645 |
| OFFENSE_CATEGORY_3 | category | 18 | 0 | Uncategorized 6.8K; possession 1.2K; drug or alcohol OVWI 810; traffic 308 |
| FIREARM | category | 2 | 0 | 0 9.7K; 1 330 |
| FRAUD | category | 2 | 0 | 0 9.8K; 1 232 |
| CHILD | category | 2 | 0 | 0 9.6K; 1 368 |
| OTHER | category | 2 | 0 | 0 9.6K; 1 422 |
| HOLD | category | 2 | 0 | 0 9.7K; 1 310 |
| PROCEDURAL | category | 2 | 0 | 0 7.0K; 1 3.0K |
| PROPERTY | category | 2 | 0 | 0 9.1K; 1 931 |
| SEX | category | 2 | 0 | 0 9.8K; 1 152 |
| TRAFFIC | category | 2 | 0 | 0 7.8K; 1 2.2K |
| VIOLENT | category | 2 | 0 | 0 8.7K; 1 1.3K |
| ALCOHOL | category | 2 | 0 | 0 8.5K; 1 1.5K |
| COCAINE | category | 2 | 0 | 0 9.8K; 1 248 |
| COMMON_NUISANCE | category | 2 | 0 | 0 10.0K; 1 12 |
| CONTROLLED_SUBSTANCE | category | 2 | 0 | 0 9.9K; 1 92 |
| DRUG_GENERAL | category | 2 | 0 | 0 9.5K; 1 518 |
| HEROIN | category | 2 | 0 | 0 10.0K; 1 2 |
| MARIJUANA | category | 2 | 0 | 0 9.6K; 1 426 |
| METH | category | 2 | 0 | 0 9.7K; 1 271 |
| NARCOTIC | category | 2 | 0 | 0 9.8K; 1 212 |
| OPIUM | other | 1 | 0 | 0 10.0K |
| PARAPHERNALIA | category | 2 | 0 | 0 9.5K; 1 492 |
| PRESCRIPTION | other | 1 | 0 | 0 10.0K |
| SNIFFING | other | 1 | 0 | 0 10.0K |
| DISPOSITION | empty | 1 | 10.0K |  |
| DISMISSED_FLAG | category | 2 | 10.0K | 0 8 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:04:16.65579 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | faaf88bd-3d13-4e44-9642-f 10.0K |
| SRC_SHA256 | who | 1 | 0 | 8551c89d57426f6706c45a28c 10.0K |
