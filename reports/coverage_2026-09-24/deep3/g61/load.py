import json
def load(q):
    d=json.load(open(f'{q}.json',encoding='utf-8'))
    return [dict(zip(d['cols'],r)) for r in d['rows']]
def num(x):
    if x is None: return None
    try: return float(x)
    except: return None
