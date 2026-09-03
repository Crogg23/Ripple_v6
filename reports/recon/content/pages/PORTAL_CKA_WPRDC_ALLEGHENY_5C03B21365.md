# PORTAL_CKA_WPRDC_ALLEGHENY_5C03B21365

rows 5.5K  columns 14  scan 3.9s

roles: audit 2, category 1, date 1, other 7, who 4

## when

INGESTED_AT
  2026      5.5K  ##############################

## who

FIRM_NAME by rows
         5  C. L. RUSSELL GROUP
         5  BELLMAX ELECTRIC LLC
         4  EDGEALL INC
         4  TALANTAGE LLC
         4  BRITTS INDUSTRIES, INC.
         4  STRATEGIC COMMUNITY ENGAGEMENT, LLC
         4  INTERDYNAMICS INC
         4  HUMMING BIRDS CONSULTING, LLC
         4  LTU SOLUTIONS, LLC
         4  EGROVE SYSTEMS CORPORATION
         4  AXIOS SERVICES LLC
         4  PRESENT SOFTWARE INC
         4  SUMMIT HEALTHCARE SOLUTIONS LLC
         4  Big Jet LLC
         4  COLLABRIUM SYSTEMS LLC
         4  CLIMATE CAPITAL STRATEGIES, INC.
         4  ANAVI STRATEGIES
         3  THE AKANKSHA LLC
         3  JULES ENTERPRISE GROUP INC
         3  ALOHA COMMUNICATIONS

OWNERS by rows
         6  Sangeetha Kancherla
         6  Jennifer Johnson
         6  Elizabeth Britt
         5  Nabaneeta Ray
         5  Gerald Mensah
         5  David Simpkins
         5  Donald Crenshaw
         4  Michelle Schrock
         4  Juan Williams
         4  Keith Searles
         4  Jose Fuertes
         4  Brigette Bethea
         4  Rebecca Peterson
         4  Joshua Pollard
         4  Sara Sargent
         4  Wayne Purville
         4  Todd Boucher
         4  CHRISTINE MEYER
         4  Renu Agarwal
         4  Brandy Weatherspoon

VENDOR_ID by rows
         6  20932274
         6  20271032
         5  20423999
         4  20233199
         4  20951959
         4  21332595
         4  20955198
         4  20137147
         4  20287825
         4  20232795
         4  20990711
         4  20137158
         4  20710358
         4  21018547
         4  20275656
         4  20043560
         3  20829327
         3  20043464
         3  20043211
         3  20389322

SRC_SHA256 by rows
      5.5K  d2254064d2b911e11df48f9b74ffa7adb0123139974551ab7e0c4f406faed833

## who x when

FIRM_NAME by INGESTED_AT  LOAD STAMP, not an event date
  ALOHA COMMUNICATIONS                      2026:3
  ANAVI STRATEGIES                          2026:4
  AXIOS SERVICES LLC                        2026:4
  BELLMAX ELECTRIC LLC                      2026:5
  BRITTS INDUSTRIES, INC.                   2026:4
  Big Jet LLC                               2026:4
  C. L. RUSSELL GROUP                       2026:5
  CLIMATE CAPITAL STRATEGIES, INC.          2026:4
  COLLABRIUM SYSTEMS LLC                    2026:4
  EDGEALL INC                               2026:4
  EGROVE SYSTEMS CORPORATION                2026:4
  HUMMING BIRDS CONSULTING, LLC             2026:4
  INTERDYNAMICS INC                         2026:4
  JULES ENTERPRISE GROUP INC                2026:3
  LTU SOLUTIONS, LLC                        2026:4
  PRESENT SOFTWARE INC                      2026:4
  STRATEGIC COMMUNITY ENGAGEMENT, LLC       2026:4
  SUMMIT HEALTHCARE SOLUTIONS LLC           2026:4
  TALANTAGE LLC                             2026:4
  THE AKANKSHA LLC                          2026:3

OWNERS by INGESTED_AT  LOAD STAMP, not an event date
  Brandy Weatherspoon                       2026:4
  Brigette Bethea                           2026:4
  CHRISTINE MEYER                           2026:4
  David Simpkins                            2026:5
  Donald Crenshaw                           2026:5
  Elizabeth Britt                           2026:6
  Gerald Mensah                             2026:5
  Jennifer Johnson                          2026:6
  Jose Fuertes                              2026:4
  Joshua Pollard                            2026:4
  Juan Williams                             2026:4
  Keith Searles                             2026:4
  Michelle Schrock                          2026:4
  Nabaneeta Ray                             2026:5
  Rebecca Peterson                          2026:4
  Renu Agarwal                              2026:4
  Sangeetha Kancherla                       2026:6
  Sara Sargent                              2026:4
  Todd Boucher                              2026:4
  Wayne Purville                            2026:4

## what

CERTIFICATION_TYPE: DBE 46%, WBE 28%, MBE 23%, ACDBE 4%, DBE (FAA Only) 0%, W/DBE 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| VENDOR_ID | who | 4.3K | 0 | 20071633 29; 21332980 29; 20137753 28; 20043382 28 |
| CERTIFICATION_TYPE | category | 6 | 0 | DBE 2.5K; WBE 1.5K; MBE 1.2K; ACDBE 216 |
| FIRM_NAME | who | 4.7K | 0 | Birkdesign Inc. 29; Neff Specialties, LLC 28; Streamline Engineering, I 28; PROSHARE SERVICES LLC 28 |
| OWNERS | who | 4.1K | 0 | JinJa Birkenbeuel 29; Shari Neff 28; Martha Frech 28; Danielle Baughman 28 |
| WORK_DESCRIPTION | other | 4.3K | 82 | Civil engineering 69; Business and corporate ma 46; Temporary personnel servi 31; Hospitality management wi 28 |
| NAICS_CODES | other | 4.0K | 0 | NA 79; 81101500 67; 541330 64; 541611 49 |
| PHYSICAL_ADDRESS | other | 4.7K | 0 | 2012 W. Augusta Chicago,  29; 1505 Main Street Hastings 28; 21 Sunrise Drive Leechbur 28; 113 Hemlock Street Pittsb 28 |
| PHONE_NUMBER | other | 4.3K | 0 | () - 70; (814) 247-8887 28; (724) 594-0326 28; (814) 242-2004 28 |
| FAX_NUMBER | other | 2.2K | 0 | () - 2.7K; (0) 000-0000 59; (312) 227-0208 15; (570) 829-6448 15 |
| EMAIL_ADDRESS | other | 4.5K | 2 | birkdesign@gmail.com 29; shari@neffspecialties.com 28; mfrech@streamlineengineer 28; DANIELLEBAUGHMAN@PROSHARE 28 |
| WEBSITE | other | 539 | 4.7K | http://WWW.WWLLCPROCUREME 7; http://www.cpromgt.com 6; http://www.tristatewaters 6; http://www.birkcreative.c 5 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:01:52.91136 5.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 7ef48bc4-677e-4a29-a3cc-e 5.5K |
| SRC_SHA256 | who | 1 | 0 | d2254064d2b911e11df48f9b7 5.5K |
