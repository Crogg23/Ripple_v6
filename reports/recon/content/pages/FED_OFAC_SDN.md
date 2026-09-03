# FED_OFAC_SDN

rows 19.1K  columns 16  scan 2.9s

roles: audit 2, category 4, id 3, other 2, who 5

## who

SDN_NAME by rows
         4  AL-AQSA FOUNDATION
         3  ATIA, Hachim K.
         2  TANGO
         2  USTINOV, Vladimir Vasilyevich
         2  SONA
         2  OKEANSKY PROSPECT
         2  JOINT STOCK COMPANY POLEMA
         2  BAZGHANDI, Rouhollah
         2  FIONA
         2  TERIBERKA
         2  NATIONAL LIBERATION ARMY
         2  AWEYS, Hassan Dahir
         2  MINISTRY OF STATE SECURITY
         2  AW-MOHAMED, Ahmed Abdi
         2  AL-HARAMAIN ISLAMIC FOUNDATION
         2  HEIDARI, Reza
         2  LIMITED LIABILITY COMPANY LEGION KOMPLEKT
         2  GLOBAL RELIEF FOUNDATION, INC.
         2  HARMONY
         2  JOINT STOCK COMPANY 103 ARSENAL

TITLE by rows
     17.9K  -0- 
       440  Member of the State Duma of the Federal Assembly of the Russian Federa
       165  Member of the Federation Council of the Federal Assembly of the Russia
        14  Vice-Chairperson, 13th National People's Congress Standing Committee
         7  State Administrative Council Member
         6  Foreign Trade Bank of the Democratic People's Republic of Korea repres
         6  Colonel
         5  Korea Ryonbong General Corporation Official
         5  Brigadier General
         4  Haji
         4  Korea United Development Bank representative
         4  Magistrate of the Constitutional Chamber of Venezuela's Supreme Court 
         3  Korea Daesong Bank representative
         3  Scientific Studies and Research Center Colonel
         3  Vice Chairman of the National Defense Commission
         3  Scientific Studies and Research Center Brigadier General
         3  IRGC Brigadier General
         3  General
         3  Aide to the President of the Russian Federation
         3  Major General

PROGRAM by rows
      5.7K  RUSSIA-EO14024
      2.2K  SDGT
      1.4K  SDNTK
       778  IRAN-EO13902
       726  GLOMAG
       608  NPWMD] [IFSR
       507  UKRAINE-EO13662] [RUSSIA-EO14024
       473  IRAN
       464  IRAN-EO13846
       455  ILLICIT-DRUGS-EO14059
       416  SDGT] [IFSR
       383  TCO
       210  NPWMD
       190  IRAQ2
       188  DPRK4
       179  BELARUS-EO14038
       173  PAARSSR-EO13894
       171  VENEZUELA-EO13850
       165  VENEZUELA
       164  BALKANS

VESS_FLAG by rows
     17.7K  -0- 
       265  Panama
       243  Russia
       188  Iran
       158  China
        73  Democratic People's Republic of Korea
        66  Barbados
        60  Liberia
        52  Palau
        38  Venezuela
        36  Cook Islands
        34  Comoros
        31  Gabon
        23  Cameroon
        21  Hong Kong
        14  San Marino
        12  Gambia
        10  Unknown
        10  Guyana
         8  Sao Tome and Principe

## what

SDN_TYPE: -0-  51%, individual 39%, vessel 8%, aircraft 2%

VESS_TYPE: -0-  94%, Crude Oil Tanker 2%, General Cargo 1%, Fishing Vessel 1%, LPG Tanker 0%, Chemical/Products Tanker 0%, Chemical/Oil Tanker 0%, Container Ship 0%, Bulk Carrier 0%, Products Tanker 0%, Oil Products Tanker 0%, Tug 0%

TONNAGE: -0-  100%, 318,000 0%, 159,681 0%, 640 0%, 317,367 0%, 317,356 0%, 164,154 0%, 298,732 0%, 299,242 0%, 299,500 0%, 99,144 0%

VESS_OWNER: -0-  100%, NITC 0%, Truong Phat Loc Shipping Tradi 0%, Beratex Group Limited 0%, Samir de Navegacion S.A. 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ENT_NUM | id | 19.2K | 0 |  96; 57973 96; 57972 96; 57971 96 |
| SDN_NAME | who | 19.2K | 1 | GENERATION CURRENCY BUREA 96; MANHATTAN BUREAU DE CHANG 96; NINE TO NINE EXCHANGE BUR 96; MUHAMMAD, Mukhtar Adamu 96 |
| SDN_TYPE | category | 5 | 1 | -0-  9.8K; individual 7.5K; vessel 1.5K; aircraft 344 |
| PROGRAM | who | 240 | 1 | RUSSIA-EO14024 5.7K; SDGT 2.2K; SDNTK 1.4K; IRAN-EO13902 778 |
| TITLE | who | 531 | 1 | -0-  17.9K; Member of the State Duma  440; Member of the Federation  165; Vice-Chairperson, 13th Na 16 |
| CALL_SIGN | other | 898 | 1 | -0-  18.2K; 3E4634 5; 3E4726 5; 3E4737 5 |
| VESS_TYPE | category | 43 | 1 | -0-  17.7K; Crude Oil Tanker 431; General Cargo 168; Fishing Vessel 149 |
| TONNAGE | category | 43 | 1 | -0-  19.1K; 318,000 5; 159,681 3; 640 3 |
| GRT | other | 80 | 1 | -0-  19.0K; 2489 6; 163,660 6; 81,479 5 |
| VESS_FLAG | who | 60 | 1 | -0-  17.7K; Panama 265; Russia 243; Iran 188 |
| VESS_OWNER | category | 6 | 1 | -0-  19.1K; NITC 3; Truong Phat Loc Shipping  1; Beratex Group Limited 1 |
| REMARKS | id | 18.2K | 1 | -0-  341; Additional Sanctions Info 165; Additional Sanctions Info 110; Secondary sanctions risk: 99 |
| IMO | id | 2.0K | 17.1K | 9131539 11; 8910897 11; 9386304 11; 9167409 11 |
| _INGESTED_AT | audit | 1 | 0 | 1782424521291621 19.1K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 25db23c4-0168-4a91-839b-0 19.1K |
| _SRC_SHA256 | who | 1 | 0 | 3d4a315bf4473cac7d951780a 19.1K |
