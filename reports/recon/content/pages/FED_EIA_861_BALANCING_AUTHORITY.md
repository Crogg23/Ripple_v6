# FED_EIA_861_BALANCING_AUTHORITY

rows 189  columns 8  scan 2.4s

roles: audit 2, other 3, state 1, who 2

## who

BALANCING_AUTHORITY_NAME by rows
        17  Midcontinent Independent Transmission System Operator, Inc..
        15  PJM Interconnection, LLC
        14  Southwest Power Pool
         9  Western Area Power Administration - Rocky Mountain Region
         7  PacifiCorp - East
         7  Bonneville Power Administration
         7  Tennessee Valley Authority
         7  ISO New England Inc.
         5  Public Service Company of New Mexico
         5  Western Area Power Administration - Desert Southwest Region
         4  Southern Company Services, Inc. - Trans
         4  PacifiCorp - West
         4  Public Service Company of Colorado
         4  Associated Electric Cooperative, Inc.
         3  Nevada Power Company
         3  California Independent System Operator
         3  New York Independent System Operator
         3  Western Area Power Administration UGP West
         3  Duke Energy Carolinas
         3  Avista Corporation

SRC_SHA256 by rows
       189  77ce49c60ac5a6bad50c442fc401aad5404a21da875dc5cbaba353af5ede54de

## where

STATE: NM 11, AZ 11, FL 10, MT 9, WA 9, CA 8, UT 7, NC 7, WY 6, CO 5, NV 5, GA 5

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DATA_YEAR | other | 1 | 0 | 2024 189 |
| BA_ID | other | 67 | 0 | 56669 17; 14725 15; 59504 14; 28503 9 |
| BA_CODE | other | 67 | 0 | MISO 17; PJM 15; SWPP 14; WACM 9 |
| STATE | state | 51 | 0 | NM 11; AZ 11; FL 10; MT 9 |
| BALANCING_AUTHORITY_NAME | who | 67 | 0 | Midcontinent Independent  17; PJM Interconnection, LLC 15; Southwest Power Pool 14; Western Area Power Admini 9 |
| INGESTED_AT | audit | 1 | 0 | 1786134152975199 189 |
| SOURCE_RUN_ID | audit | 1 | 0 | 51800c69-0e2a-4a62-b756-9 189 |
| SRC_SHA256 | who | 1 | 0 | 77ce49c60ac5a6bad50c442fc 189 |
