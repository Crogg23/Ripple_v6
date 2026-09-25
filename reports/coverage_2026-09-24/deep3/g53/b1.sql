-- S01 AustLII: every row (glance says 1)
SELECT * FROM LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_AUSTLII;

-- S02 Europol SOCTA: every row (glance says 26)
SELECT * FROM LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_EU_SOCTA_EUROPOL;

-- S03 EUR-Lex Cellar: every row (glance says 13)
SELECT * FROM LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_EURLEX_CELLAR;

-- S04 FTC datasets: every row (glance says 1,004), extract for local time and duplicate checks
SELECT * FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FTC_DATASETS;

-- S05 FBI NICS: every row (glance says 16,445), extract for local duplicate, time and peer checks
SELECT * FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FBI_NICS_CHECKS;
