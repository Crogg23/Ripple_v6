-- Peer/base rate for "dropped fast": share of appeals closed without a merits ruling within 90 days of docketing.
-- Detention habeas docketed Oct-Dec 2025 (90+ days before data ends) vs other U.S.-party civil appeals docketed FY2023-24. Split by the US-appellant flag.
with a as (select CIRCUIT, DOCKET, REOPEN, try_to_date(DOCKET_DATE::string) dd, try_to_date(JUDGMENT_DATE::string) jd,
             NATURE_OF_SUIT::string nos, APPEAL_TYPE::string t, US_APPELLANT::string usa, DISPOSITION::string disp
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
           where try_to_date(DOCKET_DATE::string) >= '2022-10-01'
           qualify row_number() over (partition by CIRCUIT, DOCKET, REOPEN order by TAPE_YEAR) = 1)
select case when nos='463' and dd between '2025-10-01' and '2025-12-31' then 'detention habeas, docketed Oct-Dec 2025'
            when t='3' and nos<>'463' and dd between '2022-10-01' and '2024-09-30' then 'other US-party civil, docketed FY2023-24' end grp,
  usa us_appellant_flag, count(*) appeals,
  sum(iff(disp in ('4','5') and datediff('day', dd, jd) <= 90,1,0)) closed_no_ruling_90d,
  sum(iff(disp in ('1','2') and datediff('day', dd, jd) <= 90,1,0)) closed_merits_90d,
  round(sum(iff(disp in ('4','5') and datediff('day', dd, jd) <= 90,1,0)) / count(*), 3) share_no_ruling_90d
from a group by 1,2 having grp is not null order by 1,2
