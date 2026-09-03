# FED_VOTEVIEW_MEMBERS

rows 51.1K  columns 25  scan 4.2s

roles: amount 7, audit 2, category 3, empty 1, other 9, state 1, who 2

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| DIED | 41.4K | 1.8K | 1.9K | 2.0K | 2.0K | 80.06M |
| NOMINATE_DIM1 | 50.8K | -1 | -0.04 | 0.74 | 1 | 366.66 |
| NOMINATE_DIM2 | 50.8K | -1 | -0.01 | 1 | 1 | 786.74 |
| NOMINATE_LOG_LIKELIHOOD | 49.8K | -1.1K | -70.02 | -5.83 | 0 | -5.08M |
| NOMINATE_GEO_MEAN_PROBABILITY | 49.8K | 0.16 | 0.76 | 0.97 | 1 | 37.7K |
| NOKKEN_POOLE_DIM1 | 50.6K | -1 | -0.04 | 0.79 | 1 | 343.84 |

## who

BIONAME by rows
        30  DINGELL, John David, Jr.
        29  HAYDEN, Carl Trumbull
        29  BYRD, Robert Carlyle
        27  INOUYE, Daniel Ken
        27  CONYERS, John, Jr.
        27  WHITTEN, Jamie Lloyd
        26  VINSON, Carl
        26  GRASSLEY, Charles Ernest
        26  MARKEY, Edward John
        25  SMITH, Samuel
        25  CELLER, Emanuel
        25  YOUNG, Donald Edwin
        25  RAYBURN, Samuel Taliaferro
        24  KENNEDY, Edward Moore (Ted)
        24  WYDEN, Ronald Lee
        24  YATES, Sidney Richard
        24  HILL, Joseph Lister
        24  LEAHY, Patrick Joseph
        24  PATMAN, John William Wright
        24  THURMOND, James Strom

BIONAME by dollars
       13.44       21 rows  SENSENBRENNER, Frank James, Jr.
       13.32       18 rows  CRANE, Philip Miller
       12.54       19 rows  GILLETT, Frederick Huntington
       12.48       13 rows  GROSS, Harold Royce
       11.55       21 rows  REED, Daniel Alden
       11.20       20 rows  TABER, John
       10.92       14 rows  DANA, Samuel Whittlesey
       10.83       19 rows  LODGE, Henry Cabot
       10.45       19 rows  INHOFE, James Mountain
       10.32       12 rows  PAUL, Ronald Ernest
       10.14       13 rows  BRANDEGEE, Frank Bosworth
        9.80       20 rows  CURTIS, Carl Thomas
        9.66       14 rows  HOFFMAN, Clare Eugene
        9.60       20 rows  WARREN, Francis Emroy
        9.60       15 rows  GOLDWATER, Barry Morris
        9.45       15 rows  ROHRABACHER, Dana
        9.45       15 rows  HELMS, Jesse
        9.43       23 rows  CANNON, Joseph Gurney
        9.36       26 rows  GRASSLEY, Charles Ernest
        9.01       17 rows  BARTON, Joe Linus

_SRC_SHA256 by rows
     51.1K  125b07032e2e1868ee42b4b3eb6c431afc7b2f80e185ef72e9c7ac3417f5a8e3

_SRC_SHA256 by dollars
      366.66    51.1K rows  125b07032e2e1868ee42b4b3eb6c431afc7b2f80e185ef72e9c7ac3417f5

## where

STATE_ABBREV: NY 4.4K, PA 3.4K, OH 2.4K, CA 2.4K, IL 2.2K, TX 1.9K, MA 1.8K, VA 1.8K, NC 1.5K, NJ 1.4K, MI 1.4K, GA 1.4K

## what

CHAMBER: House 80%, Senate 20%, President 0%

OCCUPANCY: 0 92%, 1 4%, 2 3%, 5 0%, 3 0%, 6 0%, 4 0%, 7 0%

LAST_MEANS: 1 87%, 3 9%, 2 3%, 0 1%, 5 1%, 6 0%, 7 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CONGRESS | other | 118 | 0 | 65 569; 71 567; 111 566; 77 564 |
| CHAMBER | category | 3 | 0 | House 40.9K; Senate 10.0K; President 129 |
| ICPSR | other | 12.6K | 0 | 40707 256; 20953 256; 41111 256; 29940 256 |
| STATE_ICPSR | other | 56 | 0 | 13 4.4K; 14 3.4K; 24 2.4K; 71 2.4K |
| DISTRICT_CODE | other | 109 | 0 | 0 9.5K; 1 4.3K; 2 3.7K; 3 3.3K |
| STATE_ABBREV | state | 57 | 0 | NY 4.4K; PA 3.4K; OH 2.4K; CA 2.4K |
| PARTY_CODE | other | 56 | 0 | 100 22.9K; 200 19.3K; 13 2.0K; 29 1.2K |
| OCCUPANCY | category | 9 | 2.8K | 0 44.5K; 1 1.7K; 2 1.7K; 5 149 |
| LAST_MEANS | category | 8 | 2.8K | 1 41.8K; 3 4.1K; 2 1.6K; 0 391 |
| BIONAME | who | 12.3K | 0 | BARRASSO, John A. 256; LUMMIS, Cynthia M. 256; JOHNSON, Ron 256; BALDWIN, Tammy 256 |
| BIOGUIDE_ID | other | 12.6K | 68 | B001261 256; L000571 256; J000293 256; B001230 256 |
| BORN | other | 482 | 175 | 1947 542; 1943 486; 1942 475; 1941 448 |
| DIED | amount | 414 | 9.6K | 2019.0 465; 2021.0 451; 2003.0 433; 2024.0 375 |
| NOMINATE_DIM1 | amount | 1.6K | 223 | -0.402 268; -0.381 264; -0.396 263; 0.402 262 |
| NOMINATE_DIM2 | amount | 2.0K | 223 | 1.0 359; 0.165 263; 0.257 263; -0.183 261 |
| NOMINATE_LOG_LIKELIHOOD | amount | 49.9K | 1.2K | -12.29497 251; -31.27853 251; -33.33966 251; -68.96993 251 |
| NOMINATE_GEO_MEAN_PROBABILITY | amount | 5.5K | 1.2K | 0.98759 252; 0.9855 251; 0.96257 251; 0.9609 251 |
| NOMINATE_NUMBER_OF_VOTES | other | 1.4K | 1.2K | 836 277; 497 277; 495 272; 838 271 |
| NOMINATE_NUMBER_OF_ERRORS | other | 326 | 1.2K | 11 985; 13 977; 10 977; 12 967 |
| CONDITIONAL | empty | 1 | 51.1K |  |
| NOKKEN_POOLE_DIM1 | amount | 1.9K | 474 | 0.411 256; 0.569 256; 0.656 255; 0.909 255 |
| NOKKEN_POOLE_DIM2 | amount | 2.0K | 474 | 1.0 282; 0.289 256; 0.065 256; 0.121 256 |
| _INGESTED_AT | audit | 1 | 0 | 1782766361959825 51.1K |
| _SOURCE_RUN_ID | audit | 1 | 0 | b62bd608-093c-4076-8bb8-7 51.1K |
| _SRC_SHA256 | who | 1 | 0 | 125b07032e2e1868ee42b4b3e 51.1K |
