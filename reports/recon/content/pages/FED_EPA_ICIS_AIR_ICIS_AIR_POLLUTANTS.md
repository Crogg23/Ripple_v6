# FED_EPA_ICIS_AIR_ICIS_AIR_POLLUTANTS

rows 978.4K  columns 10  scan 3.0s

roles: audit 2, category 2, other 4, who 2

## who

POLLUTANT_DESC by rows
    142.2K  FACIL
    131.7K  VOLATILE ORGANIC COMPOUNDS (VOCS)
     86.9K  TOTAL PARTICULATE MATTER
     77.3K  Carbon monoxide
     75.0K  NITROGEN OXIDES NO2
     65.2K  PARTICULATE MATTER < 10 UM
     54.3K  Sulfur dioxide
     49.7K  TOTAL HAZARDOUS AIR POLLUTANTS (HAPS)
     26.3K  Formaldehyde
     13.2K  OTHER
     12.7K  PARTICULATE MATTER < 2.5 UM
     11.8K  NITROGEN OXIDES
     11.2K  VISIBLE EMISSIONS
     10.6K  CFC (CHLOROFLUOROCARBONS)
     10.4K  Benzene
      9.7K  Tetrachloroethylene
      9.6K  Toluene
      9.3K  ADMIN
      9.3K  POLLUTANT X
      8.6K  Xylene

CHEMICAL_ABSTRACT_SERVICE_NMBR by rows
     77.3K  630080
     75.0K  10102440
     54.3K  7446095
     26.3K  50000
     11.8K  11104931
     10.6K  75718
     10.4K  71432
      9.7K  127184
      9.6K  108883
      8.6K  1330207
      7.2K  110543
      7.0K  100414
      6.3K  7439921
      4.0K  7783064
      3.9K  75070
      3.7K  67561
      3.5K  308067530
      2.6K  107028
      2.5K  540841
      2.5K  1332214

## what

AIR_POLLUTANT_CLASS_CODE: MIN 64%, SMI 14%, MAJ 10%, UNK 7%, NAP 3%, OTH 0%

AIR_POLLUTANT_CLASS_DESC: Minor Emissions 64%, Synthetic Minor Emissions 14%, Major Emissions 10%, Emissions classification unkno 7%, Not applicable 3%, Other 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PGM_SYS_ID | other | 261.9K | 0 | MN0000002700300238 1.5K; MN0000002701500010 1.5K; LA0000002205900084 1.5K; MN0000002708500002 1.5K |
| POLLUTANT_CODE | other | 663 | 0 | 300000329 142.2K; 300000243 131.7K; 300000322 86.9K; 10193 77.3K |
| POLLUTANT_DESC | who | 657 | 0 | FACIL 142.2K; VOLATILE ORGANIC COMPOUND 131.7K; TOTAL PARTICULATE MATTER 86.9K; Carbon monoxide 77.3K |
| SRS_ID | other | 589 | 165.6K | 761346 132.4K; 1647643 86.9K; 65052 77.3K; 167924 75.0K |
| CHEMICAL_ABSTRACT_SERVICE_NMBR | who | 537 | 587.8K | 630080 77.3K; 10102440 75.0K; 7446095 54.3K; 50000 26.3K |
| AIR_POLLUTANT_CLASS_CODE | category | 6 | 0 | MIN 630.9K; SMI 140.9K; MAJ 100.4K; UNK 73.3K |
| AIR_POLLUTANT_CLASS_DESC | category | 6 | 0 | Minor Emissions 630.9K; Synthetic Minor Emissions 140.9K; Major Emissions 100.4K; Emissions classification  73.3K |
| _INGESTED_AT | audit | 1 | 0 | 1785966149218673 978.4K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 28d6a611-2056-4910-8d3c-b 978.4K |
| _SRC_SHA256 | other | 1 | 0 | 9d42f3e7540b35ce680d44dce 978.4K |
