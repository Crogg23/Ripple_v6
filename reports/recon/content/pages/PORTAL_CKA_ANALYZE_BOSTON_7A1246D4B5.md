# PORTAL_CKA_ANALYZE_BOSTON_7A1246D4B5

rows 10.0K  columns 8  scan 4.6s

roles: audit 2, category 1, date 3, other 1, who 2

## when

START_DATETIME
  2024      2.4K  ###############
  2025      5.0K  ##############################
  2026      2.6K  ################
  2027         4  
  2028         1  
  2029         1  
  2032         3  
  2033         2  

STOP_DATETIME
  2021         3  
  2022         6  
  2023         7  
  2024      2.4K  ##############
  2025      5.0K  ##############################
  2026      2.6K  ################

INGESTED_AT
  2026     10.0K  ##############################

## who

ADDRESS by rows
       242  252 Huntington AV, Boston, MA 02115
       200  90 Oliver ST, Boston, MA 02110
       179  150 Oliver ST, Boston, MA 02110
       140  41 Lagrange ST, Boston, MA 02116
       135  265-285 Cambridge ST, Boston, MA 02114
       122  421 Park DR, Boston, MA 02215
       119  700 Commonwealth AV, Boston, MA 02215
       110  840 Columbus AV, Boston, MA 02120
       109  6 Avenue Louis Pasteur, Boston, MA 02115
       101  100 S Campus DR, Boston, MA 02134
       101  44 Harvard WY, Boston, MA 02163
        98  30-40 Western AV, Boston, MA 02134
        98  125 Summer ST, Boston, MA 02111
        97  34 Harvard WY, Boston, MA 02163
        96  105 Cummins HW, Boston, MA 02131
        91  115 Federal ST, Boston, MA 02110
        89  640-750 Atlantic AV, Boston, MA 02111
        87  178-180 Guest ST, Boston, MA 02135
        87  466-472 Atlantic AV, Boston, MA 02210
        82  200 Clarendon ST, Boston, MA 02116

SRC_SHA256 by rows
     10.0K  2ee63c5597d6e11482e5e47c3bedd24a55207c7a1fdbe9fe05dfa155e18e7503

## who x when

ADDRESS by START_DATETIME
  100 S Campus DR, Boston, MA 02134         2024:21 2025:53 2026:27
  105 Cummins HW, Boston, MA 02131          2024:9 2025:76 2026:11
  115 Federal ST, Boston, MA 02110          2024:51 2025:7 2026:33
  125 Summer ST, Boston, MA 02111           2025:44 2026:54
  150 Oliver ST, Boston, MA 02110           2024:43 2025:78 2026:58
  178-180 Guest ST, Boston, MA 02135        2024:1 2025:58 2026:28
  200 Clarendon ST, Boston, MA 02116        2024:33 2025:47 2026:2
  252 Huntington AV, Boston, MA 02115       2024:53 2025:128 2026:60 2027:1
  265-285 Cambridge ST, Boston, MA 02114    2024:42 2025:69 2026:24
  30-40 Western AV, Boston, MA 02134        2024:20 2025:76 2026:2
  34 Harvard WY, Boston, MA 02163           2025:35 2026:62
  41 Lagrange ST, Boston, MA 02116          2024:19 2025:118 2026:3
  421 Park DR, Boston, MA 02215             2024:38 2025:44 2026:40
  44 Harvard WY, Boston, MA 02163           2024:1 2025:39 2026:61
  466-472 Atlantic AV, Boston, MA 02210     2024:1 2025:75 2026:11
  6 Avenue Louis Pasteur, Boston, MA 02115  2024:18 2025:60 2026:31
  640-750 Atlantic AV, Boston, MA 02111     2024:28 2025:52 2026:9
  700 Commonwealth AV, Boston, MA 02215     2024:3 2025:85 2026:31
  840 Columbus AV, Boston, MA 02120         2025:39 2026:71
  90 Oliver ST, Boston, MA 02110            2024:46 2025:87 2026:67

SRC_SHA256 by START_DATETIME
  2ee63c5597d6e11482e5e47c3bedd24a55207c7a  2024:2.4K 2025:5.0K 2026:2.6K 2027:4 2028:1 2029:1 2032:3 2033:2

## what

WARD: 03 25%, 22 13%, 04 11%, 05 10%, 06 7%, 21 6%, 07 6%, 09 5%, 01 5%, 19 4%, 08 4%, 11 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| APP_NO | other | 1.4K | 0 | ERT1011837 242; ALT1473528 155; ALT1418897 145; ERT1306852 145 |
| START_DATETIME | date | 2.2K | 0 | 2024-10-26 08:00:00 87; 2024-08-10 08:00:00 86; 2024-08-17 08:00:00 86; 2024-10-12 08:00:00 85 |
| STOP_DATETIME | date | 2.9K | 4 | 2025-06-19 16:00:00 90; 2024-08-10 16:00:00 88; 2024-08-17 16:00:00 87; 2024-08-03 16:00:00 86 |
| ADDRESS | who | 1.1K | 0 | 252 Huntington AV, Boston 242; 90 Oliver ST, Boston, MA  200; 150 Oliver ST, Boston, MA 179; 41 Lagrange ST, Boston, M 144 |
| WARD | category | 22 | 0 | 03 2.1K; 22 1.1K; 04 910; 05 829 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:46:27.23867 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 8754412e-267a-42e1-8a2d-4 10.0K |
| SRC_SHA256 | who | 1 | 0 | 2ee63c5597d6e11482e5e47c3 10.0K |
