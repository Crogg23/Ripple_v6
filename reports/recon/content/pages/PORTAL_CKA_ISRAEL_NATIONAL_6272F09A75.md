# PORTAL_CKA_ISRAEL_NATIONAL_6272F09A75

rows 17  columns 13  scan 2.0s

roles: audit 2, category 10, date 1, who 1

## when

INGESTED_AT
  2026        17  ##############################

## who

SRC_SHA256 by rows
        17  e6ade34b45647c342eada2de15448fe81dd4c1ce534d4f4f39c3d61c2be4f1b3

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  e6ade34b45647c342eada2de15448fe81dd4c1ce  2026:17

## what

CATEGORY: בנקים רגילים 65%, בנקי חוץ 24%, חברות שרותים משותפות 6%, מוסדות כספיים 6%

BANK_CODE: 39 8%, 23 8%, 22 8%, 27 8%, 50 8%, 60 8%, 18 8%, 17 8%, 46 8%, 20 8%, 10 8%, 54 8%

BANK_NAME: SBI State Bank of India 8%, HSBC 8%, Citibank 8%, Barclays Bank PLC 8%, מרכז סליקה בנקאי בעמ 8%, אלטשולר שחם פיננשיאל סרביסס בע 8%, וואן זירו הבנק הדיגיטלי בעמ 8%, בנק מרכנתיל דיסקונט בעמ 8%, בנק מסד בעמ 8%, בנק מזרחי טפחות בעמ 8%, בנק לאומי לישראל בעמ 8%, בנק ירושלים בעמ 8%

INTERNET_ADDRESS: http://home.global.hsbc/ 9%, www.citibank.com 9%, https://www.onezerobank.com/ 9%, www.mercantile.co.il 9%, http://www.bankmassad.co.il 9%, http://www.mizrahi-tefahot 9%, http://www.bankleumi.co.il 9%, www.bankjerusalem.co.il 9%, http://www.bank-yahav.co.il 9%, http://www.bankhapoalim.co.il 9%, http://www.fibi.co.il 9%

SWIFT_CODE: SBINILITXXX 9%, hsbcilit 9%, CITIILITXXX 9%, BARCGB22 9%, DIGIILITXXX 9%, BARDILITXXX 9%, MASBILITXXX 9%, MIZBILITXXX 9%, LUMIILITXXX 9%, JERSILITXXX 9%, BYAHILI1XXX 9%

ADDRESS: זבוטינסקי 3 רג בורסת היהלומים  9%, בית אמות אטריום 9%, דרך מנחם בגין 121; מגדל עזריאל 9%, רחוב הארבעה 21 בנין פלטינום; ת 9%, דיסקונט 1 9%, אבא הילל 12 רמת גן 9%, ז'בוטינסקי 7; רמת גן 9%, קמפוס לאומי לוד 9%, הנגב 2 קרית תעופה 9%, ירמיהו 80; תד 36333; ירושלים 9%, שד' רוטשילד 50; תל אביב 9%

CITY: תל אביב -יפו 41%, רמת גן 24%, ראשון לציון 12%, חולון 6%, לוד 6%, אזור רמלה שלש 6%, ירושלים 6%

ZIP_CODE: 7574602 17%, 52520 8%, 52505 8%, 67012 8%, 64739 8%, 58858 8%, 67067 8%, 5250606 8%, 5252007 8%, 7129404 8%, 7019900 8%

TELEPHONE: 03-7565404 9%, 03-7101100 9%, 03-6842424 9%, 03-6238600 9%, 03-5111555 9%, 03-5188988 9%, 076-8044530 9%, 03-5641333 9%, 03-7559000 9%, 076-8858111 9%, 076-8096001 9%

FAX: 03-6005377 9%, 03-7101130 9%, 03-6842401 9%, 03-6238666 9%, 03-5101760 9%, 03-5188988 9%, 076-8044985 9%, 03-5602384 9%, 03-7559913 9%, 076-8858360 9%, 076-8096008 9%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CATEGORY | category | 4 | 0 | בנקים רגילים 11; בנקי חוץ 4; חברות שרותים משותפות 1; מוסדות כספיים 1 |
| BANK_CODE | category | 17 | 0 | 39 1; 23 1; 22 1; 27 1 |
| BANK_NAME | category | 17 | 0 | SBI State Bank of India 1; HSBC 1; Citibank 1; Barclays Bank PLC 1 |
| INTERNET_ADDRESS | category | 13 | 5 | http://home.global.hsbc/ 1; www.citibank.com 1; https://www.onezerobank.c 1; www.mercantile.co.il 1 |
| SWIFT_CODE | category | 15 | 3 | SBINILITXXX 1; hsbcilit 1; CITIILITXXX 1; BARCGB22 1 |
| ADDRESS | category | 14 | 4 | זבוטינסקי 3 רג בורסת היהל 1; בית אמות אטריום 1; דרך מנחם בגין 121; מגדל ע 1; רחוב הארבעה 21 בנין פלטינ 1 |
| CITY | category | 7 | 0 | תל אביב -יפו 7; רמת גן 4; ראשון לציון 2; חולון 1 |
| ZIP_CODE | category | 15 | 2 | 7574602 2; 52520 1; 52505 1; 67012 1 |
| TELEPHONE | category | 16 | 2 | 03-7565404 1; 03-7101100 1; 03-6842424 1; 03-6238600 1 |
| FAX | category | 16 | 2 | 03-6005377 1; 03-7101130 1; 03-6842401 1; 03-6238666 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:15:33.93242 17 |
| SOURCE_RUN_ID | audit | 1 | 0 | a4373c85-86af-4797-bc2a-d 17 |
| SRC_SHA256 | who | 1 | 0 | e6ade34b45647c342eada2de1 17 |
