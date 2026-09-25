with pats as (select column1 p from values ('%MEMBRANE WRAP%'),('%COMPLETE FT%'),('%ESANO%'),('%RESTORIGIN%'),('%HELICOLL%'),('%IMPAX%'),('%ORION%'),('%AXOLOTL%'),('%AMNICORE%'),('%AMNIO-MAXX%'),('%AMNIO MAXX%'),('%WOUNDPLUS%'),('%E-GRAFT%'),('%DERM-MAXX%'),('%DERM MAXX%'),('%AMNIOAMP%'),('%TRI-CORE%'),('%AMNIOWRAP%'),('%CYGNUS%'),('%QUAD-CORE%'),('%CAREPATCH%'),('%NEOSTIM%'),('%XWRAP%'),('%BARRERA%'),('%NOVACHOR%'),('%COGENEX%'),('%SURGRAFT%'),('%REBOUND MATRIX%'),('%EPIEFFECT%'),('%AMCHOPLAST%'))
select 'gudid' src, p, upper(BRAND_NAME) brand, COMPANY_NAME company, count(*) n, min(PUBLISH_DATE)::varchar first_pub
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID g join pats on upper(g.BRAND_NAME) like pats.p group by 1,2,3,4
union all
select '510k', p, upper(DEVICE_NAME), APPLICANT, count(*), min(DECISION_DATE)::varchar
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_510K k join pats on upper(k.DEVICE_NAME) like pats.p group by 1,2,3,4
union all
select 'estreg', p, upper(PROPRIETARY_NAME), OWNER_OPERATOR_FIRM_NAME, count(*), max(REG_EXPIRY_DATE_YEAR)::varchar
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_ESTABLISHMENT_REG e join pats on upper(e.PROPRIETARY_NAME::varchar) like pats.p group by 1,2,3,4
order by p, src
