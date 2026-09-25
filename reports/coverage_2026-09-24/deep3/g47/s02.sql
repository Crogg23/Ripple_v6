-- S02 fertility: pull the whole REFERENCE copy (19.4K rows, 4 text columns) to rank locally
SELECT entity, code, year, total_fertility_rate
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__XC_OWID_FERTILITY
