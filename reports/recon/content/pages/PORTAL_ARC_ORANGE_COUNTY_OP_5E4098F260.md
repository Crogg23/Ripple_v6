# PORTAL_ARC_ORANGE_COUNTY_OP_5E4098F260

rows 63  columns 34  scan 5.2s

roles: amount 2, audit 2, category 14, date 1, empty 1, other 10, who 5

## when

INGESTED_AT
  2026        63  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITIUDE | 63 | 33.46 | 33.46 | 33.46 | 33.46 | 2.1K |
| LONGITUDE | 63 | -117.71 | -117.70 | -117.69 | -117.69 | -7.4K |

## who

BUSINESS_N by rows
         1  Super Stop Liquor
         1  Riviera Charters
         1  Dana Point Jet Ski / Kayak Center
         1  Turk's
         1  Dream Catcher Yachts
         1  The Country Fox
         1  Dana Point Yacht Club (vessel dry storage)
         1  Sun Country Marine
         1  Dana Point Shipyard (Industrial)
         1  Embarcadero Marina
         1  El Torito (#7155)
         1  Raj Parfumerie
         1  Airtouch (Verizon)
         1  Gemmell's Restaurant
         1  Dana Point Yacht Club
         1  Nordhavn (associated with Pacific Asian Enterprises)
         1  Upstairs Store
         1  Top Brass
         1  Dana Point Marina Inn
         1  Dolphin Safari

BUSINESS_N by dollars
       33.46        1 rows  Dana Point Jet Ski / Kayak Center
       33.46        1 rows  Mariner's Yacht & Ship Brokerage (formerly Marine Tech)
       33.46        1 rows  Dana Point Shipyard (Industrial)
       33.46        1 rows  Nordhavn (associated with Pacific Asian Enterprises)
       33.46        1 rows  Sun Country Marine
       33.46        1 rows  Aventura Sailing Association & Dining Hall
       33.46        1 rows  Beach Harbor Pizza
       33.46        1 rows  White Pelican Gallery
       33.46        1 rows  Harbor Grill
       33.46        1 rows  Dana West Yacht Club
       33.46        1 rows  Bella Sea (formerly Catalina Seashell Company)
       33.46        1 rows  Slice of New York (formerly Hava Java)
       33.46        1 rows  Woody Hut
       33.46        1 rows  Catalina Channel Express
       33.46        1 rows  Brig Restaurant, The
       33.46        1 rows  Golden Galleon Boutique
       33.46        1 rows  Super Stop Liquor
       33.46        1 rows  Pacific Asian Enterprises
       33.46        1 rows  El Torito (#7155)
       33.46        1 rows  Dana West Marina

BUSINESS_1 by rows
         1  El Torito #7155
         1  Dana Point Marina Inn
         1  White Pelican Gallery
         1  Riviera Charters
         1  Jon's Fish Market
         1  Slice of New York
         1  Turk's
         1  Harpoon Henry's
         1  Nordhavn
         1  Dana Point Yacht Club (vessel dry storage)
         1  Pacific Asian Enterprises
         1  Dana Point Shipyard
         1  DaVine Food &amp; Wine
         1  Aventura Sailing Association &amp; Dining Hall
         1  Dana Point Jet Ski / Kayak Center
         1  Capo Beach Watercraft
         1  Downstairs Store
         1  Spring
         1  Sea Styles
         1  Harbor Grill

BUSINESS_1 by dollars
       33.46        1 rows  Art Sea
       33.46        1 rows  Harbor Jewelry
       33.46        1 rows  Gift Chateau
       33.46        1 rows  Turk's
       33.46        1 rows  Momilani's Island Traditions
       33.46        1 rows  Wind and Sea Restaurant
       33.46        1 rows  Verizon Cell Tower
       33.46        1 rows  Parcel 11
       33.46        1 rows  Embarcadero Marina
       33.46        1 rows  Spring
       33.46        1 rows  Slice of New York
       33.46        1 rows  Ocean Institute
       33.46        1 rows  The Scoop Deck
       33.46        1 rows  Aventura Sailing Association &amp; Dining Hall
       33.46        1 rows  Mariner's Yacht &amp; Ship Brokerage
       33.46        1 rows  Bella Sea
       33.46        1 rows  Chocolate Soldier
       33.46        1 rows  Super Stop Liquor
       33.46        1 rows  Beach Harbor Pizza
       33.46        1 rows  Upstairs Store

WATERSHED by rows
        63  Dana Point Coastal Streams

WATERSHED by dollars
        2.1K       63 rows  Dana Point Coastal Streams

CITY by rows
        63  Dana Point

CITY by dollars
        2.1K       63 rows  Dana Point

## who x when

BUSINESS_N by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITIUDE
  Airtouch (Verizon)                        2026:33.46
  Aventura Sailing Association & Dining Ha  2026:33.46
  Beach Harbor Pizza                        2026:33.46
  Bella Sea (formerly Catalina Seashell Co  2026:33.46
  Catalina Channel Express                  2026:33.46
  Dana Point Jet Ski / Kayak Center         2026:33.46
  Dana Point Marina Inn                     2026:33.46
  Dana Point Shipyard (Industrial)          2026:33.46
  Dana Point Yacht Club                     2026:33.46
  Dana Point Yacht Club (vessel dry storag  2026:33.46
  Dana West Yacht Club                      2026:33.46
  Dolphin Safari                            2026:33.46
  Dream Catcher Yachts                      2026:33.46
  El Torito (#7155)                         2026:33.46
  Embarcadero Marina                        2026:33.46
  Gemmell's Restaurant                      2026:33.46
  Harbor Grill                              2026:33.46
  Mariner's Yacht & Ship Brokerage (former  2026:33.46
  Nordhavn (associated with Pacific Asian   2026:33.46
  Raj Parfumerie                            2026:33.46
  Riviera Charters                          2026:33.46
  Slice of New York (formerly Hava Java)    2026:33.46
  Sun Country Marine                        2026:33.46
  Super Stop Liquor                         2026:33.46
  The Country Fox                           2026:33.46
  Top Brass                                 2026:33.46
  Turk's                                    2026:33.46
  Upstairs Store                            2026:33.46
  White Pelican Gallery                     2026:33.46
  Woody Hut                                 2026:33.46

BUSINESS_1 by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITIUDE
  Art Sea                                   2026:33.46
  Aventura Sailing Association &amp; Dinin  2026:33.46
  Capo Beach Watercraft                     2026:33.46
  DaVine Food &amp; Wine                    2026:33.46
  Dana Point Jet Ski / Kayak Center         2026:33.46
  Dana Point Marina Inn                     2026:33.46
  Dana Point Shipyard                       2026:33.46
  Dana Point Yacht Club (vessel dry storag  2026:33.46
  Downstairs Store                          2026:33.46
  El Torito #7155                           2026:33.46
  Embarcadero Marina                        2026:33.46
  Gift Chateau                              2026:33.46
  Harbor Grill                              2026:33.46
  Harbor Jewelry                            2026:33.46
  Harpoon Henry's                           2026:33.46
  Jon's Fish Market                         2026:33.46
  Momilani's Island Traditions              2026:33.46
  Nordhavn                                  2026:33.46
  Ocean Institute                           2026:33.46
  Pacific Asian Enterprises                 2026:33.46
  Parcel 11                                 2026:33.46
  Riviera Charters                          2026:33.46
  Sea Styles                                2026:33.46
  Slice of New York                         2026:33.46
  Spring                                    2026:33.46
  The Scoop Deck                            2026:33.46
  Turk's                                    2026:33.46
  Verizon Cell Tower                        2026:33.46
  White Pelican Gallery                     2026:33.46
  Wind and Sea Restaurant                   2026:33.46

## what

WDID: N/A 98%, CA0109313 2%

SIC_CODE: 9999 98%, 3732 2%

SIC_DESCRI: N/A 98%, Boat building and repairing 2%

PRIORITY: High 100%

INSPECTION: Permit Term 98%, Annually 2%

NOTES: Dana Point Harbor commercial f 40%, Dana Point Harbor commercial f 27%, Dana Point Harbor commercial f 17%, Dana Point Harbor commercial f 3%, Dana Point Harbor commercial f 2%, Dana Point Harbor commercial f 2%, Dana Point Harbor commercial f 2%, Dana Point Harbor commercial f 2%, Dana Point Harbor commercial f 2%, Vacant Dana Point Harbor comme 2%, Dana Point Harbor commercial f 2%, Boat maintenance facility in D 2%

DPH_FACILI: HA78H-24-003-xxxx 36%, HA78H-24-06-xx 14%, HA78H-24-20-xx 11%, Not Available 7%, HA78H-24-02-xx 7%, HA78H-24-003-0029 4%, HA78H-24-003-0027 4%, HA78H-24-003-0024 4%, HA78H-24-003-0021 4%, HA78H-24-003-0015 4%, HA78H-24-003-0010 4%, HA78H-24-003-0016 4%

FOOD_OWNER: OW0039908 25%, OW0048732 25%, OW0005822 25%, OW0003475 25%

FACILITY_T: Commercial 71%, Food 27%, Industrial 2%

STREET_NAM:  Golden Lantern 49%, Dana 14%, Golden Lantern 13%, Dana Point Harbor 10%, Puerto 6%, Embarcadero 3%, Casitas 3%, Cellular Communication 108-1 2%

STREET_TYP: Dr 50%, Pl 23%, Pl. 9%, Dr. 9%, Dr. (Bldg. E, West Basin) 5%, Dr. (Bldg 8, East Basin) 5%

CONTACT: Ken Stetson 67%, Mark Hanson 6%, Nevine Sidhom 3%, Dan Gee 3%, Dave Loesh 3%, Paul Berkery 3%, Eric Leslie 3%, Simone Costes 3%, Ralph Davidson/Dollie Van Dixh 3%, George and Diana Psilopoulos 3%, Anita Moore 3%

CONTACT_EM: cathycope@danapoint-shipyard.c 100%

PHONE_NUMB: 949-496-6177 48%, 949-248-9576 21%, 949-487-7000 3%, 949-496-2274 3%, 949-493-9493 3%, 949-661-1185 3%, 949-493-6222 3%, 949-496-2900 3%, 949-496-6113 3%, 949-240-1991 3%, 949-661-3787 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | other | 63 | 0 | 63 1; 62 1; 61 1; 60 1 |
| OBJECTID | other | 62 | 0 | 129 1; 128 1; 127 1; 126 1 |
| REGION | other | 1 | 0 | SDR 63 |
| WDID | category | 2 | 0 | N/A 62; CA0109313 1 |
| SIC_CODE | category | 2 | 0 | 9999 62; 3732 1 |
| SIC_DESCRI | category | 2 | 0 | N/A 62; Boat building and repairi 1 |
| BUSINESS_N | who | 63 | 0 | Wind and Sea Restaurant 1; Turk's 1; Super Stop Liquor 1; Slice of New York (former 1 |
| STREET_NUM | other | 56 | 0 | 34671 4; 34675 3; 34555 2; 34699 1 |
| CITY | who | 1 | 0 | Dana Point 63 |
| ZIP | other | 1 | 0 | 92629 63 |
| WATERSHED | who | 1 | 0 | Dana Point Coastal Stream 63 |
| LATITIUDE | amount | 60 | 0 | 33.461606 2; 33.459072 1; 33.459506 1; 33.461822 1 |
| LONGITUDE | amount | 61 | 0 | -117.692891 1; -117.692481 1; -117.695468 1; -117.692207 1 |
| PRIORITY | category | 2 | 62 | High 1 |
| INSPECTION | category | 2 | 0 | Permit Term 62; Annually 1 |
| WQMP | other | 1 | 0 | N 63 |
| NOTES | category | 12 | 0 | Dana Point Harbor commerc 25; Dana Point Harbor commerc 17; Dana Point Harbor commerc 11; Dana Point Harbor commerc 2 |
| DPH_FACILI | category | 47 | 0 | HA78H-24-003-xxxx 10; HA78H-24-06-xx 4; HA78H-24-20-xx 3; Not Available 2 |
| INVENTORY | other | 63 | 0 | SDR_Exist_Dev_129 1; SDR_Exist_Dev_128 1; SDR_Exist_Dev_127 1; SDR_Exist_Dev_126 1 |
| GLOBALID | other | 61 | 0 | {0E6C9A0E-069C-43D0-8930- 1; {F039F7FE-9ABF-40DA-B57E- 1; {D84FB7DC-71D7-49F2-BCB1- 1; {EFC94E81-B963-4551-B733- 1 |
| FOOD_OWNER | category | 5 | 59 | OW0039908 1; OW0048732 1; OW0005822 1; OW0003475 1 |
| FACILITY_T | category | 3 | 0 | Commercial 45; Food 17; Industrial 1 |
| BUSINESS_L | empty | 1 | 63 |  |
| BUSINESS_1 | who | 63 | 0 | Wind and Sea Restaurant 1; Turk's 1; Super Stop Liquor 1; Slice of New York 1 |
| STREET_NAM | category | 8 | 0 |  Golden Lantern 31; Dana 9; Golden Lantern 8; Dana Point Harbor 6 |
| STREET_TYP | category | 7 | 41 | Dr 11; Pl 5; Pl. 2; Dr. 2 |
| CONTACT | category | 31 | 11 | Ken Stetson 22; Mark Hanson 2; Nevine Sidhom 1; Dan Gee 1 |
| CONTACT_EM | category | 2 | 62 | cathycope@danapoint-shipy 1 |
| PHONE_NUMB | category | 41 | 5 | 949-496-6177 14; 949-248-9576 6; 949-487-7000 1; 949-496-2274 1 |
| WQMP_NUMBE | other | 1 | 0 | N/A 63 |
| GEOMETRY | other | 62 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:18:02.31622 63 |
| SOURCE_RUN_ID | audit | 1 | 0 | 3569478f-0ca7-4e40-8774-c 63 |
| SRC_SHA256 | who | 1 | 0 | 63923b1ce386ae208027ae056 63 |
