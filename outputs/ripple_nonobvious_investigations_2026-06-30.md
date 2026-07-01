# Ripple -- The Non-Obvious Investigations

These aren't the "red counties take federal money" or "Dollars for Docs" headlines. Every idea below is a receipt nobody has assembled -- either because it needs two datasets from different worlds joined on a hard key, or because it flips a known dataset upside down. Cut anything that was already a story; what's left is the moat.

## Build TODAY (every table is already landed)

**The Four Ghosts: sanctioned tankers that sat in US waters under fake names**
Four OFAC-sanctioned vessels were physically pinging US AIS in Jan 2024 under names that don't match their sanctioned identity -- caught operating under an alias before designation.
Chain: `fed_ofac_sdn` (vessel IMO) ⋈ `fed_noaa_ais` on prefix-stripped IMO; AIS `VESSELNAME` != `SDN_NAME`. Verified: 4 of 1,497, LAFIT sailed as ADVANTAGE VIRTUE (1,322 pings, Gulf of Mexico).
Nobody's connected it: OFAC is read as a legal list, AIS as logistics -- never IMO-to-IMO across the name change. **Viz: map.**

**The Post-Exclusion Payroll: pharma kept paying doctors AFTER Medicare banned them for fraud**
317 still-excluded providers received itemized pharma/device payments dated after their exclusion; 118 were banned under 1128a1 (fraud conviction) -- Skye paid $114,040 in a single post-ban check.
Chain: `fed_hhs_oig_leie` (NPI, EXCLDATE, EXCLTYPE) ⋈ `fed_cms_open_payments`/`_2023` on NPI, gated `DATE_OF_PAYMENT > EXCLDATE`, `REINDATE='00000000'`. Restrict to the 8,684 real-NPI rows.
Nobody's connected it: OIG and OpenPayments publish separately; nobody date-gates payment against the ban. **Viz: timeline.**

**The 1937 Line, Drawn in Chalk: police killings by HOLC grade**
Every named, dated police killing dropped as a lat/lon point into the literal 1930s appraisal polygon it falls in -- and the majority-White vs majority-Black split flips exactly on the grade an appraiser assigned 90 years ago.
Chain: `xc_wapo_fatal_force` point ⋈ `fed_mapping_inequality` via `ST_WITHIN` (true point-in-polygon, not FIPS). Verified: A-grade 17/36 White, D-grade 212/463 Black. Normalize per polygon area; scope to the ~200 HOLC cities.
Nobody's connected it: redlining-to-health is done at tract level; individual killing points into the actual polygon is unclaimed. **Viz: map.**

**Natural-court velocity: dating the exact vote where a new justice flipped the median**
Rebuild the sitting-justice median ideology per Court composition and show precedent-breaking spikes clustering at the exact membership swaps where the median jumped.
Chain: `fed_scdb` (`natural_court`, `precedent_alteration`, dated) + `POLITICS__JUDGE_IDEOLOGY_SCOTUS` per-term `jcs` → median per natural_court, cross-checked against `POLITICS__JCS_MEDIANS.sc_median`. Dedup precedent flags to case grain; normalize per case decided.
Nobody's connected it: everyone eyeballs "the Court moved right"; nobody rebuilds the median from the bench and dates the lurch. **Viz: timeline.**

**The FARA Overlap: registered foreign agents sitting on sanctions lists**
Legally-registered foreign lobbying operators who are simultaneously OFAC-sanctioned -- a front-page contradiction between two federal statuses that are never reconciled.
Chain: `fed_fara_bulk` `FOREIGN_PRINCIPAL_NAME`+`COUNTRY` ⋈ `fed_ofac_sdn`/`intl_opensanctions` on normalized name, cross-checking FARA country against the sanctions program. Verified: 8 on SDN, 30 on OpenSanctions (Bank Melli, PDVSA, Press TV, RDIF).
Nobody's connected it: FARA (DOJ) and OFAC (Treasury) are administered separately and never publicly joined. **Viz: network.**

**Ghost Charities: nonprofits the IRS revoked that its own master file still lists as active**
30,933 EINs whose tax exemption the IRS revoked (never reinstated) still sit in the Business Master File flagged `STATUS='01'` -- ACTIVE tax-exempt. The IRS contradicting itself.
Chain: `fed_irs_revocation` (never-reinstated EIN) ⋈ `fed_irs_bmf` on EIN (LPAD to 9), filtered to `STATUS='01'`; confirm BMF vintage post-dates revocation. Layer `fed_cms_open_payments` charity-conduit payments for the name-and-shame case.
Nobody's connected it: auto-revocation is treated as bureaucratic noise, never intersected with the still-active master file. **Viz: sankey.**

**The shadow-fleet family tree: OFAC's REMARKS field is a hidden ownership graph**
Parse the free-text `REMARKS` string and one query turns a 19k-row list into named corporate fleets -- including the Chinese distant-water fishing giants (Fujian Pingtan = 78 hulls, sanctioned for forced labor) nobody covers.
Chain: `fed_ofac_sdn` only -- `REGEXP_SUBSTR(REMARKS,'Linked To: ...')` → parent, GROUP BY. Verified: IRISL 118, Sovcomflot 81, Pingtan 78. Normalize parent strings before grouping.
Nobody's connected it: OpenSanctions treats OFAC as a flat list; the fishing-fleet angle is entirely uncovered. **Viz: network.**

**The pharma-lightning-rod prescriber inside a 1-star home**
Named provider + named drug + dollar figure of pharma money, concentrated inside a nursing home CMS already rates as failing -- influence money landing exactly where residents are most captive.
Chain: `fed_cms_nursing_home` (`overall_rating<=2`, abuse_icon, SFF) → `fed_cms_facility_affiliation` (CCN↔NPI, 40k real rows) → `fed_cms_open_payments` on NPI. Weight the payment link by facility quality. Filter affiliation to physician/medical-director roles.
Nobody's connected it: Dollars-for-Docs never used facility star rating as the vulnerability weight. **Viz: network.**

**The $124.99 escalation clock: dating the pharma meal-cap blitz**
Time-slice the known just-under-$125 meal fingerprint to weekly and detect the exact weeks a manufacturer ramps cap-hugging meals to a target specialty -- turning a static behavior into a dated campaign.
Chain: extend `health__pharma_meal_cap_fingerprint` using `fed_cms_open_payments` `DATE_OF_PAYMENT` (filter the '11/30/0002' garbage); change-point detect the [124.00,124.99] F&B share per manufacturer per specialty (via NPPES specialty).
Nobody's connected it: the meal-cap cliff is a known Ripple finding but only as a yearly aggregate -- nobody asked *when* it ramps. **Viz: heatmap.**

**Excluded-provider clusters sharing one practice address (the pill-mill signature)**
208 practice addresses host 2+ OIG-excluded providers -- scattered bad doctors rolled up into one named business you can pull corporate records on.
Chain: `fed_hhs_oig_leie` (NPI) ⋈ `fed_cms_nppes` → group by normalized practice address (NOT EIN -- NPPES EIN is 100% null); rank by (# excluded NPIs) × combined Part D opioid cost.
Nobody's connected it: exclusions are analyzed per individual NPI; the address rollup that finds the org is the connect/ moat, unpublished. **Viz: network.**

## Go get it (small acquisition unlocks a big story)

**Grandfather's Handwriting -- the 1937 slur vs today's body count.** GET: the Mapping Inequality area-description JSON from dsl.richmond.edu (free per-city GeoJSON; the landed `AREA_DESCRIPTION_DATA` is empty `{}`). Unlocks: NLP-score the actual appraiser racial prose for venom and test whether the venom out-predicts the blunt A-D grade on named 2024 police deaths -- run through the already-verified point-in-polygon join. The single highest-impact idea in the set, one re-pull away.

**The recusal engine.** GET: CourtListener/Free Law Project Financial Disclosures (free bulk API, covers SCOTUS) + SCDB case-party names. Unlocks: an every-vote conflict scanner -- justices who voted on cases involving companies they held stock in, resolved to CIK via the landed `fed_sec_edgar_company_tickers`. Ship as leads requiring human sign-off.

**Foreign-client firm, federal contract.** GET: SAM.gov Entity Registration (public, gives UEI↔legal-business-name). Unlocks: hardening the fuzzy `fed_fara_bulk` registrant ⋈ `fed_usaspending_contracts` recipient join into a keyed one -- naming firms paid by a foreign government AND billing the US Treasury. The dual-hat conflict, UEI-confirmed.

**Breach-to-bailout firewall.** GET: HHS OCR Breach Portal CSV (free, keyed on covered-entity name+state). Unlocks: anti-join 1,058 US-healthcare `xc_ransomwarelive_victims` against the mandatory breach registry -- Medicare-billing providers a ransomware gang named who never filed the legally-required disclosure. The ones who paid quietly.

**Confirmation-vote money (senator-level).** GET: Senate.gov LIS roll-call XML (public, per-senator yea/nay on nominations). Unlocks: the landed `fed_fjc_service` only stores a chamber tally -- this restores named senator votes, letting you time each senator's donor money against their actual confirmation votes.

**The Vote-Then-Cash reward window.** GET: Congress.gov bill subject/policy-area codes (free API, joins to the landed bills mart). Unlocks: the industry-match half of the reward-frame detector -- flag members who voted against their DW-NOMINATE-predicted position (`fed_voteview` -- fully landed), then window donor money [+1,+30] days, and confirm the surging donor's industry matches the bill's topic.

## The 3 that would make people gasp

**The Post-Exclusion Payroll.** A named doctor, convicted of fraud and formally banned from all federal healthcare, with a $114,040 pharma check dated *after* the government banned them. Not a trend -- a receipt with a date. It exposes that the federal ban roster is invisible to the money.

**Grandfather's Handwriting.** If a 1937 appraiser's specific racial venom -- the actual sentence he wrote -- predicts who gets killed by police on that exact block in 2024 better than the blunt grade does, that's the most direct historical-injustice-to-body-count line anyone has drawn. One data re-pull from impossible.

**The Four Ghosts.** A named tanker, calling itself ADVANTAGE VIRTUE, working the Gulf of Mexico off Louisiana in January 2024 -- eight months before Treasury sanctioned it as LAFIT, part of Iran's shadow fleet. Exact coordinates, exact ping count, a name that doesn't match its future sanction. A map you can point at.

## The multiplier

The single capability that separates Ripple from every newsroom is **entity resolution across the fuzzy bridges** -- `FEC EMPLOYER`-string ↔ company name, FARA registrant name ↔ donor/contractor name, and provider name ↔ NPI where LEIE ships only placeholder IDs. Half the killed ideas died on exactly this, and half the keepers become nobody-else-can-do-this the moment it's solid: the pill-mill address rollup, the FARA-to-contract dual-hat, the foreign-agent overlap. It's real because the hard keys anchor the fuzzy ones -- **NPI** welds the entire health graph (payments↔prescribing↔exclusions↔facilities), **IMO** the vessels, **CIK/EIN/UEI** the corporate spine, and **BIOGUIDE↔ICPSR↔FEC_CAND_ID** the money-to-vote line -- so the connect/ module only has to resolve the last dirty hop against a clean backbone, not guess in the dark.