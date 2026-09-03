# XC_GUTTMACHER_MONTHLY_ABORTION

rows 2.0K  columns 11  scan 3.7s

roles: audit 2, date 1, other 3, state 1, who 4

## when

MONTH
  2023       582  ###########################
  2024       648  ##############################
  2025       648  ##############################
  2026       162  ########

## who

SOURCE by rows
      2.0K  https://www.guttmacher.org/monthly-abortion-provision-study or https:/

NOTES by rows
      2.0K  All estimates rounded to nearest 10. Estimates include data on procedu

PUBLISHDATE by rows
      2.0K  06-09-2026

SRC_SHA256 by rows
      2.0K  2a0d49a56dd4b0054e9ae6f08aaeb5f615b6ea1ec116d8e1f09d8214395fc403

## who x when

SOURCE by MONTH
  https://www.guttmacher.org/monthly-abort  2023:582 2024:648 2025:648 2026:162

NOTES by MONTH
  All estimates rounded to nearest 10. Est  2023:582 2024:648 2025:648 2026:162

## where

STATE: WY 39, WI 39, WA 39, VT 39, VA 39, UT 39, SC 39, RI 39, PA 39, OR 39, OH 39, NY 39

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| STATE | state | 54 | 0 | WY 39; WI 39; WA 39; VT 39 |
| MONTH | date | 39 | 0 | 2026-03-15 54; 2026-02-15 54; 2026-01-15 54; 2025-12-15 54 |
| MEDIAN | other | 644 | 0 | 220 39; 40 35; 70 33; 200 33 |
| LOWERBOUND | other | 604 | 0 | 200 41; 20 40; 60 36; 30 35 |
| UPPERBOUND | other | 642 | 0 | 230 36; 50 32; 220 29; 210 29 |
| SOURCE | who | 1 | 0 | https://www.guttmacher.or 2.0K |
| NOTES | who | 1 | 0 | All estimates rounded to  2.0K |
| PUBLISHDATE | who | 1 | 0 | 06-09-2026 2.0K |
| INGESTED_AT | audit | 1 | 0 | 1782615459528645 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 367536d6-4771-4091-b2ce-e 2.0K |
| SRC_SHA256 | who | 1 | 0 | 2a0d49a56dd4b0054e9ae6f08 2.0K |
