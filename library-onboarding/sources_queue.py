"""The pre-loaded landscape sweep.

Every source the agent knows how to onboard on day one. ``onboard.py --batch``
walks this list top to bottom, running the 5-checkpoint loop for each source and
recording progress in ``onboarding_log.json`` so an interrupted run can resume.

Each entry carries only what we know *before* recon:
    name        Human-readable source name (also used as the Snowflake schema).
    url         The docs/landing page the recon step reads.
    layer       Which layer of the Library this source belongs to.
    identifiers The cross-source join keys we already expect to find.
"""

SOURCES = [
    # --- US Federal -- Layer 1 ------------------------------------------
    {"name": "FRED", "url": "https://fred.stlouisfed.org/docs/api/fred/", "layer": "us_federal", "identifiers": ["series_id", "FIPS", "country_ISO"]},
    {"name": "USASpending", "url": "https://api.usaspending.gov/docs/endpoints", "layer": "us_federal", "identifiers": ["UEI", "FIPS", "EIN", "NAICS"]},
    {"name": "SEC EDGAR", "url": "https://www.sec.gov/search-filings/edgar-application-programming-interfaces", "layer": "us_federal", "identifiers": ["CIK", "ticker", "ISIN"]},
    {"name": "CMS NPPES", "url": "https://download.cms.gov/nppes/NPI_Files.html", "layer": "us_federal", "identifiers": ["NPI", "FIPS"]},
    {"name": "BEA", "url": "https://apps.bea.gov/api/", "layer": "us_federal", "identifiers": ["FIPS", "MSA", "NAICS"]},
    {"name": "EIA", "url": "https://www.eia.gov/opendata/", "layer": "us_federal", "identifiers": ["FIPS", "EIA_plant_id"]},
    {"name": "FEC", "url": "https://api.open.fec.gov/developers/", "layer": "us_federal", "identifiers": ["FEC_committee_id", "FIPS"]},
    {"name": "IRS 990 via ProPublica", "url": "https://projects.propublica.org/nonprofits/api", "layer": "us_federal", "identifiers": ["EIN"]},
    {"name": "EPA ECHO", "url": "https://echo.epa.gov/tools/web-services", "layer": "us_federal", "identifiers": ["FIPS", "FRS_id", "lat_lon"]},
    {"name": "EPA TRI", "url": "https://www.epa.gov/toxics-release-inventory-tri-program/tri-data-and-tools", "layer": "us_federal", "identifiers": ["FIPS", "TRI_facility_id", "lat_lon"]},
    {"name": "FDA FAERS", "url": "https://open.fda.gov/apis/drug/event/", "layer": "us_federal", "identifiers": ["NDC", "NPI"]},
    {"name": "USPTO Bulk Data", "url": "https://bulkdata.uspto.gov", "layer": "us_federal", "identifiers": ["patent_number", "CIK", "EIN"]},
    {"name": "NIH Reporter", "url": "https://api.reporter.nih.gov", "layer": "us_federal", "identifiers": ["NPI", "EIN", "FIPS"]},
    {"name": "CourtListener", "url": "https://www.courtlistener.com/help/api/", "layer": "us_federal", "identifiers": ["PACER_case_id", "docket_id"]},
    {"name": "NCES", "url": "https://nces.ed.gov/datatools/", "layer": "us_federal", "identifiers": ["NCES_school_id", "FIPS"]},
    {"name": "BJS NIBRS", "url": "https://bjs.ojp.gov/data-collection/national-incident-based-reporting-system-nibrs", "layer": "us_federal", "identifiers": ["FIPS", "ORI"]},
    {"name": "SAM.gov", "url": "https://open.gsa.gov/api/sam-entity-extracts-api/", "layer": "us_federal", "identifiers": ["UEI", "CAGE", "EIN"]},
    {"name": "HUD", "url": "https://www.huduser.gov/portal/datasets/", "layer": "us_federal", "identifiers": ["FIPS", "census_tract"]},

    # --- International -- Layer 2 ---------------------------------------
    {"name": "GDELT", "url": "https://www.gdeltproject.org/data.html", "layer": "international", "identifiers": ["lat_lon", "country_ISO", "FIPS"]},
    {"name": "World Bank", "url": "https://datahelpdesk.worldbank.org/knowledgebase/articles/889386", "layer": "international", "identifiers": ["country_ISO", "WB_indicator_code"]},
    {"name": "IMF Data", "url": "https://www.imf.org/en/Data", "layer": "international", "identifiers": ["country_ISO"]},
    {"name": "OECD", "url": "https://data-explorer.oecd.org", "layer": "international", "identifiers": ["country_ISO"]},
    {"name": "WHO GHO", "url": "https://www.who.int/data/gho/info/gho-odata-api", "layer": "international", "identifiers": ["country_ISO", "ICD10"]},
    {"name": "ACLED", "url": "https://acleddata.com/acleddatanew/wp-content/uploads/dlm_uploads/2021/11/ACLED_API-User-Guide_2021.pdf", "layer": "international", "identifiers": ["lat_lon", "country_ISO"]},
    {"name": "OpenSanctions", "url": "https://www.opensanctions.org/api/", "layer": "international", "identifiers": ["LEI", "OpenCorp_id"]},
    {"name": "Global Fishing Watch", "url": "https://globalfishingwatch.org/our-apis/", "layer": "international", "identifiers": ["MMSI", "IMO", "lat_lon"]},

    # --- Corporate / Entity -- Layer 3 ----------------------------------
    {"name": "OpenCorporates", "url": "https://api.opencorporates.com/documentation/API-Reference", "layer": "corporate", "identifiers": ["OpenCorp_id", "LEI", "jurisdiction_code"]},
    {"name": "GLEIF LEI", "url": "https://www.gleif.org/en/lei-data/gleif-api", "layer": "corporate", "identifiers": ["LEI", "ISIN", "BIC", "MIC"]},
    {"name": "OpenOwnership BODS", "url": "https://register.openownership.org/api", "layer": "corporate", "identifiers": ["LEI", "OpenCorp_id"]},
    {"name": "ICIJ Offshore Leaks", "url": "https://offshoreleaks.icij.org/pages/database", "layer": "corporate", "identifiers": ["ICIJ_node_id", "jurisdiction"]},

    # --- Investigative / NGO -- Layer 4 ---------------------------------
    {"name": "ProPublica Congress API", "url": "https://projects.propublica.org/api-docs/congress-api/", "layer": "investigative", "identifiers": ["bioguide_id"]},
    {"name": "OpenSecrets", "url": "https://www.opensecrets.org/api", "layer": "investigative", "identifiers": ["FEC_committee_id", "CRP_id"]},
    {"name": "MuckRock", "url": "https://www.muckrock.com/api/", "layer": "investigative", "identifiers": []},

    # --- Geospatial -- Layer 5 ------------------------------------------
    {"name": "Census TIGER", "url": "https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html", "layer": "geospatial", "identifiers": ["FIPS", "GEOID", "lat_lon"]},
    {"name": "OpenStreetMap Overpass", "url": "https://overpass-api.de/api/interpreter", "layer": "geospatial", "identifiers": ["OSM_id", "lat_lon"]},
    {"name": "USGS National Map", "url": "https://apps.nationalmap.gov/services/", "layer": "geospatial", "identifiers": ["lat_lon", "FIPS", "HUC"]},
    {"name": "NASA Earthdata", "url": "https://earthdata.nasa.gov/engage/open-data-services-and-software/api", "layer": "geospatial", "identifiers": ["lat_lon", "tile_id"]},
]


def find_source(name_or_url: str):
    """Return the queue entry matching a name (case-insensitive) or URL."""
    needle = name_or_url.strip().lower()
    for src in SOURCES:
        if src["name"].lower() == needle or src["url"].lower() == needle:
            return src
    return None
