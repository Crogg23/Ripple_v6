# Quote check, full run, 2026-09-25

Script: `quotecheck.py`, v3 rules, unchanged. Output: `quotecheck.tsv`.

## Result

| Status | Quotes | Meaning |
|---|---|---|
| exact | 853 | every word on the page, in order |
| near | 9 | 80%+ of the words in one run |
| missing | 14 | page loaded, quote not found |
| blocked | 13 | page never loaded |
| **total** | **889** | 208 stories; S034 has no sources |

Verified = 862 of 889, 97.0%.

## How it ran

- Pass 1 fetched 854 unique pages, 16 at a time, via a wrapper that called the script's own functions.
- That pass lost 27 pages to the Internet Archive fallback: parallel lookups got nothing back.
- Passes 2 to 4 re-ran the unmodified script, one page at a time, on stories with a blocked source.
- Blocked went 40 → 25 → 14 → 13 → 13. Stopped when a pass changed nothing.
- Every status came from the script's own `check()`; the wrapper only changed fetch order.

## The 14 missing: zero are fake quotes

| Story | Idx | What happened | Real quote? |
|---|---|---|---|
| S026 | 2 | page splits words: "mi llions", "t rades" | yes |
| S033 | 0 | PDF splits words: "t ribe", "tc sa" | yes |
| S046 | 0 | PDF splits "se ptember" | yes |
| S046 | 2 | PDF splits "mi nimum" | yes |
| S159 | 2 | page joins "nearly—dead" into "nearlydead" | yes |
| S085 | 3 | page text reads "at least 0 million" where the quote says "$100 million" | words yes, number unverified |
| S181 | 0 | searcher stitched two sentences, dropped the one between | facts yes, not one quote |
| S044 | 1 | JAMA served a 1-word "loading" stub | page never loaded |
| S044 | 2 | same JAMA stub | page never loaded |
| S058 | 0 | PubMed served a "checking your browser" wall | page never loaded |
| S104 | 0 | DOJ page saved with 0 words | page never loaded |
| S107 | 3 | McDermott served an Incapsula bot-wall stub | page never loaded |
| S152 | 1 | PressReader served a 6-word stub | page never loaded |
| S067 | 4 | AJC paywall reverses each word and shuffles the paragraph: "detroper", "shtnom", "7.11" | yes, all words in one paragraph |

- S067/4 was marked paywalled false by the searcher; the page says isAccessibleForFree False.
- Caught by the skeptic pass, not the first read.
- The six stubs came back as HTTP 200, so the script cached them and graded them missing, not blocked.
- The cache means a re-run never refetches them.
- Every story above still has at least one other verified source naming its entity.

## The 13 still blocked

| Story | Idx | Site | Paywalled | Why |
|---|---|---|---|---|
| S035 | 3 | healthaffairs.org | yes | 403, no archive copy |
| S071 | 2 | gvwire.com | no | 403, no archive copy |
| S080 | 0 | pacermonitor.com | no | 429 rate limit, no archive copy |
| S082 | 5 | tandfonline.com | yes | 403, no archive copy |
| S125 | 1 | cutimes.com | yes | 403, no archive copy |
| S128 | 1 | sec.gov | no | 403 |
| S130 | 0 | sec.gov | no | 403 |
| S130 | 1 | sec.gov | no | 403 |
| S131 | 0 | sec.gov | no | 403 |
| S131 | 1 | stocktitan.net | no | 403 |
| S134 | 1 | yumaaz.gov | no | 403 |
| S151 | 0 | taxpayeradvocate.irs.gov | no | PDF would not parse |
| S194 | 0 | sec.gov | no | 403 |

- sec.gov refuses any request without a declared name and contact email.
- **S080 and S130:** every source that names the entity is blocked.
  - Under JUDGE.md, blocked and not paywalled means unusable.
  - So these two can't reach Matched on current evidence.

## Other counts the judges will meet

- 50 stories have no verified source that names the entity.
- 22 exact quotes are under 8 words: table rows, headlines, dollar figures.
- Some are real but prove nothing: S099/4 is rule text, S146 "Designated as a 501(c)(4)", S084 "Forest 317".
- S132 logged 4 queries, under the 5 needed for Unreported.
