import os, sys
from _shared.q import run, open_log
from _shared.cols import cols
HERE = os.path.dirname(os.path.abspath(__file__)); open_log(os.path.join(HERE, "probe.log"))
STEP = int(os.environ.get("STEP", "1"))
if STEP == 1:
    cols("LIBRARY_MARTS", "EDUCATION", "EDUCATION__FED_SENATE_LDA_FILINGS")
    cols("LIBRARY_MARTS", "REGULATORY", "REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS")
if STEP == 2:
    print(run("select min(filing_year) y0, max(filing_year) y1, count(*) n, count(distinct filing_uuid) uu, sum(iff(try_to_number(income)>0,1,0)) inc_pos, sum(iff(try_to_number(expenses)>0,1,0)) exp_pos from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_SENATE_LDA_FILINGS", "lda range"))
    print(run("select filing_year, count(*) n from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_SENATE_LDA_FILINGS group by 1 order by 1", "lda by year"))
    print(run("""select client_name, count(*) n, sum(try_to_number(income)) inc, sum(try_to_number(expenses)) exp from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_SENATE_LDA_FILINGS
      where client_name ilike '%HEALTH CARE ASSOCIATION%' or client_name ilike '%LEADINGAGE%' or client_name ilike '%HOSPICE%' or client_name ilike '%KIDNEY CARE%' or client_name ilike '%HOMECARE%' or client_name ilike 'DAVITA%' or client_name ilike 'FRESENIUS%'
      group by 1 order by 2 desc limit 15""", "lda trade groups"))
    print(run("""select publication_year, count(*) n, sum(iff(comments_close_on is not null,1,0)) with_close from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
      where agencies ilike '%centers for medicare%' group by 1 order by 1""", "fr cms by year"))
if STEP == 3:
    print(run("select min(publication_date) d0, max(publication_date) d1, count(*) n from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS", "fr full range"))
    print(run("select min(filing_year) y0, max(filing_year) y1, count(*) n from LIBRARY_RAW.LANDING.FED_SENATE_LDA_FILINGS", "lda landing range"))
