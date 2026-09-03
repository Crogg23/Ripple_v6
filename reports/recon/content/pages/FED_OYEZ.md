# FED_OYEZ

rows 25  columns 22  scan 2.7s

roles: audit 3, category 12, date 3, empty 4, who 1

## when

ARGUMENT_DATE
  1971         8  ##############################
  1972         8  ##############################

DECISION_DATE
  1966         1  ##
  1967         1  ##
  1968         2  ####
  1969         2  ####
  1971         2  ####
  1972        16  ##############################
  1973         1  ##

SCRAPED_AT
  2026        25  ##############################

## who

_SRC_SHA256 by rows
        25  d0d11725f978595e3381f34c71990873975011c40aa4e2efb24d0f056bbb5c04

## who x when

_SRC_SHA256 by DECISION_DATE
  d0d11725f978595e3381f34c71990873975011c4  1966:1 1967:1 1968:2 1969:2 1971:2 1972:16 1973:1

## what

CASE_ID: 50620 8%, 50619 8%, 50618 8%, 50617 8%, 50616 8%, 50615 8%, 50613 8%, 50612 8%, 50611 8%, 50609 8%, 50608 8%, 50606 8%

DOCKET: 71-11 8%, 70-5082 8%, 70-250 8%, 70-5055 8%, 70-79 8%, 70-33 8%, 70-5014 8%, 68-5009 8%, 45-orig 8%, 69-4 8%, 70-5039 8%, 70-18 8%

CASE_NAME: James v. Strange 8%, Carter v. Stanton 8%, Carleson v. Remillard 8%, Smith v. Florida 8%, Reliance Electric Company v. E 8%, Engelman v. Amos 8%, Stanley v. Illinois 8%, Schneble v. Florida 8%, Washington v. General Motors C 8%, Zicarelli v. New Jersey State  8%, Fuentes v. Shevin 8%, Roe v. Wade 8%

TERM: 1971 76%, 1967 8%, 1966 8%, 1968 4%, 1969 4%

AUDIO_URL: https://api.oyez.org/case_medi 9%, https://api.oyez.org/case_medi 9%, https://api.oyez.org/case_medi 9%, https://api.oyez.org/case_medi 9%, https://api.oyez.org/case_medi 9%, https://api.oyez.org/case_medi 9%, https://api.oyez.org/case_medi 9%, https://api.oyez.org/case_medi 9%, https://api.oyez.org/case_medi 9%, https://api.oyez.org/case_medi 9%, https://api.oyez.org/case_medi 9%

TRANSCRIPT_URL: https://api.oyez.org/cases/197 8%, https://api.oyez.org/cases/197 8%, https://api.oyez.org/cases/197 8%, https://api.oyez.org/cases/197 8%, https://api.oyez.org/cases/197 8%, https://api.oyez.org/cases/197 8%, https://api.oyez.org/cases/197 8%, https://api.oyez.org/cases/197 8%, https://api.oyez.org/cases/197 8%, https://api.oyez.org/cases/197 8%, https://api.oyez.org/cases/197 8%, https://api.oyez.org/cases/197 8%

SUMMARY: None 92%, <p>Joan Stanley had three chil 4%, <p>In 1970, Jane Roe (a fictio 4%

ADVOCATE_NAMES: Edward G. Collister, Jr., John 9%, Jon D. Noland, Mark Peden, Rob 9%, Jay S. Linderman, Carmen L. Ma 9%, Phillip A. Hubbart, Nelson E.  9%, Thomas P. Mulligan, Walter P.  9%, Patrick T. Murphy, Morton E. F 9%, Clyde B. Wells, George R. Geor 9%, Fredric C. Tausend, Lloyd N. C 9%, Michael A. Querques, Andrew F. 9%, C. Michael Abbott, Herbert T.  9%, Sarah R. Weddington, Jay Floyd 9%

PETITIONER: James 8%, Carter 8%, Carleson 8%, Smith 8%, Reliance Electric Company 8%, Engelman 8%, Peter Stanley, Sr.  8%, Schneble 8%, Washington 8%, Zicarelli 8%, Fuentes 8%, Jane Roe 8%

RESPONDENT: United States 25%, Florida 12%, Strange 6%, Stanton 6%, Remillard 6%, Emerson Electric Company 6%, Amos 6%, Illinois 6%, General Motors Corporation 6%, New Jersey State Commission of 6%, Shevin 6%, Henry Wade 6%

LOWER_COURT: Florida Supreme Court 20%, United States Court of Appeals 20%, Supreme Court of Illinois 10%, New Jersey Supreme Court 10%, State trial court 10%, United States Court of Appeals 10%, New York Court of Appeals 10%, United States Court of Appeals 10%

JUSTICE_VOTES: [{"member": {"ID": 15107, "nam 80%, [{"member": {"ID": 15099, "nam 16%, [{"member": {"ID": 15073, "nam 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CASE_ID | category | 25 | 0 | 50620 1; 50619 1; 50618 1; 50617 1 |
| DOCKET | category | 25 | 0 | 71-11 1; 70-5082 1; 70-250 1; 70-5055 1 |
| CASE_NAME | category | 25 | 0 | James v. Strange 1; Carter v. Stanton 1; Carleson v. Remillard 1; Smith v. Florida 1 |
| TERM | category | 5 | 0 | 1971 19; 1967 2; 1966 2; 1968 1 |
| ARGUMENT_DATE | date | 16 | 9 | 1971-12-07 2; 1972-03-22 1; 1971-11-08 1; 1972-04-10 1 |
| DECISION_DATE | date | 21 | 0 | 1972-06-12 3; 1972-04-03 2; 1972-02-24 2; 1972-06-07 1 |
| DECISION | empty | 1 | 25 |  |
| MAJORITY_AUTHOR | empty | 1 | 25 |  |
| DISPOSITION | empty | 1 | 25 |  |
| CITATION | empty | 1 | 25 |  |
| AUDIO_URL | category | 16 | 9 | https://api.oyez.org/case 1; https://api.oyez.org/case 1; https://api.oyez.org/case 1; https://api.oyez.org/case 1 |
| TRANSCRIPT_URL | category | 25 | 0 | https://api.oyez.org/case 1; https://api.oyez.org/case 1; https://api.oyez.org/case 1; https://api.oyez.org/case 1 |
| SUMMARY | category | 3 | 0 | None 23; <p>Joan Stanley had three 1; <p>In 1970, Jane Roe (a f 1 |
| ADVOCATE_NAMES | category | 22 | 4 | Edward G. Collister, Jr., 1; Jon D. Noland, Mark Peden 1; Jay S. Linderman, Carmen  1; Phillip A. Hubbart, Nelso 1 |
| PETITIONER | category | 25 | 0 | James 1; Carter 1; Carleson 1; Smith 1 |
| RESPONDENT | category | 21 | 0 | United States 4; Florida 2; Strange 1; Stanton 1 |
| LOWER_COURT | category | 9 | 15 | Florida Supreme Court 2; United States Court of Ap 2; Supreme Court of Illinois 1; New Jersey Supreme Court 1 |
| JUSTICE_VOTES | category | 25 | 0 | [{"member": {"ID": 15107, 20; [{"member": {"ID": 15099, 4; [{"member": {"ID": 15073, 1 |
| SCRAPED_AT | audit date | 1 | 0 | 2026-06-17T19:00:02.03592 25 |
| _INGESTED_AT | audit | 1 | 0 | 1781722799070491 25 |
| _SOURCE_RUN_ID | audit | 1 | 0 | f8f9d847-2082-4a71-83fa-9 25 |
| _SRC_SHA256 | who | 1 | 0 | d0d11725f978595e3381f34c7 25 |
