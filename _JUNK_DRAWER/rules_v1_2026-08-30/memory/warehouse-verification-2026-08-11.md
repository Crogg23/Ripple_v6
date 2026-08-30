---
name: warehouse-verification-2026-08-11
description: "First full accuracy audit of all 558 sources — 71% verifiably complete, ~50 broken; ranked defect list lives in reports/warehouse_verification_2026-08-11.md"
metadata: 
  node_type: memory
  type: project
  originSessionId: 22667980-1cab-42b8-9f42-fe69c155f9cf
  modified: 2026-08-11T15:36:02.436Z
---

2026-08-11 verification session measured (not fixed) questions 5-10 of the
nine-defect frame across all 558 modeled sources. Headline: 16/18 publisher
spot-checks match exactly; 128/181 findable-total sources complete; 33.5M exact
duplicate rows; ~50 sources materially wrong.

Top defects (repair order for next sessions): FHFA NMDB = 7,204 real rows
duplicated to 19M (runaway pager); NCUA call reports loaded the account-
description dictionary sheet instead of data; FAA registry N_NUMBER 100% blank
plus all 4 date columns YYYYMMDD-as-epoch (1970-08); CFTC COT AS_OF date column
100% epoch (other date column fine); ForeignAssistance 97.6% dups; 8 openFDA
landing tables truncated while marts full (raw copies lost); 104 blank ID
columns in 43 tables; OpenSanctions birth-date 1970-01-01 sentinel.

Also: 505/607 marts declare dbt uniqueness tests but no artifacts prove the
suite has been run since the rebuilds — unverified guards. 16 tables errored
out of the scan (ICIJ etc.), unverified either way. Warehouse schemas still
carry the routing-bug placements (commodity/lobbying under EDUCATION, hospice
under IMMIGRATION) even though repo files moved — [[loader-writes-nan-sentinel]]
and the whole-word-matching trap are related history.

Cheap-scan technique that worked: one aggregate query per table (counts, approx
distinct, length bounds, sentinel counts, year(d)=1970 counts, count(distinct
hash(*))) over 590 tables cost ~$2-4 total. Completeness via 10 web agents cost
zero warehouse credit. Evidence CSVs in outputs/ dated 2026-08-11.
