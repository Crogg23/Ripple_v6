"""Quote-aware, fail-loud parsing for FEC bulk files.

Replaces build_money_spine.read_fec's `split('|')` + pad/truncate-and-WARN -- the
behaviour the stress-test flagged as able to silently ship a WRONG follow-the-money
figure. An embedded pipe in a free-text NAME / EMPLOYER field shifts a row's
TRANSACTION_AMT / SUB_ID columns; the old parser padded the row and kept going,
landing a mis-shaped number that looks healthy to the density gate.

Here a field-count mismatch is HARD-REJECTED to a quarantine list -- never padded,
never truncated, never landed mis-shaped. The caller asserts the quarantine rate is
tiny (`require_clean`); a high rate means the wrong column list or wrong delimiter,
so we FAIL the load instead of shipping it.

FEC "Detailed Files" are pipe-delimited, latin-1, NO header row (column names come
from the data dictionary). The Independent Expenditure file is the exception --
comma-delimited WITH a header -- use `parse_csv()` for that one, not `parse_pipe()`.
"""
from __future__ import annotations

import csv
import io
from dataclasses import dataclass

import pandas as pd


class FecParseError(RuntimeError):
    """A parse that should stop the load (too many quarantined rows / bad shape)."""


@dataclass
class ParseResult:
    good: pd.DataFrame          # exactly-shaped rows, every value TEXT
    quarantine: list            # [{"lineno", "n_fields", "raw"}] -- never landed
    n_good: int
    n_bad: int
    columns: list

    @property
    def quarantine_fraction(self) -> float:
        total = self.n_good + self.n_bad
        return (self.n_bad / total) if total else 0.0

    def require_clean(self, max_fraction: float = 0.001) -> "ParseResult":
        """Fail LOUD if too many rows were quarantined -- the signal that the column
        list or delimiter is wrong, i.e. the parse is silently mis-shaping money."""
        if self.quarantine_fraction > max_fraction:
            raise FecParseError(
                f"{self.n_bad}/{self.n_good + self.n_bad} rows "
                f"({self.quarantine_fraction:.3%}) failed the field-count check "
                f"(ceiling {max_fraction:.3%}) -- wrong column list or delimiter? "
                f"first bad: {self.quarantine[:3]}"
            )
        return self


def parse_pipe(raw, columns, *, encoding: str = "latin-1") -> ParseResult:
    """Parse a pipe-delimited, NO-header FEC bulk file -- quote-aware + fail-loud.

    Every kept row has EXACTLY len(columns) fields. Rows that don't (an embedded
    pipe shifted the columns) go to `quarantine` with their line number + raw text;
    they are NEVER padded/truncated into the frame.
    """
    text = raw.decode(encoding) if isinstance(raw, (bytes, bytearray)) else raw
    width = len(columns)
    reader = csv.reader(io.StringIO(text), delimiter="|", quotechar='"')
    good, bad = [], []
    for lineno, parts in enumerate(reader, start=1):
        if not parts or (len(parts) == 1 and parts[0].strip() == ""):
            continue  # blank line
        if len(parts) != width:
            bad.append({"lineno": lineno, "n_fields": len(parts), "raw": "|".join(parts)[:500]})
            continue
        good.append(parts)
    df = pd.DataFrame(good, columns=list(columns), dtype=str)
    return ParseResult(good=df, quarantine=bad, n_good=len(good), n_bad=len(bad), columns=list(columns))


def parse_csv(raw, *, expected_columns=None, encoding: str = "utf-8") -> pd.DataFrame:
    """Parse a comma-delimited file WITH a header (the Independent Expenditure file).

    Everything stays TEXT (dtype=str, no NA coercion) to honour the raw-layer rule.
    Validates that `expected_columns` (if given) are all present, so a layout change
    fails loudly instead of dropping a column.
    """
    text = raw.decode(encoding) if isinstance(raw, (bytes, bytearray)) else raw
    df = pd.read_csv(io.StringIO(text), dtype=str, keep_default_na=False, na_values=[])
    df.columns = [c.strip() for c in df.columns]
    if expected_columns:
        missing = [c for c in expected_columns if c not in df.columns]
        if missing:
            raise FecParseError(
                f"CSV missing expected columns {missing}; got {list(df.columns)[:12]}"
            )
    return df


def looks_misparsed(df: pd.DataFrame, *, min_columns: int = 2) -> bool:
    """A pipe file parsed as one fat column (or a comma file fed to parse_pipe)
    collapses to ~1 column -- a cheap guard to catch the wrong-parser mistake early."""
    return df.shape[1] < min_columns
