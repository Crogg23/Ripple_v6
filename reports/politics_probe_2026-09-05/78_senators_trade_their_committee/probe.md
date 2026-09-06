# 78 Senators trade the industry their committee marks up
- Checked: POLITICS__SENATE_TRADES (8,350 rows, 57 bioguides, 2012-06..2020-12, every match "surname+senate+term-span") → ticker → CIK (FED_SEC_EDGAR_COMPANY_TICKERS) → SIC (FED_SEC_DERA_SUB_2024Q1..2026Q1, latest filing per CIK) → hand crosswalk of 7 Senate committees to SIC ranges → FED_CONGRESS_COMMITTEE_MEMBERSHIP (full Senate committees, current snapshot). Discovery in discover.py/profile.py/profile2.py, same log.
- First number: 13 senators, 227 buy/sell trades, 80 tickers, where the ticker's SIC sits in a sector their committee marks up. Top: Capito 47 trades in 18 Commerce-sector tickers (AAPL, INTC, T, CSX...), Cassidy 18 HELP pharma/device + 17 Energy oil/utility, Murray 19 pharma in 3 months of 2017, Hoeven 15 food + 15 oil/gas.
- Coverage: 567 of 995 traded tickers get a SIC (4,588 of 6,178 buy/sell rows); the rest are delisted, foreign, or fund tickers DERA never sees.
- Hit means: a senator held or moved stock in an industry their committee writes the rules for. Miss means: the ticker never got a SIC, or the senator is not on today's roster.
- Trap hit: vintage mismatch. Trades stop 2020-12; the roster is 2025-26 with no term dates; only 38 of 57 trading senators are on it. Every hit is "traded then, sits there now", not "sat there when trading". Second trap: the crosswalk is coarse — VMC (Vulcan, SIC 1400 mining) lands on Energy; 4 of 5 eyeballed hits were clean, 1 was crosswalk-loose.
- Voteview leg (30-day vote window) not run: rollcalls are 118th-119th Congress only, zero overlap with the trade years.
- Cost: 26 discovery queries shared across 35/78/91 plus 5 probe queries; longest 18.3s.
STATUS: dim
HEADLINE: 13 senators made 227 trades in 80 tickers inside their own committee's sector — but the trades are 2014-2020 and the roster is 2025, so the seat and the trade never line up in time.
