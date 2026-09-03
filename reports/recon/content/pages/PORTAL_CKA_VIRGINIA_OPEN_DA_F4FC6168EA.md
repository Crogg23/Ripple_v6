# PORTAL_CKA_VIRGINIA_OPEN_DA_F4FC6168EA

rows 356  columns 26  scan 5.2s

roles: amount 2, audit 2, category 9, date 1, other 7, who 6

## when

INGESTED_AT
  2026       356  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 356 | 4.1K | 60.3K | 296.7K | 584.4K | 26.32M |
| SHAPE_AREA | 356 | 898.6K | 107.31M | 1.27B | 1.75B | 64.42B |

## who

WATERSHED_NAME by rows
         6  Mill Creek
         3  Buffalo Creek
         3  Marsh Run
         3  Banister River
         2  Blue Run
         2  Beaver Creek
         2  Elk Creek
         2  Polecat Creek
         2  Dumps Creek
         2  Moores Creek
         2  Lewis Creek
         2  Reedy Creek
         2  Cedar Creek
         2  Hat Creek
         1  Cooks Creek
         1  Saylers Creek
         1  Hungars Creek
         1  Rapidan River #1
         1  Fairview Beach
         1  Deep Creek

WATERSHED_NAME by dollars
      584.4K        1 rows  Dan River
      370.3K        1 rows  Middle Clinch River
      328.8K        1 rows  Upper NF Holston River NTU 240
      298.6K        1 rows  Smith River 1
      295.1K        1 rows  Powell River - Sediment
      286.8K        1 rows  Chickahominy River
      275.9K        3 rows  Banister River
      260.9K        3 rows  Buffalo Creek
      250.4K        1 rows  Pigg River - Leesville Lake
      250.3K        6 rows  Mill Creek
      236.7K        1 rows  Lower NF Holston River NTU 239
      206.6K        1 rows  Tye River
      206.5K        1 rows  James River Riverine
      204.9K        1 rows  Willis River
      204.2K        1 rows  South Fork Holston River
      198.2K        2 rows  Elk Creek
      188.2K        1 rows  Rapidan River #2
      187.1K        1 rows  Moll Creek
      185.4K        1 rows  Lower Middle River
      182.6K        1 rows  Lower South River

IP_NAME by rows
        23  Dan River and Birch Creek
        16  Piankatank River, Gwynns Island, Milford Haven
        12  Reed Creek Watershed
        11  James River and Tributaries - City of Richmond
        11  North Fork Rivanna River
        10  Upper Rapidan River
        10  Upper Roanoke River - Part 1
         9  The Gulf, Barlow, Mattawoman, Jacobus and Hungars Creeks
         8  Smith River and Mayo River
         8  Mine Run, Mountain Run, Lower Rapidan
         8  Mattaponi River Watershed
         7  Slate River and Rock Island Creek 
         7  Big Otter River Watershed
         6  Middle Clinch River
         6  Upper York River
         6  Middle Fork Holston River and Wolf Creek
         5  Clinch River and Cove Creek
         5  Guest River
         5  Upper Roanoke River - Part 2
         5  Spring Creek, Briery Creek, Bush River, Little Sandy River and Saylers

IP_NAME by dollars
       1.73M       23 rows  Dan River and Birch Creek
      976.1K        8 rows  Smith River and Mayo River
      958.0K        8 rows  Mattaponi River Watershed
      835.7K        5 rows  North Fork Holston River Watershed
      762.4K       11 rows  James River and Tributaries - City of Richmond
      750.5K       10 rows  Upper Roanoke River - Part 1
      703.5K        6 rows  Middle Clinch River
      691.1K       11 rows  North Fork Rivanna River
      645.7K       12 rows  Reed Creek Watershed
      615.0K        7 rows  Big Otter River Watershed
      608.1K        5 rows  Powell River and Tributaries
      560.5K        5 rows  Clinch River and Cove Creek
      555.4K        5 rows  Pigg River and Old Womans Creek
      533.1K       10 rows  Upper Rapidan River
      503.6K        8 rows  Mine Run, Mountain Run, Lower Rapidan
      460.0K        6 rows  Middle Fork Holston River and Wolf Creek
      436.8K        4 rows  Flat, Nibbs, Deep and West Creeks
      431.9K        7 rows  Slate River and Rock Island Creek 
      430.5K        4 rows  Tye River, Hat Creek, Rucker Run and Piney River
      414.1K        5 rows  Three Creek, Mill Swamp, Darden Mill Run

REPORT_NAME by rows
        23  Dan River and Birch Creek
        16  Piankatank River, Gwynns Island, Milford Haven
        12  Reed Creek
        12  North Fork Rivanna River
        11  James River and Tributaries - City of Richmond
        10  Upper Roanoke River - Part 1
        10  Upper Rapidan River
         9  The Gulf, Barlow, Mattawoman, Jacobus and Hungars Creeks
         8  Lower Rapidan River
         8  Smith River and Mayo River
         8  Mattaponi River
         7  Slate River and Rock Island Creek
         7  Big Otter River
         6  Middle Clinch River
         6  Middle Fork Holston River and Wolf Creek
         6  Upper York River
         5  Buffalo River
         5  North Fork Holston River
         5  Guest River
         5  Upper Banister River and Tributaries

REPORT_NAME by dollars
       1.73M       23 rows  Dan River and Birch Creek
      976.1K        8 rows  Smith River and Mayo River
      958.0K        8 rows  Mattaponi River
      835.7K        5 rows  North Fork Holston River
      762.4K       11 rows  James River and Tributaries - City of Richmond
      750.5K       10 rows  Upper Roanoke River - Part 1
      710.5K       12 rows  North Fork Rivanna River
      703.5K        6 rows  Middle Clinch River
      645.7K       12 rows  Reed Creek
      615.0K        7 rows  Big Otter River
      608.1K        5 rows  Powell River and Tributaries
      560.5K        5 rows  Clinch River and Cove Creek
      555.4K        5 rows  Pigg River and Old Womans Creek
      533.1K       10 rows  Upper Rapidan River
      503.6K        8 rows  Lower Rapidan River
      460.0K        6 rows  Middle Fork Holston River and Wolf Creek
      436.8K        4 rows  Flat, Nibbs, Deep and West Creeks
      431.9K        7 rows  Slate River and Rock Island Creek
      430.5K        4 rows  Tye River, Hat Creek, Rucker Run and Piney River
      414.1K        5 rows  Three Creek, Mill Swamp and Darden Mill Run

DATA_DISCLAIMER by rows
       356  In collaboration with various agencies and organizations, DEQ strives 

DATA_DISCLAIMER by dollars
      26.32M      356 rows  In collaboration with various agencies and organizations, DE

## who x when

WATERSHED_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  Banister River                            2026:275.9K
  Beaver Creek                              2026:103.4K
  Blue Run                                  2026:103.9K
  Buffalo Creek                             2026:260.9K
  Cedar Creek                               2026:72.8K
  Chickahominy River                        2026:286.8K
  Cooks Creek                               2026:65.4K
  Dan River                                 2026:584.4K
  Deep Creek                                2026:136.1K
  Dumps Creek                               2026:124.7K
  Elk Creek                                 2026:198.2K
  Fairview Beach                            2026:47.0K
  Hat Creek                                 2026:100.5K
  Hungars Creek                             2026:18.3K
  James River Riverine                      2026:206.5K
  Lewis Creek                               2026:133.7K
  Lower NF Holston River NTU 239            2026:236.7K
  Marsh Run                                 2026:136.4K
  Middle Clinch River                       2026:370.3K
  Mill Creek                                2026:250.3K
  Moores Creek                              2026:92.8K
  Pigg River - Leesville Lake               2026:250.4K
  Polecat Creek                             2026:148.9K
  Powell River - Sediment                   2026:295.1K
  Rapidan River #1                          2026:49.5K
  Reedy Creek                               2026:134.8K
  Saylers Creek                             2026:47.3K
  Smith River 1                             2026:298.6K
  Tye River                                 2026:206.6K
  Upper NF Holston River NTU 240            2026:328.8K

IP_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  Big Otter River Watershed                 2026:615.0K
  Clinch River and Cove Creek               2026:560.5K
  Dan River and Birch Creek                 2026:1.73M
  Flat, Nibbs, Deep and West Creeks         2026:436.8K
  Guest River                               2026:279.4K
  James River and Tributaries - City of Ri  2026:762.4K
  Mattaponi River Watershed                 2026:958.0K
  Middle Clinch River                       2026:703.5K
  Middle Fork Holston River and Wolf Creek  2026:460.0K
  Mine Run, Mountain Run, Lower Rapidan     2026:503.6K
  North Fork Holston River Watershed        2026:835.7K
  North Fork Rivanna River                  2026:691.1K
  Piankatank River, Gwynns Island, Milford  2026:344.7K
  Pigg River and Old Womans Creek           2026:555.4K
  Powell River and Tributaries              2026:608.1K
  Reed Creek Watershed                      2026:645.7K
  Slate River and Rock Island Creek         2026:431.9K
  Smith River and Mayo River                2026:976.1K
  Spring Creek, Briery Creek, Bush River,   2026:394.5K
  The Gulf, Barlow, Mattawoman, Jacobus an  2026:148.6K
  Three Creek, Mill Swamp, Darden Mill Run  2026:414.1K
  Tye River, Hat Creek, Rucker Run and Pin  2026:430.5K
  Upper Rapidan River                       2026:533.1K
  Upper Roanoke River - Part 1              2026:750.5K
  Upper Roanoke River - Part 2              2026:410.3K
  Upper York River                          2026:304.1K

## what

INSERTED_BY: KPC74529 42%, kpc74529 35%, kpc74529@COV 23%

CHANGED_BY: kpc74529@COV 50%, KPC74529 50%

REGION: Blue Ridge - Roanoke 27%, Valley 21%, Southwest 18%, Northern 17%, Piedmont 13%, Tidewater 4%

REPORT_STATUS: Approved 93%, Draft 7%

WATERSHED_STATUS: Implementation Project Underwa 46%, Implementation Project Closed 29%, Implementation Project Not Ass 24%

POLLUTANTS: E. Coli 67%, Fecal Coliform 17%, E. Coli, Sediment (TSS) 8%, Sediment (TSS) 4%, E. Coli, Sediment 1%, E. Coli, Phosphorus, Sediment  1%, Sediment 1%, Fecal Coliform, Sediment (TSS) 1%, Sediment (TSS), Total Dissolve 1%, Phosphorus, Sediment 0%, Nitrogen, Sediment (TSS) 0%

SUCC_STORY_TYPES: EPA Type I 58%, EPA Type II 27%, Other 15%

PRIORITY: 1 98%, 2 2%

ELIGIBLE_319H: YES 69%, NO 23%, PRG 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 355 | 0 | 396 2; 395 2; 394 2; 393 2 |
| IP_NAME | who | 93 | 0 | Dan River and Birch Creek 23; Piankatank River, Gwynns  16; Reed Creek Watershed 12; North Fork Rivanna River 11 |
| INSERTED_BY | category | 4 | 223 | KPC74529 56; kpc74529 47; kpc74529@COV 30 |
| INSERTED_DATE | other | 125 | 223 | 2021/01/08 00:00:00+00 5; 2017/04/03 11:51:30+00 2; 2015/07/30 10:39:01+00 2; 2015/11/05 13:26:00+00 2 |
| CHANGED_BY | category | 2 | 0 | kpc74529@COV 178; KPC74529 178 |
| CHANGED_DATE | other | 230 | 0 | 2024/04/11 15:07:02+00 28; 2026/04/30 15:26:16+00 13; 2026/04/30 15:27:29+00 11; 2026/04/30 14:33:36+00 9 |
| GLOBALID | other | 347 | 0 | {69CF4E1D-44A5-498C-B201- 2; {8F8BDDE5-3B71-470A-95CB- 2; {A2FD1385-4B4F-44FA-A548- 2; {15111BFA-F055-4CB8-BF77- 2 |
| WATERSHED_ID | other | 357 | 0 | 385 2; 394 2; 391 2; 386 2 |
| WATERSHED_NAME | who | 333 | 0 | Mill Creek 6; Blue Run 3; Hat Creek 3; Marsh Run 3 |
| REPORT_NUMBER | other | 91 | 0 | TIP-91 23; TIP-56 16; TIP-113 12; TIP-3 12 |
| REPORT_NAME | who | 91 | 0 | Dan River and Birch Creek 23; Piankatank River, Gwynns  16; North Fork Rivanna River 12; Reed Creek 12 |
| EPA_APPROVED_DATE | who | 81 | 26 | 2020/01/02 00:00:00+00 23; 2014/08/28 00:00:00+00 16; 2015/11/12 00:00:00+00 12; 2014/01/02 00:00:00+00 11 |
| COMPLETE_REPORT_LINK | other | 87 | 28 | https://www.deq.virginia. 23; https://www.deq.virginia. 16; https://www.deq.virginia. 12; https://www.deq.virginia. 11 |
| REGION | category | 6 | 0 | Blue Ridge - Roanoke 97; Valley 73; Southwest 64; Northern 60 |
| REPORT_STATUS | category | 2 | 0 | Approved 330; Draft 26 |
| WATERSHED_STATUS | category | 3 | 0 | Implementation Project Un 164; Implementation Project Cl 105; Implementation Project No 87 |
| POLLUTANTS | category | 17 | 16 | E. Coli 223; Fecal Coliform 56; E. Coli, Sediment (TSS) 27; Sediment (TSS) 15 |
| SUCC_STORY_TYPES | category | 4 | 330 | EPA Type I 15; EPA Type II 7; Other 4 |
| SHAPE_LENGTH | amount | 361 | 0 | 66855.7066345591 3; 40585.3789455762 2; 49307.450920503 2; 66228.0756395842 2 |
| SHAPE_AREA | amount | 357 | 0 | 89215986.1470618 3; 58183224.6350163 2; 63363776.8609046 2; 156670257.097435 2 |
| PRIORITY | category | 2 | 0 | 1 348; 2 8 |
| ELIGIBLE_319H | category | 3 | 0 | YES 247; NO 83; PRG 26 |
| DATA_DISCLAIMER | who | 1 | 0 | In collaboration with var 356 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:40:05.51938 356 |
| SOURCE_RUN_ID | audit | 1 | 0 | 4338b01a-35a3-495d-aded-b 356 |
| SRC_SHA256 | who | 1 | 0 | da82036185cb4c559cfdbb150 356 |
