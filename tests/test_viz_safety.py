"""viz/safety.py — the facts-vs-leads classifier. Fail-closed, downgrade-only."""

from viz import safety


def cls(sql, df=None):
    return safety.classify_query(sql, df)


# ---- clean: single table, or hard-ID joins ---------------------------------- #
def test_single_table_is_clean():
    assert cls("SELECT state, COUNT(*) FROM a GROUP BY 1")["state"] == "clean"


def test_steel_join_over_non_claim_tables_is_clean():
    c = cls("SELECT * FROM a JOIN b ON a.NPI = b.NPI")
    assert c["state"] == "clean"
    assert all(j["tier"] in ("STEEL", "STRONG") for j in c["joins"])


def test_using_with_hard_key_is_clean():
    assert cls("SELECT * FROM a JOIN b USING (npi)")["state"] == "clean"


# ---- lead: name/address joins, claim reads ---------------------------------- #
def test_name_join_is_a_lead():
    c = cls("SELECT * FROM a JOIN b ON a.provider_name = b.org_name")
    assert c["state"] == "lead"
    assert "name-join" in c["triggers"]


def test_name_join_hidden_in_where_still_not_clean():
    # implicit comma-join: conditions live in WHERE; must NOT read as clean
    c = cls("SELECT * FROM a, b WHERE a.provider_name = b.org_name")
    assert c["state"] in ("lead", "unverified")


def test_leads_read_is_a_lead_even_on_steel_join():
    c = cls('SELECT * FROM LIBRARY_META."CONNECT".LEADS l JOIN b ON l.NPI = b.NPI')
    assert c["state"] == "lead"
    assert "claims" in c["triggers"]


def test_claim_shaped_result_columns_force_lead():
    import pandas as pd
    df = pd.DataFrame({"LEAD_ID": ["x"], "TITLE": ["t"]})
    assert cls("SELECT * FROM some_view", df)["state"] == "lead"


def test_address_join_is_a_lead():
    c = cls("SELECT * FROM a JOIN b ON a.mailing_address = b.street_address")
    assert c["state"] == "lead"
    assert "address-join" in c["triggers"]


# ---- unverified: anything the parser can't confidently tier ------------------ #
def test_alias_join_fails_closed():
    # K_N is a normalized-name alias the tagger can't tier -> never 'clean'
    c = cls("SELECT * FROM lft l JOIN rgt r ON l.K_N = r.K_N")
    assert c["state"] == "unverified"


def test_natural_join_fails_closed():
    assert cls("SELECT * FROM a NATURAL JOIN b")["state"] == "unverified"


def test_semi_join_fails_closed():
    c = cls("SELECT * FROM a WHERE id IN (SELECT id FROM b)")
    assert c["state"] == "unverified"


def test_ored_on_condition_fails_closed():
    c = cls("SELECT * FROM a JOIN b ON a.npi = b.npi OR a.name = b.name")
    assert c["state"] in ("lead", "unverified")  # the name side should make it a lead
    assert c["state"] == "lead"


def test_function_wrapped_join_fails_closed():
    c = cls("SELECT * FROM a JOIN b ON UPPER(a.col_thing) = b.col_thing")
    assert c["state"] == "unverified"


def test_geo_join_is_context_not_connection():
    c = cls("SELECT * FROM a JOIN b ON a.zip_code = b.zip_code")
    assert c["state"] == "unverified"
    assert "geo-join" in c["triggers"]


# ---- downgrade-only + badges ------------------------------------------------- #
def test_never_certifies_fact():
    # even the cleanest state carries no positive 'fact' certificate
    c = cls("SELECT * FROM a JOIN b ON a.NPI = b.NPI")
    assert "fact" not in str(c).lower()


def test_badge_args_parametrized_by_trigger():
    state, text = safety.badge_args({"state": "lead", "triggers": ["address-join"]})
    assert state == "lead" and "address" in text


def test_badge_args_none_when_clean():
    assert safety.badge_args({"state": "clean", "triggers": []}) is None


# ---- review regressions (2026-07-03): joins the scans could not see ------------ #
def test_subquery_using_name_join_is_a_lead():
    # `JOIN (subquery) v USING (name_col)` put parens between JOIN and USING and
    # slipped past the old JOIN-anchored regex - it must badge as a lead
    c = cls("SELECT * FROM contributions c "
            "JOIN (SELECT DISTINCT contributor_name FROM vendors) v "
            "USING (CONTRIBUTOR_NAME)")
    assert c["state"] == "lead"
    assert "name-join" in c["triggers"]


def test_cross_join_fails_closed():
    c = cls("SELECT * FROM contribs a CROSS JOIN vendors b")
    assert c["state"] == "unverified"


def test_join_with_uncaptured_condition_fails_closed():
    # any JOIN whose condition the parser did not capture must never read clean
    c = cls("SELECT * FROM a JOIN b")  # malformed/exotic - no ON, no USING
    assert c["state"] == "unverified"
