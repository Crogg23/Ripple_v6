import io, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def build(tpl, out, subs):
    s = io.open(tpl, encoding="utf-8").read()
    for k, path in subs.items():
        assert s.count(k) == 1, (tpl, k, s.count(k))
        s = s.replace(k, io.open(path, encoding="utf-8").read())
    io.open(out, "w", encoding="utf-8").write(s)
    print(out, os.path.getsize(out)//1024, "KB")
build("pulsegrid_template.html", "pulsegrid.html", {"__PULSE__": "pulse.json"})
build("bankdeserts_template.html", "bankdeserts.html", {"__BRANCHES__": "branches.json", "__STATES__": "c_states.json"})
build("moneyshape_template.html", "moneyshape.html", {"__AMOUNTS__": "fec_amounts.json", "__DIGITS__": "fec_digits.json", "__YEARS__": "fec_years.json"})
