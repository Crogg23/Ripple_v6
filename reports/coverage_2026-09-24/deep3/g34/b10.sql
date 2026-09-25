-- S23 SDWA PN assoc trap check: the systems with the most link rows, and how many distinct PN violations and related violations sit behind them
SELECT PWSID, COUNT(*) links, COUNT(DISTINCT PN_VIOLATION_ID) pn_viols, COUNT(DISTINCT RELATED_VIOLATION_ID) related_viols,
       MIN(COMPL_PER_BEGIN_DATE) b0, MAX(COMPL_PER_BEGIN_DATE) b1, LISTAGG(DISTINCT VIOLATION_CODE, ',') codes,
       MAX(cnt_per_pn) max_related_per_pn
FROM (SELECT a.*, COUNT(*) OVER (PARTITION BY PWSID, PN_VIOLATION_ID) cnt_per_pn FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PN_VIOLATION_ASSOC a)
GROUP BY 1 ORDER BY links DESC LIMIT 25;
