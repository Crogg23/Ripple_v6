"""Live-PDF tests for scripts/house_ptr_load.py's parse_pdf() (no Snowflake).

Every test here refetches its filing fresh from disclosures-clerk.house.gov --
that's a read of a public PDF, not a warehouse write -- and runs the real,
unmocked parse_pdf() against the bytes that come back. Marked `network` and
self-skips (like the `snowflake` tests self-skip on no connection) if the site
can't be reached.

Pins the six 2026-09-06 bug-fix cases from a fresh 20-filing audit:

  1. DOC_ID 20019022 -- five trades glued onto one pypdf line with no
     separator dropped all but the first, and the first stole its ticker
     from the second. Now: all 21 real trades, owner JT throughout, no
     ticker leaked across a trade boundary.
  2. DOC_ID 20019023 -- a mixed-case ticker rendering ("AgCO") failed an
     all-caps-only regex and fell through to a different trade's ticker.
     Now: 63 of 63 real trades, case-insensitive ticker match.
  3. DOC_ID 20020359 -- same one-line-many-trades issue, plus a bond with no
     ticker of its own that stole one from a trade three trades down the
     same blob. Now: all 5 real trades, correct owner, no stolen ticker.
  4. DOC_ID 20019292 / 20019445 -- ~370 characters of page-header boilerplate
     glued onto the front of the asset name because it was never recognized
     as a stop condition. Now: clean asset text, both filings.
  5. DOC_ID 20033709 -- the NOISE filter's bare "No" (no word boundary)
     matched the front of "note", swallowing the asset description as if it
     were the certification page's Yes/No line. Now: \\bNo\\b, non-blank.
  6. DOC_ID 20034869 -- "(Ticker: CCLFX)" failed a regex that required the
     ticker to be the first thing inside the parens. Now: TICKER='CCLFX'.

Also re-runs the fixed parser against 11 filings the same audit had already
confirmed clean, checking for regressions.
"""
import re
import sys
from pathlib import Path

import pytest
import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

# house_ptr_load imports land_frame (a warehouse writer) at module load time.
# Stub it before import so this stays a no-Snowflake test file.
sys.modules.setdefault("land_frame", type(sys)("land_frame"))
sys.modules["land_frame"].land = lambda *a, **k: {"status": "success"}

import house_ptr_load as hpl  # noqa: E402

pytestmark = pytest.mark.network

DOC_YEARS = {
    "20019022": 2021, "20019023": 2021, "20020359": 2022,
    "20019292": 2021, "20019445": 2021, "20033709": 2026, "20034869": 2026,
    "20020873": 2022, "20021946": 2022, "20022293": 2023, "20025855": 2024,
    "20030670": 2025, "20033402": 2025, "20034311": 2026, "20034521": 2026,
    "20034998": 2026, "20023257": 2023, "20023973": 2023,
}


@pytest.fixture(scope="session")
def fetch():
    session = requests.Session()

    def _fetch(doc: str) -> list[dict]:
        year = DOC_YEARS[doc]
        try:
            r = session.get(hpl.PDF_URL.format(year=year, doc=doc),
                             headers=hpl.UA, timeout=60)
        except requests.RequestException as e:
            pytest.skip(f"no network to disclosures-clerk.house.gov: {e}")
        if r.status_code != 200:
            pytest.skip(f"{doc}: HTTP {r.status_code} refetching from the live site")
        rec = {"DOC_ID": doc, "FILER_LAST": "", "FILER_FIRST": "",
               "STATE_DISTRICT": "", "FILING_YEAR": str(year), "FILING_DATE": ""}
        return hpl.parse_pdf(r.content, rec)

    return _fetch


# --- bug 1: multiple trades glued on one line, only the first landed -------

def test_alphabet_apple_daifuku_all_21_trades_land(fetch):
    rows = fetch("20019022")
    assert len(rows) == 21, f"expected 21 real trades, got {len(rows)}"


def test_alphabet_apple_daifuku_owner_is_jt_throughout(fetch):
    rows = fetch("20019022")
    owners = {r["OWNER"] for r in rows}
    assert owners == {"JT"}, f"expected every row owned JT, got {owners}"


def test_alphabet_row_does_not_steal_apples_ticker(fetch):
    rows = fetch("20019022")
    assert rows[0]["TICKER"] == "GOOG", (
        f"row 1 is the Alphabet/GOOG trade, got ticker={rows[0]['TICKER']!r} "
        "(AAPL would mean it leaked from the second trade in the blob)")


# --- bug 2: mixed-case ticker rendering fails an all-caps regex ------------

def test_agco_all_63_trades_land(fetch):
    rows = fetch("20019023")
    assert len(rows) == 63, f"expected 63 real trades, got {len(rows)}"


def test_agco_own_ticker_matches_despite_mixed_case(fetch):
    rows = fetch("20019023")
    assert rows[0]["TICKER"] == "AGCO", (
        f"row 1 is AGCO's own trade (rendered 'AgCO' in the PDF), "
        f"got ticker={rows[0]['TICKER']!r} (ALYF would mean it fell through "
        "to a different trade)")


# --- bug 3: a no-ticker bond stealing a ticker from three trades down -----

def test_hern_barclays_all_5_trades_land(fetch):
    rows = fetch("20020359")
    assert len(rows) == 5, f"expected 5 real trades, got {len(rows)}"


def test_hern_barclays_owner_is_jt_not_self(fetch):
    rows = fetch("20020359")
    owners = {r["OWNER"] for r in rows}
    assert owners == {"JT"}, f"expected every row owned JT, got {owners}"


def test_hern_barclays_bond_has_no_stolen_ticker(fetch):
    rows = fetch("20020359")
    assert rows[0]["TICKER"] is None, (
        f"row 1 is the Barclays bond, which has no ticker of its own; "
        f"got {rows[0]['TICKER']!r} (JPM would mean it was stolen from a "
        "trade three trades down the blob)")


def test_hern_jpm_ticker_lands_on_the_actual_jpm_trade(fetch):
    rows = fetch("20020359")
    jpm = [r for r in rows if r["TICKER"] == "JPM"]
    assert len(jpm) == 1 and "JP Morgan" in jpm[0]["ASSET_DESCRIPTION"]


# --- bug 4: page-header boilerplate glued onto the asset description ------

@pytest.mark.parametrize("doc,needle", [
    ("20019292", "Wells Fargo"),
    ("20019445", "Netflix"),
])
def test_asset_description_has_no_boilerplate(fetch, doc, needle):
    rows = fetch(doc)
    assert rows, f"{doc}: expected at least one trade"
    desc = rows[0]["ASSET_DESCRIPTION"]
    assert desc.startswith(needle), (
        f"{doc}: expected asset description to start with {needle!r}, "
        f"got {desc!r}")
    assert "Clerk of the House" not in desc
    assert len(desc) < 100, f"{doc}: {len(desc)}-char asset description, still polluted"


# --- bug 5: bare "No" (no word boundary) swallowing "note ..." ------------

def test_shreve_structured_note_description_is_not_blank(fetch):
    rows = fetch("20033709")
    assert rows, "expected at least one trade"
    desc = rows[0]["ASSET_DESCRIPTION"]
    assert desc, "asset description landed blank -- NOISE's bare 'No' ate 'note'"
    assert "note" in desc.lower()


# --- bug 6: "(Ticker: CCLFX)" -- the label breaks a bare-parenthetical regex

def test_cliffwater_ticker_strips_the_label_prefix(fetch):
    rows = fetch("20034869")
    assert rows, "expected at least one trade"
    assert rows[0]["TICKER"] == "CCLFX"


# --- regressions: filings the original audit had already confirmed clean --

REGRESSION_DOCS = ["20020873", "20021946", "20022293", "20025855", "20030670",
                   "20033402", "20034311", "20034521", "20034998", "20023257",
                   "20023973"]


@pytest.mark.parametrize("doc", REGRESSION_DOCS)
def test_previously_clean_filing_still_parses(fetch, doc):
    rows = fetch(doc)
    assert len(rows) >= 1, f"{doc}: expected at least one trade, got 0"
    # Every real trade line always carries its raw source text.
    for r in rows:
        assert r["RAW_LINE"], f"{doc}: a trade row landed with no RAW_LINE"
        assert re.match(r"\d{2}/\d{2}/\d{4}", r["TRANSACTION_DATE"])
