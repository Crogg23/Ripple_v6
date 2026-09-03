# ST_OPENSTATES_LEGISLATORS

rows 7.4K  columns 30  scan 3.7s

roles: audit 2, category 3, date 1, empty 6, id 6, other 7, state 1, who 4

## when

BIRTH_DATE
  1929         1  
  1930         1  
  1934         1  
  1936         2  #
  1937         5  #
  1938         1  
  1939         6  ##
  1940         5  #
  1941        14  ####
  1942        11  ###
  1943        16  ####
  1944        18  #####
  1945        18  #####
  1946        25  #######
  1947        44  ############
  1948        46  ############
  1949        42  ###########
  1950        64  #################
  1951        62  ################
  1952        75  ####################
  1953        60  ################
  1954        79  #####################
  1955        73  ###################
  1956       110  #############################
  1957        91  ########################
  1958       101  ###########################
  1959        80  #####################
  1960        91  ########################
  1961        95  #########################
  1962        93  ########################
  1963       114  ##############################
  1964       107  ############################
  1965        87  #######################
  1966        93  ########################
  1967        92  ########################
  1968        96  #########################
  1969        90  ########################
  1970        99  ##########################
  1971        86  #######################
  1972        98  ##########################
  1973        75  ####################
  1974        75  ####################
  1975        60  ################
  1976        69  ##################
  1977        91  ########################
  1978        95  #########################
  1979        88  #######################
  1980        80  #####################
  1981        78  #####################
  1982        83  ######################
  1983        83  ######################
  1984        75  ####################
  1985        57  ###############
  1986        65  #################
  1987        52  ##############
  1988        58  ###############
  1989        33  #########
  1990        40  ###########
  1991        35  #########
  1992        22  ######
  1993        23  ######
  1994        22  ######
  1995        21  ######
  1996        14  ####
  1997        12  ###
  1998         7  ##
  1999         8  ##
  2000         5  #
  2001         7  ##
  2002         2  #
  2003         4  #
  2004         1  
  2005         1  

## who

NAME by rows
         3  Mike Jones
         3  David Smith
         3  Mark Johnson
         2  Chris Todd
         2  Blake Johnson
         2  Tommy Wright
         2  Frank Burns
         2  Chad Perkins
         2  Frank Smith
         2  Michael Johnson
         2  Doug Smith
         2  Bill Weber
         2  Matt Lehman
         2  Will Davis
         2  Rob Clifton
         2  Luke Rankin
         2  Mike Petersen
         2  David Cannon
         2  Mike Thompson
         2  Mark Walker

FAMILY_NAME by rows
        51  Smith
        48  Johnson
        34  Jones
        33  Williams
        30  Brown
        29  Miller
        26  Davis
        25  Anderson
        24  Jackson
        23  Hall
        22  Taylor
        22  Moore
        19  White
        18  Harris
        17  Wilson
        16  Thomas
        16  Howard
        16  Scott
        15  Nelson
        15  Murphy

GIVEN_NAME by rows
       166  Mike
       136  John
        99  Mark
        96  Chris
        94  Steve
        94  David
        84  Bill
        75  Joe
        74  Jim
        69  Matt
        69  Brian
        68  Tom
        68  Jeff
        62  Dan
        59  Dave
        58  Scott
        53  Bob
        52  Paul
        50  Jason
        49  Tim

SRC_SHA256 by rows
      7.4K  b15a346109b54ed210354e37990cb0f46e3ceb8bde6e92f37c33246d656a2e17

## who x when

NAME by BIRTH_DATE
  Bill Weber                                1956:1 1969:1
  Blake Johnson                             1971:1
  Chad Perkins                              1978:1
  Chris Todd                                1966:1
  David Smith                               1962:1
  Doug Smith                                1967:1 1990:1
  Frank Burns                               1975:1
  Frank Smith                               1942:1
  Luke Rankin                               1962:1 1997:1
  Matt Lehman                               1977:1
  Michael Johnson                           1970:1
  Mike Jones                                1967:1
  Mike Petersen                             1960:1
  Mike Thompson                             1957:1 1976:1
  Rob Clifton                               1968:1
  Tommy Wright                              1948:1 1952:1
  Will Davis                                1968:1 1971:1

FAMILY_NAME by BIRTH_DATE
  Anderson                                  1948:2 1951:1 1952:1 1957:1 1961:1 1966:1 1967:1 1969:1 1972:1 1982:1 1991:1 1993:1 1996:1
  Brown                                     1947:1 1948:1 1968:1 1970:1 1973:1 1975:1 1987:2
  Davis                                     1950:1 1955:1 1959:1 1960:2 1961:1 1962:1 1963:1 1967:1 1968:1 1970:1 1971:1 1977:1 1980:1
  Hall                                      1942:1 1943:1 1963:1 1987:2
  Harris                                    1947:1 1953:1 1965:1 1973:2 1979:2 1981:1 1983:1 1984:1 1991:1 1995:1
  Howard                                    1944:1 1951:1 1961:1 1968:1 1974:1 1982:1 1983:1
  Jackson                                   1944:1 1948:1 1949:1 1950:1 1951:1 1957:2 1958:1 1966:1 1978:1 1983:2 1984:2
  Johnson                                   1949:1 1955:1 1956:1 1957:1 1958:1 1960:1 1962:2 1963:1 1965:1 1968:2 1970:2 1971:3 1972:1 1974:1 1978:1 1985:1 1988:1 1995:1
  Jones                                     1947:1 1952:1 1954:1 1956:1 1958:1 1959:1 1962:1 1965:2 1967:2 1968:1 1969:1 1971:2 1974:1 1976:1 1978:1 1983:1 1984:1 1987:1 1995:1
  Miller                                    1952:1 1954:2 1961:1 1970:3 1973:1 1983:1 1990:1
  Moore                                     1948:1 1963:1 1965:1 1972:1 1984:1 1989:1
  Murphy                                    1954:1 1957:1 1960:1 1962:1 1969:1 1975:1
  Nelson                                    1953:1 1957:1 1958:1 1968:1 1979:1 1985:1
  Scott                                     1945:1 1952:1 1956:1 1961:1 1965:1 1976:1 1981:1 1982:1 1984:1 2001:1
  Smith                                     1941:1 1942:1 1944:1 1945:1 1947:1 1951:1 1952:1 1955:1 1958:2 1960:2 1962:1 1964:1 1965:1 1966:1 1967:2 1968:2 1969:1 1970:1 1971:1 1973:1 1974:1 1977:1 1980:1 1981:1 1982:1 1983:1 1990:2 1991:1
  Taylor                                    1946:1 1950:1 1957:1 1961:1 1964:2 1965:1 1968:1 1973:2 1975:1
  Thomas                                    1949:1 1952:1 1953:1 1963:1 1974:1 1979:1 1993:1
  White                                     1945:1 1948:1 1950:1 1952:1 1959:1 1962:1 1969:1 1972:1 1975:1 1984:1 1988:1
  Williams                                  1947:1 1952:2 1955:1 1956:1 1957:1 1960:1 1964:1 1965:1 1966:1 1968:1 1970:1 1972:1 1973:1 1974:1 1975:1 1977:1 1979:1 1980:1 1983:1 1990:1 1991:1
  Wilson                                    1950:1 1951:1 1964:2 1972:1 1976:1 1982:1 1990:1 1992:1

## where

JURISDICTION: NH 411, PA 253, GA 235, NY 213, MN 200, MA 197, MO 191, MD 188, ME 188, CT 187, VT 180, TX 179

## what

CURRENT_PARTY: Republican 54%, Democratic 41%, Democratic-Farmer-Labor 1%, Democratic/Working Families 1%, Partido Nuevo Progresista 1%, Nonpartisan 1%, Republican/Conservative 0%, Independent 0%, Partido Popular Democrático 0%, Republican/Conservative/Indepe 0%, Democratic/Progressive 0%, Partido Independentista Puerto 0%

CURRENT_CHAMBER: lower 73%, upper 26%, legislature 1%

GENDER: Male 66%, Female 34%, X 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 7.6K | 0 | ocd-person/ab4e4bba-4cbb- 38; ocd-person/d32dffc7-d1f4- 38; ocd-person/e99c49b9-28da- 38; ocd-person/4c98369a-5291- 38 |
| NAME | who | 7.3K | 0 | Ángel Toledo López 38; Ángel Peña Ramírez 38; Ángel Morey Noble 38; Ángel Fourquet 38 |
| CURRENT_PARTY | category | 17 | 0 | Republican 4.0K; Democratic 3.1K; Democratic-Farmer-Labor 101; Democratic/Working Famili 64 |
| CURRENT_DISTRICT | other | 890 | 0 | 6 102; 5 102; 8 101; 3 101 |
| CURRENT_CHAMBER | category | 3 | 0 | lower 5.4K; upper 1.9K; legislature 62 |
| GIVEN_NAME | who | 1.9K | 2 | Mike 166; John 136; Mark 99; Chris 96 |
| FAMILY_NAME | who | 5.1K | 0 | Smith 52; Johnson 48; González 39; Román 38 |
| GENDER | category | 3 | 0 | Male 4.9K; Female 2.5K; X 15 |
| EMAIL | id | 7.3K | 12 | atoledo@senado.pr.gov 38; anpena@camara.pr.gov 38; amorey@camara.pr.gov 38; afourquet@camara.pr.gov 38 |
| BIOGRAPHY | empty | 1 | 7.4K |  |
| BIRTH_DATE | date | 3.4K | 3.7K | 1957-10-14 20; 1958-05-21 20; 1978-04-13 19; 1946-12-27 19 |
| DEATH_DATE | empty | 1 | 7.4K |  |
| IMAGE | id | 6.9K | 442 | https://www.camara.pr.gov 36; https://www.camara.pr.gov 36; https://www.camara.pr.gov 36; https://www.camara.pr.gov 36 |
| LINKS | id | 7.3K | 3 | https://www.senado.pr.gov 38; https://camara.registrok1 38; https://camara.registrok1 38; https://camara.registrok1 38 |
| SOURCES | id | 7.5K | 0 | https://api.oregonlegisla 75; https://ballotpedia.org/% 37; https://ballotpedia.org/% 37; https://ballotpedia.org/% 37 |
| CAPITOL_ADDRESS | empty | 1 | 7.4K |  |
| CAPITOL_VOICE | empty | 1 | 7.4K |  |
| CAPITOL_FAX | empty | 1 | 7.4K |  |
| DISTRICT_ADDRESS | other | 2.0K | 5.2K | UT 42; WV 35; MA 23; 1500 W. Benson Blvd., Anc 21 |
| DISTRICT_VOICE | id | 1.8K | 5.6K | 401-276-5568 11; 202-724-8028 10; 202-724-8045 10; 202-724-8174 10 |
| DISTRICT_FAX | other | 88 | 7.3K | 732-383-5116 3; 202-724-8076 1; 202-724-8055 1; 972-722-3132 1 |
| TWITTER | other | 703 | 6.7K | RepTitoFourquet 4; lisieburgospr 4; connyvarelarep 4; HectorFerrerPR 4 |
| YOUTUBE | other | 94 | 7.3K | UCdBkDQL4ync9p-qbvbNENkg 1; RepPickett 1; playlist?list=PL6C0B99856 1; playlist?list=PL4F4B6A26E 1 |
| INSTAGRAM | other | 305 | 7.1K | angelfourquet/?hl=es 2; connyvarelarep/ 2; hectorferrerpr/ 2; reptreysherwood 2 |
| FACEBOOK | other | 819 | 6.6K | angelpenajr 5; angeltito.fourquetcordero 5; RepresentanteYashiraLebro 5; jrperezortiz 5 |
| WIKIDATA | empty | 1 | 7.4K |  |
| JURISDICTION | state | 52 | 0 | NH 411; PA 253; GA 235; NY 213 |
| INGESTED_AT | audit | 1 | 0 | 1788309208392828 7.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | f22d9001-8ba6-4204-9d05-e 7.4K |
| SRC_SHA256 | who | 1 | 0 | b15a346109b54ed210354e379 7.4K |
