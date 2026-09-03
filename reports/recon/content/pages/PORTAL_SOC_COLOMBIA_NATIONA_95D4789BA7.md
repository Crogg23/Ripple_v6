# PORTAL_SOC_COLOMBIA_NATIONA_95D4789BA7

rows 840  columns 13  scan 2.5s

roles: audit 2, category 3, date 3, other 5, who 1

## when

FECHA_INGRESO
  2009         7  ###
  2010        38  ##############
  2011        31  ###########
  2012        15  #####
  2013        27  ##########
  2014        56  ####################
  2015        49  ##################
  2016        53  ###################
  2017        50  ##################
  2018        35  #############
  2019        52  ###################
  2020        53  ###################
  2021        82  ##############################
  2022        65  ########################
  2023        52  ###################
  2024        60  ######################
  2025        77  ############################
  2026        37  ##############

FECHA_SALIDA_ABOGACIA
  2009         6  ##
  2010        38  ###############
  2011        30  ############
  2012        18  #######
  2013        26  ##########
  2014        51  ####################
  2015        51  ####################
  2016        54  ######################
  2017        45  ##################
  2018        40  ################
  2019        51  ####################
  2020        55  ######################
  2021        75  ##############################
  2022        72  #############################
  2023        49  ####################
  2024        64  ##########################
  2025        72  #############################
  2026        43  #################

INGESTED_AT
  2026       840  ##############################

## who

SRC_SHA256 by rows
       840  3cf278d7cb41a580476efaaf357356dee366eb875291a616fe7787aac1820275

## who x when

SRC_SHA256 by FECHA_INGRESO
  3cf278d7cb41a580476efaaf357356dee366eb87  2009:7 2010:38 2011:31 2012:15 2013:27 2014:56 2015:49 2016:53 2017:50 2018:35 2019:52 2020:53 2021:82 2022:65 2023:52 2024:60 2025:77 2026:37

## what

NOMBRE_ENTIDAD_REGULADORA: Comisión de Regulación de Comu 17%, Comisión de Regulación de Ener 17%, Ministerio de Minas y Energía 15%, Ministerio de Comercio, Indust 12%, Ministerio de Salud y Protecci 9%, Ministerio de Transporte 9%, Ministerio de Tecnologías de l 6%, Agencia Nacional de Contrataci 5%, Superintendencia de Industria  4%, Comisión de Regulación de Agua 3%, Ministerio de Ambiente y Desar 2%, Agencia Nacional de Hidrocarbu 2%

SECTOR: Minas y Energía 29%, TIC 20%, Comercio, Industria y Turismo 13%, Salud y Protección Social 9%, Transporte 9%, Planeación 6%, Hacienda y Crédito Público 4%, Vivienda, Ciudad y Territorio 3%, Agropecuario, Pesquero y de De 3%, Ambiente y Desarrollo Sostenib 2%, Defensa 2%, Justicia y del Derecho 1%

ACOGE_COMENTARIOS_SIC: N/A 44%, SI 24%, Parcialmente 18%, NO 12%, Pendiente análisis 2%, Si 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RADICADO_INICIAL | other | 857 | 0 | 10-158347 6; 26-231249 5; 26-230809 5; 26-230776 5 |
| FECHA_INGRESO | date | 711 | 0 | 2026-04-24T00:00:00.000 7; 2025-11-11T00:00:00.000 7; 2026-06-03T00:00:00.000 6; 2025-07-08T00:00:00.000 6 |
| NOMBRE_ENTIDAD_REGULADORA | category | 47 | 0 | Comisión de Regulación de 116; Comisión de Regulación de 115; Ministerio de Minas y Ene 106; Ministerio de Comercio, I 79 |
| NOMBRE_PROYECTO | other | 822 | 0 | Proyecto Resolución “Por  5; Proyecto de Decreto “Por  5; Proyecto de Decreto “Por  5; Proyecto de Resolución "P 5 |
| SECTOR | category | 17 | 0 | Minas y Energía 241; TIC 165; Comercio, Industria y Tur 109; Salud y Protección Social 73 |
| FECHA_SALIDA_ABOGACIA | date | 690 | 0 | 2026-06-19T00:00:00.000 7; 2026-05-11T00:00:00.000 7; 2025-10-09T00:00:00.000 6; 2024-02-05T00:00:00.000 6 |
| RECOMENDACI_N_SIC_Y_O_APARTE | other | 552 | 0 | NO 285; La Superintendencia no fo 7; En relación con el numera 4; En relación con la metodo 3 |
| NORMA_REGULATORIA_DEFINITIVA | other | 710 | 0 | No ha sido expedida 53; No fue expedida 49; Resolución 104 005 del 19 5; Decreto 1072 del 15 de Oc 5 |
| ACOGE_COMENTARIOS_SIC | category | 6 | 0 | N/A 372; SI 204; Parcialmente 147; NO 101 |
| RESUMEN | other | 656 | 0 | SIN INFORMACIÓN 169; Al revisar el estudio pre 5; El proyecto tiene como ob 4; El proyecto tiene como ob 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:42:46.56457 840 |
| SOURCE_RUN_ID | audit | 1 | 0 | 525dd421-9ef7-47c7-b72d-1 840 |
| SRC_SHA256 | who | 1 | 0 | 3cf278d7cb41a580476efaaf3 840 |
