# Job search recon — 2026-08-31

Real postings pulled during a market-fit conversation about Ripple.
Not a target list. Chris does not plan to apply to these specific openings.
Purpose: calibrate what's realistic once Ripple is built out further.

## Coin-flip reach tier (revised — mid/senior, not staff-tier)

1. Senior Data Engineer — Ochsner Health
   https://careers.ochsner.org/job/new-orleans/senior-data-engineer/47519/98847923776
   Epic Clarity/Caboodle required. dbt + Azure Data Factory on Snowflake/Azure. Airflow.

2. Lead Analytics Engineer, Data Modeling & Quality — Arcadia
   https://jobs.lever.co/arcadia/16fb294b-eb50-4f1d-a3e9-fd0c34a8594e
   Owns SQL/dbt layer transforming clinical + claims data. $160K-$185K.

3. Senior Data Engineer — MDCalc
   https://www.builtinnyc.com/company/mdcalc/jobs
   ETL/ELT pipelines, Python, Snowflake, dbt/Airflow/Dagster.

4. Senior Data Engineer — WeightWatchers
   https://job-boards.greenhouse.io/ww/jobs/5370248008
   Python + Snowflake core. CI/CD (GitHub Actions/Argo CD), Prefect/Airflow, Datadog required.

5. Founding Data & Analytics Engineer — Sailor Health
   https://jobs.ashbyhq.com/sailorhealth/df9dbe7a-995d-4bfb-9bdd-08cab451e61a
   Snowflake, dbt, Python, FHIR, GraphQL. Early-stage, building from scratch.

6. Data Engineer, Fraud Analytics & Investigative Support — Praescient Analytics
   https://www.dice.com/job-detail/3533564c-23b3-4a28-ac15-f73374389ea2
   Must have fraud analysis experience. Public Trust clearance + US citizenship required.

7. Infrastructure Engineer, Sentinel — Komodo Health
   https://www.builtinsf.com/job/infrastructure-engineer-sentinel/4306331
   Mid-level. $134K-$209K. Snowflake, HIPAA/SOC2 alignment.

8. Master Data Management Engineer — CoverMyMeds (McKesson)
   https://builtin.com/job/master-data-management-engineer/8099722
   7+ yrs, 3+ yrs hands-on Ataccama/Informatica/Reltio/SAP MDG. $105K-$175K.
   Real gap: named vendor tool experience Ripple can't produce.

9. Data Engineer — Wikimedia Foundation
   https://startup.jobs/data-engineer-wikimedia-3779440
   3+ years data engineering, Spark/Hadoop exposure.

10. Data Architect, dbt & Snowflake (Banking domain) — Relevance Lab
    https://www.dice.com/job-detail/69532490-c5e3-46bc-a31b-94a95b769798
    Governance, lineage, regulatory compliance framing.

## Earlier "pie in the sky" list — corrected as too senior for 50% odds

Netflix Analytics Engineer 5 ($330K-$566K), Coinbase Staff AE Compliance (8+ yrs),
Komodo Staff Infrastructure Engineer (8+ yrs), HubSpot Staff AE — all near-zero
realistic odds regardless of Ripple's state. Kept here for reference only.

- https://www.coinbase.com/careers/positions/8104148
- https://job-boards.greenhouse.io/komodohealth/jobs/8729916002
- https://www.hubspot.com/careers/jobs/7988079

## Mission-driven / "legit cool" list (unchanged from prior message)

1. OpenSecrets, Database Engineer — https://www.opensecrets.org/about/careers-database-engineer
2. ProPublica, Data Analyst — https://job-boards.greenhouse.io/propublica
3. Scrutinize, Senior Data Engineer (Legal Insights) — https://www.idealist.org/en/nonprofit-job/4fcb8d302f644711bc9532f2000cc895-senior-data-engineer-legal-insights-scrutinize-new-york
4. HHS-OIG, IT Specialist (DATAMGT), GS-12/13/14 — https://www.usajobs.gov/job/876261000
5. Internet Archive, Software Engineer, Archiving & Data Services — https://app.trinethire.com/companies/32967-internet-archive/jobs/99996-software-engineer-archiving-data-services-remote
6. Wikimedia Foundation, Data Engineer — https://startup.jobs/data-engineer-wikimedia-3779440
7. Bloomberg, Senior Data Management Professional, Entities — https://bloomberg.avature.net/careers/JobDetail/Senior-Data-Management-Professional-Data-Engineering-Entities/20788
8. Booz Allen, Data Engineer (fraud/national intelligence) — https://careers.boozallen.com/careers/JobDetail/Arlington-Data-Engineer-R0242942/126330
9. Praescient Analytics, Data Engineer (Fraud Analytics) — https://www.dice.com/job-detail/3533564c-23b3-4a28-ac15-f73374389ea2
10. Coinbase, Staff Analytics Engineer, Compliance Data — https://www.coinbase.com/careers/positions/8104148

## Straight-fit tier (from earlier message, unchanged)

- Ochsner Health, Data Engineer — Snowflake/DBT/Epic Clarity — https://careers.ochsner.org/job/new-orleans/data-engineer-snowflake-dbt-and-epic-clarity/47519/88311735376
- JBS Technologies, Data Engineer (Epic Clarity) — https://www.dice.com/job-detail/21aa9bc2-5cfe-404e-be35-c7986870b4ea
- Global Force USA, Data Engineer DBT/Snowflake (Healthy Planet Epic) — https://www.dice.com/job-detail/02f122aa-ef81-4039-b6ac-e0df753bba0e
- Strategic Technology Institute, Data Architect (Epic Caboodle) — https://www.dice.com/job-detail/5a019be0-34d8-4162-8be4-0189ee7b3069

## Confirmed facts about Ripple's current build (checked in-repo 2026-08-31)

- dbt is live: 2,367 .sql models in library-onboarding/ripple_dbt/
  (staging, intermediate, marts, registry, timeline layers)
- CI runs `dbt parse` on every push/PR (.github/workflows/dbt.yml)
- Dedicated least-privilege Snowflake role: RIPPLE_TRANSFORM_RW
- Unconfirmed: whether an orchestrator (Airflow/Dagster/Prefect) runs the loads on schedule
- Unconfirmed: whether marts feed any downstream BI/serving layer
