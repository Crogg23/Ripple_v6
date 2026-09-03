# PORTAL_SOC_COLORADO_INFORMA_9224CC38D4

rows 2.0K  columns 10  scan 3.2s

roles: audit 2, category 3, date 1, id 1, who 4

## when

INGESTED_AT
  2026      2.0K  ##############################

## who

NATIONAL_INDUSTRY by rows
       149  Other Nonmetallic Mineral Mining and Quarrying(**)
       101  Commercial and Institutional Building Construction
        77  Other Heavy and Civil Engineering Construction
        74  Other Metal Ore Mining(**)
        70  Support Activities for Oil and Gas Operations
        67  Other Vegetable (except Potato) and Melon Farming
        49  Electrical Contractors and Other Wiring Installation Contractors
        45  Industrial Building Construction
        43  Kaolin, Clay, and Ceramic and Refractory Minerals Mining(**)
        42  Postharvest Crop Activities (except Cotton Ginning)
        38  Finfish Fishing
        38  Highway, Street, and Bridge Construction
        35  Natural Gas Extraction
        35  New Housing For-Sale Builders
        31  Water and Sewer Line and Related Structures Construction
        31  All Other Miscellaneous Crop Farming
        30  Support Activities for Animal Production
        30  Power and Communication Line and Related Structures Construction
        30  Dimension Stone Mining and Quarrying
        29  Soil Preparation, Planting, and Cultivating

NAICS22 by rows
       149  212390
       101  236220
        77  237990
        74  212290
        70  213112
        67  111219
        49  238210
        45  236210
        43  212323
        42  115114
        38  114111
        38  237310
        35  211130
        35  236117
        31  111998
        31  237110
        30  212311
        30  115210
        30  237130
        29  115112

NAICS_INDUSTRY by rows
       149  Other Nonmetallic Mineral Mining and Quarrying (T)
       146  Support Activities for Mining (T)
       104  Residential Building Construction (T)
       101  Commercial and Institutional Building Construction (T)
        92  Support Activities for Crop Production (T)
        78  Stone Mining and Quarrying (T)
        77  Other Heavy and Civil Engineering Construction (T)
        74  Other Metal Ore Mining (T)
        72  Vegetable and Melon Farming (T)
        64  Sand, Gravel, Clay, and Ceramic and Refractory Minerals Mining and Qua
        56  Fishing (T)
        55  Noncitrus Fruit and Tree Nut Farming (T)
        49  Electrical Contractors and Other Wiring Installation Contractors (T)
        45  Industrial Building Construction (T)
        38  Highway, Street, and Bridge Construction (T)
        35  Natural Gas Extraction
        33  All Other Crop Farming (T)
        32  Nursery and Floriculture Production (T)
        32  Aquaculture (T)
        31  Water and Sewer Line and Related Structures Construction (T)

SRC_SHA256 by rows
      2.0K  b82837b41ed01d0ad1d69db1691c8b07ffbc0a31c882c95ac75071e15087a265

## who x when

NATIONAL_INDUSTRY by INGESTED_AT  LOAD STAMP, not an event date
  All Other Miscellaneous Crop Farming      2026:31
  Commercial and Institutional Building Co  2026:101
  Dimension Stone Mining and Quarrying      2026:30
  Electrical Contractors and Other Wiring   2026:49
  Finfish Fishing                           2026:38
  Highway, Street, and Bridge Construction  2026:38
  Industrial Building Construction          2026:45
  Kaolin, Clay, and Ceramic and Refractory  2026:43
  Natural Gas Extraction                    2026:35
  New Housing For-Sale Builders             2026:35
  Other Heavy and Civil Engineering Constr  2026:77
  Other Metal Ore Mining(**)                2026:74
  Other Nonmetallic Mineral Mining and Qua  2026:149
  Other Vegetable (except Potato) and Melo  2026:67
  Postharvest Crop Activities (except Cott  2026:42
  Power and Communication Line and Related  2026:30
  Soil Preparation, Planting, and Cultivat  2026:29
  Support Activities for Animal Production  2026:30
  Support Activities for Oil and Gas Opera  2026:70
  Water and Sewer Line and Related Structu  2026:31

NAICS22 by INGESTED_AT  LOAD STAMP, not an event date
  111219                                    2026:67
  111998                                    2026:31
  114111                                    2026:38
  115112                                    2026:29
  115114                                    2026:42
  115210                                    2026:30
  211130                                    2026:35
  212290                                    2026:74
  212311                                    2026:30
  212323                                    2026:43
  212390                                    2026:149
  213112                                    2026:70
  236117                                    2026:35
  236210                                    2026:45
  236220                                    2026:101
  237110                                    2026:31
  237130                                    2026:30
  237310                                    2026:38
  237990                                    2026:77
  238210                                    2026:49

## what

SECTOR: Construction (T) 33%, Mining, Quarrying, and Oil and 32%, Agriculture, Forestry, Fishing 32%, Utilities (T) 3%, Other Services (except Public  0%, Public Administration (T) 0%

SUBSECTOR: Mining (except Oil and Gas) (T 22%, Crop Production (T) 13%, Construction of Buildings (T) 13%, Heavy and Civil Engineering Co 11%, Specialty Trade Contractors (T 10%, Support Activities for Mining  7%, Animal Production and Aquacult 7%, Support Activities for Agricul 7%, Utilities (T) 3%, Fishing, Hunting and Trapping  3%, Oil and Gas Extraction (T) 2%, Forestry and Logging (T) 2%

INDUSTRY: Nonmetallic Mineral Mining and 21%, Nonresidential Building Constr 10%, Support Activities for Mining  10%, Metal Ore Mining (T) 9%, Foundation, Structure, and Bui 9%, Residential Building Construct 7%, Support Activities for Crop Pr 7%, Utility System Construction (T 6%, Other Heavy and Civil Engineer 6%, Vegetable and Melon Farming (T 5%, Fruit and Tree Nut Farming (T) 5%, Building Equipment Contractors 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NAICS22 | who | 121 | 0 | 212390 149; 236220 101; 237990 77; 212290 74 |
| INDEX_ITEM_DESCRIPTION | id | 2.0K | 0 | Commercial freezer instal 10; Chimney liner installatio 10; Chilled water system inst 10; Central heating equipment 10 |
| SECTOR | category | 6 | 0 | Construction (T) 652; Mining, Quarrying, and Oi 640; Agriculture, Forestry, Fi 632; Utilities (T) 68 |
| SUBSECTOR | category | 14 | 0 | Mining (except Oil and Ga 445; Crop Production (T) 263; Construction of Buildings 250; Heavy and Civil Engineeri 211 |
| INDUSTRY | category | 37 | 0 | Nonmetallic Mineral Minin 291; Nonresidential Building C 146; Support Activities for Mi 146; Metal Ore Mining (T) 130 |
| NAICS_INDUSTRY | who | 79 | 0 | Other Nonmetallic Mineral 149; Support Activities for Mi 146; Residential Building Cons 104; Commercial and Institutio 101 |
| NATIONAL_INDUSTRY | who | 122 | 0 | Other Nonmetallic Mineral 149; Commercial and Institutio 101; Other Heavy and Civil Eng 77; Other Metal Ore Mining(** 74 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:43:51.92857 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | be735a93-5ce1-410f-8ce9-d 2.0K |
| SRC_SHA256 | who | 1 | 0 | b82837b41ed01d0ad1d69db16 2.0K |
