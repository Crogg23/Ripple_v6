"""Shared target-loading and cast-safe date parsing for the widened time sweeps.

The first sweep (sweep_time_series.py, 2026-08-20) measured ONE shape: rows per
period, one clock per table. This module is the common floor under the four
shapes it never ran:

    reporting lag   sweep_reporting_lag.py   happened -> reported, per row
    spans / stock   sweep_spans.py           what was live on date X, how long
    category mix    sweep_category_mix.py    the make-up shifting over time
    entity cohorts  sweep_entity_cohorts.py  things being born and dying

Everything here obeys the cast-safety rule from the datetime standard: a value
is never handed to a date parser until a regex has proved it already has that
format. A bare four-digit year must never reach TRY_TO_DATE -- Snowflake reads
it as epoch seconds and silently lands the row on 1970-01-01.
"""
import collections
import csv
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TI = os.path.join(REPO, "reports", "time_index")
CATALOG = os.path.join(REPO, "reports", "census_grid_2026-08-12", "fill",
                       "tier_a_columns.csv")

# July backup schemas are not the live warehouse. The 2026-08-20 scan swept them
# by accident and inflated every total by 237M rows.
BACKUP_PREFIXES = ("_RESTORE", "_BACKUP", "_OLD", "_ARCHIVE", "_TMP", "_SNAPSHOT")

DATE_TYPES = ("DATE", "TIMESTAMP_NTZ", "TIMESTAMP_LTZ", "TIMESTAMP_TZ")


def load_clock_roles():
    """model alias -> {clock role: [row, ...]}, best/primary first within a role."""
    roles = collections.defaultdict(lambda: collections.defaultdict(list))
    with open(os.path.join(TI, "clock_index.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            roles[r["model"].upper()][r["clock"]].append(r)
    conf = {"high": 0, "medium": 1, "low": 2}
    for m in roles:
        for c in roles[m]:
            roles[m][c].sort(key=lambda r: (0 if r["is_primary"] == "True" else 1,
                                            conf.get(r["confidence"], 3)))
    return roles


def load_measured():
    """(table alias, COLUMN) -> the scan's measured row from columns.csv."""
    meas = {}
    with open(os.path.join(TI, "columns.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            sch = r["table"].split(".")[0]
            if sch.upper().startswith(BACKUP_PREFIXES):
                continue
            meas[(r["table"].split(".")[-1].upper(), r["col"].upper())] = r
    return meas


def load_catalog():
    """SCHEMA.TABLE alias -> [(COLUMN, data_type), ...] for every mart column."""
    cat = collections.defaultdict(list)
    with open(CATALOG, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["schema"].upper().startswith(BACKUP_PREFIXES):
                continue
            cat[r["table"].upper()].append((r["column"].upper(), r["data_type"]))
    return cat


def table_alias_map():
    """table alias -> full SCHEMA.TABLE as the scan saw it (live schemas only)."""
    out = {}
    with open(os.path.join(TI, "columns.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            sch = r["table"].split(".")[0]
            if sch.upper().startswith(BACKUP_PREFIXES):
                continue
            out[r["table"].split(".")[-1].upper()] = r["table"]
    return out


def date_expr(col, dtype):
    """A cast-safe DATE expression for a column, whatever its storage type.

    Shape-guarded: each format is applied only to values that already proved they
    match it. Anything unrecognised comes back NULL rather than 1970-01-01.
    Clamped to the parser's 1700-2125 window so one junk row cannot invent a
    three-century span.
    """
    q = f'"{col}"'
    if dtype in DATE_TYPES:
        parsed = f"cast({q} as date)"
    else:
        v = f"trim(to_varchar({q}))"
        parsed = (
            f"coalesce("
            f"iff(regexp_like({v}, '^[0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}'),"
            f" try_to_date(left({v},10),'YYYY-MM-DD'), null),"
            f"iff(regexp_like({v}, '^[0-9]{{1,2}}/[0-9]{{1,2}}/[0-9]{{4}}$'),"
            f" try_to_date({v},'MM/DD/YYYY'), null),"
            f"iff(regexp_like({v}, '^[0-9]{{8}}$'),"
            f" try_to_date({v},'YYYYMMDD'), null),"
            f"iff(regexp_like({v}, '^[0-9]{{1,2}}-[A-Za-z]{{3}}-[0-9]{{4}}$'),"
            f" try_to_date(upper({v}),'DD-MON-YYYY'), null),"
            # Month-grain columns ('2020-05') snap to the start of their period.
            # Without this they parse to NULL and a whole monthly table vanishes
            # from the sweep -- which is how the biorxiv preprint table came back
            # empty on the first validation run.
            f"iff(regexp_like({v}, '^[0-9]{{4}}-[0-9]{{2}}$'),"
            f" try_to_date({v} || '-01','YYYY-MM-DD'), null),"
            f"iff(regexp_like({v}, '^(19|20)[0-9]{{2}}(0[1-9]|1[0-2])$'),"
            f" try_to_date({v} || '01','YYYYMMDD'), null))"
        )
    return f"iff(year({parsed}) between 1700 and 2125, {parsed}, null)"


def year_expr(col):
    """Pull a year out ARITHMETICALLY -- never through a date parser."""
    v = f'trim(to_varchar("{col}"))'
    return (f"iff(regexp_like({v}, '^[0-9]{{4}}') "
            f"and try_to_number(left({v}, 4)) between 1700 and 2125, "
            f"try_to_number(left({v}, 4)), null)")


def is_day_grain(rec_grain, dtype):
    return rec_grain in ("day", "month", "quarter") or dtype in DATE_TYPES


class Checkpoint:
    """Append-only JSONL output with a resumable done-set, one key per unit."""

    def __init__(self, out_path, ckpt_path):
        import json
        self.json = json
        self.out_path = out_path
        self.ckpt_path = ckpt_path
        self.done = set(json.load(open(ckpt_path))) if os.path.exists(ckpt_path) else set()
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        self.fh = open(out_path, "a", encoding="utf-8")

    def has(self, key):
        return key in self.done

    def write(self, key, rec):
        self.fh.write(self.json.dumps(rec, default=str) + "\n")
        self.fh.flush()
        self.done.add(key)
        self.json.dump(sorted(self.done), open(self.ckpt_path, "w"))


def pick_measurable(byrole, role, model, meas):
    """Best column for a clock role that the scan could ACTUALLY read.

    The clock index's `is_primary` flag records which column best expresses the
    role in MEANING terms. It says nothing about whether the values are usable.
    The biorxiv preprint table is the case that forced this: its primary
    "happened" column is a free-text month label the scan could not shape at all,
    while a perfectly good DATE column sits beside it. Ranking by measurability
    first, then by the reviewers' preference, keeps whole tables from silently
    dropping out of every sweep.
    """
    best = None
    for r in byrole.get(role, []):
        m = meas.get((model, r["column"].upper()))
        if not m:
            continue
        usable = int(m["trusted"] or 0) > 0 or (m["ymin"] or "").strip() not in ("", "None")
        score = (0 if usable else 1,
                 0 if r["is_primary"] == "True" else 1,
                 -int(m["nonnull"] or 0))
        if best is None or score < best[0]:
            best = (score, m)
    return None if best is None else best[1]
