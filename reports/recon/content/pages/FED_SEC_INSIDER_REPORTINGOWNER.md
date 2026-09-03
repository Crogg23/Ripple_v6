# FED_SEC_INSIDER_REPORTINGOWNER

rows 1.93M  columns 16  scan 4.0s

roles: audit 2, category 1, date 1, other 3, state 1, who 9

## when

_INGESTED_AT
  2026     1.93M  ##############################

## who

RPTOWNERNAME by rows
      2.8K  Weinstein Boaz
      2.8K  Saba Capital Management, L.P.
      1.9K  STAHL MURRAY
      1.3K  HORIZON KINETICS ASSET MANAGEMENT LLC
      1.3K  Benioff Marc
       732  Zuckerberg Mark
       636  Farquhar Scott
       635  Cannon-Brookes Michael
       605  GABELLI MARIO J
       582  Mansueto Joseph D
       530  FROST PHILLIP MD ET AL
       416  SHAW THOMAS J
       412  GARCIA ERNEST C. II
       405  Harris Parker
       401  GOLDSTEIN PHILLIP
       396  SCHWARZMAN STEPHEN A
       394  VERDE INVESTMENTS, INC.
       379  Blackstone Group Management L.L.C.
       373  BAKER BROS. ADVISORS LP
       371  Baker Bros. Advisors (GP) LLC

RPTOWNERCIK by rows
      2.8K  0001608233
      2.8K  0001510281
      1.9K  0001207097
      1.4K  0001056823
      1.3K  0001294693
       733  0001548760
       636  0001666121
       635  0001666120
       605  0001185533
       582  0001324069
       530  0000898860
       418  0001017608
       416  0001174567
       405  0001294774
       402  0001067621
       396  0001070844
       394  0001704727
       385  0001393818
       379  0001404071
       373  0001263508

RPTOWNER_TITLE by rows
     54.1K  Chief Financial Officer
     45.0K  Chief Executive Officer
     35.0K  President and CEO
     27.5K  See Remarks
     22.0K  Executive Vice President
     20.9K  President & CEO
     19.5K  Chief Operating Officer
     14.8K  President
     14.3K  Chief Accounting Officer
     13.3K  CEO
     12.9K  Senior Vice President
      9.4K  Chief Technology Officer
      8.8K  Vice President
      8.6K  Executive Chairman
      7.9K  Chairman and CEO
      7.2K  CFO
      7.0K  Chief Legal Officer
      6.8K  Chief Medical Officer
      6.8K  General Counsel
      5.3K  Chairman & CEO

RPTOWNER_TXT by rows
      7.0K  See Remarks
      6.3K  Member of a Group
      3.3K  Portfolio Manager
      2.9K  Trustee
      2.3K  See Explanation of Responses
      2.1K  Member of 10% owner group
      1.6K  Chairman of the Board
      1.2K  SEE REMARKS
      1.2K  Former 10% Owner
      1.1K  Group Member
       867  Former Director
       844  Passive Investor
       782  See Footnote 1
       709  Chairman
       662  Director-by-Deputization
       662  Member of a group
       645  See remarks
       612  Director by Deputization
       492  Possible Member of 10% Group
       439  Investment Adviser

## who x when

RPTOWNERNAME by _INGESTED_AT  LOAD STAMP, not an event date
  BAKER BROS. ADVISORS LP                   2026:373
  Baker Bros. Advisors (GP) LLC             2026:371
  Benioff Marc                              2026:1.3K
  Blackstone Group Management L.L.C.        2026:379
  Cannon-Brookes Michael                    2026:635
  FROST PHILLIP MD ET AL                    2026:530
  Farquhar Scott                            2026:636
  GABELLI MARIO J                           2026:605
  GARCIA ERNEST C. II                       2026:412
  GOLDSTEIN PHILLIP                         2026:401
  HORIZON KINETICS ASSET MANAGEMENT LLC     2026:1.3K
  Harris Parker                             2026:405
  Mansueto Joseph D                         2026:582
  SCHWARZMAN STEPHEN A                      2026:396
  SHAW THOMAS J                             2026:416
  STAHL MURRAY                              2026:1.9K
  Saba Capital Management, L.P.             2026:2.8K
  VERDE INVESTMENTS, INC.                   2026:394
  Weinstein Boaz                            2026:2.8K
  Zuckerberg Mark                           2026:732

RPTOWNERCIK by _INGESTED_AT  LOAD STAMP, not an event date
  0000898860                                2026:530
  0001017608                                2026:418
  0001056823                                2026:1.4K
  0001067621                                2026:402
  0001070844                                2026:396
  0001174567                                2026:416
  0001185533                                2026:605
  0001207097                                2026:1.9K
  0001263508                                2026:373
  0001294693                                2026:1.3K
  0001294774                                2026:405
  0001324069                                2026:582
  0001393818                                2026:385
  0001404071                                2026:379
  0001510281                                2026:2.8K
  0001548760                                2026:733
  0001608233                                2026:2.8K
  0001666120                                2026:635
  0001666121                                2026:636
  0001704727                                2026:394

## where

RPTOWNER_STATE: CA 348.5K, NY 241.8K, TX 155.6K, MA 120.7K, IL 81.4K, PA 77.2K, FL 75.1K, OH 62.6K, NJ 61.0K, VA 48.1K, CT 42.5K, CO 41.4K

## what

RPTOWNER_RELATIONSHIP: Officer 39%, Director 34%, Director,Officer 10%, TenPercentOwner 9%, Director,TenPercentOwner 3%, Other 2%, Director,Officer,TenPercentOwn 2%, TenPercentOwnerOther 0%, DirectorOther 0%, Director,TenPercentOwnerOther 0%, OfficerOther 0%, Director,Other 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ACCESSION_NUMBER | other | 1.71M | 0 | 0000899243-23-009836 1.8K; 0001104659-23-038294 1.8K; 0001104659-23-038296 1.8K; 0001104659-23-038302 1.8K |
| RPTOWNERCIK | who | 139.9K | 0 | 0001515154 3.5K; 0001336007 3.5K; 0001326389 3.5K; 0001875065 2.6K |
| RPTOWNERNAME | who | 141.7K | 1.2K | Moret Blake D. 3.5K; Green Eric Mark 3.5K; Polar Asset Management Pa 3.5K; Giroux Roland A 2.6K |
| RPTOWNER_RELATIONSHIP | category | 23 | 331 | Officer 756.2K; Director 653.1K; Director,Officer 186.4K; TenPercentOwner 180.6K |
| RPTOWNER_TITLE | who | 34.9K | 944.6K | Chief Financial Officer 54.1K; Chief Executive Officer 45.0K; President and CEO 35.0K; See Remarks 27.5K |
| RPTOWNER_TXT | who | 3.3K | 1.87M | See Remarks 7.0K; Member of a Group 6.3K; Portfolio Manager 3.3K; Trustee 2.9K |
| RPTOWNER_STREET1 | who | 51.7K | 8.5K | C/O ATLASSIAN CORPORATION 5.1K; C/O BLACKSTONE INC. 4.5K; 530 HERMAN O. WEST DRIVE 4.3K; PRINCETON SOUTH CORPORATE 3.8K |
| RPTOWNER_STREET2 | who | 22.5K | 842.5K | SUITE 300 16.0K; SUITE 200 10.6K; SUITE 100 10.6K; SUITE 600 8.7K |
| RPTOWNER_CITY | who | 6.6K | 2.9K | NEW YORK 188.4K; SAN FRANCISCO 52.8K; HOUSTON 50.8K; CHICAGO 42.3K |
| RPTOWNER_STATE | state | 172 | 6.4K | CA 348.5K; NY 241.8K; TX 155.6K; MA 120.7K |
| RPTOWNER_ZIPCODE | who | 11.0K | 9.9K | 10022 26.3K; 10019 17.9K; 94025 16.4K; 10017 16.0K |
| RPTOWNER_STATE_DESC | who | 124 | 1.86M | UNITED KINGDOM 11.6K; ONTARIO, CANADA 7.4K; BERMUDA 6.5K; BRITISH COLUMBIA, CANADA 5.8K |
| FILE_NUMBER | other | 10.9K | 8 | 001-37651 6.3K; 001-10585 5.0K; 001-39804 4.9K; 001-14920 4.7K |
| _INGESTED_AT | audit date | 1 | 0 | 2026-07-24 02:29:10.000 1.93M |
| _SOURCE_RUN_ID | audit | 1 | 0 | 72ab8f6f-9c92-4c27-8d1b-6 1.93M |
| _SRC_SHA256 | other | 1 | 0 | manifest_members:35:REPOR 1.93M |
