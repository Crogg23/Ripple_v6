# FED_COURTLISTENER_DISCLOSURE_REIMBURSEMENTS

rows 33.5K  columns 13  scan 3.7s

roles: audit 2, category 1, date 3, id 1, other 2, who 5

## when

DATE_CREATED
  2021     32.0K  ##############################
  2022      1.5K  #
  2023        27  

DATE_MODIFIED
  2021     32.0K  ##############################
  2022      1.5K  #
  2023        30  

_INGESTED_AT
  2026     33.5K  ##############################

## who

SOURCE by rows
       814  American Bankruptcy Institute
       786  American Bar Association
       377  National Conference of Bankruptcy Judges
       355  Federal Judges Association
       319  Federalist Society
       289  Federal Bar Association
       283  Federal Judicial Center
       283  State Bar of Texas
       264  American Conference Institute
       257  American Law Institute
       213  Harvard Law School
       180  ABA
       155  The Federalist Society
       154  The Florida Bar
       149  Federal Bar Council
       143  Georgetown University
       141  Nanonal Conference of Bankruptcy Judges
       132  Federal Circuit Bar Association
       129  Bankruptcy Judges
       125  New York Intellectual Property Law Association

PURPOSE by rows
       726  Speaker
       610  Teaching
       434  Board Meeting
       351  Seminar
       294  Conference
       288  Meeting
       283  Speech
       232  Moot Court
       230  Educational Seminar
       223  Annual Meeting
       193  Lecture
       179  Semmar
       153  Educational seminar
       124  Speaking Engagement
       119  Moot Court Competition
       118  Teaching Class
        91  Speaker at conference
        89  Participant
        84  Panelist
        75  Annual Conference

ITEMS_PAID_OR_PROVIDED by rows
       713  Transportation, meals, hotel
       635  Transportation
       551  Transportation, meals, lodging
       319  Travel
       281  Transportation, lodging, meals
       241  Transportation, food, lodging
       233  Transportation, lodging, food
       227  Transportation, Meals, Lodging
       218  Room, meals, transportation
       203  Transportation, Lodging, Meals
       198  Transportation, lodging, and meals
       189  Lodging
       189  Transportation, meals and lodging
       157  Transportation, Meals, Room
       151  Transportation, hotel, meals
       151  Travel related expenses
       147  Transportation, Food & Lodging
       146  travel and lodging
       132  Transportation, Lodging, Food
       123  Travel & Lodging

LOCATION by rows
      1.4K  New York, NY
      1.2K  Washington, DC
       744  Chicago, IL
       493  Washington, D.C
       380  Philadelphia, PA
       298  San Francisco, CA
       273  Cambridge, MA
       273  Atlanta, GA
       271  Washington, DX
       269  Austin, TX
       253  New Orleans, LA
       250  New York, New York
       250  Boston, MA
       217  Las Vegas, NV
       216  San Diego, CA
       200  New Haven, CT
       193  Los Angeles, CA
       173  Nashville, TN
       166  New York City
       163  Orlando, FL

## who x when

SOURCE by DATE_CREATED
  ABA                                       2021:173 2022:7
  American Bankruptcy Institute             2021:765 2022:49
  American Bar Association                  2021:727 2022:59
  American Conference Institute             2021:263 2022:1
  American Law Institute                    2021:232 2022:25
  Bankruptcy Judges                         2021:129
  Federal Bar Association                   2021:269 2022:20
  Federal Bar Council                       2021:144 2022:5
  Federal Circuit Bar Association           2021:131 2022:1
  Federal Judges Association                2021:349 2022:6
  Federal Judicial Center                   2021:262 2022:21
  Federalist Society                        2021:238 2022:81
  Georgetown University                     2021:142 2022:1
  Harvard Law School                        2021:198 2022:15
  Nanonal Conference of Bankruptcy Judges   2021:141
  National Conference of Bankruptcy Judges  2021:362 2022:15
  New York Intellectual Property Law Assoc  2021:122 2022:3
  State Bar of Texas                        2021:272 2022:11
  The Federalist Society                    2021:136 2022:19
  The Florida Bar                           2021:141 2022:13

PURPOSE by DATE_CREATED
  Annual Conference                         2021:68 2022:7
  Annual Meeting                            2021:217 2022:6
  Board Meeting                             2021:424 2022:10
  Conference                                2021:275 2022:19
  Educational Seminar                       2021:204 2022:26
  Educational seminar                       2021:150 2022:3
  Lecture                                   2021:180 2022:13
  Meeting                                   2021:275 2022:13
  Moot Court                                2021:220 2022:12
  Moot Court Competition                    2021:109 2022:10
  Panelist                                  2021:73 2022:11
  Participant                               2021:89
  Seminar                                   2021:332 2022:19
  Semmar                                    2021:179
  Speaker                                   2021:663 2022:63
  Speaker at conference                     2021:91
  Speaking Engagement                       2021:124
  Speech                                    2021:272 2022:9 2023:2
  Teaching                                  2021:584 2022:26
  Teaching Class                            2021:118

## what

REDACTED: f 100%, t 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 34.4K | 0 | 97011 168; 97010 168; 97009 168; 97007 168 |
| DATE_CREATED | date | 33.6K | 0 | 2022-05-19 16:02:06.96188 168; 2022-05-19 16:02:06.96180 168; 2022-05-19 16:02:06.96173 168; 2022-05-19 16:02:06.96159 168 |
| DATE_MODIFIED | date | 34.8K | 0 | 2022-05-19 16:02:06.96189 168; 2022-05-19 16:02:06.96182 168; 2022-05-19 16:02:06.96175 168; 2022-05-19 16:02:06.96160 168 |
| SOURCE | who | 12.8K | 1.3K | American Bankruptcy Insti 814; American Bar Association 786; National Conference of Ba 377; Federal Judges Associatio 355 |
| DATE_RAW | other | 22.5K | 8.0K | January 10-12, 2020 140; 01/27/2020 133; 02/01/2020-02/05/2020 132; 01/06/2020-01/09/2020 131 |
| LOCATION | who | 5.1K | 8.4K | New York, NY 1.4K; Washington, DC 1.2K; Chicago, IL 744; Washington, D.C 493 |
| PURPOSE | who | 11.9K | 5.9K | Speaker 726; Teaching 610; Board Meeting 434; Seminar 351 |
| ITEMS_PAID_OR_PROVIDED | who | 11.3K | 2.6K | Transportation, meals, ho 713; Transportation 635; Transportation, meals, lo 551; Travel 319 |
| REDACTED | category | 2 | 0 | f 33.4K; t 73 |
| FINANCIAL_DISCLOSURE_ID | other | 10.4K | 0 | 34160 194; 20139 189; 18265 183; 19035 182 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-12 00:04:57.954 33.5K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 4e82359c-9c11-4552-877a-3 33.5K |
| _SRC_SHA256 | who | 1 | 0 | 2f97c8211d48529d211f24366 33.5K |
