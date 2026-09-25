-- (re-run of q22 with text casts) Rename waves: latest name change per filer (FORMER/CHANGED, all nine quarters), by quarter of change, split by buzzword in the NEW name and not in the old one
with u as (
  select '2024Q1' q, * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q1 union all
  select '2024Q2', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q2 union all
  select '2024Q3', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q3 union all
  select '2024Q4', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q4 union all
  select '2025Q1', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q1 union all
  select '2025Q2', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q2 union all
  select '2025Q3', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q3 union all
  select '2025Q4', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q4 union all
  select '2026Q1', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2026Q1
),
r as (
  select try_to_number(CIK) cik, NAME, FORMER, try_to_date(CHANGED,'YYYYMMDD') chg, AFS, SIC, COUNTRYBA
  from u where FORMER is not null and trim(FORMER)<>''
  qualify row_number() over (partition by try_to_number(CIK), try_to_date(CHANGED,'YYYYMMDD') order by q desc)=1
),
t as (
  select *, 
    iff(regexp_like(upper(NAME), '.*(\bAI\b|\.AI\b|ARTIFICIAL INTELLIGENCE).*') and not regexp_like(upper(FORMER), '.*(\bAI\b|\.AI\b|ARTIFICIAL INTELLIGENCE).*'),1,0) to_ai,
    iff(regexp_like(upper(NAME), '.*(BITCOIN|\bBTC\b|CRYPTO|BLOCKCHAIN|DIGITAL ASSET|TOKEN|ETHEREUM|\bETH\b|SOLANA|\bSOL\b|DOGE|\bXRP\b|TREASURY).*') and not regexp_like(upper(FORMER), '.*(BITCOIN|\bBTC\b|CRYPTO|BLOCKCHAIN|DIGITAL ASSET|TOKEN|ETHEREUM|\bETH\b|SOLANA|\bSOL\b|DOGE|\bXRP\b|TREASURY).*'),1,0) to_crypto,
    iff(regexp_like(upper(NAME), '.*QUANTUM.*') and not regexp_like(upper(FORMER), '.*QUANTUM.*'),1,0) to_quantum
  from r where chg >= '2022-01-01'
)
select 'qtr' k, year(chg)||'Q'||quarter(chg) qtr, count(*)::text renames, sum(to_ai)::text to_ai, sum(to_crypto)::text to_crypto, sum(to_quantum)::text to_quantum,
  count_if(AFS='4-NON')::text non_acc, null a, null b
from t group by 2
union all
select 'name', year(chg)||'Q'||quarter(chg), NAME, iff(to_ai=1,'AI',iff(to_crypto=1,'CRYPTO','QUANTUM')), FORMER, AFS, SIC, COUNTRYBA, cik::text
from t where (to_ai+to_crypto+to_quantum)>0 and chg >= '2024-04-01'
order by 1 desc, 2, 4
