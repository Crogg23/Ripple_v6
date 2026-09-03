# Date/time cast inventory

Tables scanned: 2208
Flagged columns: 5772

## By bucket

| bucket | columns | tables |
|---|---|---|
| content_date | 4657 | 1941 |
| audit_num | 483 | 483 |
| unclassified_needs_eyeball | 336 | 204 |
| unclassified_blank_or_sentinel | 174 | 121 |
| native | 122 | 122 |

## By pattern (auto-fixable buckets only)

| bucket | pattern | columns |
|---|---|---|
| content_date | iso | 2916 |
| content_date | epochms | 709 |
| content_date | us | 680 |
| audit_num | epoch_microsecond | 483 |
| content_date | ymd8 | 245 |
| content_date | dmon | 101 |
| content_date | mdy8 | 4 |
| content_date | epochs | 2 |
