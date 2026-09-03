# FED_IHS_SCB_FACILITY

rows 8.7K  columns 13  scan 3.1s

roles: audit 2, category 7, id 1, who 3

## who

FACILITY by rows
       248  UNDESIG LOCS
       231  HOME
       224  OFFICE
       199  OTHER
       194  CHS OTHER
       193  NURSING HOME
       192  AMBULANCE
       188  CHS HOSPITAL
       174  CHS PHYSICIAN OFFICE
       173  UNDESIG LABS
        62  SCHOOL  UNSP
        47  SCHOOL  UNSPECIFIED
        35  SCHOOL
        34  SCHOOL UNSPEC.
        28  SCHOOL  UNSPEC
        26  SCHOOL  SPECIFIED
        24  UNDESIGNATED LABS
        24  UNDESIGNATED LOCATION
        17  UNDES./UNSPEC.
        13  OFFSITE

SERVICE_UNIT by rows
       245  ANCHORAGE
       159  CHINLE
       150  SHIPROCK
       147  MT EDGECUMBE
       146  INTER ALASKA
       137  PHOENIX
       135  NON SERVICE UNIT
       128  RURAL IHB
       128  YUK KUS DELT
       122  CENTRAL WISCONSIN
       122  EASTERN MICHIGAN
       115  ROSEBUD
       115  TOHONO O'ODHAM NATION HC
       113  FORT DEFIANCE
       113  GALLUP
       111  CHEYENNE RIVER
       108  CROWNPOINT
       107  TUBA CITY
       105  PINE RIDGE
       104  PUGET SOUND

SRC_SHA256 by rows
      8.7K  2d7676e1af9e696cc0f85423fafdaa370ed0910dd4e3e3555a82bb271d77eb9d

## what

AREA: CALIFORNIA TRIBE/638 11%, NAVAJO 11%, BEMIDJI NON-IHS 10%, GREAT PLAINS TRIBE/638 10%, ALASKA TRIBE/638 9%, GREAT PLAINS 9%, ALASKA 7%, GREAT PLAINS NON-IHS 7%, NASHVILLE NON-IHS 7%, PHOENIX 6%, NAVAJO TRIBE/638 6%, ALASKA NON-IHS 6%

FACILITY_TYPE: ? 73%, Health Location 6%, Health Center 6%, Other 6%, Health Station 2%, Alaska Village Clinic 2%, Behavioral Health Facilities 1%, Alcohol Substance Abuse Treatm 1%, Hospital 1%, Dental Clinic 1%, School Health Center 1%, Assisted Living Center 0%

LOCATION_TYPE: ? 68%, Title 5 Tribal 638 15%, IHS 10%, Title 1 Tribal 3%, Non-IHS 3%, Urban 1%, Self-Governance 0%, 9 0%

BED_COUNT: 0 100%, 16 0%, 8 0%, 10 0%, 13 0%, 60 0%, 12 0%, 6 0%, 18 0%, 17 0%, 25 0%, 73 0%

STATUS: Inactive 51%, Active 49%

APC_FLAG: ? 77%, 1 22%, 2 0%, Y 0%, N 0%, 0 0%, A 0%

ITU_CODE: T 59%, I 25%, N 12%, U 3%, ? 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ASUFAC_CODE | id | 8.9K | 0 | 96003O 44; 960039 44; 960038 44; 960037 44 |
| AREA | category | 48 | 0 | CALIFORNIA TRIBE/638 583; NAVAJO 566; BEMIDJI NON-IHS 520; GREAT PLAINS TRIBE/638 514 |
| SERVICE_UNIT | who | 292 | 7 | ANCHORAGE 245; CHINLE 168; SHIPROCK 160; MT EDGECUMBE 147 |
| FACILITY | who | 4.8K | 0 | UNDESIG LOCS 248; HOME 231; OFFICE 224; OTHER 199 |
| FACILITY_TYPE | category | 24 | 2 | ? 6.3K; Health Location 538; Health Center 537; Other 489 |
| LOCATION_TYPE | category | 8 | 5 | ? 5.9K; Title 5 Tribal 638 1.3K; IHS 837; Title 1 Tribal 276 |
| BED_COUNT | category | 41 | 313 | 0 8.3K; 16 6; 8 5; 10 4 |
| STATUS | category | 2 | 0 | Inactive 4.5K; Active 4.3K |
| APC_FLAG | category | 7 | 7 | ? 6.7K; 1 1.9K; 2 41; Y 24 |
| ITU_CODE | category | 5 | 2 | T 5.2K; I 2.2K; N 1.1K; U 260 |
| INGESTED_AT | audit | 1 | 0 | 1786153353696100 8.7K |
| SOURCE_RUN_ID | audit | 1 | 0 | f2811f63-514f-4812-ad6e-d 8.7K |
| SRC_SHA256 | who | 1 | 0 | 2d7676e1af9e696cc0f85423f 8.7K |
