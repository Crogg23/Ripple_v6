"""Lead-job tests — the flagship must bypass the bridge guards and cover its sources."""

import inspect

import pytest

from connect import leads
from connect.leads_specs import JOBS


def test_leads_never_imports_bridge():
    """The bridge fan-out/dedup guards drop high-value leads (21 of 38). The leads
    runner must NOT import connect.bridge so it can run its own ungated SQL."""
    import_lines = [ln for ln in inspect.getsource(leads).splitlines()
                    if ln.strip().startswith(("import ", "from "))]
    assert not any("bridge" in ln for ln in import_lines)


def test_banned_job_sets_no_fanout_guard():
    assert JOBS["banned_but_operating"]["no_fanout_guard"] is True


def test_compiled_sql_covers_all_sources():
    sql = leads.compile_sql(JOBS["banned_but_operating"])
    assert "FED_HHS_OIG_LEIE" in sql
    assert "FED_CMS_FACILITY_AFFILIATION" in sql
    for roster in ("FED_CMS_HOSPITAL_GENERAL", "FED_CMS_DIALYSIS", "FED_CMS_POS_OTHER"):
        assert roster in sql


def test_run_job_refuses_without_guard():
    spec = {k: v for k, v in JOBS["banned_but_operating"].items() if k != "no_fanout_guard"}
    with pytest.raises(ValueError):
        leads.run_job(None, spec, "rid")  # raises on the guard check, before any DB call


def test_lead_id_is_stable():
    a = leads._lead_id("banned_but_operating", "NPI", "1164450573")
    b = leads._lead_id("banned_but_operating", "NPI", "1164450573")
    assert a == b and a.startswith("LEAD_")
