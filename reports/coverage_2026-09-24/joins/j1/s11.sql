-- PPP miss check: how many MO/KS rows exist, how many nursing-home NAICS (623110) in MO, date span, and a sample of MO nursing-home borrowers
select BORROWERSTATE, count(*) n, count_if(NAICSCODE='623110') nh_naics, min(DATEAPPROVED) d0, max(DATEAPPROVED) d1, min(CURRENTAPPROVALAMOUNT) minamt,
  listagg(iff(NAICSCODE='623110' and BORROWERNAME ilike '%HEALTH%CARE%CENTER%', BORROWERNAME||' ('||BORROWERCITY||')', null), '; ') within group (order by BORROWERNAME) sample_hcc
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS where BORROWERSTATE in ('MO','KS') group by 1
