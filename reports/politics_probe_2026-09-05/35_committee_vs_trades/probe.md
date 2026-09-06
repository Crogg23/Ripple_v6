# 35 Committee assignment vs stock trades (House)
- Checked: FED_HOUSE_FD_PTR_INDEX (41,883 rows → 41,864 after hash(*) dedupe; DOCID 41,860 distinct, so 4 rows share a DOCID with different content) → filers of type P (periodic transaction report) → FED_CONGRESS_LEGISLATORS on surname + state + district (three fields, not a bare surname) → FED_CONGRESS_COMMITTEE_MEMBERSHIP, full House committees, current snapshot.
- First number: 180 of 204 PTR filers since 2023 match one bioguide (0 match two), 153 of them sit on a current House committee, carrying 1,739 of 1,795 PTR filings. Ways and Means leads (21 members, 324 filings), then Foreign Affairs 281, Energy and Commerce 243, Financial Services 225. 5 eyeballed matches were 5 for 5 real (Magaziner RI02, Steube FL17, McClellan VA04, Davidson OH08, Mast FL21); 0% false positives seen.
- Can support: who files trade reports, how many, when (2013-2026, ~700/yr, 100-130 filers/yr), and which committee they sit on today.
- Cannot support: what they traded. The index has no ticker, asset, amount, or transaction date — the trade lines live in the PDFs behind each DOCID. "Trading in the industry their committee regulates" has no leg here.
- Hit means: a committee member is an active trader. Miss means: not filing, or a surname/district spelling the legislators file doesn't share (24 unmatched, 56 filings).
- Trap hit: DOCID not unique, hash(*) dedupe used; FILINGDATE is m/d/yyyy text with blanks, INDEX_YEAR used instead. Committee roster is today's, so pre-2023 filings were left out on purpose.
- Cost: 5 queries (plus the shared discovery logged under 78); longest 17.7s.
STATUS: dim
HEADLINE: 153 current House committee members filed 1,739 trade reports since 2023 (Ways and Means: 21 members, 324 filings) — but the index says who filed, never what they bought.
