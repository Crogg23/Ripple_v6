-- S19 Outside money for and against each member of Congress, 2024 and 2026 cycles (a stand-in for how tight each member's race is)
SELECT BIOGUIDE, CYCLE, OUTSIDE_FOR, OUTSIDE_AGAINST, PAC_DONATIONS, N_PAC_DONORS
FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_PAC_MONEY
WHERE CYCLE IN (2024, 2026)
