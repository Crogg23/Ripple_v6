"""
One pin per table's top states, built from real warehouse value counts.

Source: reports/location_index/location_values_2026-08-30.json
  -- an actual query pass over every geo column (fill rate, distinct count,
     top values by row count). Not a name-scan.

Mechanism: for every table with a usable STATE column, take its top-5
states by row count, place a pin at that state's centroid, jitter it
so many tables in the same state don't stack into one dot. Pin size
carries the real row count behind it.
"""
import json
import random

import pandas as pd

SRC = "reports/location_index/location_values_2026-08-30.json"
OUT = "reports/location_index/geo_pinboard.csv"

STATE_CENTROIDS = {
    "AL": (32.8, -86.8), "AK": (64.2, -149.5), "AZ": (34.2, -111.7),
    "AR": (34.9, -92.4), "CA": (37.2, -119.7), "CO": (39.0, -105.5),
    "CT": (41.6, -72.7), "DE": (39.0, -75.5), "FL": (28.6, -82.4),
    "GA": (32.6, -83.4), "HI": (20.3, -156.4), "ID": (44.4, -114.6),
    "IL": (40.0, -89.2), "IN": (39.9, -86.3), "IA": (42.0, -93.5),
    "KS": (38.5, -98.4), "KY": (37.5, -85.3), "LA": (31.0, -92.0),
    "ME": (45.4, -69.2), "MD": (39.0, -76.7), "MA": (42.3, -71.8),
    "MI": (44.3, -85.4), "MN": (46.3, -94.3), "MS": (32.7, -89.7),
    "MO": (38.5, -92.5), "MT": (47.0, -109.6), "NE": (41.5, -99.8),
    "NV": (39.3, -116.6), "NH": (43.7, -71.6), "NJ": (40.1, -74.7),
    "NM": (34.4, -106.1), "NY": (42.9, -75.5), "NC": (35.6, -79.4),
    "ND": (47.5, -100.5), "OH": (40.4, -82.8), "OK": (35.6, -97.5),
    "OR": (44.0, -120.6), "PA": (40.9, -77.7), "RI": (41.7, -71.5),
    "SC": (33.9, -80.9), "SD": (44.4, -100.2), "TN": (35.9, -86.4),
    "TX": (31.5, -99.3), "UT": (39.3, -111.7), "VT": (44.0, -72.7),
    "VA": (37.5, -78.8), "WA": (47.4, -120.5), "WV": (38.6, -80.6),
    "WI": (44.6, -89.9), "WY": (43.0, -107.5), "DC": (38.9, -77.0),
}

random.seed(6)


def jitter(lat, lon):
    return lat + random.uniform(-1.2, 1.2), lon + random.uniform(-1.4, 1.4)


def main():
    tables = json.load(open(SRC, encoding="utf-8"))
    rows = []
    for key, t in tables.items():
        for col in t["columns"]:
            if col.get("kind") != "state" or not col.get("top"):
                continue
            for state, count in col["top"]:
                state = state.strip().upper()
                if state not in STATE_CENTROIDS:
                    continue
                lat, lon = jitter(*STATE_CENTROIDS[state])
                rows.append({
                    "schema": t["schema"],
                    "table": t["table"],
                    "column": col["column"],
                    "state": state,
                    "row_count": count,
                    "lat": lat,
                    "lon": lon,
                })
            break  # one state column per table is enough to place it

    df = pd.DataFrame(rows)
    df.to_csv(OUT, index=False)
    print(f"{len(df)} pins across {df['table'].nunique()} tables -> {OUT}")


if __name__ == "__main__":
    main()
