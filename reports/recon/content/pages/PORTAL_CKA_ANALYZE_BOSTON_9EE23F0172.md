# PORTAL_CKA_ANALYZE_BOSTON_9EE23F0172

rows 18  columns 14  scan 2.9s

roles: amount 3, audit 2, category 8, date 1, who 1

## when

INGESTED_AT
  2026        18  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| OBJECTID_12 | 17 | 0 | 0 | 0 | 0 | 0 |
| POINT_X | 18 | -71.16 | -71.07 | -71.04 | -71.04 | -1.3K |
| POINT_Y | 18 | 42.26 | 42.33 | 42.38 | 42.38 | 761.88 |

## who

SRC_SHA256 by rows
        18  78dd6235cc0f7e4fccc95aac96d01a6012d1f980f64e3ccac7338fdae8eef335

SRC_SHA256 by dollars
       -1.3K       18 rows  78dd6235cc0f7e4fccc95aac96d01a6012d1f980f64e3ccac7338fdae8ee

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = POINT_X
  78dd6235cc0f7e4fccc95aac96d01a6012d1f980  2026:-1.3K

## what

OBJECTID_1: 17 9%, 16 9%, 15 9%, 14 9%, 13 9%, 12 9%, 11 9%, 10 9%, 9 9%, 8 9%, 7 9%

PHONE: 635-5104 8%, 635-5241 8%, 635-5174 8%, 635-1275 8%, 635-5021 8%, 635-5181 8%, 635-5193 8%, 635-1328 8%, 635-5150 8%, 635-5146 8%, 635-5144 8%, 635-5198 8%

FAX: --- 17%, 635-5627 8%, 635-5628 8%, 635-1225 8%, 635-5273 8%, 635-1332 8%, 635-5298 8%, 635-5274 8%, 635-5152 8%, 635-5020 8%, 635-5078 8%

STREET: 1663 Columbia Rd 8%, 159 Norfolk Ave. 8%, Bunker Hill St. 8%, 475 Commercial St 8%, 5279 Washington S 8%, 160 Florence St. 8%, 20 South St. 8%, 5 Mildred Ave. 8%, 1 Worrell St. 8%, 155 Talbot Ave. 8%, 85 Olney St. 8%, 200 Heath St. 8%

NEIGH: Boston 17%, Dorchester 17%, South Boston 11%, Roxbury 11%, Charlestown 11%, Jamaica Plai 11%, West Roxbury 6%, Roslindale 6%, Mattapan 6%, East Boston 6%

ZIP: 2127 12%, 2118 12%, 2129 12%, 2130 12%, 2113 6%, 2132 6%, 2131 6%, 2126 6%, 2122 6%, 2124 6%, 2121 6%, 2119 6%

SITE: Family Friendly Beach at BCYF  8%, BCYF Mason Pool 8%, BCYF Clougherty Pool 8%, BCYF Mirabella Pool 8%, BCYF Draper Pool 8%, BCYF Flaherty Pool 8%, BCYF Curtis Hall 8%, BCYF Mildred Avenue 8%, BCYF Leahy-Holloran 8%, BCYF Perkins 8%, BCYF Holland 8%, BCYF Hennigan 8%

SHAPE_WKT: POINT (-71.035158067999987 42. 8%, POINT (-71.070818557999985 42. 8%, POINT (-71.067501163999964 42. 8%, POINT (-71.054309667999973 42. 8%, POINT (-71.159783226999934 42. 8%, POINT (-71.122208769999986 42. 8%, POINT (-71.114899934999983 42. 8%, POINT (-71.09120317299994 42.2 8%, POINT (-71.049285507999969 42. 8%, POINT (-71.080450551999945 42. 8%, POINT (-71.073619122999958 42. 8%, POINT (-71.10688861999995 42.3 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | category | 18 | 1 | 17 1; 16 1; 15 1; 14 1 |
| OBJECTID_12 | amount | 2 | 1 | 0.000000000000000 17 |
| PHONE | category | 18 | 0 | 635-5104 1; 635-5241 1; 635-5174 1; 635-1275 1 |
| FAX | category | 17 | 1 | --- 2; 635-5627 1; 635-5628 1; 635-1225 1 |
| STREET | category | 18 | 0 | 1663 Columbia Rd 1; 159 Norfolk Ave. 1; Bunker Hill St. 1; 475 Commercial St 1 |
| NEIGH | category | 10 | 0 | Boston 3; Dorchester 3; South Boston 2; Roxbury 2 |
| ZIP | category | 14 | 0 | 2127 2; 2118 2; 2129 2; 2130 2 |
| SITE | category | 18 | 0 | Family Friendly Beach at  1; BCYF Mason Pool 1; BCYF Clougherty Pool 1; BCYF Mirabella Pool 1 |
| SHAPE_WKT | category | 18 | 0 | POINT (-71.03515806799998 1; POINT (-71.07081855799998 1; POINT (-71.06750116399996 1; POINT (-71.05430966799997 1 |
| POINT_X | amount | 18 | 0 | -71.03515806799999 1; -71.07081855799998 1; -71.06750116399996 1; -71.05430966799997 1 |
| POINT_Y | amount | 18 | 0 | 42.329111339000065 1; 42.32580657700004 1; 42.38187742200006 1; 42.368752821000044 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:15:46.85054 18 |
| SOURCE_RUN_ID | audit | 1 | 0 | f2f08f90-5816-4727-8e15-8 18 |
| SRC_SHA256 | who | 1 | 0 | 78dd6235cc0f7e4fccc95aac9 18 |
