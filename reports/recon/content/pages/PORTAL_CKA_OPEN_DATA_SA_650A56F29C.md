# PORTAL_CKA_OPEN_DATA_SA_650A56F29C

rows 156  columns 9  scan 3.4s

roles: amount 2, audit 2, date 1, other 3, who 2

## when

INGESTED_AT
  2026       156  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 156 | 2.07M | 2.13M | 2.19M | 2.21M | 331.39M |
| Y | 156 | 13.64M | 13.73M | 13.76M | 13.77M | 2.14B |

## who

NAME by rows
         1  Oak Knoll 500 ft E of E Horseshoe Bend
         1  Jung Rd at Mud Creek Tributary A
         1  White Bonnet S of Lockhill
         1  Vance Jackson S of Treehill
         1  Mission Parkway at San Antonio River
         1  E Horseshoe Bend and Oakwood
         1  Blue Wing Rd between IH 37 and Mickey Rd
         1  S Hausman Rd 3300 ft N of Prue Rd
         1  Rice Rd at Salado Creek
         1  Dreamland at RR Crossing
         1  Ledgestone at Mount Joy
         1  Tallahasse
         1  Old Camp Bullis Road at Leon Creek
         1  W Quill Dr at Heather Hill
         1  Ray Ellison 300' N of Medina Base
         1  Verbena 1000 ft W of Southwell
         1  N Graytown Rd at Tributary C to Salitrillo Creek
         1  Sleepy Hollow at Sunburst
         1  Southton Rd 4700 ft W of IH-37
         1  Harness Lane 480 ft N of Marbach Rd

NAME by dollars
       2.21M        1 rows  Pfeil Rd at Bluebell Ridge
       2.19M        1 rows  N Graytown Rd at Tributary C to Salitrillo Creek
       2.19M        1 rows  New Sulphur Springs E of Beck
       2.18M        1 rows  New Sulphur Springs
       2.17M        1 rows  Lookout Rd 200 ft SW of Topperwein
       2.17M        1 rows  New Sulphur Springs N of Lodi
       2.17M        1 rows  Judson Rd 100 ft SE of Lookout Rd
       2.17M        1 rows  Judson Rd at Lookout Rd
       2.17M        1 rows  Gibbs Sprawl 800 ft NE of Castle Cross
       2.17M        1 rows  New Sulphur Springs E of Jasper
       2.17M        1 rows  Gibbs Sprawl at Rosillo Creek
       2.17M        1 rows  Old OConnor N of Lookout Rd
       2.16M        1 rows  Weidner 500 ft N of Schertz
       2.16M        1 rows  Weidner S of Leonhardt
       2.16M        1 rows  New Sulphur Springs at Rosillo Creek
       2.16M        1 rows  Leonhardt 500 ft S of Encante
       2.16M        1 rows  WW White at Rosillo Creek
       2.16M        1 rows  Southton Rd 2000 ft W of IH-37
       2.16M        1 rows  Classen Rd 800 feet NW of Stahl Rd
       2.16M        1 rows  Briarmall at Briarcrest Dr

SRC_SHA256 by rows
       156  78687dd2e9805f487a3f9306493b9187a59d5ea6bc476453f51c8b3cdb1d2ed8

SRC_SHA256 by dollars
     331.39M      156 rows  78687dd2e9805f487a3f9306493b9187a59d5ea6bc476453f51c8b3cdb1d

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  Blue Wing Rd between IH 37 and Mickey Rd  2026:2.16M
  Dreamland at RR Crossing                  2026:2.11M
  E Horseshoe Bend and Oakwood              2026:2.10M
  Gibbs Sprawl 800 ft NE of Castle Cross    2026:2.17M
  Gibbs Sprawl at Rosillo Creek             2026:2.17M
  Harness Lane 480 ft N of Marbach Rd       2026:2.08M
  Judson Rd 100 ft SE of Lookout Rd         2026:2.17M
  Judson Rd at Lookout Rd                   2026:2.17M
  Jung Rd at Mud Creek Tributary A          2026:2.15M
  Ledgestone at Mount Joy                   2026:2.14M
  Lookout Rd 200 ft SW of Topperwein        2026:2.17M
  Mission Parkway at San Antonio River      2026:2.14M
  N Graytown Rd at Tributary C to Salitril  2026:2.19M
  New Sulphur Springs                       2026:2.18M
  New Sulphur Springs E of Beck             2026:2.19M
  New Sulphur Springs E of Jasper           2026:2.17M
  New Sulphur Springs N of Lodi             2026:2.17M
  Oak Knoll 500 ft E of E Horseshoe Bend    2026:2.10M
  Old Camp Bullis Road at Leon Creek        2026:2.10M
  Pfeil Rd at Bluebell Ridge                2026:2.21M
  Ray Ellison 300' N of Medina Base         2026:2.08M
  Rice Rd at Salado Creek                   2026:2.15M
  S Hausman Rd 3300 ft N of Prue Rd         2026:2.08M
  Sleepy Hollow at Sunburst                 2026:2.11M
  Southton Rd 4700 ft W of IH-37            2026:2.16M
  Tallahasse                                2026:2.09M
  Vance Jackson S of Treehill               2026:2.11M
  Verbena 1000 ft W of Southwell            2026:2.10M
  W Quill Dr at Heather Hill                2026:2.10M
  White Bonnet S of Lockhill                2026:2.09M

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  78687dd2e9805f487a3f9306493b9187a59d5ea6  2026:331.39M

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 156 | 0 | 156 1; 155 1; 154 1; 153 1 |
| NAME | who | 157 | 0 | West Ave at W North Loop  1; Stahl Rd N of Bell 1; Leonhardt 500 ft S of Enc 1; Nacogdoches Rd at Bulverd 1 |
| CARTID | other | 157 | 0 | LWC_7070149 1; LWC_7070125 1; LWC_7070179 1; LWC_7070176 1 |
| GLOBALID | other | 157 | 0 | b915d64b-a113-4b3b-af8e-f 1; ea6e6355-ff4a-4835-bc28-c 1; 6d9862bd-2a85-4ddc-ac14-c 1; 8ea950d8-ad31-485a-9f02-2 1 |
| X | amount | 158 | 0 | 2127393.98817846 1; 2156103.57839698 1; 2161934.10709022 1; 2153477.84611563 1 |
| Y | amount | 155 | 0 | 13749604.4022081 1; 13755519.5166901 1; 13747290.5643161 1; 13745652.0265826 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:16:44.38459 156 |
| SOURCE_RUN_ID | audit | 1 | 0 | c116c409-4eed-40a6-a09e-1 156 |
| SRC_SHA256 | who | 1 | 0 | 78687dd2e9805f487a3f93064 156 |
