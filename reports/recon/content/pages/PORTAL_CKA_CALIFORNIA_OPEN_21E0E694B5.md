# PORTAL_CKA_CALIFORNIA_OPEN_21E0E694B5

rows 991  columns 50  scan 4.4s

roles: amount 8, audit 2, category 35, date 1, empty 1, other 2, who 2

## when

INGESTED_AT
  2026       991  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PCT_BARE | 991 | 0 | 0.05 | 0.66 | 0.95 | 98.89 |
| PCT_TREE | 991 | 0 | 0.01 | 0.80 | 1 | 68.53 |
| PCT_SHRUB | 991 | 0 | 0.27 | 0.91 | 0.98 | 310.12 |
| PCT_HERB | 991 | 0 | 0.51 | 0.98 | 1 | 497.66 |
| ACRES | 991 | 0.01 | 1.62 | 106.65 | 504.05 | 8.9K |
| HECTARES | 991 | 25.69 | 6.6K | 431.6K | 2.04M | 36.00M |

## who

NOTES1 by rows
       991  <Null>

NOTES1 by dollars
       98.89      991 rows  <Null>

SRC_SHA256 by rows
       991  c7024e502aef7fd669d0a77f4d8acb6edd0b306aff44559f6ea674985ff9ac43

SRC_SHA256 by dollars
       98.89      991 rows  c7024e502aef7fd669d0a77f4d8acb6edd0b306aff44559f6ea674985ff9

## who x when

NOTES1 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PCT_BARE
  <Null>                                    2026:98.89

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PCT_BARE
  c7024e502aef7fd669d0a77f4d8acb6edd0b306a  2026:98.89

## what

MCVNAME: Mediterranean California natur 31%, Malosma laurina – Lotus scopar 16%, Artemisia californica 15%, Lotus scoparius 9%, Artemisia californica – Eriogo 7%, Quercus agrifolia / Toxicodend 6%, Artemisia californica – Eriogo 4%, Quercus agrifolia 3%, Platanus racemosa – Quercus ag 2%, Quercus berberidifolia 2%, Adenostoma fasciculatum 2%, Nassella cernua 2%

MCVLEVEL: Association 65%, Group 29%, Alliance 5%, Semi-natural Association 1%, Semi-Natural Alliance 0%

MAPCODE: 7001 31%, 4401 16%, 4201 15%, 4100 9%, 4203 7%, 1102 6%, 4204 4%, 1101 3%, 2102 2%, 3200 2%, 7100 2%, 9200 2%

MAPCLASS: Mediterranean California Natur 31%, Malosma laurina-Acmispon glabe 16%, Artemisia californica 15%, Acmispon glaber 9%, Artemisia californica-Eriogonu 7%, Quercus agrifolia/Toxicodendro 6%, Artemisia californica-Eriogonu 4%, Quercus agrifolia/Salix lasiol 3%, Platanus racemosa-Quercus agri 2%, Quercus (berberidifolia; ×acut 2%, Stipa cernua 2%, Graded/Scraped/Maintained 2%

FB_HISTORIC: Scrub 49%, Herbaceous 30%, Oak Woodlands 9%, Chaparral 4%, Riparian Woodland 3%, Riparian Scrub 3%, Other Cover Types 2%, Herbaceous Wetland 1%, Unvegetated 1%, Other Woodlands 0%

ALLIANCE: Mediterranean California Natur 30%, Malosma laurina 16%, Artemisia californica 14%, Artemisia californica-Eriogonu 11%, Acmispon glaber 9%, Quercus agrifolia 9%, Platanus racemosa 3%, Adenostoma fasciculatum 2%, Quercus berberidifolia 2%, Stipa cernua 2%, Graded/Scraped/Maintained 2%, Salix lasiolepis 2%

ASSOCIATIO_1: Mediterranean California Natur 31%, Malosma laurina-Acmispon glabe 16%, Artemisia californica 15%, Acmispon glaber 9%, Artemisia californica-Eriogonu 7%, Quercus agrifolia/Toxicodendro 6%, Artemisia californica-Eriogonu 4%, Quercus agrifolia/Salix lasiol 3%, Platanus racemosa-Quercus agri 2%, Quercus (berberidifolia; ×acut 2%, Stipa cernua 2%, Graded/Scraped/Maintained 2%

HETEROGENEITY: LOW 38%, HIGH 35%, MODERATE 24%, NULL 2%

TREE_REL_COV: <1% 57%,  1-5% 19%, 5-35% 15%, 35-60% 4%, >60% 3%, NULL 2%

SHRUB_REL_COV: 5-35% 44%, 35-60% 25%, >60% 15%,  1-5% 11%, <1% 3%, NULL 2%

HERB_REL_COV: >60% 42%, 5-35% 27%, 35-60% 24%,  1-5% 3%, NULL 2%, <1% 2%

FIELD_VER_1: No 64%, Yes 36%, <Null> 0%

BARE_CAT: 3 47%, 2 28%, 1 19%, 4 4%, 0 2%, 5 1%

TREE_CAT: 1 57%, 2 19%, 3 15%, 4 4%, 5 3%, 0 2%

SHRUB_CAT: 3 44%, 4 25%, 5 15%, 2 11%, 1 3%, 0 2%

HERB_CAT: 5 42%, 3 27%, 4 24%, 2 3%, 1 2%, 0 2%

F1_FORMATIONCLASS_NAME: Mesomorphic Shrub and Herb Veg 83%, Mesomorphic Tree Vegetation (F 15%, NULL 2%, Xeromorphic Scrub and Herb Veg 0%

F2_FORMATIONSUBCLASS_NAME: Mediterranean Scrub and Grassl 82%, Temperate Forest 15%, NULL 2%, Temperate and Boreal Shrubland 2%, Warm Semi-Desert Scrub and Gra 0%

F3_FORMATION_NAME: Mediterranean Scrub 52%, Mediterranean Grassland and Fo 30%, Warm Temperate Forest 9%, Temperate Flooded and Swamp Fo 6%, NULL 2%, Temperate and Boreal Freshwate 1%, Cool Temperate Forest 0%, Temperate and Boreal Scrub and 0%, Warm Semi-Desert Scrub and Gra 0%

F4_DIVISION_NAME: California Scrub 52%, California Grassland and  Mead 30%, Madrean Forest and Woodland 9%, Western North America Warm Tem 6%, NULL 2%, Western North American Freshwa 1%, North America Introduced Everg 0%, Pacific Coast Scrub and Herb L 0%, Sonoran and Chihuahuan Semi-De 0%

F5_MACROGROUP_NAME: California Coastal Scrub 34%, California Annual and Perennia 30%, California Chaparral 18%, California Forest and Woodland 9%, Southwestern North American Ri 5%, NULL 2%, Western North America Wet Mead 1%, Introduced North American Medi 0%, Western North American Freshwa 0%, Vancouverian Coastal Dune and  0%, Madrean Warm Semi-Desert Wash  0%, Western North America Vernal P 0%

F6_GROUP_NAME: Mediterranean California natur 28%, Central and South Coastal Cali 26%, Californian maritime chaparral 15%, Californian broadleaf forest a 9%, Central and south coastal Cali 8%, Southwestern North American ri 3%, Southwestern North American ri 3%, NULL 2%, Californian xeric chaparral 2%, Californian mesic chaparral 2%, California perennial grassland 2%, Naturalized warm-temperate rip 1%

NATUESERVE: SOUTHERN CALIFORNIA COASTAL SC 49%, CALIFORNIA CENTRAL VALLEY AND  30%, SOUTHERN CALIFORNIA OAKWOODLAN 8%, NORTH AMERICAN WARM DESERT RIP 6%, <Null> 2%, SOUTHERN CALIFORNIA DRY-MESIC  2%, CALIFORNIA MESIC CHAPARRAL (CE 2%, NORTH AMERICAN ARIDWEST EMERGE 1%, MEDITERRANEAN CALIFORNIA FOOTH 1%

USNVC_CLAS: 2.B.1.Na.90.a 28%, 2.B.1.Na.2.b 26%, 2.B.1.Na.1.c 15%, 1.B.1.Nc.1.a 9%, 2.B.1.Na.2.a 8%, 1.B.3.Nd.2.b 4%, <Null> 2%, 2.B.1.Na.1.a 2%, 2.B.1.Na.1.b 2%, 2.B.1.Na.3.b 2%, 2.C.4.Nd.90.a 1%, 2.C.4.Nc.1.b 1%

CALVEGTYPE: California Sagebrush 36%, Sumac Shrub 21%, Soft Scrub Mixed Chaparral 14%, Coast Live Oak 13%, California Sycamore 4%, Chamise 3%, Scrub Oak 2%, Perennial Grasses and Forbs 2%, Barren 2%, Willow (Shrub) 2%, Baccharis (Riparian) 1%

CALVEGCODE: SS 36%, SM 21%, SQ 14%, QA 13%, QP 4%, CA 3%, CS 2%, HM 2%, BA 2%, WL 2%, ML 1%

CWHRTYPE: Mixed Chaparral 35%, Sagebrush 35%, Coastal Oak Woodland 12%, Valley Oak Woodland 4%, Coastal Scrub 3%, Valley Foothill Riparian 3%, Chamise-Redshank Chaparral 3%, Perennial Grassland 2%, Barren 2%, Lacustrine 1%, Eucalyptus 0%

CWHRCODE: MCH 35%, SGB 35%, COW 12%, VOW 4%, CSC 3%, VRI 3%, CRC 3%, PGS 2%, BAR 2%, LAC 1%, EUC 0%

GLOBALRANK: G4 47%, G5 27%, GNR 12%, G3 12%, GNA 1%, G2 0%

STATERANK: S4 59%, S5 26%, S2 9%, S3 5%, SNA 2%

SENSITIVE: N 83%, Y 17%

CACODE: 45.455.11 23%, 32.010.01 22%, 52.240.01 14%, 32.110.05 11%, 71.060.13 9%, 32.110.08 6%, 71.060.00 4%, 61.312.01 3%, 37.407.00 3%, 41.140.01 3%, 61.201.01 2%

MCVALLIANCE: Artemisia californica – (Salvi 36%, Malosma laurina 22%, Lotus scoparius – Lupinus albi 13%, Quercus agrifolia 12%, Platanus racemosa – Quercus ag 4%, Adenostoma fasciculatum 3%, Quercus berberidifolia 2%, Nassella spp. – Melica spp. 2%, Salix lasiolepis 2%, Artemisia californica – Salvia 2%, Salvia apiana 2%

MCVGROUP: Mediterranean California natur 29%, Central and South Coastal Cali 26%, Californian maritime chaparral 15%, Californian broadleaf forest a 9%, Central and south coastal Cali 9%, Southwestern North American ri 3%, Southwestern North American ri 3%, Californian xeric chaparral 2%, Californian mesic chaparral 2%, California perennial grassland 2%, Naturalized warm-temperate rip 1%

MCVMACROGROUP: California Coastal Scrub 35%, California Annual and Perennia 30%, California Chaparral 19%, California Forest and Woodland 9%, Southwestern North American Ri 6%, Western North America Wet Mead 1%, Introduced North American Medi 0%, Western North American Freshwa 0%, Vancouverian Coastal Dune and  0%, Madrean Warm Semi-Desert Wash  0%, Western North America Vernal P 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 984 | 0 | 991 5; 990 5; 989 5; 988 5 |
| MCVNAME | category | 34 | 0 | Mediterranean California  274; Malosma laurina – Lotus s 141; Artemisia californica 132; Lotus scoparius 83 |
| MCVLEVEL | category | 6 | 21 | Association 630; Group 284; Alliance 49; Semi-natural Association 5 |
| MAPCODE | category | 36 | 0 | 7001 274; 4401 141; 4201 132; 4100 83 |
| MAPCLASS | category | 35 | 0 | Mediterranean California  274; Malosma laurina-Acmispon  141; Artemisia californica 132; Acmispon glaber 83 |
| FB_HISTORIC | category | 10 | 0 | Scrub 482; Herbaceous 294; Oak Woodlands 86; Chaparral 35 |
| ALLIANCE | category | 29 | 0 | Mediterranean California  274; Malosma laurina 145; Artemisia californica 132; Artemisia californica-Eri 101 |
| ASSOCIATIO_1 | category | 32 | 0 | Mediterranean California  274; Malosma laurina-Acmispon  141; Artemisia californica 132; Acmispon glaber 83 |
| HETEROGENEITY | category | 4 | 0 | LOW 380; HIGH 351; MODERATE 239; NULL 21 |
| TREE_REL_COV | category | 6 | 0 | <1% 565;  1-5% 191; 5-35% 148; 35-60% 39 |
| SHRUB_REL_COV | category | 6 | 0 | 5-35% 432; 35-60% 249; >60% 151;  1-5% 107 |
| HERB_REL_COV | category | 6 | 0 | >60% 415; 5-35% 271; 35-60% 239;  1-5% 30 |
| FIELD_VER_1 | category | 3 | 0 | No 630; Yes 360; <Null> 1 |
| NOTES1 | who | 1 | 0 | <Null> 991 |
| PCT_BARE | amount | 880 | 0 | 0 99; 0.017986 5; 0.065015 5; 0.090909 5 |
| PCT_TREE | amount | 657 | 0 | 0 301; 0.535971 4; 0.569659 4; 0.863636 4 |
| PCT_SHRUB | amount | 939 | 0 | 0 27; 0.285714 6; 0.5 6; 0.411871 5 |
| PCT_HERB | amount | 955 | 0 | 0 33; 0.034173 5; 0.027864 5; 0.218182 5 |
| BARE_CAT | category | 6 | 0 | 3 467; 2 275; 1 185; 4 35 |
| TREE_CAT | category | 6 | 0 | 1 566; 2 192; 3 148; 4 40 |
| SHRUB_CAT | category | 6 | 0 | 3 434; 4 251; 5 152; 2 107 |
| HERB_CAT | category | 6 | 0 | 5 415; 3 271; 4 239; 2 30 |
| F1_FORMATIONCLASS_NAME | category | 4 | 0 | Mesomorphic Shrub and Her 825; Mesomorphic Tree Vegetati 144; NULL 21; Xeromorphic Scrub and Her 1 |
| F2_FORMATIONSUBCLASS_NAME | category | 5 | 0 | Mediterranean Scrub and G 810; Temperate Forest 144; NULL 21; Temperate and Boreal Shru 15 |
| F3_FORMATION_NAME | category | 9 | 0 | Mediterranean Scrub 517; Mediterranean Grassland a 293; Warm Temperate Forest 86; Temperate Flooded and Swa 55 |
| F4_DIVISION_NAME | category | 9 | 0 | California Scrub 517; California Grassland and  293; Madrean Forest and Woodla 86; Western North America War 55 |
| F5_MACROGROUP_NAME | category | 13 | 0 | California Coastal Scrub 337; California Annual and Per 293; California Chaparral 180; California Forest and Woo 86 |
| F6_GROUP_NAME | category | 17 | 0 | Mediterranean California  277; Central and South Coastal 254; Californian maritime chap 145; Californian broadleaf for 86 |
| NATUESERVE | category | 9 | 0 | SOUTHERN CALIFORNIA COAST 483; CALIFORNIA CENTRAL VALLEY 294; SOUTHERN CALIFORNIA OAKWO 79; NORTH AMERICAN WARM DESER 56 |
| USNVC_CLAS | category | 17 | 0 | 2.B.1.Na.90.a 277; 2.B.1.Na.2.b 254; 2.B.1.Na.1.c 145; 1.B.1.Nc.1.a 86 |
| UID | other | 997 | 0 | FNWS0991 5; FNWS0990 5; FNWS0989 5; FNWS0988 5 |
| CALVEGTYPE | category | 22 | 284 | California Sagebrush 244; Sumac Shrub 145; Soft Scrub Mixed Chaparra 93; Coast Live Oak 86 |
| CALVEGCODE | category | 22 | 284 | SS 244; SM 145; SQ 93; QA 86 |
| CWHRTYPE | category | 18 | 284 | Mixed Chaparral 244; Sagebrush 244; Coastal Oak Woodland 86; Valley Oak Woodland 25 |
| CWHRCODE | category | 18 | 284 | MCH 244; SGB 244; COW 86; VOW 25 |
| GLOBALRANK | category | 7 | 503 | G4 229; G5 133; GNR 60; G3 58 |
| STATERANK | category | 6 | 564 | S4 250; S5 110; S2 38; S3 22 |
| SENSITIVE | category | 3 | 305 | N 568; Y 118 |
| CACODE | category | 31 | 305 | 45.455.11 141; 32.010.01 132; 52.240.01 83; 32.110.05 64 |
| MCVALLIANCE | category | 24 | 305 | Artemisia californica – ( 233; Malosma laurina 145; Lotus scoparius – Lupinus 83; Quercus agrifolia 79 |
| MCVGROUP | category | 18 | 21 | Mediterranean California  277; Central and South Coastal 254; Californian maritime chap 145; Californian broadleaf for 86 |
| MCVMACROGROUP | category | 12 | 21 | California Coastal Scrub 337; California Annual and Per 293; California Chaparral 180; California Forest and Woo 86 |
| COMMUNITYLINK | empty | 1 | 991 |  |
| ACRES | amount | 1.0K | 0 | 1.281714 5; 0.7431408 5; 0.0503149 5; 330.4568 5 |
| HECTARES | amount | 975 | 0 | 5186.912 5; 3007.384 5; 203.6172 5; 1337311 5 |
| SHAPE__AREA | amount | 996 | 0 | 7457.04296875 5; 4323.78515625 5; 292.86328125 5; 1922212.796875 5 |
| SHAPE__LENGTH | amount | 979 | 0 | 818.736212905296 5; 376.192500861576 5; 94.6437015115094 5; 392842.022468277 5 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:48:04.17181 991 |
| SOURCE_RUN_ID | audit | 1 | 0 | d16ae0e0-7104-436c-b4ef-1 991 |
| SRC_SHA256 | who | 1 | 0 | c7024e502aef7fd669d0a77f4 991 |
