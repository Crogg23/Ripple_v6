-- S08 TopoView: pull all 250 titles, publication dates and sizes to see what the sample covers
SELECT title, LEFT(publicationdate,4) pub_year, filesize, LEFT(datecreated,10) created, LEFT(lastupdated,10) updated, boundingbox
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_TOPOVIEW
