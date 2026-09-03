# FED_COURTLISTENER_DISCLOSURE_POSITIONS

rows 37.0K  columns 10  scan 3.5s

roles: audit 2, category 1, date 3, id 1, other 1, who 3

## when

DATE_CREATED
  2021     32.0K  ##############################
  2022      5.0K  #####
  2023        34  

DATE_MODIFIED
  2021     32.0K  ##############################
  2022      5.0K  #####
  2023        34  

_INGESTED_AT
  2026     37.0K  ##############################

## who

ORGANIZATION_NAME by rows
       362  Trust #1
       340  Federal Judges Association
       166  National Conference of Bankruptcy Judges
       114  Trust #2
       113  American Bankruptcy Institute
        99  Trust No.
        80  Federal Bar Association
        77  American Bar Association
        75  Columbia Law School
        75  Trust No. 2
        73  Trust #3
        64  Amencan Law Institute
        63  Federal Magistrate Judges Association
        61  Trust
        61  American Law Institute
        53  Brooklyn Law School
        49  Georgetown University Law Center
        49  Fordham Law Alumni Association
        46  Albany Law School
        46  American Bar Foundation

POSITION by rows
      3.3K  Trustee
      3.1K  Director
      2.5K  Member
      2.1K  Board Member
       840  Co-Trustee
       794  Board of Directors
       562  Member, Board of Directors
       491  President
       484  Partner
       386  Adjunct Professor
       356  Advisory Board Member
       350  Custodian
       258  Adpunct Professor
       246  Board of Trustees
       240  Advisory Board
       239  Member, Board of Trustees
       236  TRUSTEE
       215  Adpmunct Professor
       196  Fellow
       183  MEMBER

_SRC_SHA256 by rows
     37.0K  7c96b16f4687b10d6ca1d34c6ef150c2110b524e7b24c50e07060d4dd98d9646

## who x when

ORGANIZATION_NAME by DATE_CREATED
  Albany Law School                         2021:40 2022:6
  Amencan Law Institute                     2021:64
  American Bankruptcy Institute             2021:103 2022:10
  American Bar Association                  2021:71 2022:6
  American Bar Foundation                   2021:37 2022:9
  American Law Institute                    2021:40 2022:19 2023:2
  Brooklyn Law School                       2021:47 2022:6
  Columbia Law School                       2021:63 2022:12
  Federal Bar Association                   2021:67 2022:13
  Federal Judges Association                2021:308 2022:32
  Federal Magistrate Judges Association     2021:33 2022:30
  Fordham Law Alumni Association            2021:43 2022:6
  Georgetown University Law Center          2021:43 2022:6
  National Conference of Bankruptcy Judges  2021:136 2022:30
  Trust                                     2021:60 2022:1
  Trust #1                                  2021:260 2022:102
  Trust #2                                  2021:86 2022:28
  Trust #3                                  2021:51 2022:22
  Trust No.                                 2021:99
  Trust No. 2                               2021:65 2022:10

POSITION by DATE_CREATED
  Adjunct Professor                         2021:238 2022:148
  Adpmunct Professor                        2021:215
  Adpunct Professor                         2021:258
  Advisory Board                            2021:208 2022:32
  Advisory Board Member                     2021:315 2022:41
  Board Member                              2021:1.8K 2022:339 2023:2
  Board of Directors                        2021:700 2022:92 2023:2
  Board of Trustees                         2021:225 2022:20 2023:1
  Co-Trustee                                2021:748 2022:92
  Custodian                                 2021:333 2022:17
  Director                                  2021:2.7K 2022:328
  Fellow                                    2021:165 2022:31
  MEMBER                                    2021:131 2022:52
  Member                                    2021:2.2K 2022:360
  Member, Board of Directors                2021:496 2022:66
  Member, Board of Trustees                 2021:205 2022:32 2023:2
  Partner                                   2021:407 2022:77
  President                                 2021:449 2022:42
  TRUSTEE                                   2021:206 2022:30
  Trustee                                   2021:2.6K 2022:735

## what

REDACTED: f 96%, t 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 38.0K | 0 | 99086 186; 99085 186; 99084 186; 99083 186 |
| DATE_CREATED | date | 36.5K | 0 | 2022-05-19 19:02:30.33331 186; 2022-05-19 19:02:30.33321 186; 2022-05-19 19:02:22.12769 186; 2022-05-19 19:02:22.12759 186 |
| DATE_MODIFIED | date | 37.0K | 0 | 2022-05-19 19:02:30.33333 186; 2022-05-19 19:02:30.33324 186; 2022-05-19 19:02:22.12771 186; 2022-05-19 19:02:22.12763 186 |
| POSITION | who | 5.4K | 227 | Trustee 3.3K; Director 3.1K; Member 2.5K; Board Member 2.1K |
| ORGANIZATION_NAME | who | 13.4K | 768 | Trust #1 362; Federal Judges Associatio 340; National Conference of Ba 215; Federal Magistrate Judges 190 |
| REDACTED | category | 2 | 0 | f 35.6K; t 1.4K |
| FINANCIAL_DISCLOSURE_ID | other | 16.3K | 0 | 34175 228; 33564 227; 33521 209; 33754 203 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-12 00:04:35.475 37.0K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 1749ccae-b151-4aed-b5c7-3 37.0K |
| _SRC_SHA256 | who | 1 | 0 | 7c96b16f4687b10d6ca1d34c6 37.0K |
