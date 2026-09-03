# PORTAL_CKA_CALIFORNIA_OPEN_C86733ED60

rows 10.0K  columns 34  scan 4.7s

roles: amount 5, audit 2, category 20, date 1, empty 2, id 2, other 1, who 2

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| DENSITYMIDPT | 9.8K | 5 | 17.50 | 37.50 | 87.50 | 194.4K |
| ACRES | 10.0K | 0 | 9.38 | 546.65 | 7.1K | 423.3K |
| HECTARES | 10.0K | 0 | 3.80 | 221.23 | 2.9K | 171.3K |
| SHAPE__AREA | 10.0K | 1.55 | 59.9K | 3.49M | 44.84M | 2.70B |
| SHAPE__LENGTH | 10.0K | 5.91 | 1.5K | 40.3K | 4.74M | 49.65M |

## who

MAPCLASS by rows
      4.0K  Larrea tridentata Desert Scrub
       734  Larrea tridentata - Ambrosia dumosa Bajada and Valley Desert Scrub
       670  Coleogyne ramosissima Mojave Desert Scrub
       652  Atriplex confertifolia - (Atriplex parryi) Scrub
       565  Mid-Elevation Mixed Desert Shrub Complex
       423  Artemisia tridentata - Mixed Shrub Dry Steppe and Shrubland
       364  Bedrock and Cliff Outcrop Sparse Vegetation Complex
       319  Semi-Desert Rock, Talus, and Steep Slope Sparse Scrub Complex
       247  Semi-Desert Mid Elevation Mixed Shrub and Herbaceous Vegetation Wash C
       242  Desert and Riparian Low Shrubland Wash Complex
       203  Pinus monophylla - Juniperus osteosperma / Artemisia nova - Artemisia 
       191  Sparse Desert Pavement Dwarf Scrub Complex
       135  Larrea tridentata - Encelia farinosa Desert Scrub
        96  Badlands Sparse Vegetation
        71  Yucca brevifolia / Coleogyne ramosissima - Artemisia tridentata - Arte
        70  Pinus monophylla - Juniperus osteosperma  - Yucca brevifolia Woodland
        69  Semi-Desert Basalt, Talus, and Cinders Sparse Scrub Complex
        66  Basalt and Volcanic Talus Mixed Desert Shrub Complex
        59  Pinus monophylla - Juniperus osteosperma / Sparse Understory Woodland
        58  Transitional Area

MAPCLASS by dollars
      169.4K     4.0K rows  Larrea tridentata Desert Scrub
       49.5K      734 rows  Larrea tridentata - Ambrosia dumosa Bajada and Valley Desert
       33.6K      652 rows  Atriplex confertifolia - (Atriplex parryi) Scrub
       26.9K      670 rows  Coleogyne ramosissima Mojave Desert Scrub
       26.4K      565 rows  Mid-Elevation Mixed Desert Shrub Complex
       20.6K      423 rows  Artemisia tridentata - Mixed Shrub Dry Steppe and Shrubland
       12.6K      364 rows  Bedrock and Cliff Outcrop Sparse Vegetation Complex
       12.6K      319 rows  Semi-Desert Rock, Talus, and Steep Slope Sparse Scrub Comple
       12.2K      203 rows  Pinus monophylla - Juniperus osteosperma / Artemisia nova - 
        7.9K      242 rows  Desert and Riparian Low Shrubland Wash Complex
        4.6K       11 rows  Roads and Transportation Structures
        4.4K      191 rows  Sparse Desert Pavement Dwarf Scrub Complex
        4.2K       39 rows  Allenrolfea occidentalis Shrubland
        3.3K       59 rows  Pinus monophylla - Juniperus osteosperma / Sparse Understory
        3.2K       28 rows  Mojave - Sonoran Dune Sparse Vegetation
        3.0K      135 rows  Larrea tridentata - Encelia farinosa Desert Scrub
        3.0K      247 rows  Semi-Desert Mid Elevation Mixed Shrub and Herbaceous Vegetat
        2.7K       53 rows  Artemisia nova - Artemisia arbuscula ssp. arbuscula Shrublan
        2.1K       96 rows  Badlands Sparse Vegetation
        2.1K       70 rows  Pinus monophylla - Juniperus osteosperma  - Yucca brevifolia

SRC_SHA256 by rows
     10.0K  13f4756097ffeef2e8e3f65613a3b64907394cf81d9fef0c275ffb29bc591070

SRC_SHA256 by dollars
      423.3K    10.0K rows  13f4756097ffeef2e8e3f65613a3b64907394cf81d9fef0c275ffb29bc59

## who x when

MAPCLASS by INGESTED_AT  LOAD STAMP, not an event date, dollars = ACRES
  Allenrolfea occidentalis Shrubland        2026:4.2K
  Artemisia nova - Artemisia arbuscula ssp  2026:2.7K
  Artemisia tridentata - Mixed Shrub Dry S  2026:20.6K
  Atriplex confertifolia - (Atriplex parry  2026:33.6K
  Badlands Sparse Vegetation                2026:2.1K
  Basalt and Volcanic Talus Mixed Desert S  2026:1.1K
  Bedrock and Cliff Outcrop Sparse Vegetat  2026:12.6K
  Coleogyne ramosissima Mojave Desert Scru  2026:26.9K
  Desert and Riparian Low Shrubland Wash C  2026:7.9K
  Larrea tridentata - Ambrosia dumosa Baja  2026:49.5K
  Larrea tridentata - Encelia farinosa Des  2026:3.0K
  Larrea tridentata Desert Scrub            2026:169.4K
  Mid-Elevation Mixed Desert Shrub Complex  2026:26.4K
  Mojave - Sonoran Dune Sparse Vegetation   2026:3.2K
  Pinus monophylla - Juniperus osteosperma  2026:2.1K
  Pinus monophylla - Juniperus osteosperma  2026:12.2K
  Pinus monophylla - Juniperus osteosperma  2026:3.3K
  Roads and Transportation Structures       2026:4.6K
  Semi-Desert Basalt, Talus, and Cinders S  2026:1.1K
  Semi-Desert Mid Elevation Mixed Shrub an  2026:3.0K
  Semi-Desert Rock, Talus, and Steep Slope  2026:12.6K
  Sparse Desert Pavement Dwarf Scrub Compl  2026:4.4K
  Transitional Area                         2026:91.06
  Yucca brevifolia / Coleogyne ramosissima  2026:1.8K

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = ACRES
  13f4756097ffeef2e8e3f65613a3b64907394cf8  2026:423.3K

## what

MCVNAME: Larrea tridentata 42%, Barren 9%, Larrea tridentata – Ambrosia d 8%, Coleogyne ramosissima 7%, Atriplex confertifolia 7%, Desert wash 6%, Desert & Semi-desert Biome 6%, Purshia tridentata – Artemisia 5%, Pinus monophylla – (Juniperus  4%, North American Warm Semi-Deser 2%, Urban 2%, Larrea tridentata – Encelia fa 1%

MCVLEVEL: Alliance 97%, Group 3%, Semi-Natural Alliance 0%

DENS_MOD: 10 - 25% 70%, 25 - 50% 17%, < 10% 11%, N/A 2%, 50 - 75% 0%, 75 - 100% 0%

PTRN_MOD: Homogeneous 91%, Linear 5%, N/A 2%, Gradational 1%, Bunched / Clumped 1%, Alternating 0%

HT_MOD: < 1 Meter 77%, 1 - 3 Meters 17%, 3 - 5 Meters 4%, N/A 2%, 5 - 15 Meters 1%

LANDFORM: Gently sloping ridges, fans, a 37%, Moderately dry steep slopes 30%, Nearly level terraces and plat 17%, Moderately moist steep slopes 15%, Valley flats 1%, Very moist steep slopes 0%, Gently sloping toe slopes, bot 0%

GEOLOGY: Qay - Young alluvium 32%, TvmF - Mafic volcanic deposits 12%, Qau - Undifferentiated younger 10%, TvsF - Silicic volcanic deposi 9%, Qao - Old alluvium 8%, Cb - Bonanza King Formation 6%, Cn - Nopah Formation 5%, Jis - Older Mesozoic silicic i 5%, QTa - Oldest alluvium 4%, OCp - Pogonip Group 4%, CZca - Campito Formation, undi 3%, QTau - Undifferentiated alluvi 3%

COMMENTS: N/A 97%, Deseert Holly Present 1%, Desert Pavement Understory 1%, Rock Understory 1%, Desert Holly Present 1%, Disturbed Vegetation and Soil  0%, Lava Beds and Cinder Cone Spar 0%, Disturbed Site 0%, Menodora Present 0%, Lava and Cinders Understory 0%, Galleta Grass Understory 0%, Salt Flats 0%

CALVEGTYPE: Creosote Bush 51%, Barren 11%, Blackbush 7%, Shadscale 7%, Desert Mixed Shrub 7%, Desert Mixed Wash Shrub 6%, Basin Sagebrush 5%, Singleleaf Pinyon Pine 4%, Joshua Tree 1%, Urban/Developed (General) 1%, Bitterbrush 1%

CALVEGCODE: DL 51%, BA 11%, DA 7%, DS 7%, DX 7%, NB 6%, BS 5%, PJ 4%, UJ 1%, UB 1%, BB 1%

CWHRTYPE: Desert Scrub 63%, Barren 11%, Alkali Desert Scrub 8%, Desert Wash 6%, Sagebrush 5%, Pinyon-Juniper 4%, Joshua Tree 1%, Urban 1%, Juniper 0%, Fresh Emergent Wetland 0%, Annual Grassland 0%

CWHRCODE: DSC 63%, BAR 11%, ASC 8%, DSW 6%, SGB 5%, PJN 4%, JST 1%, URB 1%, JUN 0%, FEW 0%, AGS 0%

GLOBALRANK: G5 90%, G4 10%, G4? 0%

STATERANK: S5 64%, S4 33%, S3 3%, S3S4 0%

SENSITIVE: N 97%, Y 3%

CACODE: 33.010.00 55%, 33.140.00 10%, 33.020.00 9%, 36.320.00 9%, 35.200.00 7%, 87.040.00 6%, 33.027.00 2%, 33.170.00 1%, 89.300.00 1%, 36.340.00 1%, 36.120.00 1%

MCVALLIANCE: Larrea tridentata 55%, Larrea tridentata – Ambrosia d 10%, Coleogyne ramosissima 9%, Atriplex confertifolia 9%, Purshia tridentata – Artemisia 7%, Pinus monophylla – (Juniperus  6%, Larrea tridentata – Encelia fa 2%, Yucca brevifolia 1%, Juniperus osteosperma 1%, Atriplex polycarpa 1%, Allenrolfea occidentalis 1%

MCVGROUP: Mojave-Sonoran Bajada & Valley 64%, Mojave Mid-Elevation Mixed Des 10%, Intermountain Shadscale - Salt 9%, Intermountain Basins Big Sageb 6%, Great Basin Pinyon - Juniper W 6%, North American Warm Semi-Deser 3%, North American Desert Alkaline 1%, Intermountain Utah Juniper Ope 1%, North American Warm Semi-Deser 0%, North American Warm Desert Rip 0%, Arid West Interior Freshwater  0%

MCVMACROGROUP: Mojave-Sonoran Semi-Desert Scr 64%, Great Basin-Intermountain Dry  10%, Intermountain Saltbush Scrub 9%, Great Basin-Intermountain Tall 6%, Intermountain Pinyon - Juniper 6%, North American Warm Semi-Deser 2%, North American Desert Alkali-S 1%, Warm Desert Lowland Freshwater 0%, Arid West Interior Freshwater  0%, Western Arid Lowland Flooded F 0%, North American Warm-Desert Xer 0%

COMMUNITYLINK: https://vegetation.cnps.org/al 55%, https://vegetation.cnps.org/al 10%, https://vegetation.cnps.org/al 9%, https://vegetation.cnps.org/al 9%, https://vegetation.cnps.org/al 6%, https://vegetation.cnps.org/al 6%, https://vegetation.cnps.org/al 2%, https://vegetation.cnps.org/al 1%, https://vegetation.cnps.org/al 1%, https://vegetation.cnps.org/al 1%, https://vegetation.cnps.org/al 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 10.0K | 0 | 10000 50; 9999 50; 9998 50; 9997 50 |
| MCVNAME | category | 34 | 96 | Larrea tridentata 4.0K; Barren 885; Larrea tridentata – Ambro 734; Coleogyne ramosissima 670 |
| MCVLEVEL | category | 4 | 2.3K | Alliance 7.4K; Group 243; Semi-Natural Alliance 3 |
| MAPCODE | other | 68 | 0 | S_CB 4.0K; S_CBWB 734; S_BLK 670; S_SHAD 652 |
| MAPCLASS | who | 68 | 0 | Larrea tridentata Desert  4.0K; Larrea tridentata - Ambro 734; Coleogyne ramosissima Moj 670; Atriplex confertifolia -  652 |
| DENS_MOD | category | 6 | 0 | 10 - 25% 7.0K; 25 - 50% 1.7K; < 10% 1.1K; N/A 155 |
| DENSITYMIDPT | amount | 6 | 155 | 17.5 7.0K; 37.5 1.7K; 5 1.1K; 62.5 50 |
| PTRN_MOD | category | 6 | 0 | Homogeneous 9.1K; Linear 541; N/A 156; Gradational 147 |
| HT_MOD | category | 5 | 0 | < 1 Meter 7.7K; 1 - 3 Meters 1.7K; 3 - 5 Meters 357; N/A 156 |
| LANDFORM | category | 7 | 0 | Gently sloping ridges, fa 3.7K; Moderately dry steep slop 3.0K; Nearly level terraces and 1.7K; Moderately moist steep sl 1.5K |
| GEOLOGY | category | 45 | 0 | Qay - Young alluvium 2.4K; TvmF - Mafic volcanic dep 885; Qau - Undifferentiated yo 773; TvsF - Silicic volcanic d 658 |
| COMMENTS | category | 12 | 0 | N/A 9.7K; Deseert Holly Present 112; Desert Pavement Understor 67; Rock Understory 57 |
| UID | id | 10.1K | 0 | DEVA10000 50; DEVA09999 50; DEVA09998 50; DEVA09997 50 |
| CALVEGTYPE | category | 31 | 58 | Creosote Bush 4.9K; Barren 1.1K; Blackbush 670; Shadscale 652 |
| CALVEGCODE | category | 31 | 58 | DL 4.9K; BA 1.1K; DA 670; DS 652 |
| CWHRTYPE | category | 16 | 58 | Desert Scrub 6.3K; Barren 1.1K; Alkali Desert Scrub 750; Desert Wash 569 |
| CWHRCODE | category | 16 | 58 | DSC 6.3K; BAR 1.1K; ASC 750; DSW 569 |
| GLOBALRANK | category | 4 | 2.6K | G5 6.7K; G4 706; G4? 5 |
| STATERANK | category | 5 | 2.6K | S5 4.8K; S4 2.4K; S3 211; S3S4 1 |
| SENSITIVE | category | 3 | 2.6K | N 7.2K; Y 211 |
| SENSITIVEFLAG | empty | 1 | 10.0K |  |
| CACODE | category | 23 | 2.6K | 33.010.00 4.0K; 33.140.00 734; 33.020.00 670; 36.320.00 652 |
| MCVALLIANCE | category | 23 | 2.6K | Larrea tridentata 4.0K; Larrea tridentata – Ambro 734; Coleogyne ramosissima 670; Atriplex confertifolia 652 |
| MCVGROUP | category | 18 | 2.3K | Mojave-Sonoran Bajada & V 4.9K; Mojave Mid-Elevation Mixe 773; Intermountain Shadscale - 697; Intermountain Basins Big  480 |
| MCVMACROGROUP | category | 14 | 2.3K | Mojave-Sonoran Semi-Deser 4.9K; Great Basin-Intermountain 794; Intermountain Saltbush Sc 697; Great Basin-Intermountain 480 |
| SECONDCACODE | empty | 1 | 10.0K |  |
| COMMUNITYLINK | category | 29 | 2.5K | https://vegetation.cnps.o 4.0K; https://vegetation.cnps.o 734; https://vegetation.cnps.o 670; https://vegetation.cnps.o 652 |
| ACRES | amount | 10.0K | 0 | 500.043059608815 50; 0.114595562946009 50; 20.9897321315866 50; 29.6667632981935 50 |
| HECTARES | amount | 10.0K | 0 | 202.361056168863 50; 0.0463753644899324 50; 8.49427720519153 50; 12.0057611815082 50 |
| SHAPE__AREA | amount | 10.0K | 0 | 3178940.13671875 50; 728.72265625 50; 133474.5390625 50; 188657.38671875 50 |
| SHAPE__LENGTH | amount | 9.9K | 0 | 24698.3573896652 50; 124.051825241173 50; 2005.93658904265 50; 2182.36933757472 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:02:30.65199 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 9b4a4739-bfc1-42fc-9166-1 10.0K |
| SRC_SHA256 | who | 1 | 0 | 13f4756097ffeef2e8e3f6561 10.0K |
