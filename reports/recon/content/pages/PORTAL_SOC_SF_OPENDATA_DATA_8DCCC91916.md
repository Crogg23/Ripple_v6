# PORTAL_SOC_SF_OPENDATA_DATA_8DCCC91916

rows 1.6K  columns 15  scan 3.2s

roles: audit 4, category 3, date 4, other 3, who 4

## when

DATA_AS_OF
  2026      1.6K  ##############################

DATA_UPDATED_AT
  2026      1.6K  ##############################

DATA_LOADED_AT
  2026      1.6K  ##############################

INGESTED_AT
  2026      1.6K  ##############################

## who

LAST_NAME by rows
        11  Chan
        10  Smith
        10  Yu
         9  Perez
         8  Le
         8  Wong
         8  Gonzalez
         8  Lee
         7  Rodriguez
         7  Wu
         6  Martin
         6  Jones
         6  Martinez
         6  Williams
         6  Johnson
         6  Young
         6  Luo
         5  Ramirez
         5  Hoang
         5  Mason

FIRST_NAME by rows
        16  John
        15  Maria
        13  Jennifer
        12  Elizabeth
        11  Michelle
        10  Monica
        10  Christina
         9  Ana
         9  David
         9  Emily
         9  Andrew
         8  Veronica
         8  Kimberly
         8  Patricia
         7  Thomas
         7  Aaron
         7  Michael
         7  Annie
         7  Rachel
         7  Danielle

LANGUAGES by rows
      1.1K  nan
       220  Spanish
        38  Cantonese
        27  Chinese
        20  Cantonese; Mandarin
        18  Tagalog
        15  Russian
        14  Vietnamese
        14  Filipino
        10  Spanish; Spanish
         9  French; Spanish
         7  Japanese
         7  French
         7  Mandarin
         7  Portuguese; Spanish
         5  Korean
         5  American Sign Language
         5  German
         4  Italian
         3  Hebrew; Russian

SRC_SHA256 by rows
      1.6K  28fdeea359f468e0d545b9b836c3ec307dbfce49502c57dbe4b5776372183d45

## who x when

LAST_NAME by DATA_AS_OF
  Chan                                      2026:11
  Gonzalez                                  2026:8
  Hoang                                     2026:5
  Johnson                                   2026:6
  Jones                                     2026:6
  Le                                        2026:8
  Lee                                       2026:8
  Luo                                       2026:6
  Martin                                    2026:6
  Martinez                                  2026:6
  Mason                                     2026:5
  Perez                                     2026:9
  Ramirez                                   2026:5
  Rodriguez                                 2026:7
  Smith                                     2026:10
  Williams                                  2026:6
  Wong                                      2026:8
  Wu                                        2026:7
  Young                                     2026:6
  Yu                                        2026:10

FIRST_NAME by DATA_AS_OF
  Aaron                                     2026:7
  Ana                                       2026:9
  Andrew                                    2026:9
  Annie                                     2026:7
  Christina                                 2026:10
  Danielle                                  2026:7
  David                                     2026:9
  Elizabeth                                 2026:12
  Emily                                     2026:9
  Jennifer                                  2026:13
  John                                      2026:16
  Kimberly                                  2026:8
  Maria                                     2026:15
  Michael                                   2026:7
  Michelle                                  2026:11
  Monica                                    2026:10
  Patricia                                  2026:8
  Rachel                                    2026:7
  Thomas                                    2026:7
  Veronica                                  2026:8

## what

PROVIDER_DIRECTORY: MH 81%, SUD 19%

PROVIDER_TYPE: Other 15%, Associate Marriage Family Ther 12%, Social Worker 10%, Marriage and Family Therapist 10%, Mental Health Rehabilitation S 10%, Associate Clinical Social Work 9%, Psychiatrist 9%, Nurse 6%, Nurse Practitioner 6%, Certified Substance Use Disord 5%, Registered Substance Use Disor 5%, Psychologist 4%

CULTURAL_COMPETENCY_TRAINING: Yes 72%, No 21%, nan 7%, 08/14/2025 (Archived) 0%, 10/29/2024 (Archived) 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PROVIDER_DIRECTORY | category | 2 | 0 | MH 1.3K; SUD 302 |
| SITE_ID | other | 107 | 0 | 50 94; 61 69; 7 57; 71 57 |
| NPI | other | 1.2K | 0 | 1013429810 11; 1639549157 11; 1346918851 10; 1083979348 10 |
| LAST_NAME | who | 1.1K | 0 | Lidtke 11; Chan 11; Smith 11; Camarco 11 |
| FIRST_NAME | who | 852 | 0 | John 16; Maria 15; Jennifer 13; Elizabeth 12 |
| PROVIDER_TYPE | category | 21 | 0 | Other 212; Associate Marriage Family 162; Social Worker 142; Marriage and Family Thera 140 |
| STATE_LICENSE_NUMBER | other | 835 | 0 | nan 507; LPCC11909 9; RN95200573 8; RN514787 7 |
| LANGUAGES | who | 65 | 0 | nan 1.1K; Spanish 220; Cantonese 38; Chinese 27 |
| CULTURAL_COMPETENCY_TRAINING | category | 5 | 0 | Yes 1.1K; No 330; nan 102; 08/14/2025 (Archived) 1 |
| DATA_AS_OF | date | 2 | 0 | 2026-06-23T12:20:27.087 1.3K; 2026-06-23T12:20:29.240 302 |
| DATA_UPDATED_AT | audit date | 1 | 0 | 2026-06-23T12:21:43.663 1.6K |
| DATA_LOADED_AT | audit date | 1 | 0 | 2026-06-23T13:07:58.578 1.6K |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:44:07.03613 1.6K |
| SOURCE_RUN_ID | audit | 1 | 0 | 409f77b5-48c4-4d1f-a793-2 1.6K |
| SRC_SHA256 | who | 1 | 0 | 28fdeea359f468e0d545b9b83 1.6K |
