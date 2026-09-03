# PORTAL_CKA_WPRDC_ALLEGHENY_52A0E51ACA

rows 15  columns 8  scan 2.3s

roles: audit 2, category 5, date 1, who 1

## when

INGESTED_AT
  2026        15  ##############################

## who

SRC_SHA256 by rows
        15  64d51e33436dd52dbd931538438b7bf5d6ccdf026b861087d1091777dc5b8629

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  64d51e33436dd52dbd931538438b7bf5d6ccdf02  2026:15

## what

FIELD_NAME: holiday_exception 8%, schedule 8%, event_narrative 8%, event_phone 8%, requirements 8%, recommended_for 8%, category 8%, organization 8%, longitude 8%, latitude 8%, address 8%, neighborhood 8%

TYPE: text 87%, float 13%

DESCRIPTION: Specifies any schedule deviati 8%, When the event takes place. 8%, Description of the event. 8%, Contact phone number. 8%, Pre-requisites for the event. 8%, People who could benefit from  8%, Category or categories associa 8%, Organization behind the event. 8%, Longitude of the event's locat 8%, Latitude of the event's locati 8%, The event location's address. 8%, Neighborhood where the event t 8%

EXAMPLE: Closed during date: 2018/01/15 8%, Mon - Thurs:  11am 8%, Wellsprings recovery group mee 8%, 412-263-2545 8%, none, walk-ins welcome 8%, all those recovering from addi 8%, expert-lookup 8%, Pittsburgh Mercy Health System 8%, -79.991555 8%, 40.438492 8%, 903 Watson St, PA, 15219 8%, Uptown 8%

NOTES: Note that if there are multipl 50%, A one-on-one event is one that 50%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FIELD_NAME | category | 15 | 0 | holiday_exception 1; schedule 1; event_narrative 1; event_phone 1 |
| TYPE | category | 2 | 0 | text 13; float 2 |
| DESCRIPTION | category | 15 | 0 | Specifies any schedule de 1; When the event takes plac 1; Description of the event. 1; Contact phone number. 1 |
| EXAMPLE | category | 15 | 0 | Closed during date: 2018/ 1; Mon - Thurs:  11am 1; Wellsprings recovery grou 1; 412-263-2545 1 |
| NOTES | category | 3 | 13 | Note that if there are mu 1; A one-on-one event is one 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:08:42.05482 15 |
| SOURCE_RUN_ID | audit | 1 | 0 | 14609a47-ae1d-40e3-83d4-5 15 |
| SRC_SHA256 | who | 1 | 0 | 64d51e33436dd52dbd9315384 15 |
