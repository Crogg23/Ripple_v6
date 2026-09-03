# PORTAL_CKA_HOUSTON_OPEN_DAT_AB35BB6552

rows 10.0K  columns 24  scan 3.4s

roles: audit 2, category 7, date 4, id 1, other 4, who 7

## when

IN_DATE
  2011     10.0K  ##############################

DUE_DATE
  2011      9.9K  ##############################
  2012       132  
  2015         1  
  2020         2  

OUT_DATE
  2011      9.8K  ##############################
  2012       199  #

INGESTED_AT
  2026     10.0K  ##############################

## who

STREET_NAME by rows
      1.4K   CARR ST  
      1.3K   RIESNER ST  
       154   EVELLA ST  
        71   COCHRAN   
        62   TRAVIS ST  
        55   EVELLA   
        54   SHERMAN ST  
        53   LINK RD  
        52   ASHEBURTON SPRING   
        46   GALVESTON RD  
        41   GRACELAND ST  
        35   LEY RD  
        31   HOFFMAN   
        29   LAWNDALE   
        28   GRIGGS RD  
        26   GLENWOOD DR  
        22   TERRY   
        22   FLEMING DR  
        21   JOPLIN   
        19   ARLINGTON ST  

LAT by rows
      1.4K     29.7913536
      1.3K     29.76620399999999
       209     29.790671
        89     29.7601927
        82  NA
        62     29.7556592
        62     29.82256599999999
        53     29.80744
        52     29.7340675
        45     29.6752744
        41     29.832233
        41     29.80847
        27     29.763264
        21     29.68871
        19     29.802715
        18     29.728008
        17     29.778133
        17     29.780926
        16     29.717274
        15     29.803654

LONG by rows
      1.4K   -95.3437477
      1.3K   -95.370111
       209   -95.343581
        89   -95.36938959999999
        82  NA
        62   -95.356453
        62   -95.36741099999999
        53   -95.374045
        52   -95.2901213
        45   -95.24689149999999
        41   -95.359775
        41   -95.27286699999999
        27   -95.4219619
        21   -95.285365
        19   -95.353652
        18   -95.28833999999999
        17   -95.29910520000001
        17   -95.39428699999999
        16   -95.525395
        15   -95.318951

BREED by rows
      3.0K  PIT BULL
      1.8K  LABRADOR RETR
      1.2K  GERM SHEPHERD
       600  CHIHUAHUA SH
       265  CHOW CHOW
       243  ROTTWEILER
       192  BOXER
       184  DACHSHUND
       120  BORDER COLLIE
       101  AUST CATTLE DOG
        98  POODLE MIN
        92  BEAGLE
        90  AM PIT BULL TER
        89  SCHNAUZER MIN
        72  GOLDEN RETR
        65  COCKER SPAN
        64  POINTER
        64  NORFOLK TERRIER
        60  CATAHOULA
        60  CHIHUAHUA LH

## who x when

STREET_NAME by DUE_DATE
   ARLINGTON ST                             2011:19
   ASHEBURTON SPRING                        2011:52
   CARR ST                                  2011:1.4K 2012:11 2020:1
   COCHRAN                                  2011:71
   EVELLA                                   2011:53 2012:2
   EVELLA ST                                2011:154
   FLEMING DR                               2011:22
   GALVESTON RD                             2011:46
   GLENWOOD DR                              2011:26
   GRACELAND ST                             2011:41
   GRIGGS RD                                2011:27 2012:1
   HOFFMAN                                  2011:31
   JOPLIN                                   2011:21
   LAWNDALE                                 2011:26 2012:3
   LEY RD                                   2011:35
   LINK RD                                  2011:53
   RIESNER ST                               2011:1.3K 2012:28
   SHERMAN ST                               2011:53 2012:1
   TERRY                                    2011:22
   TRAVIS ST                                2011:61 2012:1

LAT by DUE_DATE
     29.6752744                             2011:45
     29.68871                               2011:21
     29.717274                              2011:16
     29.728008                              2011:18
     29.7340675                             2011:51 2012:1
     29.7556592                             2011:61 2012:1
     29.7601927                             2011:89
     29.763264                              2011:27
     29.76620399999999                      2011:1.3K 2012:28
     29.778133                              2011:17
     29.780926                              2011:17
     29.790671                              2011:207 2012:2
     29.7913536                             2011:1.4K 2012:11 2020:1
     29.802715                              2011:19
     29.803654                              2011:15
     29.80744                               2011:53
     29.80847                               2011:41
     29.82256599999999                      2011:62
     29.832233                              2011:41
  NA                                        2011:82

## what

TOT: 1 99%, 2 0%, 5 0%, 4 0%, 9 0%, 6 0%, 3 0%, 10 0%, 7 0%, 8 0%, 13 0%, 14 0%

IN_TYPE: STRAY 55%, OWNER SUR 26%, CONFISCATE 10%, FOSTER 5%, EUTH REQ 2%, RETURN 1%, DISPO REQ 1%, TRANSFER 0%

IN_SUB: OTC 43%, FIELD 42%, BITE 7%, CITIZENTUR 4%, POLICE 1%, ADOPTION 1%, CRUELTY 1%, EVICTION 0%, NIGHT 0%, OWNER DIED 0%, OTC OWNED 0%

CONDITION: NORMAL 47%, CONDMINOR 21%, CONDSEVER 10%, UNDRAGEWT 5%, BEHMANAGE 5%, ILLSEVERE 3%, INJMINOR 2%, INJSEVERE 2%, ILLMINOR 2%, DEAD 2%, AGGRESSIVE 2%, BEHSEVERE 1%

OUT_TYPE: EUTH 51%, ADOPTION 21%, TRANSFER 10%, FOSTER 8%, RTO 7%, DIED 2%, DISPOSAL 1%, MISSING 0%, LOST EXP 0%

OUT_SUB: COND SEVER 25%, AT BARC 24%, RESCUE GRP 12%, COND MINOR 12%, HW MINOR 7%, BEH SEVERE 4%, PARVO 4%, WALKIN 4%, DISTEMPER 3%, SPACE 3%, UNDRAGE/WT 2%

AC: H 46%, TR 28%, UU 18%, TM 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 9.6K | 0 | A1049778 51; A1048710 50; A1048713 50; A1048717 50 |
| TOT | category | 13 | 0 | 1 9.9K; 2 35; 5 17; 4 13 |
| TYPE | other | 1 | 0 | DOG 10.0K |
| BREED | who | 155 | 0 | PIT BULL 3.0K; LABRADOR RETR 1.8K; GERM SHEPHERD 1.2K; CHIHUAHUA SH 600 |
| SUB_BREED | who | 85 | 3.2K | MIX 5.7K; PIT BULL 187; LABRADOR RETR 177; GERM SHEPHERD 133 |
| IN_TYPE | category | 8 | 0 | STRAY 5.5K; OWNER SUR 2.6K; CONFISCATE 1.0K; FOSTER 502 |
| IN_SUB | category | 14 | 126 | OTC 4.2K; FIELD 4.1K; BITE 734; CITIZENTUR 358 |
| CONDITION | category | 14 | 0 | NORMAL 4.6K; CONDMINOR 2.1K; CONDSEVER 995; UNDRAGEWT 520 |
| IN_DATE | date | 369 | 0 | 1/26/11 80; 1/12/11 74; 9/20/11 65; 1/4/11 65 |
| DUE_DATE | date | 391 | 0 | 1/30/11 79; 1/16/11 69; 8/8/11 64; 7/31/11 64 |
| OUT_TYPE | category | 9 | 0 | EUTH 5.1K; ADOPTION 2.1K; TRANSFER 967; FOSTER 831 |
| OUT_SUB | category | 50 | 877 | COND SEVER 1.9K; AT BARC 1.9K; RESCUE GRP 953; COND MINOR 909 |
| OUT_DATE | date | 398 | 0 | 7/22/11 66; 7/17/11 66; 12/9/11 62; 3/26/11 62 |
| ZIP | other | 83 | 93 | 77026 2.0K; 77002 1.4K; 77009 580; 77022 501 |
| STREET_NUM | other | 2.5K | 0 | 3200 1.4K; 61 1.3K; 2700 228; 3446 83 |
| STREET_NAME | who | 2.7K | 37 |  CARR ST   1.4K;  RIESNER ST   1.3K;  EVELLA ST   173;  ASHEBURTON SPRING    83 |
| AC | category | 4 | 0 | H 4.6K; TR 2.8K; UU 1.8K; TM 663 |
| DAYS | other | 93 | 0 | 0 1.8K; 5 1.4K; 4 798; 6 633 |
| ADDRESS | who | 3.7K | 0 | 3200 CARR ST 1.4K; 61 RIESNER ST 1.3K; 2700 EVELLA ST 174; 3446 ASHEBURTON SPRING 83 |
| LAT | who | 3.5K | 0 |    29.7913536 1.4K;    29.76620399999999 1.3K;    29.790671 228;    29.7601927 89 |
| LONG | who | 3.5K | 0 |  -95.3437477 1.4K;  -95.370111 1.3K;  -95.343581 228;  -95.36938959999999 89 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:50:23.69215 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 63374406-9895-40a6-b208-2 10.0K |
| SRC_SHA256 | who | 1 | 0 | 28191af9853c6220f5c0d6941 10.0K |
