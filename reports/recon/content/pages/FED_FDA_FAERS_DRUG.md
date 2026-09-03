# FED_FDA_FAERS_DRUG

rows 20.91M  columns 25  scan 12.5s

roles: amount 1, audit 2, category 7, date 2, other 7, who 7

## when

EXP_DT
  1904         2  
  1905        27  
  1906        20  
  1907        20  
  1908        27  
  1909        21  
  1910         7  
  1911         4  
  1912         2  
  1913         5  
  1914         1  
  1915         4  
  1918         1  
  1926         1  
  1931         1  
  1934         1  
  1939         1  
  1940         1  
  1941         1  
  1942         2  
  1946         1  
  1950         1  
  1951         2  
  1954         1  
  1956         1  
  1957         1  
  1972         1  
  1980         1  
  1984         3  
  1985         5  
  1986         1  
  1988         3  
  1989        23  
  1990         5  
  1991         7  
  1993         3  
  1994         8  
  1995         7  
  1996        15  
  1997        31  
  1998        82  
  1999        93  
  2000       113  
  2001       293  
  2002       296  
  2003       833  #
  2004      4.2K  #####
  2005     15.6K  ##################
  2006     16.9K  ###################
  2007     18.9K  ######################
  2008     26.0K  ##############################
  2009     15.8K  ##################
  2010     13.8K  ################
  2011     14.0K  ################
  2012     15.6K  ##################
  2013     17.4K  ####################
  2014     14.3K  ################
  2015      7.9K  #########
  2016      1.9K  ##
  2017       365  
  2018       164  
  2019        20  
  2020       292  
  2021         3  
  2022         7  
  2023         2  
  2024         1  
  2025        13  
  2026         1  
  2027         1  
  2030         1  
  2032         1  
  2033         1  

_INGESTED_AT

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| DOSE_AMT | 2.14M | -200 | 40 | 2.0K | 5.70B | 9.87B |

## who

DRUGNAME by rows
    253.6K  HUMIRA
    232.2K  ASPIRIN
    173.9K  AVONEX
    165.8K  TYSABRI
    160.5K  ENBREL
    149.5K  REMICADE
    143.3K  METHOTREXATE
    120.4K  SEROQUEL
    116.2K  LIPITOR
    114.4K  NEXIUM
    114.2K  PREDNISONE
    103.6K  VIOXX
    102.5K  LISINOPRIL
     99.1K  Enbrel
     97.6K  OMEPRAZOLE
     90.5K  FOSAMAX
     89.4K  FOLIC ACID
     86.7K  SIMVASTATIN
     83.4K  LASIX
     81.8K  SYNTHROID

DRUGNAME by dollars
       7.57B      229 rows  ALFA 2 INTERFERON 2B (INTRON-A)
     231.35M     2.8K rows  INTRON A
     190.34M       27 rows  ALFA 2 INTERFERON 2B
     186.11M     3.5K rows  FILGRASTIM
     144.00M       34 rows  RATIOGRASTIM
     113.76M       85 rows  INTERLEUKIN-2
      88.06M      867 rows  Betaferon
      86.00M      304 rows  INTERFERON BETA
      78.00M       15 rows  G-CSF (TEVAGRASTIM/RATIOGRASTIM)
      73.00M     1.5K rows  INTERFERON ALFA
      69.60M       12 rows  RETARPEN
      67.24M      584 rows  GRANOCYTE
      60.09M       40 rows  TEVAGRASTIM
      40.13M     6.4K rows  THYMOGLOBULIN
      38.49M    50.5K rows  VITAMIN D
      35.00M        7 rows  Pfizerpen
      30.36M    11.5K rows  NEUPOGEN
      30.00M        6 rows  Tevagrastim
      27.90M       50 rows  Roferon-A
      27.65M      277 rows  Interferon Alfa-2a

ISR by rows
       326  7297594
       316  7897094
       316  7439251
       288  7037084
       288  7433119
       288  7353143
       244  8458718
       232  7166245
       225  8462299
       225  8478058
       217  8546029
       217  8616652
       216  8443098
       216  8460723
       216  8483360
       216  8507333
       212  7818586
       212  7420602
       199  6241595
       197  8266269

ISR by dollars
           0        1 rows  4786658
           0        5 rows  4785574
           0        1 rows  4785938
           0        1 rows  4787309
           0        5 rows  4786788
           0        3 rows  4787328
           0        3 rows  4787356
           0        3 rows  4788065
           0        1 rows  4787406
           0        5 rows  4788070
           0        7 rows  4788137
           0        1 rows  4788102
           0        4 rows  4787859
           0        1 rows  4786508
           0        3 rows  4785592
           0        2 rows  4785562
           0        1 rows  4788113
           0        7 rows  4787250
           0        1 rows  4786985
           0        1 rows  4786017

DOSE_VBM by rows
     1.13M  UNK
     95.5K  50 MG, QWK
     85.4K  UNK, UNKNOWN
     81.8K  ORAL
     53.4K  UNKNOWN
     48.1K  UNK UKN, UNK
     42.1K  10 MG, UNK
     38.8K  SEE IMAGE
     34.6K  10 MG, QD
     34.5K  5 MG, UNK
     33.9K  UNK, UNK
     28.7K  20 MG, UNK
     26.0K  20 MCG/24HR, CONT
     25.0K  DAILY
     24.7K  PO
     24.1K  20 MG, QD
     21.9K  300 MG
     21.4K  50 MG, UNK
     21.3K  1 DF, QD
     21.3K  5 MG, QD

DOSE_VBM by dollars
     170.00M        1 rows  SUBJECT MISSED 5 DAYS OF INTERFERON ALPHA
     144.00M        5 rows  48000000 IU (INTERNATIONAL UNIT) DAILY;
      80.00M        1 rows  80000000 IU, QOD
      67.20M        2 rows  33600000 IU, QD
      40.10M        1 rows  40 MG X1 , 100 MG X2 , 145 MG X1 Q24HR IV
      35.00M       29 rows  5000000 IU, UNK
      30.00M        1 rows  30000000 IU, PRN
      30.00M        1 rows  30000000 DF, 2/WEEK
      24.00M        5 rows  24000000 IU, UNK
      24.00M        1 rows  Q24 HRS
      24.00M        1 rows  24000000 IU
      24.00M       54 rows  6000000 IU, UNK
      16.00M        2 rows  8000000 IU, QOD
      12.00M       14 rows  3000000 IU
      12.00M        8 rows  2400000 IU, UNK
      10.00M        2 rows  10000000 IU, QD
      10.00M        1 rows  10000000 IU, 5 X PER WEEK
      10.00M        1 rows  10 MILLION IU ONCE PER WEEK
      10.00M        6 rows  5000000 IU
       9.00M        4 rows  3000000 IU,

LOT_NBR by rows
     30.6K  UNKNOWN
      5.1K  NOT REPORTED
      2.6K  UNCONFIRMED
      1.6K  UNK
       838  NOT PROVIDED
       431  UNKNOWN,UNKNOWN
       352  NOT AVAILABLE
       256  1031274
       231  UNSPECIFIED
       220  1029702
       219  1031956
       217  NR
       212  1031955
       201  1031273
       198  1031954
       196  1032451
       192  1031272
       191  VNF2J028B,VNF2J026-16,VNF2J026-16,V
       189  1031957
       179  1031959

LOT_NBR by dollars
       4.52M    30.6K rows  UNKNOWN
       2.40M        1 rows  BA 1543
       1.16M      191 rows  VNF2J028B,VNF2J026-16,VNF2J026-16,V
      236.2K     5.1K rows  NOT REPORTED
      228.1K     1.6K rows  UNK
      166.2K     2.6K rows  UNCONFIRMED
      127.7K      431 rows  UNKNOWN,UNKNOWN
       80.0K        2 rows  0010108529
       57.7K       54 rows  UNKNOWN,UNKNOWN,UNKNOWN,UNKNOWN,UNK
       52.8K      145 rows  UNKNOWN,UNKNOWN,UNKNOWN
       47.4K      838 rows  NOT PROVIDED
       40.0K        1 rows  0010047779
       40.0K        1 rows  G121964A
       40.0K        1 rows  0010116556
       39.8K       53 rows  244039
       38.6K       52 rows  244038
       38.5K       53 rows  244029
       36.9K       52 rows  244033
       34.5K       47 rows  244049
       31.5K       43 rows  244030

## who x when

DRUGNAME by EXP_DT, dollars = DOSE_AMT
  ASPIRIN                                   2001:3 2002:1 2003:2 2004:14 2005:36 2006:37 2007:11 2008:4 2009:15 2010:10 2011:22 2012:81 2013:15 2014:325 2015:81
  AVONEX                                    1997:2 2001:4 2002:9 2003:47 2004:235 2005:825 2006:803 2007:373 2008:267 2009:6 2010:2 2011:2 2012:9 2013:30 2014:60.50 2015:30
  ENBREL                                    1998:1 2001:1 2003:1 2004:8 2005:25 2006:8 2007:7 2008:13 2009:13 2010:7 2011:10 2012:13 2013:50 2014:50 2015:850 2016:353.90
  FOLIC ACID                                2010:1 2011:2 2012:1 2013:3
  FOSAMAX                                   2000:2 2002:1 2005:4 2006:8 2007:8 2008:19 2009:17 2010:32 2011:15 2012:16 2013:70 2014:35 2015:1 2020:2
  HUMIRA                                    2000:1 2003:1 2004:117 2005:580 2006:257 2007:37 2008:16 2009:22 2010:18 2011:20 2012:17 2013:200 2014:671.60 2015:520 2020:1
  INTRON A                                  1998:1 1999:3 2001:2 2003:26 2004:8 2005:8 2006:10 2007:5 2008:1 2009:1 2010:7 2011:3 2014:300.0K 2015:1 2016:0.42
  LASIX                                     2005:2 2007:1 2008:1 2012:2 2013:1
  LIPITOR                                   2002:1 2003:1 2004:4 2005:32 2006:24 2007:20 2008:18 2009:30 2010:24 2011:24 2012:80 2013:71 2014:80 2015:60 2020:1
  LISINOPRIL                                2005:11 2006:5 2007:29 2008:37 2009:59 2010:46 2011:57 2012:10 2013:310 2014:172 2015:140 2016:50 2018:5 2020:1
  METHOTREXATE                              2005:6 2006:20 2007:29 2008:29 2009:33 2010:10 2011:19 2012:12 2013:2.9K 2014:308 2015:46.36 2020:3
  NEXIUM                                    2005:1 2007:5 2008:4 2009:17 2010:15 2011:28 2012:13 2013:80 2014:200 2015:81 2016:2 2020:1
  OMEPRAZOLE                                2004:2 2005:9 2006:92 2007:3 2008:11 2009:12 2010:38 2011:73 2012:20 2013:485 2014:556.60 2015:181 2020:24
  PREDNISONE                                2004:1 2005:6 2006:6 2007:5 2008:5 2009:7 2010:19 2011:20 2012:10 2013:45 2014:321 2015:20 2016:20 2017:20
  REMICADE                                  2001:3 2002:14 2003:83 2004:220 2005:39 2006:244 2007:55 2008:28 2009:35 2010:21 2011:8 2012:12 2013:7 2014:900 2015:1.8K 2016:2.5K 2017:255
  SEROQUEL                                  1998:1 2001:1 2003:1 2004:2 2005:2 2006:6 2007:16 2008:9 2009:29 2010:26 2011:14 2012:9 2013:200 2014:12.50 2020:2
  SIMVASTATIN                               2004:1 2005:2 2006:2 2007:5 2008:40 2009:68 2010:75 2011:20 2012:67 2013:205 2014:351 2015:120 2016:100 2020:2
  SYNTHROID                                 2001:1 2002:1 2003:1 2004:2 2005:5 2006:3 2007:3 2008:6 2009:6 2010:14 2011:9 2012:11 2013:125 2014:364.15 2015:25
  TYSABRI                                   2006:1 2007:1 2008:119 2009:63 2010:27 2011:3 2012:3 2013:10 2014:300 2015:300 2016:1.2K
  VIOXX                                     2000:1 2001:1 2002:10 2003:5 2004:18 2005:13 2006:12 2007:9 2009:1

ISR by EXP_DT, dollars = DOSE_AMT
  4788070                                   2007:1

## what

ROLE_COD: C 53%, PS 28%, SS 18%, I 0%

VAL_VBM: 1 81%, 2 19%

DECHAL: D 58%, Y 20%, U 15%, N 7%, ` 0%

RECHAL: D 83%, U 15%, N 2%, Y 1%

_SRC_SHA256: 86836c2acd70848d0bc4eaa776247c 10%, 8f19acee4ebf142e0a739fbede65f1 9%, 6b53053a48292a64d54c799bf708ed 9%, 764cd01cb965ea12d4c2e1b6e987a2 9%, 20562c821eebd248445b7618ad6322 8%, d60f5f7484adab4a1a4d132cff8446 8%, 352e15c360dbfcfd2a719c003876f9 8%, 2e36bab3c85215d3471dbe65628616 8%, 31df3e518d400a8ba0323629dd4c64 8%, 5596cf59ae5702f75fefa251300499 8%, 734f8847a4777c7502a1e86f93e49c 7%, 2fad8b257781c5c39c7f414355abdb 7%

_SRC_QUARTER: 2014q1 10%, 2012q1 9%, 2012q2 9%, 2010q3 9%, 2012q4 8%, 2011q2 8%, 2011q3 8%, 2013q4 8%, 2013q1 8%, 2011q4 8%, 2011q1 7%, 2014q2 7%

CUM_DOSE_UNIT: MG 77%, UG 5%, DF 5%, UG/KG 4%, GM 3%, MG/M**2 2%, ML 2%, IU 1%, MG/KG 1%, GTT 1%, MIU 0%, MEQ 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ISR | who | 4.12M | 5.00M | 4896578 14.0K; 4896686 14.0K; 4897340 14.0K; 4897518 14.0K |
| DRUG_SEQ | other | 15.92M | 0 | 1 1.57M; 2 791.5K; 3 576.7K; 4 410.4K |
| ROLE_COD | category | 4 | 2 | C 11.17M; PS 5.81M; SS 3.86M; I 73.9K |
| DRUGNAME | who | 475.4K | 126 | HUMIRA 256.1K; ASPIRIN 232.2K; TYSABRI 176.4K; ENBREL 175.3K |
| VAL_VBM | category | 2 | 0 | 1 16.90M; 2 4.01M |
| ROUTE | other | 87 | 10.40M | ORAL 5.53M; UNKNOWN 1.50M; INTRAVENOUS 1.27M; SUBCUTANEOUS 753.3K |
| DOSE_VBM | who | 1.02M | 13.13M | UNK 1.13M; 50 MG, QWK 97.2K; UNK, UNKNOWN 87.0K; ORAL 85.4K |
| DECHAL | category | 5 | 19.35M | D 909.0K; Y 317.4K; U 228.4K; N 107.3K |
| RECHAL | category | 4 | 14.99M | D 4.92M; U 859.2K; N 98.1K; Y 49.0K |
| LOT_NUM | other | 259.7K | 18.85M | UNKNOWN 402.7K;  UNKNOWN 233.1K; NOWN 137.9K; UNK 99.7K |
| EXP_DT | date | 5.4K | 20.73M | 20080901 2.6K; 20080701 2.5K; 20080601 2.5K; 20080801 2.0K |
| NDA_NUM | other | 17.2K | 15.46M | 125057 114.1K; 103795 104.6K; 020639 87.4K; 021071 82.8K |
| _INGESTED_AT | audit date | 41 | 0 | 56571590-05-31 13:25:50.0 901.6K; 56643912-12-04 14:37:45.0 861.0K; 56643915-05-17 03:58:42.0 821.2K; 56643905-05-09 22:55:29.0 792.4K |
| _SOURCE_RUN_ID | audit | 42 | 0 | 2fc213fa-65e8-4309-90b7-2 901.6K; ed32af90-ffae-4dc9-915c-d 861.0K; 18248fd8-d0b4-4240-9a0c-6 821.2K; d8d3bcd5-cf62-418a-8e36-2 792.4K |
| _SRC_SHA256 | category | 41 | 0 | 86836c2acd70848d0bc4eaa77 901.6K; 8f19acee4ebf142e0a739fbed 861.0K; 6b53053a48292a64d54c799bf 821.2K; 764cd01cb965ea12d4c2e1b6e 792.4K |
| _SRC_QUARTER | category | 42 | 0 | 2014q1 901.6K; 2012q1 861.0K; 2012q2 821.2K; 2010q3 792.4K |
| PRIMARYID | who | 1.50M | 15.92M | 91074171 6.0K; 91078591 6.0K; 91070691 6.0K; 91058441 5.9K |
| CASEID | who | 1.50M | 15.92M | 9107417 6.0K; 9107859 6.0K; 9107069 6.0K; 9105844 5.9K |
| CUM_DOSE_CHR | other | 12.7K | 20.81M | 2 1.1K; 1 1.1K; 2400 1.0K; 20 842 |
| CUM_DOSE_UNIT | category | 28 | 20.81M | MG 81.7K; UG 5.4K; DF 5.4K; UG/KG 4.2K |
| LOT_NBR | who | 15.1K | 20.83M | UNKNOWN 30.6K; NOT REPORTED 5.1K; UNCONFIRMED 2.6K; UNK 1.6K |
| DOSE_AMT | amount | 7.8K | 18.77M | 10 143.0K; 40 141.2K; 50 139.4K; 1 130.1K |
| DOSE_UNIT | other | 283 | 18.77M | MG 1.66M; UG 162.8K; DF 128.7K; MG/M**2 41.2K |
| DOSE_FORM | who | 977 | 19.04M | TABLET 428.5K; CAPSULE 125.7K; INJECTION 89.9K; Tablet 86.3K |
| DOSE_FREQ | other | 328 | 19.44M | QD 704.0K; BID 252.2K; /wk 173.1K; QOW 78.9K |
