-- Federal Register procedure by year, Feb-Aug only: interim/direct final rules, delays, repeal titles, comment windows, days until effective
select PUBLICATION_YEAR yr, count_if(TYPE='Rule') rules,
  count_if(TYPE='Rule' and ACTION ilike '%interim final%') ifr,
  count_if(TYPE='Rule' and ACTION ilike '%direct final%') dfr,
  count_if(TYPE='Rule' and (ACTION ilike '%delay%' or ACTION ilike '%postpone%')) delay_rules,
  count_if(TYPE='Rule' and (TITLE ilike '%rescission%' or TITLE ilike '%rescind%' or TITLE ilike '%repeal%' or TITLE ilike '%removal of%' or TITLE ilike '%removing%')) repeal_title,
  count_if(TYPE='Rule' and DAYS_UNTIL_EFFECTIVE is not null) eff_filled,
  count_if(TYPE='Rule' and DAYS_UNTIL_EFFECTIVE <= 0) eff_now,
  count_if(TYPE='Rule' and DAYS_UNTIL_EFFECTIVE between 1 and 29) eff_lt30,
  count_if(TYPE='Proposed Rule') props,
  count_if(TYPE='Proposed Rule' and COMMENT_WINDOW_DAYS is not null) prop_cw,
  median(iff(TYPE='Proposed Rule', COMMENT_WINDOW_DAYS, null)) prop_cw_med,
  count_if(TYPE='Proposed Rule' and COMMENT_WINDOW_DAYS < 30) prop_lt30,
  count_if(TYPE='Proposed Rule' and COMMENT_WINDOW_DAYS >= 60) prop_ge60,
  count_if(TYPE='Rule' and IS_SIGNIFICANT) sig_rules, count_if(TYPE='Rule' and IS_SIGNIFICANT is not null) sig_filled
from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
where PUBLICATION_MONTH between 2 and 8
group by 1 order by 1
