# 86 — Google ad money the FEC never saw

- **Checked:** EDUCATION mart POLADS weekly spend (298,884 rows, 21,211 advertisers, identical to LANDING) summed on SPEND_USD → six-figure US advertisers (1,968) → tagged by ADVERTISER_STATS.PUBLIC_IDS_LIST containing an FEC C-id, and by folded name equal to a DIM CMTE_NM → top state from ADVERTISER_GEO_SPEND.
- **First number:** 956 US advertisers with $100K+ on Google carry no FEC id and no committee-name match — $725M, 29% of the $2.5B six-figure total. CA alone: 228 advertisers, $294M.
- **Verified by eye (top 15):** 10 are state races or ballot measures (Steyer for Governor, Newsom ballot committee, Yes on 22/27, Spanberger), 3 are commercial (Money Metals, SmartNews, Kalshi), 1 is a 501c4 (Majority Forward), 1 is a miss — Americans for Prosperity Action does have an FEC committee. False-positive rate on "no FEC": 1 of 15.
- **Hit means:** the number is real but mostly says "state politics runs on Google", not "federal money hid from the FEC".
- **Miss means:** to isolate the federal dark slice you need PUBLIC_IDS_LIST parsed (EIN vs "Registered in US-CA" vs FEC) plus a federal-race filter from creative targeting; neither is in the chain.
- **Trap hit:** ELECTION_CYCLE is null on every weekly row, so the cycle facet in the hunch does not exist; PUBLIC_IDS_LIST is the better key than advertiser name. MEDSL margins leg not attempted.

STATUS: dim
HEADLINE: 956 six-figure Google political advertisers ($725M) have no FEC committee, but 10 of the top 15 are state races and ballot measures, so the federal "never saw" slice is unmeasured.
