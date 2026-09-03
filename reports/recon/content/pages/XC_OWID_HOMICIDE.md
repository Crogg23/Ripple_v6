# XC_OWID_HOMICIDE

rows 4.9K  columns 8  scan 3.7s

roles: amount 1, audit 2, category 2, other 1, who 2

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| HOMICIDE_RATE_PER_100_000_POPULATION | 4.9K | 0 | 3.13 | 58.26 | 138.44 | 37.9K |

## who

ENTITY by rows
        35  France
        35  Puerto Rico
        35  Romania
        34  South Korea
        34  Austria
        34  Japan
        34  Hong Kong
        34  Finland
        34  Saint Lucia
        34  Moldova
        34  Scotland
        34  Jamaica
        34  Australia
        34  Bulgaria
        34  Colombia
        34  Netherlands
        34  Mexico
        34  Spain
        34  Croatia
        34  Germany

ENTITY by dollars
        1.9K       29 rows  El Salvador
        1.6K       34 rows  Colombia
        1.5K       34 rows  Jamaica
        1.4K       31 rows  Honduras
        1.2K       29 rows  South Africa
        1.1K       31 rows  Venezuela
      969.59       30 rows  Guatemala
      837.95       34 rows  Brazil
      818.91       26 rows  Saint Kitts and Nevis
      748.97       35 rows  Puerto Rico
      742.98       23 rows  Belize
      672.14       34 rows  Saint Lucia
      671.44       31 rows  Bahamas
      649.10       29 rows  Saint Vincent and the Grenadines
      639.42       23 rows  Trinidad and Tobago
      606.67       34 rows  Mexico
      600.42       33 rows  Russia
      573.04       16 rows  United States Virgin Islands
      569.55       34 rows  Guyana
      553.68       25 rows  Latin America and the Caribbean (UN)

SRC_SHA256 by rows
      4.9K  33de85e4e3e78ae6f07db01ab906a86f806281d807b3806a2f186d920863f787

SRC_SHA256 by dollars
       37.9K     4.9K rows  33de85e4e3e78ae6f07db01ab906a86f806281d807b3806a2f186d920863

## what

YEAR: 2008 9%, 2009 9%, 2010 9%, 2012 9%, 2011 9%, 2007 9%, 2006 8%, 2019 8%, 2002 8%, 2004 8%, 2001 8%, 2013 8%

WORLD_REGION_ACCORDING_TO_OWID: Europe 31%, Asia 24%, North America 22%, Africa 11%, South America 7%, Oceania 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ENTITY | who | 232 | 0 | Venezuela 36; Uruguay 36; United States 35; Romania 35 |
| CODE | other | 209 | 513 | ROU 35; PRI 35; FRA 35; SWE 34 |
| YEAR | category | 35 | 0 | 2008 190; 2009 188; 2010 187; 2012 181 |
| HOMICIDE_RATE_PER_100_000_POPULATION | amount | 4.8K | 0 | 0 144; 6.7583313 24; 6.2162876 24; 5.0235434 24 |
| WORLD_REGION_ACCORDING_TO_OWID | category | 7 | 692 | Europe 1.3K; Asia 1.0K; North America 941; Africa 457 |
| INGESTED_AT | audit | 1 | 0 | 1782616872762124 4.9K |
| SOURCE_RUN_ID | audit | 1 | 0 | 030174c0-97b9-4f29-b1f9-7 4.9K |
| SRC_SHA256 | who | 1 | 0 | 33de85e4e3e78ae6f07db01ab 4.9K |
