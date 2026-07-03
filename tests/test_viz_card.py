"""viz/card.py — the card is the product's proof artifact, so it gets the
strongest test in the suite: a subprocess round-trip from a FOREIGN cwd."""

import re
import subprocess
import sys

import pytest

from viz import card


def _write(tmp_path, **kw):
    defaults = dict(slug="test_q", sql="SELECT 1 AS X", plug="bar",
                    plug_kwargs={"x": "KIND", "y": "N"}, outdir=tmp_path)
    defaults.update(kw)
    return card.new_card(**defaults)


# ---- the round-trip: a generated card RUNS from anywhere ---------------------- #
def test_card_executes_from_foreign_cwd(tmp_path):
    path = _write(tmp_path)
    r = subprocess.run(
        [sys.executable, str(path)], cwd=str(tmp_path), capture_output=True,
        text=True, env={**__import__("os").environ, "RIPPLE_CARD_DRY": "1"},
        timeout=120,
    )
    assert r.returncode == 0, r.stderr
    assert "imports resolve" in r.stdout


def test_card_is_utf8_ascii_and_compiles(tmp_path):
    path = _write(tmp_path)
    body = path.read_text(encoding="utf-8")
    assert body.isascii(), "cards must be ASCII (cp1252 consoles)"
    compile(body, str(path), "exec")


# ---- numbering / overwrite semantics ------------------------------------------- #
def test_named_question_overwrites_new_forks(tmp_path):
    p1 = _write(tmp_path, name="top_x")
    p2 = _write(tmp_path, name="top_x")        # same slug + EXPLICIT name -> overwrite
    assert p1 == p2
    p3 = _write(tmp_path, name="top_x", new=True)  # --new -> fork to q02
    assert p3 != p1
    assert re.match(r"q02_", p3.name)


def test_auto_named_cards_always_fork(tmp_path):
    # two DIFFERENT questions that both auto-suggest 'bar' must not clobber
    p1 = _write(tmp_path, sql="SELECT 1 AS A")
    p2 = _write(tmp_path, sql="SELECT 2 AS B")
    assert p1 != p2


def test_ejected_cards_are_never_overwritten(tmp_path):
    p1 = _write(tmp_path, name="tuned")
    card.eject(p1)
    p2 = _write(tmp_path, name="tuned")        # same name, but p1 is hand-tuned now
    assert p2 != p1


# ---- SQL escaping: the card must reproduce the EXACT SQL on re-run --------------- #
def test_sql_with_backslashes_round_trips(tmp_path):
    sql = r"SELECT SPLIT_PART(CASE_TYPE, '\t', 3) AS ST FROM T WHERE X LIKE '%\\%'"
    p = _write(tmp_path, sql=sql, name="tabby")
    ns = {}
    body = p.read_text(encoding="utf-8")
    compile(body, str(p), "exec")              # \x etc. must not be a SyntaxError
    m = re.search(r'SQL = """\\\n(.*)\n"""', body, re.DOTALL)
    assert m is not None
    # the literal, when evaluated as Python, must equal the original SQL
    assert eval(f'"""{m.group(1)}"""') == sql  # noqa: S307 - test-only eval


def test_sql_with_triple_quote_does_not_corrupt(tmp_path):
    sql = 'SELECT \'a"""b\' AS X'
    p = _write(tmp_path, sql=sql, name="quoty")
    compile(p.read_text(encoding="utf-8"), str(p), "exec")


def test_slug_sanitized_for_windows(tmp_path):
    p = _write(tmp_path, slug="what's up with X?!")
    assert re.match(r"^[a-z0-9_]+$", p.parent.name.rsplit("_", 3)[0])


# ---- badge serialization --------------------------------------------------------- #
def test_lead_badge_is_literal_code_in_the_card(tmp_path):
    p = _write(tmp_path, classification={"state": "lead", "triggers": ["name-join"]})
    body = p.read_text(encoding="utf-8")
    assert 'safety.badge(fig, ' in body and "name-based match" in body


def test_clean_classification_writes_no_badge(tmp_path):
    p = _write(tmp_path, classification={"state": "clean", "triggers": []})
    assert "safety.badge" not in p.read_text(encoding="utf-8")


# ---- eject: the plug body IS the template ------------------------------------------ #
def test_eject_inlines_real_plug_source(tmp_path):
    p = _write(tmp_path)
    card.eject(p)
    body = p.read_text(encoding="utf-8")
    assert "def bar(" in body                      # the actual plug function
    assert "def column_roles(" in body             # its helpers came along
    assert "fig = bar(df" in body                  # the call now targets local code
    assert "fig = plugs.bar(" not in body
    compile(body, str(p), "exec")                  # still valid python


def test_ejected_card_still_dry_runs(tmp_path):
    p = _write(tmp_path)
    card.eject(p)
    r = subprocess.run(
        [sys.executable, str(p)], cwd=str(tmp_path), capture_output=True,
        text=True, env={**__import__("os").environ, "RIPPLE_CARD_DRY": "1"},
        timeout=120,
    )
    assert r.returncode == 0, r.stderr


def test_ejected_figure_matches_plug_figure():
    pytest.importorskip("plotly")
    import pandas as pd
    from viz import plugs
    df = pd.DataFrame({"KIND": ["a", "b"], "N": [1, 2]})
    baseline = plugs.bar(df, x="KIND", y="N", as_of=None)
    # simulate eject: exec the inlined source and call the local function
    import inspect
    import textwrap
    ns = {"theme": __import__("viz.theme", fromlist=["theme"]),
          "_dt": __import__("datetime")}
    for n in ("META_COLS", "MAX_CATEGORIES", "MAX_TABLE_ROWS", "_US_STATES"):
        ns[n] = getattr(plugs, n)
    for fn in plugs.EJECT_HELPERS + [plugs.bar]:
        exec(textwrap.dedent(inspect.getsource(fn)), ns)
    ejected = ns["bar"](df, x="KIND", y="N", as_of=None)
    assert baseline.to_json() == ejected.to_json()
