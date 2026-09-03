# PORTAL_CKA_INDIANA_DATA_HUB_D4DAE8D984

rows 10.0K  columns 11  scan 5.0s

roles: amount 1, audit 2, category 2, date 1, other 2, who 4

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_DOLLAR_AMOUNT_OF_CLAIMS | 10.0K | 74 | 23.4K | 385.2K | 998.2K | 524.27M |

## who

TOTAL_NUMBER_OF_RECIPIENTS by rows
       232  22
       208  24
       189  25
       186  26
       184  23
       167  27
       157  30
       148  29
       147  28
       138  31
       136  36
       127  33
       122  32
       119  40
       113  35
       108  39
       106  34
       103  37
       101  38
        95  42

TOTAL_NUMBER_OF_RECIPIENTS by dollars
       1.94M       12 rows  276
       1.86M       28 rows  153
       1.73M       11 rows  290
       1.72M       22 rows  223
       1.69M       25 rows  156
       1.69M       15 rows  212
       1.66M       19 rows  264
       1.65M      189 rows  25
       1.65M       24 rows  170
       1.64M       25 rows  175
       1.63M        2 rows  1229
       1.62M       25 rows  169
       1.62M       11 rows  309
       1.62M      232 rows  22
       1.62M       13 rows  283
       1.60M      136 rows  36
       1.60M       35 rows  115
       1.60M      208 rows  24
       1.59M      148 rows  29
       1.59M       27 rows  142

TOTAL_NUMBER_OF_PROVIDERS by rows
       446  14
       445  13
       442  12
       423  11
       401  15
       398  10
       373  17
       365  18
       359  16
       335  9
       313  19
       304  20
       281  21
       265  23
       264  22
       263  8
       204  25
       200  24
       194  27
       193  26

TOTAL_NUMBER_OF_PROVIDERS by dollars
      12.18M      109 rows  39
      10.86M      265 rows  23
      10.79M      194 rows  27
      10.46M       76 rows  46
      10.44M      139 rows  34
      10.42M      147 rows  32
      10.13M      132 rows  35
      10.11M      175 rows  29
      10.09M      178 rows  28
      10.05M      163 rows  30
      10.00M      114 rows  36
       9.92M       92 rows  40
       9.78M      144 rows  31
       9.65M      193 rows  26
       9.53M      204 rows  25
       9.39M      281 rows  21
       9.26M      373 rows  17
       9.17M      264 rows  22
       9.15M      365 rows  18
       9.09M      313 rows  19

MAJOR_DIAGNOSIS_DURING_ER by rows
      1.1K  CHEST PAIN NOS                                                        
       638  Acute upper respiratory infection, unspecified                        
       620  FEVER NOS                                                             
       612  ACUTE URI NOS                                                         
       548  ABDMNAL PAIN UNSPCF SITE                                              
       476  OTITIS MEDIA NOS                                                      
       412  ACUTE PHARYNGITIS                                                     
       397  Other chest pain                                                      
       382  URIN TRACT INFECTION NOS                                              
       308  Chest pain, unspecified                                               
       269  Urinary tract infection, site not specified                           
       262  HEADACHE                                                              
       236  OTH CURR COND-ANTEPARTUM                                              
       225  Acute pharyngitis, unspecified                                        
       211  Unspecified abdominal pain                                            
       197  Chronic obstructive pulmonary disease w (acute) exacerbation          
       194  ABDMNAL PAIN OTH SPCF ST                                              
       173  Fever, unspecified                                                    
       166  PREG COMPL NEC-ANTEPART                                               
       164  OBS CHR BRONC W(AC) EXAC                                              

MAJOR_DIAGNOSIS_DURING_ER by dollars
      70.96M     1.1K rows  CHEST PAIN NOS                                              
      38.92M      548 rows  ABDMNAL PAIN UNSPCF SITE                                    
      34.98M      638 rows  Acute upper respiratory infection, unspecified              
      33.07M      397 rows  Other chest pain                                            
      29.09M      308 rows  Chest pain, unspecified                                     
      26.20M      211 rows  Unspecified abdominal pain                                  
      23.76M      612 rows  ACUTE URI NOS                                               
      23.19M      620 rows  FEVER NOS                                                   
      19.59M      236 rows  OTH CURR COND-ANTEPARTUM                                    
      17.36M      262 rows  HEADACHE                                                    
      17.27M      194 rows  ABDMNAL PAIN OTH SPCF ST                                    
      17.07M      269 rows  Urinary tract infection, site not specified                 
      15.73M      382 rows  URIN TRACT INFECTION NOS                                    
      15.01M      412 rows  ACUTE PHARYNGITIS                                           
      12.03M      476 rows  OTITIS MEDIA NOS                                            
      11.96M      139 rows  Headache                                                    
      11.77M      166 rows  PREG COMPL NEC-ANTEPART                                     
       9.55M      225 rows  Acute pharyngitis, unspecified                              
       7.18M      197 rows  Chronic obstructive pulmonary disease w (acute) exacerbation
       7.09M      138 rows  LUMBAGO                                                     

SRC_SHA256 by rows
     10.0K  1e8be5d71701923a295cee9a488c89815a733a1ed70edccc1c738c3551ac8c9d

SRC_SHA256 by dollars
     524.27M    10.0K rows  1e8be5d71701923a295cee9a488c89815a733a1ed70edccc1c738c3551ac

## who x when

TOTAL_NUMBER_OF_RECIPIENTS by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_DOLLAR_AMOUNT_OF_CLAIMS
  1229                                      2026:1.63M
  153                                       2026:1.86M
  156                                       2026:1.69M
  170                                       2026:1.65M
  175                                       2026:1.64M
  212                                       2026:1.69M
  22                                        2026:1.62M
  223                                       2026:1.72M
  23                                        2026:1.34M
  24                                        2026:1.60M
  25                                        2026:1.65M
  26                                        2026:1.52M
  264                                       2026:1.66M
  27                                        2026:1.52M
  276                                       2026:1.94M
  28                                        2026:1.32M
  29                                        2026:1.59M
  290                                       2026:1.73M
  30                                        2026:1.49M
  31                                        2026:1.27M
  32                                        2026:1.46M
  33                                        2026:1.35M
  34                                        2026:1.23M
  35                                        2026:1.30M
  36                                        2026:1.60M
  37                                        2026:1.16M
  38                                        2026:1.34M
  39                                        2026:1.40M
  40                                        2026:1.50M
  42                                        2026:1.23M

TOTAL_NUMBER_OF_PROVIDERS by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_DOLLAR_AMOUNT_OF_CLAIMS
  10                                        2026:4.70M
  11                                        2026:5.86M
  12                                        2026:6.43M
  13                                        2026:7.43M
  14                                        2026:7.41M
  15                                        2026:7.49M
  16                                        2026:7.50M
  17                                        2026:9.26M
  18                                        2026:9.15M
  19                                        2026:9.09M
  20                                        2026:8.61M
  21                                        2026:9.39M
  22                                        2026:9.17M
  23                                        2026:10.86M
  24                                        2026:8.75M
  25                                        2026:9.53M
  26                                        2026:9.65M
  27                                        2026:10.79M
  28                                        2026:10.09M
  29                                        2026:10.11M
  30                                        2026:10.05M
  32                                        2026:10.42M
  34                                        2026:10.44M
  35                                        2026:10.13M
  36                                        2026:10.00M
  39                                        2026:12.18M
  40                                        2026:9.92M
  46                                        2026:10.46M
  8                                         2026:2.34M
  9                                         2026:3.43M

## what

AGE_GROUP: 06-17 20%, 00-05 19%, 18-32 18%, 33-48 16%, 49-64 14%, 65+ 12%

YEAR: 2017 19%, 2015 17%, 2014 17%, 2016 17%, 2013 16%, 2012 15%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ZIPCODE | other | 442 | 0 | 46202 72; 46825 72; 47362 72; 46804 72 |
| TOTAL_NUMBER_OF_RECIPIENTS | who | 738 | 0 | 22 232; 24 208; 25 189; 26 186 |
| TOTAL_NUMBER_OF_CLAIMS | other | 1.7K | 0 | 60 60; 77 56; 71 56; 68 55 |
| TOTAL_DOLLAR_AMOUNT_OF_CLAIMS | amount | 9.3K | 0 | 37471 50; 16503 50; 8274 50; 8494 50 |
| TOTAL_NUMBER_OF_PROVIDERS | who | 103 | 0 | 14 446; 13 445; 12 442; 11 423 |
| MAJOR_DIAGNOSIS_DURING_ER | who | 252 | 0 | CHEST PAIN NOS            1.1K; Acute upper respiratory i 638; FEVER NOS                 620; ACUTE URI NOS             612 |
| AGE_GROUP | category | 6 | 0 | 06-17 2.0K; 00-05 1.9K; 18-32 1.8K; 33-48 1.6K |
| YEAR | category | 6 | 0 | 2017 1.9K; 2015 1.7K; 2014 1.7K; 2016 1.7K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:27:54.75766 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | b84731d0-a906-4608-979a-e 10.0K |
| SRC_SHA256 | who | 1 | 0 | 1e8be5d71701923a295cee9a4 10.0K |
