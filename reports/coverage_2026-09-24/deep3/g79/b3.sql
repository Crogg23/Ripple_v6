-- S08 TAS join test: pull the 111-row toptier agency table (the only mart with a TOPTIER_CODE); join to the tree locally on NODE_ID = TOPTIER_CODE
SELECT * FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_TOPTIER_AGENCIES;
