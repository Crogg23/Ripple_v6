-- dull-explanation test: are the coal units whose retirement date was dropped or pushed back simply converting to gas?
SELECT PLANT_NAME, STATE, GENERATOR_ID, UTILITY_NAME, NAMEPLATE_CAPACITY_MW, ENERGY_SOURCE_1, ENERGY_SOURCE_2, PLANNED_RETIREMENT_YEAR,
       PLANNED_ENERGY_SOURCE_1, PLANNED_NEW_PRIME_MOVER, PLANNED_REPOWER_YEAR, OTHER_PLANNED_MODIFICATIONS, OTHER_MODIFICATIONS_YEAR, COFIRE_FUELS, MULTIPLE_FUELS
FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR
WHERE (PLANT_CODE, GENERATOR_ID) IN ((6076,'1'),(602,'1'),(602,'2'),(889,'1'),(889,'2'),(6178,'1'),(8066,'1'),(8066,'2'),(8066,'3'),(8066,'4'),
      (6139,'1'),(6139,'3'),(8023,'1'),(8023,'2'),(8042,'1'),(8042,'2'),(564,'1'),(4050,'5'),(6101,'BW91'),(4041,'7'),(4041,'8'),(4158,'1'),(4158,'2'),(4158,'4'))
   OR (PLANT_NAME IN ('Jim Bridger','Huntington','Naughton','Dave Johnston','Wyodak','Coleto Creek','Welsh','Stanton Energy Center','Edgewater','Columbia (WI)','South Oak Creek','Brandon Shores','Baldwin Energy Complex','Sherburne County')
       AND ENERGY_SOURCE_1 IN ('BIT','SUB','LIG','NG','RC','WC'))
ORDER BY PLANT_NAME, GENERATOR_ID
