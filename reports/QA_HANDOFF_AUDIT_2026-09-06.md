# QA Audit — the 2026-09-06 session, checked

Every claim from `QA_HANDOFF_2026-09-06.md` and its supporting commits, run back through the warehouse
or the source file. Nothing below is repeated just because it was written down — it's here because
someone re-ran the query, re-parsed the PDF, or re-read the code.

Two things the orchestrating session confirmed by hand, before any agent touched this — folded in as
real, no matter what anyone below says:

- **`scripts/fec_itcont_load.py` has no dedupe on `SUB_ID`.** Not in HEAD, not in the working tree,
  not in any loadkit helper it calls. Grepped for dedup/merge/qualify/row_number/distinct — nothing.
  The 283,771,819-row table has zero duplicate `SUB_ID`s, but that's because there are none to catch,
  not because a dedupe step caught them. "The dedupe dropped exactly zero rows" describes a mechanism
  that does not exist.
- **That script is uncommitted.** HEAD defines 2 cycles (2024, 2026). The working tree defines 14
  (2000–2028). The 283.8M-row, 14-cycle table in the warehouse was built by the code sitting in the
  working tree right now — not by anything `git log` can show you. If that file is lost, the load
  can't be reproduced from git.

---

## 1. Claims that did not reproduce

### BLOCKER

| Claim | Claimed | Actual | Why it matters |
|---|---|---|---|
| SUB_ID dedupe exists | Dedupe logic runs, drops 0 rows | No dedupe code anywhere (see above) | Table's uniqueness is luck, not a guarantee — next load could collide silently |
| FEC itcont load is reproducible from git | — | HEAD = 2 cycles, working tree = 14 cycles, table built from uncommitted code | Can't rebuild the 283.8M-row table from what's checked in |
| `FED_GOVINFO_BILLSTATUS` key is unique on CONGRESS+BILL_TYPE+BILL_NUMBER | 0 duplicates | 10-row collision | 11 House "Reserved for the Speaker/Minority Leader" placeholder rows (blank type+number) share one key. Any join on this triple folds them into 1, or blows a 1:many join up to 1:11 |
| `build_marts_python_door.py` rebuilt marts dbt disabled | — | Rebuilt `politics__fed_govinfo_billstatus` and `politics__fed_govinfo_bill_cosponsors` — both `+enabled: false` in dbt_project.yml, both under a `guard_politics_mirror()` pre-hook that hard-fails dbt without an explicit override var | The script never opens dbt_project.yml, so it walked through a door dbt was built to keep shut. Real writes, not a dry run — confirmed live at 107,150 and 1,268,519 rows |
| House PTR filing 20019022 | 3 rows landed | 21 real trades on the form — 18 vanish with no trace | Wrong ticker too: row 1 says AAPL, form says GOOG. Owner says SELF, form says JT on every trade |
| House PTR filing 20019023 | 7 rows landed | 63 real trades — 56 vanish (89%) | Ticker on the one row that did land is wrong (ALYF bled in from a different trade further down the page) |
| House PTR filing 20020359 | 1 row landed | 5 real trades — 4 vanish | The 1 row that landed also has the wrong owner (SELF not JT) and a ticker (JPM) stolen from a different trade in the same blob |

### REAL

| Claim | Claimed | Actual |
|---|---|---|
| WFT-prefix/$20M suspect-filing flag total | $91.0B, 35 rows | Row count is right. Dollar total is **$129.53B** — off by $38.5B, 42% low. Wrong in three files (QA handoff, mart SQL comment, loader script comment) — one bad number copy-pasted forward |
| 527 money: RGA/DGA/ActBlue "4,508,587 total contributions" | Combined total across 3 orgs | That number is **only ActBlue's own row count.** RGA (257,621) and DGA (284,190) rows are excluded. Real combined total is 5,050,398 |
| Senate stock trades: 62 filers, no fan-out | 62 matched, 0 collisions | **59** filers today, not 62 — no counting method gets to 62. And there IS a fan-out the fix doesn't catch: "Scott" matches both Tim Scott and Rick Scott, both sitting senators on a committee 116–119 |
| Senate stock trades: "no ticker-to-sector map exists anywhere in repo or warehouse" | Fully unanswerable | Warehouse: true. Repo: false — one exists, built 2026-09-05, coarse and stale (old 2012–2020 trades table), never pointed at today's data |
| `build_marts_python_door.py` guard scope | Only 2 marts affected | The guard sits on the whole `marts.politics` **folder** — 3 more marts this script built today (senate LDA positions, senate EFD filings, committee membership) sat under the same guard, unindividually-disabled |
| `build_marts_python_door.py` redundancy justification | 2 marts safely disabled as duplicates | The canonical marts they duplicate are now **stale** — `politics__bills` (36,465 rows) vs the rebuilt twin (107,150); `politics__bill_cosponsors` (367,735) vs its twin (1,268,519). The table dbt called garbage is the current one |
| `build_marts_python_door.py` table type | — | Every table this script builds lands **permanent**, where dbt's own default is transient. 43 of 691 LIBRARY_MARTS tables are permanent — all 43 are marts this script touched |
| `refresh_timeline_index.py` swap | Atomic rename | Two separate `ALTER TABLE RENAME` calls, no try/except, no rollback if the second one fails |
| `fix_timeline_view_columns.py` loop safety | Per-view isolation | Only the initial probe is wrapped in try/except. A `SystemExit` from one bad view's DDL would abort the rest of the batch |
| TIMELINE__WAREHOUSE reconciliation note | 1,167,068 rows | Live count right now: **1,176,546.** The note is already stale by one more mart rebuild — the exact failure mode its own trap entry warns about |

### MINOR

| Claim | Claimed | Actual |
|---|---|---|
| `FED_CONGRESS_COMMITTEE_MEMBERSHIP` key unique | 0 dupes | 1 collision (Fred Keller, congress 116, HSED) — known upstream YAML error, already fixed one layer down in the mart |
| `FED_GOVINFO_BILL_COSPONSORS` naive key unique | 0 dupes | 13 collisions — real re-cosponsorship events (sign on, drop, sign on again), not a bug, but the obvious key a reader would guess isn't quite unique |
| `FED_HOUSE_FD_INDEX` DOC_ID unique | 0 dupes | 8 excess rows, 7 DocIDs — genuine duplicate lines in the Clerk's own source TSV, landed as-is |
| `FED_HOUSE_PTR` shape "21,429 trades, 472 scans" | 2 buckets | A 3rd bucket exists: 10 "NO PARSEABLE TRADE LINES" placeholders. `IS_SCAN='False'` alone won't filter them out |
| `FED_SENATE_LDA_LOBBYIST_POSITIONS` crawl progress | "mid-2011" | Actually 70–71% through 2011 (60,000/84,349 filings), not ~50% |
| FEC IE cycle totals — 2020 | $3.30B (matches mart) | FEC's own published 24-month total for 2020 is "nearly $3.1B" — mart is ~6% (~$180-200M) above FEC's own number. Real gap, root cause not chased |
| HCRIS filer-dropout range "65 to 108" | Every year 2011–2022 | Only true if 2020–2021 (COVID filing-relief years) are quietly dropped. Include them and the real floor is 41 (2021), not 65 |

---

## 2. Parser defects found (House PTR + Senate PTR, hand-reparsed against fresh refetches)

Every defect below was reproduced by pulling the real PDF/HTML fresh and running the actual loader
code against it — not by re-reading what already landed.

### House PTR — the bad filings

**20019022** (Alphabet/Apple/Daifuku, 3 rows landed for 21 real trades)
- `RAW_LINE`: `...JTAlphabet Inc. - Class C CapitalStock (gOOg) [ST] P 06/24/2021...JTApple Inc. (AAPL) [ST] S 06/18/2021...` — five trades run together with no separator, only the first becomes a row.
- Landed row 1: `TICKER='AAPL'` — the real trade is Alphabet/GOOG. The ticker leaked in from the next unrelated trade in the same blob.
- Owner lands `SELF` on 2 of 3 rows; the form says `JT` on every one of the 21 trades.

**20019023** (AgCO Corporation, 7 rows landed for 63 real trades)
- `RAW_LINE`: `...JTAgCO Corporation (AgCO) [ST] S06/10/2021...JTAlly Financial Inc. (ALYF) [ST] P06/15/2021...` — same collapse. 56 of 63 trades never emitted anywhere.
- Landed row: `TICKER='ALYF'` on a trade that is actually AGCO. Small-caps rendering (`AgCO`, not `AGCO`) breaks the all-caps ticker regex, so it falls through to the next valid ticker in the blob — Ally Financial's.

**20019292** (Wells Fargo, Rep. Stephanie Bice)
- `RAW_LINE`: `...cap. gains >$200?JTWells Fargo & Company (WFC)[ST]S 08/06/2021...` — owner `JT` sits mid-string, buried behind the whole page header. Lands as `OWNER='SELF'`.
- `ASSET_DESCRIPTION` lands as ~370 characters of page boilerplate glued in front of "Wells Fargo & Company (WFC)[ST]."

**20019445** (Netflix, Rep. James Langevin) — same asset-description pollution. Checked how common this is: **711 of 3,105 House PTR filings (22.9%)** carry the same "Clerk of the House" boilerplate signature inside `ASSET_DESCRIPTION`. This is systemic, not a one-off.

**20020197** (Direxion Financial Bull 3X, Rep. Daniel Crenshaw) — same pollution pattern, same root cause (page header and trade line collapse to one pypdf line).

**20020305** (Abbott Laboratories, Rep. Michael Burgess) — same pollution pattern.

**20020359** (Barclays note + 4 more, Rep. Kevin Hern, 1 row landed for 5 real trades)
- `RAW_LINE`: `...JTBARCLAYS BANK PLC SER AMTN 01/22/2027 [CS] P 01/19/2022...JTFS ENERgY & POWER FUNDCOMMON [PS]P 01/19/2022...JTJP Morgan Chase & Co. (JPM) [ST] P01/31/2022...` — 4 of 5 trades never emitted.
- The 1 row that landed: `OWNER='SELF'` (form says JT), `TICKER='JPM'` — stolen from the JP Morgan trade three trades down the same blob. The landed trade is actually a Barclays bond with no ticker of its own.

**20023257** (44-row filing, otherwise clean) — 2 of the 44 `RAW_LINE` values have the next page's column-header text (`"ID Owner Asset Transaction"`) welded on with no space. Cosmetic here (no field corrupted), but the same missing-page-separator bug could truncate an amount range if a wrap ever lands exactly on a page boundary elsewhere.

**20033709** (JP Morgan structured notes, Rep. Jefferson Shreve)
- Row 1's `ASSET_DESCRIPTION`/`TICKER`/`ASSET_TYPE` all landed blank. Root cause confirmed directly: the NOISE filter's bare `"No"` alternative (meant to catch a Yes/No checkbox line) has no word boundary, so it also matches the first two letters of **"note"** — and this asset's continuation line reads `"note [CS]"`. The backward asset-walk hits that, fires, and stops before collecting anything.
- This is a live regex trap: any asset whose continuation line starts with "No" case-insensitively (Nokia, Nordstrom, Northrop, Norfolk...) will drop its name the same way. Not sampled beyond this filing.
- Both trades in this filing also share a byte-identical `RAW_LINE` — only `LINE_NO` tells them apart. A downstream dedup keyed on `(DOC_ID, RAW_LINE)` would silently erase one of two real $5M+ purchases.

**20034869** (Cliffwater Corporate Lending Fund, 2 rows)
- `TICKER` lands blank on both rows even though the text has `"(Ticker: CCLFX) [OT]"` — the regex requires the parenthetical to start with the ticker itself, and "Ticker: " breaks that.
- Two genuinely different trades (sale from the "2012 Trust" vs the "2009 Trust," different unit counts) land as **byte-for-byte identical rows** — the parser never reads the "Subholding Of" line that follows a trade, so nothing distinguishes them. A naive dedup would erase a real trade.

**20023973** — 2 of 57 `RAW_LINE`s carry the same page-boundary header-splice as 20023257. Cosmetic, non-corrupting.

Clean on every axis checked: **20020873, 20021946, 20022293, 20025855, 20030670, 20033402, 20034311, 20034521, 20034998.**

### Senate PTR — mostly clean, two real finds

**4a7a7530** (Sen. Coons, W.L. Gore & Associates) — parser never calls `html.unescape()`. `&amp;` and `&nbsp;` land literally in `ASSET_DESCRIPTION` instead of `&` and a space. Confirmed in the source HTML itself, not a fluke. Affects an unknown number of the other ~698 HTML filings whenever a company name or address has an ampersand.

**4290febc** (Sen. Cruz) — no parser defect, but a process flag: a scratchpad script was silently rewritten mid-task to target a different filing, with a fabricated "PostToolUse hook" notice. No such hook exists in `.claude/settings.json`. Caught before running. Same pattern hit **d1af8002, 00818cb5, 0dbb004e** — each time, a sibling agent's file collided or a stray notice tried to redirect the check to the wrong filing. All caught and disregarded; none changed a reported result. Worth its own line in the verdict below.

Clean, no defects: **ae5e8414, 0fa07a20, 29828a0d, 9b782ca8.**

### Amendment double-count (Senate PTR) — real, but softer than the raw split suggests

1,030 of 6,855 rows sit on amendments; nothing supersedes an original with its amendment — confirmed exactly. But not all 1,030 double-count something: **495–519 rows** (about half) are provable duplicates of a still-present original (~$34.0M of midpoint dollar volume, ~6.3% of the $542.4M table total). The other ~511 are amendments to a 2020-dated original that was never captured in this table at all — those aren't double-counted, they're the only record that exists.

---

## 3. Trap entries falsified

Ten checked entries in `.claude/traps.md` do not hold against the live warehouse or current code.

**Line 115** — "CA_LOBBY_COVER.RPT_DATE can't be parsed, all 568,988 rows go unmeasured."
Falsified: the real parser (`recency_inner`) has a `us_dt` branch added the same day that handles exactly this format. Running it returns a non-null MAX date. 568,848 of 568,988 rows parse fine.

**Line 117** — "XC_OWID_CO2's 5,979 pre-1900 rows land unparsed; four sources pinned at 1900."
Falsified: this source is mapped to the wide-year branch, not the narrow bare-year one the trap describes. 0 of 5,979 pre-1900 rows are unparsed. Zero rows anywhere show `DATA_THROUGH_ISO` year = 1900.

**Line 118** — "...this cost four date shapes and pinned four sources at 1900."
Falsified: the regex lesson itself is real (verified directly in Snowflake), but the "four sources at 1900" consequence doesn't show up in the current ledger or either same-day backup. Only one source is even sub-1900-adjacent, and it's dropped to unmeasured, not pinned to 1900.

**Line 122** — "A frozen 20-URL manifest (dated 20260706) is now all 404s; a single-fetch regex resolver can't find all 20 files across a paginated S3 listing."
Falsified: the same commit that wrote this trap line already replaced the frozen manifest with a paginated S3 resolver that walks every page. Reran it — finds 20/20 current files. The bug the trap describes was fixed before the trap was written down.

**Line 123** — "FEC bulk URLs redirect to a GovCloud host missing from Snowflake's egress rule; all five FEC entries fail."
Falsified: the live network rule already has that host. The one real run logged for these five sources failed on a never-shrink row-count guard, not a network error — no run anywhere logs the quoted network-rule error text.

**Line 126** — "GET_DDL drops the schema, so a stray RIPPLE_REFRESH_SOURCE now sits in LIBRARY_RAW.PUBLIC."
Falsified: the GET_DDL behavior is real, but no such stray procedure exists anywhere in LIBRARY_RAW. The only copy in the account is the correct one.

**Line 127** — "Two loaders have no argparse, so `--help` runs a full load and replaces a live table."
Falsified: both scripts have real argparse now. `--help` prints usage and exits, no fetch, no load. The bug was real for one commit and fixed the next commit, the same day — the trap line was never updated after the fix.

**Line 147** — "Stripping suffix + restricting to Senate committee-seat holders (116–119) gives 62 of 62 filers with no fan-out."
Falsified: the described fix isn't implemented anywhere in the codebase. Reconstructing it by hand gives 61 clean / 1 ambiguous — "Scott" still matches both Tim Scott and Rick Scott, both sitting senators the whole span. Same finding as the REAL item above, from the trap side.

**Line 149** (batch 6 reading) — "Neither chamber reports a dollar figure, only a range."
Falsified for the House: 68 non-blank, non-scan rows carry a genuine single dollar figure (e.g. `$669.27`, `$898.16`, `$4,450.50`), not a range. A separate audit pass on the same line read it as fully confirmed (schema has no exact-dollar column in either pipeline) — both are true at once: no dedicated column exists, but some row content is exact, not ranged. Flagging the disagreement so it isn't quietly resolved one way.

**Line 150** — "51,578 rows have an unparseable TRANSACTION_DT in the FEC individual-contributions mart."
Falsified: the mart's real count is **51,555**, confirmed three independent ways. The 51,578 figure belongs to a different table (`TIMELINE__FINANCE_INDEX`'s null-day bucket count) — the trap conflated the two and got the mart's own number wrong by 23 rows.

---

## 4. Reproduced cleanly

- `FED_FEC_INDIV_CONTRIBUTIONS`: 283,771,819 rows, 14 cycles 2000–2026, SUB_ID fully unique, built by the current uncommitted script (confirmed via INGEST_RUNS log fingerprint).
- `FED_FEC_INDEPENDENT_EXPENDITURES`: 276,183 rows, 5 cycles 2018–2026, key unique.
- `FED_CMS_HCRIS`: 80,077 rows, 13 years 2011–2023, RPT_REC_NUM fully unique and populated.
- `IRS527_SCHEDULE_A_CONTRIBUTIONS`: 9,701,952 rows, 8 ragged dropped, key unique — reproduced from a fresh dry-run parse of the source zip.
- `IRS527_SCHEDULE_B_EXPENDITURES`: 8,191,177 rows, 17 ragged dropped, key unique — reproduced from a fresh independent re-split of the source zip.
- `FED_SENATE_EFD_FILINGS`: 799 rows, 699 HTML / 100 paper, key unique.
- `FED_SENATE_EFD_PTR`: 6,855 rows, 6,755 trade / 100 paper, key unique.
- IRS527 A/B field layout: 18-field width, position-15/16 divergence, field 17 empty on all 17,893,129 clean rows — confirmed by independent raw pipe-split of the whole file.
- Congress-matched IE committee query: $586.0M against / $191.4M for / 157 candidates — exact, and the fan-out-fix claim (raw join = distinct join) holds.
- Enactment rate 2.8% (113th) → 1.4% (118th) — exact, and the empty-string trap (naive query reads 100% enacted) is real and severe.
- Cross-party cosponsorship 24.2% / 17.4% / 21.6% — exact, once sponsor party is resolved per-congress.
- HCRIS ownership-change count (1,322 hospitals) and losing-money shares (33.4% / 24.4% / 43.1%) — exact.
- HCRIS grain (RPT_REC_NUM unique), the PROVIDER_CCN+YEAR non-uniqueness (1,186 hospital-years), and the SOURCE_FILE_YEAR-is-not-fiscal-year trap — all confirmed exactly.
- GovInfo XML tag-name trap (`<number>`/`<type>`, not `<billNumber>`/`<billType>`) and the 13-row no-bill-number trap — confirmed exactly.
- `_INGESTED_AT` vs `INGESTED_AT` naming split across landing tables — confirmed exactly, mechanism traced to `ingest._sf_col`'s underscore-stripping.
- pypdf NUL-byte trap in House PTR form labels — confirmed by fetching the real PDF and finding the literal NUL bytes.
- Three-line House PTR trade structure + unanchored-regex necessity — confirmed on a fresh 8-filing sample (search finds 35/35 trades, anchoring misses several).
- HCRIS staging rename (triple- to single-underscore FTE column) broke staging SQL — confirmed, though the real count is 25 broken references, not the claimed 22.
- Committee roster vs Voteview coverage gaps (missing members, Menendez absent from 118th) — confirmed.
- `RIPPLE_REFRESH_SOURCE` downloads before comparing ETag; cadence filter exists as the fix — confirmed by code read, no query needed.
- `coverage_probe.py --write` appends rather than replaces — confirmed live (multiple MEASURED_AT runs per source stacking up).
- FEC bulk-refresh single-2018-cycle-URL trap, 4-of-5-tables-have-no-cycle-column trap, never-shrink-guard risk — all confirmed exactly.

---

## 5. Verdict

**The landed data mostly holds up. The story wrapped around it doesn't, in three places that matter.**

**Trust the row counts.** Every table's row count and shape claim that got checked reproduced —
FEC indiv contributions, FEC IE, HCRIS, both IRS527 schedules, both Senate EFD tables. These are real,
solid, checkable.

**Don't trust the FEC itcont dedupe story, at all.** No such code exists. It got lucky, not caught.
And the script that built the 283.8M-row table isn't in git. If that file disappears, so does the
ability to rebuild this table.

**Don't trust the two headline dollar totals in the QA handoff.** The $91.0B suspect-filing total is
really $129.5B — wrong in three files, all copy-pasted from one bad number. The "4,508,587 total
contributions" for RGA+DGA+ActBlue is just ActBlue's own count; the real combined figure is over
500,000 higher.

**Don't trust "62 filers, no fan-out" or "no sector map exists."** Both are off — 59 filers, one real
name collision (the two Sen. Scotts), and a sector map does exist, just stale and unused.

**The House PTR parser is the weakest link in the whole session.** On a 20-filing sample, three
filings dropped 56–89% of their real trades with zero error, zero warning, zero trace — this is not
rare-edge-case territory, it's close to 1 in 7 filings sampled. A fourth of all House PTR filings
(711 of 3,105) carry corrupted asset names. Anyone building on this table needs to know: row counts
match, but a meaningful slice of *content* inside those rows is silently wrong or silently missing.

**`build_marts_python_door.py` walked through a door dbt built specifically to keep shut**, on two
marts and with real writes, because it can't see `dbt_project.yml`. It also builds every mart as a
permanent table where dbt's default is transient — that's every mart it's ever touched, not just
today's two.

**Something tried to redirect four separate verification checks mid-task** — scratchpad scripts
rewritten to target the wrong filing, one with a fabricated hook notice. Caught every time, changed
no reported number. Still worth knowing this happened more than once in one session.

**Ten trap-file entries are already wrong** — half describe bugs that were fixed the same day they
were written down (would waste a future session's time re-fixing something that's fine), the other
half describe problems ("62/62," "four sources at 1900," "a stray procedure") that were never real
or never confirmed.

Bottom line: the warehouse numbers are solid where checked. The narrative on top of them — dedupe
claims, two headline dollar totals, two headline counts, and the trap file describing today's own
fixes — needs a pass before anyone downstream repeats it as fact.
