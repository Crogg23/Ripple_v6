# 82 Unions with a shortage and a PAC
- Checked: LABOR__FED_DOL_OLMS (617,710 rows, 2000-2026, 34,963 file numbers) SHORTAGE_AMOUNT fill, PAC_FUNDS values, landing SHORTAGE column; FEC committees dim CONNECTED_ORG_NM for ORG_TP='L'.
- First number: SHORTAGE_AMOUNT is filled on 78 of 617,710 rows, and all 78 are column-shifted junk: UNION_NAME is a number on 39, YEAR_COVERED null on 78, TOTAL_RECEIPTS null on 78, and the "shortage" is 2009/2010 (a year that slid into the money column). Landing SHORTAGE is non-blank on 605,311 rows but positive on the same 78. Real shortage dollars in the file: zero.
- PAC leg is alive: PAC_FUNDS='T' on 41,766 filings ('F' 427,876, '' 147,988). FEC labor committees carry a connected-org name on most rows, blank on 255.
- A hit would have meant a local with missing money and a giving PAC in the same year. A miss means the LM-2 shortage field never landed as money, so the cross cannot be built here.
- Trap hit: SHORTAGE_AMOUNT looks like a money column and holds 78 shifted years; the DOL form's item-13 shortage answer is not in this extract at all.
- Nearest substitute: none landed; would need the OLMS LM-2 item-13 detail file.
STATUS: dead
HEADLINE: 0 real shortage dollars in 617,710 OLMS filings; the 78 non-zero SHORTAGE_AMOUNT rows are column-shifted years, PAC flag alone is set on 41,766 filings.
