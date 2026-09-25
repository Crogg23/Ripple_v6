# skeptic: rebuild the farm rule from s05.json with my own normalization; sensitivity tests
import json, re, collections
D = r'C:\Code\Ripple_v6\reports\coverage_2026-09-24\joins\j5'
d = json.load(open(D + r'\s05.json')); cols = d['cols']
rows = [dict(zip(cols, r)) for r in d['rows'] if r[cols.index('DEACT_DT')] is None]
AB = {'SOUTHWEST':'SW','SOUTHEAST':'SE','NORTHWEST':'NW','NORTHEAST':'NE','NORTH':'N','SOUTH':'S','EAST':'E','WEST':'W',
      'FREEWAY':'FWY','BOULEVARD':'BLVD','AVENUE':'AVE','STREET':'ST','ROAD':'RD','DRIVE':'DR','PARKWAY':'PKWY','HIGHWAY':'HWY',
      'LANE':'LN','COURT':'CT','PLACE':'PL','CIRCLE':'CIR','SUITE':'STE','EXPRESSWAY':'EXPY','TRAIL':'TRL','PLAZA':'PLZ','CENTER':'CTR'}
def addr(a):
    a = re.sub(r'[.,]', ' ', (a or '').upper())
    a = re.split(r'\s(?:STE|SUITE|#|RM|ROOM|UNIT|BLDG|BUILDING|APT|FL|FLOOR|SPC|OFC|OFFICE)\b|#', ' ' + a)[0]
    w = [AB.get(x, x) for x in a.split()]
    return ' '.join(w)
def nm(n):
    n = re.sub(r'[^A-Z0-9 ]', ' ', (n or '').upper())
    n = re.sub(r'\b(INC|LLC|L L C|CORP|CORPORATION|CO|COMPANY|PLLC|LTD|THE|DBA|D B A)\b', ' ', n)
    return re.sub(r'\s+', '', n)
HOU = {'HOUSTON','RICHMOND','KATY','STAFFORD','SUGAR LAND','MISSOURI CITY','SPRING','PEARLAND','CYPRESS','HUMBLE','PASADENA','TOMBALL','BELLAIRE','BAYTOWN','LEAGUE CITY','FRIENDSWOOD','THE WOODLANDS','CONROE','KINGWOOD','WEBSTER','ROSENBERG','FRESNO','ALVIN','SEABROOK','CHANNELVIEW','LA PORTE','DEER PARK','MAGNOLIA','HOCKLEY','FULSHEAR','MANVEL','SOUTH HOUSTON','CLEAR LAKE','GALVESTON','TEXAS CITY','DICKINSON','LEAGUE CITY'}
def area(r):
    if r['ST']=='TX' and r['CITY']=='SAN ANTONIO': return 'SA'
    if r['ST']=='TX' and r['CITY'] in HOU: return 'HOU'
    if r['ST']=='CA': return 'CA'
    return 'ELSE'
def run(keyf, namef, minn=4, label=''):
    g = collections.defaultdict(list)
    for r in rows:
        if not r['AO_LAST']: continue
        g[keyf(r)].append(r)
    farm = set()
    for k, v in g.items():
        if len({namef(x['LBN']) for x in v}) >= minn: farm.update(x['NPI'] for x in v)
    den = collections.Counter(area(r) for r in rows); num = collections.Counter(area(r) for r in rows if r['NPI'] in farm)
    print(label, {a: f"{num[a]}/{den[a]}={num[a]/den[a]*100:.1f}%" for a in ['SA','HOU','CA','ELSE']}, 'farms NPIs', len(farm))
    return farm
b = run(lambda r:(r['AO_FIRST'],r['AO_LAST'],r['ST'],r['CITY'],addr(r['A1'])), lambda n:(n or '').upper(), label='raw-name   ')
b2= run(lambda r:(r['AO_FIRST'],r['AO_LAST'],r['ST'],r['CITY'],addr(r['A1'])), nm, label='norm-name  ')
b3= run(lambda r:(r['AO_LAST'],r['ST'],r['CITY'],addr(r['A1'])), nm, label='lastname   ')
b4= run(lambda r:(r['ST'],r['CITY'],addr(r['A1'])), nm, label='addr-only  ')
b5= run(lambda r:(r['AO_FIRST'],r['AO_LAST'],r['ST'],r['CITY'],addr(r['A1'])), nm, minn=3, label='norm-name3 ')
b6= run(lambda r:(r['AO_FIRST'],r['AO_LAST'],r['ST']), nm, minn=4, label='ao+state   ')
# houston area den with just HOUSTON
print('HOUSTON city only den', sum(1 for r in rows if r['ST']=='TX' and r['CITY']=='HOUSTON'))
f = json.load(open(D + r'\farms.json'))['farms']; bf = set(x for v in f.values() for x in v)
print('builder', len(bf), 'mine raw', len(b), 'only builder', len(bf-b), 'only mine', len(b-bf))
by = {r['NPI']: r for r in rows}
for n in sorted(b-bf)[:40]: r=by[n]; print(' +', r['ST'], r['CITY'], r['AO_FIRST'], r['AO_LAST'], '|', r['A1'], '|', r['LBN'])
for n in sorted(bf-b)[:40]: r=by.get(n); print(' -', r and (r['ST'], r['CITY'], r['AO_FIRST'], r['AO_LAST'], r['A1'], r['LBN']))
# Superior Hospice-type chains inside SA
