# PORTAL_CKA_WPRDC_ALLEGHENY_694F40A849

rows 10  columns 16  scan 3.0s

roles: amount 1, audit 2, category 11, date 1, other 1, who 1

## when

INGESTED_AT
  2026        10  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENG | 10 | 468.39 | 1.1K | 3.0K | 3.1K | 12.2K |

## who

SRC_SHA256 by rows
        10  45629f3683f6dea92b2da7d514cb2ab1415bb6676d4f2d4d993bf43e19ef2b33

SRC_SHA256 by dollars
       12.2K       10 rows  45629f3683f6dea92b2da7d514cb2ab1415bb6676d4f2d4d993bf43e19ef

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENG
  45629f3683f6dea92b2da7d514cb2ab1415bb667  2026:12.2K

## what

OBJECTID_1: 19 10%, 18 10%, 17 10%, 16 10%, 15 10%, 14 10%, 13 10%, 12 10%, 11 10%, 10 10%

CITY: Pittsburgh 30%, McKeesport 10%, Tarentum 10%, South Park 10%, Elizabeth 10%, Allison Park 10%, Natrona Heights 10%, Oakdale 10%

GLOBALID: 5f908750-9055-47e2-949d-51abe7 10%, fa2e24d1-373a-4d88-9b90-5d0cb9 10%, 78fb078b-a3c0-4324-aac1-c268cd 10%, b327f936-2924-4576-bd30-ffcaba 10%, 9d6c9ef2-ab8f-42c4-9127-79dc8c 10%, e9820148-464a-4a6b-96be-ed9b22 10%, 7313d689-f835-4e80-8214-2267df 10%, 48e6999d-3acf-408b-8252-888a49 10%, 83be05e9-978d-4982-a59d-e7790a 10%, 51f030eb-1442-4956-a3f6-ebb503 10%

ADDRESS: 3301 Muse Lane 10%, 1090 Bailies Run Road 10%, 675 Old Frankstown Road  10%, 100 Buffalo Drive  10%, 200 Hartwood Acres 10%, 651 Round Hill Road  10%, 303 Pearce Mill Road  10%, 5200 Freeport Road 10%, 608 Ridge Road  10%, 799 Pinkerton Run Rd 10%

LASTUPDATE: Wed, 23 Oct 2024 14:00:00 GMT 30%, Wed, 30 Jul 2025 14:00:00 GMT 20%, Tue, 15 Apr 2025 14:00:00 GMT 20%, Mon, 17 Nov 2025 15:00:00 GMT 10%, Wed, 06 Aug 2025 14:00:00 GMT 10%, Mon, 20 Nov 2023 15:00:00 GMT 10%

ZIP: 15131 10%, 15084 10%, 15239 10%, 15129 10%, 15238 10%, 15037 10%, 15101 10%, 15065 10%, 15205 10%, 15071 10%

IMAGEURL: https://www.alleghenycounty.us 10%, https://www.alleghenycounty.us 10%, https://www.alleghenycounty.us 10%, https://www.alleghenycounty.us 10%, https://www.alleghenycounty.us 10%, https://www.alleghenycounty.us 10%, https://www.alleghenycounty.us 10%, https://www.alleghenycounty.us 10%, https://www.alleghenycounty.us 10%, https://pittsburghbotanicgarde 10%

OBJECTID: 428 10%, 1662 10%, 1262 10%, 433 10%, 427 10%, 33 10%, 32 10%, 30 10%, 29 10%, 28 10%

NAME: White Oak Park 10%, Deer Lakes 10%, Boyce Park 10%, South Park 10%, Hartwood Acres 10%, Round Hill 10%, North Park 10%, Harrison Hills 10%, Settlers Cabin 10%, Pgh Botanic Garden 10%

WEBURL: https://www.alleghenycounty.us 10%, https://www.alleghenycounty.us 10%, https://www.alleghenycounty.us 10%, https://www.alleghenycounty.us 10%, https://www.alleghenycounty.us 10%, https://www.alleghenycounty.us 10%, https://www.alleghenycounty.us 10%, https://www.alleghenycounty.us 10%, https://www.alleghenycounty.us 10%, https://pittsburghbotanicgarde 10%

DATASPATIAL_WKB: \x0000000006000000020000000003 10%, \x000000000300000003000001cec0 10%, \x000000000300000001000001e2c0 10%, \x00000000030000000100000260c0 10%, \x00000000030000000100000084c0 10%, \x0000000006000000040000000003 10%, \x0000000006000000070000000003 10%, \x0000000006000000070000000003 10%, \x00000000030000000100000189c0 10%, \x000000000300000002000000fac0 10%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | category | 10 | 0 | 19 1; 18 1; 17 1; 16 1 |
| CITY | category | 8 | 0 | Pittsburgh 3; McKeesport 1; Tarentum 1; South Park 1 |
| GLOBALID | category | 10 | 0 | 5f908750-9055-47e2-949d-5 1; fa2e24d1-373a-4d88-9b90-5 1; 78fb078b-a3c0-4324-aac1-c 1; b327f936-2924-4576-bd30-f 1 |
| ADDRESS | category | 10 | 0 | 3301 Muse Lane 1; 1090 Bailies Run Road 1; 675 Old Frankstown Road  1; 100 Buffalo Drive  1 |
| LASTUPDATE | category | 6 | 0 | Wed, 23 Oct 2024 14:00:00 3; Wed, 30 Jul 2025 14:00:00 2; Tue, 15 Apr 2025 14:00:00 2; Mon, 17 Nov 2025 15:00:00 1 |
| STATE | other | 1 | 0 | PA 10 |
| ZIP | category | 10 | 0 | 15131 1; 15084 1; 15239 1; 15129 1 |
| IMAGEURL | category | 10 | 0 | https://www.alleghenycoun 1; https://www.alleghenycoun 1; https://www.alleghenycoun 1; https://www.alleghenycoun 1 |
| SHAPE_LENG | amount | 10 | 0 | 803.34776172 1; 1164.58348473 1; 1061.99451335 1; 1998.12428087 1 |
| OBJECTID | category | 10 | 0 | 428 1; 1662 1; 1262 1; 433 1 |
| NAME | category | 10 | 0 | White Oak Park 1; Deer Lakes 1; Boyce Park 1; South Park 1 |
| WEBURL | category | 10 | 0 | https://www.alleghenycoun 1; https://www.alleghenycoun 1; https://www.alleghenycoun 1; https://www.alleghenycoun 1 |
| DATASPATIAL_WKB | category | 10 | 0 | \x00000000060000000200000 1; \x00000000030000000300000 1; \x00000000030000000100000 1; \x00000000030000000100000 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:12:38.18413 10 |
| SOURCE_RUN_ID | audit | 1 | 0 | 1933e688-dd04-481a-a7ba-d 10 |
| SRC_SHA256 | who | 1 | 0 | 45629f3683f6dea92b2da7d51 10 |
