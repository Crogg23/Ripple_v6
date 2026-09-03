# FED_WQP_MONITORING_STATIONS

rows 5.8K  columns 40  scan 4.3s

roles: amount 9, audit 2, category 17, empty 1, id 1, other 7, who 3

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| DRAINAGEAREAMEASURE_MEASUREVALUE | 257 | 0.01 | 4.61 | 431.67 | 474 | 6.4K |
| CONTRIBUTINGDRAINAGEAREAMEASURE_MEASUREVALUE | 53 | 0.28 | 6.40 | 353.08 | 416 | 1.8K |
| LATITUDEMEASURE | 5.8K | 0 | 41.56 | 42.01 | 42.02 | 230.4K |
| LONGITUDEMEASURE | 5.8K | -71.88 | -71.57 | 0 | 0 | -396.3K |
| HORIZONTALACCURACYMEASURE_MEASUREVALUE | 4.0K | -5 | 1 | 5 | 5 | 3.8K |
| VERTICALMEASURE_MEASUREVALUE | 4.1K | -2.68 | 116 | 556.35 | 717 | 614.2K |

## who

MONITORINGLOCATIONNAME by rows
       115  Narragansett Bay
        57  Rhode Island DEM And DOH
        33  Sakonnet River
        27  Pawcatuck River
        18  Mt. Hope Bay
        12  Providence River
        12  Pawtuxet River
        11  Blackstone River
        10  Seekonk River
         7  Greenwich Bay
         7  Wood River
         6  Warren River
         6  Ten Mile River
         6  Ninigret Pond
         5  No name
         5  Point Judith Pond
         5  Quicksand Pond
         5  RIDAD-0001
         5  Gorton Pond
         4  Block Island Sound

MONITORINGLOCATIONNAME by dollars
         717        1 rows  NORTH NASHUA R NR COMMERCIAL RD AT LEOMINSTER, MA
         705        1 rows  RI-BUW   85
         705        1 rows  RI-BUW  397
         695        1 rows  RI-BUW  116
         662        1 rows  RI-BUW  132
         655        1 rows  RI-BUW  140
         630        1 rows  RI-FOW   40
         623        1 rows  RI-WGW   67
         622        1 rows  RI-GLW  128
         620        1 rows  RI-BUW  126
         615        1 rows  RI-BUW  125
         615        1 rows  RI-BUW  130
         615        1 rows  RI-BUW  398
         615        1 rows  RI-FOW  291
         608        1 rows  RI-BUW   81
      607.15        1 rows  RI-FOW    4
         605        1 rows  RI-GLW  125
         594        1 rows  BURLINGAME RESERVOIR NR W. GLOCESTER, RI
         592        1 rows  RI-BUW   83
         587        1 rows  RI-GLW  123

MONITORINGLOCATIONDESCRIPTIONTEXT by rows
        83  Rhode Island DEM And DOH
        53  ID generated from official Excel list provided for Rhode Island
        39  Lake/Pond: Hydrographic Category = Perennial
        34  Lake
        29  Rhode Island
        27  Narragansett Bay
        20  Reservoir
        19  SmallStreams
        14  {"epa_region": "1", "stream_order": "5", "site_type": "Urban"}
        14  Station area=.;Strata=RI Fish ;Stratum area=.
        12  LargeStreams
        12  Beach
        10  Rhode Island Fish Survey
        10  US EPA National Exposure Research Lab
         8  Bay
         8  RiversOther
         7  NonUrban
         7  Urban
         6  {"epa_region": "1", "stream_order": "5", "site_type": "Non-urban"}
         5  Rhode Island-South Coast

MONITORINGLOCATIONDESCRIPTIONTEXT by dollars
        1.4K       19 rows  SmallStreams
      455.51       12 rows  LargeStreams
       79.60        3 rows  WTBDY_NM: Block Island Sound-PROVINCE: Virginian Province-DS
       69.24        8 rows  RiversOther
       60.60        4 rows  WTBDY_NM: Narragansett Bay-PROVINCE: Virginian Province-DSNT
          45        1 rows  XLON_DD="-71.699";XLAT_DD="41.539";FLOWSITE="WADEABLE";SITET
       30.10        3 rows  WTBDY_NM: Sakonnet River-PROVINCE: Virginian Province-DSNTYP
           6        1 rows  XLON_DD="-71.1295";XLAT_DD="41.5589";STRAHLER="0";ST_ORDER="
        5.60        2 rows  WTBDY_NM: Greenwich Bay-PROVINCE: Virginian Province-DSNTYPE
        4.70        1 rows  WTBDY_NM: Providence River-PROVINCE: Virginian Province-DSNT
        3.40        1 rows  WTBDY_NM: Mt. Hope Bay-PROVINCE: Virginian Province-DSNTYPE:
           0       10 rows  Rhode Island Fish Survey
           0       27 rows  Narragansett Bay
           0        1 rows  Buzzards Bay-Augmented
           0       29 rows  Rhode Island
           0       14 rows  Station area=.;Strata=RI Fish ;Stratum area=.
           0        5 rows  Rhode Island-South Coast
           0        1 rows  FW_ECO3="EHIGH";URBAN="NonUrban";STRAHLERORDER="4th";VISIT_N
           0        1 rows  Chipuxet River off Route 138 at the USGS gage #1117350
           0        1 rows  West River at end of Alexander Street off of Mineral Spring,

SRC_SHA256 by rows
      5.8K  6dc0d12120977c4474b745cf1823365f046296fb7d37be02602c5f46622cf981

SRC_SHA256 by dollars
      614.2K     5.8K rows  6dc0d12120977c4474b745cf1823365f046296fb7d37be02602c5f46622c

## what

ORGANIZATIONIDENTIFIER: USGS-MA 75%, RIDEM 5%, 21RIBCH 5%, NARS_WQX 4%, EMAP_CS_WQX 2%, AQS 2%, EMAP_CS 2%, WWMD_VA 2%, DEMOTEST_WQX 1%, NALMS 1%, 1111REG1 1%, GLEON 1%

ORGANIZATIONFORMALNAME: USGS Massachusetts Water Scien 74%, EPA National Aquatic Resources 5%, Rhode Island 5%, Rhode Island Department of Hea 5%, Environmental Monitoring and A 4%, Air Quality System 2%, World Water Monitoring Day Vir 1%, DEMOTEST_WQX 1%, North American Lake Management 1%, US EPA Region 1 1%, GLEON Lake Observer (Volunteer 1%, Blackstone River Coalition (Vo 0%

MONITORINGLOCATIONTYPENAME: Well 63%, Stream 6%, River/Stream 6%, Other-Surface Water 5%, Estuary 4%, Lake 4%, BEACH Program Site-Ocean 3%, Atmosphere 3%, Well: Multiple wells 2%, Well: Test hole not completed  2%, Lake, Reservoir, Impoundment 2%, BEACH Program Site-Lake 1%

HUCEIGHTDIGITCODE: 01090005 49%, 01090004 35%, 01090003 14%, 01100001 1%, 01090002 1%, 02030203 0%, 01100003 0%

SOURCEMAPSCALENUMERIC: 24000 90%, 5000 9%, 25000 1%, 0 0%, 100000 0%, 500 0%

HORIZONTALACCURACYMEASURE_MEASUREUNITCODE: seconds 90%, Unknown 8%, hours 2%

HORIZONTALCOLLECTIONMETHODNAME: Interpolated from MAP. 66%, GPS-Unspecified 14%, Unknown 5%, Interpolation-Photo 5%, Mapping grade GPS unit (handhe 4%, GPS Code (Pseudo Range) Differ 2%, Interpolated from Digital MAP. 1%, Interpolation-Digital Map Sour 1%, Differentially corrected Globa 0%, Interpolation-Map 0%, Unknown. 0%, Interpolation-Satellite 0%

HORIZONTALCOORDINATEREFERENCESYSTEMDATUMNAME: NAD83 90%, WGS84 4%, OTHER 4%, UNKWN 1%, NAD27 0%

VERTICALMEASURE_MEASUREUNITCODE: feet 94%, ft 3%, m 3%

VERTICALACCURACYMEASURE_MEASUREUNITCODE: feet 95%, m 5%

VERTICALCOLLECTIONMETHODNAME: Interpolated from topographic  63%, Level or other surveyed method 23%, Altimeter. 6%, Interpolated from Digital Elev 3%, Unknown. 2%, Unknown 2%, Digital Elevation Model 1%, GNSS2 - Level 2 Quality Survey 1%, Reported method of determinati 0%, Other 0%, Global Positioning System. 0%, Differentially corrected Globa 0%

VERTICALCOORDINATEREFERENCESYSTEMDATUMNAME: NGVD29 87%, NAVD88 8%, Unknown 3%, UNKWN 2%

COUNTYCODE: 009 53%, 007 27%, 003 13%, 005 5%, 001 1%, 000 0%

AQUIFERNAME: Sand and gravel aquifers (glac 98%, Other aquifers 2%, New York and New England cryst 0%

FORMATIONTYPETEXT: Stratified Deposits, Undiffere 41%, Outwash 29%, Bedrock 14%, Till 14%, Sediments, Undifferentiated 1%, Swamp Deposits 0%, Crystalline Rocks, Undifferent 0%, Marine Deposits 0%

AQUIFERTYPENAME: Unconfined single aquifer 96%, Confined single aquifer 2%, UNCONFINED 2%, Mixed (confined and unconfined 0%, Confined multiple aquifers 0%

PROVIDERNAME: NWIS 73%, STORET 27%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ORGANIZATIONIDENTIFIER | category | 29 | 0 | USGS-MA 4.2K; RIDEM 269; 21RIBCH 268; NARS_WQX 237 |
| ORGANIZATIONFORMALNAME | category | 28 | 0 | USGS Massachusetts Water  4.2K; EPA National Aquatic Reso 270; Rhode Island 269; Rhode Island Department o 268 |
| MONITORINGLOCATIONIDENTIFIER | id | 5.7K | 0 | WWMD_VA-UENERL-2003 30; WWMD_VA-RIDAD-9 30; WWMD_VA-RIDAD-8 30; WWMD_VA-RIDAD-7 30 |
| MONITORINGLOCATIONNAME | who | 5.2K | 13 | Narragansett Bay 138; Rhode Island DEM And DOH 84; Sakonnet River 55; Pawcatuck River 48 |
| MONITORINGLOCATIONTYPENAME | category | 36 | 0 | Well 3.5K; Stream 345; River/Stream 330; Other-Surface Water 254 |
| MONITORINGLOCATIONDESCRIPTIONTEXT | who | 380 | 5.0K | Rhode Island DEM And DOH 83; ID generated from officia 53; Lake/Pond: Hydrographic C 39; Lake 34 |
| HUCEIGHTDIGITCODE | category | 7 | 364 | 01090005 2.7K; 01090004 1.9K; 01090003 785; 01100001 51 |
| DRAINAGEAREAMEASURE_MEASUREVALUE | amount | 232 | 5.6K | 0.30 3; 0.15 3; 0.31 3; 0.50 3 |
| DRAINAGEAREAMEASURE_MEASUREUNITCODE | other | 1 | 5.6K | sq mi 257 |
| CONTRIBUTINGDRAINAGEAREAMEASURE_MEASUREVALUE | amount | 51 | 5.8K | 4.32 2; 0.28 2; 5.52 1; 295 1 |
| CONTRIBUTINGDRAINAGEAREAMEASURE_MEASUREUNITCODE | other | 1 | 5.8K | sq mi 53 |
| LATITUDEMEASURE | amount | 4.5K | 2 | 0E-10 299; 41.57058610000000 42; 41.8801400000 33; 41.4900000000 31 |
| LONGITUDEMEASURE | amount | 4.2K | 2 | 0E-10 299; -71.3813000000 33; -71.2900000000 31; -71.3630000000 30 |
| SOURCEMAPSCALENUMERIC | category | 6 | 2.8K | 24000 2.7K; 5000 263; 25000 20; 0 8 |
| HORIZONTALACCURACYMEASURE_MEASUREVALUE | amount | 7 | 1.5K | 1 3.5K; Unknown 348; .01 179; 5 163 |
| HORIZONTALACCURACYMEASURE_MEASUREUNITCODE | category | 3 | 1.5K | seconds 3.9K; Unknown 348; hours 94 |
| HORIZONTALCOLLECTIONMETHODNAME | category | 18 | 0 | Interpolated from MAP. 3.9K; GPS-Unspecified 839; Unknown 272; Interpolation-Photo 265 |
| HORIZONTALCOORDINATEREFERENCESYSTEMDATUMNAME | category | 5 | 2 | NAD83 5.2K; WGS84 256; OTHER 253; UNKWN 82 |
| VERTICALMEASURE_MEASUREVALUE | amount | 1.4K | 1.7K | 0 156; 60.00 67; 70.00 48; 65.00 45 |
| VERTICALMEASURE_MEASUREUNITCODE | category | 3 | 1.7K | feet 3.9K; ft 139; m 111 |
| VERTICALACCURACYMEASURE_MEASUREVALUE | amount | 86 | 1.8K | 5 1.4K; 10 835; 1 570; .1 424 |
| VERTICALACCURACYMEASURE_MEASUREUNITCODE | category | 2 | 1.8K | feet 3.9K; m 192 |
| VERTICALCOLLECTIONMETHODNAME | category | 12 | 1.9K | Interpolated from topogra 2.5K; Level or other surveyed m 905; Altimeter. 241; Interpolated from Digital 101 |
| VERTICALCOORDINATEREFERENCESYSTEMDATUMNAME | category | 4 | 1.7K | NGVD29 3.6K; NAVD88 327; Unknown 139; UNKWN 68 |
| COUNTRYCODE | other | 1 | 0 | US 5.8K |
| STATECODE | other | 1 | 0 | 44 5.8K |
| COUNTYCODE | category | 6 | 292 | 009 2.9K; 007 1.5K; 003 735; 005 284 |
| AQUIFERNAME | category | 3 | 4.5K | Sand and gravel aquifers  1.3K; Other aquifers 21; New York and New England  4 |
| LOCALAQFRNAME | empty | 0 | 5.8K |  |
| FORMATIONTYPETEXT | category | 8 | 5.1K | Stratified Deposits, Undi 282; Outwash 200; Bedrock 99; Till 99 |
| AQUIFERTYPENAME | category | 5 | 4.9K | Unconfined single aquifer 874; Confined single aquifer 19; UNCONFINED 17; Mixed (confined and uncon 3 |
| CONSTRUCTIONDATETEXT | other | 1.2K | 2.9K | 1957 70; 20220510 67; 1950 59; 1949 55 |
| WELLDEPTHMEASURE_MEASUREVALUE | amount | 1.2K | 2.2K | 50.0 47; 30.0 44; 20.0 41; 40.0 34 |
| WELLDEPTHMEASURE_MEASUREUNITCODE | other | 1 | 2.2K | ft 3.7K |
| WELLHOLEDEPTHMEASURE_MEASUREVALUE | amount | 810 | 3.8K | 34 25; 40 25; 44 23; 42 23 |
| WELLHOLEDEPTHMEASURE_MEASUREUNITCODE | other | 1 | 3.8K | ft 2.0K |
| PROVIDERNAME | category | 2 | 0 | NWIS 4.2K; STORET 1.6K |
| INGESTED_AT | audit | 1 | 0 | 1786164151798437 5.8K |
| SOURCE_RUN_ID | audit | 1 | 0 | b5c68388-e288-46f3-b607-6 5.8K |
| SRC_SHA256 | who | 1 | 0 | 6dc0d12120977c4474b745cf1 5.8K |
