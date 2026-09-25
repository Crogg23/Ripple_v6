-- @voeten_eyeball_argentina
-- Eyeball the raw dyad rows behind the Argentina finding, both directions, sessions 76-79: Argentina-US, Argentina-Israel, UK-US
select SESSION_X, YEAR, CCODE1, CCODE2, AGREE, IDEALPOINTFP_X, NVOTESFP_X, IDEALPOINTFP_Y, NVOTESFP_Y, IDEALPOINTDISTANCE, COL_0
from LIBRARY_MARTS.POLITICS.POLITICS__INTL_VOETEN_UNGA_VOTES
where try_to_number(SESSION_X) between 76 and 79
  and ((CCODE1 = '160' and CCODE2 in ('2', '666')) or (CCODE1 = '2' and CCODE2 in ('160', '200')))
order by CCODE1, CCODE2, SESSION_X;
