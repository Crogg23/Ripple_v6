-- S20 DOJ press-release link text (Wayback replay of justice.gov listings) for the top stays-per-patient hospitals
SELECT 'listing' src, link_text, resolved_url, captured_at FROM LIBRARY_MARTS.INVESTIGATIONS.INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_LISTING
WHERE link_text ILIKE ANY ('%oroville%', '%north vista%', '%larkin%', '%alliancehealth%', '%meritus%', '%enloe%', '%sepsis%')
UNION ALL
SELECT 'deep', link_text, resolved_url, captured_at FROM LIBRARY_MARTS.INVESTIGATIONS.INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_DEEP_PAGES
WHERE link_text ILIKE ANY ('%oroville%', '%north vista%', '%larkin%', '%alliancehealth%', '%meritus%', '%enloe%', '%sepsis%')
