-- S07 UDS health-center patient totals (Table 3A line 39 = total, cols a+b) with name, state, year
SELECT i.bhcmisid, i.grantnumber, i.reportingyear, i.healthcentername, i.healthcenterstate, i.urbanruralflag,
       TRY_TO_NUMBER(t.t3a_l39_ca) l39a, TRY_TO_NUMBER(t.t3a_l39_cb) l39b,
       TRY_TO_NUMBER(t.t3a_l1_ca) l1a, TRY_TO_NUMBER(t.t3a_l38_ca) l38a, TRY_TO_NUMBER(t.t3a_l38_cb) l38b
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_HEALTH_CENTER_INFO i
LEFT JOIN LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_TABLE3A_PATIENTS t ON t.bhcmisid = i.bhcmisid
