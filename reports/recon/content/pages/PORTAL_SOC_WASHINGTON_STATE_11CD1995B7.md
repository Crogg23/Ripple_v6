# PORTAL_SOC_WASHINGTON_STATE_11CD1995B7

rows 5.0K  columns 22  scan 4.5s

roles: amount 1, audit 2, category 1, date 2, id 1, other 4, state 1, who 11

## when

OPENEDDATE
  2026      5.0K  ##############################

INGESTED_AT
  2026      5.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ACTUALSAVINGS | 5.0K | 0 | 0 | 89.16 | 93.7K | 238.7K |

## who

BUSINESSNAME by rows
       209  Amazon.com
       154  Live Nation Entertainment Inc
       116  Comcast/Xfinity
       106  Alexandra Lozano Immigration Law
        87  Facebook/Meta
        60  Unnamed Business
        59  T-Mobile
        57  Microsoft Corporation
        39  Glenwood Mobile Estates
        27  StubHub Inc
        24  CenturyLink
        23  Verizon Wireless
        23  Multicare Health Systems
        23  Expedia
        23  Private Individual
        22  AT&T Office of the President
        21  Google Incorporated
        21  ADT Security/Protection One Alarm Services
        20  Door Dash
        19  Lowe's Home Improvement

BUSINESSNAME by dollars
       93.7K       10 rows  General Motors
       45.0K        5 rows  Gee Automotive Companies
        9.8K      209 rows  Amazon.com
        9.0K        3 rows  Younker Nissan of Renton
        7.3K       14 rows  Home Depot
        5.8K        9 rows  Synchrony Bank
        3.2K        7 rows  UW Medicine
        3.0K       23 rows  Verizon Wireless
        1.9K       23 rows  Expedia
        1.6K        3 rows  Toyota of Seattle
      936.52        7 rows  eHarmony
      550.66        2 rows  Verizon Wireline
         300       22 rows  AT&T Office of the President
      256.96       10 rows  Best Buy
         224        4 rows  Diamond Parking dba Parking Services Appeals Department
          50       20 rows  Door Dash
       20.06       18 rows  Parking Revenue Recovery Services
           0        1 rows  Toyota Financial Services
           0        1 rows  GENERALI ASSICURAZIONI GENERALI S.P.A. aka Generali Global A
           0        1 rows  Lincoln Towing

PRACTICENAME by rows
      2.7K  Other/Miscellaneous
       224  Internet & Mobile device based transaction
       187  Billing Issues
       179  Questionable Quality Product/Service
       168  Failure To Adjust/Refund
       144  Unsatisfactory Repair/Service
       132  Failure To Deliver/Perform
        73  Misrepresentation of product or service
        69  Landlord/Tenant - Residential
        69  Right To Cancel
        65  Non-Fulfillment
        57  Misrepresentation of Terms
        51  Outside Scope of Services
        42  Collection Practices
        39  Notario Issue
        37  Excessive Price or Charge
        36  Governement agency complaint
        35  Charge:Service Not Performed/Product not delivered
        32  Unauthorized Debit
        32  Warranty

PRACTICENAME by dollars
       94.7K      144 rows  Unsatisfactory Repair/Service
       24.5K       42 rows  Collection Practices
       24.3K        5 rows  Mortgage Servicing Issue
       22.8K       73 rows  Misrepresentation of product or service
       22.5K       30 rows  Used Motor Vehicle Issue
       19.8K      168 rows  Failure To Adjust/Refund
        5.6K      224 rows  Internet & Mobile device based transaction
        5.4K      187 rows  Billing Issues
        5.3K      179 rows  Questionable Quality Product/Service
        2.7K       35 rows  Charge:Service Not Performed/Product not delivered
        2.4K      132 rows  Failure To Deliver/Perform
        1.4K       57 rows  Misrepresentation of Terms
        1.2K       30 rows  Credit/Financing
        1.2K       28 rows  Alleged criminal activity
        1.2K       16 rows  Identity Theft
         830       29 rows  Advertising
         800        5 rows  Packing
      468.26       69 rows  Right To Cancel
      425.01        7 rows  Charge Above Estimate
         313        7 rows  Failure To Provide Title/Registration

BUSINESSCATEGORY by rows
       386  Electronic Shopping
       333  Auto Sales
       303  Retail Sales
       258  Residential Landlord
       257  Health Care
       196  Unclassified Establishments
       196  Contractors
       179  Promoters of performing arts, sports & similar eve
       169  Telecommunications
       159  Legal Services
       155  Broadband Providers
       132  Auto Repair
       126  Government Agencies
       123  Travel
       123  MHU Use Only - MH landlord
       111  Dating Clubs and Social Networking
       105  Collections
       104  Insurance
       103  Software Publishers
        86  Financing

BUSINESSCATEGORY by dollars
       93.7K       36 rows  Automobile Manufacturing
       55.9K      333 rows  Auto Sales
       48.7K       61 rows  Consumer Lending & Transfer Agents
       14.6K      303 rows  Retail Sales
        9.8K      386 rows  Electronic Shopping
        4.8K       32 rows  Amusement & Recreational Industries
        3.8K      169 rows  Telecommunications
        3.2K      257 rows  Health Care
        1.9K      123 rows  Travel
      936.52      111 rows  Dating Clubs and Social Networking
         696       35 rows  Educational Services
      244.06       42 rows  Parking Lots & Garages
      236.04      104 rows  Insurance
          50       67 rows  Couriers & Express Delivery Services
           0       11 rows  Accounting, Tax Preparation Bookkeeping & Payroll 
           0       12 rows  Waste Management Services
           0        3 rows  Funeral Homes
           0        7 rows  Advertising & Related Services (includes coupon bo
           0        4 rows  General Warehousing
           0       13 rows  Personal Care Services

NAICS by rows
       386  454100-Electronic Shopping & Mail Order Houses
       317  441100-Automotive Dealers
       246  531311-Residential property managers (includes landlords)
       196  990000-Unclassified Establishments
       179  711300-Promoters of performing arts, sports & similar eve
       133  514191-Internet service providers/info. services (doesn't
       123  531190-MHU Use Only - MH landlord
       118  811100-Automotive Repair & Maintenance
       116  513320-Telecommunications/Wireless
       111  812199-Dating Clubs and Social Networking
       109  541100-Legal Services- Attorneys
       105  561440-Collection Agencies
       104  524000-Insurance Carriers & Related Activities
       103  511210-Software Publishers
        99  233000-General Contracting, building, & developing
        86  235000-Special trade Contractors (includes plumbers, elec
        85  621100-Office of Physicians
        72  920000-Public Administration
        69  721100-Travel Accomodations
        67  492110-Couriers & Express Delivery Services

NAICS by dollars
       93.7K       36 rows  336111-Automobile Manufacturing
       55.6K      317 rows  441100-Automotive Dealers
       48.7K       60 rows  522291-Consumer Lending (includes Payday Lenders)
       13.1K       48 rows  444000-Building materials (incl. plumbing stores), garden
        9.8K      386 rows  454100-Electronic Shopping & Mail Order Houses
        4.8K       32 rows  713990-Amusement & Recreational Industries
        3.5K      116 rows  513320-Telecommunications/Wireless
        3.2K       85 rows  621100-Office of Physicians
        1.9K       27 rows  561510-Travel Agents
        1.3K       21 rows  454300-Direct Selling Establishments (including home fuel
      936.52      111 rows  812199-Dating Clubs and Social Networking
         696       35 rows  611000-Educational Services
         313       13 rows  441210-RV Dealers
         300       49 rows  513310-Wired Telecommunications Carriers
      256.96       25 rows  443000-Electronics/appliance stores
      244.06       42 rows  812930-Parking Lots & Garages
      236.04      104 rows  524000-Insurance Carriers & Related Activities
          50       67 rows  492110-Couriers & Express Delivery Services
           0       11 rows  238220-Solar Electric and Heating Installation
           0        1 rows  921110-Executive offices

## who x when

BUSINESSNAME by OPENEDDATE, dollars = ACTUALSAVINGS
  ADT Security/Protection One Alarm Servic  2026:0
  AT&T Office of the President              2026:300
  Alexandra Lozano Immigration Law          2026:0
  Amazon.com                                2026:9.8K
  Best Buy                                  2026:256.96
  CenturyLink                               2026:0
  Comcast/Xfinity                           2026:0
  Door Dash                                 2026:50
  Expedia                                   2026:1.9K
  Facebook/Meta                             2026:0
  Gee Automotive Companies                  2026:45.0K
  General Motors                            2026:93.7K
  Glenwood Mobile Estates                   2026:0
  Google Incorporated                       2026:0
  Home Depot                                2026:7.3K
  Live Nation Entertainment Inc             2026:0
  Lowe's Home Improvement                   2026:0
  Microsoft Corporation                     2026:0
  Multicare Health Systems                  2026:0
  Private Individual                        2026:0
  StubHub Inc                               2026:0
  Synchrony Bank                            2026:5.8K
  T-Mobile                                  2026:0
  Toyota of Seattle                         2026:1.6K
  UW Medicine                               2026:3.2K
  Unnamed Business                          2026:0
  Verizon Wireless                          2026:3.0K
  Verizon Wireline                          2026:550.66
  Younker Nissan of Renton                  2026:9.0K
  eHarmony                                  2026:936.52

PRACTICENAME by OPENEDDATE, dollars = ACTUALSAVINGS
  Advertising                               2026:830
  Alleged criminal activity                 2026:1.2K
  Billing Issues                            2026:5.4K
  Charge Above Estimate                     2026:425.01
  Charge:Service Not Performed/Product not  2026:2.7K
  Collection Practices                      2026:24.5K
  Credit/Financing                          2026:1.2K
  Excessive Price or Charge                 2026:0
  Failure To Adjust/Refund                  2026:19.8K
  Failure To Deliver/Perform                2026:2.4K
  Failure To Provide Title/Registration     2026:313
  Governement agency complaint              2026:0
  Identity Theft                            2026:1.2K
  Internet & Mobile device based transacti  2026:5.6K
  Landlord/Tenant - Residential             2026:0
  Misrepresentation of Terms                2026:1.4K
  Misrepresentation of product or service   2026:22.8K
  Mortgage Servicing Issue                  2026:24.3K
  Non-Fulfillment                           2026:0
  Notario Issue                             2026:0
  Other/Miscellaneous                       2026:0
  Outside Scope of Services                 2026:0
  Packing                                   2026:800
  Questionable Quality Product/Service      2026:5.3K
  Right To Cancel                           2026:468.26
  Unauthorized Debit                        2026:232
  Unsatisfactory Repair/Service             2026:94.7K
  Used Motor Vehicle Issue                  2026:22.5K
  Warranty                                  2026:0

## where

BUSINESSSTATE: WA 2.8K, CA 608, TX 124, FL 120, IL 85, NY 76, NM 61, NC 53, GA 49, CO 49, MN 48

## what

STATUS: New 59%, Open 23%, Closed 18%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OPENEDDATE | date | 25 | 0 | 2026-05-21T00:00:00.000 396; 2026-05-22T00:00:00.000 376; 2026-05-27T00:00:00.000 372; 2026-05-26T00:00:00.000 358 |
| OPENEDYEAR | other | 1 | 0 | 2026 5.0K |
| STATUS | category | 3 | 0 | New 3.0K; Open 1.2K; Closed 882 |
| PRACTICECODE | other | 118 | 0 | 999 2.7K; 203 224; 316 187; 303 179 |
| PRACTICENAME | who | 118 | 0 | Other/Miscellaneous 2.7K; Internet & Mobile device  224; Billing Issues 187; Questionable Quality Prod 179 |
| BUSINESSCATEGORY | who | 113 | 0 | Electronic Shopping 386; Auto Sales 333; Retail Sales 303; Residential Landlord 258 |
| NAICS | who | 161 | 0 | 454100-Electronic Shoppin 386; 441100-Automotive Dealers 317; 531311-Residential proper 246; 990000-Unclassified Estab 196 |
| BUSINESSNAME | who | 951 | 1.4K | Amazon.com 209; Live Nation Entertainment 154; Comcast/Xfinity 116; Alexandra Lozano Immigrat 106 |
| BUSINESSSTREETLINE1 | who | 873 | 1.7K | PO Box 81226 209; 9348 Civic Ctr Dr 154; 1323 34th Ave 116; 6720 Fort Dent Way Ste 23 109 |
| BUSINESSSTREETLINE2 | who | 75 | 4.6K | 2375 130th Ave NE Ste 102 39; MS: 1313-5-CUS 23; 8th Fl, South Tower 20; PO Box 560947 19 |
| BUSINESSCITY | who | 457 | 563 | Seattle 599; Bellevue 171; Beverly Hills 154; Tukwila 137 |
| BUSINESSSTATE | state | 48 | 319 | WA 2.8K; CA 608; TX 124; FL 120 |
| BUSINESSZIP | who | 765 | 730 | 98108-1226 209; 90210     154; 98424     121; 98188-2589 106 |
| ESTIMATEDSAVINGS | other | 1 | 0 | 0.00 5.0K |
| PRACTICEID | other | 120 | 0 | 60 2.7K; 27 224; 107 187; 35 179 |
| ACTUALSAVINGS | amount | 32 | 0 | 0.00 4.9K; 1160.73 5; 232.00 3; 66.32 3 |
| COMPLAINTID | who | 2.9K | 0 | 723122 28; 723223 27; 723203 27; 723097 27 |
| BUSINESSID | who | 1.8K | 1 | 120419 209; 143328 156; 204915 116; 346763 106 |
| ID | id | 4.9K | 0 | 6000723029 25; 60000723072 25; 6000723065 25; 60000723073 25 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:47:02.75898 5.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | ab594ea7-3bdc-4c83-84bd-c 5.0K |
| SRC_SHA256 | who | 1 | 0 | a308ac95babdbd639a28afdb7 5.0K |
