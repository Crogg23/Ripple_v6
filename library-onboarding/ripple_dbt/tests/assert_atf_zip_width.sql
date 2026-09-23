-- ATF dealer zips arrive with leading zeros stripped (the ArcGIS layer serves
-- them as numbers). The mart zero-fills them. Any zip that is not 5 or 9 digits
-- after that means the pad regressed, or a new width showed up at source.
-- Found by the 2026-09-23 catalog audit: 3,333 of 77,514 rows were 3, 4, 7 or 8 digits.
select ffl_number, premise_zip_code, mail_zip_code
from {{ ref('justice__fed_atf_ffl') }}
where (premise_zip_code is not null and length(premise_zip_code) not in (5, 9))
   or (mail_zip_code is not null and length(mail_zip_code) not in (5, 9))
