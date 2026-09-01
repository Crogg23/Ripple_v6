"""loadkit.archive: one member or a loud error -- plus a repo gate that keeps
the largest-member heuristic from being copy-pasted back into scripts/.

The trap: multi-part zips (EIA-860/861 bundle 13-20 files) silently truncated
when a loader picked the biggest member. Six live copies existed on 2026-09-01.
"""
import io
import re
import zipfile
from pathlib import Path

import pytest

from loadkit.archive import AmbiguousArchiveError, pick_member, pick_sheet

REPO = Path(__file__).resolve().parents[1]


def _zip(names: dict) -> zipfile.ZipFile:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name, content in names.items():
            zf.writestr(name, content)
    return zipfile.ZipFile(io.BytesIO(buf.getvalue()))


def test_single_member_wins():
    zf = _zip({"data.csv": "a,b"})
    assert pick_member(zf) == "data.csv"


def test_multiple_members_raise_and_name_them():
    zf = _zip({"one.csv": "x" * 100, "two.csv": "y"})
    with pytest.raises(AmbiguousArchiveError, match="two.csv"):
        pick_member(zf)


def test_pattern_narrows_to_one():
    zf = _zip({"Plant_2024.xlsx": "p", "Utility_2024.xlsx": "u", "readme.txt": "r"})
    assert pick_member(zf, pattern="Plant") == "Plant_2024.xlsx"


def test_size_never_decides():
    """The exact EIA shape: the biggest member is NOT silently chosen."""
    zf = _zip({"huge_wrong.csv": "x" * 10_000, "tiny_right.csv": "y"})
    with pytest.raises(AmbiguousArchiveError):
        pick_member(zf)


def test_suffix_filter_and_macosx_ignored():
    zf = _zip({"__MACOSX/junk.csv": "j", "data.txt": "d", "layout.pdf": "p"})
    assert pick_member(zf, suffixes=(".txt", ".csv")) == "data.txt"


def test_no_match_raises_with_listing():
    zf = _zip({"data.json": "{}"})
    with pytest.raises(AmbiguousArchiveError, match="data.json"):
        pick_member(zf, suffixes=(".csv",))


def test_pick_sheet_explicit_name():
    sheets = {"Notes": 1, "Data": 2}
    assert pick_sheet(sheets, name="Data") == 2


def test_pick_sheet_refuses_to_guess():
    with pytest.raises(AmbiguousArchiveError):
        pick_sheet({"Notes": 1, "Data": 2})


def test_pick_sheet_single():
    assert pick_sheet({"Only": 7}) == 7


# --- the gate: no new copies of the heuristic -------------------------------

# A largest/first-by-size (or blind-first) pick over zip members or sheets,
# in every shape the live copies used. Verified against the deleted originals.
BANNED = re.compile(
    r"(max\(|sort\(key\s*=\s*lambda).*(file_size|getsize)"
    r"|max\(sheets"
    r"|(infolist|namelist)\(\)\[0\]"
)
EXEMPT = ()  # no exemptions: recon_bulk_load_* turned out to be live loaders


def test_no_largest_member_heuristic_in_scripts():
    offenders = []
    for py in (REPO / "scripts").glob("*.py"):
        if py.name.startswith(EXEMPT):
            continue
        for i, line in enumerate(py.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if "archive-gate: allow" in line:
                continue  # audited waiver: deliberate top-N multi-file load
            if BANNED.search(line):
                offenders.append(f"{py.name}:{i}: {line.strip()}")
    assert not offenders, (
        "Largest-member zip/sheet heuristic found -- use loadkit.archive."
        "pick_member/pick_sheet instead (EIA-860 truncation trap):\n"
        + "\n".join(offenders)
    )
