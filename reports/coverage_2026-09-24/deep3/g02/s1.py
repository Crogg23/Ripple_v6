from q import run
M = "LIBRARY_MARTS.HEALTH."
run("S01", "CDC WONDER: pull all 880 rows",
    f"SELECT * FROM {M}HEALTH__FED_CDC_WONDER")
run("S02", "VA suicide national: pull all 690 rows",
    f"SELECT * FROM {M}HEALTH__FED_VA_SUICIDE_NATIONAL")
run("S03", "CDC drug poisoning county: pull all 53K rows",
    f"SELECT * FROM {M}HEALTH__FED_CDC_DRUG_POISONING_COUNTY")
run("S04", "Medicare outpatient by provider and service: pull all 116K rows",
    f"SELECT * FROM {M}HEALTH__FED_CMS_MEDICARE_OUTPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE")
