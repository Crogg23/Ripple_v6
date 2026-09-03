# FED_ICE_DETENTION_FACILITY_LIST

rows 165  columns 8  scan 2.2s

roles: audit 2, category 2, other 1, state 1, who 2

## who

FACILITY_NAME by rows
         2  BUTLER COUNTY JAIL
         2  EDEN DETENTION CENTER
         1  KROME NORTH SERVICE PROCESSING CENTER
         1  MAIN - FOLKSTON IPC (D RAY JAMES)
         1  MORGAN COUNTY ADULT DETENTION CENTER
         1  FRANKLIN COUNTY HOUSE OF CORRECTION
         1  PINE PRAIRIE ICE PROCESSING CENTER
         1  ORANGE COUNTY JAIL
         1  PHELPS COUNTY JAIL
         1  WASHINGTON COUNTY JAIL (PURGATORY CORRECTIONAL FAC
         1  TORRANCE COUNTY DETENTION FACILITY
         1  WASHOE COUNTY JAIL
         1  YORK COUNTY PRISON
         1  LINCOLN COUNTY DETENTION CENTER
         1  LINN COUNTY JAIL
         1  CCA, FLORENCE CORRECTIONAL CENTER
         1  STRAFFORD COUNTY CORRECTIONS
         1  JOE CORLEY ICE PROCESSING CENTER
         1  RIO GRANDE DETENTION CENTER
         1  ALBANY COUNTY JAIL

_SRC_SHA256 by rows
       165  6438a5ca5c1fa0795905e48d252a7de880aa12b836907b00f9c9885ba48e2652

## where

STATE: TX 26, LA 10, CA 8, FL 7, AZ 6, PA 6, MO 6, IA 5, MN 5, NY 5, OH 5, GA 5

## what

AOR: Chicago AOR 15%, Saint Paul AOR 13%, San Antonio AOR 11%, New Orleans AOR 11%, Salt Lake City AOR 9%, Detroit AOR 7%, Dallas AOR 6%, Philadelphia AOR 6%, Miami AOR 6%, Boston AOR 6%, Atlanta AOR 6%, San Francisco AOR 5%

FACILITY_TYPE_DETAILED: Inter-Governmental Service Agr 44%, U.S. Marshals Service Inter-Go 34%, Contract Detention Facility 12%, Dedicated Inter-Governmental S 7%, Service Processing Center 3%, Bureau of Prisons 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AOR | category | 24 | 0 | Chicago AOR 18; Saint Paul AOR 16; San Antonio AOR 14; New Orleans AOR 14 |
| FACILITY_NAME | who | 161 | 0 | EDEN DETENTION CENTER 2; BUTLER COUNTY JAIL 2; IMMIGRATION CENTERS OF AM 1; CAROLINE DETENTION FACILI 1 |
| CITY | other | 152 | 0 | BAKERSFIELD 3; LAREDO 3; ELOY 3; RAYMONDVILLE 2 |
| STATE | state | 45 | 0 | TX 26; LA 10; CA 8; FL 7 |
| FACILITY_TYPE_DETAILED | category | 6 | 0 | Inter-Governmental Servic 72; U.S. Marshals Service Int 56; Contract Detention Facili 19; Dedicated Inter-Governmen 12 |
| _INGESTED_AT | audit | 1 | 0 | 1785967413423707 165 |
| _SOURCE_RUN_ID | audit | 1 | 0 | c9a0e098-9a7a-4bd4-b554-9 165 |
| _SRC_SHA256 | who | 1 | 0 | 6438a5ca5c1fa0795905e48d2 165 |
