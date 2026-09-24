"""Split facts.tsv into triage chunks as one JSON file, for the workflow's args."""
import csv, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
rows = list(csv.DictReader((HERE / "facts.tsv").open(encoding="utf-8"), delimiter="\t"))
size = int(sys.argv[1]) if len(sys.argv) > 1 else 46
lines = [f"{r['table']} [{r['tags']}] :: {r['summary']} :: {r['facts']}" for r in rows]
chunks = [lines[i::(len(lines) + size - 1) // size] for i in range((len(lines) + size - 1) // size)]
(HERE / "chunks.json").write_text(json.dumps(chunks), encoding="utf-8")
print(len(lines), "tables in", len(chunks), "chunks of", max(map(len, chunks)))
