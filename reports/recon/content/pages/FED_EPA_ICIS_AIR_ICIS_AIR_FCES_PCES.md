# FED_EPA_ICIS_AIR_ICIS_AIR_FCES_PCES

rows 1.78M  columns 13  scan 3.5s

roles: audit 2, category 4, id 1, other 4, who 2

## who

ACTUAL_END_DATE by rows
      2.9K  09-30-2003
      2.5K  09-30-2005
      2.1K  09-30-2004
      2.0K  09-30-2002
      1.7K  09-30-2008
      1.7K  09-30-2009
      1.5K  09-30-2013
      1.5K  09-30-2010
      1.5K  09-30-2011
      1.3K  09-30-2014
      1.3K  09-30-2006
      1.3K  09-30-2007
      1.3K  09-30-2015
      1.2K  09-30-2021
      1.2K  09-30-2024
      1.2K  09-30-2020
      1.2K  09-30-2019
      1.2K  09-30-2022
      1.1K  09-30-2016
      1.1K  09-28-2018

PROGRAM_CODES by rows
    302.0K  CAASIP
    114.8K  CAATVP
     81.4K  CAASIP, CAATVP
     72.0K  CAANSPS, CAASIP
     54.9K  CAAMACT, CAANSPS, CAASIP
     46.2K  CAAMACT, CAANSPS, CAASIP, CAATVP
     44.0K  CAAMACT, CAASIP
     34.0K  CAAMACT, CAASIP, CAATVP
     26.2K  CAANSPS, CAASIP, CAATVP
     18.2K  CAANSPS
     15.4K  CAAMACT
     14.7K  CAAMACT, CAANSPS, CAAPSD, CAASIP, CAATVP
     14.0K  CAAFESOP, CAASIP
     13.4K  CAAFESOP
      9.8K  CAAMACT, CAANESH, CAANSPS, CAASIP, CAATVP
      6.7K  CAANSPSM, CAASIP
      6.6K  CAAGACTM, CAASIP
      6.6K  CAAMACT, CAANESH, CAANSPS, CAAPSD, CAASIP, CAATVP
      6.5K  CAANSPS, CAAPSD, CAASIP, CAATVP
      4.8K  CAAMACT, CAAPSD, CAASIP, CAATVP

## what

STATE_EPA_FLAG: S 87%, L 10%, E 3%

COMP_MONITOR_TYPE_CODE: PFF 35%, FOO 35%, PCE 20%, POR 6%, POM 2%, FFO 1%, POV 0%, POI 0%, POC 0%, PFR 0%, POF 0%

COMP_MONITOR_TYPE_DESC: PCE Off-Site 35%, FCE On-Site 35%, PCE On-Site 20%, PCE On-Site Record/Report Revi 6%, PCE On-Site Monitoring/Samplin 2%, FCE Off-Site 1%, PCE On-Site Visible Emission O 0%, PCE On-Site Interview 0%, PCE On-Site CEMS/CMS Audit 0%, PCE Off-Site - Review of 114 R 0%, PCE On-Site Fenceline/Ambient  0%

ACTIVITY_PURPOSE_DESC: Core Program 98%, Selected Monitoring Action 1%, Agency Priority 1%, Oversight 0%, Citizen Complaint/Tip 0%, Case Development 0%, Random Inspection 0%, Other 0%, Result of Spill 0%, Applicability Determination 0%, For Cause 0%, Referral Inspection 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PGM_SYS_ID | other | 153.1K | 0 | GA0000001309900001 4.8K; PA000549766 4.1K; PA000483776 4.1K; NY0000003392800001 4.1K |
| ACTIVITY_ID | id | 1.78M | 0 | 3402462771 2.4K; 3402459974 2.4K; 3402459975 2.4K; 3402459976 2.4K |
| STATE_EPA_FLAG | category | 3 | 0 | S 1.56M; L 169.5K; E 53.7K |
| ACTIVITY_TYPE_CODE | other | 1 | 0 | INS 1.78M |
| ACTIVITY_TYPE_DESC | other | 1 | 0 | Inspection/Evaluation 1.78M |
| COMP_MONITOR_TYPE_CODE | category | 11 | 0 | PFF 630.6K; FOO 629.3K; PCE 354.5K; POR 99.6K |
| COMP_MONITOR_TYPE_DESC | category | 11 | 0 | PCE Off-Site 630.6K; FCE On-Site 629.3K; PCE On-Site 354.5K; PCE On-Site Record/Report 99.6K |
| ACTUAL_END_DATE | who | 17.0K | 0 | 09-10-2002 4.8K; 08-23-2012 4.8K; 08-11-1998 4.8K; 06-14-2012 4.8K |
| PROGRAM_CODES | who | 1.4K | 741.4K | CAASIP 302.0K; CAATVP 114.8K; CAASIP, CAATVP 81.4K; CAANSPS, CAASIP 72.0K |
| ACTIVITY_PURPOSE_DESC | category | 16 | 693.8K | Core Program 1.06M; Selected Monitoring Actio 10.4K; Agency Priority 5.4K; Oversight 2.1K |
| _INGESTED_AT | audit | 1 | 0 | 1785966165496104 1.78M |
| _SOURCE_RUN_ID | audit | 1 | 0 | 4fb22f5f-ae93-499c-a6bc-c 1.78M |
| _SRC_SHA256 | other | 1 | 0 | b52db4db57a1b5a58be68a8d2 1.78M |
