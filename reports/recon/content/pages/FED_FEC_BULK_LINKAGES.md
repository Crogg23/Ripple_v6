# FED_FEC_BULK_LINKAGES

rows 16.3K  columns 11  scan 2.1s

roles: audit 2, category 5, id 1, other 2, who 1

## who

_SRC_SHA256 by rows
     16.3K  9095bb2188b568f0e56d4b90c2182d243c059a9cce0fc15b499951e732bae5cf

## what

CAND_ELECTION_YR: 2024 40%, 2026 25%, 2022 14%, 2020 11%, 2028 2%, 2018 2%, 2025 2%, 2016 1%, 2014 1%, 2023 1%, 2012 1%, 2021 0%

FEC_ELECTION_YR: 2024 53%, 2026 47%

CMTE_TP: H 66%, P 17%, S 13%, N 3%, Q 1%, X 0%, V 0%, U 0%, O 0%, Y 0%, W 0%

CMTE_DSGN: P 90%, A 5%, U 2%, J 2%, D 0%, B 0%

CYCLE: 2024 53%, 2026 47%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CAND_ID | other | 11.5K | 0 | S8ID00092 84; S8WV00143 83; S8OR00207 83; S8MS00261 83 |
| CAND_ELECTION_YR | category | 45 | 0 | 2024 6.4K; 2026 4.0K; 2022 2.2K; 2020 1.8K |
| FEC_ELECTION_YR | category | 2 | 0 | 2024 8.6K; 2026 7.7K |
| CMTE_ID | other | 11.4K | 0 | C00915710 157; C00776807 84; C00710889 82; C00417063 82 |
| CMTE_TP | category | 11 | 0 | H 10.8K; P 2.7K; S 2.1K; N 474 |
| CMTE_DSGN | category | 7 | 8 | P 14.7K; A 838; U 395; J 327 |
| LINKAGE_ID | id | 16.5K | 0 | 260453 82; 259115 82; 259758 82; 259923 82 |
| CYCLE | category | 2 | 0 | 2024 8.6K; 2026 7.7K |
| _INGESTED_AT | audit | 1 | 0 | 1782768841118701 16.3K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 5041f4d3-b9e7-4299-8016-5 16.3K |
| _SRC_SHA256 | who | 1 | 0 | 9095bb2188b568f0e56d4b90c 16.3K |
