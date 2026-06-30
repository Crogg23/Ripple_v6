"""Phase 0 -- The Political Domain ("The Stat Line") source catalogue.

The anti-laziness contract: the inventory of every ethically-sourced public
dataset about US politics, registered in the existing catalog BEFORE any bulk
ingest. This module is pure data -- the loader (register_political_sources.py)
reads it and does append-only INSERTs into LIBRARY_META.REGISTRY.SOURCE_REGISTRY.

SCOPE (this session, per the handoff Phase-0 bounding rule):
  * REGISTER NOW: the verified federal catalogue + the all-50-state STRUCTURED
    feeds (LegiScan + Open States are one schema each, not 50 tasks).
  * GAPS: the state/local long tail is captured as a small set of named GAP
    bucket rows (INCLUDE='N', CATEGORY='GAPS TO FILL') so nothing is dropped;
    the per-state enumeration lives in outputs/politics_phase0_GAPS.md.

KEY-VOCAB FLAG (verified against FACET_VOCAB this session): the political join
keys -- bioguide, icpsr, fec_id, govtrack, opensecrets -- are NOT in the governed
JOIN_KEY vocab (which is EIN/CIK/NPI/UEI/IMO/FIPS/...). Per the mandate "flag,
don't force", those keys are recorded in the free-text JOIN_KEYS column + NOTES,
JOIN_KEYS_STD carries ONLY existing-vocab keys that genuinely apply, and
JOIN_KEY_TIER is set with PROVISIONAL=TRUE. Extending the vocab is a governed,
append-only follow-up recommended to Chris -- not forced here.
"""

# Provenance tag stamped on DOMAIN_SOURCE so every row this session adds is
# queryable as a set: WHERE DOMAIN_SOURCE = 'politics_domain'.
PROVENANCE = "politics_domain"

# Default field values; each source dict overrides what it needs.
_DEFAULTS = dict(
    JURISDICTION="federal",
    CATEGORY="Politics",
    SUBCATEGORY="",
    PUBLISHER="",
    DESCRIPTION="",
    UNIT_OF_OBSERVATION="",
    TEMPORAL_COVERAGE="",
    GEOGRAPHIC_SCOPE="United States",
    ACCESS_METHOD="",
    FORMAT="",
    AUTH_REQUIRED="none",
    COST="free",
    UPDATE_CADENCE="",
    VOLUME="",
    LICENSE_TERMS="",
    URL="",
    JOIN_KEYS="",                 # free-text: the REAL keys incl. political ones
    ACCOUNTABILITY_RELEVANCE="",
    EPSTEIN_RELEVANT="",
    PRIORITY_TIER="2",
    INCLUDE="Y",
    NOTES="",
    DOMAIN_PRIMARY="government_power",
    DOMAIN_SECONDARY=[],
    ENTITY_TYPES=[],
    JOIN_KEYS_STD=[],             # governed ARRAY: existing-vocab keys ONLY
    JOIN_KEY_TIER="NONE",
    JOIN_KEY_TIER_PROVISIONAL=True,
    THEMES=[],
    HAS_EVENTS=False,
    DOMAIN_SOURCE=PROVENANCE,
    DOMAIN_CONFIDENCE="high",
    NEEDS_TOPIC=False,
)

# Shorthand used in NOTES to flag the new political keys consistently.
_KEYFLAG = ("KEY-FLAG: carries political keys (bioguide/icpsr/fec_id/govtrack) "
            "not yet in FACET_VOCAB JOIN_KEY vocab -- recorded in JOIN_KEYS free-text; "
            "JOIN_KEYS_STD holds only governed-vocab keys. STEEL tier is PROVISIONAL.")

# ---------------------------------------------------------------------------
# THE CATALOGUE -- new sources to register (already-registered ones are skipped
# automatically by the append-only loader; see _ALREADY_REGISTERED for the audit).
# ---------------------------------------------------------------------------
SOURCES = [

    # === TIER 1 -- CROWN JEWELS (free, clean, bulk) -- the skeleton ===========
    dict(
        SOURCE_ID="fed_congress_legislators",
        NAME="unitedstates/congress-legislators",
        PUBLISHER="@unitedstates project (community, public domain)",
        DESCRIPTION="Current + historical members of Congress and executives (presidents/VPs): bio, party, "
                    "state, district, terms, AND the master ID crosswalk (bioguide/icpsr/fec/opensecrets/"
                    "govtrack/votesmart/lis/thomas/wikidata/ballotpedia/cspan). The keystone for every join.",
        UNIT_OF_OBSERVATION="one row = one legislator (person)",
        TEMPORAL_COVERAGE="1789-present",
        ACCESS_METHOD="bulk_download", FORMAT="yaml", AUTH_REQUIRED="none", COST="free",
        UPDATE_CADENCE="continuous (git)", VOLUME="~12k legislators",
        LICENSE_TERMS="CC0 1.0 (public domain) -- no restriction",
        URL="https://github.com/unitedstates/congress-legislators",
        JOIN_KEYS="bioguide (PK), icpsr, fec_id (1:many), govtrack, opensecrets, votesmart, lis, thomas, "
                  "wikidata, ballotpedia, cspan, house_history, maplight",
        ACCOUNTABILITY_RELEVANCE="THE identifier spine for the politician stat card -- the table that lets "
                                 "voting (Voteview/icpsr) join money (FEC/fec_id) join everything else.",
        PRIORITY_TIER="1", DOMAIN_PRIMARY="government_power", DOMAIN_SECONDARY=["elections_voting"],
        ENTITY_TYPES=["person"], JOIN_KEYS_STD=[], JOIN_KEY_TIER="STEEL", JOIN_KEY_TIER_PROVISIONAL=True,
        THEMES=["power_who_holds_it"],
        NOTES="Files: legislators-current.yaml, legislators-historical.yaml, executive.yaml. "
              "fec is a LIST (member->many candidate IDs) -> separate member_fec_id bridge. Some executives "
              "have NO bioguide (key on govtrack/fec). " + _KEYFLAG,
    ),
    dict(
        SOURCE_ID="fed_voteview_members",
        NAME="Voteview -- Congressional Member Ideology (DW-NOMINATE)",
        PUBLISHER="Voteview / UCLA (Lewis et al.)",
        DESCRIPTION="Member-by-congress ideology scores (DW-NOMINATE dim1/dim2) plus member bio, keyed by "
                    "ICPSR. The 'ideology' stat for the spine. Small member file (HSall_members.csv); the full "
                    "member-by-vote matrix is a separate, much larger file (registered as fed_voteview_rollcalls).",
        UNIT_OF_OBSERVATION="one row = one member-congress",
        TEMPORAL_COVERAGE="1st-119th Congress (1789-present)",
        ACCESS_METHOD="bulk_download", FORMAT="csv", AUTH_REQUIRED="none", COST="free",
        UPDATE_CADENCE="per-congress", VOLUME="~50k member-congress rows",
        LICENSE_TERMS="Free for research/public use (cite Lewis et al., voteview.com)",
        URL="https://voteview.com/static/data/out/members/HSall_members.csv",
        JOIN_KEYS="icpsr (PK w/ congress), bioguide_id",
        ACCOUNTABILITY_RELEVANCE="The unspinnable ideology number for the box score; joins to the crosswalk "
                                 "via icpsr<->bioguide.",
        PRIORITY_TIER="1", DOMAIN_PRIMARY="government_power", DOMAIN_SECONDARY=["elections_voting"],
        ENTITY_TYPES=["person"], JOIN_KEYS_STD=[], JOIN_KEY_TIER="STEEL", JOIN_KEY_TIER_PROVISIONAL=True,
        THEMES=["power_who_holds_it"],
        NOTES="Built into politics__member_spine this session. " + _KEYFLAG,
    ),
    dict(
        SOURCE_ID="fed_voteview_rollcalls",
        NAME="Voteview -- Roll-Call Votes (member-by-vote matrix)",
        PUBLISHER="Voteview / UCLA (Lewis et al.)",
        DESCRIPTION="Every recorded roll-call vote, member-by-member (the large matrix): HSall_votes.csv + "
                    "HSall_rollcalls.csv. The raw material for missed-votes, party-unity, vote-similarity stats.",
        UNIT_OF_OBSERVATION="one row = one (member, roll-call) cast vote",
        TEMPORAL_COVERAGE="1st-119th Congress", ACCESS_METHOD="bulk_download", FORMAT="csv",
        AUTH_REQUIRED="none", COST="free", UPDATE_CADENCE="per-congress", VOLUME="tens of millions of cast votes",
        LICENSE_TERMS="Free for research/public use (cite voteview.com)",
        URL="https://voteview.com/static/data/out/votes/HSall_votes.csv",
        JOIN_KEYS="icpsr, congress, rollnumber, chamber",
        ACCOUNTABILITY_RELEVANCE="Objective box-score votes (missed votes, party unity, head-to-head).",
        PRIORITY_TIER="1", DOMAIN_PRIMARY="government_power", ENTITY_TYPES=["event"], HAS_EVENTS=True,
        JOIN_KEYS_STD=[], JOIN_KEY_TIER="STEEL", JOIN_KEY_TIER_PROVISIONAL=True, THEMES=["power_who_holds_it"],
        # NB: live registry row keeps these Phase-0 values (append-only; not updated). In Phase 3 the VOTES
        # MATRIX (this source's URL=HSall_votes.csv) was landed into FED_VOTEVIEW_ROLLCALLS for the 118th+119th
        # -> lifecycle is now 'landed'. Roll-call metadata is the separate fed_voteview_rollcall_meta source.
        NOTES="Phase 2 (large). Deferred this session. " + _KEYFLAG,
    ),
    dict(
        SOURCE_ID="fed_voteview_rollcall_meta",
        NAME="Voteview -- Roll-Call Metadata",
        PUBLISHER="Voteview / UCLA (Lewis et al.)",
        DESCRIPTION="Per-roll-call metadata (one row per roll-call): date, session, yea/nay counts, result, "
                    "vote question, bill number. The denominator + context for the votes matrix.",
        UNIT_OF_OBSERVATION="one row = one roll-call vote",
        TEMPORAL_COVERAGE="118th + 119th Congress (this session)", ACCESS_METHOD="bulk_download", FORMAT="csv",
        AUTH_REQUIRED="none", COST="free", UPDATE_CADENCE="per-congress",
        VOLUME="~2-3k roll-calls per congress",
        LICENSE_TERMS="Free for research/public use (cite voteview.com)",
        URL="https://voteview.com/static/data/out/rollcalls/HSall_rollcalls.csv",
        JOIN_KEYS="congress, chamber, rollnumber (PK)",
        ACCOUNTABILITY_RELEVANCE="Party-unity definition + a clean missed-vote denominator come from here.",
        PRIORITY_TIER="1", DOMAIN_PRIMARY="government_power", ENTITY_TYPES=["event"], HAS_EVENTS=True,
        JOIN_KEYS_STD=[], JOIN_KEY_TIER="STRONG", JOIN_KEY_TIER_PROVISIONAL=True,
        THEMES=["power_who_holds_it"],
        NOTES="Phase 3 (NEW). Roll-call metadata (HSall_rollcalls.csv), landed for 118th+119th into "
              "FED_VOTEVIEW_ROLLCALL_META. Pairs with the votes matrix (fed_voteview_rollcalls).",
    ),

    # === TIER 1 -- LEGISLATIVE OUTPUT (bills sponsored/cosponsored/enacted) =====
    dict(
        SOURCE_ID="fed_govinfo_billstatus",
        NAME="GovInfo BILLSTATUS -- Bill Status XML (sponsor, cosponsors, actions, laws)",
        PUBLISHER="U.S. Government Publishing Office (GovInfo, official)",
        DESCRIPTION="Official bill-status records for every measure: bill type/number, congress, sponsor "
                    "(bioguideId), cosponsor list, full action history, latest action, and the <laws> element "
                    "present ONLY when the bill became law (public-law number). One XML file per bill, bulk by "
                    "congress. The clean legislative-output leg -- sponsor AND cosponsor carry bioguide, so it "
                    "joins straight to the member spine with no fuzzy matching.",
        UNIT_OF_OBSERVATION="one row = one bill (congress, bill_type, bill_number)",
        TEMPORAL_COVERAGE="113th-present (118th + 119th landed this session; 119th partial)",
        ACCESS_METHOD="bulk_download", FORMAT="xml", AUTH_REQUIRED="none", COST="free",
        UPDATE_CADENCE="daily", VOLUME="~15-20k measures per congress",
        LICENSE_TERMS="Public domain (US Gov) -- GovInfo official primary source",
        URL="https://www.govinfo.gov/bulkdata/BILLSTATUS",
        JOIN_KEYS="bioguide (sponsor + cosponsor), congress, bill_type, bill_number, law_number",
        ACCOUNTABILITY_RELEVANCE="The legislative-output box score: bills sponsored (with the type split), "
                                 "enacted + enacted_rate (law-eligible denominator), advanced-past-committee. The "
                                 "last clean objective leg -- sponsor/cosponsor bioguide joins straight to the spine.",
        PRIORITY_TIER="1", DOMAIN_PRIMARY="government_power", DOMAIN_SECONDARY=["elections_voting"],
        ENTITY_TYPES=["filing", "event"], HAS_EVENTS=True,
        JOIN_KEYS_STD=["BIOGUIDE"], JOIN_KEY_TIER="STEEL", JOIN_KEY_TIER_PROVISIONAL=False,
        THEMES=["power_who_holds_it"],
        NOTES="Phase 4 (NEW). GovInfo BILLSTATUS bulk (govinfo.gov/bulkdata/BILLSTATUS/{congress}/{billtype}). "
              "DISTINCT from fed_congress_govinfo_bills (BILLS = full bill TEXT) and fed_govinfo_bulk (umbrella "
              "repo). became_law derives from the <laws> element (public-law number), NOT a status-string match. "
              "Cosponsor list -> child extract fed_govinfo_bill_cosponsors (kept off the bill grain). "
              "Law-eligible types = HR/S/HJRES/SJRES (the enacted-rate denominator); HRES/SRES/HCONRES/SCONRES "
              "are resolutions and cannot become law. Landed 118th + 119th into FED_GOVINFO_BILLSTATUS.",
    ),
    dict(
        SOURCE_ID="fed_govinfo_bill_cosponsors",
        NAME="GovInfo BILLSTATUS -- Cosponsor Extract",
        PUBLISHER="U.S. Government Publishing Office (GovInfo, official)",
        DESCRIPTION="The cosponsor list flattened out of GovInfo BILLSTATUS: one row per (bill, cosponsor "
                    "bioguide) with the original-cosponsor flag, sponsorship date, and the withdrawn date "
                    "(present only when a cosponsorship was withdrawn). Kept as a separate table so the list "
                    "never inflates the one-row-per-bill grain.",
        UNIT_OF_OBSERVATION="one row = one (congress, bill_type, bill_number, cosponsor_bioguide)",
        TEMPORAL_COVERAGE="118th + 119th landed this session", ACCESS_METHOD="bulk_download", FORMAT="xml",
        AUTH_REQUIRED="none", COST="free", UPDATE_CADENCE="daily",
        VOLUME="~1-2M cosponsorships per congress",
        LICENSE_TERMS="Public domain (US Gov) -- GovInfo official primary source",
        URL="https://www.govinfo.gov/bulkdata/BILLSTATUS",
        JOIN_KEYS="bioguide (cosponsor), congress, bill_type, bill_number",
        ACCOUNTABILITY_RELEVANCE="cosponsored_count per member per congress -- kept SEPARATE from sponsored "
                                 "(authoring a bill != signing on to one). Withdrawn cosponsorships excluded.",
        PRIORITY_TIER="1", DOMAIN_PRIMARY="government_power", ENTITY_TYPES=["event"], HAS_EVENTS=True,
        JOIN_KEYS_STD=["BIOGUIDE"], JOIN_KEY_TIER="STEEL", JOIN_KEY_TIER_PROVISIONAL=False,
        THEMES=["power_who_holds_it"],
        NOTES="Phase 4 (NEW). Child extract of fed_govinfo_billstatus -> FED_GOVINFO_BILL_COSPONSORS. Withdrawn "
              "cosponsorships flagged (sponsorshipWithdrawnDate) and EXCLUDED from cosponsored_count to match "
              "GovTrack / the current congress.gov API behavior. is_original = isOriginalCosponsor flag.",
    ),

    # === TIER 1 -- MONEY-IN (FEC raw bulk; committee master already landed) ====
    dict(
        SOURCE_ID="fed_fec_bulk_candidates",
        NAME="FEC Bulk Data -- Candidate Master (cn.txt)",
        PUBLISHER="Federal Election Commission",
        DESCRIPTION="Every FEC-registered candidate: FEC candidate ID, name, office sought, party, state, "
                    "district, incumbent/challenger status, by cycle. The cand_id<->name<->office anchor for "
                    "the fec bridge.",
        UNIT_OF_OBSERVATION="one row = one candidate-cycle",
        TEMPORAL_COVERAGE="1979-present (per cycle)", ACCESS_METHOD="bulk_download", FORMAT="pipe-delimited txt",
        AUTH_REQUIRED="none", COST="free", UPDATE_CADENCE="weekly (cycle)", VOLUME="~5-8k candidates/cycle",
        LICENSE_TERMS="Public domain (US Gov)",
        URL="https://www.fec.gov/files/bulk-downloads/2024/cn24.zip",
        JOIN_KEYS="fec_cand_id (PK), CAND_PCC (principal committee id), state, district",
        ACCOUNTABILITY_RELEVANCE="Resolves a member's FEC candidate ID to office/cycle; the clean half of the "
                                 "money join (the org->EIN half stays fuzzy).",
        PRIORITY_TIER="1", DOMAIN_PRIMARY="money_in_politics", DOMAIN_SECONDARY=["elections_voting"],
        ENTITY_TYPES=["person", "filing"], JOIN_KEYS_STD=["ZIP"], JOIN_KEY_TIER="STEEL",
        JOIN_KEY_TIER_PROVISIONAL=True, THEMES=["follow_the_money", "power_who_holds_it"],
        NOTES="Complements fed_fec_bulk (committee master, already landed 20,938 rows). " + _KEYFLAG,
    ),
    dict(
        SOURCE_ID="fed_fec_bulk_linkages",
        NAME="FEC Bulk Data -- Candidate-Committee Linkage (ccl.txt)",
        PUBLISHER="Federal Election Commission",
        DESCRIPTION="The official link table between FEC candidate IDs and committee IDs (which committees are "
                    "authorized by / linked to which candidate). The clean cand<->cmte bridge.",
        UNIT_OF_OBSERVATION="one row = one (candidate, committee) linkage-cycle",
        TEMPORAL_COVERAGE="per cycle", ACCESS_METHOD="bulk_download", FORMAT="pipe-delimited txt",
        AUTH_REQUIRED="none", COST="free", UPDATE_CADENCE="weekly (cycle)", VOLUME="~10k linkages/cycle",
        LICENSE_TERMS="Public domain (US Gov)",
        URL="https://www.fec.gov/files/bulk-downloads/2024/ccl24.zip",
        JOIN_KEYS="fec_cand_id, fec_cmte_id, cmte_dsgn",
        ACCOUNTABILITY_RELEVANCE="Lets money flow from a politician (cand_id) to all their committees cleanly.",
        PRIORITY_TIER="1", DOMAIN_PRIMARY="money_in_politics", ENTITY_TYPES=["filing"],
        JOIN_KEYS_STD=[], JOIN_KEY_TIER="STEEL", JOIN_KEY_TIER_PROVISIONAL=True, THEMES=["follow_the_money"],
        NOTES=_KEYFLAG,
    ),
    dict(
        SOURCE_ID="fed_fec_bulk_contributions",
        NAME="FEC Bulk Data -- Individual + Committee Contributions (itcont/itpas2/itoth)",
        PUBLISHER="Federal Election Commission",
        DESCRIPTION="Itemized contributions: who gave, how much, to which committee, with contributor name + "
                    "EMPLOYER + occupation (free-text). Money-in detail. Employer/industry are DIRTY free-text, "
                    "not keys -- the org->EIN resolution is a separate fuzzy module.",
        UNIT_OF_OBSERVATION="one row = one contribution",
        TEMPORAL_COVERAGE="per cycle", ACCESS_METHOD="bulk_download", FORMAT="pipe-delimited txt",
        AUTH_REQUIRED="none", COST="free", UPDATE_CADENCE="weekly (cycle)", VOLUME="tens of millions/cycle",
        LICENSE_TERMS="Public domain (US Gov)",
        URL="https://www.fec.gov/files/bulk-downloads/2024/indiv24.zip",
        JOIN_KEYS="fec_cmte_id, contributor name+employer (FUZZY -> EIN), ZIP",
        ACCOUNTABILITY_RELEVANCE="The 'industry donates' link of the headline chain; the bridge to corporate "
                                 "money (employer free-text -> EIN, low-confidence flagged).",
        PRIORITY_TIER="2", DOMAIN_PRIMARY="money_in_politics", DOMAIN_SECONDARY=["money_finance"],
        ENTITY_TYPES=["payment"], HAS_EVENTS=True, JOIN_KEYS_STD=["ZIP", "NAME"], JOIN_KEY_TIER="PROBABILISTIC",
        JOIN_KEY_TIER_PROVISIONAL=True, THEMES=["follow_the_money"],
        NOTES="Phase 2 (large). EMPLOYER/INDUSTRY are dirty free-text, never clean join keys. " + _KEYFLAG,
    ),
    dict(
        SOURCE_ID="fed_fec_bulk_summary",
        NAME="FEC Bulk Data -- All Candidates Financial Summary (weball)",
        PUBLISHER="Federal Election Commission",
        DESCRIPTION="Per-candidate-per-cycle financial summary: total receipts (money raised), disbursements, "
                    "cash-on-hand, transfers from/to authorized committees, individual contributions, loans, "
                    "debts. The ONLY FEC bulk file carrying dollar amounts -- the source of the money-raised stat.",
        UNIT_OF_OBSERVATION="one row = one candidate-cycle financial summary",
        TEMPORAL_COVERAGE="per cycle (2024 + 2026 landed)", ACCESS_METHOD="bulk_download",
        FORMAT="pipe-delimited txt", AUTH_REQUIRED="none", COST="free", UPDATE_CADENCE="per reporting calendar",
        VOLUME="~5-8k candidates/cycle", LICENSE_TERMS="Public domain (US Gov)",
        URL="https://www.fec.gov/files/bulk-downloads/2024/weball24.zip",
        JOIN_KEYS="fec_cand_id (PK with cycle)",
        ACCOUNTABILITY_RELEVANCE="The dollars behind the politician -- money raised per cycle, computed NET of "
                                 "inter-committee transfers (the first objective box-score stat).",
        PRIORITY_TIER="1", DOMAIN_PRIMARY="money_in_politics", ENTITY_TYPES=["filing", "payment"],
        JOIN_KEYS_STD=["FEC_CAND_ID"], JOIN_KEY_TIER="STEEL", JOIN_KEY_TIER_PROVISIONAL=False,
        THEMES=["follow_the_money", "power_who_holds_it"],
        NOTES="weball all-candidates summary. Money-raised = TTL_RECEIPTS - TRANS_FROM_AUTH (net of "
              "inter-committee transfers, avoids double-count). Cycle grain: keyed (FEC_CAND_ID, CYCLE).",
    ),
    dict(
        SOURCE_ID="fed_fec_bulk_committees",
        NAME="FEC Bulk Data -- Committee Master (cm.txt), 2026 refresh",
        PUBLISHER="Federal Election Commission",
        DESCRIPTION="Every FEC-registered committee: committee ID, name, treasurer, address, designation, type, "
                    "party, filing frequency, connected org, and linked candidate ID -- by cycle. The committee "
                    "dimension the candidate->committee linkages resolve against. This is the 2026 (cm26) cycle "
                    "snapshot, landed additively beside the existing 2024 committee master (fed_fec_bulk) to "
                    "close the Phase-2 2026 linkage-resolution gap (2026 resolved only ~57% vs ~98% for 2024).",
        UNIT_OF_OBSERVATION="one row = one committee-cycle",
        TEMPORAL_COVERAGE="2026 cycle (this refresh); per cycle", ACCESS_METHOD="bulk_download",
        FORMAT="pipe-delimited txt", AUTH_REQUIRED="none", COST="free", UPDATE_CADENCE="weekly (cycle)",
        VOLUME="~17-22k committees/cycle", LICENSE_TERMS="Public domain (US Gov)",
        URL="https://www.fec.gov/files/bulk-downloads/2026/cm26.zip",
        JOIN_KEYS="fec_cmte_id (PK with cycle), fec_cand_id (linked candidate), ZIP",
        ACCOUNTABILITY_RELEVANCE="The committee dimension behind the money leg -- resolves a candidate's linked "
                                 "committees to names/types/treasurers; the cycle-aware refresh that fixes 2026 "
                                 "linkage resolution from ~57% to ~98%.",
        PRIORITY_TIER="1", DOMAIN_PRIMARY="money_in_politics", DOMAIN_SECONDARY=["elections_voting"],
        ENTITY_TYPES=["organization", "filing"],
        JOIN_KEYS_STD=["FEC_CMTE_ID", "FEC_CAND_ID"], JOIN_KEY_TIER="STEEL", JOIN_KEY_TIER_PROVISIONAL=False,
        THEMES=["follow_the_money", "power_who_holds_it"],
        NOTES="cm26 maintenance refresh 2026-06-29. Landed cycle-keyed into FED_FEC_BULK_COMMITTEES (CYCLE='2026') "
              "alongside the verified 2024 snapshot fed_fec_bulk (single-snapshot, no cycle col -- NOT overwritten). "
              "Cycle-aware union mart: LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE (CMTE_ID, CYCLE). FEC keys "
              "are governed (Phase 2 Fix A) so JOIN_KEYS_STD is non-provisional STEEL.",
    ),

    # === TIER 2 -- PERSONAL MONEY (PDF hell -- net worth + stock trades) =======
    dict(
        SOURCE_ID="fed_house_clerk_ptr",
        NAME="House Clerk -- STOCK Act Periodic Transaction Reports (PTRs)",
        PUBLISHER="U.S. House Clerk -- Financial Disclosure",
        DESCRIPTION="House members' stock trades (Periodic Transaction Reports) under the STOCK Act: ticker, "
                    "transaction type (buy/sell), amount band, dates. Raw annual ZIPs (XML index + PDFs).",
        UNIT_OF_OBSERVATION="one row = one disclosed transaction",
        TEMPORAL_COVERAGE="2014-present", ACCESS_METHOD="bulk_download", FORMAT="zip (xml index + pdf)",
        AUTH_REQUIRED="none", COST="free", UPDATE_CADENCE="rolling (45-day disclosure)", VOLUME="thousands/yr",
        LICENSE_TERMS="Public record (US Gov)",
        URL="https://disclosures-clerk.house.gov/FinancialDisclosure",
        JOIN_KEYS="member name (-> bioguide via crosswalk, name-match), ticker (-> CIK)",
        ACCOUNTABILITY_RELEVANCE="The 'member traded the stock' link -- the personal-money box-score stat; "
                                 "stock-vs-policy overlay moonshot.",
        PRIORITY_TIER="2", DOMAIN_PRIMARY="money_in_politics", DOMAIN_SECONDARY=["money_finance"],
        ENTITY_TYPES=["filing", "payment"], HAS_EVENTS=True, JOIN_KEYS_STD=[], JOIN_KEY_TIER="PROBABILISTIC",
        JOIN_KEY_TIER_PROVISIONAL=True, THEMES=["follow_the_money", "power_who_holds_it"],
        NOTES="PDF parsing step required (XML index gives the filing list; the financials are in PDFs). "
              "Member name -> bioguide is a name-match (fuzzy). Do NOT build on House Stock Watcher (dead, 403). "
              + _KEYFLAG,
    ),
    dict(
        SOURCE_ID="fed_house_financialdisclosure",
        NAME="House Clerk -- Annual Financial Disclosures (net worth)",
        PUBLISHER="U.S. House Clerk -- Financial Disclosure",
        DESCRIPTION="House members' annual financial disclosure reports: assets, liabilities, income, "
                    "positions -> net-worth-over-time. Raw annual ZIPs (XML index + PDFs).",
        UNIT_OF_OBSERVATION="one row = one annual filing (member-year)",
        TEMPORAL_COVERAGE="2008-present", ACCESS_METHOD="bulk_download", FORMAT="zip (xml index + pdf)",
        AUTH_REQUIRED="none", COST="free", UPDATE_CADENCE="annual", VOLUME="~450/yr",
        LICENSE_TERMS="Public record (US Gov)",
        URL="https://disclosures-clerk.house.gov/FinancialDisclosure",
        JOIN_KEYS="member name (-> bioguide via crosswalk)",
        ACCOUNTABILITY_RELEVANCE="Net-worth-change box-score stat (did office make them rich?).",
        PRIORITY_TIER="3", DOMAIN_PRIMARY="money_in_politics", ENTITY_TYPES=["filing"],
        JOIN_KEYS_STD=[], JOIN_KEY_TIER="PROBABILISTIC", JOIN_KEY_TIER_PROVISIONAL=True,
        THEMES=["follow_the_money"], NOTES="PDF hell. " + _KEYFLAG,
    ),
    dict(
        SOURCE_ID="fed_oge_disclosures",
        NAME="OGE -- Executive Branch Financial Disclosures (OGE Form 278e)",
        PUBLISHER="U.S. Office of Government Ethics",
        DESCRIPTION="Public financial disclosures for executive-branch officials + presidential appointees "
                    "(OGE 278e): assets, income, positions, agreements. Covers the executive 'players'.",
        UNIT_OF_OBSERVATION="one row = one official filing",
        TEMPORAL_COVERAGE="rolling", ACCESS_METHOD="api+download", FORMAT="pdf/searchable",
        AUTH_REQUIRED="none", COST="free", UPDATE_CADENCE="rolling", VOLUME="thousands",
        LICENSE_TERMS="Public record (US Gov)", URL="https://www.oge.gov/web/oge.nsf/financial-disclosure",
        JOIN_KEYS="official name (fuzzy)",
        ACCOUNTABILITY_RELEVANCE="Extends personal-money stats to the executive branch (appointees, cabinet).",
        PRIORITY_TIER="3", DOMAIN_PRIMARY="money_in_politics", DOMAIN_SECONDARY=["government_power"],
        ENTITY_TYPES=["filing", "person"], JOIN_KEYS_STD=[], JOIN_KEY_TIER="PROBABILISTIC",
        JOIN_KEY_TIER_PROVISIONAL=True, THEMES=["follow_the_money", "revolving_door"],
        NOTES="No bioguide for non-Congress executives -- name-match territory.",
    ),

    # === TIER 2/3 -- OFFICIAL ACTIVITY, RULEMAKING, SAY-VS-DO =================
    dict(
        SOURCE_ID="fed_regulations_gov",
        NAME="Regulations.gov API -- Rulemaking + Public Comments",
        PUBLISHER="GSA / eRulemaking Program",
        DESCRIPTION="Federal rulemaking dockets, proposed/final rules, and public comments. Ties members + "
                    "agencies + industries to specific regulatory actions (the 'lobbies the bill' surface).",
        UNIT_OF_OBSERVATION="one row = one document/comment",
        TEMPORAL_COVERAGE="2000s-present", ACCESS_METHOD="api", FORMAT="json",
        AUTH_REQUIRED="api_key", COST="free (data.gov key)", UPDATE_CADENCE="daily", VOLUME="millions",
        LICENSE_TERMS="Public domain (US Gov)", URL="https://api.regulations.gov/",
        JOIN_KEYS="docket_id, agency, RIN",
        ACCOUNTABILITY_RELEVANCE="Rulemaking + comment trail for say-vs-do and industry-influence threads.",
        PRIORITY_TIER="3", DOMAIN_PRIMARY="government_power", DOMAIN_SECONDARY=["money_in_politics"],
        ENTITY_TYPES=["filing", "case"], HAS_EVENTS=True, JOIN_KEYS_STD=["DOCKET"], JOIN_KEY_TIER="STRONG",
        JOIN_KEY_TIER_PROVISIONAL=True, THEMES=["power_who_holds_it"],
        NOTES="DOCKET is a governed vocab key (STRONG). Needs a data.gov API key.",
    ),
    dict(
        SOURCE_ID="fed_house_disbursements",
        NAME="House -- Statement of Disbursements",
        PUBLISHER="U.S. House Chief Administrative Officer",
        DESCRIPTION="Quarterly office/staff spending for every House member office (salaries, vendors, travel). "
                    "Office-operations box-score + staff networks.",
        UNIT_OF_OBSERVATION="one row = one disbursement line",
        TEMPORAL_COVERAGE="2010-present", ACCESS_METHOD="bulk_download", FORMAT="csv",
        AUTH_REQUIRED="none", COST="free", UPDATE_CADENCE="quarterly", VOLUME="millions of lines",
        LICENSE_TERMS="Public record (US Gov)", URL="https://www.house.gov/the-house-explained/open-government/statement-of-disbursements",
        JOIN_KEYS="member office name (-> bioguide), vendor name",
        ACCOUNTABILITY_RELEVANCE="Office-spending + staff/vendor network stats (revolving-door feeders).",
        PRIORITY_TIER="3", DOMAIN_PRIMARY="spending_budget", DOMAIN_SECONDARY=["government_power"],
        ENTITY_TYPES=["payment"], HAS_EVENTS=True, JOIN_KEYS_STD=[], JOIN_KEY_TIER="PROBABILISTIC",
        JOIN_KEY_TIER_PROVISIONAL=True, THEMES=["follow_the_money"], NOTES=_KEYFLAG,
    ),

    # === TIER 3 -- ALL-50-STATE STRUCTURED FEEDS (one schema each) ============
    dict(
        SOURCE_ID="st_legiscan",
        NAME="LegiScan -- 50 States + Congress (bills, votes, sponsors)",
        PUBLISHER="LegiScan",
        DESCRIPTION="Unified schema across all 50 state legislatures + Congress: bills, roll-call votes, "
                    "sponsors, legislators, sessions. ONE feed covering every state (not 50 tasks).",
        JURISDICTION="state",
        UNIT_OF_OBSERVATION="one row = one bill / vote / legislator (per dataset)",
        TEMPORAL_COVERAGE="2009-present", ACCESS_METHOD="api+bulk", FORMAT="json/csv",
        AUTH_REQUIRED="api_key", COST="free (registration)", UPDATE_CADENCE="daily",
        VOLUME="millions of bills/votes across states",
        LICENSE_TERMS="Free tier for non-commercial; verify commercial-redistribution terms before publishing",
        URL="https://legiscan.com/legiscan",
        JOIN_KEYS="legiscan people_id, bill_id, state, district",
        ACCOUNTABILITY_RELEVANCE="Extends the stat line below Congress to all 50 state legislatures (no unified "
                                 "national person key -> name-match territory).",
        PRIORITY_TIER="3", DOMAIN_PRIMARY="government_power", DOMAIN_SECONDARY=["elections_voting"],
        ENTITY_TYPES=["person", "filing", "event"], HAS_EVENTS=True, JOIN_KEYS_STD=[],
        JOIN_KEY_TIER="PROBABILISTIC", JOIN_KEY_TIER_PROVISIONAL=True, THEMES=["power_who_holds_it"],
        NOTES="50-state STRUCTURED feed -- one schema, all states. Needs free API key. State persons do NOT "
              "key to bioguide (federal-only). Verify commercial terms before any paid republishing. " + _KEYFLAG,
    ),
    dict(
        SOURCE_ID="st_openstates",
        NAME="Open States -- 50 States + DC + PR (legislators, bills, votes)",
        PUBLISHER="Plural / Open States (open-source)",
        DESCRIPTION="Open data on state legislators, bills, votes, and committees across 50 states + DC + PR, "
                    "with stable Open States person IDs. API + bulk CSV/JSON.",
        JURISDICTION="state",
        UNIT_OF_OBSERVATION="one row = one legislator / bill / vote (per dataset)",
        TEMPORAL_COVERAGE="2011-present", ACCESS_METHOD="api+bulk", FORMAT="json/csv",
        AUTH_REQUIRED="api_key", COST="free (registration)", UPDATE_CADENCE="daily",
        VOLUME="all state legislatures",
        LICENSE_TERMS="CC0 / open (verify per-dataset)", URL="https://openstates.org/data/",
        JOIN_KEYS="openstates person ocd-id, jurisdiction (state), district",
        ACCOUNTABILITY_RELEVANCE="State-legislature roster + activity; the cleanest open state-person IDs we "
                                 "have (still not bioguide).",
        PRIORITY_TIER="3", DOMAIN_PRIMARY="government_power", DOMAIN_SECONDARY=["elections_voting"],
        ENTITY_TYPES=["person", "filing", "event"], HAS_EVENTS=True, JOIN_KEYS_STD=[],
        JOIN_KEY_TIER="PROBABILISTIC", JOIN_KEY_TIER_PROVISIONAL=True, THEMES=["power_who_holds_it"],
        NOTES="50-state + DC + PR STRUCTURED feed -- one schema. Bulk CSV/JSON + API (key). " + _KEYFLAG,
    ),

    # === ALSO-REGISTER (verify access) -- candidates, ratings, video =========
    dict(
        SOURCE_ID="xc_votesmart",
        NAME="Vote Smart -- Positions, Ratings, Bios",
        PUBLISHER="Vote Smart (nonpartisan)",
        DESCRIPTION="Candidate/official positions, interest-group ratings, voting records, biographical and "
                    "'political courage' data. Keys via votesmart id in the crosswalk.",
        JURISDICTION="cross-cutting",
        UNIT_OF_OBSERVATION="one row = one rating / position / official",
        ACCESS_METHOD="api", FORMAT="json/xml", AUTH_REQUIRED="api_key", COST="free (was; verify access)",
        UPDATE_CADENCE="periodic", VOLUME="all federal + state officials",
        LICENSE_TERMS="Verify ToS; nonprofit-restricted in places",
        URL="https://votesmart.org/share/api",
        JOIN_KEYS="votesmart id (in crosswalk)",
        ACCOUNTABILITY_RELEVANCE="Interest-group ratings = ready-made judgment stats; positions feed say-vs-do.",
        PRIORITY_TIER="3", DOMAIN_PRIMARY="elections_voting", DOMAIN_SECONDARY=["government_power"],
        ENTITY_TYPES=["person"], JOIN_KEYS_STD=[], JOIN_KEY_TIER="PROBABILISTIC",
        JOIN_KEY_TIER_PROVISIONAL=True, THEMES=["power_who_holds_it"],
        NOTES="ACCESS-FLAG: public API access has been curtailed/deprecated -- verify before building. " + _KEYFLAG,
    ),
    dict(
        SOURCE_ID="xc_ballotpedia",
        NAME="Ballotpedia -- Candidates, Officeholders, Elections (all levels)",
        PUBLISHER="Ballotpedia (Lucy Burns Institute)",
        DESCRIPTION="Encyclopedic coverage of candidates and officeholders at federal/state/LOCAL levels + "
                    "elections, incl. non-incumbent candidates and local offices the federal feeds miss.",
        JURISDICTION="cross-cutting",
        UNIT_OF_OBSERVATION="one row = one candidate / officeholder / race",
        ACCESS_METHOD="api/scrape", FORMAT="json/html", AUTH_REQUIRED="api_key (paid tiers)", COST="freemium",
        UPDATE_CADENCE="continuous", VOLUME="all levels incl. local",
        LICENSE_TERMS="ToS-restricted -- API/license required for bulk; NO scraping behind paywall",
        URL="https://ballotpedia.org/",
        JOIN_KEYS="ballotpedia id (in crosswalk), name+state+office (fuzzy)",
        ACCOUNTABILITY_RELEVANCE="The widest candidate + LOCAL coverage; the only practical bridge to local "
                                 "officials (mayors, councils, school boards).",
        PRIORITY_TIER="3", DOMAIN_PRIMARY="elections_voting", DOMAIN_SECONDARY=["government_power"],
        ENTITY_TYPES=["person", "event"], JOIN_KEYS_STD=[], JOIN_KEY_TIER="PROBABILISTIC",
        JOIN_KEY_TIER_PROVISIONAL=True, THEMES=["power_who_holds_it"],
        NOTES="ACCESS-FLAG: respect ToS -- official API/license only, no paywall scraping. " + _KEYFLAG,
    ),
    dict(
        SOURCE_ID="xc_cspan_congress",
        NAME="C-SPAN Congressional Video / Transcripts",
        PUBLISHER="C-SPAN",
        DESCRIPTION="Floor + hearing video and transcripts indexed by member (cspan id in the crosswalk). The "
                    "raw material for the say-vs-do (rhetoric vs votes) NLP moonshot.",
        JURISDICTION="cross-cutting",
        UNIT_OF_OBSERVATION="one row = one video/appearance/transcript segment",
        ACCESS_METHOD="api/scrape", FORMAT="json/text/video", AUTH_REQUIRED="verify", COST="verify",
        UPDATE_CADENCE="continuous", VOLUME="decades of floor video",
        LICENSE_TERMS="C-SPAN license terms -- verify reuse rights before publishing",
        URL="https://www.c-span.org/",
        JOIN_KEYS="cspan id (in crosswalk)",
        ACCOUNTABILITY_RELEVANCE="Rhetoric corpus for say-vs-do contradiction detection.",
        PRIORITY_TIER="3", DOMAIN_PRIMARY="government_power", ENTITY_TYPES=["event", "person"], HAS_EVENTS=True,
        JOIN_KEYS_STD=[], JOIN_KEY_TIER="PROBABILISTIC", JOIN_KEY_TIER_PROVISIONAL=True,
        THEMES=["power_who_holds_it"],
        NOTES="ACCESS-FLAG: verify license/reuse terms; rhetoric for the say-vs-do moonshot. " + _KEYFLAG,
    ),
]

# ---------------------------------------------------------------------------
# GAP BUCKETS -- the state/local long tail. Registered INCLUDE='N' + CATEGORY
# 'GAPS TO FILL' so nothing is dropped, without polluting the active-source
# count. Per-state enumeration lives in outputs/politics_phase0_GAPS.md.
# ---------------------------------------------------------------------------
GAP_BUCKETS = [
    dict(
        SOURCE_ID="gap_state_campaign_finance",
        NAME="GAP -- State Campaign-Finance Agencies (50-state long tail)",
        PUBLISHER="(various state agencies)", JURISDICTION="state",
        CATEGORY="GAPS TO FILL", SUBCATEGORY="state campaign finance",
        DESCRIPTION="Each state's own campaign-finance disclosure portal (e.g. CA Cal-Access/DISCLOSE, NY BOE, "
                    "TX Ethics, FL DOE). Aggregator: NIMSP/FollowTheMoney. To be researched per-state later.",
        ACCESS_METHOD="varies", FORMAT="varies", COST="free", INCLUDE="N", PRIORITY_TIER="3",
        DOMAIN_PRIMARY="money_in_politics", ENTITY_TYPES=["payment", "person"],
        ACCOUNTABILITY_RELEVANCE="State-level money-in; the long tail of donor->state-official threads.",
        DOMAIN_CONFIDENCE="low", NEEDS_TOPIC=True,
        NOTES="GAP BUCKET -- see outputs/politics_phase0_GAPS.md for the per-state enumeration. Not ingested.",
    ),
    dict(
        SOURCE_ID="gap_state_lobbying_disclosure",
        NAME="GAP -- State Lobbying Disclosure Registries (50-state long tail)",
        PUBLISHER="(various state agencies)", JURISDICTION="state",
        CATEGORY="GAPS TO FILL", SUBCATEGORY="state lobbying",
        DESCRIPTION="State lobbyist registrations + activity reports (one portal per state).",
        ACCESS_METHOD="varies", FORMAT="varies", COST="free", INCLUDE="N", PRIORITY_TIER="3",
        DOMAIN_PRIMARY="money_in_politics", ENTITY_TYPES=["filing", "organization"],
        ACCOUNTABILITY_RELEVANCE="State-level influence + revolving-door.",
        DOMAIN_CONFIDENCE="low", NEEDS_TOPIC=True,
        NOTES="GAP BUCKET -- see outputs/politics_phase0_GAPS.md. Not ingested.",
    ),
    dict(
        SOURCE_ID="gap_state_financial_disclosure",
        NAME="GAP -- State Legislator Personal Financial Disclosures",
        PUBLISHER="(various state ethics agencies)", JURISDICTION="state",
        CATEGORY="GAPS TO FILL", SUBCATEGORY="state financial disclosure",
        DESCRIPTION="State legislators' personal financial / conflict-of-interest disclosures (per-state).",
        ACCESS_METHOD="varies", FORMAT="varies", COST="free", INCLUDE="N", PRIORITY_TIER="3",
        DOMAIN_PRIMARY="money_in_politics", ENTITY_TYPES=["filing", "person"],
        ACCOUNTABILITY_RELEVANCE="State-level net worth + conflicts.",
        DOMAIN_CONFIDENCE="low", NEEDS_TOPIC=True,
        NOTES="GAP BUCKET -- see outputs/politics_phase0_GAPS.md. Not ingested.",
    ),
    dict(
        SOURCE_ID="gap_state_executive_judiciary",
        NAME="GAP -- Governors, State Executives, Elected Judges",
        PUBLISHER="(various states)", JURISDICTION="state",
        CATEGORY="GAPS TO FILL", SUBCATEGORY="state executive + judiciary",
        DESCRIPTION="Governors, statewide elected executives, and elected state judges -- rosters, terms, "
                    "actions. No unified national key.",
        ACCESS_METHOD="varies", FORMAT="varies", COST="free", INCLUDE="N", PRIORITY_TIER="3",
        DOMAIN_PRIMARY="government_power", ENTITY_TYPES=["person"],
        ACCOUNTABILITY_RELEVANCE="State executive + judicial 'players' for the wider stat universe.",
        DOMAIN_CONFIDENCE="low", NEEDS_TOPIC=True,
        NOTES="GAP BUCKET -- see outputs/politics_phase0_GAPS.md. Defer (SCOTUS/judges = separate keying). Not ingested.",
    ),
    dict(
        SOURCE_ID="gap_local_officials",
        NAME="GAP -- Local Officials (mayors, city councils, county, school boards)",
        PUBLISHER="(thousands of local jurisdictions)", JURISDICTION="local",
        CATEGORY="GAPS TO FILL", SUBCATEGORY="local officials",
        DESCRIPTION="Mayors, city councils, county officials, school boards -- the local long tail. No unified "
                    "key; Ballotpedia is the widest practical bridge.",
        ACCESS_METHOD="varies", FORMAT="varies", COST="free/varies", INCLUDE="N", PRIORITY_TIER="3",
        DOMAIN_PRIMARY="government_power", ENTITY_TYPES=["person"],
        ACCOUNTABILITY_RELEVANCE="Local-level players; pure name-match territory (defer).",
        DOMAIN_CONFIDENCE="low", NEEDS_TOPIC=True,
        NOTES="GAP BUCKET -- see outputs/politics_phase0_GAPS.md. Not ingested.",
    ),
    dict(
        SOURCE_ID="gap_nonincumbent_candidates",
        NAME="GAP -- Non-Incumbent Candidates (state + local races)",
        PUBLISHER="(states + aggregators)", JURISDICTION="state",
        CATEGORY="GAPS TO FILL", SUBCATEGORY="candidates",
        DESCRIPTION="Candidates who are not incumbents and not in FEC (state/local races) -- to complete the "
                    "'candidates, not just incumbents' scope.",
        ACCESS_METHOD="varies", FORMAT="varies", COST="free/varies", INCLUDE="N", PRIORITY_TIER="3",
        DOMAIN_PRIMARY="elections_voting", ENTITY_TYPES=["person", "event"],
        ACCOUNTABILITY_RELEVANCE="Candidate-level coverage below the federal FEC line.",
        DOMAIN_CONFIDENCE="low", NEEDS_TOPIC=True,
        NOTES="GAP BUCKET -- see outputs/politics_phase0_GAPS.md. Not ingested.",
    ),
]

# Already in the registry (verified live this session) -> the loader SKIPS these
# (append-only: never overwrites a row another session may own). Kept for the audit.
_ALREADY_REGISTERED = [
    "fed_fec_bulk", "fed_fec_api", "fed_congress_api", "fed_senate_lda", "fed_senate_lda_bulk",
    "fed_house_lda", "fed_fara", "fed_usaspending", "fed_usaspending_contracts",
    "fed_usaspending_toptier_agencies", "xc_govtrack", "xc_unitedstates_congress", "xc_opensecrets_bulk",
    "fed_senate_financialdisclosure", "fed_congress_govinfo_bills", "fed_congress_govinfo_crec",
    "fed_crs_reports", "fed_fcc_political_files",
]


def all_rows():
    """Every catalogue row (sources + gap buckets) with defaults applied."""
    out = []
    for src in SOURCES + GAP_BUCKETS:
        row = dict(_DEFAULTS)
        row.update(src)
        out.append(row)
    return out


# Column order for the registry INSERT (must match SOURCE_REGISTRY; _LOADED_AT
# is omitted -- it has a CURRENT_TIMESTAMP() default).
INSERT_COLUMNS = [
    "SOURCE_ID", "JURISDICTION", "CATEGORY", "SUBCATEGORY", "PUBLISHER", "NAME", "DESCRIPTION",
    "UNIT_OF_OBSERVATION", "TEMPORAL_COVERAGE", "GEOGRAPHIC_SCOPE", "ACCESS_METHOD", "FORMAT",
    "AUTH_REQUIRED", "COST", "UPDATE_CADENCE", "VOLUME", "LICENSE_TERMS", "URL", "JOIN_KEYS",
    "ACCOUNTABILITY_RELEVANCE", "EPSTEIN_RELEVANT", "PRIORITY_TIER", "INCLUDE", "NOTES",
    "DOMAIN_PRIMARY", "DOMAIN_SECONDARY", "ENTITY_TYPES", "JOIN_KEYS_STD", "JOIN_KEY_TIER",
    "JOIN_KEY_TIER_PROVISIONAL", "THEMES", "HAS_EVENTS", "DOMAIN_SOURCE", "DOMAIN_CONFIDENCE", "NEEDS_TOPIC",
]
ARRAY_COLUMNS = {"DOMAIN_SECONDARY", "ENTITY_TYPES", "JOIN_KEYS_STD", "THEMES"}
