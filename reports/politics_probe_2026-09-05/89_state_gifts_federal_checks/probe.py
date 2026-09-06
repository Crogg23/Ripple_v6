import os, sys
from _shared.q import run, open_log
from _shared.cols import cols
HERE = os.path.dirname(os.path.abspath(__file__)); open_log(os.path.join(HERE, "probe.log"))
STEP = int(os.environ.get("STEP", "1"))
if STEP == 1:
    cols("LIBRARY_MARTS", "POLITICS", "POLITICS__TX_LOBBY_FOOD_BEVERAGE")
    cols("LIBRARY_MARTS", "POLITICS", "POLITICS__TX_LOBBY_GIFTS")
    cols("LIBRARY_MARTS", "POLITICS", "POLITICS__CA_LOBBY_COVER")
    cols("LIBRARY_MARTS", "FINANCE", "FINANCE__FED_FEC_INDIV_CONTRIBUTIONS")
if STEP == 2:
    print(run("""select 'FOOD' t, count(*) n, count(distinct filername) filers, min(activitydate) d0, max(activitydate) d1, count(activityexactamount) exact_n, count(distinct activityamountcd) cds from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_FOOD_BEVERAGE
      union all select 'GIFTS', count(*), count(distinct filername), min(periodenddt), max(periodenddt), count(activityexactamount), count(distinct activityamountcd) from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_GIFTS""", "tx fill"))
    print(run("select activityamountcd, activityamountrangelow lo, activityamountrangehigh hi, count(*) n from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_FOOD_BEVERAGE group by 1,2,3 order by 4 desc limit 10", "tx amount codes"))
    print(run("select filername, recipientnamefirst, recipientnamelast, recipientpersenttypecd, activityamountcd, activitydate from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_FOOD_BEVERAGE limit 5", "tx sample"))
    print(run("select donor_name, city, state, employer, occupation, transaction_amt from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS where state='TX' and occupation ilike '%LOBBY%' limit 5", "fec tx lobbyist sample"))
    print(run("select count(distinct firm_name) firms, count(*) n, min(rpt_date) d0, max(rpt_date) d1 from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER", "ca cover"))
if STEP == 3:
    # TX filer "Last, First (Mr.)" -> "LAST, FIRST"; FEC donor "LAST, FIRST M." ; match multi-word prefix, TX donors flagged lobbyist by occupation
    sql = """
    with tx as (
      select distinct upper(trim(regexp_replace(filername, '\\\\s*\\\\(.*\\\\)\\\\s*$', ''))) nm from (
        select filername from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_FOOD_BEVERAGE union all select filername from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_GIFTS)
      where filername like '%,%'),
    fec as (
      select donor_name, city, count(*) n, sum(transaction_amt) amt from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
      where state='TX' and occupation ilike '%LOBBY%' and transaction_amt>0 group by 1,2)
    select count(distinct tx.nm) tx_filers_matched, (select count(*) from tx) tx_filers, count(distinct fec.donor_name) fec_names, sum(fec.n) gifts, sum(fec.amt) dollars
    from tx join fec on fec.donor_name like tx.nm || '%'
    """
    print(run(sql, "tx filer -> fec lobbyist donor"))
    sql2 = sql.replace("select count(distinct tx.nm) tx_filers_matched, (select count(*) from tx) tx_filers, count(distinct fec.donor_name) fec_names, sum(fec.n) gifts, sum(fec.amt) dollars",
                       "select tx.nm, fec.donor_name, fec.city, fec.n, fec.amt") + " order by fec.amt desc limit 8"
    print(run(sql2, "eye check top 8"))
if STEP == 4:
    # same match, no occupation filter: how many TX filers show up as any TX federal donor under the full "LAST, FIRST" string
    print(run("""
    with tx as (
      select distinct upper(trim(regexp_replace(filername, '\\\\s*\\\\(.*\\\\)\\\\s*$', ''))) nm from (
        select filername from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_FOOD_BEVERAGE union all select filername from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_GIFTS)
      where filername like '%,%'),
    fec as (select donor_name, count(*) n, sum(transaction_amt) amt from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS where state='TX' and transaction_amt>0 group by 1)
    select count(distinct tx.nm) tx_filers_matched, count(distinct fec.donor_name) fec_names, sum(fec.n) gifts, sum(fec.amt) dollars
    from tx join fec on fec.donor_name = tx.nm""", "exact LAST, FIRST match, any TX donor"))
if STEP == 5:
    print(run("""
    with tx as (
      select distinct upper(trim(regexp_replace(filername, '\\\\s*\\\\(.*\\\\)\\\\s*$', ''))) nm from (
        select filername from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_FOOD_BEVERAGE union all select filername from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_GIFTS)
      where filername like '%,%'),
    fec as (select donor_name, city, employer, occupation, count(*) n, sum(transaction_amt) amt from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS where state='TX' and transaction_amt>0 group by 1,2,3,4)
    select tx.nm, fec.city, fec.employer, fec.occupation, fec.n, fec.amt from tx join fec on fec.donor_name = tx.nm order by fec.amt desc limit 8""", "eye check exact match top 8"))
