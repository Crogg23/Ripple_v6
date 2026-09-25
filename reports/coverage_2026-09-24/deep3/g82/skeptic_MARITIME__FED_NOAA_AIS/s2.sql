-- Second field for the 16 IMO hits: does the AIS name appear in the list entry's NAME/ALIASES, does the Jan-2024 MMSI appear in IDENTIFIERS; full DATASETS and SANCTIONS text; OFAC remarks
with v as (select column1 imo, column2 aisname, column3 mmsi from values
  ('9333400','SCF NEVA','636017265'),('9308833','LOVINA','538008370'),('9275660','CONQUEROR','236728000'),('9266877','SEA VINE','538006916'),
  ('9304605','MINERVA SYMPHONY','240575000'),('9389095','MINDORO','249577000'),('9385831','ALCYONE T','538008235'),('9379698','ADVANTAGE VIRTUE','538008759'),
  ('9419450','AMAX AVENUE','538006203'),('9299563','PGC MARINA','311000138'),('9333785','CAPRICORN SUN','636016274'),('9439383','PS GENOVA','229903000'),
  ('9259317','FEDOR','538090308'),('9384564','RED SUN','636017066'),('9346859','SEA FALCON','241326000'),('9506693','PS AUGUSTA','215193000')),
os as (select distinct v.imo, v.aisname, v.mmsi, o.ID, o.NAME, o.ALIASES, o.IDENTIFIERS, o.COUNTRIES, o.DATASETS, o.SANCTIONS, o.FIRST_SEEN, o.BIRTH_DATE
       from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT o, lateral flatten(input => split(o.IDENTIFIERS, ';')) t, v
       where o.ENTITY_TYPE = 'Vessel' and regexp_replace(t.value::string,'[^0-9]','') = v.imo)
select 'os' src, imo, aisname, NAME, contains(upper(coalesce(NAME,'')||';'||coalesce(ALIASES,'')), upper(aisname)) name_in_aliases,
  contains(coalesce(IDENTIFIERS,''), mmsi) mmsi_in_ids, FIRST_SEEN::text fs, BIRTH_DATE, COUNTRIES, left(ALIASES,200) aliases, left(IDENTIFIERS,160) ids,
  DATASETS, left(SANCTIONS,700) sanctions
from os
union all
select 'ofac', v.imo, v.aisname, f.SDN_NAME, contains(upper(coalesce(f.REMARKS,'')||';'||f.SDN_NAME), upper(v.aisname)), contains(coalesce(f.REMARKS,''), v.mmsi),
  null, null, f.VESSEL_FLAG, f.VESSEL_TYPE, f.PROGRAM, left(f.REMARKS,400), null
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_OFAC_SDN f join v on regexp_replace(f.IMO_NUMBER,'[^0-9]','') = v.imo where f.IS_VESSEL
order by 2, 1
