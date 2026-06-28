#!/usr/bin/env python3
"""Second keyless tranche for the 75-issue coverage build: a spread of Our World
in Data indicators (clean CC-BY grapher CSVs), three Harvard Dataverse datasets,
and the Vera incarceration file (renamed in-repo). Per-source error isolation;
all-TEXT landing, snapshot-replace, logged + registered with inline metadata.

    python scripts/issue_batch_load2.py --run            # load all
    python scripts/issue_batch_load2.py --run sid1 sid2   # subset
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import uuid
from pathlib import Path

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))
try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass

import ingest        # noqa: E402
import register      # noqa: E402
import snow          # noqa: E402
from config import settings  # noqa: E402

UA = {"User-Agent": "Ripple-Library/1.0 (data onboarding; w.rogers9999@gmail.com)"}
MAX_BYTES = 260_000_000
DV = "https://dataverse.harvard.edu"


def _owid(slug):
    return f"https://ourworldindata.org/grapher/{slug}.csv?csvType=full"


# each: dict(sid, url|doi, fmt, name, publisher, issue, keys, license, unit, cadence)
SPECS = [
    dict(sid="xc_owid_co2", url=_owid("annual-co2-emissions-per-country"), fmt="csv",
         name="OWID — Annual CO2 emissions by country", issue="#24 climate", keys=["COUNTRY"]),
    dict(sid="xc_owid_temp_anomaly", url=_owid("temperature-anomaly"), fmt="csv",
         name="OWID — Global temperature anomaly", issue="#24 climate", keys=["COUNTRY"]),
    dict(sid="xc_owid_gini", url=_owid("economic-inequality-gini-index"), fmt="csv",
         name="OWID — Gini index (income inequality)", issue="#15 inequality", keys=["COUNTRY"]),
    dict(sid="xc_owid_refugees", url=_owid("refugee-population-by-country-or-territory-of-origin"), fmt="csv",
         name="OWID — Refugee population by country of origin", issue="#21 refugees", keys=["COUNTRY"]),
    dict(sid="xc_owid_fertility", url=_owid("children-born-per-woman"), fmt="csv",
         name="OWID — Fertility rate (children per woman)", issue="#47 aging", keys=["COUNTRY"]),
    dict(sid="xc_owid_cpi", url=_owid("ti-corruption-perception-index"), fmt="csv",
         name="OWID — Corruption Perceptions Index (TI)", issue="#38 corruption", keys=["COUNTRY"]),
    dict(sid="xc_owid_terrorism_deaths", url=_owid("terrorism-deaths"), fmt="csv",
         name="OWID — Terrorism deaths", issue="#39 extremism", keys=["COUNTRY"]),
    dict(sid="xc_owid_fossil_share", url=_owid("fossil-fuels-share-energy"), fmt="csv",
         name="OWID — Fossil fuel share of primary energy", issue="#28 fossil fuels", keys=["COUNTRY"]),
    dict(sid="xc_owid_life_expectancy", url=_owid("life-expectancy"), fmt="csv",
         name="OWID — Life expectancy", issue="#47 aging", keys=["COUNTRY"]),
    dict(sid="xc_owid_homicide", url=_owid("homicide-rate-unodc"), fmt="csv",
         name="OWID — Homicide rate (UNODC)", issue="#48 crime", keys=["COUNTRY"]),
    dict(sid="xc_vera_incarceration_trends",
         url="https://raw.githubusercontent.com/vera-institute/incarceration-trends/main/incarceration_trends_county.csv",
         fmt="csv", name="Vera Institute — Incarceration Trends (county)", publisher="Vera Institute of Justice",
         issue="#53 mass incarceration", keys=["FIPS", "COUNTRY"], license="ODC-BY"),
    dict(sid="intl_leiden_russian_ops_europe", doi="10.7910/DVN/TQ0FMQ", fmt="dataverse",
         name="Russian Operations Against Europe Dataset", publisher="Harvard Dataverse (Schuurman et al.)",
         issue="#4 Russia-NATO hybrid war", keys=["COUNTRY", "NAME"]),
    dict(sid="intl_voeten_unga_votes", doi="10.7910/DVN/LEJUQZ", fmt="dataverse",
         name="United Nations General Assembly Voting Data (Voeten)", publisher="Harvard Dataverse (Voeten)",
         issue="#11 multilateralism", keys=["COUNTRY"]),
    dict(sid="st_cannabis_policy_bundles", doi="10.7910/DVN/2SB7ZF", fmt="dataverse",
         name="US State Cannabis Policy Bundles Dataset", publisher="Harvard Dataverse",
         issue="#74 federalism", keys=["FIPS", "NAME"]),
    # --- tranche 4 (CDC Socrata + VA appendices) ---
    dict(sid="fed_cdc_overdose", url="https://data.cdc.gov/resource/xkb8-kh2a.csv?$limit=2000000", fmt="csv",
         name="CDC VSRR Provisional Drug Overdose Death Counts", publisher="CDC NCHS",
         issue="#48 drug deaths", keys=["FIPS", "NAME"], license="Public domain (US Gov)"),
    dict(sid="fed_cdc_drug_poisoning_county", url="https://data.cdc.gov/resource/pbkm-d27e.csv?$limit=2000000", fmt="csv",
         name="NCHS Drug Poisoning Mortality by County", publisher="CDC NCHS",
         issue="#48 drug deaths", keys=["FIPS"], license="Public domain (US Gov)"),
    dict(sid="fed_va_suicide_appendix",
         url="https://www.mentalhealth.va.gov/MENTALHEALTH/docs/data-sheets/2025/National_Suicide_Data_Appendix_2021-2023_508.xlsx",
         fmt="xlsx", name="VA National Veteran Suicide Data Appendix 2021-2023",
         publisher="US Dept of Veterans Affairs", issue="#70 veteran suicide", keys=["NAME"], license="Public domain (US Gov)"),
    dict(sid="fed_va_allcause_mortality",
         url="https://www.mentalhealth.va.gov/MENTALHEALTH/docs/data-sheets/2025/All-Cause_Mortality_Data_Appendix_2018-2023_508.xlsx",
         fmt="xlsx", name="VA All-Cause Mortality Data Appendix 2018-2023",
         publisher="US Dept of Veterans Affairs", issue="#70 veteran care", keys=["NAME"], license="Public domain (US Gov)"),
    # --- tranche 5 (more CDC Socrata, keyless public-domain) ---
    dict(sid="fed_cdc_suicide_rates", url="https://data.cdc.gov/resource/9j2v-jamp.csv?$limit=2000000", fmt="csv",
         name="CDC NCHS Death rates for suicide by demographics", publisher="CDC NCHS",
         issue="#31 mental health", keys=["NAME"], license="Public domain (US Gov)"),
    dict(sid="fed_cdc_anxiety_depression", url="https://data.cdc.gov/resource/8pt5-q6wp.csv?$limit=2000000", fmt="csv",
         name="CDC Indicators of Anxiety or Depression", publisher="CDC NCHS",
         issue="#31 mental health", keys=["NAME"], license="Public domain (US Gov)"),
    dict(sid="fed_cdc_injury_violence_county", url="https://data.cdc.gov/resource/psx4-wq38.csv?$limit=2000000", fmt="csv",
         name="CDC Mapping Injury, Overdose, and Violence - County", publisher="CDC",
         issue="#51 gun violence", keys=["FIPS"], license="Public domain (US Gov)"),
    dict(sid="fed_cdc_health_insurance", url="https://data.cdc.gov/resource/jb9g-gnvr.csv?$limit=2000000", fmt="csv",
         name="CDC Indicators of Health Insurance Coverage", publisher="CDC NCHS",
         issue="#32 healthcare access", keys=["NAME"], license="Public domain (US Gov)"),
]


def _fetch(url):
    r = requests.get(url, headers=UA, timeout=300, stream=True)
    r.raise_for_status()
    chunks, total = [], 0
    for c in r.iter_content(1 << 20):
        chunks.append(c); total += len(c)
        if total > MAX_BYTES:
            raise RuntimeError(f"exceeds {MAX_BYTES//1_000_000}MB cap")
    return b"".join(chunks), (r.headers.get("content-disposition", "") or "")


def _df_from_bytes(content, fname):
    fl = fname.lower()
    if fl.endswith(".dta"):
        return pd.read_stata(io.BytesIO(content), convert_categoricals=False).astype(str)
    if fl.endswith((".xlsx", ".xls")):
        sheets = pd.read_excel(io.BytesIO(content), sheet_name=None, dtype=str)
        name = max(sheets, key=lambda s: len(sheets[s]))
        return sheets[name].fillna("")
    sep = "\t" if fl.endswith((".tab", ".tsv")) else ","
    return pd.read_csv(io.BytesIO(content), dtype=str, sep=sep, keep_default_na=False,
                       low_memory=False, encoding_errors="replace")


def _fetch_dataverse(doi):
    meta = requests.get(f"{DV}/api/datasets/:persistentId/?persistentId=doi:{doi}",
                        headers=UA, timeout=120).json()
    files = meta["data"]["latestVersion"]["files"]
    def score(f):
        df = f.get("dataFile", {})
        fn = (df.get("filename") or f.get("label") or "").lower()
        tab = fn.endswith((".csv", ".tab", ".tsv", ".xlsx", ".xls", ".dta"))
        return (tab, df.get("filesize", 0))
    files = [f for f in files if score(f)[0]]
    if not files:
        raise RuntimeError("no tabular file in dataset")
    f = max(files, key=lambda x: score(x)[1])
    df = f["dataFile"]; fid = df["id"]; fname = df.get("filename") or f.get("label") or "file.tab"
    url = f"{DV}/api/access/datafile/{fid}?format=original"
    content, _ = _fetch(url)
    return _df_from_bytes(content, fname), url, fname


def _juris(sid):
    return {"fed": "federal", "intl": "international", "xc": "cross-cutting",
            "st": "state", "loc": "local"}.get(sid.split("_", 1)[0], "cross-cutting")


def _register(conn, s, rows, url):
    cfg = {
        "source_id": s["sid"], "name": s["name"][:200],
        "publisher": s.get("publisher", "Our World in Data")[:200], "url": url,
        "description": f"{s['name']} — issue {s.get('issue','')}."[:900],
        "jurisdiction": _juris(s["sid"]), "category": "Issue-coverage", "subcategory": s.get("issue", "")[:80],
        "unit_of_observation": s.get("unit", "one row = one entity-year observation")[:200],
        "geographic_scope": "", "access_method": "bulk_download", "format": s["fmt"],
        "auth": {"type": "none"}, "cost": "free", "update_cadence": s.get("cadence", "")[:80],
        "volume": f"{rows:,} rows", "license_terms": s.get("license", "CC BY 4.0")[:200],
        "join_keys": ", ".join(s.get("keys", []))[:200],
        "accountability_relevance": f"Covers issue {s.get('issue','')}."[:300],
        "priority_tier": "2", "landing_table": s["sid"].upper(),
        "notes": "Loaded by scripts/issue_batch_load2.py (75-issue tranche 2).",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def _load_one(conn, s):
    try:
        if s["fmt"] == "dataverse":
            df, url, _ = _fetch_dataverse(s["doi"])
        else:
            content, _ = _fetch(s["url"]); url = s["url"]
            df = _df_from_bytes(content, s["url"].split("?")[0])
        if df.empty:
            return False, "empty"
        df.columns = [str(c) if str(c).strip() and not str(c).startswith("Unnamed") else f"col_{i}"
                      for i, c in enumerate(df.columns)]
        started = ingest._utcnow(); run_id = str(uuid.uuid4())
        sha = hashlib.sha256(df.to_csv(index=False).encode("utf-8", "replace")).hexdigest()
        from snowflake.connector.pandas_tools import write_pandas
        out = ingest._stringify(df)
        out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
        out[ingest.META_SOURCE_RUN_ID] = run_id
        out[ingest.META_SRC_SHA256] = sha
        out.columns = [ingest._sf_col(c) for c in out.columns]
        ok, _c, _n, _ = write_pandas(conn, out, table_name=s["sid"].upper(),
                                     database=settings.raw_database, schema=settings.raw_schema,
                                     auto_create_table=True, overwrite=True, quote_identifiers=False)
        if not ok:
            return False, "write_pandas failed"
        ended = ingest._utcnow()
        dens = ingest.assess_density(df)
        status = "success" if dens.get("populated_fraction", 0) >= 0.01 else "empty"
        ingest._log_run(conn, s["sid"], run_id, status, len(df), None, sha, url, started, ended,
                        f"tranche2; {len(df):,} rows x {len(df.columns)} cols; density {dens.get('populated_fraction')}")
        _register(conn, s, len(df), url)
        return True, f"{len(df):,} rows x {len(df.columns)} cols ({status})"
    except Exception as ex:  # noqa: BLE001
        return False, f"{type(ex).__name__}: {str(ex)[:120]}"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("sids", nargs="*")
    args = ap.parse_args(argv)
    specs = [s for s in SPECS if not args.sids or s["sid"] in args.sids]
    if not args.run:
        for s in specs:
            print(f"  {s['sid']:34} {s['fmt']:10} {s.get('issue','')}")
        print("\nadd --run to load.")
        return 0
    conn = snow.connect(); ok = fail = 0
    try:
        snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{settings.raw_database}"."{settings.raw_schema}"')
        for s in specs:
            good, msg = _load_one(conn, s)
            print(f"  {'✓' if good else '✗'} {s['sid']:34} {msg}", flush=True)
            ok += good; fail += (not good)
    finally:
        conn.close()
    print(f"\nDONE: {ok} loaded, {fail} failed", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
