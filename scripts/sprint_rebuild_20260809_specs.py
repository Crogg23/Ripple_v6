"""Rebuild specs for the 2026-08-09 dead-source resurrection sprint (Chris: Option 1).

Five of the seven approved rebuilds are plain bulk CSV/zip sources, so they ride
scripts/bridge_fuel_load.py unchanged. (The other two: VA mortality xlsx ->
scripts/va_mortality_load.py, CDC WONDER XML API -> scripts/cdc_wonder_load.py;
FBI CDE waits on Chris's api.data.gov key.)

Every URL below was live-verified 2026-08-09 (HTTP 200, correct content type):
  - FAA aircraft registry zip: 73MB, MASTER.txt member (replaces dead
    fed_faa_data_portal, which had scraped the faa.gov/data nav page)
  - Irish CRO companies bulk (CKAN resource URL resolved via package_show;
    resurrects intl_ie_cro, whose old scrape landed a cookie-consent table)
  - FRA Form 54 / 57 / 55a via Socrata CSV export on data.transportation.gov
    (replaces dead fed_fra_safety, which hit the retired SOAP-era pilot pages)

    python scripts/bridge_fuel_load.py --spec fed_faa_aircraft_registry --run
    python scripts/bridge_fuel_load.py --spec all --run   # skips already-landed
"""

SPECS = [
    {
        "source_id": "fed_cdc_leading_causes_state",
        "name": "NCHS — Leading Causes of Death by State (1999-2017)",
        "publisher": "CDC — National Center for Health Statistics",
        "url": "https://data.cdc.gov/d/bi63-dtpu",
        "download_url": "https://data.cdc.gov/api/views/bi63-dtpu/rows.csv?accessType=DOWNLOAD",
        "kind": "csv",
        "join_keys": "STATE, YEAR",
        "category": "Health",
        "subcategory": "Mortality",
        "unit_of_observation": "one row = one state x year x leading cause of death",
        "update_cadence": "static (1999-2017)",
        "accountability_relevance": "State-level who-dies-of-what geography — the state "
                                    "companion to fed_cdc_wonder, whose API is national-only by CDC policy.",
        "priority_tier": "1",
        "notes": "Added 2026-08-09: CDC WONDER's API rejects any state grouping, so state "
                 "mortality geography lands from this NCHS Socrata dataset instead.",
    },
    {
        "source_id": "fed_faa_aircraft_registry",
        "name": "FAA Aircraft Registry — Releasable Master File",
        "publisher": "FAA — Civil Aviation Registry",
        "url": "https://www.faa.gov/licenses_certificates/aircraft_certification/aircraft_registry/releasable_aircraft_download",
        "download_url": "https://registry.faa.gov/database/ReleasableAircraft.zip",
        "kind": "zip_csv",
        "member": r"MASTER",
        "chunked": True,
        "chunk_rows": 250_000,
        "join_keys": "N_NUMBER, NAME, ZIP",
        "category": "Transportation",
        "subcategory": "Aircraft Ownership",
        "unit_of_observation": "one row = one registered US civil aircraft",
        "update_cadence": "daily",
        "accountability_relevance": "Joins aircraft to registered owners (companies and "
                                    "people, with addresses) — asset trail for entity mapping.",
        "priority_tier": "2",
        "notes": "Rebuild of dead fed_faa_data_portal (nav-page scrape). MASTER.txt member "
                 "of ReleasableAircraft.zip; endpoint already verified by the 2026-08-07 recon.",
    },
    {
        "source_id": "intl_ie_cro",
        "name": "Irish Companies Registration Office — Companies (bulk)",
        "publisher": "Companies Registration Office (Ireland)",
        "url": "https://opendata.cro.ie/dataset/companies",
        "download_url": "https://opendata.cro.ie/dataset/bf6f837d-0946-4c14-9a99-82cd6980c121/resource/3fef41bc-b8f4-4b10-8434-ce51c29b1bba/download/companies.csv.zip",
        "kind": "zip_csv",
        "chunked": True,
        "chunk_rows": 250_000,
        "jurisdiction": "IE",
        "geographic_scope": "Ireland",
        "join_keys": "COMPANY_NUM, NAME",
        "category": "Corporate Registry",
        "subcategory": "Companies",
        "unit_of_observation": "one row = one Irish-registered company (incl. dissolved)",
        "update_cadence": "daily",
        "license_terms": "CC-BY 4.0 (CRO Open Data)",
        "accountability_relevance": "Irish shells are a standard US-adjacent ownership hop; "
                                    "registry incl. dissolved companies supports shell tracing.",
        "priority_tier": "3",
        "notes": "Resurrects intl_ie_cro (old scrape landed the portal cookie banner). "
                 "Official CRO Open Data bulk zip, resolved via CKAN package_show 2026-08-09.",
    },
    {
        "source_id": "fed_fra_equipment_accidents",
        "name": "FRA Rail Equipment Accident/Incident Data (Form 54)",
        "publisher": "FRA — Office of Safety Analysis",
        "url": "https://data.transportation.gov/d/85tf-25kj",
        "download_url": "https://data.transportation.gov/api/views/85tf-25kj/rows.csv?accessType=DOWNLOAD",
        "kind": "csv",
        "chunked": True,
        "chunk_rows": 100_000,
        "join_keys": "RAILROAD, FIPS, ZIP",
        "category": "Transportation",
        "subcategory": "Rail Safety",
        "unit_of_observation": "one row = one reported rail equipment accident/incident",
        "update_cadence": "monthly",
        "accountability_relevance": "Train accidents with deaths, injuries, damage and "
                                    "location — direct harm events attributable to named railroads.",
        "priority_tier": "1",
        "notes": "Rebuild of dead fed_fra_safety (SOAP-era pilot pages). Socrata CSV export, "
                 "dataset id 85tf-25kj, verified 2026-08-09.",
    },
    {
        "source_id": "fed_fra_crossing_incidents",
        "name": "FRA Highway-Rail Grade Crossing Incident Data (Form 57)",
        "publisher": "FRA — Office of Safety Analysis",
        "url": "https://data.transportation.gov/d/7wn6-i5b9",
        "download_url": "https://data.transportation.gov/api/views/7wn6-i5b9/rows.csv?accessType=DOWNLOAD",
        "kind": "csv",
        "chunked": True,
        "chunk_rows": 100_000,
        "join_keys": "RAILROAD, CROSSING_ID, FIPS",
        "category": "Transportation",
        "subcategory": "Rail Safety",
        "unit_of_observation": "one row = one highway-rail grade crossing incident",
        "update_cadence": "monthly",
        "accountability_relevance": "Grade-crossing collisions (many fatal) by railroad and "
                                    "crossing — pairs with the crossing inventory for neglected-crossing patterns.",
        "priority_tier": "1",
        "notes": "Rebuild of dead fed_fra_safety. Socrata CSV export, id 7wn6-i5b9, verified 2026-08-09.",
    },
    {
        "source_id": "fed_fra_casualties",
        "name": "FRA Injury/Illness Summary — Casualty Data (Form 55a)",
        "publisher": "FRA — Office of Safety Analysis",
        "url": "https://data.transportation.gov/d/rash-pd2d",
        "download_url": "https://data.transportation.gov/api/views/rash-pd2d/rows.csv?accessType=DOWNLOAD",
        "kind": "csv",
        "chunked": True,
        "chunk_rows": 100_000,
        "join_keys": "RAILROAD, FIPS",
        "category": "Transportation",
        "subcategory": "Rail Safety",
        "unit_of_observation": "one row = one reported rail-related casualty (injury/illness/death)",
        "update_cadence": "monthly",
        "accountability_relevance": "Person-level rail casualties (workers and public) by "
                                    "railroad — the who-gets-hurt ledger behind the accident counts.",
        "priority_tier": "1",
        "notes": "Rebuild of dead fed_fra_safety. Socrata CSV export, id rash-pd2d, verified 2026-08-09.",
    },
]
