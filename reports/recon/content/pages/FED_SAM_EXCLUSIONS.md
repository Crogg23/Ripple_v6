# FED_SAM_EXCLUSIONS

rows 10.0K  columns 24  scan 2.7s

roles: audit 2, category 6, empty 2, other 4, state 1, who 9

## who

ENTITY_NAME by rows
         5  Lucas Shane Hough
         5  Derek DeShaunn Turner
         5  CARTOUCHE CORP
         5  James Thomas Estrello Jr.
         5  Antwan Nicholas Broughton
         5  Luis Ernesto Cerrillo
         5  Cole Lee Smith
         5  Lashonda Renee Brown
         5  Marion Earl Simpson Jr.
         4  Calvin Lamont Long
         4  Stephen Leon Medina
         4  Rafael Andres Esis-Marquez
         4  Jonathan  Cardenas
         4  Phillip  McBride
         4  Shane Edward Dispennett
         4  Lester  Brown
         4  Brandon Lee Blum
         4  Raymond  Rodriguez
         4  Jennifer Dawn York
         4  Rosalind  Horton

LAST_NAME by rows
        76  Williams
        58  Brown
        53  Smith
        50  Johnson
        50  Garcia
        44  Davis
        39  Martinez
        38  Rodriguez
        38  Jones
        37  Jackson
        37  Hernandez
        33  Bates
        32  Howard
        26  Tucker
        25  Lee
        23  Miller
        22  Augustine
        22  Harris
        22  Wallace
        19  Kim

FIRST_NAME by rows
        99  Michael
        82  Robert
        73  Christopher
        73  John
        72  James
        62  David
        50  Daniel
        48  Joseph
        45  Mark
        43  Richard
        41  Anthony
        40  Jose
        38  Thomas
        36  Kevin
        34  Brandon
        31  Jason
        31  Scott
        31  Kenneth
        31  Charles
        30  Luis

MIDDLE_NAME by rows
       116  L.
        76  Lee
        73  A.
        61  J.
        58  M.
        55  C.
        49  D.
        49  R.
        45  E.
        43  Edward
        40  Wayne
        38  S.
        38  Lynn
        35  B.
        34  Anthony
        32  A
        32  Michael
        31  T.
        31  James
        29  Marie

## where

STATE: TX 2.2K, FL 851, CA 752, GA 476, VA 430, MI 413, OK 368, NY 350, NC 323, LA 284, PA 280

## what

NPI: 0000000000 86%, 1801000518 2%, 1538276803 2%, 1821279258 2%, 1336247337 2%, 1043470370 2%, 1134171697 2%, 1154300812 2%, 1578779336 2%, 1659452118 2%

PREFIX: Mr. 42%, Dr. 17%, Ms. 15%, Mr.  8%, Mr 6%, Ms 5%, Ms.  3%,  Mr. 2%, #BF7843 1%, DO 1%

SUFFIX: Jr. 61%, Sr. 15%, III 7%, Ph.D. 3%, II 3%, 3rd 3%, IV 2%, Jr 2%, JR 2%, 2nd 2%

CLASSIFICATION: Individual 76%, Firm 15%, Special Entity Designation 9%, Vessel 0%

EXCLUSION_TYPE: Ineligible (Proceedings Comple 81%, Ineligible (Proceedings Comple 10%, Prohibition/Restriction 8%, Ineligible (Proceedings Pendin 1%, Voluntary Exclusion 1%

EXCLUSION_PROGRAM: Reciprocal 100%, NonProcurement 0%, Procurement 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| UEI | other | 3.2K | 6.5K | FSZWKNTGDPT5 18; TF18AUDJAMV3 18; HSJJVJNY2M31 18; HYLCXCSE1KM3 18 |
| CAGE | other | 221 | 9.8K | L0KT7 3; L0FX9 3; 87PR5 3; 6T4W3 3 |
| NPI | category | 33 | 9.9K | 0000000000 57; 1801000518 1; 1538276803 1; 1821279258 1 |
| ENTITY_NAME | who | 9.2K | 0 | Aleksandr Gennadievich  R 50; Eric Gregory Russell 50; Carlos   Scott 50; MARILYN DENISE HAYDEN 50 |
| FIRST_NAME | who | 3.2K | 2.4K | Michael 99; Robert 82; John 73; Christopher 73 |
| MIDDLE_NAME | who | 1.5K | 6.0K | L. 116; Lee 76; A. 73; J. 61 |
| LAST_NAME | who | 4.2K | 2.4K | Williams 76; Brown 58; Smith 55; Garcia 53 |
| PREFIX | category | 24 | 9.8K | Mr. 60; Dr. 25; Ms. 21; Mr.  11 |
| SUFFIX | category | 36 | 9.7K | Jr. 180; Sr. 44; III 20; Ph.D. 10 |
| DNB_OPEN_DATA | empty | 1 | 10.0K |  |
| CLASSIFICATION | category | 4 | 0 | Individual 7.6K; Firm 1.5K; Special Entity Designatio 943; Vessel 9 |
| EXCLUSION_TYPE | category | 5 | 0 | Ineligible (Proceedings C 8.1K; Ineligible (Proceedings C 1.0K; Prohibition/Restriction 753; Ineligible (Proceedings P 92 |
| EXCLUSION_PROGRAM | category | 3 | 0 | Reciprocal 10.0K; NonProcurement 48; Procurement 1 |
| EXCLUDING_AGENCY | who | 80 | 0 | DEPARTMENT OF LABOR (OASA 1.4K; JUSTICE, DEPARTMENT OF 1.3K; Justice, United States De 1.3K; U.S. IMMIGRATION AND CUST 813 |
| ACTIVATION_DATE | empty | 1 | 10.0K |  |
| TERMINATION_DATE | who | 2.0K | 741 | 01-04-2101 145; 08-12-2029 123; 01-04-2027 119; 02-15-2027 109 |
| RECORD_STATUS | who | 1 | 0 | Active 10.0K |
| CITY | who | 2.6K | 220 | Cushing 134; Bonham 128; Dallas 127; BEAUMONT 126 |
| STATE | state | 103 | 459 | TX 2.2K; FL 851; CA 752; GA 476 |
| ZIP | other | 3.6K | 494 | 75418 228; 74023 222; 77701 172; 49022 88 |
| COUNTRY | other | 81 | 7 | USA 9.4K; SGP 61; RUS 55; CHN 45 |
| _INGESTED_AT | audit | 1 | 0 | 1787443696296183 10.0K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 6595a9bd-61b9-40ff-bc22-b 10.0K |
| _SRC_SHA256 | who | 1 | 0 | 9bd829bab19399df02fd7e721 10.0K |
