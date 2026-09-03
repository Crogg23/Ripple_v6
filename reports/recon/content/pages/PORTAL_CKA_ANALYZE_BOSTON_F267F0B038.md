# PORTAL_CKA_ANALYZE_BOSTON_F267F0B038

rows 346  columns 11  scan 3.1s

roles: audit 2, category 1, date 1, other 1, who 7

## when

INGESTED_AT
  2026       346  ##############################

## who

BUSINESS_NAME by rows
         5  ?
         3  CURATED RENTALS
         3  N/A
         2  Parkway Driving School, LLC
         2  Fundamental Optical Solutions LLC
         2  Presidential Properties
         2  Alexis Frobin Acupuncture
         2  Eye Adore Threading
         2  The Rose Maven
         2  JLW Medical Management Consulting
         2  Salon Monét
         2  Curation Agency
         2  no
         2  Love Balungi LLC
         2  Queens Royal Cleaning Co
         2  Bell Chiropractic Boston
         1  High Tech Construction
         1  PM MECHANICAL SERVICES
         1  Purposeful Projects Group
         1  Esthetics Center New England

BUSINESS_WEBSITE by rows
         3  www.quincymarketsweets.com
         3  https://lovebalungi.com
         2  http://www.eyeadorethreading.com
         2  www.expozedtv.com
         2  www.onyxbos.com
         2  hairsalonmonet.com
         2  https://yourbostonapartments.com/
         2  www.bellchiropracticboston.com
         2  www.Dreamkidspa.com
         2  therosemaven.com
         2  www.ReprezentU.com
         2  www.lallabee.com
         2  n/a
         2  http://www.alexisfrobinacu.com
         1  https://flairbridesmaid.com/
         1  https://parkwaydrivingschool.com/
         1  www.branchventuregroup.com
         1  https://motivatedhelper.com/
         1  https://www.zaazey.com
         1  thehealinghound.info

BUSINESS_TYPE by rows
        39  Professional Services
        28  Retail
        18  Healthcare
        16  Food and Beverage
        15  Education
        15  Creative Economy
         6  Financial Services
         6  Technology
         5  Food and Beverage, Retail
         5  Creative Economy, Professional Services
         3  Professional Services, Real Estate
         3  Creative Economy, Retail
         3  Education, Professional Services
         3  Construction
         3  Restaurant & Catering
         2  Salon
         2  Healthcare, Professional Services
         2  Food and Beverage, Restaurant & Catering
         2  Fitness
         2  Creative Economy, Professional Services, Tabletop Rental Studio

BUSINESS_EMAIL by rows
         3  Syoungelson@aol.com
         3  info@curated-rentals.com
         3  Info@dreamkidspa.com
         2  info@aneufit.com
         2  gcoleiny@fundamentalopticalsolutions.com
         2  lovebalungi@gmail.com
         2  Rachel@ReprezentU.com
         2  hello@eyeadorethreading.com
         2  rokeya@shantiboston.com
         2  Gabriellaspinola@yahoo.com
         2  csmart@onyxbos.com
         1  Amstrokes617@gmail.com
         1  ecoleman@haianalytics.com
         1  rachel@shopcityhome.com
         1  caitlin@deirfiurhome.com
         1  kristinamelendez@kw.com
         1  yalennysvelazquez@hotmail.com
         1  Fatousy1229@gmail.com
         1  goldenflorwellness@gmail.com
         1  rleonard@purposefulprojectsgroup.com

## who x when

BUSINESS_NAME by INGESTED_AT  LOAD STAMP, not an event date
  ?                                         2026:5
  Alexis Frobin Acupuncture                 2026:2
  Bell Chiropractic Boston                  2026:2
  CURATED RENTALS                           2026:3
  Curation Agency                           2026:2
  Esthetics Center New England              2026:1
  Eye Adore Threading                       2026:2
  Fundamental Optical Solutions LLC         2026:2
  High Tech Construction                    2026:1
  JLW Medical Management Consulting         2026:2
  Love Balungi LLC                          2026:2
  N/A                                       2026:3
  PM MECHANICAL SERVICES                    2026:1
  Parkway Driving School, LLC               2026:2
  Presidential Properties                   2026:2
  Purposeful Projects Group                 2026:1
  Queens Royal Cleaning Co                  2026:2
  Salon Monét                               2026:2
  The Rose Maven                            2026:2
  no                                        2026:2

BUSINESS_WEBSITE by INGESTED_AT  LOAD STAMP, not an event date
  hairsalonmonet.com                        2026:2
  http://www.alexisfrobinacu.com            2026:2
  http://www.eyeadorethreading.com          2026:2
  https://flairbridesmaid.com/              2026:1
  https://lovebalungi.com                   2026:3
  https://motivatedhelper.com/              2026:1
  https://parkwaydrivingschool.com/         2026:1
  https://www.zaazey.com                    2026:1
  https://yourbostonapartments.com/         2026:2
  n/a                                       2026:2
  thehealinghound.info                      2026:1
  therosemaven.com                          2026:2
  www.Dreamkidspa.com                       2026:2
  www.ReprezentU.com                        2026:2
  www.bellchiropracticboston.com            2026:2
  www.branchventuregroup.com                2026:1
  www.expozedtv.com                         2026:2
  www.lallabee.com                          2026:2
  www.onyxbos.com                           2026:2
  www.quincymarketsweets.com                2026:3

## what

OTHER_INFORMATION: Minority-owned 49%, N/A 32%, Minority-owned, Immigrant-owne 14%, Immigrant-owned 4%, Minority-owned, Veteran-owned 1%, Minority-owned, Veteran-owned, 0%, Immigrant-owned, N/A 0%, Minority-owned, N/A 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| BUSINESS_NAME | who | 329 | 0 | ? 6; CURATED RENTALS 4; N/A 3; Love Balungi LLC 3 |
| BUSINESS_TYPE | who | 183 | 0 | Professional Services 39; Retail 28; Healthcare 18; Food and Beverage 16 |
| PHYSICAL_LOCATION_ADDRESS | other | 316 | 1 | Boston, MA 12; N/A 6; Boston MA 5; 3708 Washington St. Jamai 3 |
| BUSINESS_ZIPCODE | who | 56 | 0 | 02116 32; 02124 22; 02131 18; 02136 18 |
| BUSINESS_WEBSITE | who | 266 | 62 | www.lallabee.com 3; https://lovebalungi.com 3; www.Dreamkidspa.com 3; hairsalonmonet.com 3 |
| BUSINESS_PHONE_NUMBER | who | 290 | 44 | 857-218-0977 4; +1 (508) 656-7399 3; 6179305378 3; 6178942203 3 |
| BUSINESS_EMAIL | who | 325 | 3 | info@curated-rentals.com 4; Info@dreamkidspa.com 4; Gabriellaspinola@yahoo.co 3; Rachel@ReprezentU.com 3 |
| OTHER_INFORMATION | category | 8 | 0 | Minority-owned 169; N/A 111; Minority-owned, Immigrant 47; Immigrant-owned 13 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:39:53.13288 346 |
| SOURCE_RUN_ID | audit | 1 | 0 | c8186fed-7244-4f54-8dcd-5 346 |
| SRC_SHA256 | who | 1 | 0 | 7f32113a76005e56de9a77fa8 346 |
