# FED_ITIS_OTHER_SOURCES

rows 1.1K  columns 11  scan 4.1s

roles: amount 1, audit 2, category 1, date 2, id 1, other 2, who 2

## when

ACQUISITION_DATE
  1996        45  ######
  1997         1  
  1998        10  #
  1999         1  
  2000         4  #
  2001        22  ###
  2002        17  ##
  2003        28  ####
  2004        41  #####
  2005        57  #######
  2006        32  ####
  2007        31  ####
  2008        12  ##
  2009        17  ##
  2010        71  #########
  2011       231  ##############################
  2012        95  ############
  2013        38  #####
  2014        40  #####
  2015        22  ###
  2016        23  ###
  2017        14  ##
  2018        17  ##
  2019        26  ###
  2020        31  ####
  2021        32  ####
  2022        15  ##
  2023        22  ###
  2024        32  ####
  2025        30  ####
  2026        14  ##

UPDATE_DATE
  1996         6  #
  1997         1  
  1998         1  
  2000         1  
  2001         1  
  2002         7  #
  2003        37  #####
  2004        50  #######
  2005        71  ##########
  2006        30  ####
  2007        43  ######
  2008        15  ##
  2009        11  ##
  2010        22  ###
  2011       113  #################
  2012       203  ##############################
  2013        97  ##############
  2014        35  #####
  2015        26  ####
  2016        27  ####
  2017        20  ###
  2018        13  ##
  2019        17  ###
  2020        48  #######
  2021        28  ####
  2022        27  ####
  2023        19  ###
  2024        42  ######
  2025        37  #####
  2026        23  ###

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VERSION | 524 | 0.02 | 2.0K | 2.0K | 2.0K | 795.1K |

## who

SOURCE_COMMENT by rows
       193  Updated for ITIS by the Flora of North America Expertise Network, in c
        80  "Zoonomen - Zoological Nomenclature Resource" maintained by Alan P. Pe
        35  None
        31  http://www.calacademy.org/research/ichthyology/catalog/
        21  Updated by the Flora of North America Expertise Network, in connection
        13  "Zoonomen Nomenclatural data" maintained by Alan P. Peterson at http:/
        13  http://www.redlist.org/
        11  http://www.fws.gov/endangered/
        11  The International Plant Names Index, botanical information system from
         9  National Plant Data Center, NRCS, USDA. Baton Rouge, LA 70874-4490 USA
         8  Tropicos, botanical information system at the Missouri Botanical Garde
         7  Zoonomen Nomenclatural data maintained by Alan P. Peterson at http://w
         6  Food and Agriculture Organization of the United Nations (FAO) Aquatic 
         6  Uetz, P. & Jirí Hosek (eds.), The Reptile Database, (http://www.reptil
         6  García Morales, M., B. D. Denno, D. R. Miller, G. L. Miller, Y. Ben-Do
         5  http://research.calacademy.org/research/ichthyology/catalog/fishcatmai
         5  Griswold, T., and J. S. Ascher. 2005. Checklist of Apoidea of North Am
         5  'Zoonomen Nomenclatural data' maintained by Alan P. Peterson at http:/
         5  Angiosperm Phylogeny Website, botanical information system at the Miss
         5  http://www.bgbm.fu-berlin.de/iapt/ncu/genera/

SOURCE_COMMENT by dollars
      388.1K      193 rows  Updated for ITIS by the Flora of North America Expertise Net
       42.2K       21 rows  Updated by the Flora of North America Expertise Network, in 
       22.0K       13 rows  http://www.redlist.org/
       20.1K       11 rows  The International Plant Names Index, botanical information s
       16.1K        8 rows  Tropicos, botanical information system at the Missouri Botan
       10.1K        5 rows  Angiosperm Phylogeny Website, botanical information system a
        8.0K        4 rows  Kew World Checklist of Selected Plant Families, botanical in
        8.0K        4 rows  The Jepson online interface, botanical information system fr
        8.0K        4 rows  Acevedo-Rodríguez, P. & M.T. Strong. 2007. Catalogue of the 
        8.0K       35 rows  None
        6.0K        3 rows  USDA, ARS, National Genetic Resources Program. Germplasm Res
        6.0K        3 rows  eFloras, Missouri Botanical Garden, St. Louis, MO & Harvard 
        6.0K        3 rows  UNEP-WCMC (Comps.) 2011. Checklist of CITES species (CD-ROM)
        6.0K        3 rows  UNEP-WCMC (Comps.) 2008. Checklist of CITES species (CD-ROM)
        4.0K        2 rows  AviList Core Team. 2025. AviList: The Global Avian Checklist
        4.0K        2 rows  del Hoyo, J., Elliott, A., Sargatal, J., Christie, D.A. & de
        4.0K        2 rows  Yu, Dicky Sick Ki, Cornelis van Achterberg, and Klaus Horstm
        4.0K        2 rows  Pulawski, Wojciech J. 2016. Catalog of Sphecidae sensu lato:
        4.0K        2 rows  WoRMS Editorial Board (2014). World Register of Marine Speci
        4.0K        2 rows  UNEP-WCMC (Comps.) 2013. Checklist of CITES species. CITES S

SRC_SHA256 by rows
      1.1K  d98c5f0cb5207f84bb56ef033ab7d3bf4c74fb5f5cf0f50cadf6c22e71debe21

SRC_SHA256 by dollars
      795.1K     1.1K rows  d98c5f0cb5207f84bb56ef033ab7d3bf4c74fb5f5cf0f50cadf6c22e71de

## who x when

SOURCE_COMMENT by ACQUISITION_DATE, dollars = VERSION
  "Zoonomen - Zoological Nomenclature Reso  2005:1 2006:5 2007:6 2011:13 2012:55
  "Zoonomen Nomenclatural data" maintained  2005:4 2007:4 2015:1 2017:1 2018:1 2020:2
  'Zoonomen Nomenclatural data' maintained  2015:1 2021:1 2022:1 2024:2
  Acevedo-Rodríguez, P. & M.T. Strong. 200  2011:4.0K 2013:2.0K 2016:2.0K
  Angiosperm Phylogeny Website, botanical   2009:2.0K 2010:2.0K 2011:2.0K 2012:2.0K 2014:2.0K
  AviList Core Team. 2025. AviList: The Gl  2025:4.0K
  Food and Agriculture Organization of the  2021:2 2022:1 2023:1 2024:1 2026:2.0K
  García Morales, M., B. D. Denno, D. R. M  2024:2 2025:4
  Griswold, T., and J. S. Ascher. 2005. Ch  2005:3 2006:2
  Kew World Checklist of Selected Plant Fa  2010:2.0K 2011:4.0K 2014:2.0K
  National Plant Data Center, NRCS, USDA.   1996:8 1997:4.30 2000:1 2003:3.50 2007:1 2008:1 2009:1 2011:2.0K
  None                                      1996:31 1998:3 2003:8.0K 2015:1
  The International Plant Names Index, bot  2010:2.0K 2011:6.0K 2012:6.0K 2013:2.0K 2014:2.0K 2015:2.0K
  The Jepson online interface, botanical i  2011:6.0K 2013:2.0K
  Tropicos, botanical information system a  2010:2.0K 2011:6.0K 2012:2.0K 2013:2.0K 2015:2.0K 2018:2.0K
  UNEP-WCMC (Comps.) 2008. Checklist of CI  2009:6.0K
  UNEP-WCMC (Comps.) 2011. Checklist of CI  2009:2.0K 2011:4.0K
  USDA, ARS, National Genetic Resources Pr  2011:2.0K 2012:2.0K 2013:2.0K
  Uetz, P. & Jirí Hosek (eds.), The Reptil  2013:1 2014:2 2017:1 2018:1 2019:1
  Updated by the Flora of North America Ex  2010:42.2K
  Updated for ITIS by the Flora of North A  2010:44.2K 2011:343.9K
  Yu, Dicky Sick Ki, Cornelis van Achterbe  2021:2.0K 2023:2.0K
  Zoonomen Nomenclatural data maintained b  2005:7
  del Hoyo, J., Elliott, A., Sargatal, J.,  2016:4.0K
  eFloras, Missouri Botanical Garden, St.   2010:2.0K 2011:2.0K 2012:2.0K
  http://research.calacademy.org/research/  2012:2 2013:3
  http://www.bgbm.fu-berlin.de/iapt/ncu/ge  2001:2 2004:4
  http://www.calacademy.org/research/ichth  2000:2 2001:1 2002:6 2003:3 2004:8 2005:4 2007:1 2008:1 2009:1 2010:1 2012:2 2014:1
  http://www.fws.gov/endangered/            2001:6 2003:2 2004:1 2005:1 2009:1
  http://www.redlist.org/                   2001:2.0K 2003:2.0K 2004:6.0K 2005:8.0K 2006:2.0K 2007:2.0K 2018:2

SRC_SHA256 by ACQUISITION_DATE, dollars = VERSION
  d98c5f0cb5207f84bb56ef033ab7d3bf4c74fb5f  1996:2.0K 1997:4.30 1998:2.0K 1999:1 2000:2 2001:2.0K 2002:0.03 2003:18.0K 2004:10.0K 2005:16.0K 2006:12.0K 2007:4.0K 2008:2.0K 2009:10.0K 2010:104.6K 2011:408.2K 2012:34.2K 2013:42.3K 2014:22.2K 2015:6.1K 2016:16.1K 2017:2.0K 2018:6.1K 2019:4.1K 2020:12.1K 2021:8.1K 2022:36.21 2023:8.1K 2024:18.2K 2025:18.3K 2026:6.1K

## what

SOURCE_TYPE: website 46%, database 46%, document 2%, Database 2%, manuscript 2%, CD-ROM 1%, PDF 1%, Website 0%, webpage 0%, checklist 0%, series 0%, daabase 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SOURCE_ID_PREFIX | other | 1 | 0 | SRC 1.1K |
| SOURCE_ID | id | 1.1K | 0 | 1428 6; 1427 6; 1426 6; 1425 6 |
| SOURCE_TYPE | category | 26 | 0 | website 487; database 485; document 21; Database 16 |
| SOURCE | other | 991 | 0 | IOC World Bird List (vers 9; Nonindigenous Aquatic Spe 8; Handbook of the Birds of  8; ITIS & Species 2000 Catal 8 |
| VERSION | amount | 506 | 0 | 2011 195; undefined 75; 2010 56; 1 33 |
| ACQUISITION_DATE | date | 704 | 0 | 2011-01-01 27; 1996-07-29 26; 2010-01-01 21; 2012-12-03 15 |
| SOURCE_COMMENT | who | 520 | 0 | Updated for ITIS by the F 193; "Zoonomen - Zoological No 80; None 35; http://www.calacademy.org 31 |
| UPDATE_DATE | date | 274 | 0 | 2013-11-04 68; 2012-08-29 63; 2012-09-26 40; 2020-08-28 24 |
| INGESTED_AT | audit | 1 | 0 | 1786164250570840 1.1K |
| SOURCE_RUN_ID | audit | 1 | 0 | 21ca1ab0-8d12-4dc1-a750-3 1.1K |
| SRC_SHA256 | who | 1 | 0 | d98c5f0cb5207f84bb56ef033 1.1K |
