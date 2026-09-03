# PORTAL_SOC_COLORADO_INFORMA_46101BE391

rows 2.0K  columns 16  scan 4.0s

roles: audit 2, category 2, date 3, id 1, other 3, state 1, who 5

## when

TAXPERIODBEGINDT
  2009       147  ####
  2010       865  ##########################
  2011       988  ##############################

TAXPERIODENDDT
  2010       710  #######################
  2011       925  ##############################
  2012       365  ############

INGESTED_AT
  2026      2.0K  ##############################

## who

BUSINESSNAME1 by rows
         9  PTA COLORADO CONGRESS
         8  CHERRY CREEK SCHOOL DISTRIC PARENT TEACHER COMMUNITY COUNCIL INC
         8  CHERRY CREEK SCHOOL DISTRICT PARENT TEACHER COMMUNITY COUNCIL INC
         6  COLORADO ROCKY MOUNTAIN SCHOOL
         4  ASPEN CENTER FOR ENVIRONMENTAL STUDIES
         4  CREDIT UNIONS CHARTERED IN THE STATE OF COLORADO
         4  PUEBLO POLICE ACTIVITY LEAGUE INC
         4  ELEOS PROJECT
         4  COLORADO MINING ASSOCIATION
         3  SERVICIOS HOUSING INC
         3  IMAGINE FOUNDATION
         3  DENVER OPTIONS INC
         3  Colorado Association of Family
         3  SHERIDAN ARTS FOUNDATION
         3  Denver Broncos Charities
         3  NEIGHBOR TO NEIGHBOR INC
         3  COLORADO SEMINARY
         3  DEVELOPMENTAL PATHWAYS INC
         3  COLORADO STATE SCIENCE FAIR INC
         3  COLORADO BALLET

BUSINESSNAME2 by rows
      1.8K  nan
         8  INC
         5  FOUNDATION INC
         4  CENTER
         3  ASSOCIATION
         3  Charitable Fund
         3  Association (CSAHA)
         3  Medicine Residencies
         3  DBA STONE CREEK CHARTER SCHOOL
         3  MOUNTAINS - AFFILIATES
         3  SERVICES
         2  LEGAL ADMINISTRATORS
         2  COMMUNITY CENTER OF COLORADO
         2  MATERIALS DEALERS ASSOCIATION
         2  Fairmount Elementary PTA
         2  & Pipefitters Local 58
         2  KSJD
         2  School Inc (NAMES)
         2  STATE OF COLORADO 240 COMMUNITY
         2  Mountains Action Fund Inc

CITY by rows
       268  DENVER
       125  Denver
       108  COLORADO SPRINGS
       107  Colorado Springs
        87  ASPEN
        40  ENGLEWOOD
        38  AURORA
        37  LAKEWOOD
        36  Boulder
        36  BOULDER
        28  Centennial
        27  LITTLETON
        27  GRAND JUNCTION
        24  Aurora
        23  CENTENNIAL
        22  PUEBLO
        22  DURANGO
        20  FORT COLLINS
        19  TELLURIDE
        19  Fort Collins

ADDRESS_LINE_2 by rows
      1.9K  nan
         6  ROOM/SUITE 200
         3  ROOM/SUITE 400
         3  ROOM/SUITE 101
         3  Suite 108
         3  ROOM/SUITE 100
         2  ROOM/SUITE 150
         2  NO 530
         2  ROOM/SUITE D
         2  ROOM/SUITE 831
         2  ROOM/SUITE 350
         2  ROOM/SUITE 1312
         2  PO Box 3240
         2  3404
         2  212
         2  ROOM/SUITE 200D
         2  ROOM/SUITE 103
         2  ROOM/SUITE 102
         2  POB 249
         2  ROOM/SUITE 8

## who x when

BUSINESSNAME1 by TAXPERIODBEGINDT
  ASPEN CENTER FOR ENVIRONMENTAL STUDIES    2009:1 2010:2 2011:1
  CHERRY CREEK SCHOOL DISTRIC PARENT TEACH  2010:4 2011:4
  CHERRY CREEK SCHOOL DISTRICT PARENT TEAC  2009:1 2010:5 2011:2
  COLORADO BALLET                           2009:1 2010:1 2011:1
  COLORADO MINING ASSOCIATION               2009:1 2010:1 2011:2
  COLORADO ROCKY MOUNTAIN SCHOOL            2009:2 2010:2 2011:2
  COLORADO SEMINARY                         2009:1 2010:1 2011:1
  COLORADO STATE SCIENCE FAIR INC           2009:1 2010:1 2011:1
  CREDIT UNIONS CHARTERED IN THE STATE OF   2010:2 2011:2
  Colorado Association of Family            2009:1 2010:1 2011:1
  DENVER OPTIONS INC                        2009:1 2010:1 2011:1
  DEVELOPMENTAL PATHWAYS INC                2009:1 2010:1 2011:1
  Denver Broncos Charities                  2009:1 2010:1 2011:1
  ELEOS PROJECT                             2010:2 2011:2
  IMAGINE FOUNDATION                        2009:1 2010:1 2011:1
  NEIGHBOR TO NEIGHBOR INC                  2009:1 2010:1 2011:1
  PTA COLORADO CONGRESS                     2009:1 2010:3 2011:5
  PUEBLO POLICE ACTIVITY LEAGUE INC         2010:3 2011:1
  SERVICIOS HOUSING INC                     2009:1 2010:1 2011:1
  SHERIDAN ARTS FOUNDATION                  2009:1 2010:1 2011:1

BUSINESSNAME2 by TAXPERIODBEGINDT
  & Pipefitters Local 58                    2010:1 2011:1
  ASSOCIATION                               2011:3
  Association (CSAHA)                       2009:1 2010:1 2011:1
  CENTER                                    2010:1 2011:3
  COMMUNITY CENTER OF COLORADO              2010:1 2011:1
  Charitable Fund                           2009:1 2010:1 2011:1
  DBA STONE CREEK CHARTER SCHOOL            2009:1 2010:1 2011:1
  FOUNDATION INC                            2009:2 2010:1 2011:2
  Fairmount Elementary PTA                  2010:1 2011:1
  INC                                       2009:1 2010:2 2011:5
  KSJD                                      2009:1 2010:1
  LEGAL ADMINISTRATORS                      2010:1 2011:1
  MATERIALS DEALERS ASSOCIATION             2010:1 2011:1
  MOUNTAINS - AFFILIATES                    2009:1 2010:1 2011:1
  Medicine Residencies                      2009:1 2010:1 2011:1
  Mountains Action Fund Inc                 2010:1 2011:1
  SERVICES                                  2010:2 2011:1
  STATE OF COLORADO 240 COMMUNITY           2010:1 2011:1
  School Inc (NAMES)                        2009:1 2010:1
  nan                                       2009:131 2010:779 2011:871

## where

PROVINCE: CO 1.9K, MN 16, CA 15, WI 13, NY 9, TX 7, AZ 5, VA 5, FL 5, OR 4, IL 4, DC 4

## what

TAXYR: 2011 49%, 2010 43%, 2009 7%

RETURNTYPECD: 990 66%, 990EZ 34%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 2.0K | 0 | 201221799349300122 10; 201220739349200722 10; 201202489349300510 10; 201242899349200644 10 |
| TAXYR | category | 3 | 0 | 2011 988; 2010 865; 2009 147 |
| EIN | other | 1.4K | 0 | 841303335 10; 841446075 10; 841605076 10; 840705818 10 |
| BUSINESSNAME1 | who | 1.4K | 0 | PTA COLORADO CONGRESS 11; LEAVE NO TRACE CENTER FOR 10; PROFESSIONAL WILD HORSE R 10; Families of Homicide Vict 10 |
| ADDRESS_LINE_1 | other | 1.4K | 0 | 1510 17th Street 17; 325 INVERNESS DRIVE SOUTH 12; 1 OLYMPIC PLAZA 11; BOX 762 11 |
| CITY | who | 284 | 0 | DENVER 268; Denver 125; COLORADO SPRINGS 108; Colorado Springs 107 |
| POSTAL_CODE | other | 545 | 0 | 80112 44; 81611 43; 81612 43; 80203 34 |
| PROVINCE | state | 30 | 0 | CO 1.9K; MN 16; CA 15; WI 13 |
| TAXPERIODBEGINDT | date | 35 | 0 | 2011-01-01T00:00:00.000 622; 2010-01-01T00:00:00.000 562; 2011-07-01T00:00:00.000 206; 2010-07-01T00:00:00.000 172 |
| TAXPERIODENDDT | date | 33 | 0 | 2011-12-31T00:00:00.000 623; 2010-12-31T00:00:00.000 562; 2012-06-30T00:00:00.000 207; 2011-06-30T00:00:00.000 173 |
| RETURNTYPECD | category | 2 | 0 | 990 1.3K; 990EZ 679 |
| ADDRESS_LINE_2 | who | 73 | 0 | nan 1.9K; ROOM/SUITE 200 6; ROOM/SUITE 100 3; ROOM/SUITE 101 3 |
| BUSINESSNAME2 | who | 154 | 0 | nan 1.8K; INC 8; FOUNDATION INC 5; CENTER 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:42:40.93221 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 3edf03e3-a200-4c8b-b99e-f 2.0K |
| SRC_SHA256 | who | 1 | 0 | 19e05055b8d839dcf80049ade 2.0K |
