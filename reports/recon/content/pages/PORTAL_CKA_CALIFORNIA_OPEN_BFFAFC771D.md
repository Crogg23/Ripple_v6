# PORTAL_CKA_CALIFORNIA_OPEN_BFFAFC771D

rows 55  columns 13  scan 3.0s

roles: audit 2, category 7, date 2, other 1, who 2

## when

DATE_RECEIVED_ACQUIRED
  1905         1  #
  2015        10  ##############
  2016        21  ##############################
  2017         1  #
  2018         4  ######
  2019         6  #########
  2020         8  ###########

INGESTED_AT
  2026        55  ##############################

## who

DATASET_NAME_DESCRIPTION by rows
         2  Trinity County streams / lakes
         1  Culvert_Line
         1  SEKI Hydro_Swallets_Pt
         1  Marin CO Data
         1  DFW Statewide Streams Data v2.1
         1  ACSC 1914 0001
         1  USGS 1/3 Arc-Second Contours
         1  3DEP Elevation Data
         1  SEKI Hydro_Springs_pt
         1  NHD Map Services
         1  ESRI Basemap: World Hillshade
         1  SEKI BND_River_Status_In
         1  Harbor_Bay
         1  ESRI Basemap: US Topo Maps
         1  tl_2013_06093_linearwater_Siskiyou
         1  hydro_st_Mendocino
         1  DFW GNIS Name Data
         1  DFW Statewide Streams Data Sample
         1  Estuary Points (PONE-D-19-03898)
         1  Flood_Control_Channels_CN

SRC_SHA256 by rows
        55  2c91973e702c6fad6514a95fed9ac951c3bb34c8e10d4dea6ef2761897e828f9

## who x when

DATASET_NAME_DESCRIPTION by DATE_RECEIVED_ACQUIRED
  3DEP Elevation Data                       1905:1
  ACSC 1914 0001                            2015:1
  Culvert_Line                              2019:1
  DFW GNIS Name Data                        2015:1
  DFW Statewide Streams Data Sample         2015:1
  DFW Statewide Streams Data v2.1           2015:1
  ESRI Basemap: US Topo Maps                2016:1
  ESRI Basemap: World Hillshade             2016:1
  Estuary Points (PONE-D-19-03898)          2019:1
  Flood_Control_Channels_CN                 2016:1
  Harbor_Bay                                2016:1
  Marin CO Data                             2016:1
  NHD Map Services                          2015:1
  SEKI BND_River_Status_In                  2020:1
  SEKI Hydro_Springs_pt                     2020:1
  SEKI Hydro_Swallets_Pt                    2020:1
  USGS 1/3 Arc-Second Contours              2019:1
  hydro_st_Mendocino                        2016:1
  tl_2013_06093_linearwater_Siskiyou        2017:1

SRC_SHA256 by DATE_RECEIVED_ACQUIRED
  2c91973e702c6fad6514a95fed9ac951c3bb34c8  1905:1 2015:10 2016:21 2017:1 2018:4 2019:6 2020:8

## what

SOURCE_GENERAL: Sequoia & Kings Canyon Nationa 18%, ESRI 13%, CA Department of Fish & Wildli 13%, CA Department of Water Resourc 10%, County of Marin 8%, County of Sonoma 8%, U.S. Geological Survey (USGS) 8%, County of Trinity 5%, County of Lake 5%, San Diego Geographic Informati 5%, CA Department of Transportatio 5%, County of Kern - Engineering,  3%

SOURCE_SPECIFIC: Paul Hardwck - Information Res 24%, http://sonomavegmap.org/blog/2 14%, ArcGIS Online Basemaps 14%, County of Marin 7%, County of Trinity 7%, County of Lake 7%, Pacific States Marine Fisherie 7%, Keven Roth 7%, Tom Christy 7%, County of Kern - Engineering,  3%, www.sciencebase.gov 3%

AREA_GEOGRAPHY_WHERE_RELEVANT: Statewide (CA) 24%, Statewide 16%, Sequoia & Kings Canyon Nationa 16%, Sonoma County 9%, Marin County 7%, Coastal CA 7%, Trinity County 4%, Lake County 4%, San Diego CO 4%, Southwestern US 4%, Kern CO 2%, California 2%

TYPES_OF_FEATURES_RELEVANCE: Streams 33%, Aerial Photos 12%, Lakes 9%, Culvert data 9%, Wetlands 6%, Estuary/Wetlands 6%, Topo Maps 6%, Elevation 6%, Rivers, aqueducts, canals, spi 3%, Contour Lines 3%, Forest Service Boundaries 3%, Waterbodies 3%

FORMAT: gdb 30%, shp 26%, Shapefile 11%, GDB 9%, Online GIS Service 8%, GDB/Shapefile 4%, Image Tiles: one foot resoluti 2%, Unk 2%, GIS Service 2%, Aerial Mosaic (.sid)
Online GI 2%, GDB, PDFs 2%, Images, Map Docs, Doc, etc. 2%

USE_CONSTRAINTS: Data is generalized and create 22%, Data is shared to DWR by Caltr 22%, "if distributing, include disc 11%, http://geodesy.noaa.gov/storm_ 11%, See documentation by Elizabeth 11%, The State of California and th 11%, The associated data are consid 11%

NOTES: Marin County data will be upda 21%, Potential to use for Californi 14%, 2017 data. Downloaded all need 7%, The year of the aerials shown  7%, Other areas captured in 2014 a 7%, This is an associated file tha 7%, To be used as reference, if ne 7%, To be primarily used for NHD s 7%, (can you paste in the document 7%, The latest changes include an  7%, Used in ephemeral mapping/conv 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OID | other | 55 | 0 | 55 1; 54 1; 53 1; 52 1 |
| DATASET_NAME_DESCRIPTION | who | 53 | 0 | Trinity County streams /  2; wetland 1; waterbody 1; water_course 1 |
| SOURCE_GENERAL | category | 28 | 0 | Sequoia & Kings Canyon Na 7; ESRI 5; CA Department of Fish & W 5; CA Department of Water Re 4 |
| SOURCE_SPECIFIC | category | 36 | 2 | Paul Hardwck - Informatio 7; http://sonomavegmap.org/b 4; ArcGIS Online Basemaps 4; County of Marin 2 |
| AREA_GEOGRAPHY_WHERE_RELEVANT | category | 22 | 0 | Statewide (CA) 11; Statewide 7; Sequoia & Kings Canyon Na 7; Sonoma County 4 |
| TYPES_OF_FEATURES_RELEVANCE | category | 34 | 0 | Streams 11; Aerial Photos 4; Lakes 3; Culvert data 3 |
| FORMAT | category | 14 | 0 | gdb 16; shp 14; Shapefile 6; GDB 5 |
| DATE_RECEIVED_ACQUIRED | date | 29 | 3 | 1/1/2016 7; 8/19/2020 7; 2/4/2016 4; 11/1/2018 3 |
| USE_CONSTRAINTS | category | 8 | 46 | Data is generalized and c 2; Data is shared to DWR by  2; "if distributing, include 1; http://geodesy.noaa.gov/s 1 |
| NOTES | category | 17 | 36 | Marin County data will be 3; Potential to use for Cali 2; 2017 data. Downloaded all 1; The year of the aerials s 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:12:51.98634 55 |
| SOURCE_RUN_ID | audit | 1 | 0 | 021be97f-7be8-4788-aba1-1 55 |
| SRC_SHA256 | who | 1 | 0 | 2c91973e702c6fad6514a95fe 55 |
