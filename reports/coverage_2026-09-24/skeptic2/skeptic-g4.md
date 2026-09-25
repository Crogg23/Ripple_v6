# Skeptic g4, 2026-09-24

Saved by the main session from the skeptic's reply; the skeptic agent is read-only and could not write files.
SQL: `skeptic-g4.sql`, 30 statements, 3 failed to compile and were rerun. Tag `skeptic-r2-2026-09-24`.
Every name is a data match, not verified against primary records.

## POLITICS__TX_LOBBY_TRANSPORTATION: CONFIRMED, grade B
- Report 101046715 is CORLOBBYACT, a correction. Transport $79,647.58, food $2,295.04. The original April report is not in the table.
- 15 trip lines, 15 distinct travel IDs, 8 people, all private air, no duplicate legs.
- Clients: Success Academy, Kleinheinz Capital Partners.
- One report per filer/year/period: 3,448 reports with transport over $0, median $188. Rank 3 holds; #1 $156,254, #2 $130,592.
- 7 people round trip. Jeff Leach flew one leg, New York to Fort Worth. The deep pass said "did not fly": wrong.
- No other 2026 report names these 8.
- Report ID order suggests the correction was filed after 2026-05-11 though FILED_DT reads 04-10. Inference, not checked.

**Corrected headline:** A corrected April 2026 Texas lobby report puts $79,647.58 of private-jet travel on a one-night New York "educational tour," March 30-31. Travelers: Sen. Angela Paxton, Reps. Brad Buckley, Caroline Fairly, Jeff Leach (one leg), and 4 untitled people. Clients: Success Academy and Kleinheinz Capital Partners. 3rd-largest transport total of 3,448 reports since 1991; median $188.
**Next:** pull original and corrected filings from the Texas Ethics Commission; join TX_LOBBY_SUBJECT_MATTER and TX_LOBBY_DOCKETS on REPORT_ID = REPORT_INFO_IDENT. No Texas campaign-finance table exists in the warehouse.

## POLITICS__TX_LOBBY_COVER: CONFIRMED, grade B
- 62 Abboud reports with media over $0, one per monthly period. 2 corrections each replace an original.
- Amounts exact to the cent. Texas reports these as amounts, not ranges.
- $29,915,696.51 total, $20,575,810.66 Abboud, raw or deduped: 68.8% both ways.
- Only Abboud's reports name Sands with media spend. INDIVIDUAL_REPORTING is sparse, 38,662 rows, so "only" is a floor.
- Feb-May 2025: $9.37M. Off-session months $16K-$31K flat, likely a retainer.
- APPLICABLE_YEAR shifts the calendar slightly; totals unchanged.

**Corrected headline:** One Las Vegas Sands lobbyist, Andy Abboud, reported $20.58M in media spending across 62 monthly Texas reports, mid-2021 to mid-2026: 68.8% of all Texas lobby media dollars. $9.37M came in Feb-May 2025 alone.
**Next:** check TEC's definition of "media"; search prior coverage; join SUBJECT_MATTER and DOCKETS to line spend up against casino bills.

## FINANCE__FED_PCAOB_FORM_AP_FILINGS: CONFIRMED numbers, NARROWED news value, grade B (Borgers alone C)
- Operating-company rows carry 0 fund series. Fund-family explanation ruled out.
- Partner 0504100001 distinct issuers 2017-2024: 51, 78, 84, 95, 121, 162, 165, 88. Median partner 1, p99 11-17.
- 2020 top was Marcum's Edward Hackert, 111, 76 of them SPACs.
- 11 spellings on the ID, one person in practice.
- 218 operating clients 2023-24: 83 moved firms, 135 no new Form AP.
- Famous: SEC charged B F Borgers May 2024, $14M fine, bar. General knowledge, not warehouse.

**Corrected headline:** From 2017 to 2023 one B F Borgers partner ID signed 51-165 distinct operating-company audits a year; median partner 1, p99 11-17. After the 2024 bar, 135 of 218 recent clients filed no new audit.
**Next:** Borgers' former clients by ISSUER_CIK to SEC EDGAR filings/delistings; the fresh story is the successor one-partner shops signing 19-39 audits a year in 2024-25.

## FINANCE__FED_SENATE_EFD_PTR: NARROWED, grade C
- Alan Armstrong R-OK, term start 2026-03-24. March trades fall in his term, except the first day is ambiguous.
- One filing, not an amendment, filed 2026-07-21. 703 lines, 346 tickers.
- Comment: joint securities; March trades by a third-party advisor setting up direct indexing. OWNER reads Self on March lines, Joint on June: contradicts the comment.
- ISO dates, no parse error. 587 of 703 in the $1,001-$15,000 bucket. Other new senators file normally.
- 701 March lines 112-119 days late, $3,247,701 to $16,055,000.

**Corrected headline:** Sen. Alan Armstrong's first periodic trade report, filed July 21, 2026, disclosed 701 March 2026 trades worth $3.2M-$16.1M, 112-119 days after they happened. The limit is 45. The report says an advisor made them to set up a direct-indexing portfolio.
**Next:** rank lateness per filing across all senators in FINANCE__SENATE_TRADES on BIOGUIDE.
