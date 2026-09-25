-- @odd_house_accounts_creatives
-- Where six odd House-EIN accounts aimed their ads: 'Rep. Steel' (spend mostly NV/OH/MN), 'Rep. Goldman' (mostly CA), 'Rep. Kevin McCarthy' (84% outside CA),
-- and the three other generic accounts ('US House of Representatives' CO-heavy, 'US House of Reps.' NY-heavy, 'Office of Finance')
SELECT ADVERTISER_ID, ADVERTISER_NAME, GEO_TARGETING_INCLUDED, COUNT(*) ads,
       SUM(TRY_TO_NUMBER(SPEND_RANGE_MIN_USD)) min_usd, SUM(TRY_TO_NUMBER(SPEND_RANGE_MAX_USD)) max_usd,
       MIN(DATE_RANGE_START) first_day, MAX(DATE_RANGE_END) last_day
FROM LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_CREATIVE_STATS
WHERE ADVERTISER_ID IN ('AR13522503217748901889','AR16196087374160068609','AR07280544198984466433',
                        'AR07359836459274076161','AR15487617555018809345','AR11679967951481470977')
GROUP BY 1, 2, 3
