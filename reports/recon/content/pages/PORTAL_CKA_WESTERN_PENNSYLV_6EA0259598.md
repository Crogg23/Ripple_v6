# PORTAL_CKA_WESTERN_PENNSYLV_6EA0259598

rows 307  columns 11  scan 4.8s

roles: amount 2, audit 2, date 1, other 3, who 4

## when

INGESTED_AT
  2026       307  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 307 | 832.98 | 201.9K | 7.64M | 13.11M | 230.62M |
| SHAPE__LENGTH | 307 | 118.88 | 2.2K | 15.9K | 20.7K | 979.2K |

## who

NAME by rows
         6  ST JOSEPH CEMETERY
         5  ST NICHOLAS CEMETERY
         4  ST MARYS CEMETERY
         3  ST JOHNS LUTHERAN CEMETERY
         2  ST PATRICK CEMETERY
         2  ST MICHAELS CEMETERY
         2  OHAVE ZEDEK CEMETERY
         2  STS PETER & PAUL CEMETERY
         2  CROSSROADS CEMETERY
         2  ST PETERS CEMETERY
         2  ST GEORGE CEMETERY
         2  ST PAULS LUTHERAN CEMETERY
         2  FAIRVIEW CEMETERY
         2  ST JOSEPHS CEMETERY
         2  PINE CREEK CEMETERY
         2  HOLY TRINITY CEMETERY
         2  BETHANY CEMETERY
         2  OLD GERMAN CEMETERY
         1  JEFFERSON MEMORIAL CEMETERY
         1  TURNER CEMETERY

NAME by dollars
      13.11M        1 rows  ALLEGHENY CEMETERY
      13.02M        1 rows  JEFFERSON MEMORIAL CEMETERY
       7.80M        1 rows  GOOD SHEPARD CEMETERY
       7.67M        1 rows  HOMEWOOD CEMETERY
       7.16M        1 rows  CALVARY CEMETERY 
       6.28M        1 rows  GRANDVIEW CEMETERY
       5.91M        4 rows  ST MARYS CEMETERY
       5.04M        1 rows  HOLY SAVIOR CEMETERY
       4.76M        1 rows  OUR LADY OF HOPE CEMETERY
       4.71M        1 rows  ST STANISLAUS AND ST ANTHONY CATHOLIC CEMETERY
       4.51M        1 rows  RESURRECTION CEMETERY
       4.28M        1 rows  UNION DALE CEMETERY
       4.18M        1 rows  ALLEGHENY MEMORIAL CEMETERY
       3.99M        1 rows  RIVERVIEW MEMORIAL PARK
       3.96M        1 rows  RESTLAND MEMORIAL CEMETERY
       3.84M        1 rows  MT ROYAL CEMETERY
       3.82M        1 rows  HIGHWOOD CEMETERY
       3.43M        1 rows  SEWICKLEY CEMETERY
       3.05M        1 rows  CHRIST OUR REDEEMER CEMETERY
       2.82M        1 rows  MONONGAHELA CEMETERY

MUNICIPALITY by rows
        32  PITTSBURGH
        18  WEST MIFFLIN BOROUGH
        16  SHALER TOWNSHIP
        15  ROSS TOWNSHIP
        12  RESERVE TOWNSHIP
         9  PENN HILLS MUNICIPALITY
         8  ELIZABETH TOWNSHIP
         7  SOUTH FAYETTE TOWNSHIP
         7  WEST DEER TOWNSHIP
         7  NORTH VERSAILLES TOWNSHIP
         6  FRANKLIN PARK BOROUGH
         6  PINE TOWNSHIP
         6  HAMPTON TOWNSHIP
         6  MCCANDLESS TOWNSHIP
         6  KENNEDY TOWNSHIP
         6  PLUM BOROUGH
         5  RICHLAND TOWNSHIP
         5  SCOTT TOWNSHIP
         5  WILKINS TOWNSHIP
         5  MUNHALL BOROUGH

MUNICIPALITY by dollars
      52.71M       32 rows  PITTSBURGH
      13.16M       16 rows  SHALER TOWNSHIP
      13.02M        1 rows  PLEASANT HILLS BOROUGH
      12.10M        4 rows  MONROEVILLE MUNICIPALITY
      10.35M       15 rows  ROSS TOWNSHIP
       9.79M        7 rows  NORTH VERSAILLES TOWNSHIP
       8.36M        9 rows  PENN HILLS MUNICIPALITY
       5.85M        5 rows  RICHLAND TOWNSHIP
       5.43M        2 rows  BRADDOCK HILLS BOROUGH
       5.32M        7 rows  SOUTH FAYETTE TOWNSHIP
       5.21M        4 rows  MOON TOWNSHIP
       4.92M        6 rows  PLUM BOROUGH
       4.86M        6 rows  MCCANDLESS TOWNSHIP
       4.76M        1 rows  FRAZER TOWNSHIP
       4.66M       18 rows  WEST MIFFLIN BOROUGH
       4.54M        8 rows  ELIZABETH TOWNSHIP
       3.76M        4 rows  SEWICKLEY HEIGHTS BOROUGH
       3.55M       12 rows  RESERVE TOWNSHIP
       3.34M        6 rows  KENNEDY TOWNSHIP
       3.33M        4 rows  MCKEESPORT

TYPE by rows
       307  CEMETERY

TYPE by dollars
     230.62M      307 rows  CEMETERY

SRC_SHA256 by rows
       307  05e3c3290ff33e5518b59ade42bf4b30f8a8a5be756bbeacc23df90f359bcfa6

SRC_SHA256 by dollars
     230.62M      307 rows  05e3c3290ff33e5518b59ade42bf4b30f8a8a5be756bbeacc23df90f359b

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  ALLEGHENY CEMETERY                        2026:13.11M
  BETHANY CEMETERY                          2026:217.3K
  CALVARY CEMETERY                          2026:7.16M
  CROSSROADS CEMETERY                       2026:432.6K
  FAIRVIEW CEMETERY                         2026:310.4K
  GOOD SHEPARD CEMETERY                     2026:7.80M
  GRANDVIEW CEMETERY                        2026:6.28M
  HOLY SAVIOR CEMETERY                      2026:5.04M
  HOLY TRINITY CEMETERY                     2026:913.4K
  HOMEWOOD CEMETERY                         2026:7.67M
  JEFFERSON MEMORIAL CEMETERY               2026:13.02M
  OHAVE ZEDEK CEMETERY                      2026:42.5K
  OLD GERMAN CEMETERY                       2026:116.7K
  OUR LADY OF HOPE CEMETERY                 2026:4.76M
  PINE CREEK CEMETERY                       2026:140.6K
  RESURRECTION CEMETERY                     2026:4.51M
  ST GEORGE CEMETERY                        2026:811.6K
  ST JOHNS LUTHERAN CEMETERY                2026:666.6K
  ST JOSEPH CEMETERY                        2026:1.65M
  ST JOSEPHS CEMETERY                       2026:445.2K
  ST MARYS CEMETERY                         2026:5.91M
  ST MICHAELS CEMETERY                      2026:1.11M
  ST NICHOLAS CEMETERY                      2026:1.90M
  ST PATRICK CEMETERY                       2026:198.8K
  ST PAULS LUTHERAN CEMETERY                2026:169.3K
  ST PETERS CEMETERY                        2026:1.48M
  ST STANISLAUS AND ST ANTHONY CATHOLIC CE  2026:4.71M
  STS PETER & PAUL CEMETERY                 2026:329.8K
  TURNER CEMETERY                           2026:29.9K
  UNION DALE CEMETERY                       2026:4.28M

MUNICIPALITY by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  BRADDOCK HILLS BOROUGH                    2026:5.43M
  ELIZABETH TOWNSHIP                        2026:4.54M
  FRANKLIN PARK BOROUGH                     2026:1.87M
  FRAZER TOWNSHIP                           2026:4.76M
  HAMPTON TOWNSHIP                          2026:2.08M
  KENNEDY TOWNSHIP                          2026:3.34M
  MCCANDLESS TOWNSHIP                       2026:4.86M
  MCKEESPORT                                2026:3.33M
  MONROEVILLE MUNICIPALITY                  2026:12.10M
  MOON TOWNSHIP                             2026:5.21M
  MUNHALL BOROUGH                           2026:1.53M
  NORTH VERSAILLES TOWNSHIP                 2026:9.79M
  PENN HILLS MUNICIPALITY                   2026:8.36M
  PINE TOWNSHIP                             2026:616.3K
  PITTSBURGH                                2026:52.71M
  PLEASANT HILLS BOROUGH                    2026:13.02M
  PLUM BOROUGH                              2026:4.92M
  RESERVE TOWNSHIP                          2026:3.55M
  RICHLAND TOWNSHIP                         2026:5.85M
  ROSS TOWNSHIP                             2026:10.35M
  SCOTT TOWNSHIP                            2026:1.53M
  SEWICKLEY HEIGHTS BOROUGH                 2026:3.76M
  SHALER TOWNSHIP                           2026:13.16M
  SOUTH FAYETTE TOWNSHIP                    2026:5.32M
  WEST DEER TOWNSHIP                        2026:1.71M
  WEST MIFFLIN BOROUGH                      2026:4.66M
  WILKINS TOWNSHIP                          2026:1.33M

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FULL_ADDRESS | other | 308 | 0 | 1000 SHARPSHILL RD 2; 531 LANG RD
531 LANG RD 2; 444 GLENFIELD RD 2; 1803 WEDDELL RD 2 |
| MUNICIPALITY | who | 76 | 0 | PITTSBURGH 32; WEST MIFFLIN BOROUGH 18; SHALER TOWNSHIP 16; ROSS TOWNSHIP 15 |
| NAME | who | 280 | 0 | ST JOSEPH CEMETERY 6; ST NICHOLAS CEMETERY 5; ST MARYS CEMETERY 4; ST JOHNS LUTHERAN CEMETER 4 |
| OBJECTID | other | 305 | 0 | 2664 2; 1203 2; 1202 2; 1201 2 |
| SHAPE__AREA | amount | 301 | 0 | 3322539.4857788086 2; 86493.49572753906 2; 28972.0927734375 2; 5989.626312255859 2 |
| SHAPE__LENGTH | amount | 306 | 0 | 16190.368192672006 2; 1698.923833028469 2; 676.3982626778321 2; 320.26785891896077 2 |
| TYPE | who | 1 | 0 | CEMETERY 307 |
| GEOMETRY | other | 305 | 0 | MULTIPOLYGON (((590497.80 2; POLYGON ((573486.55620170 2; POLYGON ((573907.33628143 2; POLYGON ((601581.02585215 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:39:26.06467 307 |
| SOURCE_RUN_ID | audit | 1 | 0 | d8743adc-80e4-4075-93d0-d 307 |
| SRC_SHA256 | who | 1 | 0 | 05e3c3290ff33e5518b59ade4 307 |
