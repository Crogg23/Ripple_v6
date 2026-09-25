"""Draw the 20-story pilot: two positive controls plus 18 at random, spread by novelty guess."""
import csv, random
from pathlib import Path

HERE = Path(__file__).parent
rows = list(csv.DictReader(open(HERE / "stories.tsv", encoding="utf-8"), delimiter="\t"))
CONTROLS = ["S001", "S007"]
PER_NOVELTY = {"1": 3, "2": 4, "3": 5, "4": 3, "": 3}

rng = random.Random(20260925)
picked = [r for r in rows if r["story_id"] in CONTROLS]
for nov, k in PER_NOVELTY.items():
    pool = [r for r in rows if r["novelty_guess"] == nov and r["story_id"] not in CONTROLS]
    picked += rng.sample(pool, k)

with open(HERE / "pilot.tsv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, delimiter="\t")
    w.writerow(["story_id", "role", "novelty_guess", "grade", "verdict", "pre_known", "headline"])
    for r in picked:
        w.writerow([r["story_id"], "control" if r["story_id"] in CONTROLS else "random",
                    r["novelty_guess"], r["grade"], r["verdict"], r["pre_known"], r["headline"]])
print(len(picked))
