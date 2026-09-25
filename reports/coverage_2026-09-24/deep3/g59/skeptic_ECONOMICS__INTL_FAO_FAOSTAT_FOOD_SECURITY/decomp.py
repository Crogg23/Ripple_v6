# skeptic: decompose the world-minus-published-countries gap by region, from the builder's q06.json pull
import json, collections, sys
d=json.load(open(r'C:\Code\Ripple_v6\reports\coverage_2026-09-24\deep3\g59\q06.json')); cols=d['cols']
rows=[dict(zip(cols,r)) for r in d['rows']]
def num(v):
    try: return float(v)
    except: return None
ser=collections.defaultdict(dict); code={}; m49={}
for r in rows:
    ser[(r['AREA'],r['ITEM_CODE'])][r['YEAR_CODE']]=(r['VALUE'],r['FLAG'],r['NOTE'])
    code[r['AREA']]=int(r['AREA_CODE']); m49[r['AREA']]=int(str(r['AREA_CODE_M49']).strip("'"))
S=lambda s:{int(x) for x in s.split()}
REG={
 'Southern Asia':S('4 50 64 356 364 462 524 586 144'),
 'Eastern Asia':S('156 344 446 158 408 392 496 410'),
 'South-eastern Asia':S('96 116 360 418 458 104 608 702 764 626 704'),
 'Western Asia':S('51 31 48 196 268 368 376 400 414 422 512 634 682 275 760 792 784 887'),
 'Central Asia':S('398 417 762 795 860'),
 'Northern Africa':S('12 818 434 504 729 788 732'),
 'Sub-Saharan Africa':S('24 204 72 854 108 132 120 140 148 174 178 180 384 262 226 232 748 231 266 270 288 324 624 404 426 430 450 454 466 478 480 175 508 516 562 566 638 646 654 678 686 690 694 706 710 728 768 800 834 894 716'),
 'Latin America and the Caribbean':S('28 32 44 52 84 68 76 152 170 188 192 212 214 218 222 308 320 328 332 340 388 484 558 591 600 604 630 659 662 670 740 780 858 862 533 531 92 136 796 660 500 534 238 254 312 474 652 663 850'),
 'Oceania':S('36 554 242 598 90 548 540 258 882 776 798 296 520 584 583 585 16 184 570 772 316 580 612 876'),
}
per=sys.argv[1] if len(sys.argv)>1 else '20222024'; it=sys.argv[2] if len(sys.argv)>2 else '210071'
countries=[a for a in code if code[a]<5000 and code[a] not in (351,420,429)]
def reg_of(a):
    for k,v in REG.items():
        if m49[a] in v: return k
    return 'Northern America and Europe'
tot_res=0; tot_w=num(ser[('World',it)][per][0])
print('item',it,'period',per,'world',tot_w)
bucket=collections.defaultdict(list)
for a in countries: bucket[reg_of(a)].append(a)
for k in list(REG)+['Northern America and Europe']:
    rv=num(ser.get((k,it),{}).get(per,(None,))[0])
    pub=sum(num(ser.get((a,it),{}).get(per,(None,))[0]) or 0 for a in bucket[k])
    miss=[a for a in bucket[k] if num(ser.get((a,it),{}).get(per,(None,))[0]) is None and not str(ser.get((a,it),{}).get(per,('',))[0]).startswith('<')]
    res=None if rv is None else round(rv-pub,1)
    tot_res+= res or 0
    print(f'{k:34} region={rv} published={round(pub,1)} residual={res} | blank: '+', '.join(f"{a[:18]}({ser.get((a,it),{}).get(per,('',''))[1]})" for a in miss))
print('sum of regional residuals',round(tot_res,1),'world residual', round(tot_w-sum(num(ser.get((a,it),{}).get(per,(None,))[0]) or 0 for a in countries),1))
print('regions sum', round(sum(num(ser.get((k,it),{}).get(per,(None,))[0]) or 0 for k in list(REG)+['Northern America and Europe']),1))
sa=num(ser[('Southern Asia',it)][per][0]); sax=num(ser[('Southern Asia (excluding India)',it)][per][0])
print('INDIA by subtraction = Southern Asia - Southern Asia (excl India) =', round(sa-sax,1))
ssa=num(ser[('Sub-Saharan Africa (including Sudan)',it)][per][0]); ss=num(ser[('Sub-Saharan Africa',it)][per][0])
na=num(ser[('Northern Africa',it)][per][0]); nax=num(ser[('Northern Africa (excluding Sudan)',it)][per][0])
print('SUDAN by subtraction: SSA(incl)-SSA =', round(ssa-ss,1), ' NAfr-NAfr(excl) =', round(na-nax,1))
