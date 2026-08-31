# Political Domain — Phase 0 "GAPS TO FILL" (state + local long tail)

Last updated: 2026-06-29 · branch `politics-domain`

The anti-laziness contract: nothing public about US political power is silently
dropped. The **federal catalogue + all-50-state structured feeds** are registered
in `SOURCE_REGISTRY` now (DOMAIN_SOURCE='politics_domain'). The **state/local long
tail below is logged but NOT yet researched per-source** — captured as 6 GAP
bucket rows (`gap_*`, INCLUDE='N', CATEGORY='GAPS TO FILL') so it's queryable and
nothing is lost. Each bucket below is a *later session*, not this one.

> Sequencing rule (from the handoff): build from the CLEAN keys outward. State/local
> have **no unified national person key** — they are name-match territory and are
> deliberately deferred until the federal bioguide spine is solid.

---

## GAP 1 — State campaign-finance agencies → `gap_state_campaign_finance`
One disclosure portal per state. The aggregator **NIMSP / FollowTheMoney
(transparencyusa, OpenSecrets-adjacent)** covers most, but primary-source is
on-ethos. Per-state primary portals to scout:

- **CA** — Cal-Access / DISCLOSE (CA SoS) · **NY** — NYSBOE Campaign Finance
- **TX** — Texas Ethics Commission · **FL** — FL Division of Elections
- **IL** — IL State Board of Elections · **PA, OH, MI, GA, NC, WA, MA, VA, NJ, AZ,
  CO, MN, WI, MD, MO, TN, IN, …** — each has a state board/ethics portal
- Remaining states (AK, AL, AR, CT, DE, HI, IA, ID, KS, KY, LA, ME, MS, MT, ND, NE,
  NH, NM, NV, OK, OR, RI, SC, SD, UT, VT, WV, WY) — same pattern, one portal each.
- Already in the Library: `st_ca_cf` (CA campaign finance, scouted).

## GAP 2 — State lobbying disclosure registries → `gap_state_lobbying_disclosure`
Lobbyist registration + activity reports, one portal per state (often the same
Secretary of State / Ethics Commission that hosts campaign finance). Feeds
state-level revolving-door + influence threads.

## GAP 3 — State legislator personal financial disclosures → `gap_state_financial_disclosure`
Per-state ethics-commission personal financial / conflict-of-interest filings for
state legislators. Coverage and format vary wildly (many PDF-only). Net-worth +
conflicts at the state level.

## GAP 4 — Governors, state executives, elected judges → `gap_state_executive_judiciary`
Statewide elected executives (governor, AG, SoS, treasurer, …) and **elected state
judges**. NOTE: SCOTUS / federal judges are a *separate keying problem* (no bioguide)
already deferred in the federal plan; elected state judges compound it.

## GAP 5 — Local officials → `gap_local_officials`
Mayors, city councils, county officials, school boards across thousands of
jurisdictions. **No unified key.** Ballotpedia (`xc_ballotpedia`, registered) is the
widest practical bridge; municipal open-data portals (already heavily harvested into
the Library as `portal_*`) carry some local spending/contracts.

## GAP 6 — Non-incumbent candidates (state + local) → `gap_nonincumbent_candidates`
Candidates who never reach FEC (state/local races) — to honor "candidates, not just
incumbents" below the federal line. Sources: state election boards + Ballotpedia +
Open States/LegiScan candidate tables.

---

## Federal items intentionally registered now (NOT gaps)
These are real, structured, clean-keyed — registered this session:
`fed_congress_legislators`, `fed_voteview_members`, `fed_voteview_rollcalls`,
`fed_fec_bulk_candidates`, `fed_fec_bulk_linkages`, `fed_fec_bulk_contributions`,
`fed_house_clerk_ptr`, `fed_house_financialdisclosure`*, `fed_oge_disclosures`,
`fed_regulations_gov`*, `fed_house_disbursements`, `st_legiscan`, `st_openstates`,
`xc_votesmart`*, `xc_ballotpedia`*, `xc_cspan_congress`.
*(\* = already in the registry from prior scouting; left untouched, append-only.)*

## Already-registered political sources reused (not re-scouted)
`fed_fec_bulk` (LANDED 20,938), `fed_usaspending_contracts` (LANDED),
`fed_usaspending_toptier_agencies` (LANDED), `fed_fec_api`, `fed_congress_api`,
`fed_senate_lda(+_bulk)`, `fed_house_lda`, `fed_fara`, `xc_govtrack`,
`xc_unitedstates_congress`, `xc_opensecrets_bulk`, `fed_senate_financialdisclosure`,
`fed_congress_govinfo_bills/crec`, `fed_crs_reports`, `fed_fcc_political_files`.

## License landmines carried in the registry NOTES
- **OpenSecrets** (`xc_opensecrets_bulk`) — CC BY-NC-SA; Revolving Door fully
  excluded. Do NOT build publishable output on it — pull the same facts from FEC /
  Senate LDA / House+Senate+OGE disclosures / USAspending (no such restriction).
- **LegiScan / Open States / Vote Smart / Ballotpedia / C-SPAN** — verify
  commercial-redistribution terms before any paid republishing (flagged per-row).
