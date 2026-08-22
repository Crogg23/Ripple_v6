"""Domain configs for scripts/ripples/neighbor_spike_rule.py.

Each entry is one (noun, neighbor key, bad event) triple, found in the
2026-08-21 breadth-first survey across health/labor/environment (justice was
surveyed and rejected -- caseload isn't a bad event, no real substitute found).
Column names below are verified against the actual dbt model SQL, not guessed.

All queries aggregate in Snowflake (GROUP BY noun, quarter) -- only small
per-noun-per-quarter counts come back to Python, never raw event rows.
"""

DOMAINS = [
    {
        "name": "health (nursing homes, re-run with the generalized method)",
        "sql": """
            select
                d.cms_certification_number_ccn::varchar as noun_id,
                m.chain_id::varchar as neighbor_key,
                to_varchar(year(d.survey_date)) || 'Q' ||
                    to_varchar(quarter(d.survey_date)) as quarter,
                count(*) as n_events
            from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES d
            join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME m
              on m.cms_certification_number_ccn = d.cms_certification_number_ccn
            where d.survey_date is not null
              and m.chain_id is not null
            group by 1, 2, 3
        """,
    },
    {
        "name": "labor (mine safety)",
        "sql": """
            select
                v.mine_id::varchar as noun_id,
                m.current_controller_id::varchar as neighbor_key,
                to_varchar(year(v.violation_issue_date)) || 'Q' ||
                    to_varchar(quarter(v.violation_issue_date)) as quarter,
                count(*) as n_events
            from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS v
            join LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES m
              on m.mine_id = v.mine_id
            where v.violation_issue_date is not null
              and m.current_controller_id is not null
            group by 1, 2, 3
        """,
    },
    {
        "name": "environment (toxic release facilities)",
        "sql": """
            with noun as (
                select
                    c_3_frs_id::varchar as noun_id,
                    max(c_17_standard_parent_co_name) as neighbor_key
                from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023
                where c_3_frs_id is not null
                  and c_17_standard_parent_co_name is not null
                group by 1
            )
            select
                n.noun_id,
                n.neighbor_key,
                to_varchar(year(e.achieved_date)) || 'Q' ||
                    to_varchar(quarter(e.achieved_date)) as quarter,
                count(*) as n_events
            from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS e
            join noun n on n.noun_id = e.registry_id::varchar
            where e.achieved_date is not null
            group by 1, 2, 3
        """,
    },
]
