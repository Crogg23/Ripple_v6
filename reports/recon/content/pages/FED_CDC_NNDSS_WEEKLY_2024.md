# FED_CDC_NNDSS_WEEKLY_2024

rows 1.93M  columns 19  scan 4.5s

roles: audit 2, category 6, id 1, other 6, who 4

## who

REPORTING_AREA by rows
     17.7K  NEW YORK
     17.7K  CONNECTICUT
     17.7K  ILLINOIS
     17.7K  DELAWARE
     17.7K  MISSISSIPPI
     17.7K  COLORADO
     17.7K  ALABAMA
     17.7K  MOUNTAIN
     17.7K  SOUTH DAKOTA
     17.7K  MASSACHUSETTS
     17.7K  MARYLAND
     17.7K  INDIANA
     17.7K  FLORIDA
     17.7K  NEW MEXICO
     17.7K  WEST VIRGINIA
     17.7K  AMERICAN SAMOA
     17.7K  PENNSYLVANIA
     17.7K  NEVADA
     17.7K  PUERTO RICO
     17.7K  DISTRICT OF COLUMBIA

LABEL by rows
     16.7K  Measles, Imported
     16.7K  Giardiasis
     16.7K  Arboviral diseases, Western equine encephalitis virus disease
     16.7K  Salmonellosis (excluding Salmonella Typhi infection and Salmonella Par
     16.7K  Q fever, Chronic
     16.7K  Q fever, Total
     16.7K  Poliovirus infection, nonparalytic
     16.7K  Arboviral diseases, Powassan virus disease
     16.7K  Listeriosis, Probable
     16.7K  Meningococcal disease, Unknown serogroup
     16.7K  Viral hemorrhagic fevers, Marburg virus
     16.7K  Gonorrhea
     16.7K  Viral hemorrhagic fevers, Ebola virus
     16.7K  Streptococcal toxic shock syndrome
     16.7K  Rubella, congenital syndrome
     16.7K  Arboviral diseases, Jamestown Canyon  virus disease
     16.7K  Invasive pneumococcal disease, all ages, Confirmed
     16.7K  Arboviral diseases, West Nile virus disease
     16.7K  Salmonella Typhi infection
     16.7K  Anthrax

LOCATION1 by rows
     17.7K  WASHINGTON
     17.7K  ALABAMA
     17.7K  CONNECTICUT
     17.7K  NORTHERN MARIANA ISLANDS
     17.7K  GEORGIA
     17.7K  LOUISIANA
     17.7K  CALIFORNIA
     17.7K  NEW HAMPSHIRE
     17.7K  NEW YORK CITY
     17.7K  DELAWARE
     17.7K  NEW JERSEY
     17.7K  KENTUCKY
     17.7K  RHODE ISLAND
     17.7K  NEBRASKA
     17.7K  WYOMING
     17.7K  ALASKA
     17.7K  HAWAII
     17.7K  DISTRICT OF COLUMBIA
     17.7K  MISSISSIPPI
     17.7K  NEW YORK

GEOCODE by rows
     28.5K  POINT (-73.75522 42.65155)
     24.2K  POINT (-100.34987 44.36917)
     14.5K  POINT (-121.49086 38.57944)
     14.2K  POINT (-72.57627 44.26029)
     14.2K  POINT (-76.49015 38.97678)
     14.2K  POINT (-92.17785 38.57751)
     14.2K  POINT (-75.52474 39.15803)
     14.2K  POINT (-111.88822 40.76031)
     14.2K  POINT (-90.18045 32.29896)
     14.2K  POINT (-69.77631 44.31804)
     14.2K  POINT (-96.70731 40.81362)
     14.2K  POINT (-123.04382 44.93326)
     14.2K  POINT (-84.8787 38.19507)
     14.2K  POINT (-77.43367 37.54068)
     14.2K  POINT (-89.64361 39.8013)
     14.2K  POINT (-71.41198 41.82388)
     14.2K  POINT (-112.07581 33.44825)
     14.2K  POINT (-105.93825 35.69177)
     14.2K  POINT (-91.18665 30.44335)
     14.2K  POINT (-104.99203 39.74001)

## what

CURRENT_MMWR_YEAR: 2025 23%, 2024 22%, 2023 21%, 2022 21%, 2026 13%

CURRENT_WEEK_FLAG: - 96%, N 4%, U 0%

PREVIOUS_52_WEEKS_MAX_FLAG: - 84%, NC 16%

CUMULATIVE_YTD_CURRENT_MMWR_YEAR_FLAG: - 95%, N 4%, U 0%

CUMULATIVE_YTD_PREVIOUS_MMWR_YEAR_FLAG: - 93%, N 4%, NN 2%, NP 1%, U 0%

LOCATION2: NEW ENGLAND 8%, EAST NORTH CENTRAL 8%, WEST NORTH CENTRAL 8%, US TERRITORIES 8%, NON-US RESIDENTS 8%, MIDDLE ATLANTIC 8%, MOUNTAIN 8%, US RESIDENTS 8%, WEST SOUTH CENTRAL 8%, TOTAL 8%, EAST SOUTH CENTRAL 8%, SOUTH ATLANTIC 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| REPORTING_AREA | who | 140 | 0 | ARKANSAS 17.7K; MASSACHUSETTS 17.7K; WEST VIRGINIA 17.7K; NEW YORK CITY 17.7K |
| CURRENT_MMWR_YEAR | category | 5 | 0 | 2025 441.5K; 2024 425.9K; 2023 413.1K; 2022 400.4K |
| MMWR_WEEK | other | 53 | 0 | 9 40.5K; 18 40.5K; 17 40.5K; 19 40.5K |
| LABEL | who | 139 | 0 | Chlamydia trachomatis inf 16.7K; Viral hemorrhagic fevers, 16.7K; Viral hemorrhagic fevers, 16.7K; Viral hemorrhagic fevers, 16.7K |
| CURRENT_WEEK | other | 2.9K | 1.73M | 1 54.2K; 2 22.8K; 3 14.0K; 4 9.8K |
| CURRENT_WEEK_FLAG | category | 3 | 77.4K | - 1.78M; N 70.5K; U 7.1K |
| PREVIOUS_52_WEEK_MAX | other | 3.5K | 211.1K | 0 895.4K; 1 288.2K; 2 120.8K; 3 64.7K |
| PREVIOUS_52_WEEKS_MAX_FLAG | category | 2 | 623.4K | - 1.10M; NC 211.1K |
| CUMULATIVE_YTD_CURRENT_MMWR_YEAR | other | 19.2K | 1.28M | 1 106.9K; 2 54.1K; 3 35.9K; 4 27.6K |
| CUMULATIVE_YTD_CURRENT_MMWR_YEAR_FLAG | category | 3 | 235.9K | - 1.62M; N 70.5K; U 7.1K |
| CUMULATIVE_YTD_PREVIOUS_MMWR_YEAR | other | 21.6K | 1.23M | 1 117.5K; 2 61.5K; 3 38.5K; 4 29.5K |
| CUMULATIVE_YTD_PREVIOUS_MMWR_YEAR_FLAG | category | 5 | 272.4K | - 1.54M; N 66.1K; NN 34.3K; NP 14.6K |
| LOCATION1 | who | 114 | 359.0K | ARKANSAS 17.7K; MASSACHUSETTS 17.7K; WEST VIRGINIA 17.7K; NEW YORK CITY 17.7K |
| LOCATION2 | category | 26 | 1.57M | NEW ENGLAND 17.7K; EAST NORTH CENTRAL 17.7K; WEST NORTH CENTRAL 17.7K; US TERRITORIES 17.7K |
| SORT_ORDER | id | 1.96M | 0 | 20233007505 3.4K; 20233006770 3.4K; 20233002183 3.4K; 20233000812 3.4K |
| GEOCODE | who | 236 | 440.6K | POINT (-73.75522 42.65155 28.5K; POINT (-100.34987 44.3691 24.2K; POINT (-121.49086 38.5794 14.5K; POINT (-93.09649 44.94339 14.2K |
| INGESTED_AT | audit | 1 | 0 | 1785965335067376 1.93M |
| SOURCE_RUN_ID | audit | 1 | 0 | 86b51a2e-db69-44ce-83d8-6 1.93M |
| SRC_SHA256 | other | 1 | 0 | 69ca2a7147b133e5da4c444d8 1.93M |
