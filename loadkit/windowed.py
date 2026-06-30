"""Recursive window planning for cursor-hostile paginated APIs (the LDA fix).

The Senate LDA API caps page_size at 25 AND refuses to page past ~record 2,500
(page=100 -> HTTP 400). The original plan's "< 10k per slice" target is ABOVE that
ceiling, so a heavy (year) slice silently truncates at row 2,500 while the 2,500
landed rows look healthy. The fix: before paging a window, ask the API its `count`;
if it exceeds the ceiling, SUBDIVIDE (year -> year+quarter -> year+quarter+type)
until every leaf window is pageable. Then a count-reconciliation referee proves
nothing was dropped.

Pure logic (`plan_windows` / `reconcile`) -- the count_fn and subdivide strategy are
injected, so this is fully unit-tested without touching the network.
"""
from __future__ import annotations

from dataclasses import dataclass


class WindowError(RuntimeError):
    """Raised when a window can't be proven complete (records would be dropped)."""


@dataclass
class Window:
    key: dict                              # e.g. {"filing_year": 2024, "filing_type": "Q1"}
    count: int = -1
    pageable: bool = False                 # count <= ceiling -> safe to page fully
    unsplittable_overflow: bool = False    # above ceiling and can't subdivide further

    @property
    def label(self) -> str:
        return "&".join(f"{k}={v}" for k, v in self.key.items())


def plan_windows(roots, count_fn, subdivide, *, ceiling: int = 2500, max_depth: int = 6):
    """Expand `roots` into leaf windows each with count <= ceiling.

      count_fn(window_key) -> int            the API envelope 'count' for that filter
      subdivide(window_key) -> list | None   finer windows, or None if it can't split

    Returns (leaves, overflow). `leaves` are all the windows to page; the ones with
    `unsplittable_overflow=True` are ABOVE the ceiling and could not be split -- they
    are surfaced in `overflow` so the caller widens the schema or accepts a KNOWN,
    logged truncation. Nothing is ever dropped silently.
    """
    leaves, overflow = [], []
    stack = [(dict(k), 0) for k in roots]
    while stack:
        key, depth = stack.pop()
        n = count_fn(key)
        if n <= ceiling:
            leaves.append(Window(key=key, count=n, pageable=True))
            continue
        children = subdivide(key) if depth < max_depth else None
        if not children:
            w = Window(key=key, count=n, pageable=False, unsplittable_overflow=True)
            leaves.append(w)
            overflow.append(w)
            continue
        for ch in children:
            stack.append((dict(ch), depth + 1))
    return leaves, overflow


def reconcile(pages_fetched: int, page_size: int, envelope_count: int) -> bool:
    """The referee: did we page the WHOLE window? True iff the rows we could have
    fetched cover the count the API reported for that window."""
    return pages_fetched * page_size >= envelope_count


def assert_window_complete(window, pages_fetched, page_size, envelope_count) -> None:
    """Fail (don't mark the window done) if reconciliation says rows were dropped."""
    if not reconcile(pages_fetched, page_size, envelope_count):
        raise WindowError(
            f"window {getattr(window, 'label', window)}: fetched "
            f"{pages_fetched}*{page_size}={pages_fetched * page_size} < reported "
            f"{envelope_count} -- incomplete, not marking done"
        )
