# US Politics — Tier 1 + Tier 2 Build Queue
_2026-06-30 · scouted + adversarially verified_

## The shape of it

These 17 sources take the politics spine from a **numbers-only Congress core** (money, votes, bills) and give it a voice, a full history, a third branch, and a whole tier below the federal line. Tier 1 is pure steel — 8 sources that bolt straight onto BIOGUIDE / FEC_CAND_ID with zero name-matching (committee gavels, bill text + CRS summaries, press releases, tweets, the full 1789-present Voteview backfill, PAC-to-candidate money). **The single biggest win is the Voteview HSall full-history backfill** — one loader turns your 2-congress voting/ideology slice into the complete 1789→present record on the key that already threads the whole spine. Tier 2 is where you earn it: judges, lobbying, dark money, state legislators, and stock trades are all real accountability gold but they hit **THE WALL** — no shared federal person ID, so every one of them pays the same recurring tax: **name-resolution infra + a license read** (three of them are commercial landmines if you touch the wrong file).

## Tier 1 — steel bolt-ons (do these first)

Ranked by value × ease. All bolt onto BIOGUIDE or the FEC/bill grain with a real steel key.

| # | Source | source_id | Access · Auth | Key → bolts onto | License | Effort | Verdict |
|---|--------|-----------|---------------|------------------|---------|--------|---------|
| 1 | Committee membership | `fed_unitedstates_committees` | Bulk YAML · none | BIOGUIDE → MEMBER_CROSSWALK | CC0 | 1–1.5d | **GO** |
| 2 | PAC→candidate money (refresh) | `fed_fec_committee_to_candidate` | Bulk ZIP · none | FEC_CAND_ID/CMTE_ID → money spine | Public domain | 0.5–1d | **GO (refresh, not new)** |
| 3 | Congress press releases | `fed_congress_press` | Bulk JSONL · none | BIOGUIDE (99.7%) → MEMBER_CROSSWALK | MIT | 2–3d | **GO** |
| 4 | Voteview HSall full history | `fed_voteview_hsall` | Bulk CSV · none | ICPSR↔BIOGUIDE → whole spine | No data license, attrib | 1.5–2.5d | **GO** |
| 5 | CRS bill summaries | `fed_govinfo_billsum` | Bulk ZIP-of-XML · none | (congress,type,number) → BILLS | Public domain | 1.5–2d | **GO (bill enrichment)** |
| 6 | Congress tweets | `fed_congresstweets` | Bulk JSON · none | BIOGUIDE (2-hop via crosswalk) | MIT | 2–3d | **GO (frozen archive)** |
| 7 | Bill full text + PLAW | `fed_congress_govinfo_bills` (+`fed_govinfo_plaw`) | Bulk ZIP-of-XML · none | (congress,type,number) + law_number → BILLS | Public domain | 3–5d | **GO** |
| 8 | DIME CFscores | `xc_dime_cfscores` | Bulk CSV.gz · none | FEC_CAND_ID (small) / else PROBABILISTIC | ODC-BY (attrib) | 2–3d | **GO (scope to recipients)** |

**Standouts:**

- **Voteview HSall is the crown jewel** — highest value/effort ratio in the whole batch. One loader, ICPSR is the true PK at 100%, bioguide is ~100% across ALL eras (the "thin in 19th c." fear is empirically false). Only real engineering wrinkle: the 700MB votes file — stream it, don't `r.content` into a str.
- **Committee membership is the fastest genuine win** — ~1 day, CC0, pure STEEL bioguide, and it fills the one dimension the spine is missing: *who holds which gavel*. Makes committee power queryable against money and votes with zero name-matching.
- **`fed_fec_pac2cand` is a trap** — it's already landed as `fed_fec_committee_to_candidate`. Do NOT create the duplicate id. But the mart it claims to feed (`POLITICS__MEMBER_PAC_MONEY`) has NO build code in the repo — treat it as unbuilt.

## Tier 2 — high value, real work

Same shape. Every one hits THE WALL — the name-resolution builds are flagged.

| # | Source | source_id | Access · Auth | Key → bolts onto | License | Effort | Verdict |
|---|--------|-----------|---------------|------------------|---------|--------|---------|
| 1 | FJC federal judges | `fed_fjc_judges` | Bulk CSV · none | nid (new spine); SCOTUS→SCDB name-match | Public domain | 1–1.5d | **SHIP** |
| 2 | Shor-McCarty state ideology | `st_shor_mccarty` | Bulk TSV · none | **name-match** → MEMBER_CROSSWALK (jumpers) | CC0 (pinned DOI!) | 1–1.5d | **CONDITIONAL GO** |
| 3 | Judicial Common Space | `xc_judicial_common_space` | Bulk ZIP · none | **name-match** → SCDB (49) / FJC | CC0 | 1d | **SHIP** |
| 4 | CourtListener judge disclosures | `fed_courtlistener` | Bulk S3 · none | fjc_id → FJC; **PROBABILISTIC** to spine | PDM (bulk only) | 3–4d | **BUILD (S3 only)** |
| 5 | IRS 990 / EO BMF nonprofits | `fed_irs_990_nonprofit` | Bulk CSV/XML · none | **EIN** (STEEL to EIN axis, not FEC) | Public domain (IRS) | 4–6d | **GREEN (IRS layer)** |
| 6 | IRS 527 political orgs | `fed_irs_527` | Bulk ZIP · none | **EIN** (STEEL to EIN axis, not FEC) | Public domain | 3–5d | **SHIP** |
| 7 | House STOCK Act PTRs | `fed_house_ptr` | Bulk ZIP+PDF · none | **name+district→bioguide** crosswalk | Journalism-only | 6–7d | **GO (journalism scope)** |
| 8 | Federal lobbying (LDA) | `fed_lda_lobbying` | Paginated REST · optional key | **name-match** honoree→member, org→EIN | Public record | 4–6d | **GO** |
| 9 | Open States (state legislators) | `st_openstates` | Bulk S3/pgdump · none | ocd-person + GEO; bioguide (us-subset only) | CC0 / public-domain | 4–6d | **BUILD (Phase 1 first)** |

**Name-resolution builds** (these need crosswalk infra before the join fires):
- `fed_house_ptr` — name+StateDst → bioguide. The whole value (trades × votes) hinges on this fuzzy match. Build an unmatched-filer quarantine.
- `fed_lda_lobbying` — honoree_name → member, org name → EIN. Zero structured FEC/bioguide ID in the payload; every bridge is name-match + confidence.
- `st_shor_mccarty` — name+state+chamber → bioguide, but only the ~1-2% career-jumpers ever match.
- `st_openstates` — ocd-person is the state PK; wikidata is NOT populated on state people (refuted). GEO + name only below the federal line.
- `fed_fjc_judges` / `xc_judicial_common_space` / `fed_courtlistener` — SCOTUS→SCDB name-match (49 closed set = near-steel); CoA name+circuit is irreducibly fuzzy (66 surname collisions).

## Per-source dossiers

### TIER 1

---

#### `fed_unitedstates_committees` — Congress committees + membership

**What it is:** The @unitedstates project's committee files — who sits on which committee/subcommittee, who holds the gavel. Plain YAML from the same repo that already feeds MEMBER_CROSSWALK.

**Endpoint:** `raw.githubusercontent.com/unitedstates/congress-legislators/main/{committees-current,committees-historical,committee-membership-current}.yaml`. **Landmine:** `theunitedstates.io` mirror is DEAD (parked/for-sale) — use raw.githubusercontent or `unitedstates.github.io` only.

**Schema/keys:** committee_id/thomas_id (e.g. SSAF, HSAG), bioguide (every membership row, 99.7%+), house_committee_id, senate_committee_id, party (majority|minority), rank, title (Chair/Ranking), subcommittees[] (nested).

**Bolts on:** bioguide → MEMBER_CROSSWALK (native PK both sides, STEEL). ~500 current members match a subset of the 12,794 historical crosswalk — many→one LEFT JOIN, NOT 1:1 against all 12,794.

**License:** CC0 — commercial-safe, zero landmine.

**Gotchas:** membership YAML is an OBJECT keyed by committee_id (subcommittee keys = parent+sub thomas_id concatenated — split to derive parent + is_subcommittee). Member entries don't carry the committee id inline — flattener must inject from the key. Membership churns intra-Congress → snapshot-replace on a schedule.

**Build plan:** `politics/loaders/build_committees.py` (clone build_skeleton.py fetch/land). Two landing tables: `FED_UNITEDSTATES_COMMITTEES` (one row/committee) + `FED_UNITEDSTATES_COMMITTEE_MEMBERSHIP` (one row/committee×bioguide). Staging views → marts `POLITICS__COMMITTEE` + `POLITICS__COMMITTEE_MEMBERSHIP` (LEFT JOIN crosswalk on bioguide). Tests: unique+not_null on (committee_id, bioguide); relationships to COMMITTEE + MEMBER_CROSSWALK. **Smoke:** COUNT(DISTINCT committee_id), every membership row has a bioguide, ~500 current members resolve. **~1–1.5 days.**

---

#### `fed_fec_committee_to_candidate` — PAC/committee → candidate money (REFRESH)

**What it is:** FEC bulk pas2 (itpas2) — every contribution from a committee to a candidate + independent-expenditure lines. The PAC/party leg of the money box score. **Already in Ripple — this is a refresh + finish-the-mart, NOT a new onboard.**

**Endpoint:** `fec.gov/files/bulk-downloads/{CYCLE}/pas2{YY}.zip` (302→GovCloud S3 — follow redirects). Current: `/2026/pas226.zip` (163,133 rows, 6.3MB, Last-Modified 2026-06-28, grows weekly). Header from `data_dictionaries/pas2_header_file.csv` (file has NO header row).

**Schema/keys:** CMTE_ID (100%), CAND_ID (99.87%), TRANSACTION_TP (24K direct / 24E ad-FOR / 24A ad-AGAINST), TRANSACTION_AMT, MEMO_CD (X=double-count, exclude), SUB_ID (unique PK).

**Bolts on:** CAND_ID → MEMBER_FEC_ID → MEMBER_SPINE (bioguide); CMTE_ID → FEC_CAND_CMTE_LINK. True STEEL, measured live.

**License:** Public domain. The individual-contributor resale restriction does NOT bite pas2 (payers are committees, not individuals). Ship it commercially.

**Gotchas:** **DO NOT create `fed_fec_pac2cand`** — duplicate. Loader `scripts/fec_pas2_load.py` hardcodes Windows paths (`c:\Code\Ripple_v6`, lines 21,22,23,27) — repoint to the mac root. `POLITICS__MEMBER_PAC_MONEY` mart is UNBUILT (no code in repo despite registry claim) — build it. **FACTUAL FIX:** the 211 blank-CAND_ID rows are all 24K (direct contributions), NOT 24A/24E. Keep FOR (24E/24F) and AGAINST (24A/24N) SEPARATE — never net. For outside for/against, `FED_FEC_INDEPENDENT_EXPENDITURES` is source-of-truth; pas2 24A/24E is a coverage cross-check only (subset of oth).

**Build plan:** Fix loader paths, re-run for 2026 cycle. Build staging `stg_fed_fec_committee_to_candidate__transactions` (dedup on SUB_ID) + mart `politics__member_pac_money` (bioguide×cycle, fanout-guard from build_indiv_donations.py). **Smoke:** landing ≈ file, CMTE_ID 100%/CAND_ID ≥99%, 24K dominates, 0 dup (bioguide,cycle), reconcile 3-4 members to OpenFEC totals. Update registry VOLUME + URL. **~0.5–1 day.**

---

#### `fed_congress_press` — Congressional press releases

**What it is:** Derek Willis's scraped corpus of ~688k congressional press releases 2001-present, keyed to bioguide. The text/rhetoric layer — "what a member SAID" next to how they voted / who paid them.

**Endpoint:** `thescoop.org/congress-press/downloads/{2001..2025}.zip` (yearly) + `2026-MM.jsonl` (monthly). **The `/downloads/` base 404s** (static GitHub Pages, no directory index) — ENUMERATE filenames. YYYY.zip expands to nested `YYYY/YYYY-MM.jsonl`.

**Schema/keys:** url (dedup PK, md5), title, date, member.bioguide_id (99.7%), member.name/party/state/chamber, text, collected_at.

**Bolts on:** bioguide → MEMBER_CROSSWALK, first-party ^[A-Z]\d{6}$ format, 1:1. State is 2-letter postal (incl. territories DC/AS) — NOT FIPS/district, geo needs crosswalk enrichment.

**License:** MIT (commercial-safe, verified via API + raw LICENSE). Text is federal-office authored (public-domain-ish). Retain Willis attribution.

**Gotchas:** single-maintainer bus-factor=1 — mirror full history on first ingest. Pre-2013 is effectively empty (2001.zip=63KB/53 recs vs 2015.zip=61MB) — analytically-usable window is ~2013+; don't compute cross-year activity trends off pre-2013. ~3% null/partial dates; text can be null historically; dedup by URL only.

**Build plan:** `build_congress_press.py` (model on build_indiv_donations.py). Enumerate yearly ZIPs + current monthly, walk nested subdir, flatten member.* → flat TEXT. Landing `FED_CONGRESS_PRESS`. Staging (dedup by url) → mart `politics__press_releases` (join crosswalk on bioguide). **Smoke:** ~688k rows, bioguide ≥97%, ≥95% distinct bioguides in MEMBER_CROSSWALK, date span 2001→now, no dup url. **~2–3 days.**

---

#### `fed_voteview_hsall` — Full-history roll-call votes + ideology (1789-present)

**What it is:** Voteview's complete congressional record — every roll-call vote and DW-NOMINATE ideology score back to the 1st Congress. Extends your current 2-congress slice to all of history under one loader.

**Endpoint:** 4 static CSVs at `voteview.com/static/data/out/`: members (6.2MB), rollcalls (29.5MB), **votes (700MB — THE BEAST)**, parties (60KB). All Last-Modified 2026-06-30. **The claimed `current.zip` DB dump is 404/DEAD — remove it; the 4 CSVs are the only live path.**

**Schema/keys:** icpsr (true career PK, 100%), bioguide_id (~100% all eras for House/Senate; ~50% blank on President rows), congress, chamber, rollnumber, cast_code (1=Yea,6=Nay,9=NV), nominate_dim1/dim2, nokken_poole_dim1/dim2 (inside members file, NOT separate), bill_number (rollcalls, soft link to BILLS).

**Bolts on:** ICPSR↔BIOGUIDE → MEMBER_CROSSWALK → the whole spine (money, votes, bills). Votes/rollcalls join existing VOTEVIEW_VOTES/ROLLCALLS on (congress,chamber,rollnumber)+icpsr.

**License:** MIT covers CODE ONLY. **The DATA has NO explicit license** — attribution-requested (cite Lewis et al. 2026), underlying facts US public record. Commercial-safe by inference, not written grant. Stop calling the data MIT.

**Gotchas:** stream the 700MB votes file (`stream=True` + `chunksize`), do NOT `r.content` into a str (the existing loader's OOM trap). **JOIN-KEY CORRECTION:** bioguide is ~100% across ALL eras (measured), NOT thin in the 19th c. The real deep-history degradation is at the FEC-derived MEMBER_CROSSWALK into the MONEY marts (pre-FEC members won't resolve), plus President rows. icpsr-keyed marts keep full 1789-present coverage. `keep_default_na=False` (blanks land as '' not 'nan'). Loader hardcodes Windows paths.

**Build plan:** `build_voteview_hsall.py` (fork build_votes_leg.py). 4 landing tables. Staging views → extend existing marts to full history: `politics__voteview_votes`, `voteview_rollcalls`, NEW `member_ideology` (bioguide×congress×nominate scores), extend `member_voting_record`. Reconcile the 4 pre-existing partial registry rows (supersede, don't orphan). **Smoke:** members span congress 1..119, >0 rows for congress≤50, votes_eligible=cast+missed, reconcile 118th missed-vote % vs GovTrack within 1pp, bioguide resolution ≥95% for modern congresses. **~1.5–2.5 days.**

---

#### `fed_govinfo_billsum` — CRS bill summaries

**What it is:** GPO/CRS plain-English summaries of every bill, XML bulk. Adds searchable summary TEXT to the 36k-bill spine — enriches the bill node, does NOT add a member on-ramp.

**Endpoint:** `govinfo.gov/bulkdata/BILLSUM/{113..119}/{billtype}/BILLSUM-{congress}-{type}.zip`. JSON index needs `Accept: application/json`. Pre-built ZIPs exist for ALL congresses (verified 113/s = 5.18MB). Folder last-modified 2026-06-30 (updated daily).

**Schema/keys:** measure_id, congress, bill_type (lowercase → UPPER in staging), bill_number, summary_id (versioned vNN), action_desc, summary_text (CDATA HTML — store raw + stripped). **NO member/bioguide/sponsor ID in the payload** (verified by full tag enumeration).

**Bolts on:** (congress,bill_type,bill_number) → BILLS (STEEL bill grain). Reaches members only transitively via BILLS.sponsor_bioguide.

**License:** Public domain (dc:rights §105, statutory CRS authorship 2 U.S.C. 166(d)). Clean, commercial-safe.

**Gotchas:** ONE bill = MANY summary versions — grain must include summary_id or you drop later-stage summaries (build a latest_summary flag). 119th is partial — carry congress_partial=TRUE. Newest bills lag (CRS writes summaries after introduction) — legitimate coverage gap vs BILLS, not a load error.

**Build plan:** `build_billsum_leg.py` (mirror BILLSTATUS loader). Landing `FED_GOVINFO_BILLSUM`. Staging (dedup to congress,type,number,summary_id) → mart `politics__bill_summaries` (join BILLS, latest_summary flag + version history). **Smoke:** rows > file count (multi-version), 100% of current-congress summaries exist in BILLS or explain gap, spot-check id118s2048, no dup key. **~1.5–2 days.**

---

#### `fed_congresstweets` — Tweets of Congress (FROZEN archive)

**What it is:** Alex Litel's daily tweet archive of Congress-affiliated accounts, 2017-06-21 → 2023-07-11. What members SAID, next to money/votes. **Dead feed — grab-now historical corpus.**

**Endpoint:** daily `raw.githubusercontent.com/alexlitel/congresstweets/master/data/{YYYY-MM-DD}.json` (~2210 files). Crosswalk: `congresstweets-accounts/master/historical-users-filtered.json` (815 members incl. former, 100% bioguide). **Everything after 2023-07-11 is 404.** The 2026-02-21 commit is a cosmetic restore, NOT new data.

**Schema/keys:** tweet: id, user_id, screen_name, time, text, source (NO bioguide). Crosswalk: id.bioguide, id.govtrack, accounts[].id, account_type.

**Bolts on:** BIOGUIDE (STEEL) but INDIRECT/two-hop — tweet.user_id → crosswalk.accounts[].id → member.bioguide → MEMBER_CROSSWALK. **CORRECTION:** THOMAS_ID is committee-level only, NOT a member key — registry JOIN_KEYS = BIOGUIDE;GOVTRACK.

**License:** MIT (both repos). Ship derived activity/timing metrics; don't build a wholesale raw-tweet-republishing product (X ToS sits under Litel's MIT).

**Gotchas:** use `historical-users-filtered.json` (815, incl. former members) NOT `users-filtered.json` (541). Join on numeric user_id first, screen_name fallback (handles recycle over 6 years). Crosswalk mixes persons + committees/caucuses — filter type='member'. Git history is self-declared volatile — mirror both repos now. Volume (4-6M) is an estimate — count at load.

**Build plan:** `build_congresstweets.py`. Two landing tables (tweets + accounts). Staging → intermediate `int_congresstweets_tweet_member` (stamp bioguide) → marts `politics__member_tweets` + `politics__member_tweet_activity`. **Smoke:** 4-6M tweets, ≥95% member-typed tweets resolve to bioguide (hard gate), every bioguide in MEMBER_CROSSWALK, max(time) ≤ 2023-07-12. **~2–3 days.**

---

#### `fed_congress_govinfo_bills` + `fed_govinfo_plaw` — Bill full text + enacted-law text

**What it is:** GPO's actual legislative TEXT (BILLS) + enacted public-law text (PLAW USLM). The text companion to already-landed BILLSTATUS metadata.

**Endpoint:** BILLS: `govinfo.gov/bulkdata/BILLS/{congress}/{session}/{billtype}/BILLS-{congress}-{session}-{billtype}.zip` (~45MB each, 113→present only — pre-2013 is page-image PDF). PLAW: `govinfo.gov/bulkdata/PLAW/{congress}/public/PLAW-{congress}-public.zip` (2.9MB).

**Schema/keys:** congress, bill_type, bill_number, bill_version (ih/rh/es/enr...), sponsor via `name-id` attribute (e.g. R000614 — **NOT an attribute called "bioguideId"**; parser must read sponsor/@name-id). PLAW: law_number (119-32), stat_citation (139 Stat. 480), originating-bill ref — all verified populated.

**Bolts on:** (congress,type,number) → BILLS; law_number → BILLS.law_number; sponsor name-id → MEMBER_SPINE.

**License:** Public domain (§105 verbatim in real files). Commercial-clear.

**Gotchas:** **SOURCE_ID collision** — `fed_congress_govinfo_bills` stub already exists (political_sources.py:188, :794). Reuse it for BILLS text; add `fed_govinfo_plaw` sibling for enacted law. One bill = MANY versions (grain includes bill_version). BILLS uses bill-DTD XML (root `<bill>`), PLAW uses USLM (root `<pLaw>`) — two parsers. **Storage: full text is a few GB across 113-119 — decide full-text-VARIANT vs summary+char_count+URL pointer up front** (the real time sink).

**Build plan:** `build_bills_text.py` (fork build_bills_leg.py). Two landing tables. Staging (dedup on 4-part key) → marts `politics__bill_text` (per version) + `politics__public_law` (per law, wire law_number → BILLS). **Smoke:** every BILLS row with non-null law_number matches a public_law row (~100%), sponsor_bioguide joins MEMBER_SPINE at high rate for 118/119, bill_text rows ≥ BILLS rows, zero dupes on 4-part key. **~3–5 days.**

---

#### `xc_dime_cfscores` — DIME ideology (money-in-politics)

**What it is:** Bonica's common-space CFscore — ideology for every federal + state + local candidate AND donor, 1979-2024. Genuinely new to Ripple. **Scope to the Recipients file first.**

**Endpoint:** Dropbox `scl/fi` link (rlkey token) off the Stanford v4.0 page — `dime_recipients_1979_2024.csv.gz` (30.5MB, 479,502 rows × 64 cols, verified live). Single-maintainer personal Dropbox — grab-now, snapshot immediately.

**Schema/keys:** bonica.rid (PK), recipient.cfscore (100%), contributor.cfscore, Cand.ID (real FEC ^[HSP]# on only 9.5%), FEC.ID (real ^C\d{8} on 15.8%), ICPSR (~0% real — synthetic), party (ICPSR NUMERIC codes, not D/R/I).

**Bolts on:** clean FEC cand_id → MEMBER_FEC_ID → bioguide, but **only ~2,000-3,000 actual members** (only 2,233 distinct cand ids won a general). The other ~85% is state/local/PAC synthetic IDs = THE WALL.

**License:** ODC-BY 1.0 — commercial-permitted, attribution required (Bonica 2024). **One-line email to bonica@stanford.edu recommended** before publishing commercial derivatives (the page carries a contradictory "strictly academic use" sentence). NOT a hard landmine, flag the ambiguity.

**Gotchas:** **ICPSR is ~0% directly joinable** (97% alpha-synthetic like C006623872018) — never join DIME.ICPSR→Voteview. **Smoke gate rewrite:** ">20k federal members" is wrong — that's candidate ROWS; reframe to ">20k rows carry a real ^[HSP]# cand id" and set member-join gate to ~2,000. **dbt accepted_values party (D/R/I) FAILS 100%** — party is ICPSR codes (100=Dem, 200=Rep, 328=Ind); map in staging first. Row count = 479,502 after CSV parse (479,626 raw lines due to embedded newlines).

**Build plan:** `build_dime_cfscores.py` (stream gz). Landing `XC_DIME_CFSCORES` (64 cols TEXT). Staging: derive is_federal, clean_fec_cand_id/cmte_id via regex, map party codes → mart `politics__dime_cfscores` (bonica_rid PK) + `politics__member_ideology` (federal members get CFscore). **Smoke:** rows=479,502, cfscore 100% non-null numeric, clean cand_id 40-50k, member join >2,000, SHA idempotent. **~2–3 days** (+1-2 if landing the multi-GB contributors file).

### TIER 2

---

#### `fed_fjc_judges` — Federal judges biographical directory

**What it is:** FJC's complete Article III judge directory 1789-present. Opens a NEW third-branch (judiciary) spine — judges aren't members of Congress.

**Endpoint:** 6 relational CSVs at `fjc.gov/sites/default/files/history/`: demographics.csv (4,067 judges), federal-judicial-service.csv (4,766 appointments), education, professional-career, other-federal-judicial-service, other-nominations-recess. All HTTP 200, no auth, source "updated nightly."

**Schema/keys:** nid (FJC PK, clean 1:many), Appointing President + Party, Nomination/Confirmation Date, Ayes/Nays (Senate confirmation vote), Court Type (incl. "Supreme Court", 121 rows). **Zero steel keys** — grep-confirmed no bioguide/icpsr/fec/EIN.

**Bolts on (all soft):** SCOTUS (121) → SCDB by name-match (highest value); Appointing President → Voteview presidents; Birth State → FIPS/GEO. It's a NEW judiciary spine keyed on nid, NOT a spine extension.

**License:** Public domain (US gov work). Clean, commercial-safe, only a non-binding citation request.

**Gotchas:** several CSV column HEADERS contain embedded newlines inside quoted fields — use a real CSV parser (pandas C engine handles it). Dates mm/dd/yyyy. SCOTUS→SCDB 121/121 match is UNPROVEN — validate in smoke test, don't assume.

**Build plan:** `build_fjc_judges.py` (6-file bulk CSV). 6 landing tables. Staging (typed dates) → marts `politics__JUDGES` (nid PK), `politics__JUDGE_APPOINTMENTS` (unique-value: presidential appointment + Senate confirmation-vote history), `politics__JUDGE_SCOTUS_CROSSWALK` (121 name-matched to SCDB, with confidence). **Smoke:** COUNT=4067=DISTINCT nid, 121 SCOTUS rows all name-match SCDB, dates parse, no dup (nid,seq). **~1–1.5 days.**

---

#### `st_shor_mccarty` — State legislator ideology (NPAT common space)

**What it is:** 27,629 state legislators scored on the SAME NPAT ruler as federal DW-NOMINATE, 1993-2020. The ideology backbone of the state-legislature expansion.

**Endpoint:** `dataverse.harvard.edu/api/access/datafile/7067107` (the .tab, 27,629×118, 5.79MB). **Do NOT append `?format=original`** (returns unparseable Stata binary). Ungated HTTP 200.

**Schema/keys:** u_id (PK, e.g. AK1995L036), np_score (lifetime fixed score ~[-3,3]), st (2-letter, 50 states no DC/PR), senate/house year flags 1993-2020, sdistrict/hdistrict. **st_id is a temp id — do NOT join. NO bioguide/icpsr/fec anywhere.**

**Bolts on:** PROBABILISTIC name-match. Real partner is Open States (ocd-person) — must land that first. Federal bridge = ~1-2% career-jumpers via name → MEMBER_CROSSWALK.

**License:** **CC0 — but DOI-SPECIFIC.** The pinned April-2023 DOI (NWSYOS / datafile 7067107) is CC0. **The newer Jan-2025 release (SGOQ7G) is CC BY-NC-SA 4.0 = NONCOMMERCIAL LANDMINE.** Trade-off: CC0 forces the stale-at-2020 file; fresh 2022 data is only NC. **Registry MUST pin the exact CC0 DOI and hard-flag the NC successor — never auto-follow "latest."**

**Gotchas:** np_score is a SINGLE lifetime value, not per-year (new row only on party switch). File is WIDE (88 year/district columns) — UNPIVOT to legislator-chamber-year long. ~161 blank u_id rows. Frozen at 2020 — SHA won't change (expected).

**Build plan:** `build_shor_mccarty.py` (copy Dataverse idiom from build_who_won.py, pin datafile id, no `?format=original`). Land WIDE. Staging: melt to long grain → marts `politics__state_legislator_ideology` (long) + `politics__state_legislator_scores`. Add name-match column set to MEMBER_CROSSWALK with match_method. **Smoke:** rows=27,629, u_id ≥99% unique, np_score parses [-3,3], 50 states, no dup (u_id,chamber,year), career-jumper match rate REPORTED not asserted. **~1–1.5 days** + 0.1d to pin DOI + license-guard NOTE.

---

#### `xc_judicial_common_space` — JCS judge ideology

**What it is:** DW-NOMINATE-scale ideology for SCOTUS justices (49) + Courts of Appeals judges (705), 1937-2024. Fills a judicial-ideology gap, joinable to landed SCDB.

**Endpoint:** `epstein.wustl.edu/s/JCS2024.zip` (103,888 bytes, verified, SHA256 1e98021e...). CC0 mirror at Harvard Dataverse hdl:1902.1/10333 (frozen 2007 vintage). Single-maintainer Squarespace — archive on land.

**Schema/keys:** 4 CSVs — coa_judges (name, circuit, jcs; 705 rows), scotus_long (term, justiceName, jcs; 782 rows, 49 justices), medians (102 rows), scotus_wide (redundant pivot). justiceName is SCDB/Spaeth style (ACBarrett, WHRehnquist). **NO icpsr/appointing-president columns — the lead's "bridge" is methodology, DISPROVEN by grep.**

**Bolts on:** SCOTUS justiceName → SCDB (49-justice closed-set crosswalk = near-steel). CoA name+circuit → FJC (fuzzy; 66 surname collisions — disambiguate on circuit + first name). medians → Voteview by congress/year. PROBABILISTIC.

**License:** CC0 (verified on Dataverse mirror; the 2024 WUSTL zip posts no explicit license, relies on implicit CC0/thin-copyright). Commercial-safe.

**Gotchas:** judge-name field has embedded commas — proper CSV parser mandatory. Filter `__MACOSX/` + `.DS_Store`. Drop leading unnamed index column. medians "president" is a numeric ideology SCORE, not a name. Coverage floor 1953 for headline scores.

**Build plan:** `build_judicial_common_space.py` (one-shot ~104KB). Landing `XC_JUDICIAL_COMMON_SPACE` (tagged partitions or 3 sibling tables). Staging views → marts `politics__judge_ideology_coa`, `politics__judge_ideology_scotus`, int crosswalk `int_jcs_scotus_to_scdb` (49 rows). **Smoke:** coa=705, scotus=782, medians=102, jcs∈[-1,1], anchors (WHRehnquist 2004=+0.524, RBGinsburg 2004=-0.438, TMarshall 1990=-0.749). **~1 day.**

---

#### `fed_courtlistener` — Judicial financial disclosures

**What it is:** Free Law Project's parsed judicial financial-disclosure records — 1.9M investments across 4k+ federal judges. Adjacent accountability layer, off the Congress spine.

**Endpoint:** anonymous bulk S3 `s3://com-courtlistener-storage/bulk-data/` (`.csv.bz2`, quarterly snapshots). Verified: financial-disclosures (5.6MB), financial-disclosure-investments (36.6MB, LastModified 2026-06-30T20:09Z), people-db-people (hyphenated filename confirmed). **NEVER the REST API** (rate-limited, no bulk semantics).

**Schema/keys:** person.id, fjc_id (unique indexed FJC crosswalk), ftm_eid (STALE/unmaintained per CL's own docs), financial_disclosure_id (FK chain), gross_value_code (coded bands, NOT dollars), redacted flag.

**Bolts on:** fjc_id → FJC judge universe (STEEL). Internal FK chain (person→disclosure→investment) is STEEL within CL. To the Congress spine: PROBABILISTIC name-match for rare career-jumpers only. No bioguide/FEC/ICPSR.

**License:** **Public Domain Mark (PDM)** on bulk files — commercial-safe (NOT CC0 as the dossier said; say PDM). The API "noncommercial landmine" framing is overstated — it has a free tier + commercial agreements; avoid it for rate-limit reasons, not license.

**Gotchas:** snapshots not deltas + snapshot-replace = correct. Stream the 37MB investments bz2. Values are coded bands — map codes to ranges, don't treat as numeric dollars. Many line-items redacted. MAX-date per entity at runtime, don't hardcode dates.

**Build plan:** `build_courtlistener.py` (anonymous S3, bz2 stream, dtype=str). One landing table per entity. Staging views → marts `politics__judge`, `politics__judge_disclosure`, `politics__judge_investment`. **Smoke:** investments ~1.9M, disclosures ~32k, disclosure person_id joins PEOPLE.id zero orphans, >3,000 people with fjc_id, no orphan line-items. **~3–4 days.**

---

#### `fed_irs_990_nonprofit` — IRS Form 990 + EO BMF

**What it is:** IRS nonprofit filings — the Exempt Org Business Master File (1.97M orgs) + 990 e-file XML. Fills a real gap: 501c4/c6 is the dark-money spine, and Ripple has no nonprofit source.

**Endpoint:** EO BMF `irs.gov/pub/irs-soi/eo_{state}.csv` (1,966,267 orgs, last-modified 2026-06-08). 990 XML `apps.irs.gov/pub/epostcard/990/xml/{YEAR}/{YEAR}_TEOS_XML_{MM}{A-D}.zip` (2019-2026, ~100MB each) + `index_{YEAR}.csv` manifest. **AWS `s3://irs-form-990` bucket is DEAD (frozen 2021-12-31, 404).** ProPublica API is REFERENCE-ONLY.

**Schema/keys:** EIN, NAME, SUBSECTION (04=501c4, 06=501c6), NTEE_CD, STATE, REVENUE_AMT, OBJECT_ID (990 XML), RETURN_TYPE.

**Bolts on:** EIN → Ripple's EIN axis (STEEL). **NO steel path to FEC/politician spine** — dark-money c4/c6 → FEC committee is name-match only (THE WALL, confirmed by Issue One methodology). Model as EIN roster + probabilistic enrichment target.

**License:** SPLIT. **IRS layer = public domain, commercial-safe.** **ProPublica Nonprofit Explorer = PROPRIETARY** (no republish, no charge, no resale) — REFERENCE_ONLY, never land or reference it in ANY artifact (extend the ban to derived tables/notebooks/registry NOTES).

**Gotchas:** build on apps.irs.gov not AWS. 990 MeF XML is versioned by tax year — use jsfenfen/990-xml-reader (IRSx), don't hand-roll XPath or invent column names. BMF amounts have leading zeros / '000000000' sentinels, codes zero-padded ('04' not 4) — keep everything TEXT. 990 XML is e-filed only (paper/990-N thin).

**Build plan:** `build_irs_990_nonprofit.py`. Phase 1 (Day 1 win): BMF state CSVs → landing `FED_IRS_990_NONPROFIT`. Phase 2: index manifests → stream XML ZIPs → IRSx flatten → `FED_IRS_990_XML`. Staging (dedup EIN to latest TAX_PERIOD) → mart `POLITICS__NONPROFIT_POLITICAL` (SUBSECTION IN 04/06 + financials + probabilistic fec_cmte_match col). **Smoke:** unique+not_null EIN, SUBSECTION accepted_values, EIN-axis probe matches BMF set. **~4–6 days** (+2-3 for full multi-schedule XML).

---

#### `fed_irs_527` — IRS 527 political orgs (Form 8871/8872)

**What it is:** IRS bulk file of 527 political organizations — registrations + itemized donor contributions + expenditures. A NEW adjacent money domain (largely the COMPLEMENT of the FEC universe — FEC filers are exempt from 8871/8872).

**Endpoint:** `forms.irs.gov/app/pod/dataDownload/fullData` (341,461,225 bytes verified, ~1.9GB unzipped, weekly Sunday rebuild). **BOT-BLOCKED via Akamai** — needs a cookie-primed session (GET the portal page first, then /fullData reusing cookies; browser UA alone gets 302→404). Case-sensitive path.

**Schema/keys:** record_type discriminator (1=8871 org, 2=8872 report, A=Sched A donors, B=Sched B expenditures), EIN (9-digit, 100% on org rows), FORM_ID, CONT_NAME/EMPLOYER/OCCUPATION/AMOUNT, ORG_NAME/MISSION.

**Bolts on:** EIN → EIN axis (STEEL to 990/BMF/business). GEO via STATE/ZIP→FIPS. **NO FEC bridge** — FEC bans EIN from its filings, and FEC committees are exempt from 527 filing. Any FEC/member link is PROBABILISTIC.

**License:** Public domain (17 USC 105 / IRC 6104d, statutory disclosure). Commercial-safe. Donor PII is public-by-law (editorial care downstream, not a license bar).

**Gotchas:** MIXED record types in ONE pipe-delimited file, no header — demux on leading record-type code. ~0.1% corrupt lines (embedded newlines in mission fields) — defensive parse + quarantine. **Widest record is 50 fields (not ~46) — land COL_01..COL_52** or truncate 8872 headers. Electronic-only (paper filings absent from bulk). Snapshot-replace loses history (amendments overwrite).

**Build plan:** `build_pol_orgs_527.py` (session cookie-prime, demux, quarantine). Landing `FED_IRS_527` (RECORD_TYPE + COL_01..COL_52 TEXT). Staging per record type → marts `politics__pol_org_527` (EIN PK) + `politics__pol_org_527_contributions` (FORM_ID+SCHED_A_ID). **Model as `politics__pol_org_527*`, NEVER `politics__member_*`.** **Smoke:** each record_type present, >95% orgs have 9-digit EIN, Sched A FORM_IDs resolve to 8872, amount/date parse >99%, quarantine <0.5%, 527 EINs match BMF set. **~3–5 days.**

---

#### `fed_house_ptr` — House STOCK Act stock trades

**What it is:** House members' periodic transaction reports — every stock trade they disclose. Marquee accountability join (trades × votes × money × bills). House only.

**Endpoint:** index `disclosures-clerk.house.gov/public_disc/financial-pdfs/{YEAR}FD.zip` → XML (daily-refreshed, 2637 filings/515 PTRs for 2025). PTR PDFs at `/public_disc/ptr-pdfs/{YEAR}/{DocID}.pdf`. Bootstrap-only parsed feed: `TattooedHead/house-stock-watcher-data` (bus-factor=1, no license, null-byte corruption). Portal page 403s to bots — hit ZIP/PDF paths directly with a browser UA.

**Schema/keys:** DocID (filing PK), FilingType (P=PTR), Last/First name, StateDst (TN07), transaction_date, ticker, type (Purchase/Sale/Exchange), amount (BAND, model min/max/mid), owner. **NO native bioguide.**

**Bolts on:** name+StateDst → bioguide crosswalk (PROBABILISTIC native, STEEL only on matched rows) → MEMBER_CROSSWALK → whole spine. ticker → equities/CIK.

**License:** **CONDITIONAL — journalism carve-out only.** Statute (5 U.S.C. 13107(c)(1), verified verbatim) bans commercial use "other than by news and communications media for dissemination to the general public." Fits Chris's journalism/publishing path; raw-data resale = REFERENCE_ONLY. Practical enforcement risk near-zero (Unusual Whales/Capitol Trades resell openly), but resale stays off-limits.

**Gotchas:** XML index is a LOOKUP, not the trades — ticker/amount live ONLY in the PDF. **Real PTR PDFs include scanned JPEG images → OCR required on CURRENT filings** (confirmed DocID 20032062) — budget OCR in v1, hold effort at top of range. amount is always a band. Two PDF paths (PTR vs annual FD) — route by FilingType or 404. Self-reported, late, amended (dedup on DocID, keep amendment lineage). Parsed feed has garbage future tx_dates — sanity-filter.

**Build plan:** `build_fed_house_ptr.py`. Stage A: XML index (idempotent). Stage B: PTR PDFs via pdfplumber + Tesseract OCR fallback, checkpointed. Two landing tables. Staging (amount band → min/max/mid) → intermediate `int_fed_house_ptr_bioguide` (fuzzy name+StateDst → crosswalk, with unmatched-filer QUARANTINE) → marts `politics__member_trades` + `politics__member_ptr_filings`. **Smoke:** >20k rows, >150 distinct bioguides, MAX date within ~2 weeks, ZERO null bioguide after crosswalk (report match rate as build metric). **~6–7 days.**

---

#### `fed_lda_lobbying` — Federal lobbying disclosures (LD-1/LD-2/LD-203)

**What it is:** The full LDA filing universe — who lobbied whom on what, and LD-203 contributions to member honorees. Domestic sibling of already-landed FARA.

**Endpoint:** `lda.gov/api/v1/` (NEW canonical host — `lda.senate.gov`'s LAST live day is 2026-06-30). Paginated REST. Optional free key raises 15→120 req/min. Live counts verified exact: filings 96,877 (2024), LD-203 38,830, registrants 17,365.

**Schema/keys:** filing_uuid (PK), registrant/client/lobbyist.id (LDA-internal), general_issue_code, covered_position (revolving-door), honoree_name/payee_name (LD-203, free text). **Zero structured FEC/bioguide ID anywhere** (verified — the scout-era "FEC_CMTE_ID probable" is dead).

**Bolts on:** PROBABILISTIC only — honoree_name → member/FEC, org name → EIN, covered_position → bioguide. No steel key.

**License:** Public record / US gov work — SHIP. No copyright, no commercial-use restriction, no redistribution ban (only integrity + rate-limit + as-is disclaimer). Commercial-safe.

**Gotchas:** **repoint ALL loaders/registry from lda.senate.gov → lda.gov NOW.** Pagination is hostile — page_size caps at 25, bare list = 400, ~2,500-record ceiling → use existing `loadkit/windowed.py` (the pre-solved LDA fix) or silently truncate. NO structured bill_number (bills only in free-text descriptions). Deeply nested — explode activities × lobbyists into child grains. Existing scouted slug `fed_senate_lda` in _ALREADY_REGISTERED (line 791) — reconcile, and the append-only registry can't refresh it (land under new id or ship an authorized one-row UPDATE).

**Build plan:** `build_lda_lobbying.py` (windowed.py referee). 4 landing tables (filings + activities + lobbyists + contributions). Staging views → marts `politics__lda_filings`, `lda_issues`, `lda_lobbyists` (revolving-door), `lda_contributions` + a FEC referee mart (name-match + confidence, NEVER hard join). **Smoke:** landing count = API envelope count per year (zero silent truncation), filing_uuid unique+100% non-null, issue codes in constants enum, LD-203 amounts reconcile, ≥1 honoree name matches MEMBER_CROSSWALK. **~4–6 days.**

---

#### `st_openstates` — 50-state bills, votes & legislators

**What it is:** Plural/Open States — the biggest open legislative dataset. ~7,400 state legislators + millions of state bills/votes. An entire accountability tier the Library has ZERO coverage of below the federal line.

**Endpoint:** open S3, unauthenticated. People (nightly): `data.openstates.org/people/current/{ABBR}.csv` (53 files). Full warehouse (monthly): `data.openstates.org/postgres/monthly/2026-06-public.pgdump` (10.6GB, dated 2026-06-01 — **build against 2026-06; the 2026-07 dump is 403/not-yet-published**). ID crosswalk: `openstates/people` GitHub YAML. `/downloads` redirects to public `/data` (NOT login-walled — only the experimental session-csv is gated).

**Schema/keys:** ocd-person UUID (native PK, universal), bioguide+fec (**us-subset YAML ONLY** — verified Aaron Bean B001314/H2FL04211), state+district+chamber (GEO). **wikidata REFUTED — 0/160 state YAMLs, 0% of state CSV columns.**

**Bolts on:** SPLIT. US-Congress subset = STEEL bioguide/fec (but redundant with congress-legislators = validation not net-new). **The real prize = ~7,400 state legislators + state bills/votes: THE WALL — join keys are ocd-person UUID + GEO + name-match ONLY.** Extends the spine sideways into states, doesn't deepen the federal core.

**License:** GREEN. People repo = formal CC0-1.0; bulk bill/vote data = public-domain dedication (attribution appreciated, not required). The CC BY-SA 3.0 seen in Open States materials is the SOFTWARE license, not the data. **Do NOT source via OpenSanctions mirror (their CC BY-NC wrapper). Pull direct from data.openstates.org.**

**Gotchas:** grab-now — Plural is drifting friendly paths behind login. Phase 2 needs 10.6GB pg_restore to ephemeral Postgres + COPY OCD tables. Bills/votes carry no federal person ID.

**Build plan:** **PHASE 1 (do first, 1.5d, high ROI):** `build_openstates_people.py` — 53 people CSVs + openstates/people YAML → landing `ST_OPENSTATES_PEOPLE`. Marts `politics__state_legislators` (key ocd-person, NOT wikidata) + `politics__openstates_id_crosswalk` (us-subset bridge). **PHASE 2 (3-4d):** `build_openstates_bills.py` — pgdump → pg_restore → COPY → landing (bills/sponsorships/votes/vote_people/actions). Marts `politics__state_bills`, `state_bill_sponsors`, `state_votes`. **Smoke:** state_legislators ≈7,400 all with state+chamber; crosswalk bioguide set ⊆ MEMBER_CROSSWALK.bioguide (drop the wikidata check — returns 0); state_bills >500k; idempotency. **~4–6 days.**

## Dependency & sequencing

Most Tier 1 is independent — steel keys already exist in the warehouse, nothing to wait on. The dependencies are all in Tier 2's name-resolution chains.

**Hard dependencies:**
- `fed_fjc_judges` (nid judge spine) → `fed_courtlistener` disclosures (fjc_id crosswalks INTO the FJC universe) → `xc_judicial_common_space` (SCOTUS/CoA ideology hangs off both). **Load FJC first** or CourtListener/JCS have nothing durable to bolt to.
- `st_openstates` Phase 1 (ocd-person state-legislator spine) → `st_shor_mccarty` (its only real join partner is ocd-person; without it, Shor-McCarty is GEO + career-jumpers only). **Land Open States people before Shor-McCarty** if you want the state-level join.
- The **name-resolution moat** (below) → `fed_house_ptr` + `fed_lda_lobbying` (both need name→bioguide + name→EIN crosswalks before their marts fire).

**Independent quick hits (no dependencies):** `fed_unitedstates_committees`, `fed_govinfo_billsum`, `fed_congress_press`, `fed_congresstweets`, `fed_voteview_hsall`, `fed_fec_committee_to_candidate` refresh, `fed_irs_527`, `fed_irs_990_nonprofit`. All bolt onto keys that already exist.

**Concrete load ORDER:**

```
1.  fed_fec_committee_to_candidate   (refresh — fix paths, finish the mart; 0.5-1d)
2.  fed_unitedstates_committees      (fastest steel win; 1-1.5d)
3.  fed_voteview_hsall               (biggest value; 1.5-2.5d)
4.  fed_govinfo_billsum              (bill enrichment; 1.5-2d)
5.  fed_congress_press               (text layer; 2-3d)
6.  fed_congresstweets               (frozen — grab now; 2-3d)
7.  fed_fjc_judges                   (judiciary spine — BLOCKS 8+9; 1-1.5d)
8.  fed_courtlistener                (needs #7; 3-4d)
9.  xc_judicial_common_space         (needs #7 & SCDB; 1d)
10. st_openstates Phase 1 (people)   (state spine — BLOCKS #11; 1.5d)
11. st_shor_mccarty                  (needs #10 for real join; 1-1.5d)
12. [build name-resolution moat]     (BLOCKS 13+14)
13. fed_lda_lobbying                 (needs moat + host swap to lda.gov; 4-6d)
14. fed_house_ptr                    (needs moat; OCR-heavy; 6-7d)
15. fed_congress_govinfo_bills+plaw  (storage decision; 3-5d)
16. fed_irs_527 / fed_irs_990        (EIN axis; independent; 3-5d / 4-6d)
17. xc_dime_cfscores                 (email Bonica first; 2-3d)
18. st_openstates Phase 2 (bills)    (heavy pg_restore; 3-4d)
```

## The shared moat — name-resolution infra Tier 2 needs

Below the federal/Congress line there is NO shared person ID. Every Tier 2 source pays the name-resolution tax, and they pay it TWICE if each build rolls its own matcher. Build these crosswalks ONCE as shared infra — lean on the existing `connect/` module (`bridge.py` / `match.py` / `resolve.py` / `fingerprint.py`), which already does fingerprinted entity resolution. Scored on value, tagged with confidence you'll actually achieve.

| Crosswalk | Feeds | Method | Achievable confidence | Value |
|-----------|-------|--------|----------------------|-------|
| **name+state+district → bioguide** | `fed_house_ptr`, `st_shor_mccarty` (jumpers) | fingerprint surname + GEO + term-span (the build_who_won.py pattern) | HIGH for current House (closed set ~440); MEDIUM for jumpers/nicknames | **Highest** — unlocks trades×votes |
| **SCOTUS justiceName → SCDB → FJC nid** | `xc_judicial_common_space`, `fed_fjc_judges`, `fed_courtlistener` | closed-set 49-row hand crosswalk (SCDB convention matches) | HIGH (49 fixed, near-steel) | High — one small table, three sources |
| **EIN ↔ org-name → FEC-committee** | `fed_irs_527`, `fed_irs_990`, `fed_lda_lobbying` | fingerprint org name; EIN self-join is steel, EIN→FEC is name-only (THE WALL) | STEEL on EIN self-join; LOW/MEDIUM EIN→FEC (name-match, human sign-off) | High — the dark-money bridge |
| **honoree_name → member (LD-203)** | `fed_lda_lobbying` | normalize "The Honorable X" / "X for Congress" → fingerprint → MEMBER_CROSSWALK | MEDIUM (heavy normalization needed) | Medium — lobbyist money→Congress |
| **ocd-person → bioguide (us-subset)** | `st_openstates`, `st_shor_mccarty` | direct — us YAML carries bioguide (STEEL); state side is ocd-person + name only | HIGH for us-subset; N/A state (no federal key) | Medium — validates crosswalk |
| **CoA judge name+circuit → FJC nid** | `xc_judicial_common_space` | fuzzy name+circuit; 66 surname collisions → disambiguate on circuit + first name | MEDIUM (irreducibly fuzzy) | Lower — CoA enrichment |

**Doctrine (non-negotiable):** every one of these except the SCOTUS closed set and EIN self-join is PROBABILISTIC. Store `match_method` + confidence on every joined row. A name-match NEVER reads as a hard identity, and no person-level published claim ships without human sign-off (detective-trust doctrine). Build an unmatched-filer QUARANTINE table for each so `not_null` tests don't silently amputate the misses — report match rate as a build metric.

## License triage

**COMMERCIAL-SAFE — build freely, no strings:**
- `fed_unitedstates_committees` (CC0)
- `fed_fec_committee_to_candidate` (public domain — payers are committees, not individuals)
- `fed_govinfo_billsum` (public domain §105)
- `fed_congress_govinfo_bills` + `fed_govinfo_plaw` (public domain §105)
- `fed_fjc_judges` (public domain)
- `fed_irs_527` (public domain 17 USC 105 / IRC 6104d)
- `fed_irs_990_nonprofit` — **IRS LAYER ONLY** (public domain)
- `fed_lda_lobbying` (public record, no copyright/commercial restriction)
- `st_shor_mccarty` — **PINNED April-2023 CC0 DOI ONLY** (NWSYOS/7067107)
- `xc_judicial_common_space` (CC0 via Dataverse mirror)
- `fed_courtlistener` — **BULK S3 ONLY** (Public Domain Mark)
- `st_openstates` (CC0 people repo / public-domain-dedication bulk — pull direct from data.openstates.org)

**ATTRIBUTION — build, but credit:**
- `fed_congress_press` (MIT — retain Willis attribution)
- `fed_congresstweets` (MIT — retain Litel attribution; ship derived metrics, not raw-tweet republishing)
- `fed_voteview_hsall` (no data license — attribution-requested, cite Lewis et al. 2026; data is NOT MIT, code is)
- `xc_dime_cfscores` (ODC-BY — carry Bonica 2024 attribution; email to confirm before commercial derivative)
- `fed_house_ptr` (journalism carve-out — SAFE for Chris's publishing path, credit good practice)

**LANDMINE / REFERENCE-ONLY — never ship on:**
- `st_shor_mccarty` **Jan-2025 release (SGOQ7G)** — CC BY-NC-SA 4.0 NONCOMMERCIAL. Registry must pin CC0 DOI + flag this; never auto-follow "latest."
- `fed_irs_990_nonprofit` **ProPublica Nonprofit Explorer** — PROPRIETARY (no republish/charge/resale). Never land or reference in ANY artifact.
- `fed_courtlistener` **REST API v4** — avoid (rate-limited, no bulk semantics; use bulk S3).
- `st_openstates` **OpenSanctions mirror** — their CC BY-NC wrapper poisons it; pull direct.
- `fed_house_ptr` **raw-trade-record resale / paid API** — statutory commercial-use ban (fine for journalism, off-limits for a data product).

## URGENT / time-boxed — grab now

| Source | Why urgent | Action |
|--------|-----------|--------|
| **`fed_lda_lobbying`** | `lda.senate.gov`'s LAST live day is **2026-06-30 (today)** | Repoint ALL loaders/registry URLs to `lda.gov` immediately; host swap only, paths identical |
| **`fed_congresstweets`** | Frozen dead archive (ended 2023-07-11); single maintainer; git history self-declared VOLATILE/prunable | Clone/mirror BOTH repos now — don't depend on the live repo persisting |
| **`xc_dime_cfscores`** | Single-professor personal Dropbox; rlkey tokens can rotate/die with no notice; no API | Snapshot recipients + contributors + SQLite the moment you onboard |
| **`xc_judicial_common_space`** | Single-maintainer personal Squarespace; CC0 fallback frozen at 2007 vintage — 2024 currency lives ONLY on the WUSTL site | Archive the 2024 zip on land (SHA256 1e98021e...) |
| **`st_shor_mccarty`** | Frozen at 2020; upstream NPAT survey wound down; PIN the CC0 DOI before the NC successor tempts a "refresh" | Land the pinned CC0 file + license-guard NOTE now |
| **`st_openstates`** | Commercial owner (Plural) quietly gating friendly paths behind login; open S3 could follow | Snapshot the 2026-06 Postgres dump + people repo while the door is open |
| **`fed_house_ptr` parsed feed** | Only live parsed fork (TattooedHead) is bus-factor=1, 0 stars, no license; the original repo is already DELETED | Bootstrap-mirror now, but self-parse the Clerk PDFs for durability |

The primary/institutional sources (FEC, GovInfo, Voteview, IRS, FJC, CourtListener bulk, Open States dump) are NOT grab-now-or-lose-it — but the community/academic single-maintainer ones above genuinely are.

## My take — the next 5 loads

1. **`fed_fec_committee_to_candidate` (refresh)** — you're closest to done here and it's currently broken (Windows paths, a mart the registry lies about existing). Fix it, finish `politics__member_pac_money`, and the money box score is complete. ~1 day, highest "clean up what's half-built" value.
2. **`fed_unitedstates_committees`** — 1 day, CC0, pure steel bioguide, adds the gavel dimension the spine is missing. Fastest genuine new capability.
3. **`fed_voteview_hsall`** — the single biggest win in the whole batch. One loader turns 2 congresses into 1789-present on the key that threads everything. Just stream the 700MB file.
4. **`fed_fjc_judges`** — 1 day, public domain, opens the entire third branch (judiciary spine) AND unblocks CourtListener + JCS. Load it before those two or they have nothing to bolt to.
5. **`fed_congress_press`** — the text/rhetoric layer, first-party bioguide at 99.7%, pairs "what they SAID" with the numbers spine. High narrative payoff for the publishing layer, low risk.

That's ~7-9 days for five loads that each land clean on existing steel — no name-resolution moat required yet. Build the moat right before you tackle LDA + House PTRs, which is where the real name-matching work (and the biggest accountability payoffs) begin.

---

## Backfill dossiers (the 3 that blew the schema)

#### `fed_demandprogress_earmarks` — House FY2024 Earmark Requests, Enhanced (Demand Progress Ed. Fund)

**What it is:** A Google Sheet where Demand Progress Education Fund (via the Congressional Data Coalition) took the House Appropriations Committee's raw FY2024 earmark **request** disclosures and bolted on machine-readable metadata — most importantly a **Member Bioguide ID** per row, plus subcommittee codes and a GPT-standardized recipient address parsed into state/zip. It's a *request* dataset (what members asked for), not a *funded/awarded* dataset.

**Endpoint:** Live, verified 2026-06-30.
- Human page: `https://congressionaldata.org/house-publishes-more-earmarks-request-data-which-we-enhance/`
- Data (Google Sheet): `https://docs.google.com/spreadsheets/d/10ft_qlgolr7Nuf-gY-XCiECtPBXCtqFb6HgTZNtvLcY/edit`
- CSV export (loader target, no auth): `https://docs.google.com/spreadsheets/d/10ft_qlgolr7Nuf-gY-XCiECtPBXCtqFb6HgTZNtvLcY/export?format=csv&gid=<GID>` — verified: returns 307 → `googleusercontent.com` and serves the CSV. No API key. Public "anyone with link" sheet.

**Schema/keys:** One row = **one earmark request by one House member**. Verified header row on the `Earmarks` tab:
`Member Last Name, Member First Name, District, Party, Member Bioguide ID, Appropriator?, Subcommittee, Subcommittee Code, Recipient, Project Purpose, Recipient Address, Formatted recipient addresses (via GPT), Recipient State (Extracted via Formula), Recipient Zip Code (Extracted Via Formula), Amount Requested, Member Website`
- **STEEL key present & populated:** `Member Bioguide ID` — confirmed real values (e.g. B001301, C001112) throughout the visible rows.
- Other tabs: `General Statistics`, `MemberData`, `SubCmteCodes`, `States`.
- GEO: recipient **State** + **Zip** (parsed, GPT-assisted → dirty). No FIPS, no EIN, no UEI, no recipient bioguide — recipient is a free-text org name + GPT-formatted address.

**Bolts on:** `LIBRARY_MARTS.POLITICS.MEMBER_CROSSWALK` / `MEMBER_SPINE` via **BIOGUIDE = STEEL**. This is the good news — it plugs straight into the politics spine with zero name-matching, House-side. Expected bioguide population ~100% of rows (it's the whole point of the enhancement). Recipient side is **PROBABILISTIC only** (org name) or **GEO-weak** (GPT-parsed state/zip, unvalidated) — do not treat recipient joins as steel.

**License:** **UNSTATED = LANDMINE (REFERENCE_ONLY).** Checked congressionaldata.org, the guide page, the Demand Progress Ed. Fund privacy policy — **none** state a license, copyright grant, public-domain dedication, or CC mark for the data. The *underlying* House Approps disclosure is a government record (public-domain facts), but the **enhancement layer** (bioguide match, GPT-formatted addresses, subcommittee codes) is Demand Progress's original work with no license granted. For a commercial ceiling, redistributing their enhanced sheet without a license is the exact landmine to avoid.

**Freshness:** **Frozen / one-shot.** Verified: only **FY2024** exists — no FY2022/FY2023/FY2025/FY2026 enhanced version published. FY2025 (P.L. 119-4) funded no earmarks. Site itself is alive (last post 2026-06-16) but this dataset hasn't been refreshed and there's no cadence commitment. **Bus factor: high** — single Google Sheet, single org, "still tinkering," no versioned archive.

**Gotchas:**
- **Requests ≠ awards.** These are what members *asked for*, not what got funded. Do not join to USASpending CONTRACTS as if these are outlays — you'll overstate. Different universe from funded-project data.
- **House only.** No Senate CDS in this sheet.
- **GPT-derived columns are dirty** (recipient address, state, zip) — the org flags them as experimental/AI. Never use as a hard geo key.
- **Google Sheet, not a stable file** — owner can edit/move/revoke sharing any day; snapshot-and-SHA on every load, expect drift. The `gid` per tab must be pinned or the export grabs the wrong tab.
- **Amount Requested** is free-text with `$`/commas — clean before casting.
- License risk means you likely can't republish it downstream even if you land it.

**Build plan:**
- Loader: `politics/loaders/load_demandprogress_earmarks.py` — `requests.get` the CSV-export URL (follow the 307 to googleusercontent), pull the `Earmarks` tab by `gid`, pandas-parse all-TEXT, snapshot-replace into `LIBRARY_RAW.LANDING.FED_DEMANDPROGRESS_EARMARKS` with `_INGESTED_AT / _SOURCE_RUN_ID / _SRC_SHA256`, log `INGEST_RUNS`, skip on SHA match.
- Staging: `stg_demandprogress_earmarks__requests.sql` — snake_case, cast `amount_requested` to NUMBER, trim bioguide, keep GPT columns clearly suffixed `_gpt`.
- Mart: `politics__earmark_requests.sql` — one row per request, keyed on a surrogate + `member_bioguide_id`, joined to `MEMBER_CROSSWALK` for member name/state/party validation.
- Must-pass smoke test: `COUNT(*) > 0` AND `% rows with non-null member_bioguide_id > 99%` AND `100% of member_bioguide_id match MEMBER_CROSSWALK.bioguide` (any orphan = ingest/parse break).
- Effort: **~1 day** to land + stage (it's one small sheet). The work is the license call and recipient-side geo cleanup, not the pipeline.

**Verdict:** **STAGE (land internal-only, do NOT publish) → treat as REFERENCE_ONLY until license cleared.** The bioguide steel key is genuinely valuable and this bolts cleanly onto the politics spine House-side — but it's **one frozen FY2024 sheet with no license**, so land it as an internal reference/enrichment layer, keep the SHA snapshot, and get written reuse permission from Demand Progress before anything commercial touches it. If you want *broad, multi-year, license-cleaner* earmark coverage, **Taxpayers for Common Sense** (`taxpayer.net/budget-appropriations-tax/earmark-data/`) is the alternative to scout next — but I could not verify its file formats/bioguide/license live (their pages truncated on fetch), so that's an unverified lead, not a recommendation.

**Sources checked:**
- https://congressionaldata.org/house-publishes-more-earmarks-request-data-which-we-enhance/
- https://docs.google.com/spreadsheets/d/10ft_qlgolr7Nuf-gY-XCiECtPBXCtqFb6HgTZNtvLcY/edit (columns + bioguide populated, verified)
- https://docs.google.com/spreadsheets/d/10ft_qlgolr7Nuf-gY-XCiECtPBXCtqFb6HgTZNtvLcY/export?format=csv (307 redirect → CSV serves, verified)
- https://congressionaldata.org/ (site alive, last post 2026-06-16; no license stated)
- https://congressionaldata.org/a-biased-yet-reliable-guide-to-sources-of-information-and-data-about-congress/ (no license stated)
- https://demandprogresseducationfund.org/privacy/ (no data-reuse/copyright terms)
- https://www.taxpayer.net/budget-appropriations-tax/earmark-data/ and .../earmark-and-appropriations-data/ (alternative lead — pages truncated on fetch, **unverified**)

---

#### `xc_google_political_ads` — Google Political Ads Transparency (BigQuery public dataset)

**What it is:** Google's public archive of every election/political ad served on Google Ads, Search, YouTube and Display in verified regions — advertiser identity, spend ranges, impression ranges, run dates, and geo/demographic targeting, published as a queryable BigQuery public dataset. One row in the core table = one ad creative's lifetime stats.

**Endpoint:** BigQuery public dataset `bigquery-public-data.google_political_ads` (confirmed live, actively updated as of Oct 2025). Auth = any Google Cloud project with the BigQuery API on; **Google pays storage, you pay query compute — first 1 TB/month free**. No REST scrape needed. Load path: `bq query`/BQ client → export table to GCS as Parquet/CSV → pull to Snowflake landing. Confirmed tables: `creative_stats`, `advertiser_stats`, `advertiser_weekly_spend`, `geo_spend`. A regulatory-ID-bearing `advertiser_declared_stats` / "advertiser-declared" table is referenced by Google but **I could NOT verify its exact table/column name from text** — the schema doc (support.google.com answer 9575640) and the marketplace listing are JS-rendered and un-scrapable. **Must confirm the real name via `INFORMATION_SCHEMA.COLUMNS` at load time.**

**Schema/keys (verbatim where confirmed):**
- `creative_stats` — confirmed columns: `advertiser_id`, `advertiser_name`, `ad_id`, `ad_type`, `gender_targeting`, `geo_targeting_included`, `date_range_start`, `date_range_end`, `impressions` (**bucketed as text**, e.g. `"1000000-1250000"`, `"1250000-1500000"`, `"≥10000000"`). Spend is likewise **reported as ranges, not exact dollars** (confirmed by Google's own blog + FAQ; exact spend column names like `spend_range_min_usd`/`spend_range_max_usd` are the widely-used convention but **not text-verified here** — confirm in schema).
- Geo granularity: **state AND congressional district** (Google's own blog: "how much money is spent across states and congressional districts"). `geo_spend` = spend per US state.
- `advertiser_weekly_spend` — spend over time; **lacks a region column** (must join back via `advertiser_id`).
- Join spine: everything joins on **`advertiser_id`** (STEEL within this dataset) → `advertiser_name`.
- **The prize field — advertiser-declared FEC ID / EIN:** Google states outright that advertisers provide **"FEC or EIN information directly in their library,"** and that a **regulatory ID (FEC ID, EIN)** is shown to disambiguate same-named advertisers. So the identifier exists in the product — **but exact column name and populated-% are UNVERIFIED from text.**

**Bolts on:** Politics money spine. **IF** the advertiser-declared FEC committee ID is real and populated, it bolts to `LIBRARY_MARTS.POLITICS.MEMBER_FEC_ID` / `FEC_CANDIDATE` via **`FEC_CMTE_ID` — STEEL**, letting you tie digital ad spend to the same committees already carrying itcont donations + USASpending. **Honest population estimate: LOW-to-MODERATE and unverified.** The regulatory ID is *advertiser-declared and optional* — most advertisers are name-only. Realistic read: **STEEL for the subset that declares an FEC ID (likely a minority — think campaign committees & PACs, not every advertiser), PROBABILISTIC (name-match) for the rest.** Below the committee line it's GEO (state/CD → FIPS) + PROBABILISTIC. **Do not promise steel coverage until you've run `COUNT(*) WHERE regulatory_id IS NOT NULL` on the real table.**

**License:** **This is the sharp edge for a commercial build.** BigQuery public-dataset docs give a blanket "Google pays storage, you pay queries" access model but **carry NO explicit open/CC license for `google_political_ads`** — unlike truly public-domain BQ datasets, this one is Google's own ad data governed by **Google Terms of Service** ("you may use Google's content as allowed by the terms… Google retains IP rights in its content"). No CC-BY, no public-domain grant found. The peer-reviewed Meta/Google comparison paper published its Google-derived data under **CC BY-NC** precisely because of third-party-data restrictions. **Verdict: ATTRIBUTION-at-best, LANDMINE-risk for redistribution.** Querying/analyzing = clearly fine. **Re-publishing the raw rows commercially = unconfirmed rights → treat as REFERENCE_ONLY until Chris gets a straight read on Google's ToS for this dataset.** Derived aggregates/visualizations (what watchdogs and researchers do) are the intended, safe use.

**Freshness:** **LIVE and healthy.** Google added a dedicated political-ads tab to the Ads Transparency Center in **Oct 2025**; new ads appear within **48–72h**; data begins **2018** with a **7-year retention** window. BigQuery dataset updates in step with the online library. Bus-factor = Google (low risk of disappearing, but Google *has* pulled political-ads products in some regions for regulatory reasons — EU TTPA caused service changes — so region coverage can shrink).

**Gotchas:**
- **Everything is a RANGE, not a number.** Spend and impressions are text buckets (`"1000000-1250000"`). You cannot sum them — staging must derive `spend_min`/`spend_max`/`spend_mid` from the string. This breaks any naive SUM.
- **`impressions` is TEXT with `≥`/`-` glyphs** — parse carefully.
- **The FEC ID may not exist as a clean column, or may be sparse.** The entire steel-join thesis rests on a field I could not text-verify. **First load action: dump `INFORMATION_SCHEMA.COLUMNS` and profile null-rate.**
- **`advertiser_weekly_spend` has no region** → US-filter via a join, or you'll pull global rows.
- **Region scope drifts** — EU regulation has forced Google to alter/suspend political ads in places; don't assume static country coverage.
- **BQ→Snowflake is a two-hop** (BQ → GCS Parquet → Snowflake); no direct connector in the current stack. Budget for the export step.
- Ranges + advertiser self-declaration mean **spend figures are directional, not audit-grade** (DELTA Lab documented spend-reporting discrepancies).

**Build plan:**
- Loader: `politics/loaders/load_xc_google_political_ads.py` — BQ client queries `creative_stats`, `advertiser_stats`, `advertiser_weekly_spend`, `geo_spend` (+ the declared/regulatory table once its name is confirmed), exports to GCS Parquet, lands to `LIBRARY_RAW.LANDING.XC_GOOGLE_POLITICAL_ADS` (all TEXT, snapshot-replace, + `_INGESTED_AT`/`_SOURCE_RUN_ID`/`_SRC_SHA256`). Idempotent on SHA-256.
- Staging: `stg_xc_google_political_ads__creative`, `__advertiser`, `__weekly_spend`, `__geo_spend` — snake_case, cast dates, **derive `spend_range_min`/`spend_range_max`/`spend_mid` and `impressions_min`/`impressions_max` from the text buckets**, cast the declared FEC ID.
- Marts: `politics__ad_spend` (advertiser × ad, ranged spend, FEC ID where present), `politics__ad_spend_by_geo` (state/CD → FIPS). Wire `politics__ad_spend` to `MEMBER_FEC_ID` on `FEC_CMTE_ID` **only after** confirming the field populates.
- **Must-pass smoke test:** (1) landing row count > 0 for `creative_stats`; (2) `COUNT(*) WHERE regulatory_id IS NOT NULL` printed so Chris sees the *real* steel-join coverage before trusting it; (3) US-region rows present; (4) a ranged spend column parses to non-null min/max.
- Effort: **3–4 days** (extra day for the BQ→GCS→Snowflake export plumbing that isn't in the current CSV/API loaders, plus schema-discovery for the declared table).

**Verdict:** **STAGE (lean CAUTION).** The data is genuinely valuable and the source is alive and well-maintained — but two load-critical unknowns keep it out of straight-GO: (1) the FEC-committee steel join is **plausible but text-unverified and probably sparse**, and (2) the **license gives no clear commercial-redistribution grant** (Google ToS, not CC/public-domain). Land it, profile the FEC-ID column on day one, and hold it **REFERENCE_ONLY for any raw redistribution** until Chris confirms Google's reuse terms.

**Sources checked:**
- https://cloud.google.com/blog/topics/developers-practitioners/how-get-started-political-ads-transparency-report-dataset
- https://blog.google/technology/ads/introducing-new-transparency-report-political-ads/
- https://docs.cloud.google.com/bigquery/public-data (cost model + no blanket license)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12149306/ (Meta/Google comparison; CC BY-NC on derived data)
- https://ppc.land/google-adds-political-ads-to-transparency-center/ (Oct 29 2025 — confirms live + 48-72h freshness)
- https://deltalab.research.wesleyan.edu/2021/02/22/google-advertiser-discrepancies/ (advertiser_stats, spend discrepancies)
- https://support.google.com/transparencyreport/answer/9052272 (FAQ; FEC/EIN regulatory ID language)
- Attempted but JS-gated/un-scrapable (schema + license verbatim NOT obtained): marketplace listing `console.cloud.google.com/marketplace/product/transparency-report/google-political-ads`, schema doc `support.google.com/transparencyreport/answer/9575640`, `adstransparency.google.com/political/faq`

**Two items I could not text-verify and flagged as such:** (1) exact name/columns of the advertiser-declared/regulatory-ID table, and (2) verbatim license text for the dataset. Both must be resolved by querying `INFORMATION_SCHEMA` and reading Google's ToS at load time — I did not invent either.

---

#### `fed_usaspending_grants` — USASpending Financial Assistance (Grants + Loans) + FSRS Sub-Awards

**What it is:** The financial-assistance side of USASpending — every federal grant, direct payment, loan, and insurance award transaction (the twin of Ripple's existing 6.3M-row contracts source), plus sub-award (pass-through) data from FSRS File F. Government-wide "who got federal non-contract money."

**Endpoint:** Verified live, free, no auth.
- **Prime grants/loans:** `POST https://api.usaspending.gov/api/v2/bulk_download/awards/` — same endpoint the contracts loader already uses; swap `prime_award_types` to assistance codes `["02","03","04","05","06","07","08","09","10","11"]` (02=block grant, 03=formula grant, 04=project grant, 05=cooperative agreement, 06/07/08=direct payments, 09=insurance, 10=direct loan, 11=guaranteed/insured loan). Async: POST → poll `status_url` → download ZIP of `Assistance_PrimeTransactions_*.csv`.
- **Sub-awards (FSRS File F):** NO dedicated `bulk_download/subawards` endpoint exists. Verified path is `POST https://api.usaspending.gov/api/v2/download/search/` with `spending_level: "subawards"` (agencies optional, confirmed in the API contract). Returns a `SubAwards` CSV member.

**Schema/keys:** Confirmed present in the assistance download (data dictionary): `assistance_transaction_unique_key` (row grain), `fain`, `uri`, `cfda_number` + `cfda_title` (**CFDA is a real populated column here — unlike contracts**), `assistance_type_code`/`_description`, `recipient_uei`, `recipient_name`, `recipient_parent_uei`, `federal_action_obligation`, and for loans `face_value_of_loan` + `original_loan_subsidy_cost`. One row = one assistance award transaction. `usaspending_permalink` and county-FIPS columns are *not* confirmed by name from the dictionary excerpt — treat as unverified until a live 5-row preview.

**Bolts on:** Sits on the **money/politics money-spine**, not the Congress steel keys.
- **GEO/ENTITY (real, populated):** `recipient_uei` → same UEI key as `fed_usaspending_contracts` and SAM exclusions (STEEL-grade org ID where present; UEI populated for most post-2022 awards, DUNS before that). `cfda_number` → joins to CFDA/Assistance-Listings and to Ripple's existing `fed_hhs_taggs` grants mart (which is HHS-only ALN — this source is the government-wide superset). `recipient_state_code`/place-of-performance → FIPS/GEO.
- **NO Congress steel key.** This is below THE WALL for person-level linkage — there is no BIOGUIDE/ICPSR/FEC ID on a grant. Linkage to members is GEO (state/district of place-of-performance) or PROBABILISTIC (recipient_name), never steel. Honest population: UEI ~high on modern rows / sparse pre-2016; CFDA ~100% on assistance; member linkage 0% direct.

**License:** **U.S. Government work, public domain (17 U.S.C. § 105), no copyright, FFATA-mandated free public access; federal open-data policy = usable for any purpose commercial or non-commercial.** Verdict: **COMMERCIAL-SAFE.** Not a landmine. (Attribution courteous, not required.)

**Freshness:** **Live** — daily updates, monthly archive refresh by the 15th, data back to FY2008. Bus-factor: strong (Treasury-run, statutory mandate). Caveat: the `bulk_download/awards` endpoint has **open, unresolved intermittent-failure GitHub issues (#3017 Nov-2024, #4283 Feb-2025)** on large multi-day requests — Postgres-side generation timeouts. Mitigated by the existing month-by-month chunking pattern; not a blocker but expect occasional job retries.

**Gotchas:**
- **Loan dollars trap:** for loans, spend is in `original_loan_subsidy_cost` (net-present cost to gov), NOT `federal_action_obligation` (which is ~0 for loans). Face value ≠ cost. Mart must sum obligation + loan subsidy correctly or you'll undercount loans to zero.
- **Full-FY request will time out** — must chunk monthly (loader already does this).
- **`agencies` filter is documented "required"** in the API contract, but the live contracts loader omits it and works (empty = all agencies). Keep it omitted; don't "fix" it.
- **Sub-awards use a different endpoint** (`download/search`, `spending_level:subawards`) with a different response shape — do NOT assume the contracts loader handles File F.
- Assistance CSV member is named `Assistance_PrimeTransactions_*` (contracts are `Contracts_*`) — member-filter must not hardcode "Contracts".
- Volume: assistance is larger than contracts in row count for some years (millions/FY across all agencies).

**Build plan:**
- **Loader:** `politics/loaders/usaspending_grants_load.py` — near-verbatim fork of `scripts/usaspending_load.py`. Changes: `SID="fed_usaspending_grants"`, assistance `prime_award_types`, assistance `COLUMNS` list (with `cfda_number`, `fain`, `uri`, loan fields, unique key `assistance_transaction_unique_key`), CSV member filter `Assistance_`. Reuse the month-splitter, async poll, chunk-load, INGEST_RUNS log, SOURCE_REGISTRY upsert unchanged.
- **Sub-award loader (separate, phase 2):** small new function hitting `download/search` with `spending_level:subawards` → `LIBRARY_RAW.LANDING.FED_USASPENDING_SUBAWARDS` (different grain, don't co-mingle).
- **Landing:** `LIBRARY_RAW.LANDING.FED_USASPENDING_GRANTS` (all TEXT, snapshot-replace, `_INGESTED_AT`/`_SOURCE_RUN_ID`/`_SRC_SHA256`).
- **Staging:** `stg_fed_usaspending_grants__transactions.sql` — cast, snake_case, dedupe on `assistance_transaction_unique_key`; coalesce loan spend = `federal_action_obligation` + `original_loan_subsidy_cost`.
- **Marts:** `politics__federal_assistance` (grants+loans by recipient UEI + CFDA + geo) and optionally `politics__assistance_by_recipient` (rolled to UEI for money-spine joins).
- **Smoke test (must pass):** land one narrow month (e.g. 2025-01), assert row count > 0, `cfda_number` non-null on >95% of rows, `recipient_uei` non-null on a majority, loan rows (`assistance_type_code IN ('10','11')`) have `original_loan_subsidy_cost` populated and `federal_action_obligation` ≈ 0.
- **Effort:** prime grants/loans **~1.5 days** (loader is a fork); add sub-awards **+1.5 days** (new endpoint/shape) = **~3 days total**.

**Verdict:** **GO** (prime grants/loans) — public-domain, commercial-safe, reuses the proven contracts loader almost verbatim, carries real UEI + CFDA keys that bolt straight onto the money spine and the existing HHS-TAGGS grants mart. **STAGE** the FSRS sub-awards as a fast-follow (different endpoint, worth it for pass-through/conduit analysis). Only non-steel caveat: no Congress person-ID — this joins by org/place, not by member.

**Sources checked:**
- https://www.usaspending.gov/download_center/award_data_archive
- https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_contracts/contracts/v2/bulk_download/awards.md
- https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_contracts/contracts/v2/download/search.md
- https://api.usaspending.gov/api/v2/references/data_dictionary/
- https://api.usaspending.gov/docs/endpoints
- https://github.com/fedspendingtransparency/usaspending-api/issues/4283
- https://www.usaspending.gov/federal-spending-guide (loan column semantics)
- https://resources.data.gov/open-licenses/ (public-domain / commercial-use confirmation)
- Local: `/Users/chrisr./Documents/GitHub/Ripple_v6/scripts/usaspending_load.py` (contracts loader — the fork base)

---

**Two flags for the caller:** (1) unverified column names (`usaspending_permalink`, county-FIPS on assistance) — confirm with a live 5-row preview before finalizing the `COLUMNS` list; (2) the loan-dollars-in-subsidy-cost trap is the one thing that will silently corrupt the mart if the modeler treats it like contracts.

---

