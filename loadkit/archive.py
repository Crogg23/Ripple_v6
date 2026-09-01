"""Pick THE member out of a zip (or THE sheet out of a workbook) -- loudly.

The largest-member heuristic silently truncated multi-part zips: EIA-860/861
bundle 13-20 files and "biggest wins" picks wrong (recon_bulk_load_2026-08-07
documented it; 18 zip specs were at risk, USAspending FULL tables proven hit).
Six-plus hand-copied variants of that heuristic lived in scripts/.

The rule here: one candidate wins, a pattern narrows, ambiguity RAISES with
the member list printed. Nothing is ever chosen by size. Losing a load run to
a loud error beats silently landing one file of thirteen.
"""
from __future__ import annotations

import re
from typing import Iterable, Optional


class AmbiguousArchiveError(RuntimeError):
    """More (or fewer) than one candidate -- caller must pass a pattern."""


def _candidates(names: Iterable[str], suffixes=None, pattern: Optional[str] = None):
    out = [n for n in names
           if not n.endswith("/") and "__MACOSX" not in n and not n.startswith(".")]
    if suffixes:
        sfx = tuple(s.lower() for s in suffixes)
        out = [n for n in out if n.lower().endswith(sfx)]
    if pattern:
        rx = re.compile(pattern, re.IGNORECASE)
        out = [n for n in out if rx.search(n)]
    return out


def pick_member(zf, pattern: Optional[str] = None, suffixes=None) -> str:
    """The one member of ``zf`` matching ``suffixes`` and ``pattern``.

    Exactly one match -> its name. Zero or several -> AmbiguousArchiveError
    listing what IS in the zip, so the fix (a pattern) writes itself.
    """
    names = _candidates(zf.namelist(), suffixes=suffixes, pattern=pattern)
    if len(names) == 1:
        return names[0]
    want = f"pattern={pattern!r} suffixes={suffixes!r}"
    if not names:
        raise AmbiguousArchiveError(
            f"No zip member matches {want}. Members: {zf.namelist()[:20]}")
    raise AmbiguousArchiveError(
        f"{len(names)} zip members match {want} -- refusing to guess by size "
        f"(the EIA-860 trap). Pass a pattern that matches ONE. "
        f"Matches: {names[:20]}")


def pick_sheet(sheets: dict, name: Optional[str] = None, pattern: Optional[str] = None):
    """The one sheet out of a ``read_excel(sheet_name=None)`` dict.

    Explicit ``name`` wins; else exactly one sheet (or one pattern match)
    is required. Never picked by row count.
    """
    if name is not None:
        if name in sheets:
            return sheets[name]
        raise AmbiguousArchiveError(
            f"Sheet {name!r} not in workbook. Sheets: {list(sheets)}")
    keys = list(sheets)
    if pattern:
        rx = re.compile(pattern, re.IGNORECASE)
        keys = [k for k in keys if rx.search(str(k))]
    if len(keys) == 1:
        return sheets[keys[0]]
    raise AmbiguousArchiveError(
        f"{len(keys)} sheets match pattern={pattern!r} -- refusing to guess "
        f"by size. Sheets: {list(sheets)}")
