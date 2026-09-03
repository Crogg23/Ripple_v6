# PORTAL_SOC_CONNECTICUT_OPEN_1CD7311280

rows 1.6K  columns 14  scan 4.5s

roles: audit 2, category 5, date 1, other 3, who 4

## when

INGESTED_AT
  2026      1.6K  ##############################

## who

STRUCTURE_OWNER by rows
       225  SBA
       184  Crown Castle
       159  American Tower
        89  AT&T
        69  Sprint
        64  Verizon
        44  CL&P
        35  American Tower Corporation
        31  Cellco
        30  SNET/SCLP
        26  DPS
        22  Cordless Data Transfer
        21  Eversource
        21  SBA Towers
        20  Mountaintop Enterprises
        18  American Tower Management, Inc
        17  Crown
        17  Berlin Fire Dept
        17  BAM
        16  VoiceStream

USER by rows
       314  Verizon
       297  AT&T
       231  T-Mobile
       134  Sprint
        87  Cingular
        55  DISH
        42  Pocket (now MetroPCS)
        30  BAM
        29  Clearwire
        28  nan
        27  Nextel
        26  MetroPCS
        25  Cingular/AT&T
        25  AT&T Wireless
        21  SNET/SCLP
        20  SCLP
        18  SNET/Cingular
        17  VoiceStream
        12  Omni
        10  Eversource

ADDRESS by rows
        33  **** Trumbull Avenue
        33  ***-*** North Main Street
        28  ** Cow Hill Road
        26  *** Beckley Road
        25  *** Kaechele Place
        24  ** New Hartford Road
        24  *** Highland Avenue
        24  **** Blue Hills Avenue
        22  ** Wig Hill Road
        22  **** Connecticut Avenue
        22  ** Carmen Hill Road
        21  *** Wakelee Avenue
        21  *** Amity Road
        21  *** Willis Street
        20  *** Vernon Road
        20  ** Canton Springs Road
        20  * Meyers Road
        20  **** Chamberlain Highway
        20  *** Kensington Road
        20  *** Riley Mountain Road

SRC_SHA256 by rows
      1.6K  d5a13c4f37c070530274e7506be9fae422bcaf62c8b786e08605509e2d0a1536

## who x when

STRUCTURE_OWNER by INGESTED_AT  LOAD STAMP, not an event date
  AT&T                                      2026:89
  American Tower                            2026:159
  American Tower Corporation                2026:35
  American Tower Management, Inc            2026:18
  BAM                                       2026:17
  Berlin Fire Dept                          2026:17
  CL&P                                      2026:44
  Cellco                                    2026:31
  Cordless Data Transfer                    2026:22
  Crown                                     2026:17
  Crown Castle                              2026:184
  DPS                                       2026:26
  Eversource                                2026:21
  Mountaintop Enterprises                   2026:20
  SBA                                       2026:225
  SBA Towers                                2026:21
  SNET/SCLP                                 2026:30
  Sprint                                    2026:69
  Verizon                                   2026:64
  VoiceStream                               2026:16

USER by INGESTED_AT  LOAD STAMP, not an event date
  AT&T                                      2026:297
  AT&T Wireless                             2026:25
  BAM                                       2026:30
  Cingular                                  2026:87
  Cingular/AT&T                             2026:25
  Clearwire                                 2026:29
  DISH                                      2026:55
  Eversource                                2026:10
  MetroPCS                                  2026:26
  Nextel                                    2026:27
  Omni                                      2026:12
  Pocket (now MetroPCS)                     2026:42
  SCLP                                      2026:20
  SNET/Cingular                             2026:18
  SNET/SCLP                                 2026:21
  Sprint                                    2026:134
  T-Mobile                                  2026:231
  Verizon                                   2026:314
  VoiceStream                               2026:17
  nan                                       2026:28

## what

TOWN: Branford 14%, Bridgeport 13%, Bloomfield 11%, Colchester 9%, Cheshire 9%, Berlin 8%, Canton 7%, Ashford 6%, Bristol 6%, Brooklyn 6%, Avon 5%, Bethel 5%

TWR_TYPE: monopole 64%, self-support lattice 23%, guyed-lattice 6%, utility pole 3%, nan 1%, water tank 1%, self-support lattice (type J) 1%, smokestack 0%, silo 0%, Monopine 0%, monopoleonopine 0%, roof top 0%

BACKUP_POWER_TYPE: nan 91%, diesel generator 6%, propane generator 2%, natural gas generator 0%, generator 0%, BBU 0%, battery & 25kW propane gen 0%, deisel generator 0%, fuel cell backup 0%, diesel 0%, diesel-generator 0%, battery 0%

C_5G_SERVICES: nan 91%, yes 9%, NA 0%

BACKUP_POWER_SIZE_DURATION: nan 96%, 30-kilowatt 1%, 50-kilowatt 0%, 80-kilowatt 0%, 30-kW 0%, 25-kilowatt 0%, 48-kilowatt 0%, 7.5 kW 0%, 25 kW 0%, 20-kilowatt 0%, 24-kilowatt 0%, 20-kW 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| TOWN | category | 34 | 0 | Branford 139; Bridgeport 134; Bloomfield 111; Colchester 90 |
| ADDRESS | who | 173 | 0 | **** Trumbull Avenue 33; ***-*** North Main Street 33; ** Cow Hill Road 28; *** Beckley Road 26 |
| USER | who | 106 | 0 | Verizon 314; AT&T 297; T-Mobile 231; Sprint 134 |
| STRUCTURE_OWNER | who | 138 | 0 | SBA 225; Crown Castle 184; American Tower 159; AT&T 89 |
| TWR_TYPE | category | 23 | 0 | monopole 1.0K; self-support lattice 372; guyed-lattice 102; utility pole 40 |
| ANT_HEIGHT | other | 226 | 0 | nan 171; 150 57; 140 51; 110 49 |
| TWR_HEIGHT | other | 96 | 0 | 150 268; 180 162; 120 110; 125 80 |
| BACKUP_POWER_TYPE | category | 19 | 0 | nan 1.5K; diesel generator 95; propane generator 25; natural gas generator 5 |
| C_5G_SERVICES | category | 3 | 0 | nan 1.5K; yes 140; NA 1 |
| DOCKET_OR_PETITION_NUM | other | 132 | 0 | nan 1.4K; Docket No. 288 5; Petition No. 1547 5; Sub-petition No. 1133 4 |
| BACKUP_POWER_SIZE_DURATION | category | 30 | 0 | nan 1.5K; 30-kilowatt 21; 50-kilowatt 7; 80-kilowatt 5 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:08:02.47765 1.6K |
| SOURCE_RUN_ID | audit | 1 | 0 | 0d0d91a5-f34e-4114-aecb-d 1.6K |
| SRC_SHA256 | who | 1 | 0 | d5a13c4f37c070530274e7506 1.6K |
