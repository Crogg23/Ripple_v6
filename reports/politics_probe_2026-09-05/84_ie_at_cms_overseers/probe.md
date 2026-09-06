# 84 — Independent expenditures at the CMS overseers

- **Checked:** IE mart (261,033 rows, 2018–2024; LANDING is a different file: 87,541 rows, 2024–2026) → CAND_ID = legislators' FEC_IDS (JSON list, split) → current members of HSIF / HSWM / SSFI (126 members, 145 FEC ids). Amended filings dropped via PREV_FILE_NUM; SUP_OPP from the IE CSV is the for/against.
- **First number:** $773M of IE aimed at the 126 current members over 2018–2024 — $564M against, $209M for. Senate Finance takes $594M of it (Warnock alone: $149M against, $64M for).
- **Hit means:** the chain closes end to end with real dollars; spender industry comes from the DIM (top 10 are party super PACs and committees: SMP, Senate Leadership Fund, House Majority PAC, DSCC, American Crossroads, AFP Action). 3 of 10 top spenders carry IS_AMBIGUOUS.
- **Miss means:** n/a — it hit. The industry-of-spender leg is thin: CONNECTED_ORG_NM is blank or junk ("NONE", stale joint-fundraiser names) on most big spenders.
- **Trap hit:** mart and LANDING IE are different vintages with zero overlap on years; the mart's national totals ($47B in 2022) look inflated 20x against the FEC's published ~$2B, so trust roster-level sums only after a dedupe pass. Roster is current-only, so 2018 money hits people who were not yet on the committee.

STATUS: lit
HEADLINE: $773M in independent expenditures hit the 126 current members of E&C, Ways & Means and Senate Finance 2018–2024, 73% of it against them, $594M on Senate Finance alone.
