# FED_EPA_NPDES_NPDES_SICS

rows 792.8K  columns 7  scan 2.0s

roles: audit 2, category 1, other 3, who 1

## who

SIC_DESC by rows
    169.0K  Single-Family Housing Construction
     74.9K  Heavy Construction
     56.3K  Nonresidential Construction
     51.3K  Sewerage Systems
     40.2K  Highway And Street Construction
     28.1K  Water, Sewer, And Utility Lines
     19.0K  Excavation Work
     13.9K  Ready-Mixed Concrete
     12.6K  Residential Construction
     12.3K  Subdividers And Developers
     11.9K  Industrial Buildings And Warehouses
     10.3K  Construction Sand And Gravel
      9.5K  Bituminous Coal And Lignite - Surface
      8.2K  Scrap And Waste Materials
      7.6K  Electric Services
      7.0K  Gold Ores
      7.0K  Motor Vehicle Parts, Used
      6.9K  Nonclassifiable Establishments
      6.6K  Dwelling Operators, Except Apartments
      6.5K  Water Supply

## what

PRIMARY_INDICATOR_FLAG: Y 90%, N 10%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NPDES_ID | other | 700.7K | 0 | KYG405874 2.2K; KYG405873 2.2K; KYG405872 2.2K; KYG405871 2.2K |
| SIC_CODE | other | 983 | 0 | 1521 169.0K; 1629 74.9K; 1542 56.3K; 4952 51.3K |
| SIC_DESC | who | 967 | 0 | Single-Family Housing Con 169.0K; Heavy Construction 74.9K; Nonresidential Constructi 56.3K; Sewerage Systems 51.3K |
| PRIMARY_INDICATOR_FLAG | category | 2 | 0 | Y 711.6K; N 81.2K |
| _INGESTED_AT | audit | 1 | 0 | 1786043934360401 792.8K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 1948554e-dd48-47f6-8368-6 792.8K |
| _SRC_SHA256 | other | 1 | 0 | 8a1f35cdc7c965dc945ca7a14 792.8K |
