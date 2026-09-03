# PORTAL_CKA_INDIANA_DATA_HUB_BA1B037C9E

rows 26  columns 13  scan 3.5s

roles: amount 2, audit 2, category 8, date 1, who 1

## when

INGESTED_AT
  2026        26  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 26 | 37.98 | 39.88 | 41.65 | 41.67 | 1.0K |
| LONGITUDE | 26 | -87.59 | -86.27 | -84.85 | -84.85 | -2.2K |

## who

SRC_SHA256 by rows
        26  eb2fa69932c9d008ee4e50d1a5caf1015e0ae45f484c5d77cff21f9514441e54

SRC_SHA256 by dollars
        1.0K       26 rows  eb2fa69932c9d008ee4e50d1a5caf1015e0ae45f484c5d77cff21f951444

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  eb2fa69932c9d008ee4e50d1a5caf1015e0ae45f  2026:1.0K

## what

LOCATION_ID: 26 8%, 25 8%, 24 8%, 23 8%, 22 8%, 21 8%, 20 8%, 19 8%, 18 8%, 17 8%, 16 8%, 15 8%

LOCATION_ZIP: 47807 8%, 47591 8%, 46168 8%, 46619 8%, 47111 8%, 47274 8%, 46403 8%, 46201 8%, 47374 8%, 46383 8%, 46350 8%, 46143 8%

LOCATION_CITY: Indianapolis 19%, Gary 12%, Fort Wayne 12%, Terre Haute 6%, Vincennes 6%, Plainfield 6%, South Bend 6%, Charlestown 6%, Seymour 6%, Richmond 6%, Valparaiso 6%, La Porte 6%

LOCATION_STREET: 88 Wabash Court 8%, 1433 Willow Street 8%, 401 Plainfield Commons 8%, 4218 Western Ave 8%, 7509 Charlestown Pike 8%, 357 Tanger Blvd Ste 215 8%, 5001 East Dunes Highway 8%, 3419 English Ave 8%, 4265 S A St 8%, 2507 Cumberland Drive 8%, 1230 West State Road 2 8%, 65 Airport Parkway Suite 104 8%

LOCATION_COUNTY: 89 18%, 97 18%, 3 12%, 167 6%, 83 6%, 63 6%, 141 6%, 19 6%, 71 6%, 177 6%, 127 6%, 91 6%

WEBSITE: https://www.winrecovery.org/ 19%, https://www.porterstarke.org/ 12%, https://vallevistahospital.com 12%, https://victoryclinic.com/ 6%, https://www.ctcprograms.com/lo 6%, https://www.ctcprograms.com/lo 6%, https://www.newseason.com/trea 6%, https://www.eskenazihealth.edu 6%, https://www.ctcprograms.com/lo 6%, https://www.ctcprograms.com/lo 6%, https://medmark.com/locations/ 6%, https://medmark.com/locations/ 6%

NAME: WIN Recovery-Vigo 8%, WIN Recovery-Knox 8%, WIN Recovery-Hendricks 8%, Victory Clinical Services II 8%, Southern Indiana Comprehensive 8%, Seymour Comprehensive Treatmen 8%, Semoran - New Season Treatment 8%, Sandra Eskenazi Mental Health  8%, Richmond Comprehensive Treatme 8%, Porter-Starke Recovery Center- 8%, Porter-Starke Recovery Center- 8%, New Vista Outpatient Recovery  8%

PHONE: 812-231-3740 8%, 812-494-2215 8%, 317-268-2941 8%, 574-233-1524 8%, 812-256-4686 8%, 877-774-7235 8%, 219-938-4651 8%, 317-880-8491 8%, 765-962-8843 8%, 219-476-4676 8%, 219-531-0035 8%, 317-883-5330 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| LOCATION_ID | category | 26 | 0 | 26 1; 25 1; 24 1; 23 1 |
| LOCATION_ZIP | category | 26 | 0 | 47807 1; 47591 1; 46168 1; 46619 1 |
| LOCATION_CITY | category | 22 | 0 | Indianapolis 3; Gary 2; Fort Wayne 2; Terre Haute 1 |
| LOCATION_STREET | category | 26 | 0 | 88 Wabash Court 1; 1433 Willow Street 1; 401 Plainfield Commons 1; 4218 Western Ave 1 |
| LOCATION_COUNTY | category | 21 | 0 | 89 3; 97 3; 3 2; 167 1 |
| WEBSITE | category | 22 | 0 | https://www.winrecovery.o 3; https://www.porterstarke. 2; https://vallevistahospita 2; https://victoryclinic.com 1 |
| NAME | category | 26 | 0 | WIN Recovery-Vigo 1; WIN Recovery-Knox 1; WIN Recovery-Hendricks 1; Victory Clinical Services 1 |
| PHONE | category | 25 | 0 | 812-231-3740 1; 812-494-2215 1; 317-268-2941 1; 574-233-1524 1 |
| LATITUDE | amount | 26 | 0 | 39.46705 1; 38.66276 1; 39.71541 1; 41.67164 1 |
| LONGITUDE | amount | 26 | 0 | -87.42051 1; -87.53614 1; -86.35378 1; -86.30915 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:18:40.87607 26 |
| SOURCE_RUN_ID | audit | 1 | 0 | fce04d2d-925c-4c89-86bd-5 26 |
| SRC_SHA256 | who | 1 | 0 | eb2fa69932c9d008ee4e50d1a 26 |
