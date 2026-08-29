# Every real date / datetime / month-year / quarter / year column — 1275 columns, 453 tables

Source: reports/time_index/columns.csv (2026-08-20 value scan) + clock_index.csv descriptions. Excludes backups, plumbing, findings, ingest stamps, and columns that failed the value check.


### CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_RECEIVED | date (typed) | 2011-12-01 → 2026-07-23 | reported | try_to_date on the left 10 characters of CFPB's 'Date received': the day the agency received the complaint — the harm itself has no date anywhere in this source, so this reporting stamp is the honest axis for all 17.2M rows. |
| DATE_SENT_TO_COMPANY | date (typed) | 2011-12-01 → 2026-07-23 | reported | try_to_date on the left 10 characters: the day CFPB forwarded the complaint to the company — a second step in the reporting pipeline, not an event in the world. |
| DAYS_RECEIVED_TO_COMPANY | year only | 1748 → 1962 | not_a_date | The mart computes it as datediff('day', date_received, date_sent_to_company) — this is the exact duration column named in the brief as an already-confirmed trap. |
| RECEIVED_MONTH | date (typed) | 2011-12-01 → 2026-07-01 | reported | The mart computes it as date_trunc('month', date_received): a real date value carrying the same reporting clock, rolled to month grain. |
| RECEIVED_YEAR | date (typed) | 2011-01-01 → 2026-01-01 | reported | The mart computes it as date_trunc('year', date_received): the same reporting clock rolled to year grain. |

### CONSUMER_SAFETY.CONSUMER_SAFETY__FED_CPSC_NEISS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_YEAR | year only | 1999 → 2025 | ingest | try_to_number("_SRC_YEAR") - our own loader's provenance tag for which annual NEISS file the row came from, not an independently observed date; it mirrors the treatment year but must never be the clock. |
| TREATMENT_DATE | date (typed) | 1999-01-01 → 2025-12-31 | happened | try_to_date("TREATMENT_DATE",'MM/DD/YYYY') - the day the patient was treated in the emergency department for the injury. |

### CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_RECEIVED | date (typed) | 1995-01-01 → 2026-07-22 | reported | try_to_date(C17,'YYYYMMDD') - the day NHTSA ODI received the complaint; the gap from fail_date is directly measurable. |
| FAIL_DATE | date (typed) | 1900-01-01 → 2026-07-21 | happened | try_to_date(C8,'YYYYMMDD') - the day the component failed or the incident occurred; the year-0003 minimum is source typos, not the cast. |
| MODEL_YEAR | year only | 1949 → 2027 | not_a_date | trim(C6) YEARTXT kept as text while every real date in the same staging model is try_to_date'd - a vehicle model-year vintage label (NHTSA uses 9999 for unknown), a product designation rather than an event. |

### CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| CLOSE_DATE | date (typed) | 1972-05-30 → 2026-07-22 | decided | try_to_date(C8,'YYYYMMDD') - the day NHTSA closed the investigation; with open_date it also bounds how long the investigation stayed open. |
| MODEL_YEAR | year only | 1965 → 2026 | not_a_date | trim(C4) YEAR_TXT kept as text and used as part of the dedupe key - a vehicle model-year vintage label, not an event date. |
| OPEN_DATE | date (typed) | 1972-03-10 → 2026-07-13 | decided | try_to_date(C7,'YYYYMMDD') - the day NHTSA opened the investigation, an agency action. |

### CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_RECALLS
| column | format | range | meaning | description |
|---|---|---|---|---|
| BEGIN_MANUFACTURE_DATE | date (typed) | 1900-01-01 → 2026-06-25 | span_start | try_to_date(C9,'YYYYMMDD') as BGMAN - the start of the manufacturing date range of the recalled vehicles. |
| END_MANUFACTURE_DATE | date (typed) | 1900-01-01 → 2029-01-09 | span_end | try_to_date(C10,'YYYYMMDD') as ENDMAN - the end of the manufacturing date range of the recalled vehicles. |
| MODEL_YEAR | year only | 1965 → 2027 | not_a_date | trim(C5) YEARTXT kept as text - the affected vehicles' model-year vintage label, a product designation rather than an event. |
| NOTIFICATION_DATE | date (typed) | 1980-12-31 → 2027-08-16 | happened | try_to_date(C13,'YYYYMMDD') aliased from NHTSA's ODATE - the day owners were notified of the recall; the 11 far-future rows (max 3019) are source typos, and the staging model also holds RCDATE (report received) which the mart does not expose. |

### CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_ENTITIES
| column | format | range | meaning | description |
|---|---|---|---|---|
| DORM_DATE | date (typed) | 1997-11-07 → 2010-03-16 | decided | try_to_date(...,'DD-MON-YYYY') - when the entity was declared dormant by the registry. |
| INACTIVATION_DATE | date (typed) | 1930-11-30 → 2017-12-07 | decided | try_to_date(...,'DD-MON-YYYY') - when the registry or service provider marked the entity inactive. |
| INCORPORATION_DATE | date (typed) | 1865-10-26 → 2029-04-15 | happened | try_to_date(INCORPORATION_DATE,'DD-MON-YYYY') - the day the offshore entity was incorporated. |
| STRUCK_OFF_DATE | date (typed) | 1919-02-02 → 2024-06-14 | decided | try_to_date(...,'DD-MON-YYYY') - when the registrar struck the entity off the register, an authority action. |

### CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OTHERS
| column | format | range | meaning | description |
|---|---|---|---|---|
| CLOSED_DATE | date (typed) | 1994-12-21 → 2016-12-29 | decided | try_to_date(CLOSED_DATE,'DD-MON-YYYY') - when the entity was closed out by the registry or provider. |
| INCORPORATION_DATE | date (typed) | 1933-08-05 → 2016-09-22 | happened | try_to_date(INCORPORATION_DATE,'DD-MON-YYYY') - the day the foundation/partnership was formed. |
| STRUCK_OFF_DATE | date (typed) | 1991-11-14 → 2013-08-12 | decided | try_to_date(...,'DD-MON-YYYY') - when the registrar struck the node off the register. |

### CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS
| column | format | range | meaning | description |
|---|---|---|---|---|
| END_DATE | date (typed) | 1899-12-30 → 2028-12-01 | span_end | try_to_date(END_DATE,'DD-MON-YYYY') - when the relationship ended, closing the edge's period. |
| NODE_ID_END | date as text (yyyymmdd) | 2000-01-01 → 2017-12-31 | not_a_date | nullif(trim(NODE_ID_END)) - the graph edge's target node identifier, a plain ID string. |
| NODE_ID_START | date as text (yyyymmdd) | 2000-02-02 → 2017-12-04 | not_a_date | nullif(trim(NODE_ID_START)) - the graph edge's source node identifier, a plain ID string. |
| START_DATE | date (typed) | 1759-12-30 → 2029-11-02 | span_start | try_to_date(START_DATE,'DD-MON-YYYY') - when the relationship (officer_of, intermediary_of, registered_address) began, opening the edge's period. |

### CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF
| column | format | range | meaning | description |
|---|---|---|---|---|
| RULING_DATE | date (typed) | 1900-01-01 → 2026-06-01 | decided | try_to_date(RULING//'01','YYYYMMDD') - the month the IRS ruled the organization tax-exempt; RULING is a YYYYMM string per the staging header, so the day part is synthetic. |
| TAX_PERIOD_MONTH | date (typed) | 1979-06-01 → 2026-11-01 | span_end | try_to_date(TAX_PERIOD//'01','YYYYMMDD') - the same YYYYMM value in date form with a synthetic day, a duplicate of tax_period_yyyymm rather than an independent clock. |
| TAX_PERIOD_YYYYMM | month-year | 1979 → 2026 | span_end | Raw trimmed YYYYMM text (staging header states it explicitly) - the tax period whose asset/income figures the row reports, ending in that month. |

### CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_ES_BORME
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACT_MONTH | date (typed) | 2026-06-01 → 2026-06-01 | reported | date_trunc('month', date) computed in the mart - a derived truncation of the same publication clock, not an independent date. |
| ACT_YEAR | date (typed) | 2026-01-01 → 2026-01-01 | reported | date_trunc('year', date) computed in the mart - a derived truncation of the same publication clock. |
| DATE | date (typed) | 2026-06-01 → 2026-06-01 | reported | try_to_date(DATE,'YYYY-MM-DD') in staging - the BORME gazette date on which the corporate act was published (publication, not necessarily when the act itself occurred). |

### CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_IE_CRO
| column | format | range | meaning | description |
|---|---|---|---|---|
| FINANCIAL_YEAR_END | date (typed) | 1753-01-01 → 2033-06-30 | reported | MISNAMED COLUMN - staging maps LAST_ACCOUNTS_DATE into it and its own header says there is no recurring financial-year-end field, so this is the date the last annual accounts were FILED, not a period end. |
| INCORPORATION_DATE | date (typed) | 1753-01-01 → 2026-08-07 | happened | try_to_date(COMPANY_REG_DATE,'YYYY-MM-DD') - the day the Irish company was incorporated; the staging comment records that its 1970 rows were re-checked and are real, not the epoch trap. |
| INCORPORATION_YEAR | year only | 1753 → 2026 | happened | year(incorporation_date) computed in the mart - a derived year of the same incorporation clock. |

### CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE
| column | format | range | meaning | description |
|---|---|---|---|---|
| INCORPORATION_DATE | date (typed) | 1701-06-16 → 2026-06-30 | happened | try_to_date("IncorporationDate",'DD/MM/YYYY') - the day the company was incorporated; the in-file 2026-08-18 note says only 9 rows sit at 1970-01-01 and that the census's 2,237 epoch count and 1327 minimum could NOT be reproduced live. |

### CORPORATE_REGISTRY.CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC
| column | format | range | meaning | description |
|---|---|---|---|---|
| CEASED_ON | date (typed) | 1962-09-16 → 2026-08-04 |  |  |
| DOB_YEAR | year only | 1775 → 2024 | happened | try_to_number(DOB_YEAR) - the beneficial owner's birth year, the only clock among the two columns offered; note the staging model also carries notified_on and ceased_on, which are far better table clocks but were not in this batch. |
| NOTIFIED_ON | date (typed) | 1776-07-04 → 2026-06-04 |  |  |

### CRIMINAL_JUSTICE.CRIMINAL_JUSTICE__FED_BJS_DATA
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 1993 → 1993 | reported | Raw passthrough of YEAR (no cast): the NCVS data year. LOW - the compiled SQL shows only a passthrough, so whether it means the incident year or the collection year is not established from files; treated as the survey year. |

### ECONOMICS.ECONOMICS__FED_BLS_QCEW
| column | format | range | meaning | description |
|---|---|---|---|---|
| ANNUAL_AVG_WEEKLY_WAGE | year only | 1700 → 2035 | not_a_date | try_to_number(ANNUAL_AVG_WKLY_WAGE) is a dollar amount; it only matched the name sweep because 'weekly' contains 'week'. |
| YEAR | year only | 2022 → 2022 | happened | try_to_number(YEAR) in the mart SQL; the row is a county-industry-ownership measurement for that calendar year, so the year is when the measured thing was true. |

### ECONOMICS.ECONOMICS__FED_DOL_FORM5500
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_RECEIVED | date (typed) | 2026-01-02 → 2026-06-24 | reported | try_to_date(DATE_RECEIVED) is when DOL received the filing, the one clock that dates the filing event itself rather than the plan behind it, so it is the honest placement for a filing table. |
| FORM_PLAN_YEAR_BEGIN_DATE | date (typed) | 1923-01-01 → 2026-01-01 | span_start | try_to_date(FORM_PLAN_YEAR_BEGIN_DATE); the plan-year opening bound as printed on the form header, a near-duplicate of plan_year_begin_date. |
| PLAN_EFF_DATE | date (typed) | 1878-01-01 → 2026-01-01 | happened | try_to_date(PLAN_EFF_DATE) is when the benefit plan came into existence, a real-world event, but it predates the filing by decades so it must not be used to place the filing; it is also the likely source of the census floor of 1878-01-01 and of some of the 71 epoch-1970 rows, since the cast is a bare try_to_date. |

### ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT
| column | format | range | meaning | description |
|---|---|---|---|---|
| AUDIT_YEAR | year only | 2016 → 2026 | span_start | Raw TEXT passthrough of AUDIT_YEAR, the year label of the audited fiscal period that fy_start_date/fy_end_date bound precisely. |
| FAC_ACCEPTED_DATE | date (typed) | 2016-07-17 → 2026-07-26 | reported | try_to_date(FAC_ACCEPTED_DATE) is when the Federal Audit Clearinghouse accepted the submission; it dates the filing event, is present on essentially every row, and drives the census ceiling of 2026-07-26. |
| FY_END_DATE | date (typed) | 2016-01-01 → 2026-06-30 | span_end | try_to_date(FY_END_DATE); closing bound of the audited fiscal year, the best period anchor if you want to trend by year audited rather than by year filed. |
| FY_START_DATE | date (typed) | 2002-07-01 → 2026-06-29 | span_start | try_to_date(FY_START_DATE); opening bound of the fiscal year the single audit covers. |

### ECONOMICS.ECONOMICS__FED_FDIC_FAILED_BANKS
| column | format | range | meaning | description |
|---|---|---|---|---|
| FAIL_DATE | date (typed) | 1970-02-22 → 2026-05-01 | happened | Staging parses FAILDATE with two strict formats (YYYY-MM-DD then MM/DD/YYYY); it is the day the bank actually failed, the real-world event this table exists to record. |

### ECONOMICS.ECONOMICS__FED_FOREIGNASSISTANCE
| column | format | range | meaning | description |
|---|---|---|---|---|
| FISCAL_YEAR | year only | 1946 → 2026 | happened | Raw passthrough of FISCAL_YEAR and the only time-shaped column; it is the fiscal year the assistance transaction occurred in, so it places the row at year resolution — never date-parse it, a bare cast would read '2012' as epoch seconds. |

### ECONOMICS.ECONOMICS__FED_GRANTS_GOV
| column | format | range | meaning | description |
|---|---|---|---|---|
| CLOSE_DATE | date (typed) | 2026-07-02 → 2027-06-07 | span_end | try_to_date(CLOSE_DATE); the application deadline, i.e. the closing bound of the open-for-applications window, so future values are correct not corrupt. |
| POSTED_DATE | date (typed) | 2026-06-25 → 2026-07-01 | reported | try_to_date(POSTED_DATE); the day the funding opportunity was published on Grants.gov, which is the event this row records. |

### ECONOMICS.ECONOMICS__FED_IRS_990
| column | format | range | meaning | description |
|---|---|---|---|---|
| TAX_YEAR | month-year | 2023 → 2025 | span_start | try_to_number(taxyr) is a plain year integer labelling the same covered period at coarser resolution; safe as a number, dangerous if ever cast to a date. |

### ECONOMICS.ECONOMICS__FED_IRS_990_EFILE_INDEX
| column | format | range | meaning | description |
|---|---|---|---|---|
| SUB_DATE | date (typed) | 2017-01-03 → 2026-01-01 | reported | The submission date to the IRS, now parsed by three explicit strict formats after the documented 2026-08-18 fix; grain is only YEAR because the model's own comment records that 3,192,934 rows (57.6%) carry a bare 4-digit filing year, not a full date — the census min of 1970-01-01 and its 3.19M epoch rows are the PRE-FIX reading and are stale. |
| SUB_DATE_RAW | year only | 2017-01-05 → 2020-01-28 |  |  |
| TAX_PERIOD | month-year | 1916 → 2026 | span_end | Raw passthrough of TAX_PERIOD, the IRS YYYYMM period-ending code; month grain at best and never safe to date-parse bare. |

### ECONOMICS.ECONOMICS__FED_IRS_AUTO_REVOCATIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| REINSTATEMENT_DATE | date (typed) | 2010-05-15 → 2026-05-15 | decided | try_to_date(REINSTATEMENT_DATE); the day the IRS restored exempt status, populated only for the subset that came back. |
| REVOCATION_DATE | date (typed) | 2010-05-15 → 2026-05-15 | decided | try_to_date(REVOCATION_DATE); the day the IRS revoked exempt status. Chosen over the 'reported' posting date despite the stated preference because the posting date is a monthly batch-publication artifact that would pile every revocation onto ~190 publication days. |
| REVOCATION_POSTING_DATE | date (typed) | 2011-06-09 → 2026-08-04 | reported | try_to_date(REVOCATION_POSTING_DATE); when the IRS published the revocation to the public list, always later than the revocation itself — the gap is measurable here. |

### ECONOMICS.ECONOMICS__FED_IRS_BMF
| column | format | range | meaning | description |
|---|---|---|---|---|
| RULING_DATE | month-year | 1900 → 2026 | decided | trim(ruling) aliased to ruling_date — the BMF RULING field, the YYYYMM in which the IRS granted the organization's exemption; it is the only real event clock here and places every nonprofit by when it was recognised. Stored as TEXT and never parsed, so month grain and no epoch damage yet. |
| TAX_PERIOD | month-year | 1979 → 2026 | span_end | trim(tax_period) only — a raw TEXT YYYYMM period-ending code from the Business Master File; month grain, and an 6-digit bare date-parse would epoch-collapse it. |

### ECONOMICS.ECONOMICS__FED_IRS_EO_PR
| column | format | range | meaning | description |
|---|---|---|---|---|
| TAX_PERIOD | month-year | 2011 → 2026 | span_end | Raw TEXT passthrough of the BMF YYYYMM period-ending code; it is the only candidate on this Puerto Rico exempt-org extract, so it is the primary by default even though it is a period bound, not an event. |

### ECONOMICS.ECONOMICS__FED_IRS_REVOCATION
| column | format | range | meaning | description |
|---|---|---|---|---|
| REINSTATEMENT_DATE | date as text (dd_mon_yyyy) | 2010-05-15 → 2026-04-15 | decided | trim(exemption_reinstatement_date), unparsed TEXT; the day exempt status was restored, and the model uses its non-emptiness to build was_reinstated. |
| REVOCATION_DATE | date as text (dd_mon_yyyy) | 2010-05-15 → 2026-03-15 | decided | trim(revocation_date) over a staging model that is itself a bare TEXT rename — the day the IRS revoked exempt status, stored unparsed. Same reasoning as the auto_revocations twin: the decided date beats the batch posting date for honest placement. |
| REVOCATION_POSTING_DATE | date as text (dd_mon_yyyy) | 2011-06-09 → 2026-06-09 | reported | trim() of an unparsed TEXT column; when the IRS published the revocation to the list. |

### ECONOMICS.ECONOMICS__FED_IRS_SOI_CHARITIES
| column | format | range | meaning | description |
|---|---|---|---|---|
| TAX_PERIOD | month-year | 2000 → 2026 | span_end | Raw TEXT passthrough of the YYYYMM period-ending code and the only candidate on this 2,450-row SOI extract. |

### ECONOMICS.ECONOMICS__FED_PBGC_DATA
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_YEAR | year only | 2010 → 2023 | happened | Raw passthrough of DATA_YEAR, the year each pension-insurance metric describes; it is the year the measured thing was true, and it is part of the model's dedup partition key so it is populated. |

### ECONOMICS.ECONOMICS__FED_SBA_LOANS
| column | format | range | meaning | description |
|---|---|---|---|---|
| APPROVAL_DATE | date (typed) | 1990-10-01 → 2026-03-31 | decided | try_to_date(APPROVALDATE); SBA approving the loan is an authority acting, and the model's own grain comment shows APPROVALDATE is part of the row identity, so it is the one date present on every loan — first_disbursement_date is 'happened' but only exists for the disbursed subset. |
| APPROVAL_FISCAL_YEAR | year only | 1991 → 2026 | decided | try_to_number(APPROVALFY) is a fiscal-year integer restating approval_date at year grain; safe because it is a number, and it must stay one. |
| CHARGEOFF_DATE | date (typed) | 1991-10-08 → 2026-10-22 | happened | try_to_date(CHARGEOFFDATE); the day the loan was written off — the harm-side outcome clock on this table. |
| FIRST_DISBURSEMENT_DATE | date (typed) | 1987-04-01 → 2028-06-18 | happened | try_to_date(FIRSTDISBURSEMENTDATE); the day the money actually moved — the truest real-world event here, but sparsely populated relative to approval_date. |
| PAID_IN_FULL_DATE | date (typed) | 2005-05-31 → 2026-02-28 | happened | try_to_date(PAIDINFULLDATE); the day the loan was repaid, an outcome event on a subset of rows. |

### ECONOMICS.ECONOMICS__FED_SBA_PPP
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_APPROVED | date (typed) | 2020-04-03 → 2021-07-19 | decided | try_to_date(DATEAPPROVED); SBA approval of the PPP loan, present on every row and used as the dedup ordering key in the model, and it matches the census window 2020-04-03 to 2024-09-30. |
| LOAN_STATUS_DATE | date (typed) | 2020-04-30 → 2024-09-30 | decided | try_to_date(LOANSTATUSDATE); the date SBA set the loan's current status (paid in full, charged off, etc.), so it is an authority action, later than approval. |

### ECONOMICS.ECONOMICS__FED_SEC_EDGAR
| column | format | range | meaning | description |
|---|---|---|---|---|
| REPORTDATE | date as text (iso) | 2025-09-28 → 2026-07-02 | span_end | Raw TEXT passthrough of the data.sec.gov 'reportDate', the period the filing reports on (period end), and the only usable clock in the candidate list; note the model also carries FILEDAT, the true filing date, which the name sweep missed. |

### ECONOMICS.ECONOMICS__FED_TREASURY_AVG_INTEREST_RATES
| column | format | range | meaning | description |
|---|---|---|---|---|
| RECORD_CALENDAR_YEAR | year only | 2001 → 2026 | happened | Passthrough of the calendar-year component of record_date; a plain year value. |
| RECORD_DATE | date (typed) | 2001-01-31 → 2026-05-31 | happened | The Treasury observation date, part of the model's surrogate key; the file is monthly (census window 2001-01-01 to 2026-05-31 over 4,961 rows), so day grain would be a false claim. |
| RECORD_FISCAL_YEAR | year only | 2001 → 2026 | happened | Passthrough of the Treasury Fiscal Data API's own fiscal-year component of record_date; a plain year value, safe only as a number. |
| REPORT_MONTH | date (typed) | 2001-01-01 → 2026-05-01 | happened | Literally date_trunc('month', record_date) in the mart — a derived convenience truncation of the same observation clock, so it is a real DATE at month grain. |
| REPORT_YEAR | date (typed) | 2001-01-01 → 2026-01-01 | happened | Literally date_trunc('year', record_date) — a derived DATE at year grain off the same observation clock. |

### ECONOMICS.ECONOMICS__FED_TREASURY_DEBT_OUTSTANDING
| column | format | range | meaning | description |
|---|---|---|---|---|
| RECORD_CALENDAR_YEAR | year only | 1790 → 2025 | happened | Raw passthrough of the calendar-year component of record_date. |
| RECORD_DATE | date (typed) | 1790-01-01 → 2025-09-30 | happened | try_to_date(RECORD_DATE); 237 rows spanning 1790 to 2025 is one row per year, so this is an ANNUAL series and day grain would be a false claim — the census CORRUPT_RANGE flag is a false alarm, US debt outstanding genuinely starts in 1790 and the single epoch-1970 row is a real 1970 observation. |
| RECORD_FISCAL_YEAR | year only | 1790 → 2025 | happened | Raw passthrough of the API's fiscal-year component of record_date. |

### ECONOMICS.ECONOMICS__FED_TREASURY_DEBT_TO_PENNY
| column | format | range | meaning | description |
|---|---|---|---|---|
| RECORD_DATE | date (typed) | 1993-04-01 → 2026-06-15 | happened | The model description states each row is one daily debt snapshot, and the census window 1993-04-01 to 2026-06-15 over 8,329 rows matches business-daily coverage. |

### ECONOMICS.ECONOMICS__FED_TREASURY_DTS_DEPOSITS
| column | format | range | meaning | description |
|---|---|---|---|---|
| RECORD_CALENDAR_YEAR | year only | 2005 → 2026 | happened | Passthrough of the calendar-year component of record_date. |
| RECORD_DATE | date (typed) | 2005-10-03 → 2026-08-07 | happened | try_to_date(RECORD_DATE) on the Daily Treasury Statement deposits feed; 478k rows over 2005-10-03 to 2026-08-07 is a genuine daily series. |
| RECORD_FISCAL_YEAR | year only | 2006 → 2026 | happened | Passthrough of the API's fiscal-year component of record_date. |

### ECONOMICS.ECONOMICS__FED_TREASURY_MTS_RECEIPTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| CURRENT_MONTH_GROSS_RCPT_AMT | date as text (yyyymmdd) | 1781 → 1795 | not_a_date | try_to_double(...) — a dollar amount that matched the name sweep only because it starts with 'current_month'. |
| RECORD_CALENDAR_YEAR | year only | 2015 → 2026 | happened | Passthrough of the calendar-year component of record_date. |
| RECORD_DATE | date (typed) | 2015-03-31 → 2026-06-30 | happened | try_to_date(RECORD_DATE) on the Monthly Treasury Statement receipts feed; the census window 2015-03-31 to 2026-06-30 sits on month-ends, so month is the true resolution. |
| RECORD_FISCAL_YEAR | year only | 2015 → 2026 | happened | Passthrough of the API's fiscal-year component of record_date. |

### ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACTION_DATE | date as text (iso) | 2006-10-01 → 2026-02-12 | happened | The day the assistance transaction was executed — the real-world money event and the natural clock for a 19.9M-row transaction table; note this model is a pure quoted passthrough with NO cast, so it is still TEXT, which is why the census never measured it. |
| ACTION_DATE_FISCAL_YEAR | year only | 2007 → 2026 | not_a_date | Fiscal-year restatement of action_date, kept as raw TEXT here (unlike the contracts_full twin, which was cast to a date and destroyed) — leave it as a number/string, never date-parse it. |
| INITIAL_REPORT_DATE | date as text (iso) | 2010-01-19 → 2026-07-02 | reported | When the transaction was first reported into the federal award system, later than action_date; the action-to-report gap is itself measurable here. |
| LAST_MODIFIED_DATE | date as text (iso) | 2006-10-01 → 2026-07-02 | reported | USASpending's record-maintenance stamp for the last edit to this transaction record — publisher bookkeeping, not an event. |
| PERIOD_OF_PERFORMANCE_CURRENT_END_DATE | date as text (iso) | 1991-08-31 → 2035-12-31 | span_end | Current closing bound of the performance window; raw TEXT passthrough, and 'current' means it moves as the award is modified. |
| PERIOD_OF_PERFORMANCE_START_DATE | date as text (iso) | 1954-07-01 → 2027-06-29 | span_start | Opening bound of the award's performance window; raw TEXT passthrough, no cast in the model. |

### ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACTION_DATE | date as text (iso) | 2024-10-01 → 2025-09-30 | happened | The day the contract transaction was executed, the real-world event for this 6.3M-row transaction table; the model is a bare column list with no casts, so it is still TEXT and the census could not measure it. |
| LAST_MODIFIED_DATE | date as text (iso) | 2024-09-30 → 2026-06-23 | reported | USASpending's own last-edit stamp on the record — publisher bookkeeping, never an event clock. |
| PERIOD_OF_PERFORMANCE_CURRENT_END_DATE | date as text (iso) | 2000-05-15 → 2035-12-31 | span_end | Current closing bound of the performance window; uncast TEXT passthrough. |
| PERIOD_OF_PERFORMANCE_START_DATE | date as text (iso) | 1977-01-17 → 2032-09-29 | span_start | Opening bound of the contract's performance window; uncast TEXT passthrough. |

### ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACTION_DATE | date (typed) | 2007-07-17 → 2026-07-04 | happened | try_to_date("action_date") in the mart; the day the contract transaction was executed, the real clock for all 20M rows — and unaffected by the fiscal-year bug that poisoned this table's census reading. |
| ACTION_DATE_FISCAL_YEAR | year only | 2007 → 2026 | unclear | THIS IS THE 20M-ROW EPOCH BUG: git shows the line was try_to_date("action_date_fiscal_year") until commit a650975e (2026-08-18) changed it to try_to_number, so the deployed column is a DATE holding 1970-01-01 for every row — the census's epoch1970 count of 20,000,000 is exactly the row count. It is a fiscal-year integer, never a date; the table needs a rebuild for the fix to land. |
| ORDERING_PERIOD_END_DATE | date (typed) | 1975-05-30 → 2035-12-31 | span_end | try_to_date(...); the last day orders can be placed against the vehicle — another period bound that legitimately sits in the future. |
| PERIOD_OF_PERFORMANCE_CURRENT_END_DATE | date (typed) | 1929-08-30 → 2035-12-31 | span_end | try_to_date(...); the currently-agreed closing bound, which moves with each contract modification. |
| PERIOD_OF_PERFORMANCE_POTENTIAL_END_DATE | date (typed) | 1988-06-30 → 2035-12-31 | span_end | try_to_date(...); the if-all-options-exercised closing bound, and the likeliest carrier of the 9999-12-31 ceiling and most of the 32,611 far-future rows the census counted. |
| PERIOD_OF_PERFORMANCE_START_DATE | date (typed) | 1940-09-29 → 2035-06-09 | span_start | try_to_date("period_of_performance_start_date"); opening bound of the contract's performance window. |
| SOLICITATION_DATE | date (typed) | 1966-06-29 → 2026-07-03 | reported | try_to_date("solicitation_date"); when the agency issued the solicitation publicly, before the award action — sparsely populated. |

### ECONOMICS.ECONOMICS__FED_USASPENDING_TOPTIER_AGENCIES
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACTIVE_FY | year only | 2026 → 2026 | not_a_date | Raw TEXT passthrough of ACTIVE_FY, the fiscal year the outlay and budget-authority figures on each of the 111 agency rows are current for; it is the only candidate, but it is almost certainly a single constant snapshot vintage, so it places this table on the timeline and cannot trend it — the previous census called this table clock-less for exactly that reason. |

### ECONOMICS.ECONOMICS__FED_US_SEC_EDGAR
| column | format | range | meaning | description |
|---|---|---|---|---|
| FILED_AT | date (typed) | 1995-05-19 → 2026-07-01 | reported | Staging does try_to_date(filed_at), so it is a DATE (time dropped): the day the filer submitted to EDGAR, populated on every filing, matching the census window 1995-05-19 to 2026-07-01. |
| FILED_YEAR | year only | 1995 → 2026 | reported | Literally year(filed_at) in the mart — a 4-digit year integer restating the filing clock at year grain. |
| PERIOD_OF_REPORT | date (typed) | 2001-12-31 → 2026-07-01 | span_end | Staging does try_to_date(period_of_report); it is the end of the period the filing covers, which is why it always sits earlier than filed_at. |

### ECONOMICS.ECONOMICS__FED_US_USASPENDING_API
| column | format | range | meaning | description |
|---|---|---|---|---|
| AWARD_DURATION_DAYS | year only | 1791 → 2008 | not_a_date | Literally datediff('day', start_date, end_date) in the mart — a duration in days, the same bug shape as days_received_to_company. |
| END_DATE | date (typed) | 2006-05-31 → 2035-12-31 | span_end | Period-of-performance closing bound, also used in the datediff; it carries the 2100-12-31 sentinel that produced all 13 far-future rows in the census. |
| LAST_MODIFIED_DATE | date (typed) | 2023-10-31 → 2026-06-29 | reported | USASpending's own record-maintenance stamp for when the award record was last changed in their system — publisher bookkeeping about the row, not about the world, so never a primary clock. |
| START_DATE | date (typed) | 1978-09-15 → 2024-09-27 | span_start | Period-of-performance opening bound, and the mart uses it in datediff('day', start_date, end_date), which proves it is a real DATE; chosen over the year-grain fiscal_year because it is finer and over last_modified_date because that one is record maintenance, not an event. |

### ECONOMICS.ECONOMICS__INTL_FAO_FAOSTAT
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATEUPDATE | date as text (iso) | 1991-12-31 → 2026-06-17 | reported | Raw TEXT passthrough of FAO's own DATEUPDATE on a 69-row dataset catalogue (one row per FAOSTAT dataset); it is when FAO last refreshed that dataset file, so it dates the publication, not any real-world event, and the string format is unverified with the warehouse down. |

### ECONOMICS.ECONOMICS__INTL_FAO_FAOSTAT_FOOD_SECURITY
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 2000 → 2025 | happened | try_to_number("YEAR") gives the year the indicator value describes; caveat worth checking on the rebuild — FAOSTAT food-security rows that carry a range label like '2000-2002' will silently become NULL under try_to_number. |
| YEAR_CODE | year only | 2000 → 2025 | not_a_date | Raw TEXT passthrough of FAOSTAT's Year Code, which for this food-security suite is often an 8-digit range code such as '20002002' for a three-year average rather than a plain year — an 8-digit bare date-parse is exactly the epoch/garbage trap, so treat it as a code, not a clock. |

### ECONOMICS.ECONOMICS__INTL_GLEIF
| column | format | range | meaning | description |
|---|---|---|---|---|
| ENTITY_HEADQUARTERSADDRESS_ADDITIONALADDRESSLINE_1 | year only | 1700 → 2033 | not_a_date | Passthrough of an extra HQ address line; a false hit from 'headQUARTERs'. |
| ENTITY_HEADQUARTERSADDRESS_ADDITIONALADDRESSLINE_2 | year only | 1703 → 2001 | not_a_date | Passthrough of an extra HQ address line; a false hit from 'headQUARTERs'. |
| ENTITY_HEADQUARTERSADDRESS_ADDRESSNUMBER | year only | 1700 → 2031 | not_a_date | Passthrough of the HQ street number; a false hit from 'headQUARTERs'. |
| ENTITY_HEADQUARTERSADDRESS_ADDRESSNUMBERWITHINBUILDING | year only | 2001-09-25 → 2012-02-13 | not_a_date | Passthrough of the HQ suite/unit number; a false hit from 'headQUARTERs'. |
| ENTITY_HEADQUARTERSADDRESS_CITY | year only | 2010 → 2019 | not_a_date | Passthrough of the HQ city name; a false hit from 'headQUARTERs'. |
| ENTITY_HEADQUARTERSADDRESS_FIRSTADDRESSLINE | year only | 1700 → 2015 | not_a_date | Passthrough of the HQ street address first line; a false hit from 'headQUARTERs'. |
| ENTITY_HEADQUARTERSADDRESS_MAILROUTING | year only | 1777 → 1969 | not_a_date | Passthrough of the HQ mail-routing line; a false hit from 'headQUARTERs'. |
| ENTITY_HEADQUARTERSADDRESS_POSTALCODE | month-year | 1700 → 2035 | not_a_date | Passthrough of the HQ postal code; a false hit from 'headQUARTERs'. |

### ECONOMICS.ECONOMICS__INTL_GLEIF_RELATIONSHIPS
| column | format | range | meaning | description |
|---|---|---|---|---|
| RELATIONSHIP_PERIOD_1_ENDDATE | date as text (iso) | 1925-06-23 → 2035-12-31 | span_end | Closing bound of period slot 1; same slot-is-not-a-type trap as the start date. |
| RELATIONSHIP_PERIOD_1_STARTDATE | date as text (iso) | 1832-02-18 → 2030-05-30 | span_start | Opening bound of period slot 1 on a parent/child relationship row and the best available anchor for when a corporate ownership link began. TRAP: the slots are a flattened repeating group, so slot 1 is not the same KIND of period on every row — you must filter relationship_period_1_periodtype = 'RELATIONSHIP_PERIOD' before reading it as the relationship start. |
| RELATIONSHIP_PERIOD_2_ENDDATE | date as text (iso) | 1852-01-01 → 2035-12-31 | span_end | Closing bound of period slot 2; meaning depends on its periodtype. |
| RELATIONSHIP_PERIOD_2_STARTDATE | date as text (iso) | 1824-01-01 → 2032-05-27 | span_start | Opening bound of period slot 2; meaning depends on relationship_period_2_periodtype. |
| RELATIONSHIP_PERIOD_3_ENDDATE | date as text (iso) | 2006-12-31 → 2035-12-31 | span_end | Closing bound of period slot 3; meaning depends on its periodtype. |
| RELATIONSHIP_PERIOD_3_STARTDATE | date as text (iso) | 1823-12-04 → 2028-12-10 | span_start | Opening bound of period slot 3; meaning depends on its periodtype. |

### ECONOMICS.ECONOMICS__INTL_IT_ISTAT
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE | date (typed) | 2020-01-01 → 2023-01-01 | happened | Staging builds it with a regex-guarded parse: 'YYYY' rows become Jan-1 of that year and 'YYYY-MM' rows become the 1st of that month, so it is the observation-period start. Month is the finest resolution present, but the staging comment records that 202,824 of 213,284 rows are ANNUAL and only 10,460 are monthly — check the FREQ column before trending at month grain. |
| OBS_YEAR | year only | 2020 → 2023 | happened | Literally year(date) in the mart — a 4-digit year integer restating the observation clock. |

### ECONOMICS.ECONOMICS__XC_OWID_GINI
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 1963 → 2025 | happened | try_to_number("YEAR") and the only time column; the year the Gini coefficient was measured for that country. |

### EDUCATION.EDUCATION__FED_CFTC_COT_FINANCIAL
| column | format | range | meaning | description |
|---|---|---|---|---|
| AS_OF_DATE_IN_FORM_YYMMDD | date (typed) | 2013-01-08 → 2026-08-04 | happened | try_to_date(AS_OF_DATE_IN_FORM_YYMMDD,'YYMMDD') - the COT as-of Tuesday when the reported positions were actually held; same date as the ISO twin but the 2-digit year pivots wrong outside 1970-2069. |
| REPORT_DATE_AS_YYYY_MM_DD | date (typed) | 2013-01-08 → 2026-08-04 | happened | try_to_date(REPORT_DATE_AS_YYYY_MM_DD) - the same COT as-of date in ISO form, a safer cast than the YYMMDD twin, and the day the open-interest positions existed. |

### EDUCATION.EDUCATION__FED_CFTC_COT_FUTURES
| column | format | range | meaning | description |
|---|---|---|---|---|
| AS_OF_DATE_IN_FORM_YYMMDD | date (typed) | 1986-01-15 → 2026-08-04 | happened | try_to_date(...,'YYMMDD') of the COT as-of Tuesday; duplicate of the ISO column with 2-digit-year century risk on this 1986-start file. |
| AS_OF_DATE_IN_FORM_YYYY_MM_DD | date (typed) | 1986-01-15 → 2026-08-04 | happened | try_to_date on the ISO-formatted COT as-of date - when the reported futures positions were held; census range 1986-2026 matches the real COT history. |

### EDUCATION.EDUCATION__FED_ED_COLLEGE_SCORECARD_INSTITUTION
| column | format | range | meaning | description |
|---|---|---|---|---|
| AVG_FACULTY_SALARY_MONTHLY | year only | 1757 → 2032 | not_a_date | try_to_number(trim(AVGFACSAL)) — average monthly faculty salary in dollars; matched only on 'monthly'. |
| COST_OF_ATTENDANCE_ACADEMIC_YEAR | quarter | 1700 → 2035 | not_a_date | try_to_number(trim(COSTT4_A)) — a dollar cost of attendance for academic-year programs; matched only on the word 'year'. |
| COST_OF_ATTENDANCE_PROGRAM_YEAR | quarter | 1706 → 2033 | not_a_date | try_to_number(trim(COSTT4_P)) — a dollar cost of attendance for program-year schools. |
| TUITION_PROGRAM_YEAR | year only | 1709 → 2029 | not_a_date | try_to_number(trim(TUITIONFEE_PROG)) — a tuition dollar figure. |

### EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND
| column | format | range | meaning | description |
|---|---|---|---|---|
| WEEK_START_DATE | date (typed) | 2018-05-27 → 2026-08-02 | span_start | try_to_date(WEEK_START_DATE) in the mart; it is the Monday that opens each weekly spend bucket, so it is a real date whose underlying fact covers a week. |

### EDUCATION.EDUCATION__FED_GOOGLE_POLADS_CREATIVE_STATS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_RANGE_END | date (typed) | 2019-08-05 → 2026-08-05 | span_end | try_to_date(DATE_RANGE_END) — the last day of the same reported stats window. |
| DATE_RANGE_START | date (typed) | 2018-05-31 → 2026-08-04 | span_start | try_to_date(DATE_RANGE_START) — the reported first day of the window this ad's stats cover; the only properly typed DATE on the table. |
| FIRST_SERVED_TIMESTAMP | date as text (iso) | 2018-05-31 → 2026-08-04 | span_start | Pass-through with no cast at all, so its stored type is whatever landed; by name it is when the creative first actually served, i.e. the real start of the serving window. |
| LAST_SERVED_TIMESTAMP | date as text (iso) | 2019-08-05 → 2026-08-05 | span_end | Pass-through with no cast; by name it closes the actual serving window of the creative. |
| NUM_OF_DAYS | year only | 1725 → 1861 | not_a_date | try_to_number(NUM_OF_DAYS) — a duration count in days, the same bug class as days_received_to_company; never parse as a date. |

### EDUCATION.EDUCATION__FED_SENATE_LDA_FILINGS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DT_POSTED | date as text (iso) | 2020-01-02 → 2026-07-24 | reported | When the Senate posted the filing to the public LDA database — the classic reported clock; note the mart applies no cast, so its stored type is whatever landed, and the census's 2020-2021 range cannot have come from it. |
| FILING_YEAR | year only | 2020 → 2021 | span_start | Uncast pass-through of FILING_YEAR — a bare calendar year naming the year the lobbying report covers; real year, but a bare date-parse of '2020' is exactly the epoch-1970 collapse bug. |
| TERMINATION_DATE | date (typed) | 2020-01-01 → 2021-12-31 | span_end | try_to_date(TERMINATION_DATE) — closes the registrant/client lobbying engagement; the only DATE-typed column here, so the census's 2020-01-01..2021-12-31 range describes this column, not the file's coverage. |

### ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR
| column | format | range | meaning | description |
|---|---|---|---|---|
| OPERATING_YEAR | year only | 1891 → 2024 | happened | try_to_number() year; schema.yml documents it as the year the generator began operation - the real in-service event and the only broadly-populated clock on the table. |
| PLANNED_DERATE_YEAR | year only | 2025 → 2026 | happened | try_to_number() year of a scheduled future capacity derate - a forward-dated plan, not an occurred event. |
| PLANNED_RETIREMENT_YEAR | year only | 2025 → 2035 | span_end | try_to_number() year; schema.yml 'Planned retirement year, if reported' - the forward-looking end of the generator's service span, so for live units it lands in the future. |
| PLANNED_UPRATE_YEAR | year only | 2024 → 2035 | happened | try_to_number() year of a scheduled future capacity uprate - a real-world event clock but forward-dated, so it sits to the right of today on a timeline. |
| YEAR_UPRATE_OR_DERATE_COMPLETED | year only | 2024 → 2024 | happened | try_to_number() year integer - the year the uprate/derate was completed, a real-world change to the generator. It is a NUMBER, not a date; never bare-date-parse it. |

### ENERGY.ENERGY__FED_EIA860_3_2_WIND
| column | format | range | meaning | description |
|---|---|---|---|---|
| OPERATING_YEAR | year only | 1981 → 2024 | happened | try_to_number(trim(OPERATING_YEAR)) - the year the wind generator entered commercial service; the only clock on this 2024-snapshot table. |

### ENERGY.ENERGY__FED_EIA860_3_3_SOLAR
| column | format | range | meaning | description |
|---|---|---|---|---|
| OPERATING_YEAR | year only | 2001 → 2024 | happened | try_to_number(trim(OPERATING_YEAR)) - the year the solar generator entered commercial service; the only clock on this 2024-snapshot table. |

### ENERGY.ENERGY__FED_EIA860_3_4_ENERGY_STORAGE
| column | format | range | meaning | description |
|---|---|---|---|---|
| OPERATING_YEAR | year only | 1991 → 2024 | happened | try_to_number(trim(OPERATING_YEAR)) - the year the battery/storage unit entered commercial service; the only clock on this 2024-snapshot table. |

### ENERGY.ENERGY__FED_EIA860_3_5_MULTIFUEL
| column | format | range | meaning | description |
|---|---|---|---|---|
| OPERATING_YEAR | year only | 1915 → 2024 | happened | try_to_number(trim(OPERATING_YEAR)) - the year the generator entered commercial service; the only real clock on this 2024-snapshot table. |

### ENERGY.ENERGY__FED_EIA860_6_2_ENVIROEQUIP
| column | format | range | meaning | description |
|---|---|---|---|---|
| COMPLIANCE_YEAR_MERCURY | year only | 1960 → 2034 | span_start | try_to_number() year the boiler is expected to comply with the mercury standard - start of a compliance period; values unverified. |
| COMPLIANCE_YEAR_NITROGEN | year only | 1949 → 2027 | span_start | try_to_number() year the boiler is expected to comply with the NOx standard - start of a compliance period, forward-looking; values unverified. |
| COMPLIANCE_YEAR_PARTICULATE | year only | 1934 → 2025 | span_start | try_to_number() year the boiler is expected to comply with the particulate standard - start of a compliance period; values unverified. |
| COMPLIANCE_YEAR_SULFUR | year only | 1949 → 2027 | span_start | try_to_number() year; EIA documents this as the year the boiler is expected to be in compliance with the SO2 standard - the opening of a compliance period, not an event that occurred. Values not verified (warehouse down). |
| NEW_SOURCE_REVIEW_YEAR | year only | 1974 → 2026 | decided | try_to_number() year the New Source Review permit was issued - an authority acting on the boiler. Best real clock here, but sparse: only boilers that went through NSR carry it. |

### ENERGY.ENERGY__FED_EIA861_ADVANCED_METERS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_YEAR | year only | 2024 → 2024 | happened | try_to_number(nullif(trim(DATA_YEAR),'.')) - a plain NUMBER year (2024), the survey year the meter counts describe. Year grain, and it is a number not a date: bare-date-parsing it is what produced this batch's junk census ranges. |

### ENERGY.ENERGY__FED_EIA861_DELIVERY_COMPANIES
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_YEAR | year only | 2024 → 2024 | happened | try_to_number(nullif(trim(UNNAMED_0),'.')) - a NUMBER year recovered positionally after the loader ate the Excel header; per the model it is the 2024 reporting year the revenue/sales describe. |

### ENERGY.ENERGY__FED_EIA861_DEMAND_RESPONSE
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_YEAR | year only | 2024 → 2024 | happened | try_to_number(nullif(trim(UNNAMED_0),'.')) - NUMBER year recovered positionally from a header-damaged load; the 2024 program year the demand-response savings occurred in. |

### ENERGY.ENERGY__FED_EIA861_DISTRIBUTION_SYSTEMS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_YEAR | year only | 2024 → 2024 | happened | try_to_number(nullif(trim(C_2024),'.')) - the loader consumed the header row so the source column is literally named C_2024; it holds the reporting year the circuit counts describe. |

### ENERGY.ENERGY__FED_EIA861_DYNAMIC_PRICING
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_YEAR | year only | 2024 → 2024 | happened | try_to_number(nullif(trim(UNNAMED_0),'.')) - NUMBER year recovered positionally; the 2024 program year the enrollment counts describe. Only clock on the table. |

### ENERGY.ENERGY__FED_EIA861_ENERGY_EFFICIENCY
| column | format | range | meaning | description |
|---|---|---|---|---|
| COMMERCIAL_LIFE_CYCLE_ENERGY_SAVINGS_MWH | year only | 1736 → 2008 | not_a_date | try_to_number() of an MWh quantity, not a date. |
| DATA_YEAR | year only | 2024 → 2024 | happened | try_to_number(nullif(trim(UNNAMED_0),'.')) - NUMBER year recovered positionally; the 2024 program year the efficiency savings occurred in. Only clock on the table. |
| INDUSTRIAL_LIFE_CYCLE_ENERGY_SAVINGS_MWH | year only | 1730 → 1911 | not_a_date | try_to_number() of an MWh quantity, not a date. |
| RESIDENTIAL_LIFE_CYCLE_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS | year only | 1704 → 2033 | not_a_date | try_to_number(trim(CUSTOMER_INCENTIVES_THOUSAND_DOLLARS_1)) - a dollar amount, not a date. |
| RESIDENTIAL_LIFE_CYCLE_ENERGY_SAVINGS_MWH | year only | 1709 → 2028 | not_a_date | try_to_number() of an MWh quantity - energy saved over the measure's life; 'life_cycle' names the accounting basis, not a time. |
| TOTAL_LIFE_CYCLE_ENERGY_SAVINGS_MWH | year only | 1750 → 2017 | not_a_date | try_to_number() of an MWh quantity, not a date. |

### ENERGY.ENERGY__FED_EIA861_FRAME
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_YEAR | year only | 2024 → 2024 | happened | try_to_number(nullif(trim(C_2024),'.')) - the header row was consumed at load so the source column is literally named C_2024; it carries the reporting year of the respondent frame. |

### ENERGY.ENERGY__FED_EIA861_MERGERS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_YEAR | year only | 2024 → 2024 | happened | try_to_number(nullif(trim(C_2024),'.')) - the survey reporting year, a NUMBER not a date; coarser than effective_date on the same row. |
| EFFECTIVE_DATE | date (typed) | 2024-01-01 → 2024-11-20 | happened | try_to_date(trim(C_03_01_2024),'MM/DD/YYYY') - the day the utility merger/acquisition took legal effect; a real corporate event at day grain, and the only true date in the whole EIA-861 family. |

### ENERGY.ENERGY__FED_EIA861_NET_METERING
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_YEAR | year only | 2024 → 2024 | happened | try_to_number(nullif(trim(UNNAMED_0),'.')) - NUMBER year recovered positionally; the 2024 reporting year the net-metering capacity describes. |

### ENERGY.ENERGY__FED_EIA861_NON_NET_METERING_DISTRIBUTED
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_YEAR | year only | 2024 → 2024 | happened | try_to_number(nullif(trim(YEAR),'.')) - a NUMBER year (2024) naming the reporting year of the distributed-capacity figures. |

### ENERGY.ENERGY__FED_EIA861_OPERATIONAL_DATA
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_YEAR | year only | 2024 → 2024 | happened | try_to_number(nullif(trim(UNNAMED_0),'.')) - NUMBER year recovered positionally; the 2024 year the peak demand and energy flows occurred in. |
| EXCHANGE_ENERGY_RECEIVED_MWH | month-year | 1727 → 2011 | not_a_date | try_to_number(trim(POWER_EXCHANGED)) - an MWh energy quantity; 'received' names a direction of flow, not a receipt date. |
| WHEELED_POWER_RECEIVED_MWH | month-year | 1872 → 2024 | not_a_date | try_to_number(trim(WHEELED_POWER)) - an MWh energy quantity, not a receipt date. |

### ENERGY.ENERGY__FED_EIA861_RELIABILITY
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_YEAR | year only | 2024 → 2024 | happened | try_to_number(nullif(trim(UNNAMED_0),'.')) - NUMBER year recovered positionally; the 2024 year the SAIDI/SAIFI outage metrics were measured over. |

### ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_YEAR | year only | 2024 → 2024 | happened | try_to_number(nullif(trim(UNNAMED_0),'.')) - NUMBER year recovered positionally; the 2024 year the sales and revenue occurred in. |

### ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST_CS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_YEAR | year only | 2024 → 2024 | happened | try_to_number(nullif(trim(UNNAMED_0),'.')) - NUMBER year recovered positionally; the 2024 year the customer-sited sales occurred in. |

### ENERGY.ENERGY__FED_EIA861_SERVICE_TERRITORY
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_YEAR | year only | 2024 → 2024 | happened | try_to_number(nullif(trim(C_2024),'.')) - header row consumed at load so the column is named C_2024; it carries the year this county-service footprint was reported for. |

### ENERGY.ENERGY__FED_EIA861_SHORT_FORM
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_YEAR | year only | 2024 → 2024 | happened | try_to_number(nullif(trim(C_2024),'.')) - header row consumed at load; the reporting year the short-form revenue/sales describe. |

### ENERGY.ENERGY__FED_EIA861_UTILITY_DATA
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_YEAR | year only | 2024 → 2024 | happened | try_to_number(nullif(trim(DATA_YEAR),'.')) - a clean NUMBER year (2024) naming the year this utility profile describes. |

### ENERGY.ENERGY__FED_EIA_861_BALANCING_AUTHORITY
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_YEAR | year only | 2024 → 2024 | unclear | try_to_number(trim(DATA_YEAR)) - a plain NUMBER year (2024). The census's recorded range of year 56,602,308 on all 189 rows is proof the old scan date-parsed a number: this column is a year, never a timestamp. |

### ENERGY.ENERGY__INTL_EMBER_ELEC
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE | date (typed) | 2000-01-01 → 2025-01-01 | happened | Staging casts try_to_date(trim(DATE),'YYYY'), so every value is a bare year snapped to Jan-1; real resolution is YEAR not day, and the census range 2000-01-01..2025-01-01 confirms it. |
| YEAR | year only | 2000 → 2025 | happened | The mart computes year(date) - a derived duplicate of the same clock, so it adds nothing beyond `date`. |

### ENVIRONMENT.ENVIRONMENT__EPA_PENALTY_GAP
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_LAST_FORMAL_ACTION | date (typed) | 1903-12-01 → 2026-06-18 | decided | try_to_date of ECHO FAC_DATE_LAST_FORMAL_ACTION: the day a regulator took its most recent formal enforcement action. |
| DATE_LAST_INSPECTION | date (typed) | 1978-08-25 → 2026-06-18 | happened | try_to_date of ECHO FAC_DATE_LAST_INSPECTION: the day the most recent inspection actually took place at the facility. |
| PENALTY_PER_QUARTER_NC | year only | 1700 → 2028 | not_a_date | Derived in the mart as round(total_penalties / quarters_with_noncompliance, 2): dollars per quarter, a rate, not a date. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| REPORTING_YEAR | year only | 2008 → 2024 | happened | Raw passthrough of REPORTING_YEAR (no cast): the inventory year the emissions occurred in. Integer year - date-parsing it is the epoch-1970 trap. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_AQS_SITES
| column | format | range | meaning | description |
|---|---|---|---|---|
| EXTRACTION_DATE | date (typed) | 2026-06-26 → 2026-06-26 | ingest | try_to_date(EXTRACTION_DATE,'YYYY-MM-DD') - the date EPA cut the AQS file we downloaded; file vintage, not a site event. Never use as an event clock. |
| SITE_CLOSED_DATE | date (typed) | 1957-12-31 → 2026-03-27 | span_end | try_to_date(SITE_CLOSED_DATE,'YYYY-MM-DD') - the close of the site's operating tenure; null for still-open sites. |
| SITE_ESTABLISHED_DATE | date (typed) | 1957-01-01 → 2026-12-01 | span_start | Staging casts try_to_date(SITE_ESTABLISHED_DATE,'YYYY-MM-DD'); with site_closed_date it bounds the monitoring site's operating tenure, so it is the span start and the best row anchor. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_LAST_FORMAL_ACTION | date (typed) | 1900-01-01 → 2026-06-18 | decided | try_to_date(FAC_DATE_LAST_FORMAL_ACTION): the day an authority last took formal enforcement action. |
| DATE_LAST_INSPECTION | date (typed) | 1908-07-09 → 2026-06-19 | happened | try_to_date(FAC_DATE_LAST_INSPECTION): the day the facility's most recent inspection occurred; the best whole-table anchor for a facility row. |
| DATE_LAST_PENALTY | date (typed) | 1900-01-01 → 2026-06-18 | decided | try_to_date(FAC_DATE_LAST_PENALTY): the day a penalty was last assessed by the regulator. |
| DAYS_SINCE_LAST_INSPECTION | year only | 1700 → 2035 | not_a_date | try_to_number(FAC_DAYS_LAST_INSPECTION): a DURATION in days, the exact class of column that has corrupted date censuses before. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_YEAR | year only | 2022 → 2022 | happened | Raw passthrough of DATA_YEAR (no cast) in a 2022-vintage eGRID extract: the calendar year the generation and emissions figures describe. Integer year, not a date. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_GHGRP_EMISSION
| column | format | range | meaning | description |
|---|---|---|---|---|
| REPORTING_YEAR | year only | 2010 → 2023 | happened | Staging casts try_to_number(trim(YEAR)) and renames it reporting_year: the calendar year the emissions were emitted and reported for, 2010+. Integer year. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_GHGRP_FACILITY
| column | format | range | meaning | description |
|---|---|---|---|---|
| REPORTING_YEAR | year only | 2010 → 2023 | happened | try_to_number(trim(YEAR)): the GHGRP reporting year this facility row describes; facility_id + year is the declared grain. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| SETTLEMENT_ENTERED_DATE | date (typed) | 1972-10-25 → 2026-07-30 | decided | try_to_date(SETTLEMENT_ENTERED_DATE): the day the authority entered the settlement on a formal Clean Air Act enforcement action. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACHIEVED_DATE | date (typed) | 1900-01-01 → 2027-11-07 | decided | try_to_date(ACHIEVED_DATE): the day the informal enforcement action was issued/achieved by the agency. Census max 8888-01-01 with 5 far-future rows = publisher sentinel values, and min 0001-01-01 is try_to_date junk. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS
| column | format | range | meaning | description |
|---|---|---|---|---|
| BEGIN_DATE | date (typed) | 1940-01-03 → 2028-10-29 | span_start | try_to_date(BEGIN_DATE): the day the facility's air-program coverage/operating status began - the start of a coverage period, and the only real-world clock here. |
| UPDATED_DATE | date (typed) | 2014-10-19 → 2026-07-31 | reported | try_to_date(UPDATED_DATE): when the ICIS-Air program record was last maintained in EPA's system. Record housekeeping - census max 2028-10-29 and 109 epoch-1970 rows show it also carries junk. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_STACK_TESTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACTUAL_END_DATE | date (typed) | 1955-03-15 → 2026-07-29 | happened | try_to_date(ACTUAL_END_DATE): the day the stack test was performed/completed. Census min 0201-07-24 plus 1 epoch-1970 row = try_to_date passing malformed source strings. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_TITLEV_CERTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACTUAL_END_DATE | date (typed) | 1916-02-25 → 2026-07-30 | reported | try_to_date(ACTUAL_END_DATE), the only clock: the completion/receipt date of a Title V annual compliance certification the facility submits to the regulator. LOW - the compiled SQL proves the cast but not whether EPA means 'received' or 'period end'. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_CS_VIOLATIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACTUAL_DATE | date (typed) | 1977-02-25 → 2026-07-31 | happened | try_to_date(ACTUAL_DATE): the day the scheduled compliance event actually occurred; the violation is the gap between this and schedule_date. |
| REPORT_RECEIVED_DATE | date (typed) | 1977-02-25 → 2026-07-31 | reported | try_to_date(REPORT_RECEIVED_DATE): the day the permittee's report reached the agency - textbook reporting clock. |
| RNC_DETECTION_DATE | date (typed) | 1973-12-08 → 2026-07-31 | decided | try_to_date(RNC_DETECTION_DATE): the day the agency's system flagged reportable noncompliance - an authority determination, not the underlying discharge. |
| RNC_RESOLUTION_DATE | date (typed) | 1977-11-18 → 2026-07-31 | decided | try_to_date(RNC_RESOLUTION_DATE): the day the agency recorded the reportable noncompliance as resolved. |
| SCHEDULE_DATE | date (typed) | 1973-09-09 → 2026-07-30 | span_end | try_to_date(SCHEDULE_DATE): the DEADLINE the compliance schedule set for that milestone - the end of the window the permittee was given, not something that happened. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| SETTLEMENT_ENTERED_DATE | date (typed) | 1970-09-07 → 2026-07-30 | decided | try_to_date(SETTLEMENT_ENTERED_DATE): the day the authority entered the settlement on a Clean Water Act formal enforcement action. Census min 1970-09-07 with 1 epoch-1970 row - one junk row, not a systemic collapse. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACHIEVED_DATE | date (typed) | 1969-01-12 → 2029-06-24 | decided | try_to_date(ACHIEVED_DATE): the day the informal enforcement action was achieved by the agency. Census 0001-01-01 to 8202-06-10 with 3 far-future rows = source sentinels/typos surviving try_to_date. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACTUAL_BEGIN_DATE | date (typed) | 1917-09-13 → 2026-07-31 | span_start | try_to_date(ACTUAL_BEGIN_DATE): the day the inspection started; paired with actual_end_date it bounds the inspection, and it is the best anchor for the row. |
| ACTUAL_END_DATE | date (typed) | 1917-09-13 → 2026-07-31 | span_end | try_to_date(ACTUAL_END_DATE): the day the inspection finished. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_PS_VIOLATIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACTUAL_DATE | date (typed) | 1974-05-06 → 2026-07-29 | happened | try_to_date(ACTUAL_DATE): the day the permit-schedule milestone actually happened - the real-world clock on this table. |
| REPORT_RECEIVED_DATE | date (typed) | 1974-05-06 → 2026-07-29 | reported | try_to_date(REPORT_RECEIVED_DATE): the day the permittee's report reached the agency. |
| RNC_DETECTION_DATE | date (typed) | 1974-06-28 → 2026-07-31 | decided | try_to_date(RNC_DETECTION_DATE): the day the agency flagged reportable noncompliance. |
| RNC_RESOLUTION_DATE | date (typed) | 1974-07-01 → 2026-07-31 | decided | try_to_date(RNC_RESOLUTION_DATE): the day the agency recorded the noncompliance as resolved. |
| SCHEDULE_DATE | date (typed) | 1974-03-30 → 2026-07-28 | span_end | try_to_date(SCHEDULE_DATE): the permit schedule's DEADLINE for that milestone - the end of the allowed window. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEARQTR | quarter | 1973 → 2033 | happened | Raw passthrough of YEARQTR (no cast) on a quarterly-noncompliance-report history table: a YYYYQ-style year+quarter code naming the quarter the status applied to. Quarter grain - date-parsing it is the collapse-to-1970 trap. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_SE_VIOLATIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| RNC_DETECTION_DATE | date (typed) | 1979-05-01 → 2026-07-31 | decided | try_to_date(RNC_DETECTION_DATE): the day the agency flagged reportable noncompliance. |
| RNC_RESOLUTION_DATE | date (typed) | 1984-08-10 → 2026-07-31 | decided | try_to_date(RNC_RESOLUTION_DATE): the day the agency recorded the noncompliance as resolved. |
| SINGLE_EVENT_END_DATE | date (typed) | 1976-07-01 → 2026-07-31 | span_end | try_to_date(SINGLE_EVENT_END_DATE): the close of a violation that ran longer than a day. |
| SINGLE_EVENT_VIOLATION_DATE | date (typed) | 1976-07-01 → 2026-07-30 | happened | try_to_date(SINGLE_EVENT_VIOLATION_DATE): the day the single-event violation occurred - the cleanest 'happened' clock in the NPDES family. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_ENFORCEMENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ENFORCEMENT_ACTION_DATE | date (typed) | 1887-03-13 → 2026-07-31 | decided | Staging casts try_to_date(trim(ENFORCEMENT_ACTION_DATE)) and it is part of the record key: the day the hazardous-waste enforcement action was taken. Census min 0999-02-04 = try_to_date junk, not a real 10th-century row. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_EVALUATIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| EVALUATION_START_DATE | date (typed) | 1901-05-29 → 2026-07-31 | happened | try_to_date(trim(EVALUATION_START_DATE)) - the day the RCRA compliance evaluation (inspection) was conducted. No end column exists, so it is the event date, not half a span. Census min 0005-05-17 = parse junk. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_VIOLATIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACTUAL_RTC_DATE | date (typed) | 1900-01-10 → 2026-07-31 | happened | try_to_date(trim(ACTUAL_RTC_DATE)): the day the facility actually returned to compliance - a real-world fix, but only present once the violation closes. |
| DATE_VIOLATION_DETERMINED | date (typed) | 1901-02-12 → 2026-07-24 | decided | try_to_date(trim(DATE_VIOLATION_DETERMINED)): the day the agency determined the violation. Chosen as primary over actual_rtc_date because it is part of the record key and populated on every row, while RTC exists only for closed violations. |
| SCHEDULED_COMPLIANCE_DATE | date (typed) | 1919-06-20 → 2033-03-05 | span_end | try_to_date(trim(SCHEDULED_COMPLIANCE_DATE)): the DEADLINE the facility was given, so it closes an allowed window rather than recording an event. The census's 78 far-future rows and 9999-04-26 max are exactly the sentinel deadlines you would expect here. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_VIOSNC_HISTORY
| column | format | range | meaning | description |
|---|---|---|---|---|
| YRMONTH | month-year | 1980 → 2026 | happened | trim(YRMONTH) kept as text: the YYYYMM month whose violation / significant-noncompliance status the row reports. Month grain - do not date-parse. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_EVENTS_MILESTONES
| column | format | range | meaning | description |
|---|---|---|---|---|
| EVENT_ACTUAL_DATE | date (typed) | 1991-07-01 → 2032-12-31 | happened | try_to_date(EVENT_ACTUAL_DATE): the day the milestone was actually achieved - the real-world clock on this table. |
| EVENT_END_DATE | date (typed) | 1993-09-27 → 2028-03-25 | span_end | try_to_date(EVENT_END_DATE): the scheduled close of the milestone window. The census's 2099-06-30 max and 2 far-future rows are sentinel deadlines, which is what you expect from a target date rather than an actual. |
| FIRST_REPORTED_DATE | date (typed) | 2000-12-08 → 2026-07-01 | reported | try_to_date(FIRST_REPORTED_DATE): the day the row first appeared in a state submission to SDWIS. |
| LAST_REPORTED_DATE | date (typed) | 2000-12-08 → 2026-07-01 | reported | try_to_date(LAST_REPORTED_DATE): the day the row was most recently re-submitted to SDWIS - record maintenance. |
| SUBMISSIONYEARQUARTER | quarter | 2026 → 2026 | reported | Raw passthrough of SUBMISSIONYEARQUARTER (no cast): the YYYYQn SDWIS federal-reporting cycle in which the state submitted this row. A submission label, not an event - quarter grain, never date-parse it. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES
| column | format | range | meaning | description |
|---|---|---|---|---|
| FACILITY_DEACTIVATION_DATE | date (typed) | 1900-02-01 → 2027-10-31 | happened | try_to_date(FACILITY_DEACTIVATION_DATE): the day the water-system facility went out of service. Real-world, but only populated for deactivated facilities, so it cannot anchor the table. |
| FIRST_REPORTED_DATE | date (typed) | 2005-10-27 → 2026-06-30 | reported | try_to_date(FIRST_REPORTED_DATE): the day the facility first appeared in a state SDWIS submission. Made primary over the 'happened' deactivation date because it is the only clock present on every row of a registry table. |
| LAST_REPORTED_DATE | date (typed) | 1995-07-22 → 2026-06-30 | reported | try_to_date(LAST_REPORTED_DATE): most recent re-submission of the facility record. |
| SUBMISSIONYEARQUARTER | quarter | 2026 → 2026 | reported | Raw passthrough of SUBMISSIONYEARQUARTER (no cast): the YYYYQn SDWIS federal-reporting cycle in which the state submitted this row. A submission label, not an event - quarter grain, never date-parse it. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS
| column | format | range | meaning | description |
|---|---|---|---|---|
| LAST_REPORTED_DATE | date (typed) | 1995-07-22 → 2026-06-30 | reported | try_to_date(LAST_REPORTED_DATE), the only date cast on the table: when the state last submitted this water-system-to-place link. A lookup table with no event of its own. |
| SUBMISSIONYEARQUARTER | quarter | 2026 → 2026 | reported | Raw passthrough of SUBMISSIONYEARQUARTER (no cast): the YYYYQn SDWIS federal-reporting cycle in which the state submitted this row. A submission label, not an event - quarter grain, never date-parse it. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_LCR_SAMPLES
| column | format | range | meaning | description |
|---|---|---|---|---|
| SAMPLE_FIRST_REPORTED_DATE | date (typed) | 1992-08-22 → 2026-06-30 | reported | try_to_date(SAMPLE_FIRST_REPORTED_DATE): first state submission of the sample record. |
| SAMPLE_LAST_REPORTED_DATE | date (typed) | 1993-05-20 → 2026-06-30 | reported | try_to_date(SAMPLE_LAST_REPORTED_DATE): most recent re-submission of the sample record. |
| SAMPLING_END_DATE | date (typed) | 1992-01-01 → 2033-12-31 | span_end | try_to_date(SAMPLING_END_DATE): the close of the lead-and-copper monitoring period the sample belongs to. |
| SAMPLING_START_DATE | date (typed) | 1991-07-01 → 2026-01-01 | span_start | try_to_date(SAMPLING_START_DATE): the start of the monitoring period the water was actually sampled in. Primary over the four reported dates because it is the only clock tied to the water, not to SDWIS paperwork. |
| SAR_FIRST_REPORTED_DATE | date (typed) | 2006-02-28 → 2026-06-30 | reported | try_to_date(SAR_FIRST_REPORTED_DATE): first submission of the associated sample-analytical-result (SAR) record. |
| SAR_LAST_REPORTED_DATE | date (typed) | 2006-02-28 → 2026-06-30 | reported | try_to_date(SAR_LAST_REPORTED_DATE): most recent submission of the sample-analytical-result record. |
| SUBMISSIONYEARQUARTER | quarter | 2026 → 2026 | reported | Raw passthrough of SUBMISSIONYEARQUARTER (no cast): the YYYYQn SDWIS federal-reporting cycle in which the state submitted this row. A submission label, not an event - quarter grain, never date-parse it. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PN_VIOLATION_ASSOC
| column | format | range | meaning | description |
|---|---|---|---|---|
| COMPL_PER_BEGIN_DATE | date (typed) | 1992-06-30 → 2026-05-10 | span_start | try_to_date(COMPL_PER_BEGIN_DATE): the start of the compliance period the violation is scored against - the SDWIS field ECHO surfaces as the violation start, and the only clock populated on essentially every row. |
| COMPL_PER_END_DATE | date (typed) | 1992-09-30 → 2026-06-30 | span_end | try_to_date(COMPL_PER_END_DATE): the close of that compliance period. |
| FIRST_REPORTED_DATE | date (typed) | 2002-02-16 → 2026-07-01 | reported | try_to_date(FIRST_REPORTED_DATE): first state submission of this public-notice-to-violation link. |
| LAST_REPORTED_DATE | date (typed) | 2002-02-16 → 2026-07-01 | reported | try_to_date(LAST_REPORTED_DATE): most recent re-submission of the link. |
| NON_COMPL_PER_BEGIN_DATE | date (typed) | 1992-06-30 → 2026-05-10 | span_start | try_to_date(NON_COMPL_PER_BEGIN_DATE): the start of the actual noncompliance window - closer to the harm than the compliance period, but sparser. |
| NON_COMPL_PER_END_DATE | date (typed) | 1950-01-01 → 2026-06-22 | span_end | try_to_date(NON_COMPL_PER_END_DATE): the close of the noncompliance window. |
| SUBMISSIONYEARQUARTER | quarter | 2026 → 2026 | reported | Raw passthrough of SUBMISSIONYEARQUARTER (no cast): the YYYYQn SDWIS federal-reporting cycle in which the state submitted this row. A submission label, not an event - quarter grain, never date-parse it. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS
| column | format | range | meaning | description |
|---|---|---|---|---|
| FIRST_REPORTED_DATE | date (typed) | 1979-02-10 → 2026-06-30 | reported | try_to_date(FIRST_REPORTED_DATE): the day the water system first appeared in a state SDWIS submission. Primary because it is the only clock covering every row of this registry. |
| LAST_REPORTED_DATE | date (typed) | 1995-07-22 → 2026-06-30 | reported | try_to_date(LAST_REPORTED_DATE): most recent re-submission of the system record. |
| OUTSTANDING_PERFORM_BEGIN_DATE | date (typed) | 1987-01-01 → 2026-12-04 | span_start | try_to_date(OUTSTANDING_PERFORM_BEGIN_DATE): the day the system's 'outstanding performer' designation began. |
| PWS_DEACTIVATION_DATE | date (typed) | 1900-02-01 → 2026-06-30 | happened | try_to_date(PWS_DEACTIVATION_DATE): the day the public water system stopped operating. Real-world, but only present for deactivated systems. |
| REDUCED_MONITORING_BEGIN_DATE | date (typed) | 1980-01-01 → 2026-06-09 | span_start | try_to_date(REDUCED_MONITORING_BEGIN_DATE): the day reduced RTCR monitoring started for this system. |
| REDUCED_MONITORING_END_DATE | date (typed) | 2016-04-01 → 2026-06-30 | span_end | try_to_date(REDUCED_MONITORING_END_DATE): the day reduced monitoring ended. The census's 2031-05-29 max is a forward-dated end, which is normal for an open window. |
| SOURCE_PROTECTION_BEGIN_DATE | date (typed) | 1986-12-31 → 2031-05-29 | span_start | try_to_date(SOURCE_PROTECTION_BEGIN_DATE): the day the system's source-water-protection status began - opens a status period. |
| SUBMISSIONYEARQUARTER | quarter | 2026 → 2026 | reported | Raw passthrough of SUBMISSIONYEARQUARTER (no cast): the YYYYQn SDWIS federal-reporting cycle in which the state submitted this row. A submission label, not an event - quarter grain, never date-parse it. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_SITE_VISITS
| column | format | range | meaning | description |
|---|---|---|---|---|
| FIRST_REPORTED_DATE | date (typed) | 1995-07-22 → 2026-07-01 | reported | try_to_date(FIRST_REPORTED_DATE): first state submission of the visit record. |
| LAST_REPORTED_DATE | date (typed) | 2005-11-15 → 2026-07-01 | reported | try_to_date(LAST_REPORTED_DATE): most recent re-submission of the visit record. |
| SUBMISSIONYEARQUARTER | quarter | 2026 → 2026 | reported | Raw passthrough of SUBMISSIONYEARQUARTER (no cast): the YYYYQn SDWIS federal-reporting cycle in which the state submitted this row. A submission label, not an event - quarter grain, never date-parse it. |
| VISIT_DATE | date (typed) | 1900-01-01 → 2026-06-24 | happened | try_to_date(VISIT_DATE): the day the sanitary survey / site visit actually took place. Census min 1900-01-01 with 32 epoch-1970 rows = a small pocket of junk, not a broken column. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
| column | format | range | meaning | description |
|---|---|---|---|---|
| CALCULATED_RTC_DATE | date (typed) | 1900-01-31 → 2026-06-29 | decided | try_to_date(CALCULATED_RTC_DATE): the return-to-compliance date EPA calculates for the violation - an authority-derived determination, not a raw observation. |
| COMPL_PER_BEGIN_DATE | date (typed) | 1900-01-01 → 2026-06-09 | span_start | try_to_date(COMPL_PER_BEGIN_DATE): the start of the compliance period the drinking-water violation is scored against - the field ECHO treats as the violation start, and the broadest-coverage clock on a 15.4M-row mixed violation/enforcement table. |
| COMPL_PER_END_DATE | date (typed) | 1900-01-31 → 2028-12-31 | span_end | try_to_date(COMPL_PER_END_DATE): the close of that compliance period. |
| ENFORCEMENT_DATE | date (typed) | 1900-01-01 → 2026-06-29 | decided | try_to_date(ENFORCEMENT_DATE): the day the primacy agency took the enforcement action. The best 'decided' clock here, but null on the ~1M rows that are violation-only. |
| ENF_FIRST_REPORTED_DATE | date (typed) | 1980-09-30 → 2026-07-01 | reported | try_to_date(ENF_FIRST_REPORTED_DATE): first state submission of the enforcement record. |
| ENF_LAST_REPORTED_DATE | date (typed) | 1980-09-30 → 2026-07-01 | reported | try_to_date(ENF_LAST_REPORTED_DATE): most recent re-submission of the enforcement record. |
| NON_COMPL_PER_BEGIN_DATE | date (typed) | 1900-01-01 → 2026-06-09 | span_start | try_to_date(NON_COMPL_PER_BEGIN_DATE): the start of the actual noncompliance window. |
| NON_COMPL_PER_END_DATE | date (typed) | 1900-01-31 → 2027-12-31 | span_end | try_to_date(NON_COMPL_PER_END_DATE): the close of the noncompliance window. |
| PWS_DEACTIVATION_DATE | date (typed) | 1902-02-02 → 2026-06-30 | happened | try_to_date(PWS_DEACTIVATION_DATE): the day the water system shut down - denormalized from the system record onto every violation row, so it describes the system, not this violation. |
| SUBMISSIONYEARQUARTER | quarter | 2026 → 2026 | reported | Raw passthrough of SUBMISSIONYEARQUARTER (no cast): the YYYYQn SDWIS federal-reporting cycle in which the state submitted this row. A submission label, not an event - quarter grain, never date-parse it. |
| VIOL_FIRST_REPORTED_DATE | date (typed) | 1980-09-30 → 2026-07-01 | reported | try_to_date(VIOL_FIRST_REPORTED_DATE): first state submission of the violation record. |
| VIOL_LAST_REPORTED_DATE | date (typed) | 1980-09-30 → 2026-07-01 | reported | try_to_date(VIOL_LAST_REPORTED_DATE): most recent re-submission of the violation record. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_SUPERFUND_SITE_BOUNDARIES
| column | format | range | meaning | description |
|---|---|---|---|---|
| LAST_CHANGE_AT | datetime (typed) | 2008-12-01 00:00:00.000 → 2026-08-04 00:00:00.000 |  |  |
| ORIGINALLY_CREATED_AT | datetime (typed) | 2003-11-05 00:00:00.000 → 2026-04-14 18:45:46.000 | reported | Staging does to_timestamp_ntz(try_to_number(ORIGINAL_CREATION_DATE)/1000) - an epoch-MILLISECONDS string, decoded correctly here: when EPA first created the boundary feature record in its public GIS layer. Publication of the record, not contamination or NPL listing. |

### ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023
| column | format | range | meaning | description |
|---|---|---|---|---|
| C_1_YEAR | year only | 2023 → 2023 | happened | Raw passthrough of C_1_YEAR in the 2023 TRI basic file: the reporting year the releases occurred in. Integer year - the classic column that a bare date-parse turns into 1970. |

### ENVIRONMENT.ENVIRONMENT__FED_NID_DAMS
| column | format | range | meaning | description |
|---|---|---|---|---|
| CONDITION_ASSESSMENT_DATE | date (typed) | 1965-01-01 → 2031-06-30 | decided | try_to_date(CONDITION_ASSESSMENT_DATE,'MM/DD/YYYY'): the day the regulator assigned the dam's condition rating - an authority's call. |
| DATA_LAST_UPDATED | date (typed) | 2015-09-30 → 2026-08-05 | reported | try_to_date(DATA_LAST_UPDATED,'MM/DD/YYYY'). The loader note records that the NID national CSV carries a file-level 'Data Last Updated: 2026-8-5' stamp, so this is the vintage of the file we downloaded, not a dam event. |
| EAP_LAST_REVISION_DATE | date (typed) | 1960-01-17 → 2027-05-31 | happened | try_to_date(EAP_LAST_REVISION_DATE,'MM/DD/YYYY'): the day the owner last revised the emergency action plan. The census's 5023-05-25 max and 2 far-future rows are typo years surviving the MM/DD/YYYY parse. |
| LAST_INSPECTION_DATE | date (typed) | 1901-01-01 → 2026-11-05 | happened | try_to_date(LAST_INSPECTION_DATE,'MM/DD/YYYY'): the day the dam was last physically inspected. The strongest day-grain clock here and the one the harm lens uses. |
| YEAR_COMPLETED | year only | 1700 → 2026 | happened | try_to_number(YEAR_COMPLETED): the year the dam was finished - the structure's own birth date, populated for nearly every dam, so it is the honest way to lay an inventory of dams on a timeline. Integer year, not a date. |

### ENVIRONMENT.ENVIRONMENT__FED_NOAA_STORM_EVENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| BEGIN_TIME | year only | 1700 → 2035 | not_a_date | Raw BEGIN_TIME: an HHMM clock-time integer component, not a date. |
| BEGIN_YEARMONTH | month-year | 1996 → 2025 | span_start | Raw passthrough of BEGIN_YEARMONTH: a YYYYMM INTEGER giving the month the storm event began. Month grain, coarse duplicate of begin_date_time - never date-parse the integer. |
| END_TIME | year only | 1700 → 2035 | not_a_date | Raw END_TIME: HHMM clock-time integer component. |
| END_YEARMONTH | month-year | 1996 → 2025 | span_end | Raw END_YEARMONTH: YYYYMM integer for the month the event ended. |
| YEAR | year only | 1996 → 2025 | happened | try_to_number(YEAR): the year the storm event occurred - a real but coarse duplicate of begin_date_time, so it is not the primary. |

### ENVIRONMENT.ENVIRONMENT__FED_NOAA_WEATHER_API
| column | format | range | meaning | description |
|---|---|---|---|---|
| EFFECTIVE | date as text (iso) | 2026-07-01 → 2026-07-03 | span_start | Raw passthrough of EFFECTIVE (no cast): the moment a National Weather Service alert takes effect, paired with expires. Chosen as primary because it is alert-side and cannot be a fetch stamp. |
| EXPIRES | date (typed) | 2026-07-01 → 2026-07-04 | span_end | try_to_date(EXPIRES) - the only cast column here: when the alert stops being in force. |

### ENVIRONMENT.ENVIRONMENT__FED_PHMSA_FLAGGED_INCIDENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| INCIDENT_YEAR | year only | 2010 → 2026 | happened | try_to_number(trim(IYEAR)): the year the pipeline incident occurred. A coarse integer duplicate of local_datetime. |
| REPORT_RECEIVED_DATE | date (typed) | 2010-03-10 → 2026-07-31 | reported | Staging casts try_to_date(trim(REPORT_RECEIVED_DATE)): the day PHMSA received the operator's incident report - always after the incident, and the gap is itself a finding. |

### ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_TIME_COMPLETE | datetime (typed) | 1990-01-29 04:43:35.000 → 2026-08-02 23:17:00.000 | reported | try_to_timestamp(trim(DATE_TIME_COMPLETE)): when NRC closed out the report write-up. |
| DATE_TIME_RECEIVED | datetime (typed) | 1990-01-01 00:01:00.000 → 2026-08-02 23:07:00.000 | reported | try_to_timestamp(trim(DATE_TIME_RECEIVED)): the moment the National Response Center took the spill/release call - the best clock on the table. |
| SRC_YEAR | year only | 1990 → 2026 | ingest | OUR OWN bookkeeping: the loader writes df['_SRC_YEAR'] = y while walking CY90..CY26 of nrc.uscg.mil/FOIAFiles/CY<yy>.xlsx, so it names the source FILE we downloaded, not the incident. Exactly the class of column that corrupted the previous census. |

### ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENT_REPORTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_TIME_COMPLETE | datetime (typed) | 2020-01-01 00:21:00.000 → 2024-12-31 22:27:00.000 | reported | try_to_timestamp(trim(DATE_TIME_COMPLETE)): when the NRC finished writing up the report - a second, later reporting milestone. |
| DATE_TIME_RECEIVED | datetime (typed) | 2020-01-01 00:14:00.000 → 2024-12-31 22:24:00.000 | reported | try_to_timestamp(trim(DATE_TIME_RECEIVED)): the moment the National Response Center took the call. It is a report-receipt clock, not the spill itself, though NRC calls usually come in within hours. |

### ENVIRONMENT.ENVIRONMENT__FED_USGS_MINERALS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DISC_YR | year only | 1700 → 2002 | happened | Raw passthrough DISC_YR: the year the mineral deposit was discovered, with DY_BA as its basis code. Integer year. |
| YR_FST_PRD | year only | 1700 → 2007 | span_start | Raw passthrough YR_FST_PRD: year of FIRST production at the deposit, opening the site's producing life. Integer year, sits next to its YFP_BA basis code. |
| YR_LST_PRD | year only | 1760 → 2013 | span_end | Raw passthrough YR_LST_PRD: year of LAST production, closing the producing life. Integer year, sits next to its YLP_BA basis code. |

### ENVIRONMENT.ENVIRONMENT__FED_USGS_ORPHANED_OIL_GAS_WELLS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_FILE_DATE | date (typed) | 2019-07-01 → 2022-12-10 | reported | try_to_date(trim(DATA_FILE_DATE),'MM/DD/YYYY'): the date of the state agency's data file the well record came from. It is file vintage - the table carries no drilling, plugging or orphaning date at all, so this is the only clock available and a weak one. |

### ENVIRONMENT.ENVIRONMENT__FED_USGS_WATER
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATETIME | date as text (iso) | 2026-06-25 → 2026-07-02 | happened | Raw passthrough of DATETIME (no cast anywhere in the mart): the moment the water measurement was taken at the gauge. A real event clock, but still an uncast string - the census recording no min/max is consistent with that. |

### ENVIRONMENT.ENVIRONMENT__FED_USGS_WBD_HUC8
| column | format | range | meaning | description |
|---|---|---|---|---|
| LOAD_DATE | datetime (typed) | 2012-06-11 07:54:56.000 → 2024-12-28 10:42:38.000 | ingest | Staging decodes to_timestamp_ntz(cast(LOADDATE/1000 as bigint)) - an epoch-milliseconds field meaning when the boundary feature was loaded into the national Watershed Boundary Dataset. Pure data-management bookkeeping; a watershed polygon has no event date, so this reference table has no real clock. |

### ENVIRONMENT.ENVIRONMENT__FED_WQP_MONITORING_STATIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| CONSTRUCTION_DATE_TEXT | date as text (yyyymmdd) | 1918-11-09 → 2022-05-10 | happened | Staging keeps trim(CONSTRUCTIONDATETEXT) as TEXT with no cast: free-form text for when a monitoring well was constructed. LOW - a real event date in principle but unparsed, mixed-format, and only meaningful for well-type stations; the census read no min/max at all, which fits. |

### ENVIRONMENT.ENVIRONMENT__INTL_GLOBAL_WITNESS_DEFENDERS
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 2005 → 2026 | happened | try_to_number(YEAR): the year the land/environmental defender was killed or attacked - the only clock on the table and a genuine event year. |

### ENVIRONMENT.ENVIRONMENT__XC_OWID_CO2
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 1750 → 2024 | happened | try_to_number(YEAR) on an OWID annual series (annual CO2 emissions): the calendar year the measurement describes. Year grain by construction - this table is a time series and year is its whole clock. |

### ENVIRONMENT.ENVIRONMENT__XC_OWID_FOSSIL_SHARE
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 1965 → 2024 | happened | try_to_number(YEAR) on an OWID annual series (fossil share of primary energy): the calendar year the measurement describes. Year grain by construction - this table is a time series and year is its whole clock. |

### ENVIRONMENT.ENVIRONMENT__XC_OWID_TEMP_ANOMALY
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 1850 → 2026 | happened | try_to_number(YEAR) on an OWID annual series (global temperature anomaly): the calendar year the measurement describes. Year grain by construction - this table is a time series and year is its whole clock. |

### FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACHIEVED_DATE | date (typed) | 1970-06-01 → 2026-07-17 | decided | try_to_date(ACHIEVED_DATE): the day the informal federal enforcement action was achieved by the agency. Census min 1970-06-01 with 1 epoch-1970 row - one junk row only. (An environment table living in the FINANCE schema.) |

### FINANCE.FINANCE__FED_EPA_ICIS_FEC_ICIS_FEC_EPA_INSPECTIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACTUAL_BEGIN_DATE | date (typed) | 1958-05-30 → 2026-07-24 | span_start | try_to_date(ACTUAL_BEGIN_DATE): the day the federal inspection started; with actual_end_date it bounds the inspection. Census min 0201-08-01 is try_to_date junk, not a real 3rd-century row. |
| ACTUAL_END_DATE | date (typed) | 1986-07-08 → 2026-07-24 | span_end | try_to_date(ACTUAL_END_DATE): the day the federal inspection finished. |

### FINANCE.FINANCE__FED_FDIC_BANK_DATA
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATEUPDT | date (typed) | 1975-02-28 → 2026-08-05 | unclear | try_to_date(left(DATEUPDT,10)) - FDIC's own record-last-updated stamp, bookkeeping about when the directory row was refreshed rather than a world event; never a table clock. |
| ENDEFYMD | date (typed) | 1970-01-01 → 2026-07-17 |  |  |
| ESTYMD | date (typed) | 1782-01-01 → 2026-06-22 |  |  |
| INSURANCE_DROPPED_DATE | date (typed) | 1985-02-19 → 2018-03-28 | span_end | try_to_date(left(INSDROPDATE,10)) - the day insurance coverage ended, closing the coverage period; a likely home for the census's 9999-12-31 sentinel rows. |
| INSURED_DATE | date (typed) | 1934-01-01 → 2026-06-22 | unclear | try_to_date(left(INSDATE,10)) - the day FDIC insurance coverage began, opening the coverage period it shares with insurance_dropped_date; best of the three listed columns. |
| REPDTE | date (typed) | 1984-03-31 → 2026-03-31 |  |  |

### FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS
| column | format | range | meaning | description |
|---|---|---|---|---|
| INSURED_BRANCH_TIME_SAVINGS_DEPOSITS_THOUSANDS | month-year | 1793 → 1945 | not_a_date | try_to_number(INSBRTS) - a dollar amount in thousands; only the words 'time savings' made it look time-shaped. |
| SIMS_ACQUIRED_DATE | date (typed) | 1970-01-02 → 2025-06-27 | happened | try_to_date(split_part(SIMS_ACQUIRED_DATE,' ',1),'MM/DD/YYYY') - the day the branch was acquired by the institution. |
| SIMS_ESTABLISHED_DATE | date (typed) | 1782-01-01 → 2025-06-30 | happened | try_to_date(...,'MM/DD/YYYY') - the day the branch was established; the staging comment records the 2026-08-18 finding that its 26,581 rows at 1970-01-01 are real 1970 establishments, not the epoch trap. |
| SURVEY_YEAR | year only | 1994 → 2025 | happened | try_to_number(YEAR) - the SOD survey year the branch-deposit figures describe and half the table's own grain; a number, so it must never be bare date-parsed. |

### FINANCE.FINANCE__FED_FEC_BULK_COMMITTEES
| column | format | range | meaning | description |
|---|---|---|---|---|
| CYCLE | year only | 2026 → 2026 | reported | Raw CYCLE passthrough - the two-year FEC election cycle the committee registration file belongs to; a year-grain label, not a date, and the table's only time-shaped column. |

### FINANCE.FINANCE__FED_FEC_CANDIDATES
| column | format | range | meaning | description |
|---|---|---|---|---|
| CAND_ELECTION_YR | year only | 1980 → 2035 | happened | try_to_number(C4) - the election year the candidate is running in; the mart's own comment warns this landing table has no cycle column at all, so this is the only time anchor it has. |

### FINANCE.FINANCE__FED_FEC_CAND_CMTE_LINKAGE
| column | format | range | meaning | description |
|---|---|---|---|---|
| CAND_ELECTION_YR | year only | 1980 → 2034 | happened | try_to_number(C2) - the year of the election the candidate is contesting; a number, never bare date-parse it. |
| FEC_ELECTION_YR | year only | 2018 → 2024 | reported | try_to_number(C3) - the FEC's own cycle tag for the linkage record rather than the candidate's election. |

### FINANCE.FINANCE__FED_FEC_COMMITTEE_TO_CANDIDATE
| column | format | range | meaning | description |
|---|---|---|---|---|
| CYCLE | year only | 2024 → 2026 | reported | Raw CYCLE passthrough - the two-year FEC filing cycle the transaction file belongs to. |

### FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES
| column | format | range | meaning | description |
|---|---|---|---|---|
| FEC_ELECTION_YR | year only | 2018 → 2024 | reported | Uncast year label naming the election cycle the FEC filed the expenditure under. |

### FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| TRANSACTION_DATE | date (typed) | 2000-01-01 → 2029-05-21 | happened | try_to_date(transaction_dt,'MMDDYYYY') - the day the individual contribution was made; the explicit format rules out the epoch trap, and the 4 far-future rows (max 3312) are source typos. |

### FINANCE.FINANCE__FED_FEC_LEADERSHIP_PAC
| column | format | range | meaning | description |
|---|---|---|---|---|
| CAND_ELECTION_YR | year only | 1980 → 2034 | happened | Raw year passthrough - the election year the linked candidate is contesting; the only real time anchor on this crosswalk. |
| FEC_ELECTION_YR | year only | 2024 → 2024 | reported | Raw year passthrough - the FEC's own cycle tag for the leadership-PAC linkage record. |

### FINANCE.FINANCE__FED_FHFA_FHLB_MEMBERSHIP
| column | format | range | meaning | description |
|---|---|---|---|---|
| APPR_DATE | date (typed) | 1990-04-27 → 2026-03-25 | decided | try_to_date(APPR_DATE,'MM/DD/YY') - the day the membership application was approved; the 2-digit-year format is why 88 rows land in 2066 (a 1966 value read forward a century). |
| MEM_DATE | date (typed) | 1973-01-02 → 2035-12-28 | span_start | try_to_date(MEM_DATE,'MM/DD/YY') - the day FHLB membership began, opening the membership period; same 2-digit-year century risk. |

### FINANCE.FINANCE__FED_IRS_SOI
| column | format | range | meaning | description |
|---|---|---|---|---|
| TAX_YEAR | year only | 2016 → 2016 | happened | Raw TAX_YEAR passthrough - the tax year whose income/return statistics the aggregate row describes; a bare year number and exactly the shape that collapses to 1970 if date-parsed. |

### FINANCE.FINANCE__FED_NCUA_CALL_REPORTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| CYCLE_DATE | date (typed) | 2015-03-31 → 2015-03-31 |  |  |

### FINANCE.FINANCE__FED_NCUA_CALL_REPORTS_FOICU
| column | format | range | meaning | description |
|---|---|---|---|---|
| AM_DATEHELD | datetime (typed) | 2019-03-24 00:00:00.000 → 2026-05-19 05:00:00.000 | happened | Dual-format try_to_timestamp kept as a timestamp; reads as the credit union's annual-meeting date held, but the meaning is inferred from the NCUA field name and was not confirmed against values. |
| CYCLE_DATE | date (typed) | 2026-03-31 → 2026-03-31 | span_end | Dual-format try_to_timestamp of CYCLE_DATE cast to date - the quarter-end the call-report cycle covers (2026-03-31), constant across the file. |
| INSURED_DATE | date (typed) | 1899-12-30 → 2025-12-05 | span_start | Dual-format try_to_timestamp cast to date - the day NCUA share insurance took effect, opening the coverage period. |
| ISSUE_DATE | date (typed) | 1899-12-30 → 2025-12-05 | decided | Dual-format try_to_timestamp cast to date - reads as the day the charter was issued by the regulator; the staging header confirms the mixed 12/24-hour formats were handled deliberately to dodge the epoch trap. |
| YEAR_OPENED | year only | 1900 → 2025 | happened | try_to_number(YEAR_OPENED) - the year the credit union opened, the one per-row real-world event on this roster that spreads across decades; a number, never date-parse it. |

### FINANCE.FINANCE__FED_NCUA_CALL_REPORTS_FS220
| column | format | range | meaning | description |
|---|---|---|---|---|
| CYCLE_DATE | date (typed) | 2026-03-31 → 2026-03-31 | span_end | Dual-format try_to_timestamp cast to date - the quarter-end (2026-03-31) the financial statement covers; the only world-facing clock on the table. |
| UPDATE_DATE | datetime (typed) | 2026-04-01 22:01:28.000 → 2026-05-20 22:02:49.000 | unclear | Dual-format try_to_timestamp of UPDATE_DATE - NCUA's record-refresh stamp (census max 2026-05-20, weeks after the 2026-03-31 cycle), bookkeeping about the file rather than a world event. |

### FINANCE.FINANCE__FED_NCUA_FEDERALLY_INSURED_CU_LIST
| column | format | range | meaning | description |
|---|---|---|---|---|
| TOTAL_LOANS_4_QUARTER_GROWTH | year only | 1704 → 1704 | not_a_date | try_to_number of a 4-quarter growth rate, not a date. |

### FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS
| column | format | range | meaning | description |
|---|---|---|---|---|
| AUDIT_DUAL_DATE | date as text (iso) | 2016-02-17 → 2026-08-04 | happened | Left as raw trimmed TEXT while every real date in this model is try_to_date'd - semantically the report's dual date, but it can carry qualifier prose and is unusable until parsed. |
| AUDIT_PERIOD_INFORMATION | date as text (us) | 2011-03-31 → 2023-12-31 | not_a_date | nullif(trim(...)) - free text describing the audit period, not a parseable date. |

### FINANCE.FINANCE__FED_SEC_13F_FILERS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATEDENIEDEXPIRED | date (typed) | 2012-10-01 → 2027-05-17 | decided | try_to_date(DATEDENIEDEXPIRED) - when the SEC denied a confidential-treatment request or it expired; legitimately future-dated, which explains the census max of 2027-05-17. |
| DATEREPORTED | date as text (dd_mon_yyyy) | 2007-02-06 → 2026-05-15 | reported | Raw uncast DATEREPORTED - when previously-confidential holdings were finally reported; sparse, confidential-treatment rows only, so a poor table clock. |
| REPORTCALENDARORQUARTER | date as text (dd_mon_yyyy) | 1900-01-01 → 2026-03-31 | span_end | Raw uncast passthrough of the 13F report calendar quarter-end - the period the filing covers, and the only column populated on every row. |

### FINANCE.FINANCE__FED_SEC_13F_SUBMISSIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| FILING_DATE | date as text (dd_mon_yyyy) | 2013-05-20 → 2026-05-29 | reported | Raw FILING_DATE passthrough - when the 13F submission was filed with the SEC; uncast text, so never bare date-parse it. |
| PERIODOFREPORT | date as text (dd_mon_yyyy) | 1987-03-31 → 2026-03-31 | span_end | Raw PERIODOFREPORT passthrough - the quarter-end the reported holdings are as of, closing the covered period. |

### FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q1
| column | format | range | meaning | description |
|---|---|---|---|---|
| FILED | date as text (yyyymmdd) | 2024-01-02 → 2024-03-29 | reported | Raw FILED passthrough - the YYYYMMDD date the submission was filed with the SEC; uncast text, so never bare date-parse it. |
| FY | year only | 2016 → 2025 | span_end | try_to_number(FY) - the fiscal-year focus labelling the period the filing covers; a bare year number and the canonical epoch-1970 trap in this warehouse. |
| PERIOD | date as text (yyyymmdd) | 2016-09-30 → 2024-02-29 | span_end | Raw PERIOD passthrough - the DERA balance-sheet date, rounded by SEC to the nearest month end, bounding the period the filing reports; uncast YYYYMMDD text. |

### FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q2
| column | format | range | meaning | description |
|---|---|---|---|---|
| FILED | date as text (yyyymmdd) | 2024-04-01 → 2024-06-28 | reported | Raw FILED passthrough - the YYYYMMDD SEC filing date; uncast text. |
| FY | year only | 2020 → 2025 | span_end | try_to_number(FY) - fiscal-year focus of the filing; a bare year number, the classic epoch-1970 trap. |
| PERIOD | date as text (yyyymmdd) | 2020-06-30 → 2024-12-31 | span_end | Raw PERIOD passthrough - the DERA balance-sheet date rounded to month end, bounding the reported period; uncast YYYYMMDD text. |

### FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q3
| column | format | range | meaning | description |
|---|---|---|---|---|
| FILED | date as text (yyyymmdd) | 2024-07-01 → 2024-09-30 | reported | Raw FILED passthrough - the YYYYMMDD SEC filing date; uncast text. |
| FY | year only | 2022 → 2025 | span_end | try_to_number(FY) - fiscal-year focus of the filing; a bare year number, the classic epoch-1970 trap. |
| PERIOD | date as text (yyyymmdd) | 2022-03-31 → 2024-08-31 | span_end | Raw PERIOD passthrough - the DERA balance-sheet date rounded to month end; uncast YYYYMMDD text. |

### FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q4
| column | format | range | meaning | description |
|---|---|---|---|---|
| FILED | date as text (yyyymmdd) | 2024-10-01 → 2024-12-31 | reported | Raw FILED passthrough - the YYYYMMDD SEC filing date; uncast text. |
| FY | year only | 2019 → 2025 | span_end | try_to_number(FY) - fiscal-year focus of the filing; a bare year number, the classic epoch-1970 trap. |
| PERIOD | date as text (yyyymmdd) | 2019-03-31 → 2024-11-30 | span_end | Raw PERIOD passthrough - the DERA balance-sheet date rounded to month end; uncast YYYYMMDD text. |

### FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q1
| column | format | range | meaning | description |
|---|---|---|---|---|
| FILED | date as text (yyyymmdd) | 2025-01-02 → 2025-03-31 | reported | Raw FILED passthrough - the YYYYMMDD SEC filing date; uncast text. |
| FY | year only | 2018 → 2025 | span_end | try_to_number(FY) - fiscal-year focus of the filing; a bare year number, the classic epoch-1970 trap. |
| PERIOD | date as text (yyyymmdd) | 2018-12-31 → 2025-02-28 | span_end | Raw PERIOD passthrough - the DERA balance-sheet date rounded to month end; uncast YYYYMMDD text. |

### FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q2
| column | format | range | meaning | description |
|---|---|---|---|---|
| FILED | date as text (yyyymmdd) | 2025-04-01 → 2025-06-30 | reported | Raw FILED passthrough - the YYYYMMDD SEC filing date; uncast text. |
| FY | year only | 2023 → 2026 | span_end | try_to_number(FY) - fiscal-year focus of the filing; a bare year number, the classic epoch-1970 trap. |
| PERIOD | date as text (yyyymmdd) | 2021-12-31 → 2025-12-31 | span_end | Raw PERIOD passthrough - the DERA balance-sheet date rounded to month end; uncast YYYYMMDD text. |

### FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q3
| column | format | range | meaning | description |
|---|---|---|---|---|
| FILED | date as text (yyyymmdd) | 2025-07-01 → 2025-09-30 | reported | Raw FILED passthrough - the YYYYMMDD SEC filing date; uncast text. |
| FY | year only | 2021 → 2026 | span_end | try_to_number(FY) - fiscal-year focus of the filing; a bare year number, the classic epoch-1970 trap. |
| PERIOD | date as text (yyyymmdd) | 2020-12-31 → 2025-08-31 | span_end | Raw PERIOD passthrough - the DERA balance-sheet date rounded to month end; uncast YYYYMMDD text. |

### FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q4
| column | format | range | meaning | description |
|---|---|---|---|---|
| FILED | date as text (yyyymmdd) | 2025-10-01 → 2025-12-31 | reported | Raw FILED passthrough - the YYYYMMDD SEC filing date; uncast text. |
| FY | year only | 2022 → 2027 | span_end | try_to_number(FY) - fiscal-year focus of the filing; a bare year number, the classic epoch-1970 trap. |
| PERIOD | date as text (yyyymmdd) | 2022-03-31 → 2025-12-31 | span_end | Raw PERIOD passthrough - the DERA balance-sheet date rounded to month end; uncast YYYYMMDD text. |

### FINANCE.FINANCE__FED_SEC_DERA_SUB_2026Q1
| column | format | range | meaning | description |
|---|---|---|---|---|
| FILED | date as text (yyyymmdd) | 2026-01-02 → 2026-03-31 | reported | Raw FILED passthrough - the YYYYMMDD SEC filing date; uncast text. |
| FY | year only | 2023 → 2026 | span_end | try_to_number(FY) - fiscal-year focus of the filing; a bare year number, the classic epoch-1970 trap. |
| PERIOD | date as text (yyyymmdd) | 2023-04-30 → 2026-02-28 | span_end | Raw PERIOD passthrough - the DERA balance-sheet date rounded to month end; uncast YYYYMMDD text. |

### FINANCE.FINANCE__FED_SEC_EDGAR_FINANCIALS
| column | format | range | meaning | description |
|---|---|---|---|---|
| FILED | date as text (yyyymmdd) | 2023-01-03 → 2024-12-31 | reported | Raw FILED passthrough - the YYYYMMDD date the filing reached the SEC; uncast text. |
| FY | year only | 2012 → 2025 | span_end | try_to_number(FY) - fiscal-year focus labelling the covered period; a bare year number, the classic epoch-1970 trap. |
| PERIOD | date as text (yyyymmdd) | 2012-11-30 → 2024-12-31 | span_end | Raw PERIOD passthrough (same generated shape as the DERA sub marts) - the balance-sheet date rounded to month end, bounding the reported period. |

### FINANCE.FINANCE__FED_SEC_EDGAR_INSIDERS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_OF_ORIG_SUB | date (typed) | 2020-11-06 → 2026-03-30 | reported | try_to_date(DATE_OF_ORIG_SUB) - when the original submission was filed, populated for amendments. |
| FILING_DATE | date (typed) | 2026-01-02 → 2026-03-31 | reported | try_to_date(FILING_DATE) - when the Form 3/4/5 was filed with the SEC. |
| PERIOD_OF_REPORT | date as text (dd_mon_yyyy) | 2002-02-26 → 2026-03-31 | happened | Raw uncast passthrough; on Forms 3/4/5 the period of report is the date of the event requiring the statement (the transaction), so it is the closest thing to a real event clock here - inferred from SEC form semantics, not confirmed against values. |

### FINANCE.FINANCE__FED_SEC_INSIDER_DERIV_TRANS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DEEMED_EXECUTION_DATE | date (typed) | 2006-02-27 → 2034-01-12 | happened | try_to_date(DEEMED_EXECUTION_DATE) - the date the transaction is deemed to have executed. |
| EXCERCISE_DATE | date (typed) | 1988-08-08 → 2035-04-20 | span_start | try_to_date(EXCERCISE_DATE) - Form 4 Table II 'date exercisable', the day the derivative first becomes exercisable, opening the exercise window. |
| EXPIRATION_DATE | date (typed) | 1988-08-08 → 2035-12-31 | span_end | try_to_date(EXPIRATION_DATE) - the derivative's expiration, closing the exercise window; legitimately future-dated, which explains most of the 64,164 far-future rows the census flagged. |
| TRANS_DATE | date (typed) | 2000-04-20 → 2035-01-10 | happened | try_to_date(TRANS_DATE) - the day the derivative transaction occurred; the year-0018 minimum is source typos, not the cast. |

### FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS
| column | format | range | meaning | description |
|---|---|---|---|---|
| TRANSACTION_DATE | date (typed) | 1987-10-07 → 2033-12-11 | happened | try_to_date(trans_date,'DD-MON-YYYY') - the day the non-derivative insider transaction occurred; the explicit format rules out the epoch trap and the year-0022 minimum is source typos. |

### FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_OF_ORIGINAL_SUBMISSION | date (typed) | 1998-11-13 → 2027-06-04 | reported | try_to_date(date_of_orig_sub,'DD-MON-YYYY') - when the original submission was filed, populated for amendments. |
| FILING_DATE | date (typed) | 2016-07-01 → 2025-03-31 | reported | try_to_date(filing_date,'DD-MON-YYYY') - when the Form 3/4/5 was filed with the SEC. |
| PERIOD_OF_REPORT | date (typed) | 1982-04-25 → 2025-03-31 | happened | try_to_date(period_of_report,'DD-MON-YYYY'); on Forms 3/4/5 the period of report is the date of the event requiring the statement, i.e. the transaction itself, making it the closest real event clock - inferred from SEC form semantics. |

### FINANCE.FINANCE__FED_SEC_MONEY_MARKET_FUND_INFORMATION
| column | format | range | meaning | description |
|---|---|---|---|---|
| REPORTMONTH | date as text (iso) | 2026-04-30 → 2026-04-30 | span_end | Raw REPORTMONTH passthrough - the month of money-market-fund filings this fund/class listing summarizes; uncast text at month grain and the table's only time column. |

### FINANCE.FINANCE__INTL_ISO_MIC_REGISTRY
| column | format | range | meaning | description |
|---|---|---|---|---|
| CREATION_DATE | date (typed) | 2003-04-01 → 2026-07-27 | reported | try_to_date(CREATION_DATE,'YYYYMMDD') - when the market identifier code was first entered in the ISO 10383 registry. |
| EXPIRY_DATE | date (typed) | 2003-04-28 → 2026-07-27 | span_end | try_to_date(EXPIRY_DATE,'YYYYMMDD') - when the MIC expires or was deactivated, closing its validity period. |
| LAST_UPDATE_DATE | date (typed) | 2003-04-28 → 2026-07-27 | unclear | try_to_date(LAST_UPDATE_DATE,'YYYYMMDD') - the registry's own record-refresh stamp, bookkeeping about the file rather than a world event. |
| LAST_VALIDATION_DATE | date (typed) | 2010-08-23 → 2026-07-27 | unclear | try_to_date(LAST_VALIDATION_DATE,'YYYYMMDD') - the registry's periodic re-validation stamp of the record; maintenance metadata, not an event. |

### FOREIGN_INFLUENCE.FOREIGN_INFLUENCE__FED_FARA_BULK
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE | date (typed) | 1942-07-03 → 2026-06-08 | reported | The mart aliases staging's registration_date - try_to_date(...,'MM/DD/YYYY') - to `date`: the day the agent registered with DOJ under FARA. |
| DATE_STAMPED | date (typed) | 1942-07-01 → 2026-07-30 | reported | try_to_date(DATE_STAMPED,'MM/DD/YYYY') - DOJ's receipt stamp on the document; note staging also reuses it (coalesced with current_timestamp) as the incremental watermark, so it does double duty as pipeline metadata. |
| FOREIGN_PRINCIPAL_REGISTRATION_DATE | date (typed) | 1942-07-03 → 2026-06-11 | reported | try_to_date(...,'MM/DD/YYYY') - when this foreign principal was registered under the registrant. |
| FOREIGN_PRINCIPAL_TERMINATION_DATE | date (typed) | 1942-07-03 → 2026-06-11 | span_end | try_to_date(...,'MM/DD/YYYY') - when the foreign-principal relationship ended; drives the mart's active-principal flag. |
| REGISTRANT_DATE | date (typed) | 1942-07-03 → 2026-06-08 | reported | try_to_date(REGISTRANT_DATE,'MM/DD/YYYY') - a second registrant-level filing date whose exact meaning is documented nowhere in the model; treat as reported until someone checks values. |
| SHORT_FORM_DATE | date (typed) | 1942-01-16 → 2026-06-12 | reported | try_to_date(...,'MM/DD/YYYY') - when the short-form registration statement for an individual agent was filed. |
| SHORT_FORM_TERMINATION_DATE | date (typed) | 1942-06-01 → 2026-05-12 | span_end | try_to_date(...,'MM/DD/YYYY') - when the individual agent's short-form registration ended. |
| TERMINATION_DATE | date (typed) | 1942-07-03 → 2026-05-28 | span_end | try_to_date(...,'MM/DD/YYYY') - when the registration ended, closing the active-registration period; the mart's is_active flag is derived from it. |

### HEALTH.HEALTH__FED_CDC_ANXIETY_DEPRESSION
| column | format | range | meaning | description |
|---|---|---|---|---|
| TIME_PERIOD_END_DATE | datetime (typed) | 2020-05-05 00:00:00.000 → 2024-09-16 00:00:00.000 | span_end | try_to_timestamp of the window end, pairs with the start column. |
| TIME_PERIOD_START_DATE | datetime (typed) | 2020-04-23 00:00:00.000 → 2024-08-20 00:00:00.000 | span_start | try_to_timestamp of the survey collection window start; census 2020-04-23 to 2024-09-16 is sane. |

### HEALTH.HEALTH__FED_CDC_DATA_PORTAL
| column | format | range | meaning | description |
|---|---|---|---|---|
| CREATED_AT | datetime (typed) | 2013-06-10 19:09:30.000 → 2026-07-07 15:32:14.000 | happened | Row is a dataset; created_at is when it came into existence on data.cdc.gov, parsed with an explicit ISO format. |
| DATA_UPDATED_AT | datetime (typed) | 2013-06-19 14:45:55.000 → 2026-08-11 14:00:20.000 | reported | When CDC last refreshed the dataset's data - publisher bookkeeping. |
| METADATA_UPDATED_AT | datetime (typed) | 2015-08-18 21:49:28.000 → 2026-08-10 18:30:27.000 | reported | When CDC last touched the metadata - publisher bookkeeping. |
| PUBLICATION_DATE | date (typed) | 2013-06-19 → 2026-08-07 | reported | try_to_date - when CDC published the dataset. |
| UPDATED_AT | datetime (typed) | 2015-08-18 21:49:28.000 → 2026-08-11 14:00:20.000 | reported | Publisher-side last-touch stamp - a vintage, not an event. |

### HEALTH.HEALTH__FED_CDC_DRUG_POISONING_COUNTY
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 1999 → 2015 | happened | try_to_number(YEAR) - year the county's drug-poisoning deaths occurred; a bare date-parse would epoch-collapse it. |

### HEALTH.HEALTH__FED_CDC_HEALTH_INSURANCE
| column | format | range | meaning | description |
|---|---|---|---|---|
| TIME_PERIOD_END_DATE | datetime (typed) | 2020-05-05 00:00:00.000 → 2024-09-16 00:00:00.000 | span_end | try_to_timestamp of the survey window end. |
| TIME_PERIOD_START_DATE | datetime (typed) | 2020-04-23 00:00:00.000 → 2024-08-20 00:00:00.000 | span_start | try_to_timestamp of the survey window start; census 2020-2024 is sane. |

### HEALTH.HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_AS_OF | date as text (iso) | 2026-05-14 → 2026-06-22 | reported | Uncast text snapshot vintage from CDC. |
| PERIOD | year only | 2019 → 2024 | happened | Uncast text window label on a trailing-multi-year county file; the only real time reference here, value shape unverified. |

### HEALTH.HEALTH__FED_CDC_LEADING_CAUSES_STATE
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 1999 → 2017 | happened | try_to_number(trim(YEAR)) in staging; year of death, 1999-2017. |

### HEALTH.HEALTH__FED_CDC_NNDSS_WEEKLY_2024
| column | format | range | meaning | description |
|---|---|---|---|---|
| CUMULATIVE_YTD_CURRENT_MMWR_YEAR | year only | 1700 → 2035 | not_a_date | Year-to-date case count. |
| CUMULATIVE_YTD_PREVIOUS_MMWR_YEAR | year only | 1700 → 2035 | not_a_date | Prior-year YTD case count. |
| CURRENT_MMWR_YEAR | year only | 2022 → 2026 | reported | MMWR reporting year (uncast text); the only standalone time coordinate. |
| CURRENT_WEEK | year only | 1700 → 2034 | not_a_date | NNDSS 'current week' is the CASE COUNT reported that week, not a date. |
| PREVIOUS_52_WEEK_MAX | year only | 1700 → 2035 | not_a_date | Max weekly case count over the prior 52 weeks - a count. |

### HEALTH.HEALTH__FED_CDC_OVERDOSE
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 2015 → 2026 | happened | try_to_number(YEAR) - year of the provisional overdose-death window; only standalone coordinate. |

### HEALTH.HEALTH__FED_CDC_SUICIDE_RATES
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 1950 → 2018 | happened | try_to_number(YEAR) - year the rate describes; nulls on any range-valued rows. |

### HEALTH.HEALTH__FED_CDC_WONDER
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 1999 → 2020 | happened | try_to_number(trim(YEAR)) in staging; year of death for the national mortality grid. |

### HEALTH.HEALTH__FED_CLINICALTRIALS
| column | format | range | meaning | description |
|---|---|---|---|---|
| COMPLETION_DATE | date (typed) | 2009-06-10 → 2032-06-06 | span_end | Trial period end; the 3 far-future rows (max 2032) are real, not corruption. |
| DAYS_TO_RESULTS_POSTING | year only | 1767 → 2011 | not_a_date | datediff between two posting dates - a duration. |
| FIRST_POSTED_DATE | date (typed) | 1999-09-21 → 2026-06-11 | reported | try_to_date 'YYYY-MM-DD' - when the registration first appeared publicly. |
| LAST_UPDATE_POSTED_DATE | date (typed) | 2005-06-24 → 2026-06-16 | reported | Registry last-update posting stamp - the source's vintage, not an event. |
| PRIMARY_COMPLETION_DATE | date (typed) | 2009-06-10 → 2031-10-22 | span_end | End of the primary-outcome collection window; legitimately future-dated. |
| RESULTS_FIRST_POSTED_DATE | date (typed) | 2010-06-22 → 2026-06-04 | reported | When results were first posted to the registry. |
| START_DATE | date (typed) | 1997-01-01 → 2026-09-15 | span_start | try_to_date 'YYYY-MM-DD' - the trial's period-of-performance start. |
| STUDY_DURATION_DAYS | year only | 1700 → 2006 | not_a_date | datediff('day', start_date, completion_date) - a duration. |

### HEALTH.HEALTH__FED_CMS_DIALYSIS
| column | format | range | meaning | description |
|---|---|---|---|---|
| CERTIFICATION_DATE | date (typed) | 1968-01-01 → 2026-02-09 | decided | try_to_date of the Medicare certification date - the only per-facility clock on this table. |

### HEALTH.HEALTH__FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| INCORPORATION_DATE | date (typed) | 1817-01-01 → 2024-08-26 | happened | try_to_date of incorporation; 281 rows on 1970-01-01 and an 1817 floor are sentinels. |

### HEALTH.HEALTH__FED_CMS_HCRIS
| column | format | range | meaning | description |
|---|---|---|---|---|
| FISCAL_YEAR_BEGIN_DATE | date (typed) | 2022-10-01 → 2023-09-28 | span_start | try_to_date in staging; start of the cost-report period. |
| FISCAL_YEAR_END_DATE | date (typed) | 2022-11-30 → 2024-09-30 | span_end | try_to_date in staging; end of the cost report's fiscal year. |
| FISCAL_YEAR_END_DATE_KEY | date (typed) | 2022-11-30 → 2024-09-30 | span_end | A copy of fiscal_year_end_date exposed as a join key, not a second clock. |
| HOSPITAL_TOTAL_BED_DAYS_AVAILABLE_ADULTS_PEDS | year only | 1701 → 2033 | not_a_date | A count of bed-days. |
| HOSPITAL_TOTAL_DAYS_TITLE_V_ADULTS_PEDS | year only | 1720 → 1825 | not_a_date | A count of patient-days. |
| HOSPITAL_TOTAL_DAYS_TITLE_XVIII_ADULTS_PEDS | year only | 1701 → 2034 | not_a_date | A count of patient-days. |
| TOTAL_BED_DAYS_AVAILABLE | year only | 1700 → 2033 | not_a_date | A count of bed-days (capacity). |
| TOTAL_DAYS_ALL | year only | 1700 → 2035 | not_a_date | Total patient-days; used as the occupancy numerator in this same model. |
| TOTAL_DAYS_TITLE_V | year only | 1761 → 1943 | not_a_date | A count of patient-days under Title V. |
| TOTAL_DAYS_TITLE_XIX | year only | 1701 → 2035 | not_a_date | A count of patient-days under Title XIX. |
| TOTAL_DAYS_TITLE_XVIII | year only | 1701 → 2035 | not_a_date | A count of patient-days under Title XVIII. |

### HEALTH.HEALTH__FED_CMS_HOME_HEALTH
| column | format | range | meaning | description |
|---|---|---|---|---|
| CERTIFICATION_DATE | date (typed) | 1966-07-01 → 2025-10-09 | decided | try_to_date of the Medicare certification date; 26 rows land on 1970-01-01. |

### HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| INCORPORATION_DATE | date (typed) | 1808-03-08 → 2024-08-09 | happened | try_to_date of incorporation; 7 epoch-1970 rows and an 1808 floor are sentinels. |

### HEALTH.HEALTH__FED_CMS_HOSPICE
| column | format | range | meaning | description |
|---|---|---|---|---|
| CERTIFICATION_DATE | date (typed) | 1983-11-01 → 2025-10-15 | decided | try_to_date of the Medicare certification date for the hospice. |

### HEALTH.HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| INCORPORATION_DATE | date (typed) | 1800-01-01 → 2024-10-01 | happened | try_to_date of incorporation; 60 epoch-1970 rows and an 1800-01-01 floor. |
| REH_CONVERSION_DATE | date (typed) | 2023-02-10 → 2026-03-14 | happened | try_to_date of the Rural Emergency Hospital conversion; sparse, only set for converters. |

### HEALTH.HEALTH__FED_CMS_IRF
| column | format | range | meaning | description |
|---|---|---|---|---|
| CERTIFICATION_DATE | date (typed) | 1983-10-01 → 2026-10-01 | decided | try_to_date of the Medicare certification date for the rehab facility. |

### HEALTH.HEALTH__FED_CMS_LTCH
| column | format | range | meaning | description |
|---|---|---|---|---|
| CERTIFICATION_DATE | date (typed) | 1966-07-01 → 2025-02-01 | decided | try_to_date of the Medicare certification date; 1 epoch-1970 row. |

### HEALTH.HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR_COL | year only | 2021 → 2024 | happened | try_to_number(YEAR) - the measurement year for the facility-measure row. |

### HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER
| column | format | range | meaning | description |
|---|---|---|---|---|
| BENE_AGE_65_74_CNT | year only | 1774 → 1774 | not_a_date | Count of beneficiaries aged 65-74. |

### HEALTH.HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER
| column | format | range | meaning | description |
|---|---|---|---|---|
| BENE_AGE_65_74_CNT | year only | 1703 → 2034 | not_a_date | Count of beneficiaries aged 65-74. |
| BENE_AGE_75_84_CNT | year only | 1702 → 2034 | not_a_date | Count of beneficiaries aged 75-84. |
| BENE_AGE_GT_84_CNT | year only | 1700 → 2000 | not_a_date | Count of beneficiaries over 84. |
| BENE_AGE_LT_65_CNT | year only | 1704 → 1990 | not_a_date | Count of beneficiaries under 65. |
| TOT_CVRD_DAYS | year only | 1701 → 2035 | not_a_date | Total covered inpatient days - a count. |
| TOT_DAYS | year only | 1703 → 2032 | not_a_date | Total inpatient days - a count. |

### HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER
| column | format | range | meaning | description |
|---|---|---|---|---|
| BENE_AGE_65_74_CNT | year only | 1700 → 2035 | not_a_date | Count of beneficiaries aged 65-74. |
| BENE_AGE_75_84_CNT | year only | 1700 → 2034 | not_a_date | Count of beneficiaries aged 75-84. |
| BENE_AGE_GT_84_CNT | year only | 1700 → 2035 | not_a_date | Count of beneficiaries over 84. |
| BENE_AGE_LT_65_CNT | year only | 1705 → 2031 | not_a_date | Count of beneficiaries under 65. |

### HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI
| column | format | range | meaning | description |
|---|---|---|---|---|
| TOT_BENE_DAY_SRVCS | year only | 1700 → 2035 | not_a_date | Total beneficiary day-services - a service count. |

### HEALTH.HEALTH__FED_CMS_MEDICARE_PROVIDER
| column | format | range | meaning | description |
|---|---|---|---|---|
| BENE_AGE_65_74_CNT | year only | 1700 → 2035 | not_a_date | Count of beneficiaries aged 65-74. |
| BENE_AGE_75_84_CNT | year only | 1700 → 2034 | not_a_date | Count of beneficiaries aged 75-84. |
| BENE_AGE_GT_84_CNT | year only | 1700 → 2035 | not_a_date | Count of beneficiaries over 84. |
| BENE_AGE_LT_65_CNT | year only | 1705 → 2031 | not_a_date | Count of beneficiaries under 65. |

### HEALTH.HEALTH__FED_CMS_NADAC
| column | format | range | meaning | description |
|---|---|---|---|---|
| AS_OF_DATE | date (typed) | 2024-01-03 → 2024-12-25 | reported | try_to_date of the CMS file's as-of stamp - the publisher's snapshot vintage. |
| EFFECTIVE_DATE | date (typed) | 2022-11-23 → 2024-12-25 | happened | try_to_date; the date the surveyed acquisition price took effect, and half the declared grain key. |
| GENERIC_EFFECTIVE_DATE | date (typed) | 2023-01-18 → 2024-12-25 | happened | try_to_date; effective date of the corresponding generic's price. |

### HEALTH.HEALTH__FED_CMS_NPPES
| column | format | range | meaning | description |
|---|---|---|---|---|
| CERTIFICATION_DATE | date (typed) | 2010-11-24 → 2026-06-08 |  |  |
| LAST_UPDATE_DATE | date (typed) | 2007-07-08 → 2026-06-08 |  |  |
| NPI_DEACTIVATION_DATE | date (typed) | 2005-05-23 → 2026-06-07 |  |  |
| NPI_REACTIVATION_DATE | date (typed) | 2005-05-24 → 2026-06-05 |  |  |
| PROVIDER_ENUMERATION_DATE | date (typed) | 2005-05-23 → 2026-06-06 |  |  |

### HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES
| column | format | range | meaning | description |
|---|---|---|---|---|
| CORRECTION_DATE | date (typed) | 2002-04-08 → 2026-06-29 | happened | try_to_date - when the deficiency was corrected; also readable as the span_end of the open-citation window. |
| PROCESSING_DATE | date (typed) | 2026-06-01 → 2026-06-01 | reported | CMS file-processing stamp - the row's publication vintage. |
| SURVEY_DATE | date (typed) | 2017-03-23 → 2026-05-20 | happened | try_to_date - the inspection that produced the citation; census 2002-2026 is clean. |

### HEALTH.HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES
| column | format | range | meaning | description |
|---|---|---|---|---|
| CORRECTION_DATE | date (typed) | 2016-01-15 → 2027-05-30 | happened | try_to_date - when corrected; the table's 2027-05-30 census max most likely sits here. |
| PROCESSING_DATE | date (typed) | 2026-06-01 → 2026-06-01 | reported | CMS file-processing stamp. |
| SURVEY_DATE | date (typed) | 2016-07-28 → 2026-05-21 | happened | try_to_date - the fire-safety inspection date. |

### HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES
| column | format | range | meaning | description |
|---|---|---|---|---|
| PAYMENT_DENIAL_START_DATE | date (typed) | 2023-06-30 → 2026-05-15 | span_start | try_to_date - start of the payment-denial period, bounded by the length-in-days column. |
| PENALTY_DATE | date (typed) | 2023-06-17 → 2026-05-13 | decided | try_to_date - the date CMS imposed the fine or denial. |
| PROCESSING_DATE | date (typed) | 2026-06-01 → 2026-06-01 | reported | CMS file-processing stamp. |

### HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_OF_PAYMENT | date as text (us) | 2024-01-01 → 2024-12-31 | happened | The date the manufacturer paid the doctor, but passed through UNCAST from landing - 15.4M rows of text, which is why the census measured nothing. |
| PROGRAM_YEAR | year only | 2024 → 2024 | happened | Program year = the calendar year the payment was made; a bare date-parse of it is the classic epoch-1970 trap. |

### HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2022
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_OF_PAYMENT | date as text (us) | 2022-01-01 → 2022-12-31 | happened | Payment date, uncast text from landing (13.3M rows). |
| PROGRAM_YEAR | year only | 2022 → 2022 | happened | Calendar year of the payment; near-constant on this single-year table. |

### HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2023
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_OF_PAYMENT | date as text (us) | 2023-01-01 → 2023-12-31 | happened | Payment date, uncast text from landing (14.7M rows). |
| PROGRAM_YEAR | year only | 2023 → 2023 | happened | Calendar year of the payment; near-constant on this single-year table. |

### HEALTH.HEALTH__FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS
| column | format | range | meaning | description |
|---|---|---|---|---|
| MEDICARE_ID_EFFECTIVE_DATE | date (typed) | 2014-10-25 → 2026-05-20 | span_start | try_to_date - when the provider's Medicare ID became effective, the start of enrollment; no paired end column. |

### HEALTH.HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS
| column | format | range | meaning | description |
|---|---|---|---|---|
| LAST_UPDATED | date (typed) | 2024-04-15 → 2026-07-13 | reported | try_to_date of a file refresh stamp - flagged as bookkeeping; could instead be a per-record update stamp, unverified without values. |
| OPTOUT_EFFECTIVE_DATE | date (typed) | 1998-01-01 → 2026-10-01 | span_start | try_to_date - start of the physician's Medicare opt-out period. |
| OPTOUT_END_DATE | date (typed) | 2026-06-30 → 2028-10-01 | span_end | try_to_date - end of the opt-out period; the 2028-10-01 census max is a live future end date, not corruption. |

### HEALTH.HEALTH__FED_CMS_PARTD_PRESCRIBERS
| column | format | range | meaning | description |
|---|---|---|---|---|
| TOTAL_DAY_SUPPLY | year only | 1700 → 2035 | not_a_date | try_to_number('Tot_Day_Suply') - total days of drug supplied; the table's only timestamp is _loaded_at, which is what the census reported as its range. |

### HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS
| column | format | range | meaning | description |
|---|---|---|---|---|
| BENE_AGE_65_74_CNT | year only | 1750 → 2018 | not_a_date | Count of beneficiaries aged 65-74. |
| BENE_AGE_75_84_CNT | year only | 1700 → 2023 | not_a_date | Count of beneficiaries aged 75-84. |
| BENE_AGE_GT_84_CNT | year only | 1734 → 2001 | not_a_date | Count of beneficiaries over 84. |
| BENE_AGE_LT_65_CNT | year only | 1737 → 2030 | not_a_date | Count of beneficiaries under 65. |
| GE65_TOT_DAY_SUPLY | year only | 1700 → 2035 | not_a_date | Days of supply for the 65+ cohort - a count. |
| TOT_DAY_SUPLY | year only | 1700 → 2035 | not_a_date | Total days of drug supplied - a count. |

### HEALTH.HEALTH__FED_CMS_POS_OTHER
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACRDTN_EFCTV_DT | date as text (yyyymmdd) | 1966-07-01 → 2028-11-08 | span_start | Accreditation effective date - start of the accreditation span. |
| ACRDTN_EXPRTN_DT | date as text (yyyymmdd) | 1969-07-01 → 2034-06-17 | span_end | Accreditation expiration date - end of the accreditation span. |
| CHOW_DT | date as text (yyyymmdd) | 1973-06-30 → 2026-01-01 | happened | Change-of-ownership date, UNCAST; CMS POS ships YYYYMMDD text so a bare cast would epoch-collapse it. |
| CHOW_PRIOR_DT | date as text (yyyymmdd) | 1966-07-01 → 2024-08-30 | happened | Prior change-of-ownership date - uncast text. |
| CRTFCTN_DT | date as text (yyyymmdd) | 1966-07-01 → 2026-03-26 | decided | Medicare certification date - uncast text, but the most broadly populated clock here (chow_dt only exists for ownership changes). |
| FQHC_APPROVED_RHC_PROVIDER_NUM | month-year | 1838 → 1838 | not_a_date | A provider NUMBER, not a date. |
| NCRY_PRVDR_DSGNTD_DT | date as text (yyyymmdd) | 1993-12-01 → 2023-02-27 | decided | Date the necessary-provider designation was granted. |
| ORGNL_PRTCPTN_DT | date as text (yyyymmdd) | 1966-07-01 → 2026-03-24 | decided | Original Medicare participation date - uncast text. |
| TRMNTN_EXPRTN_DT | date as text (yyyymmdd) | 1963-05-07 → 2026-03-19 | span_end | Termination/expiration of Medicare participation - end of the participation span. |

### HEALTH.HEALTH__FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| INCORPORATION_DATE | date (typed) | 1859-01-28 → 2024-08-19 | happened | try_to_date of incorporation; 22 epoch-1970 rows and an 1859 floor are sentinels. |

### HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| INCORPORATION_DATE | date (typed) | 1800-01-01 → 2024-09-17 | happened | try_to_date of incorporation; 36 epoch-1970 rows and an 1800-01-01 floor. |

### HEALTH.HEALTH__FED_DEA_ARCOS
| column | format | range | meaning | description |
|---|---|---|---|---|
| TRANSACTION_DATE | date (typed) | 2006-01-01 → 2012-12-31 | happened | try_to_date(trim(TRANSACTION_DATE),'MMDDYYYY') with an explicit format - when the controlled-substance shipment moved; 178.6M rows, the cleanest big event clock in this batch. |

### HEALTH.HEALTH__FED_FDA_CAERS
| column | format | range | meaning | description |
|---|---|---|---|---|
| INITIAL_RECEIVED_DATE | date (typed) | 2001-08-09 → 2025-08-29 | reported | try_to_date 'YYYYMMDD' - when FDA first received the report; the event itself is not dated in this file. |
| LATEST_RECEIVED_DATE | date (typed) | 2001-08-09 → 2025-08-29 | reported | try_to_date 'YYYYMMDD' - when FDA last received a follow-up on the case. |

### HEALTH.HEALTH__FED_FDA_DEVICE_510K
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_RECEIVED | date (typed) | 1976-05-26 → 2026-07-17 | reported | try_to_date 'YYYY-MM-DD' - when the submitter filed the 510(k) with FDA. |
| DECISION_DATE | date (typed) | 1976-07-15 → 2026-07-26 | decided | try_to_date 'YYYY-MM-DD' - when FDA ruled on the clearance; the better anchor for 'devices cleared per year' even though the primary rule prefers date_received. |

### HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT
| column | format | range | meaning | description |
|---|---|---|---|---|
| CENTER_CLASSIFICATION_DATE | date (typed) | 2012-06-08 → 2026-07-23 | decided | try_to_date 'YYYYMMDD' - when FDA's center classified the recall. |
| RECALL_INITIATION_DATE | date (typed) | 1930-12-11 → 2026-07-07 | happened | try_to_date 'YYYYMMDD' - the firm actually started pulling product on this date. |
| REPORT_DATE | date (typed) | 2012-06-20 → 2026-07-29 | reported | try_to_date 'YYYYMMDD' - when the recall appeared in FDA's enforcement report. |
| TERMINATION_DATE | date (typed) | 2012-06-15 → 2026-07-24 | span_end | try_to_date 'YYYYMMDD' - closes the open-recall span. |

### HEALTH.HEALTH__FED_FDA_DEVICE_PMA
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_RECEIVED | date (typed) | 1900-01-01 → 2026-07-17 | reported | try_to_date 'YYYY-MM-DD' - when the PMA application or supplement was filed. |
| DECISION_DATE | date (typed) | 1960-10-14 → 2026-07-26 | decided | try_to_date 'YYYY-MM-DD' - FDA's approval decision; the 1900-01-01 floor and 5 epoch rows are source sentinels. |

### HEALTH.HEALTH__FED_FDA_DRUG_ENFORCEMENT
| column | format | range | meaning | description |
|---|---|---|---|---|
| CENTER_CLASSIFICATION_DATE | date (typed) | 2012-06-11 → 2026-07-16 | decided | try_to_date 'YYYYMMDD' - FDA's classification of the recall. |
| RECALL_INITIATION_DATE | date (typed) | 2006-02-24 → 2026-06-29 | happened | try_to_date 'YYYYMMDD' - when the firm began the drug recall. |
| REPORT_DATE | date (typed) | 2012-06-20 → 2026-07-15 | reported | try_to_date 'YYYYMMDD' - publication in FDA's enforcement report. |
| TERMINATION_DATE | date (typed) | 2012-07-05 → 2026-07-01 | span_end | try_to_date 'YYYYMMDD' - closes the recall span; feeds the model's days-open metric. |

### HEALTH.HEALTH__FED_FDA_DRUG_MASTER_FILES
| column | format | range | meaning | description |
|---|---|---|---|---|
| SUBMIT_DATE | date (typed) | 1939-07-18 → 2026-06-30 | reported | try_to_date 'YYYY-MM-DD HH24:MI:SS' - when the holder submitted the DMF to FDA; 140 rows sit on 1970-01-01. |

### HEALTH.HEALTH__FED_FDA_ESTABLISHMENT_REG
| column | format | range | meaning | description |
|---|---|---|---|---|
| REG_EXPIRY_DATE_YEAR | year only | 2026 → 2026 | span_end | A YEAR string pulled straight from the registration JSON - the year the registration lapses; device registrations renew annually so it is near-constant and weak for trending. |

### HEALTH.HEALTH__FED_FDA_FAERS_DEMO
| column | format | range | meaning | description |
|---|---|---|---|---|
| AGE | quarter | 1704 → 2035 | not_a_date | Patient age, paired with an age-unit code. |
| EVENT_DT | date as text (yyyymmdd) | 1908-07-29 → 2033-10-23 | happened | Date the adverse event occurred, passed through UNCAST; FAERS ships variable-precision YYYY/YYYYMM/YYYYMMDD so many rows resolve only to year. |
| FDA_DT | date as text (yyyymmdd) | 2012-01-06 → 2014-06-30 | reported | Date FDA received this version of the case - uncast text. |
| INIT_FDA_DT | date as text (yyyymmdd) | 1989-12-07 → 2014-06-30 | reported | Date FDA received the INITIAL version of the case - uncast text. |
| MFR_DT | date as text (yyyymmdd) | 1886-01-01 → 2014-06-30 | reported | Date the manufacturer first received the report - uncast text, variable precision. |
| REPT_DT | date as text (yyyymmdd) | 1913-05-03 → 2016-11-14 | reported | Date of the report as filed - uncast text. |
| SRC_QUARTER | quarter | 2004 → 2014 | reported | _SRC_QUARTER is underscore-prefixed like our bookkeeping columns, but its VALUE is FDA's quarterly release - a publication clock, not our load time; worth a value check. |

### HEALTH.HEALTH__FED_FDA_FAERS_DRUG
| column | format | range | meaning | description |
|---|---|---|---|---|
| EXP_DT | month-year | 1915-06-01 → 2025-12-31 | span_end | Drug expiration date on the reported product, uncast; sparsely populated in FAERS. |
| SRC_QUARTER | quarter | 2004 → 2014 | reported | FDA's quarterly release tag - the only usable clock on this 20.9M-row table. |

### HEALTH.HEALTH__FED_FDA_FAERS_INDI
| column | format | range | meaning | description |
|---|---|---|---|---|
| SRC_QUARTER | quarter | 2004 → 2014 | reported | FDA's quarterly release tag - the only time column on this 9.8M-row indication table. |

### HEALTH.HEALTH__FED_FDA_FAERS_OUTC
| column | format | range | meaning | description |
|---|---|---|---|---|
| SRC_QUARTER | quarter | 2004 → 2014 | reported | FDA's quarterly release tag - the only time column here, and part of the dedupe key. |

### HEALTH.HEALTH__FED_FDA_FAERS_REAC
| column | format | range | meaning | description |
|---|---|---|---|---|
| SRC_QUARTER | quarter | 2004 → 2014 | reported | FDA's quarterly release tag - the only time column on 20.6M rows; the header notes a 2004Q1-2012Q3 legacy-layout era, so quarter mix is not uniform. |

### HEALTH.HEALTH__FED_FDA_GUDID
| column | format | range | meaning | description |
|---|---|---|---|---|
| PUBLIC_VERSION_DATE | date (typed) | 2018-03-29 → 2026-04-30 | reported | try_to_date 'YYYY-MM-DD' - date of the current public version of the record. |
| PUBLISH_DATE | date (typed) | 2013-02-20 → 2026-04-22 | reported | try_to_date 'YYYY-MM-DD' - when the device record was published into GUDID. |

### HEALTH.HEALTH__FED_FDA_MAUDE
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_OF_EVENT | date (typed) | 1900-01-01 → 2026-06-04 | happened | try_to_date 'YYYYMMDD' - when the device injured or malfunctioned; the true harm clock, though the 1900-01-01 floor and 1 epoch row need a filter. |
| DATE_RECEIVED | date (typed) | 2020-01-01 → 2021-09-30 | reported | try_to_date 'YYYYMMDD' from a _raw text column - when FDA received the report. |
| DATE_REPORT | date (typed) | 1979-08-06 → 2026-06-30 | reported | try_to_date 'YYYYMMDD' - the date the reporter filed the report. |

### HEALTH.HEALTH__FED_FDA_PURPLE_BOOK
| column | format | range | meaning | description |
|---|---|---|---|---|
| APPROVAL_DATE | date (typed) | 1930-06-14 → 2026-06-05 | decided | try_to_date 'DD-MON-YY' with a -100-year rollback when the 2-digit year parses into the future; FDA's approval of the BLA product row. |
| DATE_OF_FIRST_LICENSURE | date (typed) | 2011-11-18 → 2025-03-05 | decided | Same parse plus rollback - when the biologic was first licensed. |
| FIRST_INTERCHANGEABLE_EXCLUSIVITY_EXP_DATE | date (typed) | 2022-11-15 → 2026-10-22 | span_end | Exclusivity period end, deliberately future-capable. |
| INTERCHANGEABLE_APPROVAL_DATE | date (typed) | 2021-07-28 → 2026-06-05 | decided | Same DD-MON-YY parse plus century rollback - FDA's interchangeability approval. |
| ORPHAN_EXCLUSIVITY_EXP_DATE | date (typed) | 1990-07-20 → 2033-04-23 | span_end | Orphan exclusivity end, future-capable by design. |
| REF_PRODUCT_EXCLUSIVITY_EXP_DATE | date (typed) | 2024-02-29 → 2035-06-22 | span_end | Reference-product exclusivity end, future-capable by design. |

### HEALTH.HEALTH__FED_HHS_OIG_LEIE
| column | format | range | meaning | description |
|---|---|---|---|---|
| EXCLUSION_DATE | date as text (yyyymmdd) | 1977-07-01 → 2026-06-18 | decided | When OIG excluded the provider - but the mart exposes trim(exclusion_date_raw), i.e. RAW 'YYYYMMDD' TEXT, discarding the parsed date staging builds; staging warns a bare CAST collapses all 83,464 rows onto ~7 garbage 1970 dates. |

### HEALTH.HEALTH__FED_HRSA_HPSA_PRIMARY_CARE
| column | format | range | meaning | description |
|---|---|---|---|---|
| DESIGNATION_DATE | date (typed) | 1970-01-01 → 2026-08-05 | decided | try_to_date 'MM/DD/YYYY' - HRSA designating the shortage area. |
| DESIGNATION_LAST_UPDATE_DATE | date (typed) | 1980-04-11 → 2026-08-05 | reported | try_to_date 'MM/DD/YYYY' - HRSA's last touch on the designation record. |
| RECORD_CREATE_DATE | date (typed) | 2026-08-07 → 2026-08-07 | reported | HRSA's own data-warehouse record-create stamp - the publisher's bookkeeping, not a world event and not ours. |
| WITHDRAWN_DATE | date (typed) | 1980-04-11 → 2026-07-01 | decided | try_to_date 'MM/DD/YYYY' - HRSA withdrawing the designation. |

### HEALTH.HEALTH__FED_HRSA_NPDB
| column | format | range | meaning | description |
|---|---|---|---|---|
| AA_EFFECTIVE_YEAR | year only | 1900 → 2029 | span_start | try_to_number(AAEFYEAR) - year the adverse action took effect, the start of the sanction period. |
| AA_SIGNED_YEAR | year only | 1900 → 2026 | decided | try_to_number(AASIGYR) - year the adverse-action order was signed. |
| ADVERSE_ACTION_YEAR | year only | 1944 → 2026 | decided | try_to_number(AAYEAR) - year the licensing or hospital authority took the adverse action. |
| GRAD_YEAR | year only | 1900 → 2020 | happened | try_to_number(GRAD) - year the practitioner graduated; a person attribute, useless as the row's event clock. |
| MALPRACTICE_YEAR_1 | year only | 1900 → 2026 | happened | try_to_number(MALYEAR1) - year of the malpractice incident; only on malpractice-payment reports. |
| MALPRACTICE_YEAR_2 | year only | 1902 → 2025 | happened | try_to_number(MALYEAR2) - year of a second malpractice incident on the same report. |
| ORIG_YEAR | year only | 1990 → 2026 | reported | try_to_number(ORIGYEAR) - year the malpractice/disciplinary report was originally submitted; the only year populated on every row. |

### HEALTH.HEALTH__FED_HRSA_SHORTAGE_AREAS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_WAREHOUSE_RECORD_CREATE_DATE | date (typed) | 2026-06-30 → 2026-06-30 | reported | HRSA's data-warehouse record-create stamp - publisher bookkeeping, must not be read as an event clock. |
| HPSA_DESIGNATION_DATE | date (typed) | 1970-01-01 → 2026-06-26 | decided | try_to_date (bare, from landing) - HRSA designating the shortage area; census 1970-2026 with only 2 epoch rows. |
| HPSA_DESIGNATION_LAST_UPDATE_DATE | date (typed) | 1979-12-14 → 2026-06-29 | reported | try_to_date - HRSA's last touch on the designation record. |
| WITHDRAWN_DATE | date (typed) | 1979-12-14 → 2026-04-07 | decided | try_to_date - HRSA withdrawing the designation. |

### HEALTH.HEALTH__FED_HRSA_UDS_HEALTH_CENTER_INFO
| column | format | range | meaning | description |
|---|---|---|---|---|
| REPORTINGYEAR | year only | 2025 → 2025 | reported | nullif(trim(REPORTINGYEAR)) - TEXT year of the UDS reporting cycle; likely one constant across all 1,356 rows, so it anchors the snapshot but cannot trend. |

### HEALTH.HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES
| column | format | range | meaning | description |
|---|---|---|---|---|
| RECORD_CREATE_DATE | date (typed) | 2026-08-07 → 2026-08-07 | reported | HRSA's data-warehouse record-create stamp - publisher bookkeeping. |
| SITE_ADDED_TO_SCOPE_DATE | date (typed) | 1966-01-01 → 2026-08-06 | decided | try_to_date 'MM/DD/YYYY' of SITE_ADDED_TO_SCOPE_THIS_DATE - HRSA approving the site into scope; readable as 'happened' too, 32 epoch-1970 rows need a filter. |

### HEALTH.HEALTH__FED_NLM_DAILYMED_SPL_SETID_MAP
| column | format | range | meaning | description |
|---|---|---|---|---|
| UPLOAD_DATE | date (typed) | 2006-07-13 → 2026-08-07 | reported | try_to_date on the trimmed value - when the drug label file was uploaded to DailyMed; the 2026 census max is _ingested_at leakage. |

### HEALTH.HEALTH__FED_NURSINGHOME411
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_FIRST_APPROVED_TO_PROVIDE_MEDICARE_AND_MEDICAID_SERVICES | date (typed) | 1967-01-01 → 2025-12-12 | decided | try_to_date (bare) - CMS approving the facility; 153 epoch-1970 rows on this table. |

### HEALTH.HEALTH__FED_VA_ALLCAUSE_MORTALITY
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 2018 → 2023 | happened | try_to_number(trim(YEAR)) in staging - year of veteran death, 2018-2023; the census's 2026 range is _ingested_at leakage. |

### HEALTH.HEALTH__FED_VA_SUICIDE_NATIONAL
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR_OF_DEATH | year only | 2001 → 2023 | happened | try_to_number(trim(YEAR_OF_DEATH)) in staging - the year the veterans died. |

### HEALTH.HEALTH__FED_VA_SUICIDE_STATE
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR_OF_DEATH | year only | 2001 → 2023 | happened | coalesce(try_to_number(YEAR_OF_DEATH), try_to_number(YEAR)) in staging so every row carries a year of death. |

### HEALTH.HEALTH__INTL_HEALTHCANADA_DPD_DRUG
| column | format | range | meaning | description |
|---|---|---|---|---|
| LAST_UPDATE_DATE | date (typed) | 2025-03-22 → 2026-07-31 | reported | try_to_date(C_24_DEC_2025,'DD-MON-YYYY') - the source column name shows the loader ate the header row, and this reads as Health Canada's record-update stamp, not a drug event. |

### HEALTH.HEALTH__PHARMA_MEAL_CAP_FINGERPRINT
| column | format | range | meaning | description |
|---|---|---|---|---|
| PROGRAM_YEAR | year only | 2022 → 2024 | happened | try_to_number(program_year) and half the declared grain key - the Open Payments program year the food-and-beverage payments were made in. |

### HEALTH.HEALTH__ST_OEHHA_PROPOSITION_65_LIST
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_LISTED | date (typed) | 1987-02-27 → 2026-07-17 | decided | try_to_date on the trimmed value (staging notes an explicit MM/DD/YYYY format nulled 100% of rows, so the bare parse is deliberate) - the state listing the chemical; census 1987-2026 is clean. |

### HEALTH.HEALTH__XC_GUTTMACHER_MONTHLY_ABORTION
| column | format | range | meaning | description |
|---|---|---|---|---|
| MONTH | date as text (iso) | 2023-01-15 → 2026-03-15 | happened | Uncast text month key of the monthly abortion estimate - the row's own period; census measured nothing because it is text. |

### HEALTH.HEALTH__XC_OWID_LIFE_EXPECTANCY
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 1703 → 2023 | happened | try_to_number(YEAR) - the year the life-expectancy figure describes. |

### HISTORICAL_RECORDS.HISTORICAL_RECORDS__FED_SLAVEVOYAGES_INTRAAMERICAN
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATEDEPC | year only | 1744 → 1799 | happened | Per the same codebook comment, the YEAR component of the voyage departure date - the only one of the three that stands alone. |
| DATE_BUY1 | date as text (us) | 1788-03-01 → 1788-03-01 | happened | Raw uncast landing column (this mart applies no casts at all); the SlaveVoyages codebook has it as the date slave purchase began, but the stored format and real resolution are unverified with the warehouse down. |
| DATE_LAND1 | date as text (us) | 1700-01-08 → 1841-11-12 | happened | Raw uncast landing column; codebook meaning is the date of arrival at the first place of landing, format unverified. |
| DATE_LAND2 | date as text (us) | 1702-05-01 → 1809-07-31 | happened | Raw uncast landing column; date of arrival at the second place of landing per the codebook, format unverified and sparsely populated by nature. |
| DATE_LEFTAFR | date as text (us) | 1700-01-05 → 1841-10-30 | happened | Raw uncast landing column; codebook meaning is the date the vessel left the African coast, but format and resolution are unverified. |
| YEARAM | year only | 1700 → 1841 | happened | The sibling staging model's codebook comment states 'YEARAM = Year of arrival at port of disembarkation' - the canonical voyage year. In this mart it is a raw uncast landing column. |

### HISTORY.HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATEDEPC | year only | 1700 → 1864 | not_a_date | raw uncast: third component of the split datedep triplet; if any of A/B/C is the year it is most likely this one, but that is a guess - yeardep already carries the year cleanly, so use that instead. |

### HISTORY.HISTORY__FED_WPA_SLAVE_NARRATIVES
| column | format | range | meaning | description |
|---|---|---|---|---|
| INTERVIEW_DATE | date (typed) | 1937-01-01 → 1938-01-01 | happened | try_to_date(interview_date,'YYYY-MM-DD') in staging with an explicit format: when the WPA interview actually took place; census CLEAN with a 1937-01-01 minimum, matching the 1936-38 field programme. |
| INTERVIEW_YEAR | year only | 1937 → 1938 | happened | literally year(interview_date) in the mart - a derived INTEGER year, correct but redundant with interview_date and never to be date-parsed. |

### HOUSING.HOUSING__FED_CFPB_HMDA
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACTIVITY_YEAR | year only | 2022 → 2022 | happened | nullif(trim(ACTIVITY_YEAR),'') keeps it as TEXT year; HMDA's activity year is the calendar year the action on the application was taken. This slice is a single state-year (DC 2023), so the whole table sits on one point. |

### HOUSING.HOUSING__FED_CFPB_HMDA_DC_ONLY
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACTIVITY_YEAR | year only | 2022 → 2022 | happened | Raw ACTIVITY_YEAR passthrough from LANDING with no cast; HMDA's activity year is the calendar year the action was taken. Table is 100% DC, so it is one state on one year. |

### HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC
| column | format | range | meaning | description |
|---|---|---|---|---|
| AS_OF_YEAR | year only | 2015 → 2017 | happened | trim(AS_OF_YEAR) TEXT; schema.yml calls it 'HMDA reporting year (2015, 2016, or 2017 only)' - the year the loan action was taken. Only three distinct values across 19.1M rows. |
| SOURCE_YEAR | year only | 2015 → 2017 | ingest | schema.yml: 'Year of the source file the record was loaded from' - a vintage label for OUR download, not a world event. Mistaking it for a lending clock is exactly the trap this index exists to catch. |

### HOUSING.HOUSING__FED_CFPB_HMDA_LAR
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACTIVITY_YEAR | year only | 2023 → 2023 | happened | try_to_number(trim(ACTIVITY_YEAR)) - a NUMBER year; HMDA's activity year is the calendar year the action was taken. A number, not a date. |

### HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| APPLIED_DATE | date (typed) | 2000-01-15 → 2026-08-05 | reported | try_to_date(trim(APPLIEDDATE)); schema.yml: 'Date the applicant registered for assistance' - the moment a person told FEMA. There is no incident/damage date on this table, so this is the best anchor. |
| CENSUS_YEAR | year only | 2000 → 2020 | not_a_date | trim() TEXT with no date cast - the census vintage used for the row's geographic coding (a reference-geography label), not when anything happened to the applicant. |
| DECLARATION_DATE | date (typed) | 2002-10-24 → 2026-08-03 | decided | try_to_date(trim(DECLARATIONDATE)); schema.yml: 'Date the disaster was declared' - an authority acting, and the same value repeats across every registration under that disaster. |
| RENTAL_ASSISTANCE_END_DATE | date (typed) | 2006-02-28 → 2026-11-30 | span_end | try_to_date(trim(RENTALASSISTANCEENDDATE)) - closes the rental-assistance period for that household; bounds a span rather than marking an event. |

### HOUSING.HOUSING__FED_FEMA_NFIP_COMMUNITY_STATUS_BOOK
| column | format | range | meaning | description |
|---|---|---|---|---|
| CLASS_RATING_EFFECTIVE_DATE | date (typed) | 1991-10-01 → 2026-04-01 |  |  |
| CURRENTLY_EFFECTIVE_MAP_DATE | date (typed) | 1972-05-12 → 2026-12-10 |  |  |
| INITIAL_FLOOD_HAZARD_BOUNDARY_MAP_DATE | date (typed) | 1970-02-08 → 2020-05-29 |  |  |
| INITIAL_FLOOD_INSURANCE_RATE_MAP_DATE | date (typed) | 1970-02-03 → 2026-12-10 |  |  |
| LAST_REFRESH_AT | datetime (typed) | 2026-06-30 15:16:07.336 → 2026-08-07 00:21:05.352 |  |  |
| ORIGINAL_ENTRY_DATE | date (typed) | 1991-10-01 → 2026-04-01 |  |  |
| REGULAR_EMERGENCY_PROGRAM_DATE | date (typed) | 1970-02-03 → 2026-08-05 |  |  |

### HOUSING.HOUSING__FED_FHFA_HPI
| column | format | range | meaning | description |
|---|---|---|---|---|
| YR | year only | 1975 → 2026 | happened | Raw YR passthrough from LANDING with no cast in the mart - the calendar year of the index observation. On its own it is year grain; only `period` plus `frequency` can sharpen it. |

### HOUSING.HOUSING__FED_FHFA_NMDB
| column | format | range | meaning | description |
|---|---|---|---|---|
| PERIOD_VALUE | month-year | 1998 → 2025 | happened | try_to_double(PERIOD_VALUE) - the period the mortgage statistic covers, but its resolution is defined by period_type on the same row, so grain is year or quarter depending. Must be decoded before it can go on a shared axis. |
| RELEASE_DATE | date (typed) | 2026-07-01 → 2026-07-01 | reported | try_to_date(RELEASE_DATE) - when FHFA published the file. The census read min=max=2026-07-01, so it is a single constant and useless as a timeline axis. |

### HOUSING.HOUSING__FED_HUD_DATA
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 2000 → 2000 | happened | try_to_number("YEAR") in the mart - a NUMBER year attached to a value in a scraped HUD dataset listing. The model carries no description and only 77 rows, so what the year refers to may vary row to row; low confidence. |

### HOUSING.HOUSING__FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT
| column | format | range | meaning | description |
|---|---|---|---|---|
| ENDORSEMENT_YEAR | year only | 2026 → 2026 | decided | try_to_number(trim(ENDORSEMENT_YEAR)) - the year FHA endorsed (insured) the loan, i.e. the agency's approval action. A NUMBER year, never date-parse it bare. |

### HOUSING.HOUSING__FED_HUD_MF_FIRM_COMMITMENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| FIRM_ACTIVITY_DATE | date (typed) | 2000-10-02 → 2026-06-30 | decided | coalesce(try_to_date(left(raw,10),'YYYY-MM-DD'), try_to_date(raw,'MM/DD/YYYY')) - the day HUD acted on the multifamily firm commitment; census floor 2000-10-02 matches the stated FY2001 start. |
| FISCAL_YEAR_AT_FIRM_ACTIVITY | year only | 2001 → 2026 | decided | try_to_number(fiscal_year_raw) - the federal FISCAL year of the same action. Fiscal years run Oct-Sep, so laying this on a calendar axis shifts rows by up to a quarter. |

### HOUSING.HOUSING__FED_HUD_MF_SECTION8_CONTRACTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| TRACS_CURRENT_EXPIRATION_DATE | date (typed) | 1900-01-02 → 2035-12-31 | span_end | try_to_date(left(trim(...),10),'YYYY-MM-DD') - the end of the CURRENT contract term, a different span from the overall expiration on the same row. |
| TRACS_EFFECTIVE_DATE | date (typed) | 1977-11-21 → 2027-05-01 | span_start | try_to_date(left(trim(...),10),'YYYY-MM-DD') - the day the Section 8 contract took effect. The table has no happened/reported column, so the span start is the anchor. Census floor 1900-01-02 says some rows carry a sentinel low date. |
| TRACS_OVERALL_EXPIRATION_DATE | date (typed) | 1997-07-31 → 2035-12-31 | span_end | try_to_date(left(trim(...),10),'YYYY-MM-DD') - the outer end of the contract span. 17,283 of 24,309 rows sit past 2030 (max 2056-02-29): plausible for long HAP contracts, but unverified and worth a value check. |
| TRACS_OVERALL_EXP_FISCAL_YEAR | year only | 1997 → 2035 | span_end | try_to_number(trim(...)) - the federal FISCAL year the overall contract expires; a year NUMBER, offset from the calendar year. |

### HOUSING.HOUSING__FED_HUD_PUBLIC_HOUSING_AUTHORITIES
| column | format | range | meaning | description |
|---|---|---|---|---|
| ANNUAL_EXPENSE_AMOUNT_PREV_YR | month-year | 1700 → 2031 |  |  |
| CAPITAL_FUND_AMOUNT_PREV_YR | month-year | 1701 → 2034 |  |  |
| LAST_UPDATED_AT | datetime (typed) | 2025-07-16 22:56:19.000 → 2025-07-16 22:56:19.000 |  |  |
| OPERATING_FUND_AMOUNT_PREV_YR | month-year | 1700 → 2033 |  |  |
| SPENDING_PER_MONTH | year only | 1701 → 2016 |  |  |
| SPENDING_PER_MONTH_PREV_YR | year only | 1708 → 2023 |  |  |

### HOUSING.HOUSING__FED_USDA_RD_MFH_ACTIVE_PROJECTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_OF_OPERATION | date (typed) | 1964-04-29 → 2019-09-11 |  |  |
| DATE_RESTRICTIVE_CLAUSE_EXPIRES | date (typed) | 1944-12-20 → 2035-12-30 |  |  |
| DATE_TAX_CREDIT_EXPIRES | date (typed) | 1933-09-28 → 2035-12-31 |  |  |

### IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| INCORPORATION_DATE | date (typed) | 1848-05-29 → 2024-09-14 | happened | try_to_date of incorporation; 6 epoch-1970 rows and an 1848 floor are sentinels. Note this CMS hospice table is mis-filed under the IMMIGRATION schema. |

### IMMIGRATION.IMMIGRATION__FED_DHS_OHSS
| column | format | range | meaning | description |
|---|---|---|---|---|
| FISCAL_YEAR | year only | 2014 → 2025 | happened | Uncast passthrough of the multi-sheet spreadsheet's fiscal-year label: a federal fiscal year (Oct-Sep), so it is offset about three months from calendar time and must not be aligned as a calendar year. |

### IMMIGRATION.IMMIGRATION__FED_DHS_YEARBOOK
| column | format | range | meaning | description |
|---|---|---|---|---|
| FISCAL_YEAR | year only | 1996 → 2022 | reported | try_to_number in the mart and carries both not_null and unique tests across the 27 rows, so it is a fully populated one-row-per-year key — a federal fiscal year (Oct-Sep), not a calendar year. |
| YEARBOOK_EDITION | year only | 1996 → 2022 | reported | Uncast varchar naming which published edition of the DHS Yearbook a row came from — a publication vintage label, the class the brief explicitly calls out as not a date. |

### IMMIGRATION.IMMIGRATION__FED_DOL_OFLC
| column | format | range | meaning | description |
|---|---|---|---|---|
| DECISION_DATE | date (typed) | 2018-10-01 → 2019-09-30 | decided | try_to_date on DOL's decision date: the day the Office of Foreign Labor Certification ruled on the case, which is this table's own dated event and matches the census range 2012-09-17 to 2023-12-31. |
| ORIGINAL_CERT_DATE | date (typed) | 2014-03-10 → 2019-09-30 | decided | try_to_date: the day the original labor certification was granted, an earlier authority decision carried on amended or extended cases. |
| PERIOD_OF_EMPLOYMENT_END_DATE | date (typed) | 2015-09-16 → 2023-12-31 | span_end | try_to_date: the last day of the certified employment period, the closing bound of that pair. |
| PERIOD_OF_EMPLOYMENT_START_DATE | date (typed) | 2012-09-17 → 2020-03-31 | span_start | try_to_date: the first day of the certified employment period, the opening bound of an explicit start/end pair. |
| PW_NON_OES_YEAR_1 | year only | 1977 → 2020 | not_a_date | Uncast varchar non-OES wage-survey vintage label for worksite 1, same class as pw_oes_year_1. |
| PW_NON_OES_YEAR_2 | year only | 2009 → 2020 | not_a_date | Uncast varchar non-OES wage-survey vintage label for worksite 2. |
| PW_NON_OES_YEAR_3 | year only | 2015 → 2020 | not_a_date | Uncast varchar non-OES wage-survey vintage label for worksite 3. |
| PW_OES_YEAR_1 | year only | 2001 → 2020 | not_a_date | Uncast varchar sitting in worksite 1's prevailing-wage block beside pw_survey_publisher_1 and pw_survey_name_1: the OES wage-survey vintage label (published as a range string like '7/1/2021 - 6/30/2022'), an attribute of the wage source rather than a clock for the case. |
| PW_OES_YEAR_2 | year only | 2008 → 2019 | not_a_date | Uncast varchar OES wage-survey vintage label for worksite 2, one of ten repeated worksite blocks. |
| PW_OES_YEAR_3 | year only | 2013 → 2019 | not_a_date | Uncast varchar OES wage-survey vintage label for worksite 3. |
| PW_OES_YEAR_4 | year only | 2013 → 2019 | not_a_date | Uncast varchar OES wage-survey vintage label for worksite 4. |

### IMMIGRATION.IMMIGRATION__FED_EPA_SDWA_SDWA_SERVICE_AREAS
| column | format | range | meaning | description |
|---|---|---|---|---|
| FIRST_REPORTED_DATE | date (typed) | 2005-10-27 → 2026-06-30 | reported | try_to_date(FIRST_REPORTED_DATE): the day the state first submitted this water-system service-area row. A link table with no event of its own, so the reporting clock is all there is. (An environment table living in the IMMIGRATION schema.) |
| LAST_REPORTED_DATE | date (typed) | 1995-07-22 → 2026-06-30 | reported | try_to_date(LAST_REPORTED_DATE): most recent re-submission of the service-area row. |
| SUBMISSIONYEARQUARTER | quarter | 2026 → 2026 | reported | Raw passthrough of SUBMISSIONYEARQUARTER (no cast): the YYYYQn SDWIS federal-reporting cycle in which the state submitted this row. A submission label, not an event - quarter grain, never date-parse it. |

### IMMIGRATION.IMMIGRATION__FED_ICE_DETAINERS
| column | format | range | meaning | description |
|---|---|---|---|---|
| APPREHENSION_AT | datetime (typed) | 1989-09-25 00:00:00.000 → 2027-01-12 19:40:04.000 |  |  |
| BIRTH_YEAR | year only | 1903 → 2025 | happened | try_to_number on the anonymized birth year: a real event at year grain but a demographic attribute of the person, never the record's clock. |
| DETAINER_PREPARE_DATE | date (typed) | 2022-10-01 → 2026-08-25 | decided | try_to_date on the date ICE prepared the detainer — the enforcement action this table is one-row-per, and the staging header warns some prepare dates run slightly past the publication date as landed. |
| ENTRY_DATE | date (typed) | 1921-03-15 → 2026-03-11 | happened | try_to_date (no format) on the person's date of entry to the US — a real-world event, but a life-history attribute rather than the detainer's own date, and the likely source of the census's 1919-07-12 floor. |
| FINAL_ORDER_DATE | date (typed) | 1919-07-12 → 2026-03-10 | decided | try_to_date on the date a final order of removal was issued — an authority ruling, and the outcome half of the detainer story. |
| MSC_CHARGE_DATE | date (typed) | 1931-05-01 → 2026-03-09 | reported | try_to_date on the most-serious-conviction charge date: when charges were filed, which is later than the underlying offence and must never be read as the offence date. |
| MSC_CONVICTION_DATE | date (typed) | 1968-06-14 → 2026-03-09 | decided | try_to_date on the date a court convicted the person of the most serious charge — an adjudication, and prior history rather than this row's event. |

### IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| BIRTH_YEAR | year only | 1930 → 2025 | happened | try_to_number on the anonymized birth year: a demographic attribute of the person at year grain, not the stint's clock. |
| BOOK_IN_AT | datetime (typed) | 2004-12-05 22:30:00.000 → 2026-03-11 00:30:00.000 |  |  |
| BOOK_OUT_AT | datetime (typed) | 2022-10-01 01:25:00.000 → 2026-03-11 00:27:00.000 |  |  |
| ENTRY_DATE | date (typed) | 1916-12-26 → 2026-03-11 | happened | try_to_date on the person's US entry date, a life-history event and the likely source of the census's 1919-07-12 floor. |
| MSC_CHARGE_DATE | date (typed) | 1923-02-19 → 2027-02-01 | reported | try_to_date on the date charges were filed for the most serious conviction, later than the offence itself. |
| MSC_CONVICTION_DATE | date (typed) | 1966-11-09 → 2026-03-10 | decided | try_to_date on the court's conviction date for the most serious charge — an adjudication in the person's prior history. |
| STAY_BOOK_IN_AT | datetime (typed) | 2004-12-05 22:30:00.000 → 2026-03-11 00:30:00.000 |  |  |
| STAY_BOOK_OUT_AT | datetime (typed) | 2022-10-01 05:40:00.000 → 2026-03-11 00:22:00.000 |  |  |
| STAY_BOOK_OUT_DATE | date (typed) | 2022-10-01 → 2026-03-11 | span_end | try_to_date on the date the person was booked out of the detention stay — the closing bound of the stint, chosen as primary only because the candidate list omitted the book-IN timestamps that actually open the span; the staging header notes some book-outs are future-dated scheduled releases, which is the census's 2027-02-01 max. |

### IMMIGRATION.IMMIGRATION__FED_ICE_STATISTICS
| column | format | range | meaning | description |
|---|---|---|---|---|
| FISCAL_YEAR | year only | 1986 → 1986 | not_a_date | try_to_number in the mart: the federal fiscal year (Oct-Sep) the published ICE counts cover, and the only column that can place these 221 aggregate rows on a timeline. |
| SNAPSHOT_DATE | date (typed) | 2026-07-02 → 2026-07-02 | ingest | try_to_date on a value the census measured as identical across every row (min = max = 2026-07-02), i.e. the single scrape/snapshot stamp for the whole file — it carries zero within-table time signal and the dedup note shows 18 blank placeholder rows sharing it. |

### IMMIGRATION.IMMIGRATION__XC_OWID_REFUGEES
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 1951 → 2024 | happened | try_to_number in the mart and part of the model's unique combination (entity, year, code): the calendar year the refugee population was measured, and the table's only clock. |

### INVESTIGATIONS.INVESTIGATIONS__INTL_LEIDEN_RUSSIAN_OPS_EUROPE
| column | format | range | meaning | description |
|---|---|---|---|---|
| INCIDENTDATEEND | date as text (iso) | 2022-08-30 → 2025-12-31 | span_end | Closes the incident window; equals the start for single-day incidents; uncast raw passthrough. |
| INCIDENTDATESTART | date as text (iso) | 2022-01-01 → 2025-10-01 | unclear | Opens the window in which the incident occurred - the finest real clock on this 153-row table (incidentyear is only year grain); uncast raw passthrough, so the stored format is unverified. |
| INCIDENTYEAR | year only | 2022 → 2025 | unclear | Year the incident occurred - a raw uncast passthrough year value, coarser than the start/end pair on the same row. |

### INVESTIGATIONS.INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_DEEP_PAGES
| column | format | range | meaning | description |
|---|---|---|---|---|
| CAPTURED_AT | datetime (typed) | 2026-02-15 14:31:21.000 → 2026-06-04 07:26:55.000 |  |  |

### INVESTIGATIONS.INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_LISTING
| column | format | range | meaning | description |
|---|---|---|---|---|
| CAPTURED_AT | datetime (typed) | 2025-12-19 21:13:27.000 → 2026-06-03 04:27:34.000 |  |  |

### JUDICIARY.JUDICIARY__FED_OYEZ
| column | format | range | meaning | description |
|---|---|---|---|---|
| ARGUMENT_DATE | date (typed) | 1971-10-19 → 1972-04-20 | decided | try_to_date(ARGUMENT_DATE) in staging: when oral argument was heard - a court proceeding (the authority acting) that precedes the ruling, not a real-world harm event; census min 1966-01-17 comes from this or decision_date. |
| DATE | date (typed) | 1966-01-17 → 1973-01-22 | decided | a straight alias of decision_date in the mart (select decision_date as date) - a duplicate column kept as the cross-source join name, so it must not be counted as a second clock. |
| DECISION_DATE | date (typed) | 1966-01-17 → 1973-01-22 | decided | try_to_date(DECISION_DATE) in staging: when the Court handed down its ruling - the mart itself aliases this very column as the canonical 'date' for cross-source joins, so it is the table's own chosen anchor. |
| TERM | year only | 1966 → 1971 | decided | try_to_number(TERM) in staging: the SCOTUS term year as an integer, and a term runs October to June so the label is not a calendar year - year grain at best, and never date-parse it. |

### JUSTICE.JUSTICE__COUNTY_DOUBLE_BURDEN
| column | format | range | meaning | description |
|---|---|---|---|---|
| JAIL_RATE_YEAR | year only | 1970 → 2024 | happened | The compiled mart selects j.jail_year (Vera county-year panel year) as jail_rate_year -- the year the jail-rate measurement refers to. |

### JUSTICE.JUSTICE__FED_BOP_STATISTICS
| column | format | range | meaning | description |
|---|---|---|---|---|
| REPORT_DATE | date (typed) | 2026-07-01 → 2026-07-01 |  |  |

### JUSTICE.JUSTICE__FED_CISA_KEV
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_ADDED | date (typed) | 2021-11-03 → 2026-07-01 | decided | try_to_date(DATE_ADDED): the date CISA added the vulnerability to the Known Exploited Vulnerabilities catalog -- an agency designation act. |
| DUE_DATE | date (typed) | 2021-11-17 → 2026-07-04 | span_end | try_to_date(DUE_DATE): the federal remediation deadline; it closes the required-action window that date_added opens, so it bounds a period rather than marking an event. |

### JUSTICE.JUSTICE__FED_CONSOLIDATED_SCREENING_LIST
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATES_OF_BIRTH | date as text (iso) | 1921-05-06 → 2006-01-01 | not_a_date | Staging keeps it as nullif(trim(DATES_OF_BIRTH),'') raw text and the name is plural -- a multi-valued DOB string, never cast to a date. |
| END_DATE | date (typed) | 2000-04-04 → 2035-03-13 | span_end | try_to_date(nullif(trim(END_DATE),'')) -- the close of the entry's in-force period; the census's 129 far-future rows are genuine future expiry dates, not corruption. |
| START_DATE | date (typed) | 1974-11-17 → 2026-03-26 | span_start | Staging casts try_to_date(nullif(trim(START_DATE),'')); paired with END_DATE it bounds the period the screening-list entry is in force. |

### JUSTICE.JUSTICE__FED_COURTLISTENER_CITATIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_CREATED | date (typed) | 2025-09-26 → 2026-06-30 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. Its 2025-09-26 floor is when CourtListener built these citation rows, not when anything was cited. |
| DATE_MODIFIED | date (typed) | 2025-09-26 → 2026-06-30 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |

### JUSTICE.JUSTICE__FED_COURTLISTENER_COURTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_MODIFIED | date (typed) | 2013-08-14 → 2026-06-12 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| END_DATE | date (typed) | 1776-07-03 → 2012-09-15 | span_end | try_to_date(END_DATE): when the court ceased to exist; null for courts still operating. |
| START_DATE | date (typed) | 1701-01-01 → 2023-06-09 | span_start | try_to_date(START_DATE) on a court record: the date the court was established, paired with END_DATE (abolished) -- a period, not a point. The census's 1200-01-01 floor is a historical/placeholder founding date, not an epoch artefact. |

### JUSTICE.JUSTICE__FED_COURTLISTENER_DISCLOSURE_AGREEMENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_CREATED | date (typed) | 2021-01-03 → 2023-08-31 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_MODIFIED | date (typed) | 2021-01-03 → 2024-11-11 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_RAW | year only | 1981-01-01 → 2021-10-01 | not_a_date | The model's own comment (BUG FIXED 2026-08-18) documents DATE_RAW as CourtListener's as-extracted OCR text off scanned financial-disclosure PDFs, now passed through as text; the census's epoch-1970 count for this table is the old bare try_to_date(). |

### JUSTICE.JUSTICE__FED_COURTLISTENER_DISCLOSURE_DEBTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_CREATED | date (typed) | 2021-01-03 → 2023-08-31 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_MODIFIED | date (typed) | 2021-01-03 → 2025-02-05 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |

### JUSTICE.JUSTICE__FED_COURTLISTENER_DISCLOSURE_GIFTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_CREATED | date (typed) | 2021-01-04 → 2023-08-31 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_MODIFIED | date (typed) | 2021-01-04 → 2023-08-31 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |

### JUSTICE.JUSTICE__FED_COURTLISTENER_DISCLOSURE_NON_INVESTMENT_INCOME
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_CREATED | date (typed) | 2021-01-03 → 2023-08-31 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_MODIFIED | date (typed) | 2021-01-03 → 2023-08-31 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_RAW | year only | 2005-01-30 → 2022-12-20 | not_a_date | The model's own comment (BUG FIXED 2026-08-18) documents DATE_RAW as CourtListener's as-extracted OCR text off scanned financial-disclosure PDFs, now passed through as text; the census's epoch-1970 count for this table is the old bare try_to_date(). |

### JUSTICE.JUSTICE__FED_COURTLISTENER_DISCLOSURE_POSITIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_CREATED | date (typed) | 2021-01-03 → 2023-08-31 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_MODIFIED | date (typed) | 2021-01-03 → 2023-08-31 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |

### JUSTICE.JUSTICE__FED_COURTLISTENER_DISCLOSURE_REIMBURSEMENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_CREATED | date (typed) | 2021-01-03 → 2023-08-31 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_MODIFIED | date (typed) | 2021-01-03 → 2023-08-31 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_RAW | date (typed) | 1970-01-01 → 2030-11-06 | not_a_date | DATE_RAW across this whole disclosure family is CourtListener's as-extracted OCR text off scanned PDFs (confirmed samples in the sibling models: 'See VIII', "'84-presnt", '1987-2002'). LIVE BUG: unlike its siblings this model still wraps it in try_to_date(), which is what produced the census's 599 epoch-1970 rows and 45 far-future rows (max 3201-04-14). |

### JUSTICE.JUSTICE__FED_COURTLISTENER_DISCLOSURE_SPOUSAL_INCOME
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_CREATED | date (typed) | 2021-01-03 → 2023-08-31 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_MODIFIED | date (typed) | 2021-01-03 → 2023-08-31 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_RAW | year only | 2000-05-12 → 2021-02-22 | not_a_date | The model's own comment (BUG FIXED 2026-08-18) documents DATE_RAW as CourtListener's as-extracted OCR text off scanned financial-disclosure PDFs, now passed through as text; the census's epoch-1970 count for this table is the old bare try_to_date(). |

### JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_ARGUED | date (typed) | 1802-01-08 → 2026-06-26 | happened | try_to_date(DATE_ARGUED): the day oral argument actually took place. |
| DATE_CERT_DENIED | date (typed) | 1925-08-03 → 2011-09-22 | decided | try_to_date(DATE_CERT_DENIED): the date certiorari was denied -- an authority ruling. |
| DATE_CERT_GRANTED | date (typed) | 1941-10-07 → 2007-10-15 | decided | try_to_date(DATE_CERT_GRANTED): the date certiorari was granted -- an authority ruling. |
| DATE_CREATED | date (typed) | 2014-10-30 → 2026-06-30 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_FILED | date (typed) | 1871-10-12 → 2030-01-28 | reported | try_to_date(DATE_FILED): when the case was filed with the court. Chosen as primary because it is the only case-level date populated across the whole 71.7M-row docket universe; the 'happened' candidates (argument dates) exist on a tiny minority of dockets. |
| DATE_LAST_FILING | date (typed) | 1918-08-20 → 2030-12-29 | reported | try_to_date(DATE_LAST_FILING): the date of the most recent document filed on the docket. |
| DATE_MODIFIED | date (typed) | 2014-10-30 → 2026-06-30 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_REARGUED | date (typed) | 1870-01-10 → 2016-03-05 | happened | try_to_date(DATE_REARGUED): the day the case was reargued. |
| DATE_REARGUMENT_DENIED | date (typed) | 1842-03-26 → 2020-12-19 | decided | try_to_date(DATE_REARGUMENT_DENIED): the court's refusal to rehear -- a ruling. |
| DATE_TERMINATED | date (typed) | 1899-12-31 → 2029-11-18 | decided | try_to_date(DATE_TERMINATED): when the court closed the case. |
| IA_DATE_FIRST_CHANGE | date (typed) | 2018-01-01 → 2026-06-30 | ingest | try_to_date(IA_DATE_FIRST_CHANGE): part of the Internet Archive upload block (ia_needs_upload, ia_upload_failure_count) -- archival plumbing, not a case event. |

### JUSTICE.JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_CREATED | date (typed) | 1970-01-01 → 2023-08-31 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_MODIFIED | date (typed) | 1970-01-01 → 2024-11-15 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| YEAR_COL | year only | 1700 → 2022 | span_start | try_to_number("YEAR") -- the calendar year the disclosure report covers, so it opens a one-year reporting period. Stored as a NUMBER: a bare date-parse would read '2019' as epoch seconds and dump every row on 1970-01-01. |

### JUSTICE.JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED
| column | format | range | meaning | description |
|---|---|---|---|---|
| AMOUNT_RECEIVED | year only | 1700 → 2035 | not_a_date | try_to_double(AMOUNT_RECEIVED) -- a dollar figure. It only matched because of the word 'received'. |
| DATE_CREATED | date (typed) | 2017-09-17 → 2022-06-03 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_FILED | date (typed) | 1901-01-01 → 2022-03-31 | reported | try_to_date(DATE_FILED): when the case was filed with the district court -- the only date populated on every linked IDB record, so it is the timeline anchor. |
| DATE_MODIFIED | date (typed) | 2017-09-17 → 2022-06-03 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_TERMINATED | date (typed) | 1973-03-28 → 2022-03-31 | decided | try_to_date(DATE_TERMINATED): when the court terminated the case. |
| DATE_TRANSFER | date (typed) | 1931-01-01 → 2031-01-01 | decided | try_to_date(DATE_TRANSFER): the date the case was transferred between courts -- a court-ordered action. |
| YEAR_OF_TAPE | year only | 1988 → 2022 | not_a_date | YEAR_OF_TAPE passes through as raw text: the FJC data-tape (annual release) the record came from -- a snapshot/vintage label about the data release, not about the case. |

### JUSTICE.JUSTICE__FED_COURTLISTENER_INVESTMENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_CREATED | date (typed) | 2020-12-31 → 2023-08-31 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_MODIFIED | date (typed) | 2020-12-31 → 2025-02-05 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| TRANSACTION_DATE | date (typed) | 1969-12-31 → 2022-12-27 | happened | try_to_date(TRANSACTION_DATE) -- the clean, already-working sibling of the OCR column per the model's comment: when the judge's reported trade actually occurred. |
| TRANSACTION_DATE_RAW | month-year | 1720-01-12 → 2020-12-22 | not_a_date | The model's own comment documents TRANSACTION_DATE_RAW as CourtListener's OCR text off scanned PDFs ('04/01/20', garbled fragments); a bare try_to_date() epoch-mangled 57,859 of 57,860 rows, which is exactly the census's epoch1970 count for this table. |
| TRANSACTION_DURING_REPORTING_PERIOD | year only | 1720 → 2008 | not_a_date | Raw passthrough text/flag saying whether (and what kind of) a transaction occurred in the period -- not a date. |

### JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGES
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_COMPLETED | date (typed) | 2020-12-23 → 2022-08-09 | ingest | try_to_date(DATE_COMPLETED): when CourtListener finished compiling this judge record -- data-entry bookkeeping, not a life or career event. |
| DATE_CREATED | date (typed) | 2016-04-20 → 2025-05-14 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_DOB | date (typed) | 1707-01-01 → 1999-12-14 | happened | try_to_date(DATE_DOB): the judge's date of birth -- the only real-world event on a person row, so it is the timeline anchor for this table. |
| DATE_DOD | date (typed) | 1764-01-01 → 2023-12-01 | happened | try_to_date(DATE_DOD): the judge's date of death. |
| DATE_MODIFIED | date (typed) | 2016-04-26 → 2026-06-24 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| FTM_TOTAL_RECEIVED | month-year | 2030 → 2030 | not_a_date | FollowTheMoney total dollars received -- a money amount; it only matched on 'received'. |
| IS_ALIAS_OF_ID | quarter | 1810 → 1810 | not_a_date | A self-referencing record ID pointing at the canonical judge row -- an identifier, not a date. |

### JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGE_EDUCATIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_CREATED | date (typed) | 2016-04-20 → 2023-11-08 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_MODIFIED | date (typed) | 2016-04-20 → 2023-11-08 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DEGREE_YEAR | year only | 1751 → 2023 | happened | DEGREE_YEAR passes through as raw text: the year the degree was awarded. Year grain only, and it is a bare year string, so it must never be handed to a plain date-parse. |

### JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_CREATED | date (typed) | 2016-04-20 → 2022-08-09 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_END | date (typed) | 1806-02-21 → 2017-04-09 | span_end | try_to_date(DATE_END): when the affiliation ended. |
| DATE_MODIFIED | date (typed) | 2016-04-20 → 2022-08-09 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_START | date (typed) | 1798-04-11 → 2022-03-30 | span_start | try_to_date(DATE_START): when the judge's affiliation with that party began -- paired with DATE_END it is a tenure span. |

### JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_BLOCKED | date (typed) | 2010-07-20 → 2026-06-30 | ingest | When CourtListener flagged the cluster to be hidden from search engines -- aggregator site administration. |
| DATE_CREATED | date (typed) | 2014-10-30 → 2026-06-30 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_FILED | date (typed) | 1700-05-08 → 2028-04-13 | decided | try_to_date(DATE_FILED): the day the opinion was handed down by the court. The model's comment records that the ~49,791 rows landing in 1970 are real 1970 opinions, not sentinel garbage -- so the census's epoch count here is NOT corruption. |
| DATE_MODIFIED | date (typed) | 2014-10-30 → 2026-06-30 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| OTHER_DATES | date (typed) | 1947-09-25 → 2017-09-22 | not_a_date | A plural free-text field of miscellaneous case dates ('argued...; decided...') wrapped in try_to_date(); it is prose, not a single point in time. |

### JUSTICE.JUSTICE__FED_COURTLISTENER_ORAL_ARGUMENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_BLOCKED | date (typed) | 2015-10-11 → 2026-03-04 | ingest | When CourtListener flagged the recording to be hidden from search engines -- site administration. |
| DATE_CREATED | date (typed) | 2014-10-31 → 2026-06-26 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. The census's 2014-2026 range for this table is this column. |
| DATE_MODIFIED | date (typed) | 2019-07-19 → 2026-06-26 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DURATION | year only | 1700 → 2035 | not_a_date | try_to_double(DURATION) -- the length of the audio recording in seconds. A duration, not a date. |

### JUSTICE.JUSTICE__FED_COURTLISTENER_ORIGINATING_COURT_INFO
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_CREATED | date (typed) | 2018-06-27 → 2026-06-30 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_DISPOSED | date (typed) | 1975-07-01 → 2026-05-13 | decided | try_to_date(DATE_DISPOSED): when the originating court disposed of the case. |
| DATE_FILED | date (typed) | 1951-01-25 → 2029-09-09 | reported | try_to_date(DATE_FILED): when the case was filed in the originating (district) court -- the anchor date present on the broadest slice of rows. |
| DATE_FILED_NOA | date (typed) | 1935-09-26 → 2029-09-18 | reported | try_to_date(DATE_FILED_NOA): when the notice of appeal was filed by a party. |
| DATE_JUDGMENT | date (typed) | 1971-08-08 → 2030-09-06 | decided | try_to_date(DATE_JUDGMENT): when the lower court entered judgment. |
| DATE_JUDGMENT_EOD | date (typed) | 1985-06-26 → 2026-12-19 | decided | try_to_date(DATE_JUDGMENT_EOD): judgment entered-on-docket date -- the clerk recording the court's own ruling. |
| DATE_MODIFIED | date (typed) | 2018-06-27 → 2026-06-30 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_RECEIVED_COA | date (typed) | 1984-05-23 → 2030-06-25 | reported | try_to_date(DATE_RECEIVED_COA): when the court of appeals received the case -- a receipt date. |

### JUSTICE.JUSTICE__FED_COURTLISTENER_POSITIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_CONFIRMATION | date (typed) | 1789-09-25 → 2022-05-18 | decided | try_to_date(DATE_CONFIRMATION): the day the Senate confirmed the appointment. |
| DATE_CREATED | date (typed) | 2016-04-20 → 2025-05-21 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_ELECTED | date (typed) | 1980-11-04 → 2022-11-08 | happened | try_to_date(DATE_ELECTED): the day the judge was elected to the seat -- an election event. |
| DATE_HEARING | date (typed) | 1983-02-23 → 2022-02-16 | happened | try_to_date(DATE_HEARING): the day the confirmation hearing took place. |
| DATE_JUDICIAL_COMMITTEE_ACTION | date (typed) | 1826-05-22 → 2022-07-19 | decided | try_to_date(...): the day the committee acted on the nomination (paired with judicial_committee_action naming what it did). |
| DATE_MODIFIED | date (typed) | 2016-04-20 → 2025-06-16 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_NOMINATED | date (typed) | 1789-09-24 → 2023-02-01 | decided | try_to_date(DATE_NOMINATED): the day the appointing authority (usually the President) nominated the person. |
| DATE_RECESS_APPOINTMENT | date (typed) | 1789-11-18 → 2026-12-31 | decided | try_to_date(DATE_RECESS_APPOINTMENT): the day a recess appointment was made -- an executive act. |
| DATE_REFERRED_TO_JUDICIAL_COMMITTEE | date (typed) | 1826-05-08 → 2021-04-19 | decided | try_to_date(...): the day the Senate referred the nomination to committee -- an authority acting. |
| DATE_START | date (typed) | 1742-01-01 → 2024-12-31 | span_start | try_to_date(DATE_START): when the person actually took the seat. Chosen as primary over the 'happened' candidates because a position row IS a tenure, and date_start is the field populated across the file while hearing/election dates are sparse. |
| DATE_TERMINATION | date (typed) | 1750-01-01 → 2035-12-31 | span_end | try_to_date(DATE_TERMINATION): when the tenure ended; paired with TERMINATION_REASON. |

### JUSTICE.JUSTICE__FED_COURTLISTENER_SCHOOLS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_CREATED | date (typed) | 2010-06-08 → 2022-08-09 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| DATE_MODIFIED | date (typed) | 2010-06-08 → 2025-06-16 | ingest | CourtListener's own row bookkeeping (when the aggregator's database created/last-touched the row), not a real-world event; same class as our ingest stamps. |
| IS_ALIAS_OF_ID | year only | 1707 → 2019 | not_a_date | A self-referencing school record ID -- an identifier, not a date. |

### JUSTICE.JUSTICE__FED_DOJ_FCA_SETTLEMENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| FISCAL_YEAR | year only | 2023 → 2026 | decided | try_to_number(trim(FISCAL_YEAR)) -- DOJ's fiscal year for the same settlement, a coarse duplicate of settlement_date. It is a NUMBER: a bare date-parse would read '2019' as epoch seconds and collapse every row onto 1970-01-01. |

### JUSTICE.JUSTICE__FED_FBI_CDE
| column | format | range | meaning | description |
|---|---|---|---|---|
| MONTH_DATE | date (typed) | 1985-01-01 → 2023-12-01 | happened | Staging: try_to_date(trim(MONTH),'MM-YYYY') with the day defaulting to the 1st -- the month the offenses/clearances were counted in. Month grain only; the day component is manufactured. |

### JUSTICE.JUSTICE__FED_FBI_NICS_CHECKS
| column | format | range | meaning | description |
|---|---|---|---|---|
| MONTH | month-year | 1998 → 2023 | happened | "MONTH" is a raw text passthrough (no cast in either the mart or the minimal staging view); the file is a state x month panel of background checks, so it marks the month the checks were run. Format not verifiable with the warehouse down. |

### JUSTICE.JUSTICE__FED_FHFA_SUSPENDED_COUNTERPARTIES
| column | format | range | meaning | description |
|---|---|---|---|---|
| EFFECTIVE_DATE | date (typed) | 2013-04-15 → 2026-07-29 | span_start | try_to_date(EFFECTIVE_DATESORT_ASCENDING): the day the suspension order takes effect -- the opening bound of the ban period. |
| SUSPENSION_END_DATE | date (typed) | 2026-08-26 → 2033-03-08 | span_end | try_to_date(SUSPENSION_END_DATE): the close of the ban. The mart's own header records that most rows read 'Indefinite' and go NULL after the cast; the census's 13 far-future rows are real future end dates. |

### JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
| column | format | range | meaning | description |
|---|---|---|---|---|
| APPEAL_DATE | date (typed) | 1900-01-01 → 2026-03-31 | reported | try_to_date(trim(APPDATE)): when the appeal was taken/filed below. |
| BRIEFS_FILED | date as text (us) | 1900-01-01 → 2026-03-23 | not_a_date | trim(BRFILED) -- a code/flag for whether briefs were filed, passed through as text with no date cast. |
| COURT_RECORD_DATE | date (typed) | 1900-01-01 → 1900-01-01 | reported | try_to_date(trim(CRECDATE)): when the record was received from the court below -- a receipt date. |
| DISTRICT_DOCKET_DATE | date (typed) | 1900-01-01 → 2026-03-20 | reported | try_to_date(trim(DDKTDATE)): when the underlying case was docketed in the district court. |
| DOCKET_DATE | date (typed) | 1967-02-06 → 2026-03-31 | reported | try_to_date(trim(DKTDATE)): when the appeal was docketed in the court of appeals. Primary because it is part of the source's exactly-unique key, so it is populated on every row, while hearing/submission dates exist only for a minority of appeals. |
| HEARING_DATE | date (typed) | 1900-01-01 → 2026-03-31 | happened | try_to_date(trim(HEARDATE)): the day oral argument was heard. |
| JUDGMENT_DATE | date (typed) | 1900-01-01 → 2026-03-31 | decided | try_to_date(trim(JUDGDATE)): the day the court of appeals entered judgment. |
| SUBMISSION_DATE | date (typed) | 1900-01-01 → 2026-03-31 | happened | try_to_date(trim(SUBDATE)): the day the case was submitted to the panel -- a proceeding, not a party filing. |
| TAPE_YEAR | year only | 2008 → 2026 | not_a_date | trim(TAPEYEAR) raw text -- which annual FJC data tape (release) the record came from. A snapshot/vintage label about the data release, not about the appeal. |
| TRANSFER_DATE | date (typed) | 1900-01-01 → 2013-10-29 | decided | try_to_date(trim(TRANSDATE)), paired with TRANSCODE: the day the case was transferred -- a court-ordered action. |

### JUSTICE.JUSTICE__FED_FJC_IDB_BANKRUPTCY
| column | format | range | meaning | description |
|---|---|---|---|---|
| AVG_MONTHLY_EXPENSES | year only | 1700 → 2035 | not_a_date | try_to_number(trim(AVGMNTHE)) -- a dollar amount per month, not a date. |
| AVG_MONTHLY_INCOME | year only | 1700 → 2035 | not_a_date | try_to_number(trim(AVGMNTHI)) -- a dollar amount per month, not a date. |
| CLOSE_DATE | date (typed) | 2020-10-01 → 2026-04-15 | decided | try_to_date(trim(CLOSEDT)): the day the court closed the case. |
| DEBTOR1_CHANGE_DATE | date (typed) | 2006-10-15 → 2026-04-08 | reported | try_to_date(trim(D1CHGDT)) in the debtor block -- the date debtor 1's record (name/address) was changed on the court's file. Read as 'when the change was recorded'; the codebook meaning is not documented in this repo. |
| DEBTOR2_CHANGE_DATE | date (typed) | 2006-10-17 → 2026-04-08 | reported | try_to_date(trim(D2CHGDT)) -- same as debtor1_change_date for the second debtor. |
| FILE_DATE | date (typed) | 1950-06-03 → 2026-03-31 | reported | try_to_date(trim(FILEDATE)): the filing date for this snapshot of the case -- the anchor date, populated on every row of the 7.0M-row file. |
| FILING_CALENDAR_YEAR | year only | 1950 → 2026 | reported | trim(FILECY) raw text -- the calendar year of the filing, a coarse duplicate of file_date. A bare year string: never hand it to a plain date-parse. |
| FILING_FISCAL_YEAR | year only | 1950 → 2026 | reported | trim(FILEFY) raw text -- the federal FISCAL year of the filing (Oct-Sep), so it does not line up with the calendar year. |
| ORIGINAL_FILING_DATE | date (typed) | 1923-08-25 → 2026-03-31 | reported | try_to_date(trim(ORGFLDT)): when the petition was originally filed with the bankruptcy court. |

### JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
| column | format | range | meaning | description |
|---|---|---|---|---|
| AMOUNT_RECEIVED | year only | 1700 → 2035 | not_a_date | try_to_number(trim(AMTREC)) -- a dollar amount awarded/received; it matched only on 'received'. |
| FILE_DATE | date (typed) | 1901-01-01 → 2026-03-31 | reported | try_to_date(trim(FILEDATE)): when the civil case was filed. Primary because it is part of the near-unique natural key, so it is populated across all 10.9M rows. |
| FILE_DATE_USE | date as text (us) | 1901-01-01 → 2026-03-01 | not_a_date | trim(FDATEUSE) -- FJC's code describing how the filing date should be used/interpreted; a code, no date cast. |
| ISSUE_JOINED_DATE | date (typed) | 1900-05-21 → 2035-05-21 | reported | try_to_date(trim(DJOINED)): the date issue was joined (the answer filed) -- a party filing with the court. |
| PRETRIAL_DATE | date (typed) | 1909-09-07 → 2026-03-31 | happened | try_to_date(trim(PRETRIAL)): the date of the pretrial conference -- a proceeding that took place. |
| TAPE_YEAR | year only | 1988 → 2026 | not_a_date | trim(TAPEYEAR) raw text -- which annual FJC release the record came from; a snapshot/vintage label, not a case event. |
| TERM_DATE | date (typed) | 1900-01-01 → 2026-03-31 | decided | try_to_date(trim(TERMDATE)): the day the court terminated the case. |
| TERM_DATE_USE | date as text (us) | 1987-07-01 → 2026-03-01 | not_a_date | trim(TDATEUSE) -- FJC's code describing how the termination date should be used; a code, no date cast. |
| TRANSFER_DATE | date (typed) | 1931-01-01 → 2031-01-01 | decided | try_to_date(trim(TRANSDAT)): the day the case was transferred to another court -- a court-ordered action. |

### JUSTICE.JUSTICE__FED_FJC_IDB_CRIMINAL
| column | format | range | meaning | description |
|---|---|---|---|---|
| APP_DATE | date (typed) | 1900-01-01 → 2026-04-10 | decided | try_to_date(trim(APPDATE)), paired with APPCD (appeal code): read as the date of the appellate action. The codebook meaning is not documented in this repo, so the clock is a reasoned guess. |
| C_UPDATE | date as text (us) | 1900-01-01 → 2012-02-13 | not_a_date | trim(C_UPDATE) sits in the geography/transfer block and is passed through as raw text with no date cast; its meaning is undocumented here. Treated as not-a-date because nothing in the model treats it as one. |
| DISPOSITION_DATE | date (typed) | 1900-01-01 → 2026-03-31 | decided | try_to_date(trim(DISPDATE)): the day the charge was disposed of -- an adjudication. |
| FILE_DATE | date (typed) | 1904-03-23 → 2026-04-01 | reported | try_to_date(trim(FILEDATE)): when the criminal case was filed against the defendant. Primary: the anchor populated across the 6.3M-row file. The model's comment confirms the 6,731 rows in 1970 are real (1970 is the first year of FJC criminal coverage), NOT epoch corruption -- but it also flags that this cast has no explicit format string, so a source-format change could silently reintroduce the epoch trap. |
| FISCAL_YEAR | year only | 1996 → 2026 | reported | trim(FISCALYR) raw text -- FJC's fiscal-year label for the defendant record and part of its natural key. It indexes the statistical year the record was counted in; it is a bare year string, never a date. |
| FUGITIVE_END_DATE | date (typed) | 1900-01-01 → 2026-04-13 | span_end | try_to_date(trim(FGENDDATE)): closes the fugitive period. |
| FUGITIVE_START_DATE | date (typed) | 1900-01-01 → 2026-04-09 | span_start | try_to_date(trim(FGSTRTDATE)), paired with FGENDDATE: opens the period the defendant was a fugitive. |
| PROCEEDING_DATE | date (typed) | 1907-07-22 → 2026-03-31 | happened | try_to_date(trim(PROCDATE)), paired with PROCCD naming which proceeding: the day that proceeding took place. Shares the format-string latent risk flagged in the model comment. |
| SENTENCE_DATE | date (typed) | 1900-01-01 → 2026-03-31 | decided | try_to_date(trim(SENTDATE)): the day sentence was imposed. |
| TAPE_YEAR | year only | 1996 → 2026 | not_a_date | trim(TAPEYEAR) raw text -- which annual FJC release the record came from; a vintage label. |
| TERM_DATE | date (typed) | 1900-01-01 → 2026-03-31 | decided | try_to_date(trim(TERMDATE)): the day the defendant's case was terminated. |

### JUSTICE.JUSTICE__FED_FTC_DATASETS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_FILED | date (typed) | 2021-07-28 → 2026-07-07 | reported | try_to_date(DATE_FILED). Ambiguous: on a real FTC enforcement action this is the day the agency filed the case (a 'decided'-type act), but the model's own dedup note says the sampled rows are FTC news/blog/event listings with no case fields, where this reads as the item's posting date. Recorded as a posting/publication clock with the alternative flagged. |

### JUSTICE.JUSTICE__FED_SCDB
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_ARGUMENT | date (typed) | 1944-10-08 → 2025-05-15 | happened | try_to_date(DATEARGUMENT,'MM/DD/YYYY') -- the day oral argument took place; null for cases decided without argument. |
| DATE_DECISION | date (typed) | 1946-11-18 → 2025-06-30 | decided | Staging: try_to_date(DATEDECISION,'MM/DD/YYYY') -- the day the Supreme Court handed down the decision. Chosen as primary over date_argument despite the happened>decided preference: SCOTUS cases are canonically dated by decision and many are decided without argument. The model's comment confirms the 1970 rows are real 1970-term decisions, not epoch garbage. |
| DATE_REARGUMENT | date (typed) | 1946-10-14 → 2019-01-16 | happened | try_to_date(DATEREARG,'MM/DD/YYYY') -- the day the case was reargued. |
| TERM | year only | 1946 → 2024 | span_start | try_to_number(TERM) -- the Supreme Court TERM (e.g. 1994 = the term starting Oct 1994 and running to Jun 1995), so it opens a term-long period. It is a NUMBER: a bare date-parse would read it as epoch seconds. |

### JUSTICE.JUSTICE__INTL_EURLEX_CELLAR
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_OF_DOCUMENT | date (typed) | 1987-01-28 → 2026-03-26 | decided | try_to_date(DATE_OF_DOCUMENT) -- the document's own date, i.e. when the institution adopted/signed the act. Chosen as primary over date_published (against the reported>decided preference) because the adoption date is EUR-Lex's canonical anchor and publication merely trails it by OJ scheduling. |
| DATE_PUBLISHED | date (typed) | 1987-01-28 → 2026-03-26 | reported | try_to_date(DATE_PUBLISHED) -- when the act appeared in the Official Journal. |

### JUSTICE.JUSTICE__INTL_EU_SANCTIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ADDR_LEBA_PUBLICATION_DATE | date (typed) | 2002-05-29 → 2026-04-23 | reported | Same OJ publication clock for the ADDRESS sub-record's legal basis. |
| BIRT_DATE | date (typed) | 1925-01-25 → 2004-05-20 | happened | try_to_date(BIRT_DATE) -- the designated person's date of birth (a real-world event, but a person attribute, not the row's designation clock). |
| BIRT_LEBA_PUBLICATION_DATE | date (typed) | 2002-05-29 → 2026-04-23 | reported | Same OJ publication clock for the BIRTH-DETAIL sub-record's legal basis. |
| CITI_LEBA_PUBLICATION_DATE | date (typed) | 2002-05-29 → 2026-04-23 | reported | Same OJ publication clock for the CITIZENSHIP sub-record's legal basis. |
| DATE_FILE | date (typed) | 2026-05-06 → 2026-05-06 | ingest | try_to_date(DATE_FILE) -- the generation date of the EU consolidated-list export file we downloaded, i.e. the snapshot vintage, not a designation event. |
| IDEN_LEBA_PUBLICATION_DATE | date (typed) | 2003-05-20 → 2026-04-23 | reported | Same OJ publication clock for the IDENTITY-DOCUMENT sub-record's legal basis. |
| LEBA_PUBLICATION_DATE | date (typed) | 2002-05-29 → 2026-04-23 | reported | try_to_date(LEBA_PUBLICATION_DATE) -- the Official Journal publication date of the legal basis that designated this entity. The entity-level designation clock and the best anchor on the row. |
| NAAL_LEBA_PUBLICATION_DATE | date (typed) | 2002-05-29 → 2026-04-23 | reported | Same OJ publication clock for the NAME-ALIAS sub-record's legal basis. |

### JUSTICE.JUSTICE__INTL_EU_SOCTA_EUROPOL
| column | format | range | meaning | description |
|---|---|---|---|---|
| PUBLISH_DATE | date (typed) | 2025-03-18 → 2025-03-18 | reported | try_to_date(PUBLISH_DATE) on a row that IS a published report -- the day Europol published it. |
| REPORT_YEAR | year only | 2025 → 2025 | reported | REPORT_YEAR raw text passthrough -- the report's edition year, a coarse duplicate of publish_date. A bare year string, not a date. |
| UPDATE_DATE | date (typed) | 2025-05-27 → 2025-05-27 | ingest | try_to_date(UPDATE_DATE) -- when the publisher's listing entry for the report was last touched; catalogue maintenance rather than a world event. |

### JUSTICE.JUSTICE__INTL_NTI_CNS_DPRK_MISSILE_TESTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE | date as text (iso) | 1984-04-09 → 2024-11-04 | happened | "DATE" is a raw text passthrough (no cast) on a missile-test row -- the day of the launch. It is the real event clock, but it must be parsed with an explicit format before use. |
| DATE_ENTERED_UPDATED | date (typed) | 2016-12-23 → 2024-11-18 | ingest | try_to_date(DATE_ENTERED_UPDATED) -- when the CNS/NTI database entry was created or edited; publisher bookkeeping, not the launch. |

### JUSTICE.JUSTICE__INTL_OPENSANCTIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| BIRTH_DATE | date (typed) | 1921-05-06 → 2022-06-08 | happened | The mart's guarded CASE only lets exact 'YYYY-MM-DD', non-future values become dates -- the sanctioned person's date of birth. The only real-world clock among this table's candidates. |
| BIRTH_DATE_RAW | date as text (iso) | 1905-05-11 → 2022-06-08 | not_a_date | The model's own comment: BIRTH_DATE arrives in mixed precision (full dates, year-only '1997', impossible future dates); a bare try_to_date() read year-only values as epoch SECONDS and collapsed ~6.8k rows onto 1970-01-01. Kept as raw text on purpose. |

### JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT
| column | format | range | meaning | description |
|---|---|---|---|---|
| BIRTH_DATE | date as text (iso) | 1900-01-01 → 2026-03-29 | happened | Staging keeps it as nullif(trim(BIRTH_DATE),'') -- raw, never cast; the sibling OpenSanctions model documents this field as mixed precision (full dates and year-only), so grain is unknown. NOTE: the census's range for this table (min 2018-03-08, max 56596957-10-21, far_future = all 1,281,846 rows) CANNOT come from this text column -- it points at one of the timestamp columns (first_seen/last_seen/last_change/_ingested_at), where an epoch-unit mistake pushes a stamp to year 56 million. Worth a separate look. |
| FIRST_SEEN | datetime (typed) | 2018-03-08 00:00:00.000 → 2026-08-05 18:46:24.000 |  |  |
| LAST_CHANGE | datetime (typed) | 2022-01-01 00:00:00.000 → 2026-08-05 18:48:06.000 |  |  |
| LAST_SEEN | datetime (typed) | 2025-04-03 16:06:48.000 → 2026-08-05 18:53:01.000 |  |  |

### JUSTICE.JUSTICE__INTL_UCDP_GED
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_END | date (typed) | 1989-01-01 → 2024-12-31 | span_end | try_to_date(DATE_END) -- the last day the event could have occurred; the census's 13 far-future rows (to 2055) live here. |
| DATE_START | date (typed) | 1989-01-01 → 2024-12-31 | span_start | try_to_date(DATE_START) -- the first day the event could have occurred; with date_end it bounds the event window. Primary because it is day grain (vs. year for `year`) and is the event's own clock. |
| SOURCE_DATE | date (typed) | 1989-01-05 → 2025-03-20 | reported | try_to_date(SOURCE_DATE) -- the date of the source report the event was coded from; always at or after the event. |
| YEAR | year only | 1989 → 2024 | happened | try_to_number("YEAR") -- the year the violent event occurred, as a NUMBER. This is almost certainly what produced the census's epoch1970 = 385,918 (every row): a bare date-parse reads '1989' as epoch seconds and dumps the file on 1970-01-01. |

### JUSTICE.JUSTICE__RACIAL_JAIL_DISPARITY
| column | format | range | meaning | description |
|---|---|---|---|---|
| BLACK_WORKING_AGE_POP | year only | 1700 → 2035 | not_a_date | black_pop_15to64 -- a population count (the rate denominator). It matched only on 'age'. |
| LATINX_WORKING_AGE_POP | year only | 1700 → 2035 | not_a_date | latinx_pop_15to64 -- a population count, not a date. |
| TOTAL_WORKING_AGE_POP | year only | 1700 → 2035 | not_a_date | total_pop_15to64 -- a population count, not a date. |
| WHITE_WORKING_AGE_POP | year only | 1700 → 2035 | not_a_date | white_pop_15to64 -- a population count, not a date. |
| YEAR | year only | 1970 → 2026 | happened | The Vera county-year panel year carried through from staging (try_to_number(trim(YEAR))) -- the year the jail populations were measured. |

### JUSTICE.JUSTICE__STATE_MO_SEX_OFFENDER_REGISTRY
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_OF_BIRTH | date (typed) | 1926-04-17 → 2008-06-06 | happened | Staging: try_to_date(nullif(trim(DATE_OF_BIRTH),'')) with a header note that the source is an ISO timestamp string -- the registrant's birth date. It is the only clock available here (no registration or offense date is exposed), and the census's 771 epoch-1970 rows suggest a slice of blank/garbage values still parses badly. |

### JUSTICE.JUSTICE__XC_MAPPING_POLICE_VIOLENCE
| column | format | range | meaning | description |
|---|---|---|---|---|
| CHIEF_PROSECUTOR_TERM | year only | 1998 → 2019 | not_a_date | CHIEF_PROSECUTOR_TERM sits in the prosecutor block as raw uncast text -- a tenure label (and possibly a range) rather than a parseable date. |
| DATE_OF_INCIDENT_MONTH_DAY_YEAR | date (typed) | 2013-01-01 → 2026-07-22 | happened | try_to_date(DATE_OF_INCIDENT_MONTH_DAY_YEAR) -- the day the killing occurred. |
| TOTAL_POPULATION_OF_CENSUS_TRACT_2019_ACS_5_YEAR_ESTIMATES | year only | 1700 → 2035 | not_a_date | A census-tract population count from the 2019 ACS 5-year estimates, raw passthrough. It matched only on '2019' and '5_year'. |

### JUSTICE.JUSTICE__XC_NAGIX_DPRK_MISSILE_TESTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE | date as text (iso) | 1984-04-09 → 2026-05-26 | happened | "DATE" raw text passthrough on a missile-test row -- the day of the launch. Real event clock, but uncast text. |

### JUSTICE.JUSTICE__XC_OWID_HOMICIDE
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 1990 → 2024 | happened | try_to_number("YEAR") -- the year the homicide rate refers to, as a NUMBER. Year grain; a bare date-parse would read it as epoch seconds. |

### JUSTICE.JUSTICE__XC_OWID_NUCLEAR_WARHEADS
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 1945 → 2026 | happened | try_to_number("YEAR") -- the year the warhead stockpile estimate refers to, as a NUMBER. Year grain; a bare date-parse would read it as epoch seconds. |

### JUSTICE.JUSTICE__XC_OWID_TERRORISM_DEATHS
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 1970 → 2021 | happened | try_to_number("YEAR") -- the year the terrorism death count refers to, as a NUMBER. Year grain; a bare date-parse would read it as epoch seconds. |

### JUSTICE.JUSTICE__XC_UK_SANCTIONS_LIST
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_DESIGNATED | date (typed) | 2000-04-12 → 2026-07-22 | decided | try_to_date(nullif(trim(DATE_DESIGNATED),''),'DD/MM/YYYY') -- the day OFSI designated the person/entity under a UK sanctions regime; the authority's act and the row's anchor. |
| DATE_OF_BIRTH_RAW | date as text (us) | 1933-05-07 → 2002-12-09 | not_a_date | nullif(trim(D_O_B),'') -- kept deliberately as raw uncast text (the model's own _raw suffix); mixed/partial formats, not usable as a date without parsing. |
| LAST_UPDATED | date (typed) | 2021-12-18 → 2026-08-04 | ingest | try_to_date(nullif(trim(LAST_UPDATED),''),'DD/MM/YYYY') -- when OFSI last edited the list entry; publisher record maintenance, not a world event. |

### JUSTICE.JUSTICE__XC_UN_CONSOLIDATED_SANCTIONS_LIST
| column | format | range | meaning | description |
|---|---|---|---|---|
| LISTED_ON | date (typed) | 2000-04-12 → 2026-07-22 |  |  |

### JUSTICE.JUSTICE__XC_VERA_INCARCERATION_TRENDS
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 1970 → 2026 | happened | Staging: try_to_number(trim(YEAR)) on a county x year panel (source columns are all TEXT) -- the year the incarceration measures refer to. Year grain, stored as a NUMBER. |

### JUSTICE.JUSTICE__XC_WAPO_FATAL_FORCE
| column | format | range | meaning | description |
|---|---|---|---|---|
| INCIDENT_DATE | date (typed) | 2015-01-02 → 2024-12-31 | happened | try_to_date(date,'YYYY-MM-DD') with an explicit format -- the day of the fatal police encounter. |

### LABOR.LABOR__FED_DOL_EBSA_FORM5500_SCHEDULE_SB
| column | format | range | meaning | description |
|---|---|---|---|---|
| SB_CARRYOVER_PR_YR_AMT | month-year | 1760-05-04 → 1855-01-15 | not_a_date | try_to_number(): a prior-year carryover balance in dollars (_AMT); the 'PR_YR' fragment is what pulled it into the candidate list. |
| SB_CARRYOVER_PR_YR_TOT_AMT | month-year | 1760-05-04 → 1982-03-10 | not_a_date | try_to_number(): a prior-year carryover total in dollars (_TOT_AMT). |
| SB_CARRYOVER_USED_PR_YR_AMT | month-year | 1721 → 2012 | not_a_date | try_to_number(): dollars of carryover balance used in the prior year (_AMT). |
| SB_PLAN_YEAR_BEGIN_DATE | date (typed) | 2008-01-01 → 2025-03-01 | span_start | try_to_date(trim(SB_PLAN_YEAR_BEGIN_DATE),'YYYY-MM-DD') in staging: the first day of the plan year this actuarial filing covers, so it opens the filing's period and is the one date every SB row must carry; chosen as primary over sb_value_date because it is the definitional period key at one-row-per-filing grain. |
| SB_PRE_FNDNG_PR_YR_AMT | month-year | 1770-02-17 → 1950-12-12 | not_a_date | try_to_number(): a prior-year prefunding balance in dollars (_AMT). |
| SB_PRE_FNDNG_USED_PR_YR_AMT | month-year | 1717-08-02 → 1798-04-03 | not_a_date | try_to_number(): dollars of prefunding balance used in the prior year (_AMT). |
| SB_SIGNATURE_DATE | date (typed) | 1956-09-26 → 2028-09-06 | reported | try_to_date(trim(SB_SIGNATURE_DATE),'YYYY-MM-DD'): the date the enrolled actuary signed and certified the schedule to DOL/IRS, always at or after the plan year it covers - and the likeliest home for the census's single far-future 2055-09-17 row and its 1956 minimum, since Schedule SB only exists from 2008 onward. |
| SB_TAX_PRD | date (typed) | 2008-12-31 → 2025-12-31 |  |  |
| SB_TERM_FNDNG_TGT_AMT | year only | 1710-10-25 → 1987-12-24 | not_a_date | try_to_number(): a dollar funding-target amount for terminated-vested participants (_AMT), no time content. |
| SB_TERM_PARTCP_CNT | year only | 1702 → 2031 | not_a_date | try_to_number(): a count of terminated-vested participants (_CNT), not a date - 'TERM' here means terminated, not term dates. |
| SB_VALUE_DATE | date (typed) | 2008-12-31 → 2025-12-30 | span_start | try_to_date(trim(SB_VALUE_DATE),'YYYY-MM-DD'): the actuarial valuation as-of date the funding numbers were measured at (for most single-employer plans this equals the plan-year begin date), a real measurement point rather than a filing act. |

### LABOR.LABOR__FED_DOL_OLMS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ESTABLISHED_DATE | date (typed) | 1970-12-01 → 2026-06-18 | happened | try_to_date(trim(EST_DATE)): when the union local was established - but the staging model carries a live-confirmed warning that 395,053 of 617,710 rows (64%) hold the literal string '1970-12-01', DOL's own 'not on file' sentinel, which is most of the census's 589,063 epoch-1970 rows and makes this column unusable as a clock without filtering. |
| NEXT_ELECTION_DATE | date (typed) | 1806-03-01 → 2032-11-01 | happened | coalesce of three explicit formats (MM/DD/YY, MM/YYYY, MMYYYY) after a documented 2026-08-18 epoch-bug fix; it is a union-self-reported FUTURE officer-election date, month-precision for ~384k of 617k rows (only 2,247 carry a day), so it must never be used to date the filing itself. |
| PERIOD_COVERED_FROM | date (typed) | 1999-01-01 → 2026-01-01 | span_start | try_to_date(trim(PD_COVERED_FROM)) with NO format string: the first day of the period the filing covers; the bare cast is the same epoch/garbage trap that produced this table's CORRUPT_RANGE verdict. |
| PERIOD_COVERED_TO | date (typed) | 1970-01-03 → 2026-07-31 | span_end | try_to_date(trim(PD_COVERED_TO)) with NO format string: the last day of the covered period, closing the span opened by period_covered_from. |
| RECEIVE_DATE | date (typed) | 1899-12-30 → 2026-08-07 | reported | try_to_date(trim(RECEIVE_DATE)) bare cast: when DOL received the LM filing - the classic reported clock, always after the year it covers. |
| REGISTER_DATE | date (typed) | 1999-04-10 → 2026-08-07 | reported | try_to_date(trim(REGISTER_DATE)) bare cast, filed by the staging model under 'filing period / lifecycle dates': when OLMS registered the union or filing in its system. |
| REPORT_YEAR_RAW | year only | 2000 → 2026 | reported | trim(REPORT_YEAR) deliberately kept as raw TEXT (the _raw suffix says so): a year label for the report itself, not a date, and whether it differs from year_covered is unverified. |
| TERMINATION_DATE | date (typed) | 1970-01-04 → 2026-07-15 | happened | try_to_date(trim(TERM_DATE)) bare cast: when the union unit terminated; the likeliest home for the 9999-01-01 'never' sentinel behind the census's 28 far-future rows, unverifiable with the warehouse down. |
| YEAR_COVERED | year only | 2000 → 2026 | happened | try_to_number(trim(YR_COVERED)): the fiscal year whose money the LM filing reports, i.e. when the union's finances actually moved; picked as primary because it is a clean integer year with no cast risk while every date column on this table runs through a bare try_to_date and the census graded the whole table CORRUPT_RANGE (0003-11-08 to 9999-01-01, 589,063 epoch-1970 rows). |

### LABOR.LABOR__FED_MSHA_ACCIDENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACCIDENT_DATE | date (typed) | 2000-01-01 → 2026-07-14 | happened | try_to_date(accident_dt,'MM/DD/YYYY') in the mart - an explicit format, no epoch risk - dating the moment the mining accident occurred; census graded CLEAN, 2000-01-01 onward. |
| CAL_YR | year only | 2000 → 2026 | happened | try_to_number(cal_yr): the calendar year of the accident as an INTEGER, not a date - a bare date-parse of it is exactly the 1970 collapse bug. |
| DAYS_LOST | year only | 1980 → 1980 | not_a_date | try_to_number(days_lost): a duration - number of workdays the injured miner was away. |

### LABOR.LABOR__FED_MSHA_MINES
| column | format | range | meaning | description |
|---|---|---|---|---|
| CURRENT_STATUS_DT | date (typed) | 1925-01-01 → 2026-07-17 | happened | try_to_date(current_status_dt,'MM/DD/YYYY') in the mart: the date the mine entered its CURRENT status (active/abandoned/temporarily idled), so it is a real change of state at the mine - though MSHA is the one recording it, and because the mart is a current-state snapshot this column only ever holds the latest status change, not a history. |

### LABOR.LABOR__FED_MSHA_VIOLATIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| CAL_YR | year only | 1994 → 2026 | happened | try_to_number(cal_yr): an integer calendar year for the violation; the previous census groups it beside the issue date, so whether it keys to occurrence or issue is unverified. |
| VIOLATION_ISSUE_DATE | date (typed) | 1994-09-09 → 2026-07-18 | decided | try_to_date(violation_issue_dt,'MM/DD/YYYY'): when the MSHA inspector issued the citation - the enforcement act, and the gap from violation_occur_date is itself measurable. |
| VIOLATION_OCCUR_DATE | date (typed) | 1994-09-09 → 2026-07-18 | happened | try_to_date(violation_occur_dt,'MM/DD/YYYY') in the mart with an explicit format: when the violating condition actually existed at the mine, which is earlier than or equal to the citation date. |
| VIOLATOR_INSPECTION_DAY_CNT | year only | 1700 → 2035 | not_a_date | try_to_number(violator_inspection_day_cnt): a COUNT of inspection days for that violator (_CNT), a duration-style tally, not a date. |

### LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2023
| column | format | range | meaning | description |
|---|---|---|---|---|
| CREATED_TIMESTAMP | datetime (typed) | 2024-01-01 00:00:00.000 → 2024-12-31 00:00:00.000 | reported | try_to_timestamp(CREATED_TIMESTAMP): when the establishment's 300A submission was created in OSHA's ITA portal - the census range for this 2023 file is exactly 2024-01-01 to 2024-12-31, a full year after the year it covers, which proves this is the submission clock and not the injury clock. |
| NAICS_YEAR | year only | 2012 → 2022 | not_a_date | raw passthrough sitting immediately beside NAICS_CODE: the NAICS revision vintage the industry code belongs to (a classification version label), not a time for the row. |
| TOTAL_DAFW_DAYS | year only | 1700 → 2035 | not_a_date | raw passthrough total of days-away-from-work across the establishment's cases - a duration tally, not a date. |
| TOTAL_DJTR_DAYS | year only | 1700 → 2033 | not_a_date | raw passthrough total of job-transfer/restriction days - a duration tally, not a date. |
| YEAR_FILING_FOR | year only | 2023 → 2023 | happened | raw passthrough integer naming the recordkeeping year the 300A summary covers; the injury counts on the row are that year's injuries, so this is the honest year-grain placement - anchoring on created_timestamp instead would misdate the whole file by a year. |

### LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024
| column | format | range | meaning | description |
|---|---|---|---|---|
| CREATED_TIMESTAMP | datetime (typed) | 2025-01-01 00:00:00.000 → 2025-12-31 00:00:00.000 | reported | try_to_timestamp(CREATED_TIMESTAMP): the ITA portal submission timestamp; census range 2025-01-01 to 2025-12-31 for a file covering 2024, i.e. the reporting lag made visible. |
| NAICS_YEAR | year only | 2012 → 2022 | not_a_date | raw passthrough beside NAICS_CODE: the NAICS revision vintage, a classification version label. |
| TOTAL_DAFW_DAYS | year only | 1700 → 2032 | not_a_date | raw passthrough total of days-away-from-work - a duration tally. |
| TOTAL_DJTR_DAYS | year only | 1700 → 2035 | not_a_date | raw passthrough total of job-transfer/restriction days - a duration tally. |
| YEAR_FILING_FOR | year only | 2024 → 2024 | happened | raw passthrough integer naming the recordkeeping year the 300A summary covers; the counts are that year's injuries, and the file's created_timestamp range (2025) confirms the submission year is one later. |

### LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2025
| column | format | range | meaning | description |
|---|---|---|---|---|
| CREATED_TIMESTAMP | datetime (typed) | 2026-01-01 00:00:00.000 → 2026-03-15 00:00:00.000 | reported | try_to_timestamp(CREATED_TIMESTAMP): ITA portal submission timestamp; census range 2026-01-01 to 2026-03-15 shows this file is still mid-submission-window (graded SHORT_SPAN), so row counts here are not final. |
| NAICS_YEAR | year only | 1801 → 2025 | not_a_date | raw passthrough beside NAICS_CODE: the NAICS revision vintage, a classification version label. |
| TOTAL_DAFW_DAYS | year only | 1706 → 2033 | not_a_date | raw passthrough total of days-away-from-work - a duration tally. |
| TOTAL_DJTR_DAYS | year only | 1701 → 2032 | not_a_date | raw passthrough total of job-transfer/restriction days - a duration tally. |
| YEAR_FILING_FOR | year only | 2025 → 2025 | happened | raw passthrough integer naming the recordkeeping year (2025) the summary covers, one row per establishment; the year-grain anchor for this annual file. |

### LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2023
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_OF_DEATH | date (typed) | 2023-01-01 → 2024-05-04 | happened | try_to_date(DATE_OF_DEATH): when the injured worker died; populated only for fatalities, so it cannot serve as the table's clock. |
| DATE_OF_INCIDENT | date (typed) | 2022-02-26 → 2024-12-12 | happened | try_to_date(DATE_OF_INCIDENT) in the mart: the day the injury or illness incident happened to a named worker - the true event clock for this case-grain table. |
| NAICS_YEAR | year only | 2012 → 2022 | not_a_date | raw passthrough beside NAICS_CODE: the NAICS revision vintage, a classification version label, not a row time. |
| YEAR_FILING_FOR | year only | 2023 → 2023 | reported | raw passthrough integer recordkeeping year the case was logged under; this file's earliest incident is 2022-02-26, proving the log year can trail the incident, so it is a reporting-year label rather than the event year. |

### LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2024
| column | format | range | meaning | description |
|---|---|---|---|---|
| NAICS_YEAR | year only | 2012 → 2022 | not_a_date | raw passthrough beside NAICS_CODE: the NAICS revision vintage, a classification version label. |
| YEAR_OF_FILING | year only | 2024 → 2024 | reported | raw passthrough integer (the 2024/2025 marts rename this YEAR_OF_FILING where 2023 called it YEAR_FILING_FOR): the recordkeeping year the case was logged under, which can trail the incident year. |

### LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2025
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_OF_INCIDENT | date (typed) | 2024-01-01 → 2025-12-31 | happened | try_to_date(DATE_OF_INCIDENT) in the mart: the day the injury or illness happened; census CLEAN, 2024-01-01 to 2025-12-31 (incidents from the prior year still appear on the 2025 log). |
| NAICS_YEAR | year only | 2012 → 2022 | not_a_date | raw passthrough beside NAICS_CODE: the NAICS revision vintage, a classification version label. |
| YEAR_OF_FILING | year only | 2025 → 2025 | reported | raw passthrough integer recordkeeping year the case was logged under; the census range proves incidents from 2024 sit on the 2025 log, so this is a reporting year, not the event year. |

### LABOR.LABOR__FED_PBGC_TRUSTEED_PLANS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_OF_PBGC_TRUSTEESHIP | date (typed) | 1975-02-27 → 2026-06-12 | decided | try_to_date(left(trim(DATE_OF_PBGC_TRUSTEESHIP),10)): the day the federal insurer acted to take the failed plan over - an authority's action, at or after termination, and the gap between the two is itself a finding. |
| DATE_OF_PLAN_TERMINATION | date (typed) | 1972-04-01 → 2026-04-30 | happened | try_to_date(left(trim(DATE_OF_PLAN_TERMINATION),10)) in staging: the day the pension plan terminated - the real-world failure this one-row-per-case table exists to record, and the census min of 1972-04-01 is a plausible genuine value. |

### LEGAL_ENFORCEMENT.LEGAL_ENFORCEMENT__FED_NAAG_MULTISTATE_SETTLEMENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATERESOLVED | date as text (us) | 1983-03-25 → 2021-07-23 | happened | raw passthrough - this mart applies NO casts at all, selecting straight from the landing table - naming the date the multistate settlement was resolved, the event the dataset exists to record; the census could not measure it (UNMEASURED_CLOCK) precisely because nothing types it as a date. |
| DATE_ENTRY_CREATED | date as text (us) | 2021-07-12 → 2021-07-12 | reported | raw passthrough: when a NAAG researcher typed this row into their database - curation bookkeeping that tracks NAAG's own data-entry campaigns, not the settlement's timing; the same hazard class as an ingest column even though it is the upstream publisher's, not Ripple's, so never use it as the settlement clock. |
| DATE_FILED | date as text (us) | 2019-07-22 → 2019-07-26 | reported | raw passthrough: when the complaint was filed with the court - a filing act preceding the resolution. |
| YEAR | year only | 1980 → 2019 | happened | raw passthrough integer year of the settlement - the year-grain twin of dateresolved, and the safer of the two if the text dates turn out to be messy. |

### MARITIME.MARITIME__FED_NOAA_AIS
| column | format | range | meaning | description |
|---|---|---|---|---|
| BASE_DATETIME | datetime (typed) | 2024-01-01 00:00:00.000 → 2024-01-08 23:59:59.000 | happened | try_to_timestamp on BASEDATETIME: the exact moment the vessel broadcast its position, the finest and truest clock on the table — real resolution is seconds, recorded as 'day' only because the grain vocabulary has no sub-day option. |
| BASE_DATETIME_HOUR | datetime (typed) | 2024-01-01 00:00:00.000 → 2024-01-08 23:00:00.000 | happened | The mart computes it as date_trunc('hour', base_datetime): the same event clock bucketed to the hour, again recorded as 'day' because the grain vocabulary stops there. |
| DATE | date (typed) | 2024-01-01 → 2024-01-08 | happened | try_to_date on the AIS file's DATE field: the calendar day of the vessel position report, the day-grain twin of base_datetime. |

### MONEY_FINANCE.MONEY__DEBT_REPAYMENT_CLIFF
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATA_YEAR | year only | 2026 → 2032 | happened | try_to_number(substr(year_col,3,4)) unpivoted from the c_2025..c_2032 columns - the year a scheduled debt-service payment falls due. The mart filters to data_year >= 2026, so this entire table sits in the FUTURE: it is a contractual schedule, not a record of payments made. |

### OPEN_DATA.OPEN_DATA__INTL_AR_DATOSGOB
| column | format | range | meaning | description |
|---|---|---|---|---|
| LAST_MODIFIED | date as text (iso) | 2025-03-24 → 2026-07-02 | unclear | Raw pass-through with no cast — the Argentine portal's own stamp for when the dataset record was last changed; publisher record-maintenance, not Ripple's ingest. |

### OPEN_DATA.OPEN_DATA__INTL_CA_OPEN_CANADA
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_PUBLISHED | date as text (iso) | 2012-06-26 → 2026-07-02 | unclear | Uncast TEXT — the dataset's declared publication date; semantically the better publication clock than metadata_created but its fill rate is unverified. |
| METADATA_CREATED | date as text (iso) | 2016-09-23 → 2026-07-02 | unclear | Uncast TEXT (the staging header says casts are kept as landed) holding the CKAN record-creation stamp — when the dataset was registered on the portal; the densest publication clock on a catalog row. |
| METADATA_MODIFIED | date as text (iso) | 2026-07-01 → 2026-07-02 | reported | Uncast TEXT — when the portal last edited the catalog record; record maintenance by the publisher, always later than creation. |
| TIME_PERIOD_COVERAGE_END | date as text (iso) | 1935-12-31 → 2030-01-01 | span_end | Uncast TEXT closing the data-coverage period; same precision caveat. |
| TIME_PERIOD_COVERAGE_START | date as text (iso) | 1760-01-01 → 2026-05-28 | span_start | Uncast TEXT bounding the period the DATA covers, not when anything was published; publisher-entered coverage strings vary in precision. |

### OPEN_DATA.OPEN_DATA__INTL_CH_OPENDATASWISS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ISSUED | date as text (iso) | 1767-01-01 → 2026-07-01 | reported | Uncast TEXT (casts kept as landed) — the DCAT issued date, i.e. when the dataset was published. |
| METADATA_CREATED | date as text (iso) | 2015-11-25 → 2023-09-17 | reported | Uncast TEXT CKAN record-creation stamp — when the dataset appeared on opendata.swiss; the portal-core field most likely populated on every row. |
| METADATA_MODIFIED | date as text (iso) | 2025-03-18 → 2026-07-02 | reported | Uncast TEXT — when the portal last edited the catalog record; publisher record maintenance. |

### OPEN_DATA.OPEN_DATA__INTL_CL_DATOSGOB
| column | format | range | meaning | description |
|---|---|---|---|---|
| METADATA_CREATED | date as text (iso) | 2015-10-30 → 2026-07-02 | reported | Uncast TEXT CKAN record-creation stamp — when the dataset was registered on datos.gob.cl. |
| METADATA_MODIFIED | date as text (iso) | 2024-01-22 → 2026-07-02 | reported | Uncast TEXT — when the portal last edited the catalog record. |

### OPEN_DATA.OPEN_DATA__INTL_DE_GOVDATA
| column | format | range | meaning | description |
|---|---|---|---|---|
| METADATA_CREATED | date as text (iso) | 2013-02-17 → 2025-08-12 | reported | Uncast TEXT CKAN record-creation stamp — when the dataset was registered on GovData.de. |
| METADATA_MODIFIED | date as text (iso) | 2021-03-26 → 2025-08-12 | reported | Uncast TEXT — when the portal last edited the catalog record. |
| TEMPORAL_END | date as text (iso) | 1971-11-08 → 2028-12-31 | span_end | Uncast TEXT closing the data-coverage period; same caveat. |
| TEMPORAL_START | date as text (iso) | 1849-12-30 → 2025-08-06 | span_start | Uncast TEXT opening the period the DATA covers, not a publication event; publisher-entered precision varies. |

### OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV
| column | format | range | meaning | description |
|---|---|---|---|---|
| CREATED_AT | datetime (typed) | 1827-01-01 00:00:00.000 → 2028-07-01 00:00:00.000 | reported | try_to_timestamp_ntz(left(created_at,19),'YYYY-MM-DD"T"HH24:MI:SS') per the mart's own sampled-format note — when the dataset was created on data.gouv.fr; the dense, clean publication clock. |
| LAST_MODIFIED | datetime (typed) | 1991-01-01 08:56:11.000 → 2026-08-11 05:45:01.000 | reported | Same ISO timestamp cast — when the dataset record was last changed on the portal; publisher record maintenance, not Ripple's ingest. |
| TEMPORAL_COVERAGE_END | date (typed) | 1738-12-31 → 2035-12-31 | span_end | Same YYYY-MM-DD cast closing the data-coverage period; equally polluted by publisher-typed placeholder years. |
| TEMPORAL_COVERAGE_START | date (typed) | 1700-01-01 → 2030-04-19 | span_start | try_to_date(left(temporal_coverage_start,10),'YYYY-MM-DD') — opens the period the DATA covers; publisher-typed free text, so this is where the census's 0001-01-01 minimum, 9999-12-31 maximum, 68 epoch rows and 583 far-future rows come from, NOT from created_at. |

### OPEN_DATA.OPEN_DATA__INTL_GR_DATAGOV
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_CREATED | date as text (iso) | 2025-11-17 → 2026-07-02 | reported | Uncast TEXT record-creation stamp — when the dataset was registered on data.gov.gr. |
| METADATA_MODIFIED | date as text (iso) | 2026-05-25 → 2026-07-02 | reported | Uncast TEXT — when the portal last edited the catalog record. |

### OPEN_DATA.OPEN_DATA__XC_WAYBACK_DOJ_EPSTEIN
| column | format | range | meaning | description |
|---|---|---|---|---|
| CAPTURED_AT | datetime (typed) | 2025-12-19 21:13:27.000 → 2026-06-09 02:03:36.000 |  |  |

### POLITICS.POLITICS__BILLS
| column | format | range | meaning | description |
|---|---|---|---|---|
| INTRODUCED_DATE | date (typed) | 2023-01-03 → 2026-06-26 | happened | The day the bill was introduced - the row's own birth event; try_to_date cast in staging and used as the dedup ordering key. |
| LATEST_ACTION_DATE | date as text (iso) | 2023-01-03 → 2026-06-26 | decided | Date of the most recent legislative action (referral, floor vote, signature) - an authority acting; NOTE staging leaves it as trimmed TEXT (no try_to_date) unlike introduced_date, so it is an uncast date string. |

### POLITICS.POLITICS__BILL_COSPONSORS
| column | format | range | meaning | description |
|---|---|---|---|---|
| SPONSORSHIP_DATE | date (typed) | 2023-01-09 → 2026-06-25 | happened | The day the member actually signed on as cosponsor; staging casts it with try_to_date on a trimmed non-empty string. |
| SPONSORSHIP_WITHDRAWN_DATE | date (typed) | 2023-01-11 → 2026-06-25 | happened | The day the member withdrew the cosponsorship - a second real event on the same row, try_to_date cast, null on the rows that never withdrew. |

### POLITICS.POLITICS__CA_LOBBY_AMENDMENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ADD_LE_EFF | date (typed) | 1935-11-20 → 2028-02-20 |  |  |
| ADD_LF_EFF | date (typed) | 1999-01-01 → 2026-07-31 |  |  |
| ADD_L_EFF | date (typed) | 2001-01-16 → 2028-04-27 |  |  |
| DEL_LE_EFF | date (typed) | 1999-04-01 → 2026-12-05 |  |  |
| DEL_LF_EFF | date (typed) | 1999-01-01 → 2026-06-30 |  |  |
| DEL_L_EFF | date (typed) | 1928-06-29 → 2026-09-30 |  |  |
| EXEC_DATE | date (typed) | 1823-10-01 → 2028-07-28 | reported | try_to_date(split_part(EXEC_DATE,' ',1),'MM/DD/YYYY') — the date the Form 605 amendment was executed and submitted; the row's own filing event. |
| FROM_DATE | date (typed) | 1987-01-31 → 2026-07-31 | span_start | Same MM/DD/YYYY cast; opens the period the amendment covers. |
| OTHER_EFF | date (typed) | 2000-12-04 → 2026-08-03 |  |  |
| THRU_DATE | date (typed) | 2000-12-04 → 2026-12-31 | span_end | Same MM/DD/YYYY cast; closes the covered period. The census's 0107-10-31 / 5201-11-18 extremes and 15 far-future rows are published CAL-ACCESS typo years surviving a strict-format parse, not a cast bug. |

### POLITICS.POLITICS__CA_LOBBY_CHG_LOG
| column | format | range | meaning | description |
|---|---|---|---|---|
| EFFECT_DT | date (typed) | 1900-01-01 → 2030-07-01 | happened | MM/DD/YYYY date for when the logged attribute change takes effect — the truer real-world clock than log_dt, but I could not verify its fill rate with the warehouse down, so log_dt is the safer primary. |
| ETHICS_DT | date (typed) | 1900-01-01 → 2025-01-16 | happened | Real MM/DD/YYYY date column, but I could not confirm what it dates; by CAL-ACCESS convention it is the filer's ethics-training completion date. Treat the meaning as unverified. |
| LOG_DT | date (typed) | 1999-10-12 → 2026-08-03 | reported | try_to_date(...,'MM/DD/YYYY') — the date the registry logged the change; for a change-log grain this is the row's own recorded event and the one column certain to carry a value on every row. |

### POLITICS.POLITICS__CA_LOBBY_CONTRIBUTIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| FILING_PERIOD_END_DT | date (typed) | 2000-03-31 → 2031-03-01 | span_end | Same cast; closes the disclosure period. |
| FILING_PERIOD_START_DT | date (typed) | 2000-01-01 → 2001-04-01 | span_start | try_to_date(...,'MM/DD/YYYY') — opens the disclosure period the contribution was reported in; the dense fallback placement for rows whose contribution_dt is blank. |

### POLITICS.POLITICS__CA_LOBBY_COVER
| column | format | range | meaning | description |
|---|---|---|---|---|
| FROM_DATE | datetime (typed) | 1899-12-30 00:00:00.000 → 2033-07-01 00:00:00.000 | span_start | Same timestamp cast; opens the period the cover page reports on. |
| RPT_DATE | datetime (typed) | 1724-01-01 00:00:00.000 → 2035-07-18 00:00:00.000 | reported | try_to_timestamp(RPT_DATE,'MM/DD/YYYY HH12:MI:SS AM') — the report date on the disclosure cover page; the time part is midnight padding so the real resolution is a day. |
| THRU_DATE | datetime (typed) | 1899-12-30 00:00:00.000 → 2035-12-31 00:00:00.000 | span_end | Same timestamp cast; closes the reported period. The 0001-07-01 / 8201-04-01 extremes and 219 far-future rows are published typo years passing a strict format, not a cast defect. |

### POLITICS.POLITICS__CA_LOBBY_EMPLOYER
| column | format | range | meaning | description |
|---|---|---|---|---|
| SESSION_YR_1 | year only | 1999 → 1999 | span_start | Kept as trimmed text while every amount column beside it got try_to_number(18,2), so it reads as the first calendar year of the two-year legislative session — the only real clock on this employer-session table. |
| SESSION_YR_2 | year only | 2000 → 2000 | span_end | Same treatment as session_yr_1; the second calendar year of the session, closing the span. |

### POLITICS.POLITICS__CA_LOBBY_FIRM
| column | format | range | meaning | description |
|---|---|---|---|---|
| SESSION_YR_1 | year only | 2001 → 2001 | span_start | Left as trimmed text while every neighbouring amount got try_to_number(18,2) — the first calendar year of the two-year session, and the only real clock on this firm-session table. |
| SESSION_YR_2 | year only | 2002 → 2002 | span_end | Second calendar year of the session, closing the span. |

### POLITICS.POLITICS__CA_LOBBY_FIRM_EMPLOYER
| column | format | range | meaning | description |
|---|---|---|---|---|
| RPT_END | date (typed) | 2001-06-30 → 2001-06-30 | span_end | Same cast; closes the billing period. The census's 2026-08-05 max is the ingest timestamp bleeding in, not a real report end. |
| RPT_START | date (typed) | 2001-04-01 → 2001-04-01 | span_start | try_to_date(...,'MM/DD/YYYY') — opens the billing period the firm-employer line covers; the grain is literally firm-filing-employer-period, so this is the row's own clock. |

### POLITICS.POLITICS__FEC_CANDIDATE
| column | format | range | meaning | description |
|---|---|---|---|---|
| CAND_ELECTION_YR | year only | 1980 → 2035 | happened | Year of the election the candidate registered for - the event year, try_to_number integer; also the mart's dedup ordering key. |
| CYCLE | year only | 2024 → 2026 | span_end | FEC two-year cycle label (raw CYCLE passthrough) that keys the row; names the closing year of the covered period, not a point event. |

### POLITICS.POLITICS__FEC_CANDIDATE_SUMMARY
| column | format | range | meaning | description |
|---|---|---|---|---|
| COVERAGE_END_DATE | date as text (us) | 2023-01-01 → 2026-12-31 | span_end | Last day of the financial reporting period the dollar totals cover; HAZARD - staging leaves it as a trimmed MM/DD/YYYY TEXT string (no try_to_date), so any bare parse must be told the US format. |
| CYCLE | year only | 2024 → 2026 | span_end | FEC two-year cycle label keying the financial summary; a period label, coarser than coverage_end_date on the same row. |

### POLITICS.POLITICS__FEC_CAND_CMTE_LINK
| column | format | range | meaning | description |
|---|---|---|---|---|
| CAND_ELECTION_YR | year only | 1980 → 2034 | happened | Year of the election the candidate is contesting - the real-world event year; stored via try_to_number so it is an integer, and a bare date-parse of it would collapse to 1970. |
| CYCLE | year only | 2024 → 2026 | span_end | FEC two-year election-cycle label (raw CYCLE passthrough, a number not a date) naming the closing year of the reporting period the linkage file covers. |
| FEC_ELECTION_YR | year only | 2024 → 2026 | happened | FEC's own coded election year for the linkage; same integer shape as cand_election_yr (try_to_number) and can disagree with it, which is why both are kept. |

### POLITICS.POLITICS__FEC_COMMITTEE
| column | format | range | meaning | description |
|---|---|---|---|---|
| CYCLE | year only | 2024 → 2026 |  |  |

### POLITICS.POLITICS__FED_CONGRESS_LEGISLATORS
| column | format | range | meaning | description |
|---|---|---|---|---|
| TERM_END | date as text (iso) | 1790-06-01 → 2031-01-03 | span_end | End of the person's service span (staging names it last_term_end); for sitting members this is a scheduled future date, so far-future values here are legitimate. |
| TERM_START | date as text (iso) | 1789-03-04 → 2026-06-10 | unclear | Start of the person's service span (staging names it first_term_start); one row per legislator, so it bounds a career, not a single term - raw trimmed TEXT, never cast to date. |

### POLITICS.POLITICS__FED_FCC_LICENSING
| column | format | range | meaning | description |
|---|---|---|---|---|
| CANCELLATION_DATE | date (typed) | 1917-07-11 → 2026-06-27 | decided | The day the FCC cancelled the licence - an authority action, try_to_date cast; null on live licences. |
| EXPIRED_DATE | date (typed) | 1994-05-29 → 2035-12-31 | span_end | End of the licence term (10-year terms are normal), which explains the census's 373,860 'far future' rows and the 2036 max - those are legitimate expirations, not corruption. |
| GRANT_DATE | date (typed) | 1984-05-29 → 2026-06-27 | decided | The day the FCC granted the license - the authority's act and the best single anchor for a licence row; explicit try_to_date in the mart. |
| LAST_ACTION_DATE | date (typed) | 1917-07-11 → 2026-06-27 | decided | Date the FCC last touched the licence record - the publisher's maintenance clock, not ours, so not 'ingest'; try_to_date cast. |

### POLITICS.POLITICS__FED_FEC_API
| column | format | range | meaning | description |
|---|---|---|---|---|
| CONTRIBUTION_RECEIPT_DATE | date as text (iso) | 2000-09-01 → 2022-05-26 | happened | The date the committee received the contribution — the real-world money event; note the staging model explicitly keeps all casts as landed TEXT, so it is an unparsed string today. |
| LOAD_DATE | date as text (iso) | 2025-02-25 → 2026-06-30 | reported | The FEC's own stamp for when the transaction entered their published database — publisher bookkeeping, not Ripple's ingest, and never the event clock. |

### POLITICS.POLITICS__FED_FEC_PAC_SUMMARY
| column | format | range | meaning | description |
|---|---|---|---|---|
| CASH_BEGINNING_OF_PERIOD | year only | 1700 → 2032 | not_a_date | FALSE POSITIVE - a DOLLAR amount (coh_bop, try_to_double) that matched only on the word 'period' in its name. |
| CASH_CLOSE_OF_PERIOD | year only | 1700 → 2032 | not_a_date | FALSE POSITIVE - a DOLLAR amount (coh_cop, try_to_double), matched on 'period'. |
| COVERAGE_END_DATE | date (typed) | 2017-01-01 → 2025-01-31 | span_end | Last day of the committee's reporting period - cast try_to_date(trim(C27),'MM/DD/YYYY') in staging and part of the table's grain key, so it is the honest anchor; the census max of 2026-07-24 02:13:26 is a timestamp and must have come from _loaded_at, not this column. |
| NONFEDERAL_TRANSFERS_RECEIVED | year only | 1700 → 2000 | not_a_date | FALSE POSITIVE - a DOLLAR amount (nonfed_trans_received, try_to_double), matched on 'received'. |

### POLITICS.POLITICS__FED_FJC_JUDGES
| column | format | range | meaning | description |
|---|---|---|---|---|
| BIRTH_YEAR | year only | 1732 → 1991 | happened | Year the judge was born - a real event at year grain; raw passthrough number, so a bare date-parse would read it as epoch seconds and land on 1970-01-01. |
| COMMITTEE_ACTION_DATE_1 | date (typed) | 1826-05-22 → 2026-06-18 | decided | Day the committee voted/reported on nomination 1 - an authority acting; try_to_date cast. |
| COMMITTEE_REFERRAL_DATE_1 | date (typed) | 1826-05-08 → 2026-04-14 | decided | Day the Senate referred nomination 1 to the Judiciary Committee - an authority acting; try_to_date cast. |
| CONFIRMATION_DATE_1 | date (typed) | 1789-09-25 → 2026-06-24 | decided | Day the full Senate confirmed the judge to seat 1 - the ruling; try_to_date cast. |
| DEATH_YEAR | year only | 1790 → 2026 | happened | Year the judge died - a real event at year grain; raw passthrough number with the same epoch-parse hazard as birth_year. |
| HEARING_DATE_1 | date (typed) | 1890-02-17 → 2026-04-29 | decided | Day the Judiciary Committee held the confirmation hearing for seat 1 - a formal proceeding by the authority; try_to_date cast. |
| NOMINATION_DATE_1 | date (typed) | 1789-09-24 → 2026-04-14 | decided | Day the President formally nominated the judge to seat 1 - an authority acting; try_to_date cast. |
| RECESS_APPOINTMENT_DATE_1 | date (typed) | 1789-11-18 → 2004-02-20 | decided | Day the President made a recess appointment to the judge's 1st seat - an authority acting; explicit try_to_date in the mart. |

### POLITICS.POLITICS__FED_FJC_SERVICE
| column | format | range | meaning | description |
|---|---|---|---|---|
| COMMISSION_DATE | date (typed) | 1789-09-26 → 2026-06-18 | decided | Day the commission was signed and judicial service in this seat actually began - the most complete, most meaningful anchor for a service record; try_to_date cast, and it pairs with termination_date to bound the tenure. |
| COMMITTEE_ACTION_DATE | date (typed) | 1826-05-22 → 2026-06-18 | decided | Day the committee voted/reported (the companion judiciary_committee_action holds what it decided); try_to_date cast. |
| COMMITTEE_REFERRAL_DATE | date (typed) | 1826-05-08 → 2026-04-14 | decided | Day the Senate referred the nomination to the Judiciary Committee; try_to_date cast. |
| CONFIRMATION_DATE | date (typed) | 1789-09-25 → 2026-06-24 | decided | Day the full Senate confirmed the judge - the ruling; try_to_date cast, and the gap from nomination_date is the confirmation-delay finding. |
| C_2ND_SERVICE_AS_CHIEF_JUDGE_BEGIN | year only | 1966 → 2024 | span_start | Start of a SECOND chief-judge tenure in the same seat, published as a YEAR; uncast raw passthrough. |
| C_2ND_SERVICE_AS_CHIEF_JUDGE_END | year only | 1968 → 2021 | span_end | End of a SECOND chief-judge tenure, published as a YEAR; uncast raw passthrough. |
| HEARING_DATE | date (typed) | 1890-02-17 → 2026-04-29 | decided | Day the committee held the confirmation hearing - a formal proceeding by the authority; try_to_date cast. |
| NOMINATION_DATE | date (typed) | 1789-09-24 → 2026-04-14 | decided | Day the President formally nominated the judge to this seat; try_to_date cast. |
| RECESS_APPOINTMENT_DATE | date (typed) | 1789-11-18 → 2004-02-20 | decided | Day the President made a recess appointment to this seat - an authority acting; explicit try_to_date in the mart. |
| SENIOR_STATUS_DATE | date (typed) | 1919-10-06 → 2026-06-21 | decided | Day the judge's senior status took effect - a formal status change; try_to_date cast. |
| SERVICE_AS_CHIEF_JUDGE_BEGIN | year only | 1801 → 2026 | span_start | Start of the chief-judge tenure, published by FJC as a YEAR - the mart deliberately does NOT wrap it in try_to_date while wrapping every neighbouring date column, and a bare parse of those year strings is the likeliest source of the census's 365 epoch-1970 rows on this table. |
| SERVICE_AS_CHIEF_JUDGE_END | year only | 1802 → 2026 | span_end | End of the chief-judge tenure, published as a YEAR; uncast raw passthrough - same epoch-1970 hazard. |

### POLITICS.POLITICS__FED_MEDSL_HOUSE_RETURNS
| column | format | range | meaning | description |
|---|---|---|---|---|
| CANDIDATE_VOTES | month-year | 1700 → 2035 | not_a_date | FALSE POSITIVE - a vote COUNT, try_to_number(candidatevotes); matched on the same 'candi-DATE' substring. |
| ELECTION_YEAR | year only | 1976 → 2018 | happened | Year the House election was held - the event; try_to_number(year) so it is an INTEGER, which is why the census logged no date range and why a bare date-parse would collapse the table to 1970. |

### POLITICS.POLITICS__FED_MEDSL_PRESIDENT_RETURNS
| column | format | range | meaning | description |
|---|---|---|---|---|
| CANDIDATE_VOTES | year only | 1702 → 2035 | not_a_date | FALSE POSITIVE - a vote COUNT, try_to_number(candidatevotes). |
| ELECTION_YEAR | year only | 1976 → 2016 | happened | Year the presidential election was held; try_to_number(year) integer, so year grain is the finest real resolution. |

### POLITICS.POLITICS__FED_MEDSL_SENATE_RETURNS
| column | format | range | meaning | description |
|---|---|---|---|---|
| CANDIDATE_VOTES | month-year | 1701 → 2033 | not_a_date | FALSE POSITIVE - a vote COUNT, try_to_number(candidatevotes). |
| ELECTION_YEAR | year only | 1976 → 2024 | happened | Year the Senate election was held; try_to_number(year) integer. |

### POLITICS.POLITICS__FED_VOTEVIEW_ROLLCALL_META
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE | date as text (iso) | 1789-05-16 → 2026-08-08 | happened | The day the roll-call vote was taken; this mart passes raw DATE through UNCAST, but the sibling staging model documents it landing as 'YYYY-MM-DD' and parses it with that explicit format. |

### POLITICS.POLITICS__FJC_APPOINTMENT
| column | format | range | meaning | description |
|---|---|---|---|---|
| COMMISSION_DATE | date as text (iso) | 1789-09-26 → 2026-06-18 |  |  |
| CONFIRMATION_DATE | date as text (iso) | 1789-09-25 → 2026-06-24 |  |  |
| NOMINATION_DATE | date as text (iso) | 1789-09-24 → 2026-04-14 |  |  |
| TERMINATION_DATE | date as text (iso) | 1790-05-18 → 2026-06-27 |  |  |

### POLITICS.POLITICS__FJC_JUDGE
| column | format | range | meaning | description |
|---|---|---|---|---|
| BIRTH_YEAR | year only | 1732 → 1991 |  |  |
| DEATH_YEAR | year only | 1790 → 2026 |  |  |

### POLITICS.POLITICS__FJC_SCOTUS_CROSSWALK
| column | format | range | meaning | description |
|---|---|---|---|---|
| FIRST_TERM | year only | 1946 → 2022 |  |  |
| LAST_TERM | year only | 1948 → 2024 |  |  |
| _BUILT_AT | datetime (typed) | 2026-06-30 20:47:45.146 -0700 → 2026-06-30 20:47:45.146 -0700 |  |  |

### POLITICS.POLITICS__INTL_ELECTIONS_CANADA_CONTRIBUTIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| CONTRIBUTION_RECEIVED_DATE | date (typed) | 1900-01-02 → 2035-01-01 | happened | try_to_date(trim(CONTRIBUTION_RECEIVED_DATE)) — when the contribution was received; the 0025-04-07 / 4002-06-15 extremes, 2 epoch rows and 77 far-future rows are published typos surviving a permissive parse. |
| FISCAL_ELECTION_DATE | date (typed) | 2004-01-20 → 2026-12-31 | span_end | try_to_date(trim(...)) with no format; it carries the fiscal-period end or the election date of the financial return the contribution was reported on, so it closes the return's period rather than dating the gift. |

### POLITICS.POLITICS__INTL_OWID_MILSPEND
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 1949 → 2025 | happened | The observation year of an annual country-level military-spending series; try_to_number(YEAR) so it is an INTEGER, not a date - year is the finest real resolution. |

### POLITICS.POLITICS__INTL_VOETEN_UNGA_VOTES
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 1946 → 2024 | happened | Year of the UN General Assembly session the vote-agreement row covers; try_to_number(YEAR) integer - do NOT read day grain into this 1.8M-row table. |

### POLITICS.POLITICS__IRS527_8871_ORGS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ESTABLISHED_DATE | date (typed) | 1808-01-01 → 2026-07-24 | happened | try_to_date(ESTABLISHED_DATE,'YYYYMMDD') — when the 527 organization was established; the only real-world event clock here, though it dates the org rather than the notice, and the 1808 minimum plus 34 epoch rows are published typos. |
| INSERT_DATETIME | datetime (typed) | 2001-05-13 21:20:54.000 → 2026-07-24 20:46:44.000 | reported | try_to_timestamp(INSERT_DATETIME,'YYYY-MM-DD HH24:MI:SS') — the IRS's own stamp for when the notice was inserted into their disclosure database; a publisher load stamp, not Ripple's ingest, and dating rows by it is the mistake that corrupted the previous census. |

### POLITICS.POLITICS__IRS527_8872_REPORTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| INSERT_DATETIME | datetime (typed) | 2000-11-17 16:41:01.000 → 2026-07-23 20:42:11.000 | reported | try_to_timestamp_ntz of the IRS's own database insert stamp; publisher bookkeeping, not Ripple's ingest, and it is what pushed the census max to 2026-08-05. |
| ORG_FORMATION_DATE | date (typed) | 1869-09-01 → 2026-06-01 | happened | try_to_date(...,'YYYYMMDD') for when the organization was formed — a real event, but it dates the org, not this report row; the 1869 minimum and 123 epoch rows are published typos. |
| PERIOD_BEGIN_DATE | date (typed) | 2000-01-01 → 2026-07-01 | span_start | try_to_date(...,'YYYYMMDD') — opens the period the 8872 report covers; the row is a periodic report, so this is its own clock. |
| PERIOD_END_DATE | date (typed) | 2000-08-31 → 2026-07-23 | span_end | Same YYYYMMDD cast; closes the reported period. |
| PRE_OR_POST_ELECT_DATE | date (typed) | 2000-11-07 → 2026-05-19 | happened | try_to_date(...,'YYYYMMDD') carrying the date of the election a pre- or post-election report is tied to; a real event date, but the election's, not the report's. |

### POLITICS.POLITICS__JCS_MEDIANS
| column | format | range | meaning | description |
|---|---|---|---|---|
| TERM | year only | 1936 → 2023 |  |  |
| YEAR | year only | 1924 → 2024 |  |  |
| _BUILT_AT | datetime (typed) | 2026-06-30 21:08:25.743 -0700 → 2026-06-30 21:08:25.743 -0700 |  |  |

### POLITICS.POLITICS__JUDGE_IDEOLOGY_COA
| column | format | range | meaning | description |
|---|---|---|---|---|
| _BUILT_AT | datetime (typed) | 2026-06-30 21:08:24.607 -0700 → 2026-06-30 21:08:24.607 -0700 |  |  |

### POLITICS.POLITICS__JUDGE_IDEOLOGY_SCOTUS
| column | format | range | meaning | description |
|---|---|---|---|---|
| TERM | year only | 1937 → 2022 |  |  |
| _BUILT_AT | datetime (typed) | 2026-06-30 21:08:22.950 -0700 → 2026-06-30 21:08:22.950 -0700 |  |  |

### POLITICS.POLITICS__MEMBER_CROSSWALK
| column | format | range | meaning | description |
|---|---|---|---|---|
| FIRST_TERM_START | date as text (iso) | 1789-03-04 → 2026-06-10 | span_start | Start of the member's congressional career on a one-row-per-member table - the only forward-looking anchor here; raw trimmed TEXT in staging, never cast to date. |
| LAST_TERM_END | date as text (iso) | 1790-06-01 → 2031-01-03 | span_end | End of the member's most recent term; for sitting members it is a SCHEDULED FUTURE date, so far-future values are legitimate here; raw trimmed TEXT. |

### POLITICS.POLITICS__MEMBER_INDIV_DONATIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| CYCLE | year only | 2024 → 2026 |  |  |

### POLITICS.POLITICS__MEMBER_MONEY_RAISED
| column | format | range | meaning | description |
|---|---|---|---|---|
| CYCLE | year only | 2024 → 2026 | span_end | FEC two-year election cycle the money total covers, inherited from fec_candidate_summary and part of the (bioguide, cycle) key; a period label naming its closing year, not a point event. |

### POLITICS.POLITICS__MEMBER_PAC_MONEY
| column | format | range | meaning | description |
|---|---|---|---|---|
| CYCLE | year only | 2024 → 2026 |  |  |

### POLITICS.POLITICS__MEMBER_SPINE
| column | format | range | meaning | description |
|---|---|---|---|---|
| FIRST_TERM_START | date as text (iso) | 1789-03-04 → 2026-06-10 | span_start | Start of the member's career, passed straight through from the crosswalk; raw TEXT upstream, never cast to date. |
| LAST_TERM_END | date as text (iso) | 1790-06-01 → 2031-01-03 | span_end | End of the member's most recent term, from the crosswalk; scheduled future dates are legitimate for sitting members. |

### POLITICS.POLITICS__SCOTUS_JUSTICE
| column | format | range | meaning | description |
|---|---|---|---|---|
| FIRST_TERM | year only | 1946 → 2022 |  |  |
| LAST_TERM | year only | 1948 → 2024 |  |  |
| _BUILT_AT | datetime (typed) | 2026-06-30 20:16:35.621 -0700 → 2026-06-30 20:16:35.621 -0700 |  |  |

### POLITICS.POLITICS__SENATE_TRADES
| column | format | range | meaning | description |
|---|---|---|---|---|
| TRANSACTION_DATE | date (typed) | 2012-06-14 → 2020-12-02 |  |  |

### POLITICS.POLITICS__ST_CANNABIS_POLICY_BUNDLES
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 1994 → 2023 | happened | Panel-observation year of a state-year policy grid (the repo's spine backfill records the natural key as FIPS+YEAR; 1,500 rows is 50 states x 30 years); try_to_number(YEAR) integer. |

### POLITICS.POLITICS__ST_NYC_CFB_CAMPAIGN_2001_CONTRIBUTION
| column | format | range | meaning | description |
|---|---|---|---|---|
| ELECTION_CYCLE | year only | 2001 → 2001 | span_end | trim(ELECTION) — the election year the contribution was raised for; the cycle closes in that year, and on this single-cycle table it is effectively constant. |

### POLITICS.POLITICS__ST_NYC_CFB_CAMPAIGN_2009_CONTRIBUTION
| column | format | range | meaning | description |
|---|---|---|---|---|
| CONTRIBUTION_DATE | date (typed) | 2000-05-02 → 2010-01-11 | happened | try_to_date(trim(DATE)) — when the contribution was made; the census's 2000-05-02 minimum shows the permissive parse does land real values here, unlike the 2001 table. |
| ELECTION_CYCLE | year only | 2009 → 2009 | span_end | trim(ELECTION) — the election year the money was raised for; the cycle closes in that year. |
| REFUND_DATE | date (typed) | 2004-01-06 → 2010-01-11 | happened | try_to_date(trim(REFUNDDATE)) — when the contribution was refunded, a real second event on the same row. |

### POLITICS.POLITICS__ST_NYC_CFB_CAMPAIGN_2013_CONTRIBUTION
| column | format | range | meaning | description |
|---|---|---|---|---|
| CONTRIBUTION_DATE | date (typed) | 1913-06-13 → 2014-01-11 | happened | try_to_date(trim(DATE)) — when the contribution was made; the census's 1913-06-13 minimum is a published '13-for-2013' typo that the no-format parse accepted. |
| ELECTION_CYCLE | year only | 2013 → 2013 | span_end | trim(ELECTION) — the election year the money was raised for; the cycle closes in that year. |
| REFUND_DATE | date (typed) | 2001-01-10 → 2014-01-11 | happened | try_to_date(trim(REFUNDDATE)) — when the contribution was refunded. |

### POLITICS.POLITICS__ST_NYC_CFB_CAMPAIGN_2021_CONTRIBUTIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| CONTRIBUTION_DATE | date (typed) | 2011-03-11 → 2023-12-04 | happened | try_to_date(trim(DATE)) — when the contribution was made; census minimum 2011-03-11 shows real values land here. |
| ELECTION_CYCLE | year only | 2021 → 2021 | span_end | trim(ELECTION) — the election year the money was raised for; the cycle closes in that year. |
| REFUND_DATE | date (typed) | 2017-11-30 → 2024-01-04 | happened | try_to_date(trim(REFUNDDATE)) — when the contribution was refunded. |

### POLITICS.POLITICS__ST_NYC_CFB_CAMPAIGN_2025_CONTRIBUTIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| CONTRIBUTION_DATE | date (typed) | 2014-07-31 → 2025-11-27 | happened | try_to_date(trim(DATE)) — when the contribution was made; census minimum 2014-07-31 shows real values land here. |
| ELECTION_CYCLE | year only | 2025 → 2025 | span_end | trim(ELECTION) — the election year the money was raised for; the cycle closes in that year. |
| REFUND_DATE | date (typed) | 2022-03-25 → 2025-11-27 | happened | try_to_date(trim(REFUNDDATE)) — when the contribution was refunded. |

### POLITICS.POLITICS__TX_LOBBY_AWARDS
| column | format | range | meaning | description |
|---|---|---|---|---|
| APPLICABLEYEAR | year only | 2005 → 2026 | span_start | Kept as trimmed text (no cast) — the calendar year the lobby report applies to; a real year label, but bare-date-parsing it is the epoch-1970 bug class. |
| DUEDT | date (typed) | 2005-02-10 → 2026-07-10 |  |  |
| PERIODENDDT | date (typed) | 2005-01-31 → 2026-06-30 | span_end | try_to_date(...,'YYYYMMDD') — closes the same reporting period. |
| PERIODSTARTDT | date (typed) | 2005-01-01 → 2026-06-01 | span_start | try_to_date(...,'YYYYMMDD') — opens the reporting period the award expenditure falls in; the finest real clock on the table since award rows carry no activity date. |
| RECEIVEDDT | date (typed) | 2005-02-09 → 2026-07-09 |  |  |

### POLITICS.POLITICS__TX_LOBBY_COVER
| column | format | range | meaning | description |
|---|---|---|---|---|
| APPLICABLE_YEAR | year only | 1991 → 2026 | span_start | Raw pass-through of APPLICABLEYEAR with no cast — the calendar year the cover sheet applies to; a real year label, not a date value. |
| DUE_DT | date (typed) | 1992-01-03 → 2027-04-12 | span_end | try_to_date(DUEDT,'YYYYMMDD') — the regulatory deadline that closes the filing window; a real date, but a scheduled deadline rather than an event, and the gap to filed_dt measures lateness. |
| FILED_DT | date (typed) | 1988-08-10 → 2026-08-04 | reported | try_to_date(FILEDDT,'YYYYMMDD') — when the lobby report was filed; the report's own event and the best shared-timeline anchor, with received_dt as a near-duplicate. The 0205-02-28 census minimum is a published typo year, not a cast bug. |
| PERIOD_END_DT | date (typed) | 1991-12-31 → 2026-12-31 | span_end | try_to_date(PERIODENDDT,'YYYYMMDD') — closes that activity period; the census's 2027-04-12 max is a forward-dated period end or a published typo. |
| PERIOD_START_DT | date (typed) | 1991-10-01 → 2026-12-01 | span_start | try_to_date(PERIODSTARTDT,'YYYYMMDD') — opens the activity period the cover sheet reports on. |
| RECEIVED_DT | date (typed) | 1988-08-10 → 2026-08-04 | reported | try_to_date(RECEIVEDDT,'YYYYMMDD') — when the Ethics Commission received the report. |

### POLITICS.POLITICS__TX_LOBBY_DOCKETS
| column | format | range | meaning | description |
|---|---|---|---|---|
| APPLICABLEYEAR | year only | 2001 → 2026 | span_start | Trimmed text year the docket designation applies to; a real year label, uncast. |
| DUEDT | date (typed) | 2001-06-11 → 2027-01-11 |  |  |
| PERIODENDDT | date (typed) | 2001-05-31 → 2026-07-14 | span_end | try_to_date(...,'YYYYMMDD') — closes the same reporting period. |
| PERIODSTARTDT | date (typed) | 2001-05-01 → 2026-01-01 | span_start | try_to_date(...,'YYYYMMDD') — opens the reporting period the docket line falls in; the finest clock available on this table. |
| RECEIVEDDT | date (typed) | 2001-06-07 → 2026-07-14 |  |  |

### POLITICS.POLITICS__TX_LOBBY_ENTERTAINMENT
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACTIVITYDATE | date (typed) | 2005-01-01 → 2026-06-15 | happened | try_to_date(ACTIVITYDATE,'YYYYMMDD') — the day the entertainment was actually provided to the official; the true event clock. |
| APPLICABLEYEAR | year only | 2005 → 2026 | span_start | Trimmed text year the report applies to; a real year label, uncast. |
| DUEDT | date (typed) | 2005-02-10 → 2026-07-10 |  |  |
| PERIODENDDT | date (typed) | 2005-01-31 → 2026-06-30 | span_end | try_to_date(...,'YYYYMMDD') — closes that reporting period. |
| PERIODSTARTDT | date (typed) | 2005-01-01 → 2026-06-01 | span_start | try_to_date(...,'YYYYMMDD') — opens the reporting period containing the entertainment expenditure. |
| RECEIVEDDT | date (typed) | 2005-02-04 → 2026-07-10 |  |  |

### POLITICS.POLITICS__TX_LOBBY_EVENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACTIVITYDATE | date (typed) | 2005-01-10 → 2026-06-04 | happened | try_to_date(ACTIVITYDATE,'YYYYMMDD') — the day the ceremony or reception for officials was held; the true event clock. |
| APPLICABLEYEAR | year only | 2005 → 2026 | span_start | Trimmed text year the report applies to; a real year label, uncast. |
| DUEDT | date (typed) | 2005-03-10 → 2026-07-10 |  |  |
| PERIODENDDT | date (typed) | 2005-02-28 → 2026-06-30 | span_end | try_to_date(...,'YYYYMMDD') — closes that reporting period. |
| PERIODSTARTDT | date (typed) | 2005-01-01 → 2026-06-01 | span_start | try_to_date(...,'YYYYMMDD') — opens the reporting period containing the event expenditure. |
| RECEIVEDDT | date (typed) | 2005-06-29 → 2026-07-10 |  |  |

### POLITICS.POLITICS__TX_LOBBY_FOOD_BEVERAGE
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACTIVITYDATE | date (typed) | 2004-11-02 → 2026-06-23 | happened | try_to_date(ACTIVITYDATE,'YYYYMMDD') — the day the meal was bought for the state official; the true event clock. |
| APPLICABLEYEAR | year only | 2004 → 2026 | span_start | Trimmed text year the report applies to; a real year label, uncast. |
| DUEDT | date (typed) | 2005-01-10 → 2026-07-10 |  |  |
| PERIODENDDT | date (typed) | 2004-12-31 → 2026-06-30 | span_end | try_to_date(...,'YYYYMMDD') — closes that reporting period. |
| PERIODSTARTDT | date (typed) | 2004-01-01 → 2026-06-01 | span_start | try_to_date(...,'YYYYMMDD') — opens the reporting period containing the food and beverage spend. |
| RECEIVEDDT | date (typed) | 2005-01-07 → 2026-07-10 |  |  |

### POLITICS.POLITICS__TX_LOBBY_GIFTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| APPLICABLEYEAR | year only | 2004 → 2026 | span_start | Trimmed text year the report applies to; a real year label, uncast. |
| DUEDT | date (typed) | 2005-01-10 → 2026-07-10 |  |  |
| PERIODENDDT | date (typed) | 2004-12-31 → 2026-06-30 | span_end | try_to_date(...,'YYYYMMDD') — closes that reporting period. |
| PERIODSTARTDT | date (typed) | 2004-01-01 → 2026-06-01 | span_start | try_to_date(...,'YYYYMMDD') — opens the reporting period containing the gift; gift rows carry no activity date, so this is the finest clock here. |
| RECEIVEDDT | date (typed) | 2005-01-05 → 2026-07-02 |  |  |

### POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING
| column | format | range | meaning | description |
|---|---|---|---|---|
| APPLICABLEYEAR | year only | 2000 → 2026 | span_start | Trimmed text year the report applies to; a real year label, uncast. |
| DUEDT | date (typed) | 2000-08-10 → 2027-01-11 |  |  |
| PERIODENDDT | date (typed) | 2000-07-31 → 2026-12-31 | span_end | try_to_date(...,'YYYYMMDD') — closes that reporting period. |
| PERIODSTARTDT | date (typed) | 2000-07-01 → 2026-07-01 | span_start | try_to_date(...,'YYYYMMDD') — opens the reporting period the on-behalf-of line falls in; the finest clock on this table. |
| RECEIVEDDT | date (typed) | 2000-09-08 → 2026-08-04 |  |  |

### POLITICS.POLITICS__TX_LOBBY_SUBJECT_MATTER
| column | format | range | meaning | description |
|---|---|---|---|---|
| APPLICABLEYEAR | year only | 1999 → 2026 | span_start | Trimmed text year the report applies to; a real year label, uncast. |
| DUEDT | date (typed) | 1999-09-10 → 2027-04-12 |  |  |
| PERIODENDDT | date (typed) | 1999-08-31 → 2026-12-31 | span_end | try_to_date(...,'YYYYMMDD') — closes that reporting period; the 2027-04-12 census max is a forward-dated or typo period end. |
| PERIODSTARTDT | date (typed) | 1999-08-01 → 2026-07-01 | span_start | try_to_date(...,'YYYYMMDD') — opens the reporting period the subject-matter line belongs to; the finest clock on this table. |
| RECEIVEDDT | date (typed) | 2001-01-10 → 2026-08-04 |  |  |

### POLITICS.POLITICS__TX_LOBBY_TRANSPORTATION
| column | format | range | meaning | description |
|---|---|---|---|---|
| APPLICABLEYEAR | year only | 2004 → 2026 | span_start | Trimmed text year the report applies to; a real year label, uncast. |
| ARRIVALDT | date (typed) | 2004-12-02 → 2026-06-18 |  |  |
| CHECKINDT | date (typed) | 2000-02-06 → 2028-06-26 |  |  |
| CHECKOUTDT | date (typed) | 2004-12-03 → 2026-06-18 |  |  |
| DEPARTUREDT | date (typed) | 2004-12-01 → 2026-06-18 |  |  |
| DUEDT | date (typed) | 2005-01-10 → 2026-07-10 |  |  |
| PERIODENDDT | date (typed) | 2004-12-31 → 2026-06-30 | span_end | try_to_date(...,'YYYYMMDD') — closes that reporting period; the 2028-06-26 census max is a forward-dated or typo period end worth a look. |
| PERIODSTARTDT | date (typed) | 2004-01-01 → 2026-06-01 | unclear | try_to_date(...,'YYYYMMDD') — opens the reporting period the travel leg falls in; travel rows carry no activity date, so this is the finest clock here. |
| RECEIVEDDT | date (typed) | 2005-01-05 → 2026-07-10 |  |  |

### POLITICS.POLITICS__VOTEVIEW_ROLLCALLS
| column | format | range | meaning | description |
|---|---|---|---|---|
| VOTE_DATE | date (typed) | 2023-01-03 → 2026-06-25 | happened | The day the roll-call vote was taken; staging parses it with an explicit try_to_date(...,'YYYY-MM-DD') after sampling the landed format on 2026-08-11. |

### POLITICS.POLITICS__WHO_WON
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 1976 → 2024 |  |  |

### POLITICS.POLITICS__XC_JCS_MEDIANS
| column | format | range | meaning | description |
|---|---|---|---|---|
| TERM | year only | 1936 → 2023 | happened | Supreme Court TERM label (a year number in the Judicial Common Space files), sitting beside year and congress; raw uncast passthrough - a SCOTUS term straddles Oct-Sep, so it is not a clean calendar year. |
| YEAR | year only | 1924 → 2024 | happened | Observation year of an annual institution-ideology panel (102 rows, roughly one per year); try_to_number(YEAR) integer. |

### POLITICS.POLITICS__XC_JCS_SCOTUS
| column | format | range | meaning | description |
|---|---|---|---|---|
| TERM | year only | 1937 → 2022 | happened | Supreme Court term the justice's ideology score belongs to (782 rows = justice x term) - the only time-shaped column on the table; raw uncast passthrough year number, and a SCOTUS term runs Oct-Sep so it is not exactly a calendar year. |

### POLITICS.POLITICS__XC_OWID_CPI
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 2012 → 2024 | happened | Observation year of the annual Corruption Perceptions Index country panel; try_to_number(YEAR) integer, year grain only. |

### PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACTIVATION_DATE | date (typed) | 1908-04-20 → 2026-08-06 | span_start | Day the debarment/suspension took effect - it opens the exclusion period the model itself describes ('and for how long?') and is cast try_to_date(...,'YYYY-MM-DD'); the census's 1908 minimum is a source typo, not a parse bug. |
| TERMINATION_DATE | date (typed) | 2026-03-02 → 2035-12-29 | span_end | Day the exclusion lapses - the parsed half of the pair, NULL on the ~95% 'Indefinite' rows; the census's 2227 max and 1,690 far-future rows are real source placeholder dates for effectively permanent debarments. |
| TERMINATION_DATE_RAW | date as text (iso) | 2026-03-02 → 2035-12-29 | not_a_date | FALSE POSITIVE - the model header states this is the LITERAL TEXT 'Indefinite' on about 95% of rows; it is the uncast string kept beside the parsed column, so it is mostly not a date at all. |

### PROCUREMENT.PROCUREMENT__FED_USASPENDING_BULK
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACTION_DATE | date as text (iso) | 2026-05-26 → 2026-06-04 | happened | Day the contract action (award or modification) was signed - the transaction event and part of the table's uniqueness key; NOTE the staging model states plainly 'Casts kept as landed (TEXT)', so this is an UNCAST date string. |
| ACTION_DATE_FISCAL_YEAR | year only | 2026 → 2026 | not_a_date | THE KNOWN TRAP - a bare 4-digit FISCAL-year label ('2012') landed as TEXT; it is not a calendar date (federal FY runs Oct-Sep), it is redundant with action_date on the same row, and a bare date-parse reads it as epoch seconds and collapses every row to 1970-01-01. |
| ORDERING_PERIOD_END_DATE | date as text (iso) | 2007-10-30 → 2035-11-30 | span_end | Last day orders can be placed against the vehicle (IDV ordering window) - a different span from the performance period; uncast TEXT. |
| PERIOD_OF_PERFORMANCE_CURRENT_END_DATE | date as text (iso) | 2007-09-30 → 2035-05-09 | span_end | Closes the currently-exercised period of performance; legitimately in the future for live contracts; uncast TEXT. |
| PERIOD_OF_PERFORMANCE_POTENTIAL_END_DATE | date as text (iso) | 2007-09-30 → 2035-12-31 | span_end | Closes the period of performance if every option is exercised - a HYPOTHETICAL end, always at or after the current end; uncast TEXT. |
| PERIOD_OF_PERFORMANCE_START_DATE | date as text (iso) | 1981-01-25 → 2027-06-14 | span_start | Opens the contract's period of performance; uncast TEXT per the staging header. |
| SOLICITATION_DATE | date as text (iso) | 1977-05-11 → 2026-06-04 | happened | Day the agency issued the solicitation that led to this award - a real event earlier than action_date, so the gap is a procurement-speed measure; uncast TEXT and sparsely populated in FPDS. |

### PROCUREMENT.PROCUREMENT__FED_USASPENDING_SUBAWARDS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACTION_DATE | date (typed) | 2008-08-01 → 2026-05-29 | happened | Day the subaward action occurred, pulled from the JSON record with try_to_date; the census max of 2026-06-10 16:00:23.716 carries a millisecond time and must have bled in from _ingested_at, since this column is date-typed. |

### PROCUREMENT.PROCUREMENT__INTL_EC_SERCOP
| column | format | range | meaning | description |
|---|---|---|---|---|
| AWARD_DATE | date (typed) | 2023-12-20 → 2026-06-05 | decided | Day the buying authority awarded the contract - the authority's ruling; try_to_date(AWARD_DATE) in staging. |
| CONTRACT_DATE_SIGNED | date (typed) | 2023-12-26 → 2026-12-17 | happened | Day the contract was actually signed - the real-world event the row exists to record; try_to_date(CONTRACT_DATESIGNED) in staging; note the census's 2026-12-17 max is beyond today, so at least one date column here carries future or bad values worth a real query later. |
| RECORD_DATE | date (typed) | 2025-01-01 → 2026-06-05 | reported | The OCDS record's own release date - when SERCOP published or refreshed this contracting record, not when anything happened; try_to_date(DATE) in staging. |

### REFERENCE.REFERENCE__FED_DHS_HIFLD
| column | format | range | meaning | description |
|---|---|---|---|---|
| SOURCE_DATE | date (typed) | 2014-06-12 → 2021-05-26 | reported | try_to_date(left(nullif(trim(SOURCE_DATE),''),10)) in staging: the date of the underlying source the facility record was compiled from, i.e. the vintage of the data rather than anything the facility did; the only candidate on a 500-row SAMPLE table that is explicitly not the full dataset. |

### REFERENCE.REFERENCE__FED_ITIS_COMMENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| COMMENT_TIME_STAMP | datetime (typed) | 1996-06-13 14:51:08.000 → 2026-07-28 12:30:13.000 | happened | try_to_timestamp_ntz(trim(COMMENT_TIME_STAMP)) in staging: when the curator wrote the comment - the row IS the comment, so its creation is the event itself; census min 1996-06-13 14:51:08 matches ITIS's founding era. |
| UPDATE_DATE | date (typed) | 1996-06-17 → 2026-07-28 | reported | try_to_date(trim(UPDATE_DATE),'YYYY-MM-DD'): ITIS's own record-last-modified date - the upstream register's clock, NOT Ripple's loader, which is the separate _loaded_at column that supplies the census's 2026-08-08 04:44:10.570840 maximum. |

### REFERENCE.REFERENCE__FED_ITIS_EXPERTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| UPDATE_DATE | date (typed) | 1998-04-28 → 2024-06-25 | reported | same ITIS pattern verified in the sibling staging models: try_to_date(trim(UPDATE_DATE),'YYYY-MM-DD'), the date ITIS curators last touched this expert record - the only clock this 197-row table has, and it is the register's, not Ripple's. |

### REFERENCE.REFERENCE__FED_ITIS_GEOGRAPHIC_DIV
| column | format | range | meaning | description |
|---|---|---|---|---|
| UPDATE_DATE | date (typed) | 1900-01-01 → 2026-07-28 | reported | the ITIS UPDATE_DATE pattern (try_to_date with an explicit YYYY-MM-DD format in every sibling staging model): when curators last touched this taxon-by-region row; note the census minimum is exactly 1900-01-01, which reads as a placeholder rather than a real edit. |

### REFERENCE.REFERENCE__FED_ITIS_JURISDICTION
| column | format | range | meaning | description |
|---|---|---|---|---|
| UPDATE_DATE | date (typed) | 1997-10-27 → 2026-07-28 | reported | the ITIS UPDATE_DATE pattern: when curators last touched this taxon-by-jurisdiction row; the only clock the table carries, and it dates the register's curation, not the species. |

### REFERENCE.REFERENCE__FED_ITIS_KINGDOMS
| column | format | range | meaning | description |
|---|---|---|---|---|
| UPDATE_DATE | date (typed) | 1996-03-26 → 2014-08-20 | reported | the ITIS UPDATE_DATE pattern on a 7-row lookup of the kingdoms of life: the curator edit date, the table's only clock and of essentially no timeline value at this grain. |

### REFERENCE.REFERENCE__FED_ITIS_NODC_IDS
| column | format | range | meaning | description |
|---|---|---|---|---|
| UPDATE_DATE | date (typed) | 1996-06-24 → 1997-03-10 | reported | the ITIS UPDATE_DATE pattern on the legacy NODC-to-TSN crosswalk: when curators last touched the mapping row. |

### REFERENCE.REFERENCE__FED_ITIS_OTHER_SOURCES
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACQUISITION_DATE | date (typed) | 1996-01-01 → 2026-04-17 | happened | try_to_date(trim(ACQUISITION_DATE),'YYYY-MM-DD') in staging: when ITIS acquired the cited database or website - a real acquisition event on a row that IS a source, so it beats update_date as the anchor. |
| UPDATE_DATE | date (typed) | 1996-07-29 → 2026-07-28 | reported | try_to_date(trim(UPDATE_DATE),'YYYY-MM-DD'): ITIS's record-last-modified date for this source entry - upstream curation, not Ripple's _loaded_at. |

### REFERENCE.REFERENCE__FED_ITIS_PUBLICATIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ACTUAL_PUB_DATE | date (typed) | 1753-01-01 → 2026-07-15 | happened | try_to_date(trim(ACTUAL_PUB_DATE),'YYYY-MM-DD') in staging: the real publication date of the cited work - on a bibliographic table the publication IS the event, so this is the honest anchor. |
| LISTED_PUB_DATE | date (typed) | 1753-01-01 → 2026-07-15 | happened | try_to_date(trim(LISTED_PUB_DATE),'YYYY-MM-DD'): the publication date as printed on the work; the census minimum is exactly 1753-01-01, which is genuine (Linnaeus, the start of botanical nomenclature) but its January-1 shape says many entries are year-only padded to Jan 1, so year is the honest grain. |
| UPDATE_DATE | date (typed) | 1997-07-01 → 2026-07-28 | reported | try_to_date(trim(UPDATE_DATE),'YYYY-MM-DD'): ITIS's record-last-modified date; note the census counted 255 epoch-1970 rows on this table, and because all three date columns use an EXPLICIT format those must be literal '1970-01-01' sentinels in the source, not a cast bug. |

### REFERENCE.REFERENCE__FED_ITIS_REFERENCE_LINKS
| column | format | range | meaning | description |
|---|---|---|---|---|
| UPDATE_DATE | date (typed) | 1996-11-12 → 2026-07-28 | reported | the ITIS UPDATE_DATE pattern on the 1.97M-row taxon-to-document bridge: when curators last touched the link row - the register's clock, the table's only one. |

### REFERENCE.REFERENCE__FED_ITIS_SYNONYM_LINKS
| column | format | range | meaning | description |
|---|---|---|---|---|
| UPDATE_DATE | date (typed) | 1996-06-24 → 2026-07-28 | reported | the ITIS UPDATE_DATE pattern on the synonym-to-accepted-TSN mapping: when curators last recorded or revised this synonymy. |

### REFERENCE.REFERENCE__FED_ITIS_TAXONOMIC_UNITS
| column | format | range | meaning | description |
|---|---|---|---|---|
| INITIAL_TIME_STAMP | datetime (typed) | 1996-06-13 14:51:08.000 → 2026-07-28 12:29:46.000 | reported | try_to_timestamp_ntz(trim(INITIAL_TIME_STAMP)) in staging: when ITIS first recorded this taxon; the taxon itself long predates the record, so this is the register reporting, and it beats update_date as an anchor because it does not drift with later edits. |
| UPDATE_DATE | date (typed) | 1996-06-24 → 2026-07-28 | reported | try_to_date(trim(UPDATE_DATE),'YYYY-MM-DD'): when curators last revised the taxon record - a moving target, so it is the weaker of the two anchors. |

### REFERENCE.REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP
| column | format | range | meaning | description |
|---|---|---|---|---|
| UPDATE_DATE | date (typed) | 1996-06-13 → 2026-07-28 | reported | the ITIS UPDATE_DATE pattern on the taxon-author lookup: the curator edit date, the only clock present. |

### REFERENCE.REFERENCE__FED_ITIS_TAXON_UNIT_TYPES
| column | format | range | meaning | description |
|---|---|---|---|---|
| UPDATE_DATE | date (typed) | 1996-06-13 → 2024-07-18 | reported | the ITIS UPDATE_DATE pattern on a 182-row rank-definition lookup: the curator edit date, of little timeline value at this grain. |

### REFERENCE.REFERENCE__FED_ITIS_TU_COMMENTS_LINKS
| column | format | range | meaning | description |
|---|---|---|---|---|
| UPDATE_DATE | date (typed) | 1996-06-17 → 2026-07-28 | reported | the ITIS UPDATE_DATE pattern on the taxon-to-comment bridge: the curator edit date, the table's only clock. |

### REFERENCE.REFERENCE__FED_ITIS_VERNACULARS
| column | format | range | meaning | description |
|---|---|---|---|---|
| UPDATE_DATE | date (typed) | 1997-08-20 → 2026-07-28 | reported | try_to_date(trim(UPDATE_DATE),'YYYY-MM-DD') in staging: when curators last touched this common-name row - the only clock the table has. |

### REFERENCE.REFERENCE__FED_ITIS_VERN_REF_LINKS
| column | format | range | meaning | description |
|---|---|---|---|---|
| UPDATE_DATE | date (typed) | 1900-01-01 → 2026-07-28 | reported | the ITIS UPDATE_DATE pattern on the vernacular-name-to-document bridge; as with geographic_div the census minimum is exactly 1900-01-01, which reads as a placeholder rather than a real edit date. |

### REFERENCE.REFERENCE__FED_USGS_GNIS_ALL_NAMES
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_CREATED | date (typed) | 1700-12-31 → 2026-06-29 | span_start | try_to_date(trim(DATE_CREATED)) bare cast: when the name record was created in GNIS, which pairs with ending_date as the name's validity window - though it could equally be read as pure record-creation (a reported clock), which is why confidence is low; the census min of 1700-12-31 also looks like a rollover artifact. |
| ENDING_DATE | date (typed) | 2000-01-01 → 2020-08-01 | span_end | try_to_date(trim(ENDING_DATE)) bare cast: when the name stopped applying to the feature - the closing bound of the name's validity window. |
| PUBLICATION_DATE | date (typed) | 1700-12-31 → 2023-03-17 | reported | try_to_date(trim(PUBLICATIONDATE)) with NO format string: the publication date of the map or document that cites this name, and since one row IS one name-citation this dates the attestation; WARNING - the bare cast is the epoch trap, year-only strings parse as epoch seconds, which is almost certainly the census's 225 epoch-1970 rows behind the CORRUPT_RANGE verdict. |

### REFERENCE.REFERENCE__FED_USGS_TOPOVIEW
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATECREATED | date (typed) | 2018-02-18 → 2025-03-26 | reported | try_to_date(DATECREATED) in the mart: when USGS created the digital product record; this and lastupdated are the ONLY source of the census's whole 2018-02-18 to 2025-09-22 range, i.e. the scanning programme's clock, not the maps'. |
| LASTUPDATED | date (typed) | 2025-09-17 → 2025-09-22 | reported | try_to_date(LASTUPDATED) in the mart: when the USGS product record was last revised - source-side bookkeeping about the digital file. |
| PUBLICATIONDATE | date as text (iso) | 1943-01-01 → 1994-01-01 | happened | raw passthrough with NO cast in the mart: the original publication date of the historical topographic map, the only column that dates the MAP rather than its scan; it is unmeasured by the census precisely because it was never typed as a date, and anchoring on datecreated instead would date 19th-century maps to 2018-2025. |

### REFERENCE.REFERENCE__INTL_EUROSTAT
| column | format | range | meaning | description |
|---|---|---|---|---|
| TIME | year only | 2020 → 2023 | unclear | raw passthrough of the SDMX TIME_PERIOD string ("TIME" as time, no cast): the period each observation covers - but the mart also carries a FREQ column, so the shape varies by series (annual / quarterly / monthly) and the real grain cannot be claimed without reading FREQ row by row. |

### REFERENCE.REFERENCE__INTL_GDELT
| column | format | range | meaning | description |
|---|---|---|---|---|
| MONTHYEAR | month-year | 2025 → 2026 | happened | raw passthrough: the same event date in YYYYMM form - month grain by construction, and a number rather than a date. |
| SQLDATE | date as text (yyyymmdd) | 2025-07-02 → 2026-07-02 | happened | raw passthrough with no cast: GDELT's event date in YYYYMMDD form; it is the true event clock and the finest one here, but it is NOT a date type - parsing it needs an explicit 'YYYYMMDD' format, and a bare parse is the documented epoch trap. |
| YEAR | year only | 2025 → 2026 | happened | try_to_number("YEAR") in the mart: the integer year of the event - the coarsest of GDELT's three redundant date encodings. |

### REFERENCE.REFERENCE__XC_OWID_FERTILITY
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 1891 → 2023 | happened | try_to_number("YEAR") in the mart: the year the fertility rate describes, one row per entity-year - an integer, not a date, so a bare date-parse would collapse the whole 19,402-row series onto 1970. |

### REFERENCE.REFERENCE__XC_ROR_RESEARCH_ORGANIZATIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| ESTABLISHED_YEAR | year only | 1700 → 2026 | happened | try_to_number(trim(ESTABLISHED)) in staging: the year the research organisation was founded - the only real-world event on the row, and an integer year rather than a date; confidence is medium because ROR leaves ESTABLISHED blank for a large share of organisations and fill cannot be checked with the warehouse down. |
| RECORD_CREATED_DATE | date (typed) | 2018-11-14 → 2026-08-03 | reported | try_to_date(trim(ADMIN_CREATED_DATE)): when the ROR registry record was created; the census minimum of 2018-11-14 is ROR's own launch, which proves this column dates the registry, not the organisation. |
| RECORD_LAST_MODIFIED_DATE | date (typed) | 2024-12-11 → 2026-08-03 | reported | try_to_date(trim(ADMIN_LAST_MODIFIED_DATE)): when the ROR registry record was last edited - registry maintenance, not an event at the organisation. |

### REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| COMMENTS_CLOSE_ON | date (typed) | 2013-10-28 → 2026-12-31 |  |  |
| DAYS_UNTIL_EFFECTIVE | year only | 1731 → 1731 | not_a_date | The mart computes datediff('day', publication_date, effective_on) - a duration in days, not a point in time. |
| EFFECTIVE_ON | date (typed) | 2010-12-14 → 2033-03-07 | span_start | try_to_date(effective_on) - when the rule starts applying, opening its effective period. Legitimately future-dated: the census max 2033-03-07 with 1 far-future row is a long-lead rule, not corruption. |
| END_PAGE | quarter | 1700 → 2035 | not_a_date | try_to_number(end_page) - the page the document ends on; a page number, not an end time. |
| PUBLICATION_DATE | date (typed) | 2023-01-03 → 2026-06-16 | reported | try_to_date(publication_date) in staging - the day the document appeared in the Federal Register. Publication is a reporting clock, and it is the anchor every derived part on this table is built from. |
| PUBLICATION_QUARTER | date (typed) | 2023-01-01 → 2026-04-01 | reported | The mart computes date_trunc('quarter', publication_date) - a real DATE, but only quarter resolution; do not read it as a day. |
| PUBLICATION_YEAR | year only | 2023 → 2026 | reported | The mart computes year(publication_date) - a coarsened copy of the publication clock. |
| START_PAGE | quarter | 1700 → 2035 | not_a_date | try_to_number(start_page) in staging - the Federal Register page the document starts on; a page number, not a start time. |

### SCIENCE.SCIENCE__FED_NASA_OPEN_DATA
| column | format | range | meaning | description |
|---|---|---|---|---|
| RESPONSE_DATE | date (typed) | 1998-05-02 → 2026-07-02 | happened | try_to_date(RESPONSE_DATE) on a 54-row API crawl; the census range starts 1998-05-02, which rules out a request stamp, so it appears to be the date carried by the item the NASA API returned — meaning unverified, and the model has no description. |

### SCIENCE.SCIENCE__FED_NSF_AWARDS
| column | format | range | meaning | description |
|---|---|---|---|---|
| AWARD_DATE | date (typed) | 2026-01-16 → 2026-07-01 | decided | try_to_date(AWARD_DATE) — when NSF granted the award; an authority acting, and the best anchor on a 125-row sample table. |
| END_DATE | date (typed) | 2027-06-30 → 2031-12-31 | span_end | try_to_date(END_DATE) — closes the period of performance; the 17 far-future rows and the 2031-12-31 census max are legitimately forward-dated grant end dates, not corruption. |
| START_DATE | date (typed) | 2026-09-15 → 2027-03-01 | span_start | try_to_date(START_DATE) — opens the award's period of performance. |

### SCIENCE.SCIENCE__FED_USGS_EARTHQUAKES
| column | format | range | meaning | description |
|---|---|---|---|---|
| TIME | date as text (iso) | 2010-01-01 → 2026-06-13 | happened | The USGS catalog's event origin time — exactly when the quake occurred — but the mart passes "TIME" through with NO cast, so it is an unparsed string today and needs a real timestamp cast; grain is nominally sub-second, capped at day by this scale. |
| UPDATED | date (typed) | 2013-02-27 → 2026-06-28 | reported | try_to_date(UPDATED) — when USGS last revised the catalog record for that quake; publisher record maintenance, and since it is the only DATE-typed column here the census's 2013-2026 range likely describes revisions rather than event times. |

### SCIENCE.SCIENCE__XC_OWID_AI_INCIDENTS_ANNUAL
| column | format | range | meaning | description |
|---|---|---|---|---|
| YEAR | year only | 2012 → 2025 | happened | try_to_number("YEAR") — a genuine calendar year, and on a 14-row annual incident-count series it is the year the incidents occurred; stored as a NUMBER, so a bare date-parse would read 2012 as epoch seconds, the exact bug that collapsed 20M rows onto 1970. |

### SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_NIH_REPORTER
| column | format | range | meaning | description |
|---|---|---|---|---|
| AWARD_NOTICE_DATE | date (typed) | 1999-10-20 → 2026-08-08 | decided | try_to_date on the left 10 characters: the day NIH issued the notice of award, the crisp day-grain moment the money was committed and the best axis for this table (fiscal_year is the coarser fully-populated fallback). |
| BUDGET_END_DATE | date (typed) | 1899-12-31 → 2031-02-28 | span_end | try_to_date on the left 10 characters: the closing bound of the budget period. |
| BUDGET_START_DATE | date (typed) | 1978-03-01 → 2026-08-08 | span_start | try_to_date on the left 10 characters: the opening bound of this application's budget period, a narrower span nested inside the project period. |
| DATE_ADDED | datetime (typed) | 2011-01-01 00:00:00.000 → 2026-08-08 17:03:55.000 | reported | try_to_timestamp_ntz on the date the record first appeared in the public RePORTER database — a publisher-side disclosure stamp (the gap to award_notice_date is a publication lag), not the award event and not Ripple's loader. |
| FISCAL_YEAR | year only | 2000 → 2026 | happened | try_to_number on the NIH fiscal year of the award (Oct-Sep, so offset from calendar time); it is the fully populated year-grain fallback but too coarse to be the table's primary clock. |
| PROJECT_END_DATE | date (typed) | 1987-05-31 → 2035-09-29 | span_end | try_to_date on the left 10 characters: the closing bound of the project period, and the plausible source of the census's 445 non-ingest far-future values since multi-year grants legitimately end past 2030. |
| PROJECT_START_DATE | date (typed) | 1965-06-01 → 2026-08-25 | span_start | try_to_date on the left 10 characters of an ISO string: the opening bound of the funded project's period, paired with project_end_date. |

### SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_RETRACTION_WATCH
| column | format | range | meaning | description |
|---|---|---|---|---|
| ORIGINAL_PAPER_DATE | date (typed) | 1753-01-01 → 2026-05-04 | happened | Same explicit 'MM/DD/YYYY' cast: the day the original paper was published, the antecedent event — the gap to retraction_date is the response lag, and genuinely old papers explain the 1753 census floor (15 epoch-1970 values are the suspect part). |
| RETRACTION_DATE | date (typed) | 1756-06-24 → 2026-07-17 | decided | try_to_date with an explicit 'MM/DD/YYYY' format after splitting the time off 'M/D/YYYY H:MM' text: the day the journal or publisher issued the retraction, which is the event this row IS. |

### SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS
| column | format | range | meaning | description |
|---|---|---|---|---|
| AWARD_YEAR | year only | 1983 → 2026 | happened | try_to_number on the award year, which the staging model also uses as part of the surrogate key: the year the award was made, at year grain. |
| CONTRACT_END_DATE | date (typed) | 1905-07-02 → 2032-09-12 | span_end | try_to_date: the closing bound of the award's period of performance. |
| DATE_OF_NOTIFICATION | date (typed) | 1900-02-01 → 2025-11-03 | decided | try_to_date on the day the applicant was notified of the agency's decision — the communication of the ruling, usually at or after proposal_award_date. |
| PROPOSAL_AWARD_DATE | date (typed) | 1905-07-01 → 2026-12-20 | decided | try_to_date with no format on the day the agency awarded the contract — the row's own dated event, but the bare cast lets junk source values through, which is why the census shows a 0001-01-01 floor and a 5025-05-05 ceiling (3 far-future values). |
| PROPOSAL_RECEIPT_DATE | date (typed) | 1987-01-01 → 2025-10-17 | reported | try_to_date on the day the agency received the proposal — a receipt date, the textbook 'reported' clock. |
| SOLICITATION_CLOSE_DATE | date (typed) | 1989-01-01 → 2025-11-05 | span_end | try_to_date on the day the solicitation window closed — the deadline bound of the application period, not an action on this award. |
| SOLICITATION_YEAR | year only | 1985 → 2025 | reported | try_to_number on the year the agency issued the solicitation this proposal answered — an attribute of the solicitation, one step before the award. |

### SCIENCE_RESEARCH.SCIENCE_RESEARCH__XC_BIORXIV_MEDRXIV
| column | format | range | meaning | description |
|---|---|---|---|---|
| DAYS_PREPRINT_TO_PUBLICATION | year only | 1795 → 1795 | not_a_date | The mart computes it as datediff('day', coalesce(preprint_date, preprint_posted_date), published_date) — a duration in days, proven in the SQL. |
| PREPRINT_DATE | date (typed) | 2021-06-18 → 2026-05-06 | reported | try_to_date on the posting date as reported by the publication-link endpoint — the same posting event seen from a second endpoint, which is why the mart coalesces it with preprint_posted_date. |
| PREPRINT_POSTED_DATE | date (typed) | 2026-05-18 → 2026-05-18 | reported | try_to_date on the API's 'date' field: the day the preprint was posted to bioRxiv/medRxiv, the row's own public-disclosure event and the first term in the mart's own preprint-to-publication datediff. |
| PUBLISHED_DATE | date (typed) | 2026-05-18 → 2026-06-01 | reported | try_to_date on the day the peer-reviewed journal version appeared — a publication date later than the preprint posting. |

### SCIENCE_RESEARCH.SCIENCE_RESEARCH__XC_OSF_REGISTRATIONS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_CREATED | datetime (typed) | 2025-12-12 14:24:31.823 → 2026-08-08 01:49:36.351 | reported | try_to_timestamp_ntz on OSF's attributes.date_created: when the researcher created the object on the platform, earlier than the registration itself. |
| DATE_MODIFIED | datetime (typed) | 2026-07-31 03:49:36.983 → 2026-08-08 01:42:16.104 | ingest | try_to_timestamp_ntz on OSF's attributes.date_modified: a mutable record last-touched stamp that tells you when the row was last edited, not when anything happened. |
| DATE_REGISTERED | datetime (typed) | 2025-12-12 14:24:31.802 → 2026-08-08 01:49:36.333 | reported | try_to_timestamp_ntz on attributes.date_registered: the moment the preregistration was frozen and posted to the public registry — the event this row IS; note the mart is an explicit 10-row proof slice, not the full dataset. |
| EMBARGO_END_DATE | datetime (typed) | 2029-01-01 00:00:00.000 → 2029-01-01 00:00:00.000 | span_end | try_to_timestamp_ntz on attributes.embargo_end_date: the closing bound of the embargo period during which the registration stays private, which legitimately explains the 2029-01-01 census max. |

### SCIENCE_RESEARCH.SCIENCE_RESEARCH__XC_RETRACTION_WATCH_DATABASE
| column | format | range | meaning | description |
|---|---|---|---|---|
| ORIGINAL_PAPER_DATE | date (typed) | 1753-01-01 → 2026-05-04 | happened | Same explicit 'MM/DD/YYYY' cast: the original paper's publication day, the antecedent whose distance from retraction_date is the response lag; the 1753 floor is genuinely old scholarship, the 15 epoch-1970 values are not. |
| RETRACTION_DATE | date (typed) | 1756-06-24 → 2026-07-17 | decided | try_to_date with an explicit 'MM/DD/YYYY' format after splitting the time off 'M/D/YYYY H:MM' text (the staging model documents that format): the day the retraction was issued, the row's own event. |

### TRANSPORT.TRANSPORT__FED_FAA_AIRCRAFT_REGISTRY
| column | format | range | meaning | description |
|---|---|---|---|---|
| AIRWORTHINESS_DATE | date (typed) | 1920-12-09 → 2026-07-09 | decided | try_to_date with explicit 'YYYYMMDD': the day the airworthiness certificate was issued; the staging comment records that the 2,325 rows landing in 1970 were checked live on 2026-08-18 and are genuinely old aircraft spread over ~230 distinct days, not sentinel garbage. |
| CERT_ISSUE_DATE | date (typed) | 1940-12-26 → 2026-08-07 | decided | try_to_date with explicit 'YYYYMMDD': the day the FAA issued this registration certificate, the record's own dated event and the only near-fully-populated day-grain column here. |
| EXPIRATION_DATE | date (typed) | 2018-02-28 → 2033-08-31 | span_end | try_to_date with explicit 'YYYYMMDD': the end of the current registration's validity period, which is why the census counted 64,406 'far future' rows (2027-2033 expiries) — legitimate, not corruption. |
| LAST_ACTION_DATE | date (typed) | 1971-11-24 → 2026-08-07 | decided | try_to_date with an explicit 'YYYYMMDD' format: the date the FAA last processed an action on the registration record, i.e. the agency acting, though it can also be read as a record-currency stamp. |
| YEAR_MFR | year only | 1909 → 2026 | happened | try_to_number on a 4-digit year string: the year the airframe was manufactured, a real-world event but an attribute of the aircraft rather than of the registration record (staging header notes it is blank on ~22% of rows). |

### TRANSPORT.TRANSPORT__FED_FAA_REGISTRY
| column | format | range | meaning | description |
|---|---|---|---|---|
| AIR_WORTH_DATE | date (typed) | 1970-08-11 → 1970-08-23 | decided | The airworthiness certificate issue date, destroyed by the same bare try_to_date on 'YYYYMMDD'; the live replacement table spells the same field airworthiness_date and casts it correctly. |
| CERT_ISSUE_DATE | date (typed) | 1970-08-13 → 1970-08-23 | decided | The registration certificate issue date, destroyed by the same bare try_to_date on 'YYYYMMDD' — values in this mart are epoch-collapsed and unusable as landed. |
| EXPIRATION_DATE | date (typed) | 1970-08-22 → 1970-08-24 | span_end | The end of the registration's validity window, also epoch-collapsed by the bare try_to_date — note the census saw zero far-future rows here precisely because every expiry got crushed into August 1970. |
| LAST_ACTION_DATE | date (typed) | 1970-08-17 → 1970-08-23 | decided | Semantically the FAA's last action on the registration, but the mart calls bare try_to_date on an 8-digit 'YYYYMMDD' string so Snowflake read it as epoch seconds — this is one of the four columns behind the table's 1,199,875 epoch-1970 values and its absurd 1970-08-11..1970-08-24 census range. |
| YEAR_MFR | year only | 1909 → 2026 | happened | Passed through as a raw varchar year with no cast, so it escaped the epoch bug that destroyed all four date columns on this table and is the only honest time value left on it — the year the airframe was built. |

### TRANSPORT.TRANSPORT__FED_FRA_CASUALTIES
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE | date (typed) | 1997-01-01 → 2026-05-31 | happened | try_to_date with an explicit 'MM/DD/YYYY' format — the full calendar date the casualty occurred, and the one column that puts one row (one reported casualty) on a shared timeline. |
| INCIDENT_YEAR | year only | 1975 → 2026 | happened | try_to_number on a comma-stripped string: the year the casualty occurred, part of the FRA report key alongside railroad code and incident number. |

### TRANSPORT.TRANSPORT__FED_FRA_CROSSING_INCIDENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE | date (typed) | 1975-01-01 → 2026-05-31 | happened | try_to_date with an explicit 'MM/DD/YYYY' format — the calendar date of the crossing collision and the only full date on the table. |
| REPORT_YEAR | year only | 1975 → 2026 | reported | Uncast varchar sitting with the reporting railroad's identifiers: the FRA reporting year of the filing rather than the year the collision happened. |

### TRANSPORT.TRANSPORT__FED_FRA_EQUIPMENT_ACCIDENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE | date (typed) | 1975-01-01 → 2026-05-31 | happened | try_to_date with an explicit 'MM/DD/YYYY' format — the calendar date of the equipment accident; note the table repeats one accident per reporting railroad, so counts on this clock double-count multi-railroad events. |
| YEAR | year only | 1975 → 2026 | reported | Uncast varchar sandwiched between reporting_railroad_name and accident_number, i.e. the reporting-year element of the FRA report key rather than the accident's own year (which is accident_year). |

### TRANSPORT.TRANSPORT__FED_FRA_RAIL_DEATHS_BY_RAILROAD
| column | format | range | meaning | description |
|---|---|---|---|---|
| INCIDENT_YEAR | year only | 1975 → 2026 | happened | The mart derives it from the casualty table's incident_year with two-digit years normalized ('20' to 2020), it carries a not_null test and is part of the model's unique key, so it is a real fully-populated year of death. |

### TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT
| column | format | range | meaning | description |
|---|---|---|---|---|
| DATE_LAST_INSP | date (typed) | 1980-06-20 → 2026-07-15 | happened | try_to_date on the left 10 characters of an ISO string: the date the aircraft's last inspection actually took place, and the only real-world event date on this table — the crash date itself lives on the events table via ev_id. |
| LCHG_DATE | date (typed) | 2020-09-25 → 2026-07-31 | ingest | NTSB's own 'last change' stamp on the database row (it sits next to lchg_userid on the sibling injury model): record-maintenance bookkeeping that says when the row was last edited, never when anything happened — mistaking it for an event clock is the exact failure this index exists to prevent. |

### TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_EVENTS
| column | format | range | meaning | description |
|---|---|---|---|---|
| EV_DATE | date (typed) | 2008-01-01 → 2026-07-29 | happened | try_to_date on the left 10 characters of an ISO string: the date the aviation accident or incident occurred, one row per event, which is the table's true clock. |
| EV_YEAR | year only | 2008 → 2026 | happened | Uncast varchar year of the accident, a redundant decomposition of ev_date. |
| LCHG_DATE | date (typed) | 2020-09-25 → 2026-07-31 | ingest | NTSB's own last-change stamp on the database row: bookkeeping about when the record was last edited, not about the accident. |

### TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_INJURY
| column | format | range | meaning | description |
|---|---|---|---|---|
| LCHG_DATE | date (typed) | 2020-09-25 → 2026-07-31 | ingest | The staging model pairs it with lchg_userid, confirming it is NTSB's record last-edited stamp; the census range starting 2020-09-25 on injuries from decades of accidents proves it tracks database edits, not events, so this table has no clock of its own — join to the events mart on ev_id for ev_date. |

### UNCATEGORIZED.UNCATEGORIZED__FED_FEC_LEADERSHIP_PAC
| column | format | range | meaning | description |
|---|---|---|---|---|
| CAND_ELECTION_YR | year only | 1980 → 2034 |  |  |
| FEC_ELECTION_YR | year only | 2024 → 2024 |  |  |
