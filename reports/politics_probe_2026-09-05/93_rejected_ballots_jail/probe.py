import os, sys
from _shared.q import run, open_log
from _shared.cols import cols
HERE = os.path.dirname(os.path.abspath(__file__)); open_log(os.path.join(HERE, "probe.log"))
STEP = int(os.environ.get("STEP", "1"))
if STEP == 1:
    r = cols("LIBRARY_MARTS", "POLITICS", "POLITICS__FED_EAC_EAVS")
    cols("LIBRARY_MARTS", "CORE", "DIM_COUNTY")
    cols("LIBRARY_MARTS", "JUSTICE", "JUSTICE__XC_VERA_INCARCERATION_TRENDS")
    cols("LIBRARY_MARTS", "POLITICS", "POLITICS__FED_MEDSL_HOUSE_RETURNS")
if STEP == 2:
    print(run("select count(*) n, count(distinct fipscode) fips, min(length(fipscode)) l0, max(length(fipscode)) l1, count(distinct state_abbr) states from LIBRARY_MARTS.POLITICS.POLITICS__FED_EAC_EAVS", "eavs keys"))
    print(run("select fipscode, jurisdiction_name, state_abbr, a1a, c1a, c1b, c4a, c4b, c8a, c9a, e1a, e2a, f1a from LIBRARY_MARTS.POLITICS.POLITICS__FED_EAC_EAVS where state_abbr in ('GA','TX','AZ') limit 6", "eavs sample"))
    print(run("select c1g_other, c9r_other, e1e_other, c1comments from LIBRARY_MARTS.POLITICS.POLITICS__FED_EAC_EAVS where c9r_other is not null and c9r_other<>'' limit 3", "eavs other text"))
    print(run("select min(_ingested_at) i0 from LIBRARY_RAW.LANDING.FED_EAC_EAVS", "eavs vintage"))
    print(run("select max(year) y1, count(distinct county_fips) fips, count_if(year=2018) n18 from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_VERA_INCARCERATION_TRENDS", "vera range"))
if STEP == 3:
    # C1B = mail ballots returned, C9A = rejected: C8A + C9A = C1B on every AZ sample row, that arithmetic is the codebook we don't have.
    print(run("""select count(*) n, sum(iff(try_to_number(c1b)>0 and try_to_number(c9a)>=0,1,0)) usable, sum(iff(c9a in ('-99','-88'),1,0)) sentinel, sum(iff(c9a='' or c9a is null,1,0)) blank,
      sum(iff(try_to_number(c8a)+try_to_number(c9a)=try_to_number(c1b),1,0)) identity_holds, sum(iff(length(fipscode)<10,1,0)) short_fips
      from LIBRARY_MARTS.POLITICS.POLITICS__FED_EAC_EAVS""", "eavs c-block fill"))
    print(run("select max(year) y from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_VERA_INCARCERATION_TRENDS where total_jail_pop_rate is not null", "vera last jail year"))
    sql = """
    with e as (
      select left(fipscode,5) cf, sum(try_to_number(c1b)) ret, sum(try_to_number(c9a)) rej
      from LIBRARY_MARTS.POLITICS.POLITICS__FED_EAC_EAVS where length(fipscode)=10 and try_to_number(c1b)>0 and try_to_number(c9a)>=0 group by 1 having sum(try_to_number(c1b))>=500),
    v as (select county_fips, total_jail_pop_rate jail, try_to_number(black_pop_15to64)/nullif(total_pop_15to64,0) black_sh
          from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_VERA_INCARCERATION_TRENDS where year=(select max(year) from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_VERA_INCARCERATION_TRENDS where total_jail_pop_rate is not null) and total_jail_pop_rate is not null),
    j as (select e.*, rej/ret rej_share, v.jail, v.black_sh, ntile(10) over (order by rej/ret) dec from e join v on v.county_fips=e.cf)
    select dec, count(*) counties, round(median(rej_share)*100,2) rej_pct, round(median(jail),0) jail_rate_med, round(avg(jail),0) jail_rate_avg, round(median(black_sh)*100,1) black_pct
    from j group by 1 order by 1
    """
    print(run(sql, "rejected share decile vs jail rate"))
if STEP == 4:
    print(run("""select (select count(distinct left(fipscode,5)) from LIBRARY_MARTS.POLITICS.POLITICS__FED_EAC_EAVS where length(fipscode)=10) eavs_counties,
      (select count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_VERA_INCARCERATION_TRENDS where year=2024 and total_jail_pop_rate is not null) vera_2024_with_jail,
      (select count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_VERA_INCARCERATION_TRENDS where year=2018 and total_jail_pop_rate is not null) vera_2018_with_jail""", "coverage"))
    print(run("select state_abbr, count(*) n, min(length(fipscode)) l from LIBRARY_MARTS.POLITICS.POLITICS__FED_EAC_EAVS where length(fipscode)<10 group by 1 order by 2 desc limit 6", "short fips states"))
if STEP == 5:
    # same deciles on Vera 2018, the last year with near-full county coverage (2,865 vs 1,440 in 2024)
    print(run("""
    with e as (
      select left(fipscode,5) cf, sum(try_to_number(c1b)) ret, sum(try_to_number(c9a)) rej
      from LIBRARY_MARTS.POLITICS.POLITICS__FED_EAC_EAVS where length(fipscode)=10 and try_to_number(c1b)>0 and try_to_number(c9a)>=0 group by 1 having sum(try_to_number(c1b))>=500),
    v as (select county_fips, total_jail_pop_rate jail, try_to_number(black_pop_15to64)/nullif(total_pop_15to64,0) black_sh
          from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_VERA_INCARCERATION_TRENDS where year=2018 and total_jail_pop_rate is not null),
    j as (select e.*, rej/ret rej_share, v.jail, v.black_sh, ntile(10) over (order by rej/ret) dec from e join v on v.county_fips=e.cf)
    select dec, count(*) counties, round(median(rej_share)*100,2) rej_pct, round(median(jail),0) jail_rate_med, round(median(black_sh)*100,1) black_pct, round(corr(rej_share, jail),3) r_all
    from j group by 1 order by 1""", "deciles on vera 2018"))
