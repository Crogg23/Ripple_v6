"""
build_from_cache.py — Build the explorer HTML from cached query results.
Run this when you already have the cached data but can't connect to Snowflake.
"""
import json
from pathlib import Path

CACHE_DIR = Path(r"c:\Users\wroge\.snowflake\cortex\cache\tool_outputs\3982792f-8af1-4174-a24b-876822493b60")
VENDOR_DIR = Path(r"c:\Code\Ripple_v6\reports\vendor")
OUTPUT = Path(r"c:\Code\Ripple_v6\reports\the_library_explorer.html")


def read_jsonl(filename):
    """Read a JSONL cache file: line 0 = {columns, query}, lines 1+ = [row arrays]."""
    path = CACHE_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        meta = json.loads(f.readline())
        cols = meta["columns"]
        rows = []
        for line in f:
            line = line.strip()
            if line:
                row_data = json.loads(line)
                rows.append(dict(zip(cols, row_data)))
    return rows


def main():
    print("Reading cached data...")
    nodes = read_jsonl("query_003.jsonl")
    edges = read_jsonl("query_001.jsonl")
    columns = read_jsonl("query_002.jsonl")
    print(f"  Nodes: {len(nodes)}, Edges: {len(edges)}, Columns: {len(columns)}")

    print("Reading vendor JS...")
    cytoscape_js = (VENDOR_DIR / "cytoscape.min.js").read_text(encoding="utf-8")
    cosebilkent_js = (VENDOR_DIR / "cytoscape-cose-bilkent.js").read_text(encoding="utf-8")

    # Build data blob
    data = {"nodes": nodes, "edges": edges, "columns": columns}
    data_json = json.dumps(data, default=str, ensure_ascii=False)

    # Stats
    schemas = sorted(set(n["FRIENDLY_SCHEMA"] for n in nodes))
    total_cols = len(columns)
    entity_keys = {"NPI", "EIN", "BIOGUIDE", "CIK", "CCN", "CCN~NPI", "DOCKET",
                   "LEI", "ICPSR", "CIK~EIN", "DUNS", "DUNS~UEI", "EIN~UEI", "UEI", "PATENT"}
    entity_edge_count = sum(1 for e in edges if e["KEY"] in entity_keys)

    # Import the HTML template builder from rebuild_explorer
    import sys
    sys.path.insert(0, str(Path(r"c:\Code\Ripple_v6\reports")))
    from rebuild_explorer import build_html
    
    html = build_html(nodes, edges, columns, VENDOR_DIR)
    
    OUTPUT.write_text(html, encoding="utf-8")
    size_mb = OUTPUT.stat().st_size / (1024 * 1024)
    print(f"\nDone! {OUTPUT}")
    print(f"Size: {size_mb:.1f} MB")


if __name__ == "__main__":
    main()
