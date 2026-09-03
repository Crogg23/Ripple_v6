# PORTAL_SOC_UTAH_OPEN_DATA_P_55EF6EF0C6

rows 2.0K  columns 13  scan 3.6s

roles: audit 2, date 1, other 6, who 5

## when

INGESTED_AT
  2026      2.0K  ##############################

## who

LST_NM by rows
        44  Smith
        25  Anderson
        19  Williams
        18  Hansen
        17  Call
        17  Johnson
        17  Parker
        15  Brown
        15  Orr
        15  Burton
        15  Ward
        14  Carter
        14  O'brien
        13  Rock
        13  Gardner
        12  Wright
        12  Hemmersmeier
        11  Young
        11  Valadez
        10  Christensen

FRST_NM by rows
        61  Michael
        56  Robert
        47  Richard
        44  David
        38  Daniel
        36  Jeffrey
        35  James
        32  Stephen
        29  Matthew
        29  Jonathan
        26  John
        26  Steven
        26  Jason
        26  Mark
        24  Douglas
        24  Scott
        22  Brett
        21  William
        20  Tyler
        19  Christopher

SPEC by rows
       436  FAMILY MEDICINE
       192  DIAGNOSTIC RADIOLOGY
       123  PHYSICAL THERAPY
       106  PHYSICIAN ASSISTANT
        88  DERMATOLOGY
        86  INTERNAL MEDICINE
        79  ORTHOPEDIC SURGERY
        70  OPHTHALMOLOGY
        70  NURSE PRACTITIONER
        62  OPTOMETRY
        60  PODIATRY
        55  CARDIOVASCULAR DISEASE (CARDIOLOGY)
        51  ANESTHESIOLOGY
        39  GASTROENTEROLOGY
        37  UROLOGY
        36  PATHOLOGY
        26  PAIN MANAGEMENT
        24  EMERGENCY MEDICINE
        23  NEUROLOGY
        21  MEDICAL ONCOLOGY

HCPCS_DESCRIPTION by rows
        70  Insertion of needle into vein for collection of blood sample
        69  Annual wellness visit, includes a personalized prevention plan of serv
        63  Administration of influenza virus vaccine
        56  Injection beneath the skin or into muscle for therapy, diagnosis, or p
        53  Hemoglobin A1C level
        51  Automated urinalysis test
        49  Vaccine for influenza for injection into muscle
        47  Administration of pneumococcal vaccine
        46  Complete blood cell count (red cells, white blood cell, platelets), au
        44  X-ray of chest, 2 views
        42  Injection, triamcinolone acetonide, not otherwise specified, 10 mg
        38  Aspiration and/or injection of large joint or joint capsule
        32  Blood test, comprehensive group of blood chemicals
        32  Therapeutic exercise to develop strength, endurance, range of motion, 
        29  Routine electrocardiogram (EKG) using at least 12 leads with interpret
        27  Eye and medical examination for diagnosis and treatment, established p
        25  Manual (physical) therapy techniques to 1 or more regions, each 15 min
        24  Destruction of skin growth
        24  X-ray of shoulder, minimum of 2 views
        22  Eye and medical examination for diagnosis and treatment, established p

## who x when

LST_NM by INGESTED_AT  LOAD STAMP, not an event date
  Anderson                                  2026:25
  Brown                                     2026:15
  Burton                                    2026:15
  Call                                      2026:17
  Carter                                    2026:14
  Christensen                               2026:10
  Gardner                                   2026:13
  Hansen                                    2026:18
  Hemmersmeier                              2026:12
  Johnson                                   2026:17
  O'brien                                   2026:14
  Orr                                       2026:15
  Parker                                    2026:17
  Rock                                      2026:13
  Smith                                     2026:44
  Valadez                                   2026:11
  Ward                                      2026:15
  Williams                                  2026:19
  Wright                                    2026:12
  Young                                     2026:11

FRST_NM by INGESTED_AT  LOAD STAMP, not an event date
  Brett                                     2026:22
  Christopher                               2026:19
  Daniel                                    2026:38
  David                                     2026:44
  Douglas                                   2026:24
  James                                     2026:35
  Jason                                     2026:26
  Jeffrey                                   2026:36
  John                                      2026:26
  Jonathan                                  2026:29
  Mark                                      2026:26
  Matthew                                   2026:29
  Michael                                   2026:61
  Richard                                   2026:47
  Robert                                    2026:56
  Scott                                     2026:24
  Stephen                                   2026:32
  Steven                                    2026:26
  Tyler                                     2026:20
  William                                   2026:21

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NPI | other | 771 | 0 | 1104826700 17; 1174569131 16; 1114900206 16; 1063460913 16 |
| IND_PAC_ID | other | 775 | 0 | 2860305752 17; 749253680 16; 5698688828 16; 547296493 16 |
| LST_NM | who | 627 | 0 | Smith 44; Anderson 25; Hansen 20; Call 20 |
| FRST_NM | who | 394 | 0 | Michael 61; Robert 56; Richard 47; David 44 |
| SPEC | who | 58 | 0 | FAMILY MEDICINE 436; DIAGNOSTIC RADIOLOGY 192; PHYSICAL THERAPY 123; PHYSICIAN ASSISTANT 106 |
| PRAC_ST | other | 1 | 0 | UT 2.0K |
| HCPCS_CODE | other | 208 | 0 | 36415 70; G0439 69; G0008 63; 96372 56 |
| HCPCS_DESCRIPTION | who | 200 | 0 | Insertion of needle into  70; Annual wellness visit, in 69; Administration of influen 63; Injection beneath the ski 56 |
| LINE_SRVC_CNT | other | 465 | 0 | 17 51; 13 46; 15 43; 14 42 |
| BENE_CNT | other | 291 | 0 | 13 84; 11 83; 12 66; 15 60 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:45:28.36262 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 0fe78de2-45db-44ae-bfb5-7 2.0K |
| SRC_SHA256 | who | 1 | 0 | 73e7ca54be95d8aa7450b7dd7 2.0K |
