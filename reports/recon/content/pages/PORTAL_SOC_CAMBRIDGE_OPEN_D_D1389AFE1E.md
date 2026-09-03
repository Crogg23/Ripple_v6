# PORTAL_SOC_CAMBRIDGE_OPEN_D_D1389AFE1E

rows 1.1K  columns 18  scan 4.9s

roles: amount 2, audit 2, category 6, date 1, other 4, who 4

## when

INGESTED_AT
  2026      1.1K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_WORKERS_LCA | 1.1K | 1 | 1 | 2.91 | 100 | 1.3K |
| PREVAILING_WAGE | 1.1K | 20.95 | 99.0K | 223.4K | 288.3K | 112.04M |

## who

SOC_DETAILED by rows
       120  Biological Scientists, All Other
        95  Software Developers
        87  Data Scientists
        51  Medical Scientists, Except Epidemiologists
        46  Biochemists and Biophysicists
        37  Computer Occupations, All Other
        34  Operations Research Analysts
        30  Computer and Information Research Scientists
        26  Bioengineers and Biomedical Engineers
        22  Statisticians
        22  Computer and Information Systems Managers
        20  Market Research Analysts and Marketing Specialists
        20  Chemists
        19  Natural Sciences Managers
        15  Engineers, All Other
        14  nan
        14  Industrial Engineers
        14  Financial and Investment Analysts
        12  Project Management Specialists
        12  Software Quality Assurance Analysts and Testers

SOC_DETAILED by dollars
         222       95 rows  Software Developers
         120      120 rows  Biological Scientists, All Other
          87       87 rows  Data Scientists
          51       51 rows  Medical Scientists, Except Epidemiologists
          46       46 rows  Biochemists and Biophysicists
          37       37 rows  Computer Occupations, All Other
          34       34 rows  Operations Research Analysts
          31       22 rows  Computer and Information Systems Managers
          30       30 rows  Computer and Information Research Scientists
          26       26 rows  Bioengineers and Biomedical Engineers
          25        6 rows  Network and Computer Systems Administrators
          22       22 rows  Statisticians
          20       20 rows  Market Research Analysts and Marketing Specialists
          20       20 rows  Chemists
          19       19 rows  Natural Sciences Managers
          15       15 rows  Engineers, All Other
          14       12 rows  Computer Systems Analysts
          14       14 rows  Industrial Engineers
          14       14 rows  Financial and Investment Analysts
          14       14 rows  nan

SOC_BROAD_GROUP by rows
       167  Biological Scientists
       115  Software and Web Developers, Programmers, and Testers
        87  Data Scientists
        51  Medical Scientists
        40  Miscellaneous Computer Occupations
        34  Operations Research Analysts
        30  Computer and Information Research Scientists
        26  Chemists and Materials Scientists
        26  Bioengineers and Biomedical Engineers
        22  Computer and Information Systems Managers
        22  Statisticians
        21  Computer and Information Analysts
        20  Market Research Analysts and Marketing Specialists
        19  Natural Sciences Managers
        19  Database and Network Administrators and Architects
        16  Astronomers and Physicists
        16  Logisticians and Project Management Specialists
        15  Electrical and Electronics Engineers
        15  Miscellaneous Engineers
        14  Industrial Engineers, Including Health and Safety

SOC_BROAD_GROUP by dollars
         242      115 rows  Software and Web Developers, Programmers, and Testers
         167      167 rows  Biological Scientists
          87       87 rows  Data Scientists
          51       51 rows  Medical Scientists
          42       19 rows  Database and Network Administrators and Architects
          40       40 rows  Miscellaneous Computer Occupations
          34       34 rows  Operations Research Analysts
          31       22 rows  Computer and Information Systems Managers
          30       30 rows  Computer and Information Research Scientists
          26       26 rows  Bioengineers and Biomedical Engineers
          26       26 rows  Chemists and Materials Scientists
          23       21 rows  Computer and Information Analysts
          22       22 rows  Statisticians
          20       20 rows  Market Research Analysts and Marketing Specialists
          19       19 rows  Natural Sciences Managers
          16       16 rows  Astronomers and Physicists
          16       16 rows  Logisticians and Project Management Specialists
          15       15 rows  Miscellaneous Engineers
          15       15 rows  Electrical and Electronics Engineers
          14       14 rows  Designers

NAICS_INDUSTRY_GROUP by rows
       268  Scientific Research and Development Services
       167  Pharmaceutical and Medicine Manufacturing
       154  Colleges, Universities, and Professional Schools
       101  Computer Systems Design and Related Services
        41  Management, Scientific, and Technical Consulting Services
        35  Architectural, Engineering, and Related Services
        34  Software Publishers
        31  Medical and Diagnostic Laboratories
        26  Computing Infrastructure Providers, Data Processing, Web Hosting, and 
        20  General Medical and Surgical Hospitals
        18  Web Search Portals, Libraries, Archives, and Other Information Service
        14  Semiconductor and Other Electronic Component Manufacturing
        13  Other Financial Investment Activities
        12  Accounting, Tax Preparation, Bookkeeping, and Payroll Services
        12  Educational Support Services
        10  Advertising, Public Relations, and Related Services
        10  Newspaper, Periodical, Book, and Directory Publishers
         9  Computer and Peripheral Equipment Manufacturing
         8  Other Professional, Scientific, and Technical Services
         7  Health and Personal Care Stores

NAICS_INDUSTRY_GROUP by dollars
         268      268 rows  Scientific Research and Development Services
         167      167 rows  Pharmaceutical and Medicine Manufacturing
         154      154 rows  Colleges, Universities, and Professional Schools
         133       34 rows  Software Publishers
         111      101 rows  Computer Systems Design and Related Services
          41       41 rows  Management, Scientific, and Technical Consulting Services
          35       35 rows  Architectural, Engineering, and Related Services
          33       14 rows  Semiconductor and Other Electronic Component Manufacturing
          31       31 rows  Medical and Diagnostic Laboratories
          26       26 rows  Computing Infrastructure Providers, Data Processing, Web Hos
          24        9 rows  Computer and Peripheral Equipment Manufacturing
          24        6 rows  Electronic Shopping and Mail-Order Houses
          20       20 rows  General Medical and Surgical Hospitals
          19       10 rows  Newspaper, Periodical, Book, and Directory Publishers
          18       18 rows  Web Search Portals, Libraries, Archives, and Other Informati
          13       13 rows  Other Financial Investment Activities
          12       12 rows  Educational Support Services
          12       12 rows  Accounting, Tax Preparation, Bookkeeping, and Payroll Servic
          10       10 rows  Advertising, Public Relations, and Related Services
           9        3 rows  Child Care Services

SRC_SHA256 by rows
      1.1K  f121ec577899c8aae65c94d65cf1064952f96732bfbcd5292c3bb5989062efcf

SRC_SHA256 by dollars
        1.3K     1.1K rows  f121ec577899c8aae65c94d65cf1064952f96732bfbcd5292c3bb5989062

## who x when

SOC_DETAILED by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_WORKERS_LCA
  Biochemists and Biophysicists             2026:46
  Bioengineers and Biomedical Engineers     2026:26
  Biological Scientists, All Other          2026:120
  Chemists                                  2026:20
  Computer Occupations, All Other           2026:37
  Computer Systems Analysts                 2026:14
  Computer and Information Research Scient  2026:30
  Computer and Information Systems Manager  2026:31
  Data Scientists                           2026:87
  Engineers, All Other                      2026:15
  Financial and Investment Analysts         2026:14
  Industrial Engineers                      2026:14
  Market Research Analysts and Marketing S  2026:20
  Medical Scientists, Except Epidemiologis  2026:51
  Natural Sciences Managers                 2026:19
  Network and Computer Systems Administrat  2026:25
  Operations Research Analysts              2026:34
  Project Management Specialists            2026:12
  Software Developers                       2026:222
  Software Quality Assurance Analysts and   2026:12
  Statisticians                             2026:22
  nan                                       2026:14

SOC_BROAD_GROUP by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_WORKERS_LCA
  Astronomers and Physicists                2026:16
  Bioengineers and Biomedical Engineers     2026:26
  Biological Scientists                     2026:167
  Chemists and Materials Scientists         2026:26
  Computer and Information Analysts         2026:23
  Computer and Information Research Scient  2026:30
  Computer and Information Systems Manager  2026:31
  Data Scientists                           2026:87
  Database and Network Administrators and   2026:42
  Designers                                 2026:14
  Electrical and Electronics Engineers      2026:15
  Industrial Engineers, Including Health a  2026:14
  Logisticians and Project Management Spec  2026:16
  Market Research Analysts and Marketing S  2026:20
  Medical Scientists                        2026:51
  Miscellaneous Computer Occupations        2026:40
  Miscellaneous Engineers                   2026:15
  Natural Sciences Managers                 2026:19
  Operations Research Analysts              2026:34
  Software and Web Developers, Programmers  2026:242
  Statisticians                             2026:22

## what

STATUS: Certified 83%, Certified-Withdrawn 14%, Withdrawn 2%, Denied 1%

SOC_MAJOR_GROUP: Computer and Mathematical Occu 34%, Life, Physical, and Social Sci 27%, Architecture and Engineering O 11%, Management Occupations 10%, Business and Financial Operati 9%, Educational Instruction and Li 5%, Arts, Design, Entertainment, S 2%, Healthcare Practitioners and T 0%, Community and Social Service O 0%, Legal Occupations 0%, Sales and Related Occupations 0%

SOC_MINOR_GROUP: Computer Occupations 22%, Life Scientists 21%, Mathematical Science Occupatio 14%, Engineers 11%, Business Operations Specialist 7%, Physical Scientists 5%, Postsecondary Teachers 5%, Other Management Occupations 4%, Operations Specialties Manager 4%, Financial Specialists 3%, Social Scientists and Related  2%, Art and Design Workers 1%

NAICS_SECTOR: Professional, Scientific, and  44%, Manufacturing 20%, Educational Services 16%, Information 8%, Health Care and Social Assista 6%, Finance and Insurance 3%, Retail Trade 1%, Other Services (except Public  1%, Real Estate and Rental and Lea 0%, Wholesale Trade 0%, Administrative and Support and 0%, Arts, Entertainment, and Recre 0%

NAICS_SUBSECTOR: Professional, Scientific, and  47%, Educational Services 17%, Chemical Manufacturing 16%, Ambulatory Health Care Service 4%, Publishing Industries 3%, Computer and Electronic Produc 3%, Computing Infrastructure Provi 3%, Hospitals 2%, Web Search Portals, Libraries, 2%, Securities, Commodity Contract 1%, Credit Intermediation and Rela 1%, Religious, Grantmaking, Civic, 1%

PW_UNIT_OF_PAY: Year 94%, Hour 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FY | other | 1 | 0 | 2025 1.1K |
| PROGRAM | other | 1 | 0 | LCA 1.1K |
| STATUS | category | 4 | 0 | Certified 921; Certified-Withdrawn 157; Withdrawn 23; Denied 9 |
| SOC_CODE | other | 175 | 0 | 15-1252.00 95; 15-2051.00 52; 19-1042.00 51; 19-1021.00 46 |
| SOC_MAJOR_GROUP | category | 11 | 0 | Computer and Mathematical 379; Life, Physical, and Socia 303; Architecture and Engineer 124; Management Occupations 110 |
| SOC_MINOR_GROUP | category | 28 | 0 | Computer Occupations 230; Life Scientists 221; Mathematical Science Occu 149; Engineers 111 |
| SOC_BROAD_GROUP | who | 102 | 0 | Biological Scientists 167; Software and Web Develope 115; Data Scientists 87; Medical Scientists 51 |
| SOC_DETAILED | who | 141 | 0 | Biological Scientists, Al 120; Software Developers 95; Data Scientists 87; Medical Scientists, Excep 51 |
| NAICS_CODE | other | 136 | 0 | 541714 121; 6113 91; 54171 82; 32541 70 |
| NAICS_SECTOR | category | 17 | 0 | Professional, Scientific, 484; Manufacturing 219; Educational Services 171; Information 91 |
| NAICS_SUBSECTOR | category | 39 | 0 | Professional, Scientific, 484; Educational Services 171; Chemical Manufacturing 167; Ambulatory Health Care Se 41 |
| NAICS_INDUSTRY_GROUP | who | 74 | 0 | Scientific Research and D 268; Pharmaceutical and Medici 167; Colleges, Universities, a 154; Computer Systems Design a 101 |
| TOTAL_WORKERS_LCA | amount | 9 | 0 | 1 1.1K; 5 4; 10 3; 2 3 |
| PREVAILING_WAGE | amount | 473 | 0 | 122970 34; 85842 25; 102856 22; 125819 21 |
| PW_UNIT_OF_PAY | category | 2 | 0 | Year 1.0K; Hour 64 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:46:44.59350 1.1K |
| SOURCE_RUN_ID | audit | 1 | 0 | 5ccc72a5-b58e-45a7-8865-b 1.1K |
| SRC_SHA256 | who | 1 | 0 | f121ec577899c8aae65c94d65 1.1K |
