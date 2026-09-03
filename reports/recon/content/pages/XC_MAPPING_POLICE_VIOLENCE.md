# XC_MAPPING_POLICE_VIOLENCE

rows 15.5K  columns 67  scan 5.4s

roles: amount 10, audit 2, category 24, date 1, empty 1, id 7, other 8, state 1, who 13

## when

DATE_OF_INCIDENT_MONTH_DAY_YEAR
  2013      1.1K  #########################
  2014      1.0K  #########################
  2015      1.1K  ##########################
  2016      1.1K  #########################
  2017      1.1K  ##########################
  2018      1.1K  ###########################
  2019      1.1K  ##########################
  2020      1.2K  ###########################
  2021      1.1K  ###########################
  2022      1.2K  ############################
  2023      1.2K  #############################
  2024      1.3K  ##############################
  2025      1.2K  ############################
  2026       638  ###############

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 14.5K | 19.04 | 36.02 | 47.91 | 71.30 | 529.2K |
| LONGITUDE | 14.5K | -171.74 | -93.22 | -71.35 | -67.26 | -1.39M |
| TOTAL_POPULATION_OF_CENSUS_TRACT_2019_ACS_5_YEAR_ESTIMATES | 14.2K | 0 | 1.4K | 4.3K | 18.3K | 21.58M |
| WHITE_NON_HISPANIC_PERCENT_OF_THE_POPULATION_ACS | 14.1K | 0 | 0.54 | 1 | 1 | 7.1K |
| BLACK_NON_HISPANIC_PERCENT_OF_THE_POPULATION_ACS | 14.1K | 0 | 0.05 | 0.97 | 1 | 2.3K |
| NATIVE_AMERICAN_PERCENT_OF_THE_POPULATION_ACS | 14.1K | 0 | 0 | 0.19 | 1 | 135.83 |

## who

VICTIM_S_NAME by rows
       588  Name withheld by police
         4  Michael Johnson
         4  Michael Brown
         4  Name withheld by polce
         3  Daniel Rivera
         3  Richard Rodriguez
         3  Robert Brown
         3  Robert Edwards
         3  Joseph Moreno
         3  Christopher Jones
         3  David Garcia
         2  Joseph Roy
         2  Matthew Graham
         2  Michael Ferguson
         2  Samuel Gonzales
         2  Christopher Anderson
         2  David Willoughby
         2  Victor Rivera
         2  Kenneth Johnson
         2  Darius Smith

VICTIM_S_NAME by dollars
      682.5K      588 rows  Name withheld by police
       18.3K        1 rows  Calvin Elmore
       14.2K        1 rows  Greg Hightower
       14.2K        1 rows  Nathan Humphrey
       12.8K        1 rows  Dustin Alan Rush
       12.6K        1 rows  D'Andre Berghardt Jr.
       11.0K        1 rows  Ryan Thomas Stanush
       11.0K        1 rows  India Nelson
       10.7K        1 rows  Cresencio Rodriguez
       10.0K        1 rows  Jeffrey Alan Martin
        9.3K        1 rows  Alexis Jovany Cardenas
        9.3K        1 rows  Jerry Blaine Barnes Jr
        9.2K        1 rows  Robert Fanello
        8.8K        1 rows  Frankie Salvatore Riccio
        8.7K        4 rows  Michael Johnson
        8.4K        1 rows  Isaac Lemoine Christensen
        8.2K        1 rows  DeOntre L. Dorsey
        8.2K        1 rows  Don Robert Astor
        8.1K        1 rows  Jerry Paul Stovall III
        7.6K        1 rows  Raul Casas Campos

NAMES_OF_OFFICERS_INVOLVED by rows
         4  Juan David Ortiz
         4  Rodolfo Mirabel, Jose Mateo, Richard Santiesteban, Leslie Lee
         3  Watson Morgan
         3  Terry L. Strawn
         3  Joshua Mora
         3  Jonathon Matz
         2  Nick Mills
         2  John Rosello
         2  Edward Agdeppa
         2  Darren Potter
         2  William Dorsey Jones
         2  Andrew Hall
         2  John Aguillon, George Herrera, Jesse Arias, Johnny Longoria
         2  Aidan O’Driscoll, Daniel Rosaia, Trent Collins, Joshua Dequis
         2  Jesse Hiliger
         2  Ryan Phillips
         2  Ronald Anthony Burgos Aviles
         2  Devin Williams Jr.
         2  Brian Mulkeen, Brian Mahon, Robert Wichers, Keith Figueroa, Daniel Bed
         2  Alfonso Perdomo

NAMES_OF_OFFICERS_INVOLVED by dollars
       12.8K        1 rows  D. Delay, J. Carballosa
       11.0K        1 rows  David Dreyer
       10.8K        2 rows  Larry Jones
       10.0K        1 rows  Joshua J. Clark, Tyler L. Clark, Dzevad Isic, Benjamin J. La
        9.9K        3 rows  Terry L. Strawn
        8.9K        4 rows  Rodolfo Mirabel, Jose Mateo, Richard Santiesteban, Leslie Le
        7.4K        1 rows  Joshua Berrios, Dannett Brennan
        7.2K        1 rows  Malik Grego-Smith, Dustin Xaypanya
        7.2K        1 rows  William Michael, Nick Rodriguez
        6.8K        1 rows  Jacob Mekeel, Timothy Brooks, Martin Moran, Danny Kincaid, L
        6.8K        1 rows  Kenneth Pilette, Chad Betts
        6.6K        1 rows  Izak Ackerman
        6.4K        2 rows  Ty Shelton
        6.3K        2 rows  Zachary Adam
        6.0K        1 rows  Charles Garcia
        5.8K        1 rows  James Colucci; Edgar Hernandez
        5.8K        1 rows  Alex Millian
        5.8K        1 rows  Johnny Tuitavake
        5.8K        1 rows  Zach Vercher, Brett Veith
        5.7K        2 rows  Jesse Hiliger

CONGRESSIONAL_REPRESENTATIVE_FULL_NAME_HTTPS_BALLOTPEDIA_ORG_UNITED_STATES_HOUSE_OF_REPRESENTATIVES by rows
       127  Yassamin Ansari
       114  Melanie Stansbury
       100  Gabriel (Gabe) Vasquez
       100  Josh Brecheen
        99  Adelita Grijalva
        88  Wesley Bell
        86  Eli Crane
        86  Nicholas Begich
        85  Jeff Hurd
        84  Jay Obernolte
        83  Carol Miller
        83  Teresa Leger Fernandez
        82  Gabe Evans
        81  Frank Lucas
        80  Aaron Bean
        80  Greg Stanton
        79  David Valadao
        78  Emanuel Cleaver
        77  Doug LaMalfa
        72  Dina Titus

CONGRESSIONAL_REPRESENTATIVE_FULL_NAME_HTTPS_BALLOTPEDIA_ORG_UNITED_STATES_HOUSE_OF_REPRESENTATIVES by dollars
      216.9K      127 rows  Yassamin Ansari
      165.1K       80 rows  Aaron Bean
      162.5K      114 rows  Melanie Stansbury
      142.8K       84 rows  Jay Obernolte
      141.7K       99 rows  Adelita Grijalva
      141.4K       82 rows  Gabe Evans
      137.9K      100 rows  Gabriel (Gabe) Vasquez
      127.4K       80 rows  Greg Stanton
      120.7K       67 rows  Paul Gosar
      120.1K       86 rows  Nicholas Begich
      119.3K       67 rows  Pete Aguilar
      117.4K       79 rows  David Valadao
      114.0K       86 rows  Eli Crane
      111.3K       69 rows  Raul Ruiz
      108.0K       72 rows  Dina Titus
      107.4K       59 rows  Gregorio Casar
      105.4K       56 rows  Celeste Maloy
      103.9K       85 rows  Jeff Hurd
      101.7K      100 rows  Josh Brecheen
      101.5K       83 rows  Teresa Leger Fernandez

ORI_AGENCY_IDENTIFIER_IF_AVAILABLE by rows
       219  CA0194200
       185  AZ0072300
       171  CA0190000
       145  Not Found/No Agency ORI
       140  TXHPD0000
       140  NY0303000
       131  US Marshals
       111  ILCPD0000
       110  TXSPD0000
       103  NV0020100
        83  NM0010100
        81  CA0360000
        78  FL0160200
        76  CA0330000
        71  PAPSP0000
        71  CA0349900
        70  OK0550600
        66  OHCOP0000
        66  PAPEP0000
        62  FL0130000

ORI_AGENCY_IDENTIFIER_IF_AVAILABLE by dollars
      333.0K      219 rows  CA0194200
      306.8K      185 rows  AZ0072300
      301.5K      171 rows  CA0190000
      213.3K      140 rows  TXHPD0000
      196.3K      140 rows  NY0303000
      177.6K      103 rows  NV0020100
      159.1K      110 rows  TXSPD0000
      158.8K      131 rows  US Marshals
      153.3K      145 rows  Not Found/No Agency ORI
      151.6K       78 rows  FL0160200
      145.3K       61 rows  TX1010000
      138.8K      111 rows  ILCPD0000
      134.4K       81 rows  CA0360000
      127.4K       76 rows  CA0330000
      119.1K       83 rows  NM0010100
      107.0K       60 rows  TXDPD0000
      103.9K       58 rows  TX2270100
       96.2K       71 rows  CA0349900
       92.0K       66 rows  OHCOP0000
       91.1K       62 rows  FL0130000

## who x when

VICTIM_S_NAME by DATE_OF_INCIDENT_MONTH_DAY_YEAR, dollars = TOTAL_POPULATION_OF_CENSUS_TRACT_2019_ACS_5_YEAR_ESTIMATES
  Alexis Jovany Cardenas                    2025:9.3K
  Calvin Elmore                             2021:18.3K
  Christopher Anderson                      2014:892 2015:1.0K
  Christopher Jones                         2014:1.2K 2022:2.0K 2023:949
  Cresencio Rodriguez                       2018:10.7K
  D'Andre Berghardt Jr.                     2014:12.6K
  Daniel Rivera                             2020:2.1K 2022:1.8K 2023:1
  Darius Smith                              2015:830 2017:1.1K
  David Garcia                              2013:2.7K 2015:1.4K 2025:1.8K
  David Willoughby                          2018:2.2K 2019:1.1K
  Dustin Alan Rush                          2023:12.8K
  Greg Hightower                            2022:14.2K
  India Nelson                              2017:11.0K
  Jeffrey Alan Martin                       2023:10.0K
  Joseph Moreno                             2013:1.9K 2016:809 2026:1
  Joseph Roy                                2015:1.5K 2022:1.5K
  Kenneth Johnson                           2014:630 2017:1.5K
  Matthew Graham                            2015:673 2019:1.8K
  Michael Brown                             2014:1.1K 2016:1.5K 2017:1.9K 2024:1
  Michael Ferguson                          2016:2.5K 2020:304
  Michael Johnson                           2016:3.4K 2018:1.5K 2022:468 2023:3.3K
  Name withheld by polce                    2026:4
  Name withheld by police                   2013:16.6K 2014:12.1K 2015:2.9K 2016:2.1K 2017:18.1K 2018:30.4K 2019:22.5K 2020:65.6K 2021:70.4K 2022:97.9K 2023:99.6K 2024:118.5K 2025:125.9K 2026:88
  Nathan Humphrey                           2022:14.2K
  Richard Rodriguez                         2013:1.7K 2020:910 2023:2.5K
  Robert Brown                              2013:1.0K 2022:3.0K 2023:717
  Robert Edwards                            2015:2.0K 2017:1.0K
  Ryan Thomas Stanush                       2023:11.0K
  Samuel Gonzales                           2013:379 2019:553
  Victor Rivera                             2013:1.5K 2016:2.1K

NAMES_OF_OFFICERS_INVOLVED by DATE_OF_INCIDENT_MONTH_DAY_YEAR, dollars = TOTAL_POPULATION_OF_CENSUS_TRACT_2019_ACS_5_YEAR_ESTIMATES
  Aidan O’Driscoll, Daniel Rosaia, Trent C  2022:3.9K
  Alfonso Perdomo                           2022:1.5K 2023:1.5K
  Andrew Hall                               2018:1.7K 2021:1.2K
  Brian Mulkeen, Brian Mahon, Robert Wiche  2019:2.8K
  D. Delay, J. Carballosa                   2023:12.8K
  Darren Potter                             2020:2.3K
  David Dreyer                              2017:11.0K
  Devin Williams Jr.                        2022:2
  Edward Agdeppa                            2017:2.1K 2018:755
  Izak Ackerman                             2022:6.6K
  Jacob Mekeel, Timothy Brooks, Martin Mor  2023:6.8K
  Jesse Hiliger                             2021:5.7K
  John Aguillon, George Herrera, Jesse Ari  2017:4.8K
  John Rosello                              2023:938
  Jonathon Matz                             2024:2.8K
  Joshua Berrios, Dannett Brennan           2018:7.4K
  Joshua J. Clark, Tyler L. Clark, Dzevad   2023:10.0K
  Joshua Mora                               2017:1.6K 2023:1.1K
  Juan David Ortiz                          2018:2.0K
  Kenneth Pilette, Chad Betts               2018:6.8K
  Larry Jones                               2022:1.6K 2025:9.2K
  Malik Grego-Smith, Dustin Xaypanya        2020:7.2K
  Nick Mills                                2022:4.6K
  Rodolfo Mirabel, Jose Mateo, Richard San  2019:8.9K
  Ronald Anthony Burgos Aviles              2018:2
  Ryan Phillips                             2018:2.0K 2024:1.3K
  Terry L. Strawn                           2018:9.9K
  Watson Morgan                             2023:3
  William Dorsey Jones                      2021:3.0K
  William Michael, Nick Rodriguez           2024:7.2K

## where

STATE: CA 2.1K, TX 1.5K, FL 1.1K, AZ 676, GA 602, CO 484, NC 446, OH 438, TN 406, WA 399, MO 393, OK 391

## what

VICTIM_S_GENDER: Male 95%, Female 5%, Unknown 0%, Transgender Woman 0%, Transgender Man 0%, Transgender 0%, male 0%, Non-Binary 0%, Non-binary 0%

VICTIM_S_RACE: White 44%, Black 25%, Hispanic 18%, Unknown race 9%, Asian 2%, Native American 1%, Pacific Islander 0%, Black;Hispanic 0%, Native American;Hispanic 0%

CAUSE_OF_DEATH: Gunshot 93%, Taser 2%, Gunshot, Taser 2%, Vehicle 1%, Physical Restraint 1%, Beaten 0%, Taser, Gunshot 0%, Asphyxiated 0%, Taser, Physical Restraint 0%, Physical restraint 0%, Other 0%, Gunshot, Vehicle 0%

SYMPTOMS_OF_MENTAL_ILLNESS: No 68%, Yes 20%, Unclear 9%, Drug or alcohol use 3%, Drug or Alcohol Use 0%, No  0%

ARMED_UNARMED_STATUS: Allegedly Armed 74%, Unarmed/Did Not Have Actual We 13%, Unclear 7%, Vehicle 6%, Allegedly armed 0%

ALLEGED_THREAT_LEVEL_SOURCE_WAPO_AND_REVIEW_OF_CASES_NOT_INCLUDED_IN_WAPO_DATABASE: attack 60%, other 33%, undetermined 7%, other  0%, vehicle 0%

THREAT_LEVEL_DESCRIPTION: used weapon 38%, brandished weapon 18%, pointed weapon 18%, advanced towards officers 9%, sudden movement 8%, undetermined 8%, none 0%, Yes 0%, brandised weapon 0%, brandished "weapon" 0%, advanced towards others 0%, flee 0%

FLEEING_SOURCE_WAPO_AND_REVIEW_OF_CASES_NOT_INCLUDED_IN_WAPO_DATABASE: Not Fleeing 66%, Car 17%, Foot 13%, Other 2%, Car, Foot 1%, Not fleeing 1%, car 0%, foot 0%, car  0%, Foot, Car 0%, other 0%

BODY_CAMERA_SOURCE_WAPO: No 78%, yes 10%, Yes 10%, no 0%, Surveillance Video 0%, Dash Cam Video 0%, Bystander Video 0%, Body Cam, Dash Cam Video 0%, Body Cam, Bystander Video 0%, Police Helicopter Video 0%, Surveillance video 0%, surveillance video 0%

OFF_DUTY_KILLING: off-duty 97%, Off-Duty 1%, Off-duty 1%, off-duty   1%

GEOGRAPHY_VIA_TRULIA_METHODOLOGY_BASED_ON_ZIPCODE_POPULATION_DENSITY_HTTP_JEDKOLKO_COM_WP_CONTENT_UPLOADS_2015_05_FULL_ZCTA_URBAN_SUBURBAN_RURAL_CLASSIFICATION_XLSX: Suburban 50%, Urban 27%, Rural 24%

ENCOUNTER_TYPE: Part 1 Violent Crime 25%, Other Non-Violent Offense 18%, Mental Health/Welfare Check 10%, Domestic Disturbance 9%, Traffic Stop 8%, None/Unknown 8%, Person with a Weapon 7%, Part 1 Violent Crime/Domestic  4%, Other Crimes Against People 4%, Other Crimes Against People/Do 3%, Traffic Stop/Other Non-Violent 2%, Traffic stop 1%

KNOWN_PAST_SHOOTINGS_OF_OFFICER_S: 1 72%, 2 13%, 3 6%, 4 2%, 0 2%, 1 subsequent fatal shooting (R 1%, 1, 1, 1, Unknown 1%, 2 (nonfatal shooting in 2011 a 0%, 1 prior (and 1 subsequent shoo 0%, 1 (nonfatally shot Oston Shilo 0%, 1 (fatal shooting in 2007) 0%, 1 (subsequent shooting of Nich 0%

CALL_FOR_SERVICE: Yes 67%, No 28%, Unavailable 4%, No  1%, yes 0%

HUD_UPSAI_GEOGRAPHY: Suburban 43%, Urban 34%, Rural 23%

NCHS_URBAN_RURAL_CLASSIFICATION_SCHEME_CODES_HTTPS_WWW_CDC_GOV_NCHS_DATA_ACCESS_URBAN_RURAL_HTM: Large central metro (1) 34%, Medium metro (3) 23%, Large fringe metro (2) 18%, Small metro (4) 10%, Micropolitan (5) 9%, Non-core (6) 7%

CONGRESSIONAL_REPRESENTATIVE_PARTY_HTTPS_BALLOTPEDIA_ORG_UNITED_STATES_HOUSE_OF_REPRESENTATIVES: Republican 54%, Democrat 46%

PROSECUTOR_RACE: White 70%, Black 21%, Hispanic 7%, Asian 1%, White, White 0%, Pacific Islander 0%, White, Asian 0%

PROSECUTOR_GENDER: Male 68%, Female 31%, Female, Male 0%, Female, Female 0%

CHIEF_PROSECUTOR_POLITICAL_PARTY: Democrat 67%, Republican 31%, Nonpartisan 1%, Republican pre-2019, Independe 1%

CHIEF_PROSECUTOR_TERM: 2020- 18%, 2016 12%, 2017- 12%, 2021- 10%, 2019- 10%, 2015- 8%, 2016- 8%, 2013-2018 5%, 2009 5%, 2014 5%, 2018 5%, 2001-17 2%

OFFICER_PROSECUTED_BY_PROSECUTOR_IN_COURT: Dana Anton 8%, State Attorney General took ca 8%, Michael Dunty 8%, Tim Donnelly 8%, Chester Cedars 8%, Randi McGinn (W/F special pros 8%, Regina Mescall 8%, Joseph McMahon (W/M special pr 8%, Gerald Byers (B/M) 8%, Deputy DAs Martha Carrillo and 8%, Assistant AG Stanley Alexander 8%, AG's office handled the case 8%

SPECIAL_PROSECUTOR: no 80%, yes 9%, yes (AG's office) 5%, No 2%, no (but did appoint a former U 0%, yes (Corey O'Brien (W/M) from  0%, yes (Conflict of interest with 0%, yes (Jason Hicks of Stephens c 0%, no (outside state) 0%, yes (Newport News prosecutors  0%, Yes (state inspector general) 0%, yes (state AG's Office) 0%

INDEPENDENT_INVESTIGATION: yes 25%, no 20%, yes (Texas Rangers) 10%, yes (Georgia Bureau of Investi 8%, yes (MS Bureau of Investigatio 6%, yes (FDLE) 6%, yes (Mississippi Bureau of Inv 6%, yes (SC State Division of Law  4%, yes (DA's Office Independent I 4%, yes (Tennessee Bureau of Inves 4%, yes (Oklahoma State Bureau of  4%, yes (Florida Department of Law 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| VICTIM_S_NAME | who | 14.7K | 0 | Name withheld by police 588; Andrew L. Closson 75; Mark Chavez 75; Tyree Bell 75 |
| VICTIM_S_AGE | other | 96 | 7 | Unknown 758; 34 491; 32 483; 31 480 |
| VICTIM_S_GENDER | category | 9 | 0 | Male 14.6K; Female 772; Unknown 40; Transgender Woman 10 |
| VICTIM_S_RACE | category | 9 | 0 | White 6.7K; Black 3.9K; Hispanic 2.8K; Unknown race 1.4K |
| URL_OF_IMAGE_OF_VICTIM | id | 7.2K | 8.3K | http://www.superiortelegr 36; http://www.tricitytribune 36; http://content.omaha.com/ 36; http://bloximages.chicago 36 |
| DATE_OF_INCIDENT_MONTH_DAY_YEAR | date | 4.8K | 0 | 2013-06-16 00:00:00 83; 2013-03-10 00:00:00 82; 2013-06-08 00:00:00 82; 2013-01-01 00:00:00 81 |
| STREET_ADDRESS_OF_INCIDENT | id | 14.4K | 453 | SW 56th Street and 117th  77; U.S. Highway 53 76; 912 Loma Linda Ave. 76; 3727 N. 42nd St. 76 |
| CITY | who | 4.4K | 43 | Houston 213; Phoenix 192; Los Angeles 190; New York 140 |
| STATE | state | 51 | 0 | CA 2.1K; TX 1.5K; FL 1.1K; AZ 676 |
| ZIPCODE | other | 8.1K | 138 | 87401 78; 33175 78; 59101 78; 89005 78 |
| COUNTY | who | 1.4K | 2 | Los Angeles 568; Maricopa 403; Harris 258; Orange 208 |
| AGENCY_RESPONSIBLE_FOR_DEATH | who | 4.6K | 0 | Los Angeles Police Depart 219; Phoenix Police Department 185; Los Angeles County Sherif 171; New York Police Departmen 140 |
| ORI_AGENCY_IDENTIFIER_IF_AVAILABLE | who | 5.0K | 3 | CA0194200 219; AZ0072300 185; CA0190000 171; Not Found/No Agency ORI 145 |
| CAUSE_OF_DEATH | category | 40 | 0 | Gunshot 14.4K; Taser 384; Gunshot, Taser 302; Vehicle 126 |
| MEDIA_DESCRIPTION_OF_THE_CIRCUMSTANCES_SURROUNDING_THE_DEATH | id | 15.7K | 10 | Yolanda Thomas and Xavier 79; Deputies responded to a 9 78; An officer responded to a 78; Omaha Police Department r 78 |
| OFFICIAL_DISPOSITION_OF_DEATH_JUSTIFIED_OR_OTHER | who | 234 | 8 | Pending investigation/No  6.3K; Pending investigation/No  4.9K; Unreported 1.2K; Pending investigation 689 |
| CRIMINAL_CHARGES | who | 70 | 0 | No known charges 14.1K; No Known Charges 1.1K; Charged with a crime 111; Charged, Acquitted 35 |
| LINK_TO_NEWS_ARTICLE_OR_PHOTO_OF_OFFICIAL_DOCUMENT | id | 15.6K | 0 | http://miami.cbslocal.com 79; http://www.abqjournal.com 79; http://www.superiortelegr 78; http://www.daily-times.co 78 |
| SYMPTOMS_OF_MENTAL_ILLNESS | category | 6 | 55 | No 10.5K; Yes 3.1K; Unclear 1.3K; Drug or alcohol use 393 |
| ARMED_UNARMED_STATUS | category | 5 | 0 | Allegedly Armed 11.5K; Unarmed/Did Not Have Actu 2.0K; Unclear 1.0K; Vehicle 913 |
| ALLEGED_WEAPON_SOURCE_WAPO_AND_REVIEW_OF_CASES_NOT_INCLUDED_IN_WAPO_DATABASE | who | 227 | 0 | gun 8.5K; knife 2.1K; no object 1.5K; vehicle 845 |
| ALLEGED_THREAT_LEVEL_SOURCE_WAPO_AND_REVIEW_OF_CASES_NOT_INCLUDED_IN_WAPO_DATABASE | category | 5 | 2.4K | attack 7.8K; other 4.3K; undetermined 944; other  4 |
| THREAT_LEVEL_DESCRIPTION | category | 18 | 10.6K | used weapon 1.8K; brandished weapon 890; pointed weapon 887; advanced towards officers 428 |
| FLEEING_SOURCE_WAPO_AND_REVIEW_OF_CASES_NOT_INCLUDED_IN_WAPO_DATABASE | category | 11 | 3.1K | Not Fleeing 8.1K; Car 2.1K; Foot 1.6K; Other 229 |
| BODY_CAMERA_SOURCE_WAPO | category | 12 | 4.7K | No 8.5K; yes 1.1K; Yes 1.1K; no 52 |
| WAPO_ID_IF_INCLUDED_IN_WAPO_DATABASE | id | 10.4K | 5.1K | 3 52; 4 52; 5 52; 8 52 |
| OFF_DUTY_KILLING | category | 4 | 15.1K | off-duty 360; Off-Duty 5; Off-duty 4; off-duty   3 |
| GEOGRAPHY_VIA_TRULIA_METHODOLOGY_BASED_ON_ZIPCODE_POPULATION_DENSITY_HTTP_JEDKOLKO_COM_WP_CONTENT_UPLOADS_2015_05_FULL_ZCTA_URBAN_SUBURBAN_RURAL_CLASSIFICATION_XLSX | category | 3 | 916 | Suburban 7.2K; Urban 3.9K; Rural 3.4K |
| MPV_ID | id | 15.5K | 0 | 5 78; 1 78; 2 78; 6 78 |
| FATAL_ENCOUNTERS_ID | id | 9.8K | 5.6K | 12172 50; 12175 50; 12173 50; 12171 50 |
| ENCOUNTER_TYPE | category | 35 | 4.3K | Part 1 Violent Crime 2.7K; Other Non-Violent Offense 1.9K; Mental Health/Welfare Che 1.1K; Domestic Disturbance 952 |
| INITIAL_REPORTED_REASON_FOR_ENCOUNTER | who | 2.7K | 4.3K | domestic disturbance 439; shooting 323; person with a gun 255; robbery 251 |
| NAMES_OF_OFFICERS_INVOLVED | who | 3.8K | 11.7K | James A. Stuart 20; Sam Clayton, Jayson Forte 20; Bruce Barthelemy 20; John Morningstar 20 |
| RACE_OF_OFFICERS_INVOLVED | who | 91 | 14.9K | White 232; Hispanic 64; White, White 64; Black 39 |
| KNOWN_PAST_SHOOTINGS_OF_OFFICER_S | category | 39 | 15.2K | 1 148; 2 27; 3 13; 4 5 |
| CALL_FOR_SERVICE | category | 5 | 5.5K | Yes 6.7K; No 2.8K; Unavailable 423; No  55 |
| CENSUS_TRACT_CODE | other | 6.6K | 1.3K | 000800 77; 000600 74; 000200 74; 008704 72 |
| HUD_UPSAI_GEOGRAPHY | category | 3 | 5.4K | Suburban 4.4K; Urban 3.4K; Rural 2.3K |
| NCHS_URBAN_RURAL_CLASSIFICATION_SCHEME_CODES_HTTPS_WWW_CDC_GOV_NCHS_DATA_ACCESS_URBAN_RURAL_HTM | category | 6 | 864 | Large central metro (1) 4.9K; Medium metro (3) 3.3K; Large fringe metro (2) 2.6K; Small metro (4) 1.5K |
| MEDIAN_HOUSEHOLD_INCOME_ACS_CENSUS_TRACT | other | 9.7K | 2.4K | 96313 67; 250001 67; 78574 67; 60250 66 |
| LATITUDE | amount | 14.0K | 1.0K | 25.717203 74; 46.243621 73; 36.739514 73; 41.29311 73 |
| LONGITUDE | amount | 14.2K | 1.0K | -80.382658 74; -91.800796 73; -108.201029 73; -95.975491 73 |
| TOTAL_POPULATION_OF_CENSUS_TRACT_2019_ACS_5_YEAR_ESTIMATES | amount | 3.1K | 1.3K | 1235 72; 1637 72; 1319 72; 1178 72 |
| WHITE_NON_HISPANIC_PERCENT_OF_THE_POPULATION_ACS | amount | 12.5K | 1.4K | 0 409; 1 111; 0.11056811240073305 70; 0.7245322245322245 70 |
| BLACK_NON_HISPANIC_PERCENT_OF_THE_POPULATION_ACS | amount | 9.5K | 1.4K | 0 3.5K; 1 69; 0.42672064777327934 54; 0.11903114186851212 54 |
| NATIVE_AMERICAN_PERCENT_OF_THE_POPULATION_ACS | amount | 2.8K | 1.4K | 0 10.8K; 0.0008680555555555555 18; 0.002018842530282638 18; 0.405223251895535 17 |
| ASIAN_PERCENT_OF_THE_POPULATION_ACS | amount | 6.7K | 1.4K | 0 6.6K; 0.013439218081857055 39; 0.004158004158004158 39; 0.030927835051546393 38 |
| PACIFIC_ISLANDER_PERCENT_OF_THE_POPULATION_ACS | amount | 794 | 1.4K | 0 13.2K; 0.003205128205128205 6; 0.010958904109589041 6; 0.013461538461538462 6 |
| OTHER_TWO_OR_MORE_RACE_PERCENT_OF_THE_POPULATION_ACS | amount | 9.7K | 1.4K | 0 2.8K; 0.23284823284823286 58; 0.03868194842406877 57; 0.0340080971659919 57 |
| HISPANIC_PERCENT_OF_THE_POPULATION_ACS | amount | 979 | 1.3K | 0 1.8K; 0.017 80; 0.029 76; 0.038 75 |
| CONGRESSIONAL_DISTRICT | other | 433 | 720 | AZ3 128; NM1 114; OK2 102; AZ7 101 |
| CONGRESSIONAL_REPRESENTATIVE_FULL_NAME_HTTPS_BALLOTPEDIA_ORG_UNITED_STATES_HOUSE_OF_REPRESENTATIVES | who | 433 | 786 | Yassamin Ansari 128; Melanie Stansbury 114; Josh Brecheen 102; Adelita Grijalva 101 |
| UNNAMED_52 | empty | 0 | 15.5K |  |
| CONGRESSIONAL_REPRESENTATIVE_PARTY_HTTPS_BALLOTPEDIA_ORG_UNITED_STATES_HOUSE_OF_REPRESENTATIVES | category | 2 | 786 | Republican 7.9K; Democrat 6.8K |
| OFFICER_PROSECUTED_BY_CHIEF_PROSECUTOR | other | 198 | 15.2K | Sharen Wilson 5; Jim Hood 4; Fani Willis 4; Faith Johnson 4 |
| PROSECUTOR_RACE | category | 7 | 15.2K | White 184; Black 55; Hispanic 18; Asian 2 |
| PROSECUTOR_GENDER | category | 4 | 15.2K | Male 178; Female 82; Female, Male 1; Female, Female 1 |
| CHIEF_PROSECUTOR_POLITICAL_PARTY | category | 4 | 15.4K | Democrat 65; Republican 30; Nonpartisan 1; Republican pre-2019, Inde 1 |
| CHIEF_PROSECUTOR_TERM | category | 28 | 15.4K | 2020- 7; 2016 5; 2017- 5; 2021- 4 |
| OFFICER_PROSECUTED_BY_PROSECUTOR_IN_COURT | category | 27 | 15.4K | Dana Anton 1; State Attorney General to 1; Michael Dunty 1; Tim Donnelly 1 |
| SPECIAL_PROSECUTOR | category | 14 | 15.2K | no 193; yes 22; yes (AG's office) 11; No 6 |
| INDEPENDENT_INVESTIGATION | category | 45 | 15.4K | yes 13; no 10; yes (Texas Rangers) 5; yes (Georgia Bureau of In 4 |
| PROSECUTOR_SOURCE_LINK | other | 163 | 15.3K | https://www.chicagotribun 2; https://www.lmtonline.com 2; https://apnews.com/articl 2; https://abcnews.go.com/US 2 |
| KILLED_BY_POLICE_2013_26 | other | 1 | 0 | 1 15.5K |
| INGESTED_AT | audit | 1 | 0 | 1785099349116918 15.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 01ea24e3-eff7-40ec-b6d4-d 15.5K |
| SRC_SHA256 | who | 1 | 0 | fff1d18045e48ae5f8befa965 15.5K |
