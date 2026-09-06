# 94 Judges' politics and their dockets
- Checked: JUDGE_POLITICAL_AFFILIATIONS (latest d/r row per person, 7,226 persons) -> DOCKETS.ASSIGNED_TO_ID -> DOCKETS.IDB_DATA_ID = FJC_IDB_CL_LINKED.ID (10.3M IDB rows already keyed to dockets) -> JUDGMENT / NATURE_OF_SUIT. FJC_SERVICE route not needed: IDB FILEJUDG is blank on the big districts, CourtListener's linked copy carries the judge.
- First number: **6.87M civil cases, 1,824 judges; judgment for plaintiff 36.5% under Democratic-affiliated judges vs 36.7% under Republican** (of 1.44M cases with a plaintiff/defendant judgment). Flat across civil rights (11.1 vs 10.4), prisoner (1.9 vs 1.9), labor (80.5 vs 80.3), patent (52.8 vs 54.4). One gap: product liability NOS 365, 20.9% vs 12.8% (6,601 vs 7,567 decided; MDL-heavy, one or two judges can move it).
- FEC leg: judge name+state = FEC NAME/STATE matched 4,533 rows for 87 judges, 0 dated before the judge's first bench date; eye sample is an auto dealer, a physician, a retiree - 0 of 3 real. The FEC landing is dominated by 2023-2025 rows and carries a year-3312 date. Dead as loaded.
- Hit means: disposition mix moves with the judge's party for a suit type. Miss means: party does not predict who wins in the IDB judgment field.
- Traps: JUDGMENT is filled on 21% of cases (1.44M of 6.87M); the rest are dismissals/settlements with no side. POLITICAL_PARTY is a one-letter code (d, r, i, j, f, w...) and 1,260 persons carry more than one row. Pro se plaintiffs win 2% vs 13% represented, so any party gap must hold pro se constant.
- Cost: 12 queries, longest 10s, ~33s total.

STATUS: dim
HEADLINE: Plaintiffs win 36.5% before Democratic-appointee-affiliated judges vs 36.7% before Republican across 1.44M decided civil cases; the donation leg is dead (0 pre-bench FEC rows, name matches are strangers).
