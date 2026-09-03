# XC_JCS_SCOTUS

rows 782  columns 7  scan 2.6s

roles: amount 1, audit 2, category 1, other 1, who 2

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| JCS | 782 | -0.86 | 0.23 | 0.78 | 0.79 | 64.05 |

## who

UNNAMED_0 by rows
         1  117
         1  11
         1  52
         1  60
         1  226
         1  63
         1  101
         1  162
         1  110
         1  183
         1  158
         1  113
         1  154
         1  99
         1  18
         1  5
         1  157
         1  32
         1  21
         1  19

UNNAMED_0 by dollars
        0.79        1 rows  683
        0.79        1 rows  682
        0.79        1 rows  681
        0.79        1 rows  685
        0.79        1 rows  684
        0.78        1 rows  686
        0.78        1 rows  679
        0.78        1 rows  687
        0.78        1 rows  680
        0.77        1 rows  688
        0.77        1 rows  678
        0.77        1 rows  689
        0.77        1 rows  134
        0.76        1 rows  690
        0.76        1 rows  126
        0.76        1 rows  131
        0.76        1 rows  128
        0.76        1 rows  125
        0.76        1 rows  135
        0.76        1 rows  129

_SRC_SHA256 by rows
       782  77e88171e7ec9863848a2ed54abc623fe9bd9ea5afe7dca82c9c22881e530cdb

_SRC_SHA256 by dollars
       64.05      782 rows  77e88171e7ec9863848a2ed54abc623fe9bd9ea5afe7dca82c9c22881e53

## what

JUSTICENAME: WODouglas 10%, JPStevens 9%, WJBrennan 9%, WHRehnquist 9%, HLBlack 9%, CThomas 8%, BRWhite 8%, AMKennedy 8%, AScalia 8%, SGBreyer 7%, RBGinsburg 7%, SDOConnor 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| UNNAMED_0 | who | 763 | 0 | 782 4; 781 4; 780 4; 779 4 |
| TERM | other | 87 | 0 | 1956 11; 1975 10; 1961 10; 1958 10 |
| JUSTICENAME | category | 49 | 0 | WODouglas 38; JPStevens 35; WJBrennan 34; WHRehnquist 34 |
| JCS | amount | 738 | 0 | -0.385528206825256 5; 0.217386797070503 5; -0.861323654651642 4; -0.861215770244598 4 |
| _INGESTED_AT | audit | 1 | 0 | 1782878862150794 782 |
| _SOURCE_RUN_ID | audit | 1 | 0 | a2f33224-499e-40b9-8478-3 782 |
| _SRC_SHA256 | who | 1 | 0 | 77e88171e7ec9863848a2ed54 782 |
