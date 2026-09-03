# FED_MSHA_ACCIDENTS

rows 273.6K  columns 60  scan 4.6s

roles: audit 2, category 25, date 1, id 3, other 18, who 12

## when

_INGESTED_AT
  2026    273.6K  ##############################

## who

OPERATOR_NAME by rows
      3.1K  "Consolidation Coal Company"
      2.9K  "Freeport-McMoRan Morenci Inc."
      2.3K  "Vulcan Construction Materials, LLC"
      2.3K  "Jim Walter Resources Inc"
      2.0K  "Peabody Midwest Mining, LLC"
      2.0K  "Newmont USA Limited"
      1.9K  "Stillwater Mining Company"
      1.9K  "Consol Pennsylvania Coal Company LLC"
      1.8K  "Illnois Land Resources, Inc."
      1.8K  "Rosebud Mining Company"
      1.5K  "Eastern Associated Coal LLC"
      1.4K  "Drummond Company Inc"
      1.3K  "Ash Grove Cement Company"
      1.2K  "Buzzi Unicem USA"
      1.2K  "Consol Pennsylvania Coal Company"
      1.2K  "Emerald Coal Resources LP"
      1.1K  "Webster County Coal LLC"
      1.1K  "Marfork Coal Company, LLC"
      1.0K  "United States Steel Corp-Minnesota Ore Operations"
      1.0K  "Heidelberg Materials US Cement LLC"

CONTROLLER_NAME by rows
      8.2K  "Alliance Resource Partners LP"
      7.8K  "Robert E  Murray"
      7.5K  "CONSOL Energy Inc"
      7.1K  "Peabody Energy Corporation"
      6.8K  "Alpha Natural Resources, Inc."
      6.5K  "Massey Energy Company"
      5.2K  "Freeport-McMoRan Inc"
      3.4K  "Heidelberg Materials AG"
      3.1K  "Arch Resources Inc"
      3.0K  "CRH PLC"
      2.8K  "Martin Marietta Materials Inc"
      2.7K  "Cemex S A"
      2.6K  "James River Coal Company"
      2.4K  "Walter Energy Incorporated"
      2.3K  "Patriot Coal Corporation"
      2.2K  "Holcim Ltd"
      2.2K  "ACNR Holdings, Inc"
      2.2K  "Newmont Corporation"
      2.0K  "Buzzi S p A"
      1.9K  "Lafarge S A"

EQUIP_MFR_NAME by rows
    151.1K  "NO VALUE FOUND"
     57.0K  "Not Reported"
     16.7K  "Not on this list"
     14.5K  "Caterpillar"
      4.9K  "Fletcher"
      4.6K  "Not listed"
      2.8K  "Joy"
      2.0K  "Komatsu"
      1.2K  "Nordberb&Rexnord"
      1.2K  "Joy Machinery Co. (Joy, Joy Manufacturing Co.)"
       977  "Mack"
       900  "Unknown"
       845  "Ford"
       680  "Long-Airdox"
       595  "Ingersol-Rand"
       567  "Eimco"
       494  "Fairchild"
       424  "Cedar Rapids"
       421  "S & S"
       381  "Bucyrus-Erie"

ACCIDENT_DT by rows
        96  "07/24/2000"
        93  "09/10/2001"
        93  "09/05/2000"
        92  "08/16/2000"
        91  "07/17/2000"
        91  "08/08/2001"
        91  "06/26/2000"
        90  "08/23/2001"
        90  "09/18/2000"
        89  "08/01/2001"
        89  "09/14/2000"
        89  "05/15/2000"
        88  "01/21/2002"
        88  "07/31/2000"
        88  "04/16/2002"
        87  "08/22/2000"
        87  "05/21/2007"
        86  "10/03/2000"
        86  "08/13/2001"
        85  "09/04/2001"

## who x when

OPERATOR_NAME by _INGESTED_AT  LOAD STAMP, not an event date
  "Ash Grove Cement Company"                2026:1.3K
  "Buzzi Unicem USA"                        2026:1.2K
  "Consol Pennsylvania Coal Company LLC"    2026:1.9K
  "Consol Pennsylvania Coal Company"        2026:1.2K
  "Consolidation Coal Company"              2026:3.1K
  "Drummond Company Inc"                    2026:1.4K
  "Eastern Associated Coal LLC"             2026:1.5K
  "Emerald Coal Resources LP"               2026:1.2K
  "Freeport-McMoRan Morenci Inc."           2026:2.9K
  "Heidelberg Materials US Cement LLC"      2026:1.0K
  "Illnois Land Resources, Inc."            2026:1.8K
  "Jim Walter Resources Inc"                2026:2.3K
  "Marfork Coal Company, LLC"               2026:1.1K
  "Newmont USA Limited"                     2026:2.0K
  "Peabody Midwest Mining, LLC"             2026:2.0K
  "Rosebud Mining Company"                  2026:1.8K
  "Stillwater Mining Company"               2026:1.9K
  "United States Steel Corp-Minnesota Ore   2026:1.0K
  "Vulcan Construction Materials, LLC"      2026:2.3K
  "Webster County Coal LLC"                 2026:1.1K

CONTROLLER_NAME by _INGESTED_AT  LOAD STAMP, not an event date
  "ACNR Holdings, Inc"                      2026:2.2K
  "Alliance Resource Partners LP"           2026:8.2K
  "Alpha Natural Resources, Inc."           2026:6.8K
  "Arch Resources Inc"                      2026:3.1K
  "Buzzi S p A"                             2026:2.0K
  "CONSOL Energy Inc"                       2026:7.5K
  "CRH PLC"                                 2026:3.0K
  "Cemex S A"                               2026:2.7K
  "Freeport-McMoRan Inc"                    2026:5.2K
  "Heidelberg Materials AG"                 2026:3.4K
  "Holcim Ltd"                              2026:2.2K
  "James River Coal Company"                2026:2.6K
  "Lafarge S A"                             2026:1.9K
  "Martin Marietta Materials Inc"           2026:2.8K
  "Massey Energy Company"                   2026:6.5K
  "Newmont Corporation"                     2026:2.2K
  "Patriot Coal Corporation"                2026:2.3K
  "Peabody Energy Corporation"              2026:7.1K
  "Robert E  Murray"                        2026:7.8K
  "Walter Energy Incorporated"              2026:2.4K

## what

SUBUNIT_CD: "01" 39%, "03" 30%, "30" 25%, "02" 4%, "06" 1%, "99" 1%, "17" 0%, "04" 0%, "12" 0%, "05" 0%

SUBUNIT: "UNDERGROUND" 39%, "STRIP, QUARY, OPEN PIT" 30%, "MILL OPERATION/PREPARATION PL 25%, "SURFACE AT UNDERGROUND" 4%, "DREDGE" 1%, "OFFICE WORKERS AT MINE SITE" 1%, "INDEPENDENT SHOPS OR YARDS" 0%, "AUGER" 0%, "OTHER MINING" 0%, "CULM BANK/REFUSE PILE" 0%

CAL_YR: 2000 11%, 2001 10%, 2002 9%, 2005 9%, 2004 8%, 2006 8%, 2003 8%, 2007 8%, 2008 8%, 2011 6%, 2009 6%, 2010 6%

CAL_QTR: 3 27%, 2 26%, 1 25%, 4 22%

FISCAL_YR: 2001 11%, 2002 10%, 2003 9%, 2005 9%, 2006 9%, 2000 9%, 2007 9%, 2004 9%, 2008 8%, 2009 7%, 2011 7%, 2010 6%

FISCAL_QTR: 4 27%, 3 26%, 2 25%, 1 22%

DEGREE_INJURY_CD: "03" 32%, "06" 26%, "05" 16%, "00" 11%, "04" 8%, "07" 4%, "02" 1%, "10" 1%, "08" 1%, "01" 0%, "?" 0%, "09" 0%

DEGREE_INJURY: "DAYS AWAY FROM WORK ONLY" 32%, "NO DYS AWY FRM WRK,NO RSTR AC 26%, "DAYS RESTRICTED ACTIVITY ONLY 16%, "ACCIDENT ONLY" 11%, "DYS AWY FRM WRK & RESTRCTD AC 8%, "OCCUPATNAL ILLNESS NOT DEG 1- 4%, "PERM TOT OR PERM PRTL DISABLT 1%, "ALL OTHER CASES (INCL 1ST AID 1%, "INJURIES DUE TO NATURAL CAUSE 1%, "FATALITY" 0%, "NO VALUE FOUND" 0%, "INJURIES INVOLVNG NONEMPLOYEE 0%

UG_LOCATION_CD: "?" 61%, "03" 12%, "06" 12%, "04" 7%, "98" 3%, "01" 2%, "99" 1%, "02" 1%, "05" 1%

UG_LOCATION: "NO VALUE FOUND" 61%, "FACE" 12%, "LAST OPEN CROSSCUT" 12%, "INTERSECTION" 7%, "OTHER" 3%, "VERTICAL SHAFT" 2%, "NOT MARKED" 1%, "SLOPE/INCLINED SHAFT" 1%, "UNDERGROUND SHOP/OFFICE" 1%

UG_MINING_METHOD_CD: "?" 65%, "05" 24%, "01" 5%, "03" 3%, "08" 2%, "06" 0%, "07" 0%, "02" 0%

UG_MINING_METHOD: "NO VALUE FOUND" 65%, "Continuous Mining" 24%, "Longwall" 5%, "Conventional Stoping" 3%, "Other" 2%, "Hand" 0%, "Caving" 0%, "Shortwall" 0%

CLASSIFICATION_CD: "09" 31%, "18" 18%, "10" 11%, "17" 11%, "07" 11%, "12" 8%, "21" 3%, "31" 2%, "13" 2%, "19" 1%, "20" 1%, "06" 1%

CLASSIFICATION: "HANDLING OF MATERIALS" 31%, "SLIP OR FALL OF PERSON" 18%, "HANDTOOLS (NONPOWERED)" 11%, "MACHINERY" 11%, "FALL OF ROOF OR BACK" 11%, "POWERED HAULAGE" 8%, "OTHER" 3%, "DISORDERS (REPEATED TRAUMA)" 2%, "HOISTING" 2%, "STEPPING OR KNEELING ON OBJEC 1%, "STRIKING OR BUMPING" 1%, "FALL OF FACE/RIB/PILLAR/SIDE/ 1%

ACCIDENT_TYPE_CD: "30" 15%, "08" 14%, "44" 14%, "04" 11%, "27" 8%, "21" 8%, "01" 7%, "17" 6%, "02" 5%, "05" 5%, "24" 4%, "18" 4%

ACCIDENT_TYPE: "Over-exertion NEC" 15%, "Struck by... NEC" 14%, "Accident type, without injuri 14%, "Struck by falling object" 11%, "Over-exertion in lifting obje 8%, "Caught in, under or between a 8%, "Struck against stationary obj 7%, "Fall to the walkway or workin 6%, "Struck against a moving objec 5%, "Struck by flying object" 5%, "Caught in, under or between N 4%, "Fall onto or against objects" 4%

NO_INJURIES: "1" 88%, "0" 11%, "2" 1%, "3" 0%, "4" 0%, "6" 0%, "5" 0%, "9" 0%, "36" 0%, "7" 0%, "10" 0%, "16" 0%

NATURE_INJURY_CD: "330" 30%, "180" 21%, "220" 14%, "?" 13%, "160" 7%, "400" 4%, "370" 3%, "270" 2%, "170" 2%, "120" 1%, "130" 1%, "320" 1%

NATURE_INJURY: "SPRAIN,STRAIN RUPT DISC" 30%, "CUT,LACER,PUNCT-OPN WOUND" 21%, "FRACTURE,CHIP" 14%, "NO VALUE FOUND" 13%, "CONTUSN,BRUISE,INTAC SKIN" 7%, "UNCLASSIFIED,NOT DETERMED" 4%, "MULTIPLE INJURIES" 3%, "JOINT,TENDON,MUSCL INFLAM" 2%, "CRUSHING" 2%, "BURN OR SCALD (HEAT)" 1%, "BURN,CHEMICL-FUME,COMPOUN" 1%, "DUST IN EYES" 1%

INJ_BODY_PART_CD: "340" 19%, "?" 16%, "420" 15%, "512" 9%, "450" 7%, "700" 6%, "330" 6%, "130" 6%, "520" 5%, "320" 4%, "530" 3%, "430" 3%

INJ_BODY_PART: "FINGER(S)/THUMB" 19%, "NO VALUE FOUND" 16%, "BACK (MUSCLES/SPINE/S-CORD/TA 15%, "KNEE/PATELLA" 9%, "SHOULDERS (COLLARBONE/CLAVICL 7%, "MULTIPLE PARTS (MORE THAN ONE 6%, "HAND (NOT WRIST OR FINGERS)" 6%, "EYE(S) OPTIC NERVE/VISON" 6%, "ANKLE" 5%, "WRIST" 4%, "FOOT(NOT ANKLE/TOE)/TARSUS/ME 3%, "CHEST (RIBS/BREAST BONE/CHEST 3%

TRANS_TERM: "N" 95%, "Y" 5%

IMMED_NOTIFY_CD: "? " 66%, "13" 20%, "08" 6%, "02" 3%, "11" 2%, "06" 1%, "01" 0%, "05" 0%, "03" 0%, "04" 0%, "12" 0%, "09" 0%

IMMED_NOTIFY: "NO VALUE FOUND" 66%, "NOT MARKED" 20%, "ROOF FALL" 6%, "SERIOUS INJURY" 3%, "HOISTING" 2%, "MINE FIRE" 1%, "DEATH" 0%, "GAS OF DUST IGNITION" 0%, "ENTRAPMENT" 0%, "INNUMDATION" 0%, "OFFSITE INJURY" 0%, "OUTBURST" 0%

COAL_METAL_IND: "M" 53%, "C" 47%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| MINE_ID | other | 13.4K | 0 | "0200024" 2.9K; "4601437" 2.3K; "1102752" 1.8K; "3607230" 1.6K |
| CONTROLLER_ID | other | 6.7K | 721 | "C15455" 8.2K; "C13408" 7.8K; "C00692" 7.5K; "C15833" 7.1K |
| CONTROLLER_NAME | who | 6.7K | 721 | "Alliance Resource Partne 8.2K; "Robert E  Murray" 7.8K; "CONSOL Energy Inc" 7.5K; "Peabody Energy Corporati 7.1K |
| OPERATOR_ID | other | 8.0K | 721 | "P00812" 3.2K; "L12058" 2.9K; "L16168" 2.5K; "P01155" 2.3K |
| OPERATOR_NAME | who | 10.3K | 721 | "Consolidation Coal Compa 3.2K; "Freeport-McMoRan Morenci 2.9K; "Jim Walter Resources Inc 2.3K; "Vulcan Construction Mate 2.3K |
| CONTRACTOR_ID | who | 5.3K | 245.2K | "MVK" 711; "E24" 324; "B96" 315; "A01" 312 |
| DOCUMENT_NO | id | 277.0K | 0 | "220222690012" 329; "220260070015" 329; "220240390009" 329; "220070470041" 329 |
| SUBUNIT_CD | category | 10 | 0 | "01" 106.8K; "03" 81.6K; "30" 67.5K; "02" 10.6K |
| SUBUNIT | category | 10 | 0 | "UNDERGROUND" 106.8K; "STRIP, QUARY, OPEN PIT" 81.6K; "MILL OPERATION/PREPARATI 67.5K; "SURFACE AT UNDERGROUND" 10.6K |
| ACCIDENT_DT | who | 9.6K | 0 | "01/24/2000" 657; "06/24/2003" 546; "07/10/2001" 544; "07/03/2001" 544 |
| CAL_YR | category | 27 | 0 | 2000 18.7K; 2001 17.6K; 2002 16.0K; 2005 14.8K |
| CAL_QTR | category | 4 | 0 | 3 74.2K; 2 70.0K; 1 68.9K; 4 60.4K |
| FISCAL_YR | category | 27 | 0 | 2001 17.8K; 2002 16.5K; 2003 14.8K; 2005 14.7K |
| FISCAL_QTR | category | 4 | 0 | 4 74.2K; 3 70.0K; 2 68.9K; 1 60.4K |
| ACCIDENT_TIME | who | 1.4K | 1 | "9999" 20.1K; "1000" 9.3K; "1100" 7.6K; "0900" 7.0K |
| DEGREE_INJURY_CD | category | 12 | 0 | "03" 88.7K; "06" 71.3K; "05" 43.3K; "00" 30.4K |
| DEGREE_INJURY | category | 12 | 0 | "DAYS AWAY FROM WORK ONLY 88.7K; "NO DYS AWY FRM WRK,NO RS 71.3K; "DAYS RESTRICTED ACTIVITY 43.3K; "ACCIDENT ONLY" 30.4K |
| FIPS_STATE_CD | other | 54 | 0 | "54" 41.8K; "21" 28.8K; "42" 20.4K; "17" 12.7K |
| UG_LOCATION_CD | category | 9 | 0 | "?" 166.9K; "03" 32.3K; "06" 31.5K; "04" 19.7K |
| UG_LOCATION | category | 8 | 0 | "NO VALUE FOUND" 166.9K; "FACE" 32.3K; "LAST OPEN CROSSCUT" 31.5K; "INTERSECTION" 19.7K |
| UG_MINING_METHOD_CD | category | 8 | 0 | "?" 178.9K; "05" 66.8K; "01" 13.6K; "03" 7.1K |
| UG_MINING_METHOD | category | 8 | 0 | "NO VALUE FOUND" 178.9K; "Continuous Mining" 66.8K; "Longwall" 13.6K; "Conventional Stoping" 7.1K |
| MINING_EQUIP_CD | other | 71 | 0 | "?" 151.0K; "28" 28.2K; "54" 8.9K; "44" 8.9K |
| MINING_EQUIP | who | 71 | 0 | "NO VALUE FOUND" 151.0K; "Hand tools (not powered) 28.2K; "Rock or roof bolting mac 8.9K; "Ore haulage trucks - off 8.9K |
| EQUIP_MFR_CD | other | 241 | 0 | "?" 151.1K; "121" 40.8K; "119" 16.7K; "0000" 16.2K |
| EQUIP_MFR_NAME | who | 193 | 0 | "NO VALUE FOUND" 151.1K; "Not Reported" 57.0K; "Not on this list" 16.7K; "Caterpillar" 14.5K |
| EQUIP_MODEL_NO | other | 21.2K | 164.7K | "?" 55.3K; "RRII" 636; "777" 360; "488" 348 |
| SHIFT_BEGIN_TIME | other | 827 | 990 | "0700" 54.6K; "0600" 38.2K; "700" 19.4K; "1500" 15.9K |
| CLASSIFICATION_CD | category | 29 | 0 | "09" 78.6K; "18" 46.7K; "10" 28.8K; "17" 27.9K |
| CLASSIFICATION | category | 29 | 0 | "HANDLING OF MATERIALS" 78.6K; "SLIP OR FALL OF PERSON" 46.7K; "HANDTOOLS (NONPOWERED)" 28.8K; "MACHINERY" 27.9K |
| ACCIDENT_TYPE_CD | category | 45 | 0 | "30" 33.1K; "08" 31.9K; "44" 30.4K; "04" 23.9K |
| ACCIDENT_TYPE | category | 45 | 0 | "Over-exertion NEC" 33.1K; "Struck by... NEC" 31.9K; "Accident type, without i 30.4K; "Struck by falling object 23.9K |
| NO_INJURIES | category | 16 | 0 | "1" 241.0K; "0" 30.5K; "2" 1.4K; "3" 265 |
| TOT_EXPER | other | 3.3K | 44.2K | "2" 5.1K; "5" 4.9K; "10" 4.9K; "3" 4.8K |
| MINE_EXPER | other | 3.2K | 41.3K | "2" 8.1K; "1" 8.0K; "3" 6.4K; "4" 4.7K |
| JOB_EXPER | other | 3.1K | 40.5K | "2" 9.3K; "1" 8.7K; "3" 7.2K; "5" 6.4K |
| OCCUPATION_CD | other | 256 | 0 | "304" 37.0K; "?" 32.2K; "374" 20.3K; "316" 20.2K |
| OCCUPATION | who | 205 | 0 | "Maintenance man, Mechani 44.2K; "NO VALUE FOUND" 32.2K; "Warehouseman, Bagger, Pa 20.3K; "Laborer, Blacksmith, Bul 20.2K |
| ACTIVITY_CD | other | 99 | 0 | "028" 45.9K; "039" 35.6K; "?" 32.6K; "030" 25.8K |
| ACTIVITY | who | 98 | 0 | "Handling supplies or mat 45.9K; "Machine maintenance" 35.6K; "NO VALUE FOUND" 32.6K; "Hand tools (not powered) 25.8K |
| INJURY_SOURCE_CD | other | 128 | 0 | "?" 32.6K; "088" 29.2K; "117" 18.2K; "086" 16.5K |
| INJURY_SOURCE | who | 128 | 0 | "NO VALUE FOUND" 32.6K; "METAL,NEC(PIPE,WIRE,NAIL 29.2K; "GROUND" 18.2K; "METAL COVERS & GUARDS" 16.5K |
| NATURE_INJURY_CD | category | 38 | 0 | "330" 75.9K; "180" 53.0K; "220" 34.8K; "?" 32.8K |
| NATURE_INJURY | category | 39 | 0 | "SPRAIN,STRAIN RUPT DISC" 75.9K; "CUT,LACER,PUNCT-OPN WOUN 53.0K; "FRACTURE,CHIP" 34.8K; "NO VALUE FOUND" 32.8K |
| INJ_BODY_PART_CD | category | 47 | 0 | "340" 40.1K; "?" 32.8K; "420" 31.8K; "512" 18.7K |
| INJ_BODY_PART | category | 46 | 0 | "FINGER(S)/THUMB" 40.1K; "NO VALUE FOUND" 32.8K; "BACK (MUSCLES/SPINE/S-CO 31.8K; "KNEE/PATELLA" 18.7K |
| SCHEDULE_CHARGE | other | 226 | 65.0K | "0" 203.3K; "6000" 2.2K; "50" 700; "100" 322 |
| DAYS_RESTRICT | other | 450 | 62.4K | "0" 145.5K; "5" 4.2K; "2" 3.7K; "3" 3.5K |
| DAYS_LOST | other | 657 | 46.9K | "0" 115.2K; "1" 8.7K; "2" 7.7K; "3" 5.6K |
| TRANS_TERM | category | 3 | 36.8K | "N" 225.1K; "Y" 11.8K |
| RETURN_TO_WORK_DT | who | 9.5K | 43.3K | "05/01/2004" 886; "05/01/2008" 884; "07/29/2002" 599; "04/30/2001" 557 |
| IMMED_NOTIFY_CD | category | 14 | 0 | "? " 181.6K; "13" 55.9K; "08" 17.2K; "02" 8.5K |
| IMMED_NOTIFY | category | 14 | 0 | "NO VALUE FOUND" 181.6K; "NOT MARKED" 55.9K; "ROOF FALL" 17.2K; "SERIOUS INJURY" 8.5K |
| INVEST_BEGIN_DT | who | 8.7K | 218.9K | "10/04/2001" 143; "07/05/2005" 143; "07/23/2009" 109; "02/14/2003" 109 |
| NARRATIVE | id | 270.8K | 2 | "On night shift of Septem 329; "The morning of 1-3-26 @  329; "EE was using excavator t 329; "Attempting to fit contro 329 |
| CLOSED_DOC_NO | id | 122.4K | 152.4K | "320122220016" 147; "320072960007" 147; "320241370005" 147; "320061310019" 147 |
| COAL_METAL_IND | category | 2 | 0 | "M" 145.7K; "C" 127.9K |
| _INGESTED_AT | audit date | 1 | 0 | 2026-07-24 00:47:40.000 273.6K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 045d66ec-6df7-4852-be1b-0 273.6K |
| _SRC_SHA256 | other | 1 | 0 | "c5583eeb3e18dd1:0" 273.6K |
