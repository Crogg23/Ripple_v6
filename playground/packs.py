"""Question packs — the Playground's front door. DATA ONLY, no logic.

A pack answers: "for this plain-English question, WHERE do I look?" — the
exact tables, the columns that matter, how they join, and the traps. Packs
NEVER contain SQL (Chris writes the SQL; the dictionary points). Packs never
contain row counts either — counts are pulled live at render, so prose can't
rot (the numbers-only policy, enforced structurally).

Trap keys resolve against honesty/traps.py TRAPS first, then PACK_TRAPS here.
Validated offline by tests/test_playground_offline.py against the committed
inventory snapshot.
"""
from __future__ import annotations

# Politics data traps not (yet) in the honesty registry seeds.
PACK_TRAPS: dict[str, str] = {
    "trap_fec_net_of_transfers": (
        "Money raised must be net of inter-committee transfers: "
        "TTL_RECEIPTS minus TRANS_FROM_AUTH. The naive receipts sum "
        "double-counts money the candidate moved between their own "
        "committees."),
    "trap_itcont_naive_sum": (
        "A naive SUM over the raw individual-contributions firehose gave a "
        "plausible-but-wrong answer three separate times before the smoke "
        "referee existed. Reconcile any donor total against "
        "POLITICS__MEMBER_INDIV_DONATIONS before believing it."),
    "trap_who_won_name_join": (
        "Election-returns data carries no FEC ID and no vote-archive ID - "
        "the join to a member is name plus state (plus district), which is "
        "lead-grade matching, never a fact."),
    "trap_lobbying_fuzzy_name": (
        "Lobbying filings name their targets and clients as free text. "
        "Filing-to-member and client-to-company joins are fuzzy name "
        "chains, not hard-ID joins - treat every match as a lead to "
        "verify."),
    "trap_stock_watcher_provenance": (
        "Senate Stock Watcher is a volunteer-maintained re-parse of the "
        "Senate's official filings, with no stated license - and its "
        "coverage ENDS in late 2020 (verified at load, 2026-08-01): this is "
        "historical data, never current activity. JOURNALISM USE ONLY - "
        "federal law (5 USC 13107(c)(1)) forbids commercial, credit, or "
        "solicitation use of financial disclosure data. Amounts are "
        "disclosure BANDS, never exact figures - do not average band "
        "edges. The member link is a name match (MATCH_METHOD), not a "
        "hard ID."),
    "trap_bills_sponsored_headline": (
        "A raw count of bills sponsored is spam-able (rename a post "
        "office, sponsor a resolution). Always pair sponsorship counts "
        "with how far bills advanced, and split substantive bills from "
        "ceremonial resolutions."),
    "trap_cycle_linkage_2026": (
        "FEC candidate-committee linkage for the 2026 cycle resolves at "
        "roughly half the rate of 2024 - current-cycle money totals are a "
        "FLOOR, not a complete picture."),
}

_P = "LIBRARY_MARTS.POLITICS."
_L = "LIBRARY_RAW.LANDING."

# Tables whose LOADER ships in the same commit as their pack but which have
# not been landed yet — the offline inventory test accepts these, and the
# app degrades gracefully (row count unavailable) until the loader runs.
# Remove entries after landing + re-snapshotting the inventory fixture.
PENDING_FQNS: set[str] = set()  # trades landed 2026-08-01; nothing pending

PACKS: list[dict] = [

    {
        "id": "member_money",
        "question": "Who pays for this politician's campaign?",
        "why": ("Money raised is the first accountability number - and the "
                "naive version of it is wrong."),
        "tables": [
            {
                "fqn": _P + "POLITICS__MEMBER_MONEY_RAISED",
                "role": "the answer table - one row per sitting member per cycle, already net of transfers",
                "key_columns": ["BIOGUIDE", "CYCLE"],
                "joins": [{"to": _P + "POLITICS__MEMBER_SPINE",
                           "on": "BIOGUIDE = BIOGUIDE", "tier": "STEEL",
                           "gotcha": ""}],
                "traps": ["trap_fec_net_of_transfers"],
            },
            {
                "fqn": _P + "POLITICS__FEC_CANDIDATE_SUMMARY",
                "role": "the raw FEC financial summary per candidate committee - the ingredients behind the answer table",
                "key_columns": ["CAND_ID"],
                "joins": [{"to": _P + "POLITICS__MEMBER_FEC_ID",
                           "on": "CAND_ID = FEC_CAND_ID", "tier": "STEEL",
                           "gotcha": "one member can hold several FEC candidate IDs across cycles - the bridge is one-to-many on purpose"}],
                "traps": ["trap_fec_net_of_transfers", "trap_cycle_linkage_2026"],
            },
            {
                "fqn": _P + "POLITICS__MEMBER_FEC_ID",
                "role": "the bridge: member ID to FEC candidate ID",
                "key_columns": ["BIOGUIDE", "FEC_CAND_ID"],
                "joins": [{"to": _P + "POLITICS__MEMBER_SPINE",
                           "on": "BIOGUIDE = BIOGUIDE", "tier": "STEEL",
                           "gotcha": ""}],
                "traps": [],
            },
            {
                "fqn": _P + "POLITICS__MEMBER_SPINE",
                "role": "who's who: one row per member with name, party, state, chamber",
                "key_columns": ["BIOGUIDE"],
                "joins": [],
                "traps": [],
            },
        ],
        "observations": [
            "Net money = TTL_RECEIPTS minus TRANS_FROM_AUTH - the naive sum is wrong.",
            "Compare a member against the median for their chamber and cycle before calling a number big.",
            "Current-cycle totals are floors, not final - see the linkage trap.",
        ],
    },

    {
        "id": "donors_to_votes",
        "question": "Did the votes follow the donors?",
        "why": ("The core accountability question: money on one side, "
                "roll-call votes on the other, one person in the middle."),
        "tables": [
            {
                "fqn": _P + "POLITICS__MEMBER_INDIV_DONATIONS",
                "role": "itemized individual donations rolled up per member - the SAFE money side (already reconciled)",
                "key_columns": ["BIOGUIDE"],
                "joins": [{"to": _P + "POLITICS__MEMBER_SPINE",
                           "on": "BIOGUIDE = BIOGUIDE", "tier": "STEEL",
                           "gotcha": ""}],
                "traps": ["trap_itcont_naive_sum"],
            },
            {
                "fqn": _L + "FED_FEC_INDIV_CONTRIBUTIONS",
                "role": "the raw firehose: every itemized individual contribution - donor name, employer, amount, date",
                "key_columns": ["CMTE_ID"],
                "joins": [{"to": _P + "POLITICS__FEC_CAND_CMTE_LINK",
                           "on": "CMTE_ID = CMTE_ID", "tier": "STEEL",
                           "gotcha": "contributions go to COMMITTEES; walk committee to candidate to member"}],
                "traps": ["trap_itcont_naive_sum"],
            },
            {
                "fqn": _P + "POLITICS__FEC_CAND_CMTE_LINK",
                "role": "the committee-to-candidate bridge",
                "key_columns": ["CAND_ID", "CMTE_ID"],
                "joins": [{"to": _P + "POLITICS__MEMBER_FEC_ID",
                           "on": "CAND_ID = FEC_CAND_ID", "tier": "STEEL",
                           "gotcha": ""}],
                "traps": [],
            },
            {
                "fqn": _P + "POLITICS__MEMBER_FEC_ID",
                "role": "the bridge: member ID to FEC candidate ID",
                "key_columns": ["BIOGUIDE", "FEC_CAND_ID"],
                "joins": [{"to": _P + "POLITICS__MEMBER_SPINE",
                           "on": "BIOGUIDE = BIOGUIDE", "tier": "STEEL",
                           "gotcha": ""}],
                "traps": [],
            },
            {
                "fqn": _P + "POLITICS__VOTEVIEW_VOTES",
                "role": "every recorded roll-call vote by every member",
                "key_columns": ["ICPSR", "CONGRESS", "ROLLNUMBER"],
                "joins": [{"to": _P + "POLITICS__MEMBER_SPINE",
                           "on": "ICPSR = ICPSR", "tier": "STEEL",
                           "gotcha": "votes are keyed on the vote-archive ID (ICPSR), not BIOGUIDE - the spine carries both, cross over there"}],
                "traps": [],
            },
            {
                "fqn": _P + "POLITICS__MEMBER_SPINE",
                "role": "the crosswalk holding BIOGUIDE and ICPSR together",
                "key_columns": ["BIOGUIDE", "ICPSR"],
                "joins": [],
                "traps": [],
            },
        ],
        "observations": [
            "Donor employer is free text typed by the donor - bucket it before trusting it.",
            "Timing beats totals: donations clustered before a specific vote say more than a career sum.",
            "Start from the rolled-up donations table; open the firehose only when you need donor-level detail.",
        ],
    },

    {
        "id": "lobbying_committees",
        "question": "Who lobbies the committees, and who sits on them?",
        "why": ("Lobbying money aims at committees; committee seats decide "
                "what gets a hearing."),
        "tables": [
            {
                "fqn": _L + "FED_SENATE_LDA_FILINGS",
                "role": "federal lobbying filings: who paid whom to lobby which agencies and issues",
                "key_columns": ["REGISTRANT_ID", "CLIENT_ID"],
                "joins": [],
                "traps": ["trap_lobbying_fuzzy_name"],
            },
            {
                "fqn": _L + "FED_CONGRESS_COMMITTEE_MEMBERSHIP",
                "role": "who sits on which committee, by member ID",
                "key_columns": ["BIOGUIDE"],
                "joins": [{"to": _P + "POLITICS__MEMBER_SPINE",
                           "on": "BIOGUIDE = BIOGUIDE", "tier": "STEEL",
                           "gotcha": ""}],
                "traps": [],
            },
            {
                "fqn": _P + "POLITICS__MEMBER_SPINE",
                "role": "who's who",
                "key_columns": ["BIOGUIDE"],
                "joins": [],
                "traps": [],
            },
        ],
        "observations": [
            "There is NO hard-ID join from a lobbying filing to a member - any such link is a name match and stays a lead.",
            "The honest chart is issue-level or agency-level: lobbying volume by topic against committee activity on that topic.",
        ],
    },

    {
        "id": "senate_stock_trades",
        "question": "What stocks do senators trade, and when?",
        "why": ("Trades near committee work or market-moving votes are the "
                "canonical congressional accountability story."),
        "tables": [
            {
                "fqn": _L + "FED_SENATE_STOCK_WATCHER",
                "role": "every disclosed Senate stock transaction, as filed: who (by name), what, when, in what amount band",
                "key_columns": ["SENATOR", "TICKER", "TRANSACTION_DATE",
                                "AMOUNT", "PTR_LINK"],
                "joins": [{"to": _P + "POLITICS__SENATE_TRADES",
                           "on": "same rows, plus the member match",
                           "tier": "STEEL",
                           "gotcha": "prefer the mart - it carries BIOGUIDE via a documented name match with MATCH_METHOD recorded per row"}],
                "traps": ["trap_stock_watcher_provenance"],
            },
            {
                "fqn": _P + "POLITICS__SENATE_TRADES",
                "role": "the trades with the member link resolved: BIOGUIDE by surname+chamber+term-span name match, unmatched rows kept and flagged",
                "key_columns": ["BIOGUIDE", "TICKER", "TRANSACTION_DATE",
                                "AMOUNT_BAND", "MATCH_METHOD"],
                "joins": [{"to": _P + "POLITICS__MEMBER_SPINE",
                           "on": "BIOGUIDE = BIOGUIDE",
                           "tier": "PROBABILISTIC",
                           "gotcha": "the source names senators as free text - the BIOGUIDE here comes from a name match (MATCH_METHOD says how); treat member-level claims as leads to verify against the PTR_LINK filing"}],
                "traps": ["trap_stock_watcher_provenance"],
            },
            {
                "fqn": _L + "FED_CONGRESS_COMMITTEE_MEMBERSHIP",
                "role": "the committee seats - trades in industries a member's committee oversees are the interesting cross",
                "key_columns": ["BIOGUIDE"],
                "joins": [{"to": _P + "POLITICS__MEMBER_SPINE",
                           "on": "BIOGUIDE = BIOGUIDE", "tier": "STEEL",
                           "gotcha": ""}],
                "traps": [],
            },
            {
                "fqn": _P + "POLITICS__MEMBER_SPINE",
                "role": "who's who",
                "key_columns": ["BIOGUIDE"],
                "joins": [],
                "traps": [],
            },
        ],
        "observations": [
            "AMOUNT is a band, never a number - count trades and band frequencies, never fake precision.",
            "This source carries no disclosure date - the filing itself (PTR_LINK) is the receipt for timing claims.",
            "The interesting cross: trades in industries the member's committee oversees, near key votes.",
            "Journalism use only - this data is legally restricted from any commercial use.",
        ],
    },

    {
        "id": "bills_networks",
        "question": "Who writes the laws, and who signs on?",
        "why": ("Sponsorship and cosponsorship are the visible fingerprints "
                "of agenda and alliance."),
        "tables": [
            {
                "fqn": _P + "POLITICS__BILLS",
                "role": "one row per bill: sponsor, dates, how far it got",
                "key_columns": ["SPONSOR_BIOGUIDE"],
                "joins": [{"to": _P + "POLITICS__MEMBER_SPINE",
                           "on": "SPONSOR_BIOGUIDE = BIOGUIDE", "tier": "STEEL",
                           "gotcha": ""}],
                "traps": ["trap_bills_sponsored_headline"],
            },
            {
                "fqn": _P + "POLITICS__BILL_COSPONSORS",
                "role": "the network edges: every member who signed onto every bill",
                "key_columns": ["COSPONSOR_BIOGUIDE"],
                "joins": [{"to": _P + "POLITICS__BILLS",
                           "on": "bill id = bill id", "tier": "STEEL",
                           "gotcha": ""}],
                "traps": [],
            },
            {
                "fqn": _P + "POLITICS__MEMBER_BILL_RECORD",
                "role": "the per-member rollup: sponsored, cosponsored, advanced",
                "key_columns": ["BIOGUIDE"],
                "joins": [{"to": _P + "POLITICS__MEMBER_SPINE",
                           "on": "BIOGUIDE = BIOGUIDE", "tier": "STEEL",
                           "gotcha": ""}],
                "traps": ["trap_bills_sponsored_headline"],
            },
            {
                "fqn": _P + "POLITICS__MEMBER_SPINE",
                "role": "who's who",
                "key_columns": ["BIOGUIDE"],
                "joins": [],
                "traps": [],
            },
        ],
        "observations": [
            "Cross-party cosponsorship rates say more about how a member works than any speech.",
            "Split substantive bills from ceremonial resolutions before counting anything.",
        ],
    },

    {
        "id": "judges_bench",
        "question": "Who appointed the judges, and where do they lean?",
        "why": ("The judiciary is appointed power - the accountability trail "
                "runs through the presidents and senates that confirmed it."),
        "tables": [
            {
                "fqn": _P + "POLITICS__FJC_JUDGE",
                "role": "one row per federal judge: biography and identifiers",
                "key_columns": ["NID"],
                "joins": [],
                "traps": [],
            },
            {
                "fqn": _P + "POLITICS__FJC_APPOINTMENT",
                "role": "every appointment: which president, which court, which seat, when",
                "key_columns": ["NID"],
                "joins": [{"to": _P + "POLITICS__FJC_JUDGE",
                           "on": "NID = NID", "tier": "STEEL", "gotcha": ""}],
                "traps": [],
            },
            {
                "fqn": _P + "POLITICS__JUDGE_IDEOLOGY_COA",
                "role": "ideology scores for appeals-court judges",
                "key_columns": ["NID"],
                "joins": [{"to": _P + "POLITICS__FJC_JUDGE",
                           "on": "NID = NID", "tier": "STEEL", "gotcha": ""}],
                "traps": [],
            },
            {
                "fqn": _P + "POLITICS__JUDGE_IDEOLOGY_SCOTUS",
                "role": "ideology scores for Supreme Court justices",
                "key_columns": ["NID"],
                "joins": [{"to": _P + "POLITICS__FJC_JUDGE",
                           "on": "NID = NID", "tier": "STEEL", "gotcha": ""}],
                "traps": [],
            },
        ],
        "observations": [
            "Ideology scores are estimates from voting/donation behavior - useful for cohorts, unfair for one individual in isolation.",
            "Appointment cohorts by president and circuit are the systemic view - the map, not a pin.",
        ],
    },

    {
        "id": "who_won",
        "question": "Who actually won the seat, and by how much?",
        "why": ("Margins are the pressure gauge: safe seats and knife-edge "
                "seats produce different behavior."),
        "tables": [
            {
                "fqn": _P + "POLITICS__WHO_WON",
                "role": "election results joined toward the member spine",
                "key_columns": ["STATE", "DISTRICT"],
                "joins": [{"to": _P + "POLITICS__MEMBER_SPINE",
                           "on": "name + state (+district)", "tier": "PROBABILISTIC",
                           "gotcha": "returns data has no hard member ID - this join is a name match, lead-grade"}],
                "traps": ["trap_who_won_name_join"],
            },
            {
                "fqn": _P + "POLITICS__MEMBER_SPINE",
                "role": "who's who",
                "key_columns": ["BIOGUIDE"],
                "joins": [],
                "traps": [],
            },
        ],
        "observations": [
            "Cross vote-margin against money raised: the expensive safe seat is its own pattern.",
        ],
    },

    {
        "id": "excluded_providers",
        "question": "Are banned health providers still active in federal programs?",
        "why": ("The Reading Room's flagship pattern - here is its raw "
                "material, for your own cuts of it."),
        "tables": [
            {
                "fqn": _L + "FED_HHS_OIG_LEIE",
                "role": "the ban list: every person and business excluded from federal health programs",
                "key_columns": ["NPI", "LASTNAME", "EXCLDATE"],
                "joins": [{"to": _L + "FED_CMS_NPPES",
                           "on": "NPI = NPI", "tier": "STEEL",
                           "gotcha": "most LEIE rows carry an all-zero NPI placeholder - filter those before joining"}],
                "traps": ["trap_leie_npi_and_dates"],
            },
            {
                "fqn": _L + "FED_CMS_NPPES",
                "role": "the federal provider registry - the identity backbone for anyone with an NPI",
                "key_columns": ["NPI"],
                "joins": [],
                "traps": ["trap_nppes_ein_masked"],
            },
            {
                "fqn": _L + "FED_CMS_PART_D_PRESCRIBERS",
                "role": "the activity side: Medicare drug-prescribing volume per provider",
                "key_columns": ["NPI"],
                "joins": [{"to": _L + "FED_CMS_NPPES",
                           "on": "NPI = NPI", "tier": "STEEL", "gotcha": ""}],
                "traps": [],
            },
        ],
        "observations": [
            "Exclusion dates are stored as YYYYMMDD text - parse with the explicit format or every date collapses to 1970.",
            "The systemic view: exclusions by state, specialty, and statute code over time - not one bad doctor.",
        ],
    },

    {
        "id": "contractor_floors",
        "question": "Who really gets federal contract money?",
        "why": ("Procurement is the biggest discretionary money flow in the "
                "public record."),
        "tables": [
            {
                "fqn": _L + "FED_USASPENDING_CONTRACTS",
                "role": "federal contract transactions: recipient, agency, obligation, dates",
                "key_columns": ["RECIPIENT_UEI", "FEDERAL_ACTION_OBLIGATION"],
                "joins": [{"to": _L + "FED_SAM_EXCLUSIONS",
                           "on": "RECIPIENT_UEI = UEI", "tier": "STEEL",
                           "gotcha": ""}],
                "traps": ["trap_usaspending_grain"],
            },
            {
                "fqn": _L + "FED_SAM_EXCLUSIONS",
                "role": "the debarment list: entities barred from federal contracting",
                "key_columns": ["UEI"],
                "joins": [],
                "traps": [],
            },
        ],
        "observations": [
            "Sum FEDERAL_ACTION_OBLIGATION (transaction increments) - the cumulative column double-counts.",
            "Negative obligations are real: de-obligated and terminated awards.",
            "The systemic view: concentration - what share of an agency's dollars go to its top ten recipients.",
        ],
    },
]


def pack_ids() -> list[str]:
    return [p["id"] for p in PACKS]


def get_pack(pack_id: str) -> dict | None:
    return next((p for p in PACKS if p["id"] == pack_id), None)
