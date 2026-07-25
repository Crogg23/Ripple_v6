#!/usr/bin/env python3
"""Write the analytical (non-PORTAL) source list to scripts/analytical_sources.txt"""
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "connect"))
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:
    pass

import snow

conn = snow.connect()
cur = conn.cursor()
cur.execute(
    "SELECT TABLE_NAME FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES "
    "WHERE TABLE_SCHEMA = 'LANDING' AND TABLE_NAME NOT LIKE 'PORTAL_%' "
    "ORDER BY TABLE_NAME"
)
tables = [r[0] for r in cur.fetchall()]
out = _REPO / "scripts" / "analytical_sources.txt"
out.write_text("\n".join(tables), encoding="utf-8")
print(f"Wrote {len(tables)} sources to {out}")
conn.close()
