# PORTAL_CKA_ANALYZE_BOSTON_4A5CA3BCE5

rows 301  columns 20  scan 3.4s

roles: amount 2, audit 2, category 4, date 2, empty 1, other 4, who 6

## when

ETL_UPDATEDTIMESTAMP
  2026       301  ##############################

INGESTED_AT
  2026       301  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| POINT_X | 253 | -71.17 | -71.07 | -71.01 | -71.01 | -18.0K |
| POINT_Y | 253 | 42.25 | 42.33 | 42.39 | 42.39 | 10.7K |

## who

NEIGHBORHOOD_NAME by rows
        28  Roxbury
        21  Dorchester
        15  Downtown Boston - City Hall Plaza and Pavilion
        14  Downtown Boston - City Hall - Quincy Market
        14  Parks
        10  BCYF-Vines-CC_ Indoor
        10  Strand Theatre - Internal
        10  BCYF-Jackson-Mann-CC_Indoor
         9  Hyde Park
         8  BCYF-Curley-CC_Indoor
         8  BCYF-Tremont
         7  East Boston
         6  YEE Tremont
         6  Bolling
         5  South Boston
         5  BCYF-Mattahunt-CC_Indoor
         5  East Boston Senior Center
         5  Nubian-Bus-Stop
         5  Jamaica Plain
         4  BCYF-Curley_Outdoor

NEIGHBORHOOD_NAME by dollars
      -71.05        1 rows  BCYF-DeepFreeze_test
      -71.06        3 rows  BCYF-Gallivan-CC-Indoor
      -71.06        1 rows  BCYF-Quincy-CC_Indoor
      -71.08       10 rows  BCYF-Vines-CC_ Indoor
      -71.09        1 rows  BCYF-Mildred-CC_Indoor
      -71.10        1 rows  BCYF-Tobin_CC_Outdoor
      -71.11        5 rows  Jamaica Plain
      -71.15        1 rows  BCYF-Roche-CC_Indoor
     -142.08        2 rows  BCYF-Paris-St-Pool_CC_Indoor
     -142.08        5 rows  South Boston
     -142.12        3 rows  200-Frontage-RD-TEMPO-APs
     -142.12        2 rows  Downtown City Hall Pavilion_Indoor
     -142.12        2 rows  BCYF-Leahy-Holloran-CC_Indoor
     -142.12        2 rows  BCYF-Charlestown-CC_Indoor
     -142.14        2 rows  BCYF-Mason-Pool-CC_Indoor
     -142.15        6 rows  Bolling
     -142.16        2 rows  OPAT
     -142.17        2 rows  BCYF-Tobin_CC_Indoor
     -142.18        2 rows  Mattapan-Bus-stop
     -142.24        2 rows  BCYF-Flaherty-Pool-CC_Indoor

DEVICE_LONG by rows
        25  -71.058270909000001
        14  -71.098239898000003
        12  -71.035149919000006
        10  -71.065961410000000
        10  -71.137700383999999
         7  -71.067527405000007
         6  -71.093159400000005
         6  -71.090162401000001
         6  -71.083664403000000
         5  -71.061069907000004
         5  -71.121081895000003
         5  -71.103909899000001
         5  -71.076707404999993
         5  -71.005970000000005
         4  -71.166729879000002
         4  -71.101394399000000
         3  -71.077908905000001
         3  -71.010818423000003
         3  -71.067581408999999
         3  -71.159574882000001

DEVICE_LONG by dollars
      -71.03        1 rows  -71.030199920000001
      -71.05        1 rows  -71.054069999999996
      -71.05        1 rows  -71.054028868675246
      -71.05        1 rows  -71.053272485733046
      -71.05        1 rows  -71.053288578987136
      -71.05        1 rows  -71.054061055183425
      -71.05        1 rows  -71.053267121315017
      -71.06        1 rows  -71.061771911999998
      -71.06        1 rows  -71.063443422317519
      -71.06        1 rows  -71.055750846862807
      -71.06        1 rows  -71.064921908000002
      -71.06        1 rows  -71.063808202743544
      -71.06        1 rows  -71.063936948776259
      -71.06        1 rows  -71.061038406999998
      -71.06        1 rows  -71.064089999999993
      -71.06        1 rows  -71.059260913000003
      -71.06        1 rows  -71.055804491043105
      -71.06        1 rows  -71.063969135284438
      -71.07        1 rows  -71.065535545349135
      -71.07        1 rows  -71.066919565200820

DEVICE_LAT by rows
        25  42.360291326999999
        14  42.332229333000001
        12  42.329115332000001
        10  42.315948335000002
        10  42.352047331000001
         7  42.381864323000002
         6  42.330141333000000
         6  42.322428334999998
         6  42.334470332999999
         5  42.326802334000000
         5  42.380109322999999
         5  42.256296347999999
         5  42.275826344000002
         5  42.386080000000000
         4  42.270768347000001
         4  42.292440341000002
         3  42.260022349000003
         3  42.308829338000002
         3  42.349077330999997
         3  42.330267333000002

DEVICE_LAT by dollars
      -71.03        1 rows  42.332112330999998
      -71.05        1 rows  42.373779683456029
      -71.05        1 rows  42.358159999999998
      -71.05        1 rows  42.373684570469855
      -71.05        1 rows  42.373720237856546
      -71.05        1 rows  42.360153280620700
      -71.05        1 rows  42.360319764108517
      -71.06        1 rows  42.355340924400998
      -71.06        1 rows  42.300792338000001
      -71.06        1 rows  42.381680000000003
      -71.06        1 rows  42.360022471856553
      -71.06        1 rows  42.360169136209969
      -71.06        1 rows  42.347970328999999
      -71.06        1 rows  42.297966338000002
      -71.06        1 rows  42.380838322999999
      -71.06        1 rows  42.355539134157915
      -71.06        1 rows  42.355443993552619
      -71.07        1 rows  42.355872125142234
      -71.07        1 rows  42.352938572443840
      -71.07        1 rows  42.299766337999998

DEVICE_ADDRESS by rows
        12  1663 Columbia Rd, Boston, MA 02127
        11  1483 Tremont St Boston, MA
        10  40 Armington St, Allston, MA 02134
        10  Boston Common
         7  1 City Hall Plaza, Pavilion
Boston, MA  02201
         7  543 Columbia Rd, Boston, MA 02125
         7  345 Bunker Hill St, Boston, MA 02129
         6  68 Annunciation Rd, Mission Hill, MA 02120
         5  One City Hall Sq  Boston MA 02201
         5  100 Hebron St, Mattapan, MA 02126
         5  1 City Hall Square, Boston, MA 02201
         5  2300 Washington Roxbury
         5  18 Barnes Avenue, East Boston, MA 02128
         4  339 Dudley St, Roxbury
         4  Faneuil Hall Marketplace
Boston MA 02201
         4  430A Canterbury Street, Roslindale, MA 02131
         4  2730 Washington St., Boston, MA 02119
         4  131 Dale St, Boston, MA 02119
         4  1179 River St, Hyde Park, MA 02136
         3  25 Warren St, Brighton, MA 02135

DEVICE_ADDRESS by dollars
      -71.03        1 rows  745 E 7th St, South Boston, MA 02127
      -71.05        1 rows  navy yard cambridge
      -71.05        1 rows  1 worrell st Dorchester, ma Basketball Court
      -71.05        1 rows  1 worrell st Dorchester, ma
      -71.05        1 rows  One Worrell St., Dorchester, MA -  inside admin office
      -71.06        1 rows  One City Hall Sq, Pavilion Bld, IWF Room,
Boston, MA 02201
      -71.06        1 rows  One City Hall Sq
Boston MA 02201
      -71.06        1 rows  BPS-Quincy_Elem_232, 885 Washington Street, Boston, MA 02111
      -71.06        1 rows  11 Charles St, Dorchester
      -71.06        1 rows  One City Hall Sq.  Boston MA 02201
      -71.06        1 rows  One City Hall Sq Boston MA 02201
      -71.06        1 rows  40 Gibson st, Dorchester, ma
      -71.06        1 rows  255 Medford St, Charlestown, MA 02129 (Charlestown Community
      -71.07        1 rows  543 Columbia Road
Boston, MA 02125
      -71.07        1 rows  35 Westville St., Dorchester, MA
      -71.07        1 rows  500 Columbia Rd., Dorchester, MA

BPL-Uphams-Corner
10.255.2
      -71.08        1 rows  35 Brookford St., Roxbury, MA
      -71.08        1 rows  174 Dudley St., Roxbury, MA - Rear Roof Facing Palmer Street
      -71.08        1 rows  174 Dudley St., Roxbury, MA - Accross from Engine 14
      -71.08        1 rows  Devon & Columbia Rd, Dorchester, MA

## who x when

NEIGHBORHOOD_NAME by ETL_UPDATEDTIMESTAMP, dollars = POINT_X
  200-Frontage-RD-TEMPO-APs                 2026:-142.12
  BCYF-Curley-CC_Indoor                     2026:-568.32
  BCYF-Curley_Outdoor                       2026:-284.16
  BCYF-DeepFreeze_test                      2026:-71.05
  BCYF-Gallivan-CC-Indoor                   2026:-71.06
  BCYF-Jackson-Mann-CC_Indoor               2026:-711.40
  BCYF-Leahy-Holloran-CC_Indoor             2026:-142.12
  BCYF-Mattahunt-CC_Indoor                  2026:-355.50
  BCYF-Mildred-CC_Indoor                    2026:-71.09
  BCYF-Paris-St-Pool_CC_Indoor              2026:-142.08
  BCYF-Quincy-CC_Indoor                     2026:-71.06
  BCYF-Roche-CC_Indoor                      2026:-71.15
  BCYF-Tobin_CC_Outdoor                     2026:-71.10
  BCYF-Tremont                              2026:-426.60
  BCYF-Vines-CC_ Indoor                     2026:-71.08
  Bolling                                   2026:-142.15
  Dorchester                                2026:-1.5K
  Downtown Boston - City Hall - Quincy Mar  2026:-994.82
  Downtown Boston - City Hall Plaza and Pa  2026:-1.1K
  Downtown City Hall Pavilion_Indoor        2026:-142.12
  East Boston                               2026:-284.16
  East Boston Senior Center                 2026:-355.05
  Hyde Park                                 2026:-640.03
  Jamaica Plain                             2026:-71.11
  Nubian-Bus-Stop                           2026:-355.40
  Parks                                     2026:-852.90
  Roxbury                                   2026:-2.0K
  South Boston                              2026:-142.08
  Strand Theatre - Internal                 2026:-497.49
  YEE Tremont                               2026:-426.60

DEVICE_LONG by ETL_UPDATEDTIMESTAMP, dollars = POINT_X
  -71.005970000000005                       2026:-355.05
  -71.010818423000003                       2026:-213.03
  -71.030199920000001                       2026:-71.03
  -71.035149919000006                       2026:-852.48
  -71.053267121315017                       2026:-71.05
  -71.053272485733046                       2026:-71.05
  -71.053288578987136                       2026:-71.05
  -71.054028868675246                       2026:-71.05
  -71.054061055183425                       2026:-71.05
  -71.054069999999996                       2026:-71.05
  -71.055750846862807                       2026:-71.06
  -71.058270909000001                       2026:-1.8K
  -71.061069907000004                       2026:-355.30
  -71.061771911999998                       2026:-71.06
  -71.063443422317519                       2026:-71.06
  -71.065961410000000                       2026:-710.70
  -71.067527405000007                       2026:-497.49
  -71.067581408999999                       2026:-213.21
  -71.076707404999993                       2026:-355.40
  -71.077908905000001                       2026:-213.24
  -71.083664403000000                       2026:-426.48
  -71.090162401000001                       2026:-426.54
  -71.093159400000005                       2026:-426.54
  -71.098239898000003                       2026:-995.40
  -71.101394399000000                       2026:-284.40
  -71.103909899000001                       2026:-355.50
  -71.121081895000003                       2026:-355.60
  -71.137700383999999                       2026:-711.40
  -71.159574882000001                       2026:-213.48
  -71.166729879000002                       2026:-284.68

## what

DEVICE_TAGS: {} 49%, {recently-added} 15%, {employee} 13%, {City-Hall} 5%, {employee,recently-added} 4%, {bcyf,cob-employee} 3%, {BCYF,Inside,UXI,employee} 3%, {Inside} 2%, {Outside} 2%, {Inside,employee} 2%, {BPL,Outside,Uphams-Corner-Bra 1%, {BPS,Outside} 1%

ORG1: BCYF 62%, BPL 17%, BPS 17%, DYEE 4%

INSIDE_OUTSIDE: Inside 65%, Outside 35%

LANDMARK: employee 54%, City Hall 14%, cob employee 9%, UXI employee 8%, Uphams Corner Branch 4%, CoB Employee 4%, bcfy employee 3%, City Hall employee 3%, Curtis Jamaica Plain 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NEIGHBORHOOD_ID | other | 63 | 0 | N_579275502070532581 28; N_568579452955534204 21; N_601230550253966673 15; N_568579452955527921 14 |
| NEIGHBORHOOD_NAME | who | 63 | 0 | Roxbury 28; Dorchester 21; Downtown Boston - City Ha 15; Parks 14 |
| DEVICE_SERIAL | other | 305 | 0 | Q3AK-CQWK-ZYPY 2; Q3AK-CVAW-H5UM 2; Q3KG-VR8G-WJJ6 2; Q3AK-DCRG-BFEQ 2 |
| DEVICE_CONNECTEDTO | other | 296 | 4 | PARKS-COMMON-AP8 2; PARKS-COMMON-AP9 2; PARKS-FRANKLIN_CLUBHOUSE- 2; ROX-EMERSON-MR76 AP2 2 |
| DEVICE_ADDRESS | who | 105 | 53 | 1663 Columbia Rd, Boston, 12; 1483 Tremont St Boston, M 11; Boston Common 10; 40 Armington St, Allston, 10 |
| DEVICE_LAT | who | 89 | 48 | 42.360291326999999 25; 42.332229333000001 14; 42.329115332000001 12; 42.315948335000002 10 |
| DEVICE_LONG | who | 91 | 48 | -71.058270909000001 25; -71.098239898000003 14; -71.035149919000006 12; -71.065961410000000 10 |
| DEVICE_TAGS | category | 23 | 0 | {} 137; {recently-added} 41; {employee} 37; {City-Hall} 14 |
| ETL_UPDATEDTIMESTAMP | date | 44 | 0 | 6/19/2026 2:31:40.000 35; 6/19/2026 2:31:44.000 28; 6/19/2026 2:31:53.000 17; 6/19/2026 2:31:54.000 15 |
| IS_CURRENT | other | 1 | 0 | 1 301 |
| ORG1 | category | 5 | 277 | BCYF 15; BPL 4; BPS 4; DYEE 1 |
| ORG2 | empty | 1 | 301 |  |
| INSIDE_OUTSIDE | category | 3 | 264 | Inside 24; Outside 13 |
| LANDMARK | category | 10 | 201 | employee 54; City Hall 14; cob employee 9; UXI employee 8 |
| SHAPE_WKT | who | 90 | 48 | POINT (-71.05827090899998 25; POINT (-71.09823989799997 14; POINT (-71.03514991899993 12; POINT (-71.06596140999994 10 |
| POINT_X | amount | 91 | 48 | -71.058270908999987 25; -71.098239897999974 14; -71.035149918999934 12; -71.065961409999943 10 |
| POINT_Y | amount | 90 | 48 | 42.360291327000027 25; 42.332229333000043 14; 42.329115332000072 12; 42.315948335000030 10 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:38:59.74869 301 |
| SOURCE_RUN_ID | audit | 1 | 0 | 861200ed-8afa-4e13-82d3-7 301 |
| SRC_SHA256 | who | 1 | 0 | fb3ff37ed6340ad959beb31c2 301 |
