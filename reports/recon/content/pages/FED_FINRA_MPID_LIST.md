# FED_FINRA_MPID_LIST

rows 4.2K  columns 12  scan 2.1s

roles: audit 2, category 5, other 2, who 3

## who

NAME by rows
        68  Bofa Securities, Inc.
        47  VELOCITY CLEARING, LLC
        31  GOLDMAN SACHS & CO. LLC
        27  District 8 - Chicago
        22  J.P. Morgan Securities LLC
        22  Citigroup Global Markets Inc.
        19  Piper Sandler & Co.
        17  OTC LINK LLC
        17  DRW EXECUTION SERVICES, LLC
        17  OES Brokerage Services, L.L.C.
        17  VIRTU Americas LLC
        16  Pershing LLC
        15  RODMAN & RENSHAW, LLC
        14  MORGAN STANLEY & CO. LLC
        14  INSTINET, LLC
        13  JUMP TRADING, LLC
        13  CURVATURE SECURITIES LLC
        12  Deutsche Bank Securities Inc.
        12  Raymond James & Associates, Inc.
        12  BOFA Securities, INC.

LOCATION by rows
       140  NASDAQ TRADING
       110  NEW YORK, NY
        44  TRADING
        27  NEW YORK  NY
        25  TRADING DESK
        24  NASDAQ/OTCBB TRADING
        23  Trading Desk
        17  CHICAGO, IL
        15  NEW YORK
        12  MINNEAPOLIS, MN
        11  ARBITRAGE
        11  Main Line
        11  NEW YORK NY
        10  CONVERTIBLES
        10  JERSEY CITY, NJ
         9  PREFERRED
         9  ATLANTA, GA
         9  BOSTON, MA
         8  SAN FRANCISCO, CA
         8  Trade Floor

SRC_SHA256 by rows
      4.2K  6f33a0d570e0e65f94d1591b42e5a4cdc01f0f06e775831d240e4dfe4e0e5d6c

## what

MP_TYPE: P 65%, M 19%, N 9%, O 5%, E 1%, C 0%, Q 0%, S 0%

NASDAQ_MEMBER: N 67%, Y 33%

FINRA_MEMBER: Y 67%, N 33%

NASDAQ_BX_MEMBER: N 84%, Y 16%

PSX_PARTICIPANT: N 84%, Y 16%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| MPID | other | 3.5K | 0 | NASD 39; SBSH 31; MLCO 30; WEED 29 |
| MP_TYPE | category | 8 | 1 | P 2.7K; M 807; N 374; O 230 |
| NAME | who | 2.6K | 1 | Bofa Securities, Inc. 69; VELOCITY CLEARING, LLC 62; District 8 - Chicago 38; GOLDMAN SACHS & CO. LLC 34 |
| LOCATION | who | 553 | 2.9K | NASDAQ TRADING 140; NEW YORK, NY 110; TRADING 44; NEW YORK  NY 27 |
| TELEPHONE | other | 1.3K | 2.8K | 800-825-9550 10; 212-856-3697 9; 310-734-0040 8; 801-532-6761 8 |
| NASDAQ_MEMBER | category | 2 | 1 | N 2.8K; Y 1.4K |
| FINRA_MEMBER | category | 2 | 1 | Y 2.8K; N 1.4K |
| NASDAQ_BX_MEMBER | category | 2 | 1 | N 3.5K; Y 690 |
| PSX_PARTICIPANT | category | 2 | 1 | N 3.5K; Y 669 |
| INGESTED_AT | audit | 1 | 0 | 1786153459479637 4.2K |
| SOURCE_RUN_ID | audit | 1 | 0 | 04be7889-a7b7-4f0a-ad1f-3 4.2K |
| SRC_SHA256 | who | 1 | 0 | 6f33a0d570e0e65f94d1591b4 4.2K |
