import json, sys
w = int(sys.argv[2]) if len(sys.argv) > 2 else 60
d = json.load(open(sys.argv[1] + ".json", encoding="utf-8"))
print(" | ".join(d["cols"]))
for r in d["rows"]:
    print(" | ".join("" if v is None else str(v)[:w] for v in r))
