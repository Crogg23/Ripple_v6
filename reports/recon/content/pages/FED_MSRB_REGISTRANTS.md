# FED_MSRB_REGISTRANTS

rows 925  columns 7  scan 1.7s

roles: audit 2, category 1, other 1, state 1, who 2

## who

FIRM_NAME by rows
         1  Financial Security Management, Inc.
         1  Mutual Funds Associates, Inc.
         1  GlobaLink Securities, Inc
         1  Quincy Wells Capital, LLC
         1  Nancy Barron & Associates Inc.
         1  Memphis Capital
         1  SF Investments, Inc.
         1  Momentum Independent Network Inc.
         1  Alight Financial Solutions LLC
         1  American Capital Partners, LLC
         1  VALIC Financial Advisors, Inc
         1  ICE Securities Execution & Clearing, LLC
         1  TE Laird Securities, LLC
         1  Morgan Stanley & Co. LLC
         1  Bernardi Securities, Inc.
         1  APW Capital, Inc.
         1  Syndicated Capital, Inc.
         1  Folio Investments, Inc.
         1  JKR & Co., Inc.
         1  Monarch Capital Group, LLC

SRC_SHA256 by rows
       925  969de87915296812c032073acb05fe07f7e27ad2b37666e5e3ddaefab311ac50

## where

STATE: NY 187, CA 70, FL 68, IL 64, TX 64, NJ 46, OH 34, PA 32, MO 27, NC 25, MA 23, MN 22

## what

REGISTRANT_TYPE: Broker Dealer 92%, Broker Dealer/Municipal Adviso 7%, Bank Dealer 2%, Bank Dealer/Municipal Advisor 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FIRM_NAME | who | 926 | 0 | USA Financial Securities, 5; Guzman & Company 5; LPS Capital LLC 5; Wealthfront Brokerage LLC 5 |
| MSRB_ID | other | 925 | 0 | A5759 5; A2938 5; A7167 5; A7401 5 |
| STATE | state | 49 | 0 | NY 187; CA 70; FL 68; IL 64 |
| REGISTRANT_TYPE | category | 4 | 0 | Broker Dealer 848; Broker Dealer/Municipal A 61; Bank Dealer 15; Bank Dealer/Municipal Adv 1 |
| INGESTED_AT | audit | 1 | 0 | 1786165044012327 925 |
| SOURCE_RUN_ID | audit | 1 | 0 | 9a638720-399e-496a-a65f-6 925 |
| SRC_SHA256 | who | 1 | 0 | 969de87915296812c032073ac 925 |
