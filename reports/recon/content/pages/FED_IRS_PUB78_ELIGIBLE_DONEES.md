# FED_IRS_PUB78_ELIGIBLE_DONEES

rows 1.44M  columns 9  scan 4.1s

roles: audit 2, category 1, id 1, other 1, state 1, who 3

## who

LEGAL_NAME by rows
       184  American Legion Auxiliary
       181  American Legion
       137  Knights of Columbus
       117  Church of Christ
       111  First Baptist Church
        98  Little League Baseball Inc.
        79  Ancient Order of Hibernians Ladies
        76  Calvary Baptist Church
        70  Grace Baptist Church
        64  Daughters of Union Veterans of the Civil War 1861-1865
        59  Fraternal Order of Police
        56  Serra International
        55  International Association of Lions Clubs
        53  Grace Bible Church
        51  Faith Baptist Church
        47  Grace Community Church
        46  First Christian Church
        42  4-H Clubs & Affiliated 4-H Organizations
        42  Ladies Ancient Order of Hibernians Inc.
        38  Victory Baptist Church

CITY by rows
     18.3K  New York
     15.6K  Brooklyn
     14.5K  Chicago
     13.7K  Houston
     12.4K  Los Angeles
     10.8K  Washington
      9.8K  Dallas
      8.2K  Atlanta
      7.9K  Philadelphia
      6.6K  Saint Louis
      6.4K  Austin
      6.0K  San Diego
      6.0K  Miami
      5.9K  Las Vegas
      5.9K  Columbus
      5.7K  Portland
      5.4K  Pittsburgh
      5.4K  Wilmington
      5.4K  San Francisco
      5.3K  Phoenix

COUNTRY by rows
     1.43M  United States
       376  CANADA
        55  AFGHANISTAN
        45  UNITED KINGDOM
        33  ISRAEL
        30  PUERTO RICO
        25  BRITISH VIRGIN ISLANDS
        22  AUSTRALIA
        20  GEORGIA
        17  FRANCE
        12  MEXICO
        11  KENYA
        10  JAPAN
         9  NETHERLANDS
         8  ITALY
         8  GERMANY
         7  COSTA RICA
         6  UGANDA
         6  PHILIPPINES
         6  ALBANIA

## where

STATE: CA 160.3K, TX 116.2K, NY 98.6K, FL 91.0K, PA 57.3K, OH 50.8K, IL 50.7K, GA 49.3K, NC 46.2K, NJ 41.5K, MI 39.4K, VA 39.1K

## what

DEDUCTIBILITY_STATUS: PC 88%, PF 9%, EO 1%, SOUNK 1%, POF 1%, SO 1%, EO,LODGE 0%, GROUP 0%, FORGN 0%, UNKWN 0%, EO,GROUP,LODGE 0%, SONFI 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| EIN | id | 1.44M | 0 | 812927619 2.3K; 812927547 2.3K; 812927460 2.3K; 812927442 2.3K |
| LEGAL_NAME | who | 1.38M | 0 | Carlos D Coleman Ministri 2.3K; Coastal Neighbors Network 2.3K; Saint Michaels Clinics In 2.3K; Midland Community Former  2.3K |
| CITY | who | 21.9K | 30 | New York 18.4K; Brooklyn 15.6K; Chicago 14.6K; Houston 13.8K |
| STATE | state | 61 | 871 | CA 160.3K; TX 116.2K; NY 98.6K; FL 91.0K |
| COUNTRY | who | 104 | 0 | United States 1.43M; CANADA 376; AFGHANISTAN 55; UNITED KINGDOM 45 |
| DEDUCTIBILITY_STATUS | category | 27 | 0 | PC 1.26M; PF 123.3K; EO 15.6K; SOUNK 14.3K |
| _INGESTED_AT | audit | 1 | 0 | 1785965106069674 1.44M |
| _SOURCE_RUN_ID | audit | 1 | 0 | 03e1f4cc-31a4-423b-8dc3-2 1.44M |
| _SRC_SHA256 | other | 1 | 0 | bcdb1032fb69ad92286355106 1.44M |
