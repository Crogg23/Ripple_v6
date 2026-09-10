"""CMS year-series specs — the depth pour, 2026-09-09.

Why: the four big per-provider CMS files on disk are ONE data year each
(Part D by drug = DY2022, Part B by provider and by service = DY2024). Every
"before / after / rise" question on doctors, drugs and money needs a year slider.
CMS publishes every year 2013-2024 as a direct CSV. This lands all twelve, for
all four files, one table per year, suffixed _DYyyyy.

Row-count reality (Range probe 2026-09-09, 2013 files):
  Part D by provider and drug   3.4 GB  ~25M rows/yr   (the big one)
  Part B by provider and service 2.9 GB  ~10M rows/yr
  Part D by provider             0.56 GB ~1.3M rows/yr
  Part B by provider             0.33 GB ~1.2M rows/yr

Existing unsuffixed tables are NOT touched:
  FED_CMS_PARTD_PRESCRIBER_DRUG                                 = DY2022
  FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER    = DY2024
  FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI = DY2024
Those years are landed again here, suffixed, so the series is uniform.

URLs come from https://data.cms.gov/data.json (distribution.downloadURL,
mediaType text/csv), pulled 2026-09-09. They are dated paths and may rotate;
regenerate with the block at the bottom if one 404s.

    python scripts/bridge_fuel_load.py --spec FED_CMS_PARTD_PRESCRIBER_DY2013 --run
    python scripts/bridge_fuel_load.py --list | grep _DY20
"""

_YEARS = [str(y) for y in range(2013, 2025)]

_URLS = {
    "PARTD_PRESCRIBER_DRUG": {
        "2024": "https://data.cms.gov/sites/default/files/2026-05/0ae165f4-eb44-495d-8cac-67f4571b6b83/MUP_DPR_RY26_P04_V10_DY24_NPIBN.csv",
        "2023": "https://data.cms.gov/sites/default/files/2025-04/0d5915ce-002c-4d87-bde8-24ffb08bb6cc/MUP_DPR_RY25_P04_V10_DY23_NPIBN.csv",
        "2022": "https://data.cms.gov/sites/default/files/2024-05/18f82097-61a6-4889-9941-9a0b6ad7523c/MUP_DPR_RY24_P04_V10_DY22_NPIBN.csv",
        "2021": "https://data.cms.gov/sites/default/files/2024-05/43359391-e7fa-40b9-9bd4-5dc295e18712/MUP_DPR_RY24_P04_V10_DY21_NPIBN.csv",
        "2020": "https://data.cms.gov/sites/default/files/2024-05/75fecc51-c9e8-4904-b570-9da9dc101721/MUP_DPR_RY24_P04_V10_DY20_NPIBN.csv",
        "2019": "https://data.cms.gov/sites/default/files/2024-05/129e7c21-d492-425b-be03-d2e59d933ab6/MUP_DPR_RY24_P04_V10_DY19_NPIBN.csv",
        "2018": "https://data.cms.gov/sites/default/files/2024-05/be3019b4-1164-4b40-af5d-cab40847d222/MUP_DPR_RY24_P04_V10_DY18_NPIBN.csv",
        "2017": "https://data.cms.gov/sites/default/files/2024-05/d9d685a0-dc49-4da5-9416-4cf3e6349296/MUP_DPR_RY24_P04_V10_DY17_NPIBN.csv",
        "2016": "https://data.cms.gov/sites/default/files/2024-05/67c457c6-b62d-424f-ad85-2bb8117c928d/MUP_DPR_RY24_P04_V10_DY16_NPIBN.csv",
        "2015": "https://data.cms.gov/sites/default/files/2024-05/bc1caf7f-dcbb-4258-b243-ee3666b6a20b/MUP_DPR_RY24_P04_V10_DY15_NPIBN.csv",
        "2014": "https://data.cms.gov/sites/default/files/2024-05/06e87540-68a5-4a10-bf9c-a0521dc4ebed/MUP_DPR_RY24_P04_V10_DY14_NPIBN.csv",
        "2013": "https://data.cms.gov/sites/default/files/2024-05/5fb694b1-2ec5-4e00-8efe-14161bdbdbea/MUP_DPR_RY24_P04_V10_DY13_NPIBN.csv",
    },
    "PARTD_PRESCRIBER": {
        "2024": "https://data.cms.gov/sites/default/files/2026-08/373e45e5-33ec-452c-9302-a4bdbc203459/mup_dpr_ry26_p04_v20_dy24_npi.csv",
        "2023": "https://data.cms.gov/sites/default/files/2026-08/7f74c86e-ca81-4255-8951-3275c4361241/mup_dpr_ry25_p04_v20_dy23_npi.csv",
        "2022": "https://data.cms.gov/sites/default/files/2026-08/0cdbfc0d-257d-4eb0-bcc8-71e5462ec320/mup_dpr_ry24_p04_v20_dy22_npi.csv",
        "2021": "https://data.cms.gov/sites/default/files/2026-08/a8cb773f-4a79-42de-b7ad-83da254416bf/mup_dpr_ry23_p04_v20_dy21_npi.csv",
        "2020": "https://data.cms.gov/sites/default/files/2026-08/0df99eb3-9bfe-46ac-8dd0-c5e700781aae/mup_dpr_ry22_p04_v20_dy20_npi.csv",
        "2019": "https://data.cms.gov/sites/default/files/2026-08/d4a0a871-5e6a-4180-8d89-82b56ff08175/mup_dpr_ry21_p04_v20_dy19_npi.csv",
        "2018": "https://data.cms.gov/sites/default/files/2026-08/a4b0ff0a-f869-4a51-9dce-59a5b018a609/mup_dpr_ry21_p04_v20_dy18_npi.csv",
        "2017": "https://data.cms.gov/sites/default/files/2026-08/8a65e4c8-3c6a-48f2-99ba-422987d953af/mup_dpr_ry21_p04_v20_dy17_npi.csv",
        "2016": "https://data.cms.gov/sites/default/files/2026-08/e8255bdf-5e85-425c-9e6c-1cc460ccce51/mup_dpr_ry21_p04_v20_dy16_npi.csv",
        "2015": "https://data.cms.gov/sites/default/files/2026-08/a846e593-06fb-4ed5-9b2f-b5a31acfef82/mup_dpr_ry21_p04_v20_dy15_npi.csv",
        "2014": "https://data.cms.gov/sites/default/files/2026-08/e11a5415-1967-4207-8ae3-329cfe3fedef/mup_dpr_ry21_p04_v20_dy14_npi.csv",
        "2013": "https://data.cms.gov/sites/default/files/2026-08/c39345cb-ea6d-4312-a695-8410b45c92ab/mup_dpr_ry21_p04_v20_dy13_npi.csv",
    },
    "PARTB_PROVIDER_SERVICE": {
        "2024": "https://data.cms.gov/sites/default/files/2026-05/b5ebab5a-f490-418a-9bce-4b9f31419356/PHY_R26_P05_V10_D24_Prov_Svc.csv",
        "2023": "https://data.cms.gov/sites/default/files/2025-04/e3f823f8-db5b-4cc7-ba04-e7ae92b99757/MUP_PHY_R25_P05_V20_D23_Prov_Svc.csv",
        "2022": "https://data.cms.gov/sites/default/files/2025-11/53fb2bae-4913-48dc-a6d4-d8c025906567/MUP_PHY_R25_P05_V20_D22_Prov_Svc.csv",
        "2021": "https://data.cms.gov/sites/default/files/2025-11/bffaf97a-c2ab-4fd7-8718-be90742e3485/MUP_PHY_R25_P05_V20_D21_Prov_Svc.csv",
        "2020": "https://data.cms.gov/sites/default/files/2025-11/d22b18cd-7726-4bf5-8e9c-3e4587c589a1/MUP_PHY_R25_P05_V20_D20_Prov_Svc.csv",
        "2019": "https://data.cms.gov/sites/default/files/2025-11/7befba27-752e-47a8-a76c-6c6d4f74f2e3/MUP_PHY_R25_P04_V20_D19_Prov_Svc.csv",
        "2018": "https://data.cms.gov/sites/default/files/2025-11/5669eafb-f0b3-4dc5-be6d-abc09b480c2e/MUP_PHY_R25_P04_V20_D18_Prov_Svc.csv",
        "2017": "https://data.cms.gov/sites/default/files/2025-11/4623fb40-781e-4eef-860e-b851cd5d10ea/MUP_PHY_R25_P04_V20_D17_Prov_Svc.csv",
        "2016": "https://data.cms.gov/sites/default/files/2025-11/426bf97a-4cb8-47ca-9727-a535d9e8c298/MUP_PHY_R25_P04_V20_D16_Prov_Svc.csv",
        "2015": "https://data.cms.gov/sites/default/files/2025-11/14954ce3-4c43-43df-97e9-2c0437d7b43c/MUP_PHY_R25_P04_V20_D15_Prov_Svc.csv",
        "2014": "https://data.cms.gov/sites/default/files/2025-11/6700f86d-d2e5-4f2d-9dcb-8c30412768ff/MUP_PHY_R25_P04_V20_D14_Prov_Svc.csv",
        "2013": "https://data.cms.gov/sites/default/files/2025-11/bf4231f9-ec7f-4189-afc3-ba5d53b8bd12/MUP_PHY_R25_P04_V20_D13_Prov_Svc.csv",
    },
    "PARTB_PROVIDER": {
        "2024": "https://data.cms.gov/sites/default/files/2026-05/7323ba02-52e7-4a86-b2ce-ad210c25d9aa/MUP_PHY_R26_P05_V10_D24_Prov.csv",
        "2023": "https://data.cms.gov/sites/default/files/2025-04/22edfd1e-d17a-4478-ad6b-92cac2a5a3c4/MUP_PHY_R25_P05_V20_D23_Prov.csv",
        "2022": "https://data.cms.gov/sites/default/files/2025-11/adcd20c5-4534-43cd-8dfa-881ebe7bacfd/MUP_PHY_R25_P07_V20_D22_Prov.csv",
        "2021": "https://data.cms.gov/sites/default/files/2025-11/fc6ea9aa-12f0-4c2f-9909-6c8e06c961cf/MUP_PHY_R25_P07_V20_D21_Prov.csv",
        "2020": "https://data.cms.gov/sites/default/files/2025-11/056e8c6b-7e39-4945-b9a4-52d0a1cbbb9a/MUP_PHY_R25_P07_V20_D20_Prov.csv",
        "2019": "https://data.cms.gov/sites/default/files/2025-11/ac110c46-3429-4f3c-9348-56f0a5312cb8/MUP_PHY_R25_P07_V20_D19_Prov.csv",
        "2018": "https://data.cms.gov/sites/default/files/2025-11/57ea60f2-ef4b-46f2-8778-c7a50fab1737/MUP_PHY_R25_P07_V20_D18_Prov.csv",
        "2017": "https://data.cms.gov/sites/default/files/2025-11/b7e195ce-710d-4584-8293-787ffc38b017/MUP_PHY_R25_P07_V20_D17_Prov.csv",
        "2016": "https://data.cms.gov/sites/default/files/2025-11/e4cd28e1-2d05-4f33-b232-f32b5bebc153/MUP_PHY_R25_P05_V20_D16_Prov.csv",
        "2015": "https://data.cms.gov/sites/default/files/2025-11/efb7e2f9-b903-4f54-b57f-742f436c316f/MUP_PHY_R25_P05_V20_D15_Prov.csv",
        "2014": "https://data.cms.gov/sites/default/files/2025-11/da4b3b2b-1ee2-4e25-b2fe-012b880afd37/MUP_PHY_R25_P05_V20_D14_Prov.csv",
        "2013": "https://data.cms.gov/sites/default/files/2025-11/4fe919a0-94d4-4681-b076-4106f3766eef/MUP_PHY_R25_P05_V20_D13_Prov.csv",
    },
}

_META = {
    "PARTD_PRESCRIBER_DRUG": dict(
        name="CMS Medicare Part D Prescribers by Provider and Drug",
        npi_col="Prscrbr_NPI",
        unit="one row = one prescriber x one drug x one data year",
        why="Prescribing by doctor and drug, every year. The before/after for pharma money, opioid shifts, cost growth.",
        chunk_rows=500_000,
    ),
    "PARTD_PRESCRIBER": dict(
        name="CMS Medicare Part D Prescribers by Provider",
        npi_col="Prscrbr_NPI",
        unit="one row = one prescriber x one data year",
        why="Prescriber totals with ZIP5 and RUCA, every year. Doctor counts by place by year.",
        chunk_rows=500_000,
    ),
    "PARTB_PROVIDER_SERVICE": dict(
        name="CMS Medicare Physician and Other Practitioners by Provider and Service",
        npi_col="Rndrng_NPI",
        unit="one row = one provider x one HCPCS code x place of service x one data year",
        why="Billing by doctor and service, every year. Suppressed under 11 benes (trap 2026-09-05).",
        chunk_rows=500_000,
    ),
    "PARTB_PROVIDER": dict(
        name="CMS Medicare Physician and Other Practitioners by Provider",
        npi_col="Rndrng_NPI",
        unit="one row = one provider x one data year",
        why="Provider totals with ZIP5 and RUCA, every year. The doctor roster with money, by place by year.",
        chunk_rows=500_000,
    ),
}


def _spec(family: str, year: str) -> dict:
    m = _META[family]
    return {
        "source_id": f"FED_CMS_{family}_DY{year}",
        "name": f"{m['name']} DY{year}",
        "publisher": "CMS",
        "url": "https://data.cms.gov/data.json",
        "download_url": _URLS[family][year],
        "kind": "csv",
        "chunked": True,
        "chunk_rows": m["chunk_rows"],
        "loader": "bridge_fuel",
        "key_cols": [{"col": m["npi_col"], "as": "NPI"}],
        "join_keys": "NPI",
        "category": "Health",
        "subcategory": "Medicare Provider Utilization",
        "unit_of_observation": m["unit"],
        "update_cadence": "annual",
        "license_terms": "Public domain (US Gov)",
        "accountability_relevance": m["why"],
        "priority_tier": "1",
        "notes": (f"Data year {year}. Part of the 2013-2024 year series landed 2026-09-09 "
                  f"so the per-provider CMS files carry a year slider. All columns TEXT. "
                  f"Sibling unsuffixed table is a single year; see module docstring."),
    }


SPECS = [_spec(fam, y) for fam in _URLS for y in _YEARS]


# Regenerate _URLS from the CMS catalog if a dated path rotates:
#   import requests, json
#   j = requests.get("https://data.cms.gov/data.json").json()
#   titles = {"Medicare Part D Prescribers - by Provider and Drug": "PARTD_PRESCRIBER_DRUG",
#             "Medicare Part D Prescribers - by Provider": "PARTD_PRESCRIBER",
#             "Medicare Physician & Other Practitioners - by Provider and Service": "PARTB_PROVIDER_SERVICE",
#             "Medicare Physician & Other Practitioners - by Provider": "PARTB_PROVIDER"}
#   for ds in j["dataset"]:
#       if ds["title"] in titles:
#           for d in ds["distribution"]:
#               if d.get("mediaType") == "text/csv":
#                   print(titles[ds["title"]], d["title"][-10:-6], d["downloadURL"])
