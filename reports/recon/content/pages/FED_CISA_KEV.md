# FED_CISA_KEV

rows 1.7K  columns 14  scan 3.1s

roles: audit 2, category 2, date 2, id 2, other 1, who 5

## when

DATE_ADDED
  2021       311  #################
  2022       555  ##############################
  2023       187  ##########
  2024       186  ##########
  2025       245  #############
  2026       190  ##########

DUE_DATE
  2021       111  ####
  2022       747  ##############################
  2023       193  ########
  2024       178  #######
  2025       247  ##########
  2026       198  ########

## who

VULNERABILITY_NAME by rows
        23  Microsoft Win32k Privilege Escalation Vulnerability
        19  Google Chromium V8 Type Confusion Vulnerability
        11  Apple Multiple Products Memory Corruption Vulnerability
        11  Microsoft Windows Kernel Privilege Escalation Vulnerability
         9  Microsoft Windows Privilege Escalation Vulnerability
         8  Microsoft Internet Explorer Memory Corruption Vulnerability
         8  Adobe Flash Player Use-After-Free Vulnerability
         8  Microsoft Exchange Server Remote Code Execution Vulnerability
         7  Cisco IOS and IOS XE Software SNMP Remote Code Execution Vulnerability
         7  Microsoft Internet Explorer Use-After-Free Vulnerability
         6  Microsoft Office Memory Corruption Vulnerability
         6  Microsoft Internet Explorer Scripting Engine Memory Corruption Vulnera
         5  Adobe ColdFusion Deserialization of Untrusted Data Vulnerability
         5  Oracle WebLogic Server Unspecified Vulnerability
         5  Oracle Fusion Middleware Unspecified Vulnerability
         5  Synacor Zimbra Collaboration Suite (ZCS) Cross-Site Scripting (XSS) Vu
         5  Qualcomm Multiple Chipsets Use-After-Free Vulnerability
         5  Linux Kernel Privilege Escalation Vulnerability
         5  Cisco Small Business RV Series Routers Stack-based Buffer Overflow Vul
         4  Microsoft Office Remote Code Execution Vulnerability

VENDOR_PROJECT by rows
       385  Microsoft
        96  Cisco
        94  Apple
        80  Adobe
        72  Google
        45  Oracle
        40  Apache
        35  Ivanti
        29  Fortinet
        26  Linux
        26  VMware
        26  D-Link
        22  Citrix
        19  Synacor
        17  SonicWall
        17  Android
        15  Samsung
        15  Palo Alto Networks
        14  SAP
        13  Mozilla

PRODUCT by rows
       170  Windows
        79  Multiple Products
        39  Chromium V8
        36  Internet Explorer
        33  Flash Player
        29  Office
        29  Kernel
        25  Win32k
        17  Exchange Server
        16  Zimbra Collaboration Suite (ZCS)
        16  ColdFusion
        14  IOS and IOS XE Software
        13  Mobile Devices
        13  Acrobat and Reader
        12  WebLogic Server
        12  PAN-OS
        11  Multiple Chipsets
        11  iOS, iPadOS, and macOS
        10  NetWeaver
         9  FortiOS

CWES by rows
        94  CWE-78
        91  CWE-20
        90  CWE-416
        84  CWE-119
        84  CWE-787
        71  CWE-22
        63  CWE-94
        61  CWE-502
        37  CWE-287
        33  CWE-284
        33  CWE-306
        32  CWE-843
        31  CWE-264
        28  CWE-89
        27  CWE-79
        24  CWE-200
        23  CWE-77
        20  CWE-434
        18  CWE-122
        18  CWE-288

## who x when

VULNERABILITY_NAME by DATE_ADDED
  Adobe ColdFusion Deserialization of Untr  2021:1 2023:2 2024:2
  Adobe Flash Player Use-After-Free Vulner  2021:1 2022:7
  Apple Multiple Products Memory Corruptio  2021:2 2022:5 2024:3 2025:1
  Cisco IOS and IOS XE Software SNMP Remot  2022:6 2023:1
  Cisco Small Business RV Series Routers S  2022:5
  Google Chromium V8 Type Confusion Vulner  2021:5 2022:5 2023:2 2024:4 2025:3
  Linux Kernel Privilege Escalation Vulner  2022:5
  Microsoft Exchange Server Remote Code Ex  2021:7 2022:1
  Microsoft Internet Explorer Memory Corru  2021:1 2022:6 2023:1
  Microsoft Internet Explorer Scripting En  2021:6
  Microsoft Internet Explorer Use-After-Fr  2022:4 2024:1 2026:2
  Microsoft Office Memory Corruption Vulne  2021:4 2022:2
  Microsoft Office Remote Code Execution V  2021:1 2022:3
  Microsoft Win32k Privilege Escalation Vu  2021:9 2022:13 2023:1
  Microsoft Windows Kernel Privilege Escal  2021:4 2022:6 2024:1
  Microsoft Windows Privilege Escalation V  2021:1 2022:7 2025:1
  Oracle Fusion Middleware Unspecified Vul  2021:1 2022:3 2023:1
  Oracle WebLogic Server Unspecified Vulne  2021:1 2022:1 2023:1 2025:1 2026:1
  Qualcomm Multiple Chipsets Use-After-Fre  2021:1 2023:2 2024:1 2025:1
  Synacor Zimbra Collaboration Suite (ZCS)  2022:1 2023:2 2025:2

VENDOR_PROJECT by DATE_ADDED
  Adobe                                     2021:5 2022:54 2023:6 2024:8 2025:3 2026:4
  Android                                   2021:2 2022:3 2023:2 2024:6 2025:3 2026:1
  Apache                                    2021:12 2022:13 2023:5 2024:5 2025:3 2026:2
  Apple                                     2021:23 2022:26 2023:21 2024:7 2025:9 2026:8
  Cisco                                     2021:11 2022:50 2023:7 2024:6 2025:8 2026:14
  Citrix                                    2021:6 2022:5 2023:3 2024:2 2025:5 2026:1
  D-Link                                    2021:2 2022:10 2023:2 2024:6 2025:5 2026:1
  Fortinet                                  2021:4 2022:5 2023:2 2024:4 2025:8 2026:6
  Google                                    2021:23 2022:21 2023:7 2024:9 2025:7 2026:5
  Ivanti                                    2021:9 2023:3 2024:11 2025:7 2026:5
  Linux                                     2021:1 2022:8 2023:3 2024:4 2025:7 2026:3
  Microsoft                                 2021:83 2022:165 2023:27 2024:36 2025:39 2026:35
  Mozilla                                   2021:3 2022:7 2023:1 2024:1 2025:1
  Oracle                                    2021:7 2022:22 2023:4 2024:4 2025:5 2026:3
  Palo Alto Networks                        2022:4 2024:7 2025:2 2026:2
  SAP                                       2021:6 2022:4 2024:1 2025:3
  Samsung                                   2022:3 2023:8 2025:3 2026:1
  SonicWall                                 2021:5 2022:4 2024:1 2025:5 2026:2
  Synacor                                   2022:7 2023:2 2024:1 2025:4 2026:5
  VMware                                    2021:8 2022:8 2023:2 2024:5 2025:3

## what

REQUIRED_ACTION: Apply updates per vendor instr 55%, Apply mitigations per vendor i 20%, Apply mitigations per vendor i 16%, Apply mitigations in accordanc 3%, The impacted product is end-of 3%, Apply updates per vendor instr 1%, Apply remediations or mitigati 1%, The impacted product is end-of 0%, Apply updates per vendor instr 0%, Please adhere to CISA’s guidel 0%, This vulnerability affects leg 0%, The impacted product could be  0%

KNOWN_RANSOMWARE_CAMPAIGN_USE: Unknown 79%, Known 21%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CVE_ID | id | 1.7K | 0 | CVE-2020-29583 9; CVE-2019-8394 9; CVE-2020-10189 9; CVE-2021-40539 9 |
| VENDOR_PROJECT | who | 275 | 0 | Microsoft 385; Cisco 96; Apple 94; Adobe 80 |
| PRODUCT | who | 675 | 0 | Windows 170; Multiple Products 79; Chromium V8 39; Internet Explorer 36 |
| VULNERABILITY_NAME | who | 1.3K | 0 | Microsoft Win32k Privileg 26; Google Chromium V8 Type C 20; Microsoft Windows Kernel  14; Microsoft Exchange Server 13 |
| DATE_ADDED | date | 458 | 0 | 2021-11-03 290; 2022-03-03 98; 2022-03-25 69; 2022-06-08 38 |
| SHORT_DESCRIPTION | other | 1.6K | 0 | Google Chromium V8 Engine 12; Microsoft Exchange Server 11; Microsoft Win32k contains 10; Microsoft Windows kernel  10 |
| REQUIRED_ACTION | category | 46 | 0 | Apply updates per vendor  893; Apply mitigations per ven 322; Apply mitigations per ven 259; Apply mitigations in acco 57 |
| DUE_DATE | date | 483 | 0 | 2022-05-03 192; 2021-11-17 101; 2022-03-24 71; 2022-04-15 69 |
| KNOWN_RANSOMWARE_CAMPAIGN_USE | category | 2 | 0 | Unknown 1.3K; Known 352 |
| NOTES | id | 1.7K | 0 | This vulnerability affect 24; Reference CISA's ED 21-03 14; This vulnerability could  14; Reference CISA's ED 21-02 11 |
| CWES | who | 246 | 171 | CWE-78 94; CWE-20 91; CWE-416 90; CWE-787 84 |
| INGESTED_AT | audit | 1 | 0 | 1787434842633752 1.7K |
| SOURCE_RUN_ID | audit | 1 | 0 | 7c1eb6e7-03cf-471d-97bb-0 1.7K |
| SRC_SHA256 | who | 1 | 0 | 9e5e62375ebbfec095d44d0f3 1.7K |
