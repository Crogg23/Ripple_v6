-- Federal Register midnight rules: final rules in the Nov 8 - Jan 19 window of every year, vs the same year Feb-Oct daily pace
with d as (select PUBLICATION_DATE dt, TYPE, IS_SIGNIFICANT sig, PAGE_LENGTH pg
           from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS where TYPE in ('Rule','Proposed Rule')),
w as (select *, case when dt >= date_from_parts(year(dt),11,8) then year(dt) when dt <= date_from_parts(year(dt),1,19) then year(dt)-1 end wy from d),
win as (select wy, count_if(TYPE='Rule') rules, count_if(TYPE='Rule' and sig) sig_rules, count_if(TYPE='Rule' and sig is not null) sig_filled,
          sum(iff(TYPE='Rule', pg, 0)) rule_pages, count_if(TYPE='Proposed Rule') props, count(distinct dt) pubdays
        from w where wy between 2009 and 2025 group by 1),
base as (select year(dt) y, count_if(TYPE='Rule') rules, count_if(TYPE='Rule' and sig) sig_rules, sum(iff(TYPE='Rule', pg, 0)) rule_pages, count(distinct dt) pubdays
         from d where month(dt) between 2 and 10 group by 1)
select win.wy, win.rules, win.sig_rules, win.sig_filled, win.rule_pages, win.props, win.pubdays,
  base.rules base_rules, base.sig_rules base_sig, base.pubdays base_days,
  round((win.rules/win.pubdays)/(base.rules/base.pubdays),2) rule_pace_ratio,
  round((win.sig_rules/win.pubdays)/nullif(base.sig_rules/base.pubdays,0),2) sig_pace_ratio,
  round((win.rule_pages/win.pubdays)/nullif(base.rule_pages/base.pubdays,0),2) page_pace_ratio
from win left join base on base.y = win.wy order by 1
