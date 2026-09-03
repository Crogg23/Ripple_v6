# FED_EPA_RCRA_VIOSNC_HISTORY

rows 2.68M  columns 8  scan 2.3s

roles: audit 2, category 2, other 2, state 1, who 1

## who

YRMONTH by rows
      9.5K  199304
      9.5K  199404
      9.4K  199309
      9.4K  199303
      9.4K  199308
      9.4K  199403
      9.3K  199306
      9.3K  199203
      9.3K  199305
      9.2K  199405
      9.2K  199406
      9.2K  199407
      9.2K  199307
      9.2K  199310
      9.1K  199209
      9.1K  199204
      9.1K  199408
      9.1K  199210
      9.1K  199311
      9.0K  199207

## where

ACTIVITY_LOCATION: CA 170.9K, OH 159.2K, CT 152.5K, MA 152.4K, MI 126.9K, PA 122.8K, FL 119.2K, IN 118.9K, NY 109.9K, IL 104.7K, TX 82.6K, NJ 76.1K

## what

VIO_FLAG: Y 96%, N 4%

SNC_FLAG: N 86%, Y 14%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID_NUMBER | other | 146.9K | 0 | ILD048843809 4.3K; ILD006536239 4.2K; ILD041889023 4.2K; ILD006294102 4.2K |
| ACTIVITY_LOCATION | state | 62 | 0 | CA 170.9K; OH 159.2K; CT 152.5K; MA 152.4K |
| YRMONTH | who | 564 | 0 | 199206 13.4K; 199207 13.4K; 199312 13.4K; 199511 13.4K |
| VIO_FLAG | category | 2 | 0 | Y 2.57M; N 106.4K |
| SNC_FLAG | category | 2 | 0 | N 2.30M; Y 373.9K |
| INGESTED_AT | audit | 1 | 0 | 1786163847152640 2.68M |
| SOURCE_RUN_ID | audit | 1 | 0 | ee35a6a3-0939-44ee-a263-f 2.68M |
| SRC_SHA256 | other | 1 | 0 | 8457e99a525f9546773bc2e3f 2.68M |
