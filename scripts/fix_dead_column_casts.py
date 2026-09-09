"""Fix the 118 mart columns a bad cast emptied.

Every fix here was chosen from the raw values measured in
reports/dead_columns_2026-09-08.csv, not from the column name.

Three shapes of fix:
  TEXT   the column holds codes or labels, so a numeric/date cast wiped it.
         Becomes nullif(trim(COL), '') so blanks land as real NULLs.
  DATE   the column holds a real date in a format the bare cast cannot read.
         Gets the format mask the raw values actually use.
  TS     same, but the value carries a time.

Run with --dry to see the diff without writing.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DBT = REPO / "library-onboarding" / "ripple_dbt"
MODELS = DBT / "models"

# (model file -> the columns actually measured dead in it). Built by the
# manifest walk in dead_column_fix_scope.json. A column name alone is not
# enough: FILING_DATE is broken in PCAOB and correct in SEC 13F.
SCOPE = {
    k.replace("/", "\\"): set(v)
    for k, v in json.loads((REPO / "scripts" / "dead_column_fix_scope.json").read_text()).items()
}

# column -> format mask, from the raw values. One entry per distinct format.
DATE_MASK = {
    # ISO 8601 with UTC offset: 2026-05-22T11:54:05-0500
    "ADMIN_SIGNED_DATE": "ISO_TZ",
    "SPONS_SIGNED_DATE": "ISO_TZ",
    "DFE_SIGNED_DATE": "ISO_TZ",
    "ADMIN_MANUAL_SIGNED_DATE": "ISO_TZ",
    "SPONS_MANUAL_SIGNED_DATE": "ISO_TZ",
    "DFE_MANUAL_SIGNED_DATE": "ISO_TZ",
    # 09-30-2003
    "ACTUAL_END_DATE": "MM-DD-YYYY",
    "EARLIEST_FRV_DETERM_DATE": "MM-DD-YYYY",
    "HPV_DAYZERO_DATE": "MM-DD-YYYY",
    "HPV_RESOLVED_DATE": "MM-DD-YYYY",
    "DSCV_PATHWAY_DATE": "MM-DD-YYYY",
    "NFTC_PATHWAY_DATE": "MM-DD-YYYY",
    # 2024/01/02
    "HPSA_WITHDRAWN_DATE_STRING": "YYYY/MM/DD",
    # 3/1/1788
    "DATE_BUY1": "MM/DD/YYYY",
    # 2026-05-01
    "DATE_FIRST_APPROVED_TO_PROVIDE_MEDICARE_AND_MEDICAID_SERVICES": "YYYY-MM-DD",
    "PROCESSING_DATE": "YYYY-MM-DD",
    "RATING_CYCLE_1_STANDARD_SURVEY_HEALTH_DATE": "YYYY-MM-DD",
    "RATING_CYCLE_2_STANDARD_HEALTH_SURVEY_DATE": "YYYY-MM-DD",
    # 2/25/2021 12:00:00 AM
    "AUDIT_REPORT_DATE": "MM/DD/YYYY HH12:MI:SS AM",
    "FISCAL_PERIOD_END_DATE": "MM/DD/YYYY HH12:MI:SS AM",
    "SIGNED_DATE": "MM/DD/YYYY HH12:MI:SS AM",
    "FILING_DATE": "MM/DD/YYYY HH12:MI:SS AM",
    # 22JAN2024
    "DATE_OF_INCIDENT": "DDMONYYYY",
    # 10OCT25:00:00:00
    "DATE_OF_DEATH": "DDMONYY:HH24:MI:SS",
}

TS_MASK = {
    # 01-JUL-12 00:00:00
    "BEGIN_DATE_TIME": "DD-MON-YY HH24:MI:SS",
    "END_DATE_TIME": "DD-MON-YY HH24:MI:SS",
    # 8/2/2025 15:30
    "LOCAL_DATETIME": "MM/DD/YYYY HH24:MI",
    # 03MAY24:18:33:00 in some years, 24FEB2025:16:26:00 in others
    "CREATED_TIMESTAMP": "SAS_DUAL",
}

# columns that must stay text; the cast was simply the wrong type
TO_TEXT = {
    "SPONS_DFE_MAIL_FOREIGN_CNTRY", "SPONS_DFE_LOC_FOREIGN_CNTRY", "ADMIN_FOREIGN_CNTRY",
    "DATE_OF_ANALYSIS", "FLAG_INDICATING_IF_THE_PLANT_BURNED_OR_GENERATED_ANY_AMOUNT_OF_COAL",
    "PLANT_ANNUAL_HG_TOTAL_OUTPUT_EMISSION_RATE_LB_MWH",
    "PLANT_ANNUAL_HG_INPUT_EMISSION_RATE_LB_MMBTU",
    "PLANT_ANNUAL_HG_COMBUSTION_OUTPUT_EMISSION_RATE_LB_MWH",
    "SEASON_BEGIN_DATE", "SEASON_END_DATE", "ALTERATION", "SCORE",
    "CONFDENIEDEXPIRED", "CONV_EXERCISE_PRICE_FN", "TRANS_DATE_FN",
    "DEEMED_EXECUTION_DATE_FN", "TRANS_TOTAL_VALUE_FN", "TRANS_PRICEPERSHARE_FN",
    "EXCERCISE_DATE_FN", "EXPIRATION_DATE_FN", "UNDLYNG_SEC_VALUE_FN",
    "ESTIMATED_AGE_ADJUSTED_DEATH_RATE_11_CATEGORIES_IN_RANGES",
    "TTM_DATE_RANGE", "FIVE_STAR_DATE", "LATE_SHIFT", "CLAIMS_DATE", "EQRS_DATE",
    "SMR_DATE", "SHR_DATE", "SRR_DATE", "STRR_DATE", "FYSWR_DATE", "SEDR_DATE",
    "ED30_DATE", "SIR_DATE", "HCP_VACCINATION_DATA_COLLECTION_DATES",
    "REPORT_DATE", "FOOTNOTE_FOR_DISCHARGE_FUNCTION_SCORE",
    "INDIANPLANVARIATIONESTIMATEDADVANCEDPAYMENTAMOUNTPERENROLLEE",
    "RFRG_PRVDR_CNTRY", "SUPLR_PRVDR_CNTRY", "RNDRNG_PRVDR_CNTRY",
    "OVRRD_BED_CNT_SW", "COST_REWEIGHTING_EUC", "MONTHLY_TOTALS",
    "WILLFUL_VIOLATOR", "ARBITRATION_AT_FILING",
    "DATE_GRANULARITY_DOB", "DATE_GRANULARITY_DOD", "DATE_GRANULARITY_START",
    "DATE_GRANULARITY_END", "DATE_GRANULARITY_TERMINATION",
    "DATE_FILED_IS_APPROXIMATE", "OTHER_DATES",
    "INITIAL_REPORTED_REASON_FOR_ENCOUNTER", "LAST_DAY_UPDATED", "LAST_REVIEWED_ON",
    "ACTIONGEO_LAT", "ACTIONGEO_LONG",
    "PRIVATE_AIRPORT_LIST_FOR_WHICH_INFORMATION_HAS_NOT_BEEN_UPDATED_IN_THE_LAST_3_YEARS",
} | {f"COST_MEASURE_ID_{i}" for i in range(1, 31)}


def new_expr(col: str, raw: str) -> str | None:
    """The expression that should replace the broken one."""
    src = f"nullif(trim({raw}), '')"
    if col in DATE_MASK:
        m = DATE_MASK[col]
        if m == "ISO_TZ":
            # the offset lands as -0500 with no colon, which the auto
            # parser refuses; the explicit TZHTZM mask reads it
            mask = "YYYY-MM-DD\"T\"HH24:MI:SSTZHTZM"
            return f"try_to_timestamp_tz({src}, '{mask}')::date"
        return f"try_to_date({src}, '{m}')"
    if col in TS_MASK:
        m = TS_MASK[col]
        if m == "SAS_DUAL":
            return (f"coalesce(try_to_timestamp({src}, 'DDMONYYYY:HH24:MI:SS'), "
                    f"try_to_timestamp({src}, 'DDMONYY:HH24:MI:SS'))")
        return f"try_to_timestamp({src}, '{m}')"
    if col in TO_TEXT:
        return src
    return None


# expr that currently wraps the column, e.g. try_to_date(FOO) or try_to_double(trim(FOO))
BROKEN = re.compile(
    r"(?P<lead>^[ \t]*)"
    r"(?P<expr>try_to_\w+\s*\(.*?\)|\{\{\s*ripple_dt\s*\(.*?\)\s*\}\})"
    r"(?P<mid>[ \t]+as[ \t]+)"
    r"(?P<alias>\"?(?P<col>\w+)\"?)"
    r"(?P<tail>[ \t]*,?[ \t]*)$",
    re.M,
)
INNER = re.compile(r"\b([A-Z][A-Z0-9_]{2,})\b")


def fix_file(path: Path, dry: bool) -> list[tuple[str, str, str]]:
    rel = str(path.relative_to(DBT))
    in_scope = SCOPE.get(rel)
    if not in_scope:
        return []
    txt = path.read_text(encoding="utf-8")
    changes: list[tuple[str, str, str]] = []

    def sub(m: re.Match) -> str:
        col = m.group("col").upper()
        if col not in in_scope:
            return m.group(0)
        expr = m.group("expr")
        cols = INNER.findall(expr)
        raw = next((c for c in cols if c == col), cols[-1] if cols else None)
        if raw is None:
            return m.group(0)
        ne = new_expr(col, raw)
        if ne is None or ne == expr:
            return m.group(0)
        changes.append((col, expr, ne))
        return f"{m.group('lead')}{ne}{m.group('mid')}{m.group('alias')}{m.group('tail')}"

    out = BROKEN.sub(sub, txt)

    # the hardcoded null in the nursing-home staging model
    if "_SOURCE_RUN_ID" in in_scope and "null::varchar" in out:
        out2 = re.sub(r"null::varchar(\s+as\s+_source_run_id)", r"_SOURCE_RUN_ID\1", out)
        if out2 != out:
            changes.append(("_SOURCE_RUN_ID", "null::varchar", "_SOURCE_RUN_ID"))
            out = out2

    if changes and not dry:
        path.write_text(out, encoding="utf-8")
    return changes


def main():
    dry = "--dry" in sys.argv
    total = 0
    touched = 0
    for p in sorted(MODELS.rglob("*.sql")):
        ch = fix_file(p, dry)
        if ch:
            touched += 1
            total += len(ch)
            print(f"\n{p.relative_to(MODELS)}")
            for col, old, new in ch:
                print(f"   {col}")
                print(f"     - {old}")
                print(f"     + {new}")
    print(f"\n{'DRY RUN ' if dry else ''}{total} casts fixed in {touched} files")


if __name__ == "__main__":
    main()
