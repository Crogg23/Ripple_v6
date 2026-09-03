# PORTAL_CKA_WESTERN_PENNSYLV_A3608CE8E0

rows 145  columns 17  scan 3.9s

roles: amount 3, audit 2, category 2, date 1, empty 1, other 7, who 2

## when

INGESTED_AT
  2026       145  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 145 | 772.33 | 28.6K | 591.6K | 7.02M | 16.26M |
| SHAPE__LENGTH | 145 | 113.22 | 729.95 | 3.6K | 28.7K | 163.4K |
| SHAPE_LENG_1 | 98 | 111.51 | 692.52 | 3.3K | 3.7K | 83.4K |

## who

NAME by rows
         4  Iron City Brewery
         2  Baywood  (The King Estate)
         1  Mamaux Building
         1  Greenfield Elementary School
         1  National Negro Opera Company
         1  Card Estate Carraige House
         1  Carrick Municipal Hall
         1  John Woods House
         1  Monongahela Incline/Upper Street Station
         1  Temp - knoxville Middle School
         1  Woolslair Elementary Gifted Center
         1  B'Nai Israel Synagogue
         1  Allegheny County Jail (next to courthouse)
         1  Centre Avenue YMCA (Frank Bolden Marker)
         1  Phipps Conservatory - Schenley Park
         1  Monongahela Incline
         1  Workingmen's Savings Bank
         1  Concord Elementary School
         1  Carnegie Library of Pittsburgh, Lawrenceville Branch
         1  Madison Elementary School (formerly Minersville P*

NAME by dollars
       7.02M        1 rows  VA Facility Building 10 & 13 - Chapel & Laboratory
      619.6K        1 rows  David P. Oliver High School
      556.0K        1 rows  Cathedral of Learning
      367.5K        1 rows  Westinghouse High School (William "Billy" Strayho*
      366.0K        1 rows  Greenfield Elementary School
      336.0K        1 rows  Phipps Conservatory - Schenley Park
      334.0K        2 rows  Baywood  (The King Estate)
      331.6K        1 rows  Temp - Taylor Allderdice High School
      295.2K        1 rows  Mifflin Elementary School
      264.8K        1 rows  Langley High School
      254.5K        4 rows  Iron City Brewery
      240.7K        1 rows  Perry High School/Traditional Academy
      218.9K        1 rows  Allegheny Arsenal Area
      174.7K        1 rows  Arsenal Junior High School (Arsenal Middle School)
      168.9K        1 rows  Rodef Shalom
      160.2K        1 rows  Temp - Prospect Middle School for Multicultural Education
      158.2K        1 rows  Soldier's and Sailor's Memorial Hall
      154.4K        1 rows  Connolley School
      154.4K        1 rows  Temp - Connelly Skill Learning Center
      139.5K        1 rows  B'Nai Israel Synagogue

SRC_SHA256 by rows
       145  96b1044a010e6d73f0383394bc6b5451dd237d670fd2bb6653b888b02714b6f7

SRC_SHA256 by dollars
      16.26M      145 rows  96b1044a010e6d73f0383394bc6b5451dd237d670fd2bb6653b888b02714

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  Allegheny Arsenal Area                    2026:218.9K
  Allegheny County Jail (next to courthous  2026:69.8K
  Arsenal Junior High School (Arsenal Midd  2026:174.7K
  B'Nai Israel Synagogue                    2026:139.5K
  Baywood  (The King Estate)                2026:334.0K
  Card Estate Carraige House                2026:7.5K
  Carnegie Library of Pittsburgh, Lawrence  2026:10.0K
  Carrick Municipal Hall                    2026:3.2K
  Cathedral of Learning                     2026:556.0K
  Centre Avenue YMCA (Frank Bolden Marker)  2026:19.4K
  Concord Elementary School                 2026:121.0K
  David P. Oliver High School               2026:619.6K
  Greenfield Elementary School              2026:366.0K
  Iron City Brewery                         2026:254.5K
  John Woods House                          2026:5.9K
  Langley High School                       2026:264.8K
  Madison Elementary School (formerly Mine  2026:35.7K
  Mamaux Building                           2026:7.1K
  Mifflin Elementary School                 2026:295.2K
  Monongahela Incline                       2026:23.8K
  Monongahela Incline/Upper Street Station  2026:63.7K
  National Negro Opera Company              2026:35.6K
  Perry High School/Traditional Academy     2026:240.7K
  Phipps Conservatory - Schenley Park       2026:336.0K
  Temp - Taylor Allderdice High School      2026:331.6K
  Temp - knoxville Middle School            2026:114.8K
  VA Facility Building 10 & 13 - Chapel &   2026:7.02M
  Westinghouse High School (William "Billy  2026:367.5K
  Woolslair Elementary Gifted Center        2026:2.5K
  Workingmen's Savings Bank                 2026:8.0K

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  96b1044a010e6d73f0383394bc6b5451dd237d67  2026:16.26M

## what

ALTERNATIV: 1000 Madison Ave 100%

PROVIDED_A: 412 Blvd of the Allies 10%, 4905 Fifth Avenue 10%, 836 W North Ave 10%, 624-624 e Ohio St 10%, 1251 N Negley Ave 10%, Biglo Blvd - 4228 5th Ave 10%, 5136 5th Ave 10%, 2940 Sheridan Ave 10%, 1530 Federal St 10%, 450 Ross St 10%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GLOBALID | other | 146 | 0 | 063884db-a48a-4891-83c1-0 1; 201975ef-2c76-4167-97fe-0 1; cdaa51ff-eccd-4462-86e7-7 1; 39ecf1ee-67b2-46df-b15a-c 1 |
| OBJECTID | other | 146 | 0 | 950 1; 949 1; 947 1; 944 1 |
| SHAPE__AREA | amount | 145 | 0 | 154417.8775024414 2; 2902.9202880859375 1; 2248.6471557617188 1; 9828.27230834961 1 |
| SHAPE__AREA_1 | empty | 1 | 145 |  |
| SHAPE__LENGTH | amount | 145 | 0 | 1703.851516986912 2; 321.95281055856776 1; 231.3761870805018 1; 396.9699587530086 1 |
| ADDRESS | other | 136 | 4 | 3340 Liberty Ave 4; Schenley Park 3; 1435 Bedford Ave 2; 1226 Herron Ave 1 |
| ALTERNATIV | category | 3 | 144 | 1000 Madison Ave 1 |
| HISTORIC_I | other | 139 | 0 | Iron City Brewery 4; Baywood  (The King Estate 2; Donny's Place 1; The Troy Hill Fire House 1 |
| LOTBLOCK | other | 141 | 2 | 0027S00150000001 4; 0009R00194000000 2; 0026E00197000000 1; 0048N00010000000 1 |
| NAME | who | 138 | 0 | Iron City Brewery 4; Baywood  (The King Estate 2; Donny's Place 1; The Troy Hill Fire House 1 |
| PROVIDED_A | category | 30 | 117 | 412 Blvd of the Allies 1; 4905 Fifth Avenue 1; 836 W North Ave 1; 624-624 e Ohio St 1 |
| SHAPE_LENG_1 | amount | 99 | 47 | 111.50505217 1; 752.4347728 1; 356.67118492 1; 187.65184211 1 |
| STREET | other | 106 | 2 | 5th Ave 6; Liberty Ave 4; W North Ave 4; Centre Ave 3 |
| GEOMETRY | other | 146 | 0 | POLYGON ((585761.26520612 2; POLYGON ((587683.25035179 1; POLYGON ((586268.22019473 1; POLYGON ((581875.87589514 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:35:12.58165 145 |
| SOURCE_RUN_ID | audit | 1 | 0 | 94a4170b-fbad-45a7-bcc2-c 145 |
| SRC_SHA256 | who | 1 | 0 | 96b1044a010e6d73f0383394b 145 |
