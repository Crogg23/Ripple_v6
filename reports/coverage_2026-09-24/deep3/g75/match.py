import pandas as pd, numpy as np, re, unicodedata
def norm(s):
    s=unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().upper()
    return re.sub(r'[^A-Z0-9 \-,]',' ',s)
SUFF={'JR','SR','II','III','IV','MR','MRS','MS','DR','ESQ','MD','PHD','CPA','THE','MISS','SIR','LORD','LADY'}
ORG=re.compile(r'\b(LLC|L L C|INC|LTD|LIMITED|CORP|CORPORATION|COMPANY|CO|LP|L P|LLP|TRUST|FUND|FOUNDATION|BANK|HOLDINGS?|PARTNERS|CAPITAL|GROUP|MANAGEMENT|SA|S A|AG|GMBH|BV|NV|PLC|ASSOCIATES|INVESTMENTS?|ENTERPRISES?|SERVICES|INTERNATIONAL|AND|&|OF|ESTATE)\b')
def person_key(name):
    n=norm(name)
    if ORG.search(n): return None
    if ' - ' in n:  # Appleby "Last - First Middle"
        last,first=n.split(' - ',1)
        lt=[t for t in re.split(r'[ ,\-]+',last) if t and t not in SUFF]
        ft=[t for t in re.split(r'[ ,\-]+',first) if t and t not in SUFF]
        if not lt or not ft: return None
        return (ft[0], lt[-1], ft[1][0] if len(ft)>1 else '')
    if ',' in n:
        last,first=n.split(',',1)
        lt=[t for t in re.split(r'[ \-]+',last) if t and t not in SUFF]
        ft=[t for t in re.split(r'[ \-]+',first) if t and t not in SUFF]
        if not lt or not ft: return None
        return (ft[0], lt[-1], ft[1][0] if len(ft)>1 else '')
    t=[x for x in re.split(r'[ \-]+',n) if x and x not in SUFF and len(x)>0]
    t=[x for x in t if not (len(x)==1 and False)]
    if len(t)<2: return None
    return (t[0], t[-1], t[1][0] if len(t)>2 else '')
