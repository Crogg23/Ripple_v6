import json, statistics as st
from pathlib import Path
from collections import defaultdict, Counter
H = Path(__file__).parent
d = json.load(open(H/'r04_medsl_all.json'))
cols = d['cols']; rows = [dict(zip(cols, r)) for r in d['rows']]
print(len(rows), cols)
print('years', sorted(Counter(r['ELECTION_YEAR'] for r in rows).items()))
print('states per year', {y: len({r['STATE_ABBR'] for r in rows if r['ELECTION_YEAR']==y}) for y in sorted({r['ELECTION_YEAR'] for r in rows})})
print('writein', Counter(r['IS_WRITEIN'] for r in rows))
print('fips sample', Counter(r['STATE_FIPS'] for r in rows).most_common(5), 'loaded', Counter(r['_LOADED_AT'] for r in rows).most_common(3))
print('party top', Counter(r['PARTY'] for r in rows).most_common(15))
print('cand NA/blank', sum(1 for r in rows if r['CANDIDATE_NAME'] in ('NA','',None)), Counter(r['CANDIDATE_NAME'] for r in rows).most_common(6))
# total_votes consistency within state-year
g = defaultdict(list)
for r in rows: g[(r['ELECTION_YEAR'], r['STATE_ABBR'])].append(r)
incons = [(k, sorted({x['TOTAL_VOTES'] for x in v})) for k,v in g.items() if len({x['TOTAL_VOTES'] for x in v})>1]
print('state-years', len(g), 'total_votes inconsistent', len(incons), incons[:5])
# sum of candidate votes vs total
diffs = []
for k,v in g.items():
    s = sum(int(x['CANDIDATE_VOTES']) for x in v); t = int(v[0]['TOTAL_VOTES'])
    diffs.append((round(s/t,4), k))
diffs.sort()
print('sum/total min', diffs[:5], 'max', diffs[-5:])
# duplicate candidate rows within state-year (fusion lines)
dup = Counter((r['ELECTION_YEAR'], r['STATE_ABBR'], r['CANDIDATE_NAME']) for r in rows if r['CANDIDATE_NAME'] not in ('NA','',None))
dd = [(k,n) for k,n in dup.items() if n>1]
print('candidate repeated within state-year', len(dd), dd[:8])
# NA candidate votes
na = [(r['ELECTION_YEAR'], r['STATE_ABBR'], r['PARTY'], r['CANDIDATE_VOTES'], r['IS_WRITEIN']) for r in rows if r['CANDIDATE_NAME'] in ('NA','',None)]
print('NA rows', len(na), na[:10])
# max
mx = max(rows, key=lambda r: int(r['CANDIDATE_VOTES']))
print('max cand', mx)
