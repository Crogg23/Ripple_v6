# PORTAL_CKA_HOUSTON_OPEN_DAT_BC15145E45

rows 4.7K  columns 17  scan 2.8s

roles: audit 2, category 8, date 1, other 4, who 3

## when

INGESTED_AT
  2026      4.7K  ##############################

## who

GL_ACCOUNT by rows
        63  502010
        63  503090
        62  503010
        62  501070
        62  500010
        62  503015
        62  503060
        62  501075
        61  511070
        58  522430
        57  520114
        55  522721
        55  522830
        54  522724
        54  522726
        54  520765
        54  522728
        53  522722
        53  522727
        52  520905

GL_DESCRIPTION by rows
        63  Workers Compensation-Civilian-Admin
        63  FICA - Civilian
        62  Pension Legacy-Civilian
        62  Pension - Civilian
        62  Long Term Disability-Civilian
        62  Health Ins-Act Civilian
        62  Basic Life Insurance - Active Civilian
        62  Salary Base Pay - Civilian
        61  Misc Office Supplies
        58  Misc Other Services & Charges
        57  Miscellaneous Support Services
        57  Interfund GIS Services
        56  Interfund HR Client Services
        54  Interfund - Data Services Exp
        54  Interfund - Application Services Exp
        54  Interfund - Wireless Services Exp
        54  Membership & Professional Fees
        53  Interfund KRONOS Service Chargeback
        53  Interfund - Voice Services Exp
        52  Travel - Training Related

SRC_SHA256 by rows
      4.7K  ab7fa8525cf00945380243ab06d4d6e1735064a690eb0a55669cf3887bb98adc

## who x when

GL_ACCOUNT by INGESTED_AT  LOAD STAMP, not an event date
  500010                                    2026:62
  501070                                    2026:62
  501075                                    2026:62
  502010                                    2026:63
  503010                                    2026:62
  503015                                    2026:62
  503060                                    2026:62
  503090                                    2026:63
  511070                                    2026:61
  520114                                    2026:57
  520765                                    2026:54
  520905                                    2026:52
  522430                                    2026:58
  522721                                    2026:55
  522722                                    2026:53
  522724                                    2026:54
  522726                                    2026:54
  522727                                    2026:53
  522728                                    2026:54
  522830                                    2026:55

GL_DESCRIPTION by INGESTED_AT  LOAD STAMP, not an event date
  Basic Life Insurance - Active Civilian    2026:62
  FICA - Civilian                           2026:63
  Health Ins-Act Civilian                   2026:62
  Interfund - Application Services Exp      2026:54
  Interfund - Data Services Exp             2026:54
  Interfund - Voice Services Exp            2026:53
  Interfund - Wireless Services Exp         2026:54
  Interfund GIS Services                    2026:57
  Interfund HR Client Services              2026:56
  Interfund KRONOS Service Chargeback       2026:53
  Long Term Disability-Civilian             2026:62
  Membership & Professional Fees            2026:54
  Misc Office Supplies                      2026:61
  Misc Other Services & Charges             2026:58
  Miscellaneous Support Services            2026:57
  Pension - Civilian                        2026:62
  Pension Legacy-Civilian                   2026:62
  Salary Base Pay - Civilian                2026:62
  Travel - Training Related                 2026:52
  Workers Compensation-Civilian-Admin       2026:63

## what

FUND_ID: 1000 51%, 1002 8%, 8300 7%, 8001 6%, 2301 5%, 2312 4%, 1001 4%, 2302 4%, 8700 3%, 1004 3%, 1005 3%, 2105 3%

FUND_NAME: General Fund 51%, Central Service 8%, Wtr&SwrSystOperating 7%, HAS-Revenue 6%, Building Inspection 5%, DDSRF - Metro ET AL 4%, Project Cost Recovry 4%, Stormwater Fund 4%, ParkHouston Special Revenue Fu 3%, Property & Casualty 3%, Fleet Management 3%, M.R.R Fund 3%

FUND_TYPE: Special Revenue Funds 40%, General Funds 34%, Service Chargeback Funds 14%, Enterprise Funds 10%, Internal Services Funds 2%

DEPARTMENT_ID: 2000 26%, 3800 11%, 1000 10%, 3600 10%, 6500 10%, 8000 6%, 2500 5%, 2800 5%, 2100 5%, 5000 5%, 1200 4%, 9000 4%

DEPARTMENT_NAME: Houston Public Works - HPW 26%, Houston Health Department 11%, Houston Police Department-HPD 10%, Parks & Recreation 10%, Admn. & Regulatory Affairs 10%, Human Resources Dept. 6%, General Services Department 5%, Houston Airport System (HAS) 5%, Solid Waste Management 5%, Mayor's Office 5%, Houston Fire Department (HFD) 4%, Legal Department 4%

DEPARTMENT_TYPE: Development & Maintenance Serv 30%, Administrative Services 27%, Human & Cultural Services 20%, Public Safety 15%, Enterprise Funds 4%, Revolving Funds 2%, General Government 1%, Debt Service 0%

GL_CATEGORY: Other Services and Charges 49%, Personnel Services 21%, Supplies 14%, Charges for Services 4%, Miscellaneous/Other 2%, Licenses and Permits 2%, Debt Service and Other Uses 2%, Non-Capital Equipment 2%, Equipment 1%, Direct Interfund Services 1%, Interest 1%, Other Resources 1%

REVENUE_OR_EXPENDITURE: Expenditures 87%, Revenues 13%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FISCAL_YEAR | other | 1 | 0 | 2025 4.7K |
| FUND_ID | category | 49 | 0 | 1000 1.6K; 1002 239; 8300 229; 8001 175 |
| FUND_NAME | category | 49 | 0 | General Fund 1.6K; Central Service 239; Wtr&SwrSystOperating 229; HAS-Revenue 175 |
| FUND_TYPE | category | 5 | 0 | Special Revenue Funds 1.9K; General Funds 1.6K; Service Chargeback Funds 636; Enterprise Funds 458 |
| DEPARTMENT_ID | category | 28 | 0 | 2000 922; 3800 402; 1000 349; 3600 341 |
| DEPARTMENT_NAME | category | 28 | 0 | Houston Public Works - HP 922; Houston Health Department 402; Houston Police Department 349; Parks & Recreation 341 |
| DEPARTMENT_TYPE | category | 8 | 0 | Development & Maintenance 1.4K; Administrative Services 1.3K; Human & Cultural Services 941; Public Safety 699 |
| GL_ACCOUNT | who | 697 | 0 | 503090 63; 502010 63; 503060 62; 503015 62 |
| GL_DESCRIPTION | who | 665 | 0 | Workers Compensation-Civi 63; FICA - Civilian 63; Long Term Disability-Civi 62; Basic Life Insurance - Ac 62 |
| GL_CATEGORY | category | 24 | 0 | Other Services and Charge 2.2K; Personnel Services 959; Supplies 646; Charges for Services 195 |
| REVENUE_OR_EXPENDITURE | category | 2 | 0 | Expenditures 4.0K; Revenues 615 |
| C_CURRENT | other | 3.1K | 0 | 0 295; 2000 47; 1000 46; 5000 44 |
| ADOPTED | other | 3.1K | 0 | 0 309; 1000 46; 2000 45; 5000 44 |
| ACTUALS | other | 2.6K | 0 | 0 1.7K; 1521450 16; 145780 15; 57957 15 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:32:59.61887 4.7K |
| SOURCE_RUN_ID | audit | 1 | 0 | 94cf8904-51e3-4012-80f6-5 4.7K |
| SRC_SHA256 | who | 1 | 0 | ab7fa8525cf00945380243ab0 4.7K |
