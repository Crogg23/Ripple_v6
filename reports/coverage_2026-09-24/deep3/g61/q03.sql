-- OWNER: top owners by generators held; is the owner also the operator; how many plant states
SELECT OWNERSHIP_ID, OWNER_NAME, OWNER_CITY, OWNER_STATE, COUNT(*) gens, COUNT(DISTINCT PLANT_CODE) plants,
       COUNT(DISTINCT STATE) plant_states, SUM(IFF(STATE<>OWNER_STATE,1,0)) gens_out_of_state,
       ROUND(SUM(PERCENT_OWNED),2) sum_pct, SUM(IFF(OWNERSHIP_ID=UTILITY_ID,1,0)) owner_is_operator,
       COUNT(DISTINCT OWNER_NAME) name_variants
FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_4_OWNER
GROUP BY 1,2,3,4 ORDER BY gens DESC LIMIT 40
