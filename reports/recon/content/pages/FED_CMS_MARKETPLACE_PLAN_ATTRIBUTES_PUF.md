# FED_CMS_MARKETPLACE_PLAN_ATTRIBUTES_PUF

rows 22.1K  columns 154  scan 6.3s

roles: amount 8, audit 2, category 71, date 3, empty 14, id 1, other 6, state 1, who 48

## when

IMPORTDATE
  2025     16.1K  ##############################
  2026      5.9K  ###########

PLANEFFECTIVEDATE
  2025         3  
  2026     22.1K  ##############################

PLANEXPIRATIONDATE
  2026     16.9K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| EHBPERCENTTOTALPREMIUM | 20.4K | 0.95 | 1 | 1 | 1 | 20.3K |
| EHBPEDIATRICDENTALAPPORTIONMENTQUANTITY | 1.2K | 0.10 | 1 | 1 | 1 | 1.2K |
| SBCHAVINGABABYCOPAYMENT | 20.7K | 0 | 10 | 3.6K | 6.3K | 3.93M |
| SBCHAVINGDIABETESCOPAYMENT | 20.7K | 0 | 400 | 2.4K | 5.5K | 11.56M |
| SBCHAVINGSIMPLEFRACTURECOPAYMENT | 20.7K | 0 | 100 | 2.1K | 2.7K | 4.63M |
| INPATIENTCOPAYMENTMAXIMUMDAYS | 22.1K | 0 | 0 | 3 | 5 | 1.8K |

## who

PLANVARIANTMARKETINGNAME by rows
       189  Blue Advantage Plus Silver℠ 202
       189  Blue Advantage Plus Silver℠ 605
       189  Blue Advantage Plus Silver℠ Standard
       189  Blue Advantage Silver HMO℠ 205
       189  Blue Advantage Silver HMO℠ Standard
       168  AIAN Cost Share
       147  Standard Silver
       140  Standard Silver + Vision + Adult Dental
       108  Blue Advantage Bronze HMO℠ Standard
       108  Blue Advantage Plus Bronze℠ 303
       108  Blue Advantage Plus Bronze℠ 305
       108  Blue Advantage Plus Bronze℠ Standard
       108  Blue Advantage Plus Gold℠ Standard
       108  Blue Advantage Plus Gold℠ 203
       108  Blue Advantage Gold HMO℠ 206
       108  Blue Advantage Gold HMO℠ Standard
       108  Blue Advantage Bronze HMO℠ 204
       108  Blue Advantage Plus Gold℠ 803
        98  Blue Advantage Silver HMO℠ 801
        91  MyBlue Health Silver℠ 405

PLANVARIANTMARKETINGNAME by dollars
          78       39 rows  Bronze Elite + PCP Saver Plus
          39       13 rows  UHC Bronze-X Copay Focus $0 Indiv Med Ded ($0 Virtual Urgent
          39       13 rows  UHC Bronze Copay Focus $0 Indiv Med Ded ($0 Virtual Urgent C
          39       13 rows  UHC Bronze-B Copay Focus $0 Indiv Med Ded ($0 Virtual Urgent
          34      168 rows  AIAN Cost Share
          27       12 rows  AvMed Entrust Platinum 25 (2026)
          27       12 rows  AvMed Entrust Platinum 25 Dental+Vision (2026)
          24        8 rows  UHC Silver Copay Focus $0 Indiv Med Ded ($0 Virtual Urgent C
          24        8 rows  UHC Silver-E Copay Focus $0 Indiv Med Ded ($0 Virtual Urgent
          24        8 rows  UHC Silver-X Copay Focus $0 Indiv Med Ded ($0 Virtual Urgent
          24        8 rows  UHC Silver-B Copay Focus $0 Indiv Med Ded ($0 Virtual Urgent
          21        7 rows  UHC Bronze-X Copay Focus+ $0 Indiv Med Ded ($0 Virtual Urgen
          21        7 rows  UHC Bronze Copay Focus+ $0 Indiv Med Ded ($0 Virtual Urgent 
          21        7 rows  UHC Bronze-B Copay Focus+ $0 Indiv Med Ded ($0 Virtual Urgen
          20        4 rows  Capital Health Plan HMO Gold 3000
          18        6 rows  UHC Gold Copay Focus $0 Indiv Med Ded ($0 Virtual Urgent Car
          18        6 rows  UHC Gold-X Copay Focus $0 Indiv Med Ded ($0 Virtual Urgent C
          18        6 rows  Gold Elite Saver Plus
          18        6 rows  UHC Gold-B Copay Focus $0 Indiv Med Ded ($0 Virtual Urgent C
          15        5 rows  UHC Silver-B Copay Focus+ $0 Indiv Med Ded ($0 Virtual Urgen

PLANMARKETINGNAME by rows
       189  Blue Advantage Silver HMO℠ Standard
       189  Blue Advantage Plus Silver℠ Standard
       189  Blue Advantage Plus Silver℠ 202
       189  Blue Advantage Silver HMO℠ 205
       189  Blue Advantage Plus Silver℠ 605
       147  Standard Silver
       140  Standard Silver + Vision + Adult Dental
       108  Blue Advantage Plus Bronze℠ Standard
       108  Blue Advantage Plus Gold℠ Standard
       108  Blue Advantage Plus Bronze℠ 303
       108  Blue Advantage Plus Gold℠ 803
       108  Blue Advantage Plus Bronze℠ 305
       108  Blue Advantage Bronze HMO℠ Standard
       108  Blue Advantage Gold HMO℠ 206
       108  Blue Advantage Plus Gold℠ 203
       108  Blue Advantage Bronze HMO℠ 204
       108  Blue Advantage Gold HMO℠ Standard
       105  Silver Classic Standard
       105  UHC Silver Standard (No Referrals)
        98  Blue Advantage Silver HMO℠ 801

PLANMARKETINGNAME by dollars
         144       56 rows  UHC Silver Copay Focus $0 Indiv Med Ded ($0 Virtual Urgent C
         117       52 rows  UHC Bronze Copay Focus $0 Indiv Med Ded ($0 Virtual Urgent C
         104       52 rows  Bronze Elite + PCP Saver Plus
          90       35 rows  UHC Silver Copay Focus+ $0 Indiv Med Ded ($0 Virtual Urgent 
          63       28 rows  UHC Bronze Copay Focus+ $0 Indiv Med Ded ($0 Virtual Urgent 
          54       24 rows  UHC Gold Copay Focus $0 Indiv Med Ded ($0 Virtual Urgent Car
          36       16 rows  UHC Gold Copay Focus $0 Indiv Med Ded ($0 Virtual Urgent Car
          36       16 rows  UHC Gold Copay Focus+ $0 Indiv Med Ded ($0 Virtual Urgent Ca
          27       12 rows  UHC Bronze Copay Focus $0 Indiv Med Ded ($0 Virtual Urgent C
          27       12 rows  AvMed Entrust Platinum 25 Dental+Vision (2026)
          27       12 rows  AvMed Entrust Platinum 25 (2026)
          24        8 rows  Gold Elite Saver Plus
          21        7 rows  Gym Access IND Silver POS OA 1009
          21        7 rows  Gym Access IND Silver HMO OA 1009
          20        4 rows  Capital Health Plan HMO Gold 3000
          18        7 rows  UHC Kelsey-Seybold Silver Copay Focus+ $0 Indiv Med Ded (Den
          18        7 rows  UHC Silver Advantage+ ($0 Virtual Urgent Care, $8 Tier 2 Rx,
          18       21 rows  Connect Silver 3000 Indiv Med Deductible
          18        7 rows  UHC Silver Copay Focus $0 Indiv Med Ded ($0 Virtual Urgent C
          18        7 rows  UHC Silver Copay Focus (Virtual Urgent Care, No Referrals)

ISSUERMARKETPLACEMARKETINGNAME by rows
      2.7K  Blue Cross and Blue Shield of Texas
      1.5K  UnitedHealthcare
      1.1K  Oscar Insurance Company
      1.0K  Medica
       696  Anthem Blue Cross and Blue Shield
       589  Blue Cross Blue Shield of Arizona
       585  Blue Cross and Blue Shield of NC
       529  Cigna Healthcare
       504  BlueCross BlueShield of Tennessee
       457  Blue Cross and Blue Shield of Oklahoma
       452  Florida Blue HMO (a BlueCross BlueShield FL company)
       435  Ambetter Health
       402  Molina Healthcare
       402  Blue Cross and Blue Shield of Nebraska
       394  BlueCross BlueShield of South Carolina
       344  CareSource
       335  Blue Cross and Blue Shield of Montana
       331  AvMed
       276  Quartz
       276  Security Health Plan

ISSUERMARKETPLACEMARKETINGNAME by dollars
        1.0K     1.5K rows  UnitedHealthcare
         120      452 rows  Florida Blue HMO (a BlueCross BlueShield FL company)
         100     1.1K rows  Oscar Insurance Company
          80       90 rows  Blue Cross and Blue Shield of Alabama
          69      116 rows  Florida Health Care Plans
          69      156 rows  Florida Blue (BlueCross BlueShield FL)
          54      331 rows  AvMed
          27      402 rows  Molina Healthcare
          24      122 rows  Network Health
          20       85 rows  Oscar Health Insurance
          20       41 rows  Capital Health Plan
          18      118 rows  Health First Commercial Plans, Inc.
          18       37 rows  WellSense Health Plan
          18      529 rows  Cigna Healthcare
          16      126 rows  Oscar Health Plan, Inc.
          16      181 rows  Oscar Health Maintenance Organization of Florida
          16      121 rows  Oscar Health Plan of North Carolina, Inc
          16      100 rows  Kaiser Permanente
          15       45 rows  Alliant Health Plans, Inc.
          12       85 rows  Oscar Insurance Corporation of Ohio

PLANBROCHURE by rows
      2.6K  https://www.bcbstx.com/plan-docs/ind/brochure-tx-2026.pdf
       592  http://file.anthem.com/2026/1081326MUCENABS_2026.pdf
       589  https://www.azblue.com/2026plans/IndividualShoppersGuide
       577  https://www.hioscar.com/asset/plan-brochure-texas-2026
       445  https://www.bcbsok.com/plan-docs/ind/brochure-ok-2026.pdf
       402  https://www.nebraskablue.com/-/media/Files/NebraskaBlueDotCom/Shop-Pla
       384  https://www.bcbst.com/sbc/2026/pb/Network-E.pdf
       341  https://www.floridablue.com/individualsandfamilies/products/myblue-202
       331  https://shc-p-001.sitecorecontenthub.cloud/api/public/content/2026-Avm
       323  https://www.bcbsmt.com/plan-docs/ind/brochure-mt-2026.pdf
       246  https://www.priorityhealth.com/individual-family-health-insurance/2026
       231  https://www.ambetterhealth.com/en/fl/health-plans/
       225  https://www.Medica.com/IAPlans-2026
       181  https://www.hioscar.com/asset/plan-brochure-florida-2026
       180  https://www.Medica.com/MOPlans-2026
       180  https://www.bluecrossnc.com/content/dam/bcbsnc/pdf/hosted/blatrium26.p
       180  https://www.Medica.com/NEPlans-2026
       174  https://amb.et/mktbrochure/TX
       172  https://www.averahealthplans.com/app/files/public/d4d062ba-cf0b-4303-9
       166  https://www.securityhealth.org/myplans

PLANBROCHURE by dollars
         117       71 rows  https://www.uhc.com/azplanbrochure2026
          72       30 rows  https://www.uhc.com/txksplanbrochure2026
          72       78 rows  https://www.uhc.com/inplanbrochure2026
          72      341 rows  https://www.floridablue.com/individualsandfamilies/products/
          72       86 rows  https://www.uhc.com/ohplanbrochure2026
          72       75 rows  https://www.uhc.com/msplanbrochure2026
          72       74 rows  https://www.uhc.com/neplanbrochure2026
          72       56 rows  https://www.uhc.com/txsnplanbrochure2026
          54       67 rows  https://www.uhc.com/alplanbrochure2026
          54      331 rows  https://shc-p-001.sitecorecontenthub.cloud/api/public/conten
          54       67 rows  https://www.uhc.com/laplanbrochure2026
          50       14 rows  https://www.alabamablue.com/pb/2026smallgroup.pdf
          48      111 rows  https://www.floridablue.com/individualsandfamilies/products/
          45       86 rows  https://www.uhc.com/scplanbrochure2026
          45       60 rows  https://www.uhc.com/tnplanbrochure2026
          45       91 rows  https://www.floridablue.com/individualsandfamilies/products/
          36       60 rows  https://www.uhc.com/iaplanbrochure2026
          36       75 rows  https://www.uhc.com/ksplanbrochure2026
          36       67 rows  https://www.uhc.com/moplanbrochure2026
          30       75 rows  https://www.alabamablue.com/pb/2026individualpb.pdf

## who x when

PLANVARIANTMARKETINGNAME by PLANEFFECTIVEDATE, dollars = INPATIENTCOPAYMENTMAXIMUMDAYS
  AIAN Cost Share                           2026:34
  AvMed Entrust Platinum 25 (2026)          2026:27
  AvMed Entrust Platinum 25 Dental+Vision   2026:27
  Blue Advantage Bronze HMO℠ 204            2026:0
  Blue Advantage Bronze HMO℠ Standard       2026:0
  Blue Advantage Gold HMO℠ 206              2026:0
  Blue Advantage Gold HMO℠ Standard         2026:0
  Blue Advantage Plus Bronze℠ 303           2026:0
  Blue Advantage Plus Bronze℠ 305           2026:0
  Blue Advantage Plus Bronze℠ Standard      2026:0
  Blue Advantage Plus Gold℠ 203             2026:0
  Blue Advantage Plus Gold℠ 803             2026:0
  Blue Advantage Plus Gold℠ Standard        2026:0
  Blue Advantage Plus Silver℠ 202           2026:0
  Blue Advantage Plus Silver℠ 605           2026:0
  Blue Advantage Plus Silver℠ Standard      2026:0
  Blue Advantage Silver HMO℠ 205            2026:0
  Blue Advantage Silver HMO℠ 801            2026:0
  Blue Advantage Silver HMO℠ Standard       2026:0
  Bronze Elite + PCP Saver Plus             2026:78
  MyBlue Health Silver℠ 405                 2026:0
  Standard Silver                           2026:0
  Standard Silver + Vision + Adult Dental   2026:0
  UHC Bronze Copay Focus $0 Indiv Med Ded   2026:39
  UHC Bronze-B Copay Focus $0 Indiv Med De  2026:39
  UHC Bronze-X Copay Focus $0 Indiv Med De  2026:39
  UHC Silver Copay Focus $0 Indiv Med Ded   2026:24
  UHC Silver-B Copay Focus $0 Indiv Med De  2026:24
  UHC Silver-E Copay Focus $0 Indiv Med De  2026:24
  UHC Silver-X Copay Focus $0 Indiv Med De  2026:24

PLANMARKETINGNAME by PLANEFFECTIVEDATE, dollars = INPATIENTCOPAYMENTMAXIMUMDAYS
  AvMed Entrust Platinum 25 Dental+Vision   2026:27
  Blue Advantage Bronze HMO℠ 204            2026:0
  Blue Advantage Bronze HMO℠ Standard       2026:0
  Blue Advantage Gold HMO℠ 206              2026:0
  Blue Advantage Gold HMO℠ Standard         2026:0
  Blue Advantage Plus Bronze℠ 303           2026:0
  Blue Advantage Plus Bronze℠ 305           2026:0
  Blue Advantage Plus Bronze℠ Standard      2026:0
  Blue Advantage Plus Gold℠ 203             2026:0
  Blue Advantage Plus Gold℠ 803             2026:0
  Blue Advantage Plus Gold℠ Standard        2026:0
  Blue Advantage Plus Silver℠ 202           2026:0
  Blue Advantage Plus Silver℠ 605           2026:0
  Blue Advantage Plus Silver℠ Standard      2026:0
  Blue Advantage Silver HMO℠ 205            2026:0
  Blue Advantage Silver HMO℠ 801            2026:0
  Blue Advantage Silver HMO℠ Standard       2026:0
  Bronze Elite + PCP Saver Plus             2026:104
  Silver Classic Standard                   2026:0
  Standard Silver                           2026:0
  Standard Silver + Vision + Adult Dental   2026:0
  UHC Bronze Copay Focus $0 Indiv Med Ded   2026:27
  UHC Bronze Copay Focus $0 Indiv Med Ded   2026:117
  UHC Bronze Copay Focus+ $0 Indiv Med Ded  2026:63
  UHC Gold Copay Focus $0 Indiv Med Ded ($  2026:54
  UHC Gold Copay Focus $0 Indiv Med Ded ($  2026:36
  UHC Gold Copay Focus+ $0 Indiv Med Ded (  2026:36
  UHC Silver Copay Focus $0 Indiv Med Ded   2026:144
  UHC Silver Copay Focus+ $0 Indiv Med Ded  2026:90
  UHC Silver Standard (No Referrals)        2026:0

## where

STATECODE: TX 4.3K, FL 2.2K, WI 1.7K, NC 1.1K, OH 1.1K, AZ 1.1K, OK 980, NE 868, TN 864, MI 722, SC 697, MO 654

## what

SOURCENAME: HIOS 71%, SERFF 29%

MARKETCOVERAGE: Individual 98%, SHOP (Small Group) 2%

DENTALONLYPLAN: No 94%, Yes 6%

ISNEWPLAN: Existing 83%, New 17%

PLANTYPE: HMO 50%, EPO 25%, PPO 15%, POS 10%, Indemnity 0%

METALLEVEL: Silver 47%, Gold 22%, Expanded Bronze 21%, Low 4%, Bronze 3%, High 3%, Platinum 1%, Catastrophic 1%

DESIGNTYPE: Not Applicable 66%, Design 1 32%, Design 2 1%, Design 3 1%

UNIQUEPLANDESIGN: No 72%, Yes 28%

QHPNONQHPTYPEID: Both 97%, On the Exchange 2%, Off the Exchange 1%

ISNOTICEREQUIREDFORPREGNANCY: No 87%, Yes 13%

ISREFERRALREQUIREDFORSPECIALIST: No 75%, Yes 25%

SPECIALISTREQUIRINGREFERRAL: Referrals are required for som 57%, All specialists except Behavio 11%, All Specialists require a refe 7%, All except OB/Gyn, Chiropracto 7%, All, except OBGYN and as state 6%, All 3%, All except for mental or behav 2%, Allergy, Asthma, Audiology, Ca 2%, All except routine OB/GYN & pe 2%, All Specialists 1%, The member's PCP will refer to 1%, All specialists seen in an off 1%

PLANLEVELEXCLUSIONS: Some exclusions may apply. See 49%, Non-covered services and any s 20%, Abortion (except when the life 8%, No 4%, All services must be rendered  4%, Abortions/Termination of Pregn 4%, Prior Authorization, Medically 3%, Out of Pocket Maximum applies  3%, See Policy 2%, See Plan Document 2%, See Policy for Details 1%, Out of Pocket Maximum applies  0%

COMPOSITERATINGOFFERED: No 100%, Yes 0%

CHILDONLYOFFERING: Allows Adult and Child-Only 99%, Allows Child-Only 1%

WELLNESSPROGRAMOFFERED: No 81%, Yes 19%

DISEASEMANAGEMENTPROGRAMSOFFERED: Asthma, Depression, Diabetes,  32%, Asthma, Diabetes, Heart Diseas 14%, Asthma, Depression, Diabetes,  10%, Asthma, Depression, Diabetes,  10%, Asthma, Diabetes, Heart Diseas 8%, Asthma, Depression, Diabetes,  5%, Asthma, Depression, Diabetes,  4%, Asthma, Depression, Diabetes,  4%, Diabetes, Heart Disease, Pregn 4%, Asthma, Depression, Diabetes,  4%, Asthma, Depression, Diabetes,  3%, Asthma, Depression, Diabetes,  3%

OUTOFCOUNTRYCOVERAGE: Yes 60%, No 40%

OUTOFSERVICEAREACOVERAGE: Yes 74%, No 26%

NATIONALNETWORK: No 87%, Yes 13%

CSRVARIATIONTYPE: Limited Cost Sharing Plan Vari 19%, Zero Cost Sharing Plan Variati 19%, Standard Silver On Exchange Pl 7%, Standard Silver Off Exchange P 7%, 94% AV Level Silver Plan 7%, 87% AV Level Silver Plan 7%, 73% AV Level Silver Plan 7%, Standard Bronze On Exchange Pl 6%, Standard Bronze Off Exchange P 6%, Standard Gold On Exchange Plan 6%, Standard Gold Off Exchange Pla 6%, Standard Low On Exchange Plan 2%

MEDICALDRUGDEDUCTIBLESINTEGRATED: Yes 90%, No 10%

MULTIPLEINNETWORKTIERS: No 75%, Yes 25%

FIRSTTIERUTILIZATION: 100% 77%, 85% 8%, 44% 6%, 40% 2%, 13% 1%, 0% 1%, 49% 1%, 24% 1%, 28% 1%, 70% 1%, 53% 1%, 1% 0%

SECONDTIERUTILIZATION: 15% 34%, 56% 27%, 60% 7%, 87% 6%, 100% 5%, 51% 4%, 76% 4%, 72% 4%, 30% 3%, 47% 2%, 99% 2%, 79% 2%

SBCHAVINGABABYLIMIT: $60  70%, $0  25%, $50  4%, $70  0%, $80  0%, $40  0%, $20  0%, $10  0%, $1,400  0%

SBCHAVINGDIABETESCOINSURANCE: $0  86%, $200  3%, $400  2%, $100  2%, $60  2%, $300  1%, $30  1%, $20  1%, $600  0%, $10  0%, $40  0%, $90  0%

SBCHAVINGDIABETESLIMIT: $20  54%, $0  42%, $60  2%, $70  2%, $200  1%, $40  0%, $100  0%, $300  0%, $500  0%

SBCHAVINGSIMPLEFRACTURECOINSURANCE: $0  73%, $500  4%, $400  4%, $20  4%, $100  3%, $200  3%, $600  3%, $300  2%, $700  1%, $10  1%, $60  1%, $800  1%

SBCHAVINGSIMPLEFRACTURELIMIT: $0  100%, $10  0%

SPECIALTYDRUGMAXIMUMCOINSURANCE: $650  53%, $150  20%, $1,000  14%, $500  8%, $250  3%, $750  1%

MEHBINNTIER1INDIVIDUALMOOP: $450  66%, Not Applicable 19%, $350  6%, $400  4%, $0  2%, $375  2%, $425  1%

MEHBINNTIER1FAMILYPERPERSONMOOP: $450 per person 66%, per person not applicable 19%, $350 per person 6%, $400 per person 4%, $0 per person 2%, $375 per person 2%, $425 per person 1%

MEHBINNTIER1FAMILYPERGROUPMOOP: $900 per group 65%, per group not applicable 20%, $700 per group 6%, $800 per group 4%, $0 per group 2%, $750 per group 2%, $850 per group 1%

MEHBINNTIER2INDIVIDUALMOOP: $450  70%, $375  11%, $425  10%, $350  5%, Not Applicable 4%

MEHBINNTIER2FAMILYPERPERSONMOOP: $450 per person 70%, $375 per person 11%, $425 per person 10%, $350 per person 5%, per person not applicable 4%

MEHBINNTIER2FAMILYPERGROUPMOOP: $900 per group 70%, $750 per group 11%, $850 per group 10%, $700 per group 5%, per group not applicable 4%

MEHBOUTOFNETINDIVIDUALMOOP: Not Applicable 91%, $900  7%, $450  3%

MEHBOUTOFNETFAMILYPERPERSONMOOP: per person not applicable 91%, $900 per person 6%, $450 per person 3%

MEHBOUTOFNETFAMILYPERGROUPMOOP: per group not applicable 91%, $1800 per group 6%, $900 per group 3%

MEHBCOMBINNOONINDIVIDUALMOOP: Not Applicable 80%, $450  18%, $375  1%, $350  0%, $425  0%, $75  0%, $900  0%

MEHBCOMBINNOONFAMILYPERPERSONMOOP: per person not applicable 80%, $450 per person 18%, $375 per person 1%, $350 per person 0%, $425 per person 0%, $75 per person 0%, $900 per person 0%

MEHBCOMBINNOONFAMILYPERGROUPMOOP: per group not applicable 81%, $900 per group 18%, $750 per group 1%, $700 per group 0%, $850 per group 0%, $1800 per group 0%

MEHBDEDINNTIER1COINSURANCE: 0.00% 27%, 50.00% 26%, 30.00% 17%, 20.00% 9%, 40.00% 9%, 45.00% 3%, 10.00% 3%, 25.00% 2%, 5.00% 1%, 35.00% 0%, 15.00% 0%

MEHBDEDINNTIER2INDIVIDUAL: $0  53%, Not Applicable 12%, $7,500  7%, $1,475  6%, $250  3%, $7,250  3%, $1,500  3%, $4,000  3%, $2,000  2%, $1,000  2%, $5,000  2%, $6,900  2%

MEHBDEDINNTIER2FAMILYPERPERSON: $0 per person 53%, per person not applicable 12%, $7500 per person 7%, $1475 per person 6%, $250 per person 3%, $7250 per person 3%, $1500 per person 3%, $4000 per person 3%, $2000 per person 2%, $1000 per person 2%, $5000 per person 2%, $6900 per person 2%

MEHBDEDINNTIER2FAMILYPERGROUP: $0 per group 53%, per group not applicable 13%, $15000 per group 7%, $2950 per group 6%, $3000 per group 4%, $14500 per group 3%, $8000 per group 3%, $4000 per group 2%, $500 per group 2%, $10000 per group 2%, $13800 per group 2%, $6250 per group 2%

MEHBDEDINNTIER2COINSURANCE: 0.00% 30%, 50.00% 23%, 40.00% 18%, 20.00% 12%, 30.00% 12%, 10.00% 4%, 35.00% 0%

MEHBDEDOUTOFNETINDIVIDUAL: Not Applicable 75%, $0  5%, $50  5%, $100  5%, $75  2%, $500  2%, $15,000  2%, $25  2%, $2,000  1%, $60  1%, $10,000  1%, $29,000  1%

MEHBDEDOUTOFNETFAMILYPERPERSON: per person not applicable 76%, $0 per person 5%, $100 per person 4%, $50 per person 4%, $75 per person 2%, $500 per person 2%, $15000 per person 2%, $25 per person 1%, $2000 per person 1%, $60 per person 1%, $10000 per person 1%, $29000 per person 1%

MEHBDEDOUTOFNETFAMILYPERGROUP: per group not applicable 85%, $0 per group 5%, $150 per group 2%, $30000 per group 2%, $1000 per group 1%, $75 per group 1%, $4000 per group 1%, $20000 per group 1%, $58000 per group 1%, $10000 per group 1%, $6000 per group 1%, $12000 per group 1%

MEHBDEDCOMBINNOONINDIVIDUAL: Not Applicable 69%, $50  14%, $0  5%, $100  4%, $75  2%, $25  2%, $85  1%, $3,500  1%, $60  1%, $150  1%, $22,350  1%, $35  0%

MEHBDEDCOMBINNOONFAMILYPERPERSON: per person not applicable 70%, $50 per person 14%, $0 per person 5%, $100 per person 3%, $25 per person 2%, $75 per person 1%, $85 per person 1%, $3500 per person 1%, $60 per person 1%, $150 per person 1%, $22350 per person 1%, $35 per person 0%

MEHBDEDCOMBINNOONFAMILYPERGROUP: per group not applicable 79%, $150 per group 7%, $0 per group 5%, $200 per group 2%, $75 per group 2%, $100 per group 1%, $300 per group 1%, $7000 per group 1%, $44700 per group 1%, $1000 per group 0%, $225 per group 0%, $7500 per group 0%

DEHBDEDINNTIER1INDIVIDUAL: $0  51%, $500  7%, $400  7%, $3,800  7%, Not Applicable 6%, $4,500  5%, $600  3%, $250  3%, $2,500  3%, $1,000  3%, $7,000  2%, $2,100  2%

DEHBDEDINNTIER1FAMILYPERPERSON: $0 per person 50%, $500 per person 7%, $400 per person 7%, per person not applicable 7%, $3800 per person 7%, $4500 per person 5%, $600 per person 3%, $250 per person 3%, $2500 per person 3%, $1000 per person 3%, $7000 per person 2%, $2100 per person 2%

DEHBDEDINNTIER1FAMILYPERGROUP: $0 per group 46%, per group not applicable 21%, $1000 per group 7%, $7600 per group 7%, $9000 per group 5%, $800 per group 3%, $5000 per group 3%, $14000 per group 2%, $200 per group 2%, $7000 per group 2%, $500 per group 2%, $10000 per group 2%

DEHBDEDINNTIER1COINSURANCE: 0.00% 45%, 50.00% 29%, 40.00% 8%, 30.00% 7%, 20.00% 4%, 25.00% 3%, 10.00% 2%, 45.00% 1%, 100.00% 0%, 15.00% 0%, 5.00% 0%

DEHBDEDINNTIER2INDIVIDUAL: $0  49%, $400  10%, $600  8%, $7,000  7%, $2,100  7%, $250  4%, $2,900  3%, $50  3%, Not Applicable 3%, $300  3%, $3,000  2%, $750  1%

DEHBDEDINNTIER2FAMILYPERPERSON: $0 per person 49%, $400 per person 10%, $600 per person 8%, $7000 per person 7%, $2100 per person 7%, $250 per person 4%, $2900 per person 3%, $50 per person 3%, per person not applicable 3%, $300 per person 3%, $3000 per person 2%, $750 per person 1%

DEHBDEDINNTIER2FAMILYPERGROUP: $0 per group 47%, per group not applicable 28%, $14000 per group 7%, $800 per group 4%, $500 per group 4%, $5800 per group 3%, $2100 per group 1%, $1500 per group 1%, $400 per group 1%, $13000 per group 1%, $15000 per group 1%, $100 per group 1%

DEHBDEDINNTIER2COINSURANCE: 50.00% 42%, 0.00% 26%, 40.00% 17%, 25.00% 5%, 20.00% 5%, 45.00% 3%, 10.00% 1%

DEHBDEDOUTOFNETINDIVIDUAL: Not Applicable 91%, $0  8%, $500  0%, $7,600  0%

DEHBDEDOUTOFNETFAMILYPERPERSON: per person not applicable 91%, $0 per person 8%, $500 per person 0%, $7600 per person 0%

DEHBDEDOUTOFNETFAMILYPERGROUP: per group not applicable 92%, $0 per group 8%, $15200 per group 0%

DEHBDEDCOMBINNOONINDIVIDUAL: Not Applicable 85%, $0  11%, $250  1%, $400  1%, $1,000  1%, $750  0%, $500  0%, $4,000  0%, $200  0%, $3,000  0%, $825  0%, $1,500  0%

DEHBDEDCOMBINNOONFAMILYPERPERSON: per person not applicable 85%, $0 per person 11%, $250 per person 1%, $400 per person 1%, $1000 per person 1%, $750 per person 0%, $500 per person 0%, $4000 per person 0%, $200 per person 0%, $3000 per person 0%, $825 per person 0%, $1500 per person 0%

DEHBDEDCOMBINNOONFAMILYPERGROUP: per group not applicable 87%, $0 per group 10%, $2250 per group 0%, $750 per group 0%, $500 per group 0%, $8000 per group 0%, $1200 per group 0%, $600 per group 0%, $2475 per group 0%, $4500 per group 0%

TEHBDEDINNTIER1COINSURANCE: 0.00% 26%, 50.00% 24%, 40.00% 16%, 30.00% 12%, 25.00% 11%, 20.00% 5%, 35.00% 2%, 10.00% 1%, 15.00% 0%, 45.00% 0%, 5.00% 0%, 80.00% 0%

TEHBDEDINNTIER2COINSURANCE: 50.00% 37%, 0.00% 24%, 30.00% 16%, 40.00% 11%, 20.00% 6%, 35.00% 4%, 25.00% 2%, 10.00% 1%, 60.00% 0%, 15.00% 0%, 45.00% 0%

ISHSAELIGIBLE: No 73%, Yes 27%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| BUSINESSYEAR | other | 1 | 0 | 2026 22.1K |
| STATECODE | state | 30 | 0 | TX 4.3K; FL 2.2K; WI 1.7K; NC 1.1K |
| ISSUERID | other | 347 | 0 | 33602 2.7K; 53901 589; 20069 585; 11512 585 |
| ISSUERMARKETPLACEMARKETINGNAME | who | 161 | 0 | Blue Cross and Blue Shiel 2.7K; UnitedHealthcare 1.5K; Oscar Insurance Company 1.1K; Medica 1.0K |
| SOURCENAME | category | 2 | 0 | HIOS 15.7K; SERFF 6.4K |
| IMPORTDATE | date | 15 | 0 | 10/15/2025 10.6K; 2/3/2026 5.0K; 10/28/2025 1.7K; 11/10/2025 1.1K |
| MARKETCOVERAGE | category | 2 | 0 | Individual 21.6K; SHOP (Small Group) 489 |
| DENTALONLYPLAN | category | 2 | 0 | No 20.7K; Yes 1.4K |
| STANDARDCOMPONENTID | who | 5.1K | 0 | 49714WY0210002 115; 49714WY0200006 115; 49714WY0200005 115; 49714WY0200004 115 |
| PLANMARKETINGNAME | who | 2.7K | 0 | Blue Advantage Plus Silve 262; Blue Advantage Plus Silve 262; Blue Advantage Plus Silve 261; Blue Advantage Silver HMO 261 |
| HIOSPRODUCTID | who | 909 | 0 | 33602TX046 1.5K; 33602TX087 1.3K; 53901AZ142 589; 20069TX051 565 |
| NETWORKID | who | 170 | 0 | TXN009 2.3K; FLN001 1.3K; TXN002 981; OHN001 912 |
| SERVICEAREAID | who | 263 | 0 | FLS001 880; OHS001 840; TXS001 760; WIS001 584 |
| FORMULARYID | who | 772 | 1.4K | TXF001 781; TXF004 419; TXF003 331; TXF011 321 |
| ISNEWPLAN | category | 2 | 0 | Existing 18.4K; New 3.7K |
| PLANTYPE | category | 5 | 0 | HMO 11.0K; EPO 5.5K; PPO 3.4K; POS 2.1K |
| METALLEVEL | category | 8 | 0 | Silver 10.3K; Gold 4.8K; Expanded Bronze 4.7K; Low 807 |
| DESIGNTYPE | category | 4 | 1.7K | Not Applicable 13.5K; Design 1 6.5K; Design 2 283; Design 3 105 |
| UNIQUEPLANDESIGN | category | 2 | 1.4K | No 14.8K; Yes 5.8K |
| QHPNONQHPTYPEID | category | 3 | 0 | Both 21.4K; On the Exchange 341; Off the Exchange 288 |
| ISNOTICEREQUIREDFORPREGNANCY | category | 2 | 1.4K | No 18.0K; Yes 2.7K |
| ISREFERRALREQUIREDFORSPECIALIST | category | 2 | 1.4K | No 15.5K; Yes 5.2K |
| SPECIALISTREQUIRINGREFERRAL | category | 20 | 16.9K | Referrals are required fo 2.8K; All specialists except Be 520; All Specialists require a 341; All except OB/Gyn, Chirop 331 |
| PLANLEVELEXCLUSIONS | category | 43 | 19.0K | Some exclusions may apply 1.4K; Non-covered services and  589; Abortion (except when the 230; No 122 |
| INDIANPLANVARIATIONESTIMATEDADVANCEDPAYMENTAMOUNTPERENROLLEE | who | 1 | 1.7K | $0.00  20.4K |
| COMPOSITERATINGOFFERED | category | 2 | 0 | No 22.0K; Yes 69 |
| CHILDONLYOFFERING | category | 2 | 0 | Allows Adult and Child-On 21.8K; Allows Child-Only 211 |
| CHILDONLYPLANID | empty | 0 | 22.1K |  |
| WELLNESSPROGRAMOFFERED | category | 2 | 1.4K | No 16.8K; Yes 3.9K |
| DISEASEMANAGEMENTPROGRAMSOFFERED | category | 34 | 3.8K | Asthma, Depression, Diabe 5.2K; Asthma, Diabetes, Heart D 2.2K; Asthma, Depression, Diabe 1.7K; Asthma, Depression, Diabe 1.5K |
| EHBPERCENTTOTALPREMIUM | amount | 344 | 1.7K | 1 15.0K; 0.9997 290; 0.998 266; 0.9999 155 |
| EHBPEDIATRICDENTALAPPORTIONMENTQUANTITY | amount | 56 | 20.8K | 1 1.0K; 0.991 10; 0.7 8; 0.98 8 |
| ISGUARANTEEDRATE | who | 1 | 20.7K | Guaranteed Rate 1.4K |
| PLANEFFECTIVEDATE | date | 4 | 0 | 1/1/2026 22.1K; 1/1/2025 2; 1/2/2026 2; 1/2/2025 1 |
| PLANEXPIRATIONDATE | date | 1 | 5.2K | 12/31/2026 16.9K |
| OUTOFCOUNTRYCOVERAGE | category | 2 | 0 | Yes 13.3K; No 8.8K |
| OUTOFCOUNTRYCOVERAGEDESCRIPTION | who | 94 | 6.4K | Emergency Services Only 2.8K; No coverage for any servi 2.6K; Emergency Services 884; Urgent/Emergency Coverage 777 |
| OUTOFSERVICEAREACOVERAGE | category | 2 | 0 | Yes 16.4K; No 5.7K |
| OUTOFSERVICEAREACOVERAGEDESCRIPTION | who | 153 | 3.3K | Coverage outside our serv 2.8K; Emergency and Urgent Serv 1.7K; Plan covers eligible expe 1.1K; Emergency Services 1.1K |
| NATIONALNETWORK | category | 2 | 0 | No 19.3K; Yes 2.8K |
| URLFORENROLLMENTPAYMENT | who | 131 | 816 | https://apply.bcbstx.com/ 2.7K; https://ssoprod.healthpla 2.2K; https://business.hioscar. 1.7K; https://sso.uhc.com/ext/s 1.4K |
| FORMULARYURL | who | 183 | 1.4K | https://www.hioscar.com/s 1.7K; https://www.myprime.com/c 1.7K; https://www.myprime.com/c 975; https://www.cigna.com/ifp 634 |
| PLANID | id | 22.7K | 0 | 83964WY0040002-00 111; 83964WY0040001-00 111; 83964WY0030002-00 111; 83964WY0030001-00 111 |
| PLANVARIANTMARKETINGNAME | who | 6.2K | 0 | Blue Advantage Plus Silve 264; Blue Advantage Plus Silve 264; Blue Advantage Plus Silve 264; Blue Advantage Silver HMO 263 |
| CSRVARIATIONTYPE | category | 19 | 0 | Limited Cost Sharing Plan 4.0K; Zero Cost Sharing Plan Va 4.0K; Standard Silver On Exchan 1.5K; Standard Silver Off Excha 1.5K |
| ISSUERACTUARIALVALUE | who | 547 | 16.2K | 100.00% 1.1K; 70.88% 96; 64.38% 90; 81.64% 84 |
| AVCALCULATOROUTPUTNUMBER | who | 1.5K | 4.0K | 1 3.5K; 0.700079495 1.3K; 0.641164683 1.2K; 0.7803779227020161 1.2K |
| MEDICALDRUGDEDUCTIBLESINTEGRATED | category | 2 | 1.4K | Yes 18.6K; No 2.1K |
| MEDICALDRUGMAXIMUMOUTOFPOCKETINTEGRATED | other | 1 | 1.4K | Yes 20.7K |
| MULTIPLEINNETWORKTIERS | category | 2 | 0 | No 16.6K; Yes 5.5K |
| FIRSTTIERUTILIZATION | category | 37 | 0 | 100% 16.6K; 85% 1.7K; 44% 1.4K; 40% 366 |
| SECONDTIERUTILIZATION | category | 36 | 16.6K | 15% 1.7K; 56% 1.4K; 60% 366; 87% 312 |
| SBCHAVINGABABYDEDUCTIBLE | who | 185 | 1.4K | $0  8.5K; $6,000  1.4K; $2,000  1.2K; $7,500  1.2K |
| SBCHAVINGABABYCOPAYMENT | amount | 63 | 1.4K | $0  9.9K; $10  3.2K; $50  781; $1,000  678 |
| SBCHAVINGABABYCOINSURANCE | who | 128 | 1.4K | $0  8.5K; $2,600  1.6K; $2,500  724; $2,200  715 |
| SBCHAVINGABABYLIMIT | category | 9 | 1.4K | $60  14.4K; $0  5.2K; $50  749; $70  66 |
| SBCHAVINGDIABETESDEDUCTIBLE | other | 118 | 1.4K | $0  8.9K; $900  2.3K; $100  1.1K; $800  708 |
| SBCHAVINGDIABETESCOPAYMENT | amount | 76 | 1.4K | $0  7.2K; $800  1.2K; $700  1.2K; $600  1.1K |
| SBCHAVINGDIABETESCOINSURANCE | category | 44 | 1.4K | $0  17.4K; $200  629; $400  457; $100  401 |
| SBCHAVINGDIABETESLIMIT | category | 9 | 1.4K | $20  11.1K; $0  8.7K; $60  359; $70  339 |
| SBCHAVINGSIMPLEFRACTUREDEDUCTIBLE | who | 84 | 1.4K | $0  8.4K; $2,100  2.0K; $2,800  1.2K; $2,000  1.2K |
| SBCHAVINGSIMPLEFRACTURECOPAYMENT | amount | 56 | 1.4K | $0  7.8K; $200  2.8K; $400  2.2K; $300  1.9K |
| SBCHAVINGSIMPLEFRACTURECOINSURANCE | category | 40 | 1.4K | $0  14.4K; $500  850; $400  817; $20  694 |
| SBCHAVINGSIMPLEFRACTURELIMIT | category | 2 | 1.4K | $0  20.6K; $10  102 |
| SPECIALTYDRUGMAXIMUMCOINSURANCE | category | 6 | 21.8K | $650  156; $150  60; $1,000  42; $500  24 |
| INPATIENTCOPAYMENTMAXIMUMDAYS | amount | 5 | 0 | 0 21.4K; 3 450; 2 126; 5 23 |
| BEGINPRIMARYCARECOSTSHARINGAFTERNUMBEROFVISITS | amount | 6 | 0 | 0 20.8K; 3 687; 1 197; 4 174 |
| BEGINPRIMARYCAREDEDUCTIBLECOINSURANCEAFTERNUMBEROFCOPAYS | amount | 6 | 0 | 0 21.9K; 3 125; 4 35; 5 9 |
| MEHBINNTIER1INDIVIDUALMOOP | category | 7 | 20.7K | $450  916; Not Applicable 268; $350  80; $400  54 |
| MEHBINNTIER1FAMILYPERPERSONMOOP | category | 7 | 20.7K | $450 per person 916; per person not applicable 268; $350 per person 80; $400 per person 54 |
| MEHBINNTIER1FAMILYPERGROUPMOOP | category | 7 | 20.7K | $900 per group 908; per group not applicable 276; $700 per group 80; $800 per group 54 |
| MEHBINNTIER2INDIVIDUALMOOP | category | 5 | 22.0K | $450  70; $375  11; $425  10; $350  5 |
| MEHBINNTIER2FAMILYPERPERSONMOOP | category | 5 | 22.0K | $450 per person 70; $375 per person 11; $425 per person 10; $350 per person 5 |
| MEHBINNTIER2FAMILYPERGROUPMOOP | category | 5 | 22.0K | $900 per group 70; $750 per group 11; $850 per group 10; $700 per group 5 |
| MEHBOUTOFNETINDIVIDUALMOOP | category | 3 | 20.7K | Not Applicable 1.3K; $900  94; $450  35 |
| MEHBOUTOFNETFAMILYPERPERSONMOOP | category | 3 | 20.7K | per person not applicable 1.3K; $900 per person 90; $450 per person 35 |
| MEHBOUTOFNETFAMILYPERGROUPMOOP | category | 3 | 20.7K | per group not applicable 1.3K; $1800 per group 90; $900 per group 35 |
| MEHBCOMBINNOONINDIVIDUALMOOP | category | 7 | 20.7K | Not Applicable 1.1K; $450  248; $375  10; $350  6 |
| MEHBCOMBINNOONFAMILYPERPERSONMOOP | category | 7 | 20.7K | per person not applicable 1.1K; $450 per person 248; $375 per person 10; $350 per person 6 |
| MEHBCOMBINNOONFAMILYPERGROUPMOOP | category | 6 | 20.7K | per group not applicable 1.1K; $900 per group 244; $750 per group 10; $700 per group 6 |
| DEHBINNTIER1INDIVIDUALMOOP | empty | 0 | 22.1K |  |
| DEHBINNTIER1FAMILYPERPERSONMOOP | empty | 0 | 22.1K |  |
| DEHBINNTIER1FAMILYPERGROUPMOOP | empty | 0 | 22.1K |  |
| DEHBINNTIER2INDIVIDUALMOOP | empty | 0 | 22.1K |  |
| DEHBINNTIER2FAMILYPERPERSONMOOP | empty | 0 | 22.1K |  |
| DEHBINNTIER2FAMILYPERGROUPMOOP | empty | 0 | 22.1K |  |
| DEHBOUTOFNETINDIVIDUALMOOP | empty | 0 | 22.1K |  |
| DEHBOUTOFNETFAMILYPERPERSONMOOP | empty | 0 | 22.1K |  |
| DEHBOUTOFNETFAMILYPERGROUPMOOP | empty | 0 | 22.1K |  |
| DEHBCOMBINNOONINDIVIDUALMOOP | empty | 0 | 22.1K |  |
| DEHBCOMBINNOONFAMILYPERPERSONMOOP | empty | 0 | 22.1K |  |
| DEHBCOMBINNOONFAMILYPERGROUPMOOP | empty | 0 | 22.1K |  |
| TEHBINNTIER1INDIVIDUALMOOP | who | 219 | 1.4K | $0  4.0K; $10,600  1.7K; $8,900  1.5K; $10,000  1.4K |
| TEHBINNTIER1FAMILYPERPERSONMOOP | who | 218 | 1.4K | $0 per person 4.0K; $10600 per person 1.7K; $8900 per person 1.5K; $10000 per person 1.4K |
| TEHBINNTIER1FAMILYPERGROUPMOOP | who | 218 | 1.4K | $0 per group 4.0K; $21200 per group 1.7K; $17800 per group 1.5K; $20000 per group 1.4K |
| TEHBINNTIER2INDIVIDUALMOOP | who | 146 | 16.6K | $0  1.0K; $10,150  810; $10,600  474; $8,000  194 |
| TEHBINNTIER2FAMILYPERPERSONMOOP | who | 146 | 16.6K | $0 per person 1.0K; $10150 per person 810; $10600 per person 474; $8000 per person 194 |
| TEHBINNTIER2FAMILYPERGROUPMOOP | who | 142 | 16.6K | $0 per group 1.0K; $20300 per group 810; $21200 per group 474; $16000 per group 194 |
| TEHBOUTOFNETINDIVIDUALMOOP | who | 131 | 1.4K | Not Applicable 17.2K; $0  1.8K; $36,800  104; $30,000  102 |
| TEHBOUTOFNETFAMILYPERPERSONMOOP | who | 133 | 1.4K | per person not applicable 17.2K; $0 per person 1.8K; $36800 per person 104; $30000 per person 102 |
| TEHBOUTOFNETFAMILYPERGROUPMOOP | who | 131 | 1.4K | per group not applicable 17.2K; $0 per group 1.8K; $73600 per group 104; $60000 per group 102 |
| TEHBCOMBINNOONINDIVIDUALMOOP | who | 153 | 1.4K | Not Applicable 17.4K; $0  1.7K; $10,600  79; $10,000  74 |
| TEHBCOMBINNOONFAMILYPERPERSONMOOP | who | 158 | 1.4K | per person not applicable 17.4K; $0 per person 1.7K; $10600 per person 79; $10000 per person 74 |
| TEHBCOMBINNOONFAMILYPERGROUPMOOP | who | 154 | 1.4K | per group not applicable 17.4K; $0 per group 1.7K; $21200 per group 79; $20000 per group 74 |
| MEHBDEDINNTIER1INDIVIDUAL | who | 83 | 18.6K | $0  1.3K; Not Applicable 782; $50  238; $25  91 |
| MEHBDEDINNTIER1FAMILYPERPERSON | who | 83 | 18.6K | $0 per person 1.3K; per person not applicable 884; $50 per person 210; $25 per person 74 |
| MEHBDEDINNTIER1FAMILYPERGROUP | who | 82 | 18.6K | $0 per group 1.3K; per group not applicable 1.2K; $3600 per group 69; $150 per group 67 |
| MEHBDEDINNTIER1COINSURANCE | category | 11 | 20.0K | 0.00% 576; 50.00% 555; 30.00% 365; 20.00% 194 |
| MEHBDEDINNTIER2INDIVIDUAL | category | 30 | 21.3K | $0  328; Not Applicable 75; $7,500  45; $1,475  36 |
| MEHBDEDINNTIER2FAMILYPERPERSON | category | 30 | 21.3K | $0 per person 328; per person not applicable 75; $7500 per person 45; $1475 per person 36 |
| MEHBDEDINNTIER2FAMILYPERGROUP | category | 30 | 21.3K | $0 per group 328; per group not applicable 81; $15000 per group 45; $2950 per group 36 |
| MEHBDEDINNTIER2COINSURANCE | category | 7 | 21.4K | 0.00% 194; 50.00% 144; 40.00% 118; 20.00% 79 |
| MEHBDEDOUTOFNETINDIVIDUAL | category | 48 | 18.6K | Not Applicable 2.4K; $0  172; $50  155; $100  151 |
| MEHBDEDOUTOFNETFAMILYPERPERSON | category | 48 | 18.6K | per person not applicable 2.5K; $0 per person 172; $100 per person 145; $50 per person 131 |
| MEHBDEDOUTOFNETFAMILYPERGROUP | category | 43 | 18.6K | per group not applicable 2.8K; $0 per group 169; $150 per group 72; $30000 per group 51 |
| MEHBDEDCOMBINNOONINDIVIDUAL | category | 46 | 18.6K | Not Applicable 2.3K; $50  471; $0  169; $100  117 |
| MEHBDEDCOMBINNOONFAMILYPERPERSON | category | 45 | 18.6K | per person not applicable 2.3K; $50 per person 472; $0 per person 169; $100 per person 117 |
| MEHBDEDCOMBINNOONFAMILYPERGROUP | category | 35 | 18.6K | per group not applicable 2.7K; $150 per group 245; $0 per group 166; $200 per group 78 |
| DEHBDEDINNTIER1INDIVIDUAL | category | 48 | 20.0K | $0  860; $500  127; $400  125; $3,800  117 |
| DEHBDEDINNTIER1FAMILYPERPERSON | category | 48 | 20.0K | $0 per person 842; $500 per person 127; $400 per person 125; per person not applicable 119 |
| DEHBDEDINNTIER1FAMILYPERGROUP | category | 49 | 20.0K | $0 per group 830; per group not applicable 377; $1000 per group 120; $7600 per group 117 |
| DEHBDEDINNTIER1COINSURANCE | category | 11 | 20.0K | 0.00% 956; 50.00% 604; 40.00% 169; 30.00% 142 |
| DEHBDEDINNTIER2INDIVIDUAL | category | 25 | 21.4K | $0  285; $400  60; $600  48; $7,000  42 |
| DEHBDEDINNTIER2FAMILYPERPERSON | category | 25 | 21.4K | $0 per person 285; $400 per person 60; $600 per person 48; $7000 per person 42 |
| DEHBDEDINNTIER2FAMILYPERGROUP | category | 24 | 21.4K | $0 per group 281; per group not applicable 170; $14000 per group 42; $800 per group 24 |
| DEHBDEDINNTIER2COINSURANCE | category | 7 | 21.4K | 50.00% 271; 0.00% 169; 40.00% 108; 25.00% 30 |
| DEHBDEDOUTOFNETINDIVIDUAL | category | 4 | 20.0K | Not Applicable 1.9K; $0  178; $500  7; $7,600  3 |
| DEHBDEDOUTOFNETFAMILYPERPERSON | category | 4 | 20.0K | per person not applicable 1.9K; $0 per person 178; $500 per person 7; $7600 per person 3 |
| DEHBDEDOUTOFNETFAMILYPERGROUP | category | 3 | 20.0K | per group not applicable 1.9K; $0 per group 170; $15200 per group 3 |
| DEHBDEDCOMBINNOONINDIVIDUAL | category | 15 | 20.0K | Not Applicable 1.8K; $0  224; $250  29; $400  14 |
| DEHBDEDCOMBINNOONFAMILYPERPERSON | category | 15 | 20.0K | per person not applicable 1.8K; $0 per person 224; $250 per person 29; $400 per person 14 |
| DEHBDEDCOMBINNOONFAMILYPERGROUP | category | 10 | 20.0K | per group not applicable 1.8K; $0 per group 217; $2250 per group 10; $750 per group 9 |
| TEHBDEDINNTIER1INDIVIDUAL | who | 190 | 3.5K | $0  5.0K; $6,000  1.7K; $2,000  1.5K; $7,500  1.4K |
| TEHBDEDINNTIER1FAMILYPERPERSON | who | 196 | 3.5K | $0 per person 5.0K; $6000 per person 1.7K; $2000 per person 1.5K; $7500 per person 1.4K |
| TEHBDEDINNTIER1FAMILYPERGROUP | who | 201 | 3.5K | $0 per group 5.0K; $12000 per group 1.7K; $4000 per group 1.5K; $15000 per group 1.4K |
| TEHBDEDINNTIER1COINSURANCE | category | 13 | 3.5K | 0.00% 4.9K; 50.00% 4.4K; 40.00% 3.1K; 30.00% 2.1K |
| TEHBDEDINNTIER2INDIVIDUAL | who | 127 | 17.3K | $0  1.4K; $6,000  214; $5,500  174; $5,000  147 |
| TEHBDEDINNTIER2FAMILYPERPERSON | who | 126 | 17.3K | $0 per person 1.4K; $6000 per person 214; $5500 per person 174; $5000 per person 147 |
| TEHBDEDINNTIER2FAMILYPERGROUP | who | 129 | 17.3K | $0 per group 1.4K; $12000 per group 214; $11000 per group 174; $10000 per group 147 |
| TEHBDEDINNTIER2COINSURANCE | category | 11 | 17.3K | 50.00% 1.8K; 0.00% 1.1K; 30.00% 754; 40.00% 533 |
| TEHBDEDOUTOFNETINDIVIDUAL | who | 137 | 3.5K | Not Applicable 13.7K; $0  1.7K; $15,000  1.2K; $20,000  182 |
| TEHBDEDOUTOFNETFAMILYPERPERSON | who | 135 | 3.5K | per person not applicable 13.7K; $0 per person 1.7K; $15000 per person 1.2K; $20000 per person 176 |
| TEHBDEDOUTOFNETFAMILYPERGROUP | who | 131 | 3.5K | per group not applicable 13.8K; $0 per group 1.7K; $45000 per group 1.1K; $40000 per group 182 |
| TEHBDEDCOMBINNOONINDIVIDUAL | who | 135 | 3.5K | Not Applicable 15.4K; $0  1.7K; $7,500  86; $6,000  83 |
| TEHBDEDCOMBINNOONFAMILYPERPERSON | who | 133 | 3.5K | per person not applicable 15.4K; $0 per person 1.7K; $7500 per person 86; $6000 per person 83 |
| TEHBDEDCOMBINNOONFAMILYPERGROUP | who | 133 | 3.5K | per group not applicable 15.4K; $0 per group 1.7K; $15000 per group 86; $4000 per group 83 |
| ISHSAELIGIBLE | category | 2 | 1.4K | No 15.1K; Yes 5.6K |
| HSAORHRAEMPLOYERCONTRIBUTION | other | 1 | 21.7K | No 316 |
| HSAORHRAEMPLOYERCONTRIBUTIONAMOUNT | empty | 0 | 22.1K |  |
| URLFORSUMMARYOFBENEFITSCOVERAGE | other | 14.7K | 1.3K | https://edge.sitecoreclou 107; https://shop.yourwyoblue. 105; https://shop.yourwyoblue. 105; https://shop.yourwyoblue. 105 |
| PLANBROCHURE | who | 1.8K | 588 | https://www.bcbstx.com/pl 2.7K; http://file.anthem.com/20 594; https://www.hioscar.com/a 592; https://www.azblue.com/20 589 |
| INGESTED_AT | audit | 1 | 0 | 1786162645841662 22.1K |
| SOURCE_RUN_ID | audit | 1 | 0 | 7d2bb6bd-8659-405a-9ec5-8 22.1K |
| SRC_SHA256 | who | 1 | 0 | 27d589739a845f368a99476b6 22.1K |
