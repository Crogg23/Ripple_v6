# FED_EPA_NPDES_NPDES_NAICS

rows 326.5K  columns 7  scan 2.6s

roles: audit 2, category 1, other 3, who 1

## who

NAICS_DESC by rows
    137.5K  New Single-Family Housing Construction [except For-Sale Builders]
     37.7K  Commercial and Institutional Building Construction
     14.9K  Sewage Treatment Facilities
     14.0K  Highway, Street, and Bridge Construction
      9.8K  Water and Sewer Line and Related Structures Construction
      7.9K  Industrial Building Construction
      7.2K  Other Heavy and Civil Engineering Construction
      5.6K  Power and Communication Line and Related Structures Construction
      3.9K  Construction Sand and Gravel Mining
      3.8K  Site Preparation Contractors
      3.6K  Bituminous Coal and Lignite Surface Mining
      3.1K  Ready-Mix Concrete Manufacturing
      2.8K  New Multifamily Housing Construction [except For-Sale Builders]
      2.4K  New Housing For-Sale Builders
      2.2K  Lessors of Residential Buildings and Dwellings
      1.9K  Water Supply and Irrigation Systems
      1.7K  Administration of Air and Water Resource and Solid Waste Management Pr
      1.6K  Land Subdivision
      1.6K  Recyclable Material Merchant Wholesalers
      1.4K  General Warehousing and Storage

## what

PRIMARY_INDICATOR_FLAG: Y 88%, N 12%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NPDES_ID | other | 300.0K | 0 | WAR315160 1.6K; WAR305536 1.6K; WAR314662 1.6K; WAR314366 1.6K |
| NAICS_CODE | other | 1.1K | 0 | 236115 137.5K; 236220 37.7K; 221320 14.9K; 237310 14.0K |
| NAICS_DESC | who | 1.1K | 0 | New Single-Family Housing 137.5K; Commercial and Institutio 37.7K; Sewage Treatment Faciliti 14.9K; Highway, Street, and Brid 14.0K |
| PRIMARY_INDICATOR_FLAG | category | 2 | 0 | Y 288.8K; N 37.7K |
| _INGESTED_AT | audit | 1 | 0 | 1786043926558927 326.5K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 68c090ac-130f-45eb-8520-b 326.5K |
| _SRC_SHA256 | other | 1 | 0 | c8aefda0acaf4e4d517810791 326.5K |
