"""Guards on the deterministic dbt scaffolder (loadkit.scaffold).

Regression coverage for the 2026-08-09 incident: with no connection and no
key_cols, scaffold_if_missing fabricated a phantom "ID" staging model AND
overwrote the curated intl_ie_cro schema.yml. Both paths must now refuse.
"""
from __future__ import annotations

import pytest

from loadkit import scaffold


@pytest.fixture
def models_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(scaffold, "MODELS_DIR", tmp_path)
    return tmp_path


def test_refuses_without_columns_or_keys(models_dir):
    """No conn + no key_cols -> refuse, never invent an 'ID' column."""
    with pytest.raises(RuntimeError, match="fabricated columns"):
        scaffold.scaffold_if_missing("fed_demo_source")
    assert not (models_dir / "staging" / "fed_demo_source").exists()


def test_refuses_to_overwrite_curated_schema(models_dir):
    """A schema.yml under another model's name is curated work — never clobber."""
    model_dir = models_dir / "staging" / "intl_demo"
    model_dir.mkdir(parents=True)
    curated = "version: 2\n# hand-curated, do not touch\n"
    (model_dir / "schema.yml").write_text(curated, encoding="utf-8")
    (model_dir / "stg_intl_demo_curated.sql").write_text("select 1", encoding="utf-8")

    with pytest.raises(RuntimeError, match="curated model in place"):
        scaffold.scaffold_if_missing(
            "intl_demo", key_cols=[{"col": "company_num", "as": "COMPANY_NO"}])

    assert (model_dir / "schema.yml").read_text(encoding="utf-8") == curated
    assert not (model_dir / "stg_intl_demo__all.sql").exists()


def test_key_cols_fallback_scaffolds_real_columns(models_dir):
    """No conn but spec-declared keys -> model built from those real columns."""
    out = scaffold.scaffold_if_missing(
        "fed_demo_keys", key_cols=[{"col": "ein", "as": "EIN"}])
    assert out is not None
    sql = (models_dir / "staging" / "fed_demo_keys" /
           "stg_fed_demo_keys__all.sql").read_text(encoding="utf-8")
    assert '"ein" as EIN' in sql
    assert '"ID"' not in sql


def test_existing_model_is_noop(models_dir):
    model_dir = models_dir / "staging" / "fed_done"
    model_dir.mkdir(parents=True)
    (model_dir / "stg_fed_done__all.sql").write_text("select 1", encoding="utf-8")
    assert scaffold.scaffold_if_missing("fed_done") is None
