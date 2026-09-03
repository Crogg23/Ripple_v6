# PORTAL_CKA_INDIANA_DATA_HUB_77FCBC0131

rows 11  columns 5  scan 2.9s

roles: audit 2, category 2, date 1, who 1

## when

INGESTED_AT
  2026        11  ##############################

## who

SRC_SHA256 by rows
        11  c20f7260e74d56e2bff1821fad1105534e054fb0e10529fd02974fa05e048d2e

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  c20f7260e74d56e2bff1821fad1105534e054fb0  2026:11

## what

COLUMN_NAME: Total_or_per_1k 9%, Aggregated_Value 9%, Year 9%, Count_Subcategory 9%, Count_Category 9%, County 9%, County_Type 9%, Dispensation_Prescription 9%, Cooccurrence_flg 9%, Drug 9%, Drug_Class 9%

DEFINITION: Denotes whether the aggregated 9%, Value of aggregated count or r 9%, Year of prescription 9%, Subcategory (the more granular 9%, Primary category that the coun 9%, County that the Aggregated_cou 9%, Denotes whether the county is  9%, Denoting whether the data is r 9%, A co-occurance is a dispensati 9%, Name of the drug's active ingr 9%, Drug class or group of drug cl 9%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COLUMN_NAME | category | 11 | 0 | Total_or_per_1k 1; Aggregated_Value 1; Year 1; Count_Subcategory 1 |
| DEFINITION | category | 11 | 0 | Denotes whether the aggre 1; Value of aggregated count 1; Year of prescription 1; Subcategory (the more gra 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:07:10.42709 11 |
| SOURCE_RUN_ID | audit | 1 | 0 | 97bb21ef-c387-4369-af5c-f 11 |
| SRC_SHA256 | who | 1 | 0 | c20f7260e74d56e2bff1821fa 11 |
