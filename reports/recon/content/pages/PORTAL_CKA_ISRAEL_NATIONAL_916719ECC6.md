# PORTAL_CKA_ISRAEL_NATIONAL_916719ECC6

rows 1.3K  columns 10  scan 2.7s

roles: audit 2, category 4, date 1, id 1, who 3

## when

INGESTED_AT
  2026      1.3K  ##############################

## who

TRADENAMEDESC by rows
       289  Kamrab
        56  ProQuad
        53  Pentaxim
        41  Synagis (Palivizumab)
        37  BNT162b2
        34  Pneumovax
        34  Infanrix Hib IPV
        33  Vaqta 50U
        31  Boostrix
        26  Imovax Polio
        26  Verorab
        23  Engerix B Adult
        22  Typhim Vi
        22  RotaTeq
        21  Zostavax
        21  Stamaril
        20  Gardasil9
        20  Menactra
        19  Havrix 1440 Adult
        18  Nimenrix

TRADENAMECODE by rows
       289  46
        56  70
        53  121
        41  138
        37  109
        34  61
        34  39
        33  91
        31  14
        26  96
        26  36
        23  21
        22  74
        22  89
        21  152
        21  82
        20  101
        20  49
        19  28
        18  53

SRC_SHA256 by rows
      1.3K  12d155910f23c3f05205a4b4050f6ea6a0d228e1348321746da4963ac8440acb

## who x when

TRADENAMEDESC by INGESTED_AT  LOAD STAMP, not an event date
  BNT162b2                                  2026:37
  Boostrix                                  2026:31
  Engerix B Adult                           2026:23
  Gardasil9                                 2026:20
  Havrix 1440 Adult                         2026:19
  Imovax Polio                              2026:26
  Infanrix Hib IPV                          2026:34
  Kamrab                                    2026:289
  Menactra                                  2026:20
  Nimenrix                                  2026:18
  Pentaxim                                  2026:53
  Pneumovax                                 2026:34
  ProQuad                                   2026:56
  RotaTeq                                   2026:22
  Stamaril                                  2026:21
  Synagis (Palivizumab)                     2026:41
  Typhim Vi                                 2026:22
  Vaqta 50U                                 2026:33
  Verorab                                   2026:26
  Zostavax                                  2026:21

TRADENAMECODE by INGESTED_AT  LOAD STAMP, not an event date
  101                                       2026:20
  109                                       2026:37
  121                                       2026:53
  138                                       2026:41
  14                                        2026:31
  152                                       2026:21
  21                                        2026:23
  28                                        2026:19
  36                                        2026:26
  39                                        2026:34
  46                                        2026:289
  49                                        2026:20
  53                                        2026:18
  61                                        2026:34
  70                                        2026:56
  74                                        2026:22
  82                                        2026:21
  89                                        2026:22
  91                                        2026:33
  96                                        2026:26

## what

VACCINATIONCODE: 79 33%, 21 10%, 65 9%, 13 9%, 23 7%, 10 5%, 28 5%, 16 5%, 60 5%, 49 4%, 17 4%, 76 4%

VACCINATIONDESC: R-IG 33%, DTaP-IPV-Hib 10%, COVID-19 9%, HAV 9%, MMRV 7%, HBV 5%, RSV-IG 5%, infl.TIV/QIV 5%, Tdap 5%, MCV4 4%, Pneu-P-23 4%, VZV 4%

MANUFACTURERCODE: 14 23%, 23 21%, 9 18%, 18 16%, 22 9%, 48 3%, 30 2%, 5 2%, 1 1%, 29 1%, 43 1%, 7 1%

MANUFACTURERDESC: Kamada 23%, Sanofi Pasteur 21%, GSK 18%, Merck/MSD 16%, Pfizer 9%, AbbVie 3%, Moderna 2%, Biotest 2%, Abbott 1%, AstraZeneca 1%, Valneva 1%, CSL Behring 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| VACCINATIONCODE | category | 43 | 0 | 79 289; 21 87; 65 80; 13 75 |
| VACCINATIONDESC | category | 43 | 0 | R-IG 289; DTaP-IPV-Hib 87; COVID-19 80; HAV 75 |
| MANUFACTURERCODE | category | 23 | 0 | 14 289; 23 256; 9 219; 18 203 |
| MANUFACTURERDESC | category | 22 | 0 | Kamada 289; Sanofi Pasteur 256; GSK 219; Merck/MSD 203 |
| TRADENAMECODE | who | 91 | 0 | 46 289; 70 56; 121 53; 138 41 |
| TRADENAMEDESC | who | 91 | 0 | Kamrab 289; ProQuad 56; Pentaxim 53; Synagis (Palivizumab) 41 |
| BATCHNUMBER | id | 1.3K | 0 | Z29 7; Z24A 7; Z23 7; Z19 7 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:25:26.03121 1.3K |
| SOURCE_RUN_ID | audit | 1 | 0 | 9721e453-73f1-4748-b189-9 1.3K |
| SRC_SHA256 | who | 1 | 0 | 12d155910f23c3f05205a4b40 1.3K |
