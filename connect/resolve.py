"""Fuzzy record linkage — the entity-resolution frontier, BUILT BUT GATED.

Everything else in the engine matches on exact (normalized) values. This module
links the SAME real-world person across sources with NO shared hard ID, using
in-warehouse fuzzy scoring. It is deliberately GATED: it writes candidate links to
LIBRARY_META.CONNECT.ENTITY_LINKS and NEVER mutates the hard-ID spine. Promoting
a link into the spine is a separate, post-eval decision (see evaluate.py / Phase 6)
— the zero-false-merge hard-ID core stays a fixed point until precision is proven.

Method (all set-based, all in Snowflake — no client-side matching):
  BLOCK  cheap candidate generation: SOUNDEX(last name) + ZIP5. The right (large)
         side is pre-filtered to blocks the left (probe) side actually has, so we
         never compare all-vs-all.
  SCORE  within a block: JAROWINKLER_SIMILARITY on last + nickname-expanded first,
         EDITDISTANCE prune. Continuous 0-1.
  BAND   AUTO (>=0.92) / REVIEW (0.80-0.92) / WEAK. Only AUTO would ever be eligible
         to merge — and only after the eval gate.

The v1 recipe (`leie_nppes`) links OIG-excluded persons to NPPES providers by
name+place. Pairs that ALSO share an NPI are ground truth the scorer should rank
high (used by evaluate.py); pairs that match on name+place but NOT on NPI are the
real leads — a possibly-excluded person operating under a different/again no NPI.

    python -m connect resolve --pair leie_nppes            # dry-run: scored preview
    python -m connect resolve --pair leie_nppes --write    # persist ENTITY_LINKS
"""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd
from snowflake.connector.pandas_tools import write_pandas

from . import db, store
from .keys import normalize_sql, quote_ident

SCRATCH_FQN = store.cfqn("RESOLVE_SCRATCH")
LINKS_FQN = store.cfqn("ENTITY_LINKS")
NICK_FQN = store.cfqn("NICKNAME_MAP")
NICK_CSV = (Path(__file__).resolve().parents[1] / "library-onboarding" / "ripple_dbt"
            / "seeds" / "connect" / "nickname_map.csv")

MIN_SCORE = 0.80      # floor for writing a link
HIGH = 0.92           # AUTO band (merge-eligible, post-eval only)
MAX_EDIT_LAST = 3     # hard prune: surnames more than this far apart can't be the same
PAIR_BUDGET = 100_000  # multi-pass blocking: drop any block whose L*R self-join exceeds this

PAIRS: dict[str, dict] = {
    "leie_nppes": {
        "desc": "OIG-excluded persons vs NPPES providers (fuzzy name + ZIP)",
        "left":  {"table": "FED_HHS_OIG_LEIE", "last": "LASTNAME", "first": "FIRSTNAME",
                  "zip": "ZIP", "id": "NPI", "addr": "ADDRESS", "mid": "MIDNAME"},
        "right": {"table": "FED_CMS_NPPES", "last": "PROVIDER_LAST_NAME__LEGAL_NAME",
                  "first": "PROVIDER_FIRST_NAME",
                  "zip": "PROVIDER_BUSINESS_MAILING_ADDRESS_POSTAL_CODE", "id": "NPI",
                  "addr": "PROVIDER_FIRST_LINE_BUSINESS_MAILING_ADDRESS",
                  "mid": "PROVIDER_MIDDLE_NAME"},
    },
}

LINKS_DDL = f"""
CREATE TABLE IF NOT EXISTS {LINKS_FQN} (
    LEFT_REF   STRING NOT NULL, RIGHT_REF STRING NOT NULL,
    LEFT_SRC   STRING, RIGHT_SRC STRING,
    METHOD     STRING NOT NULL, SCORE FLOAT NOT NULL, BAND STRING,
    NPI_MATCH  BOOLEAN, EVIDENCE VARIANT,
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
)
"""


def _ensure_nickname_map(conn) -> int:
    """Load the nickname seed into Snowflake (idempotent); dedupe on variant."""
    rows = list(csv.DictReader(NICK_CSV.open(encoding="utf-8")))
    df = pd.DataFrame(rows).drop_duplicates(subset=["variant"]).reset_index(drop=True)
    df["variant"] = df["variant"].str.upper()
    df["canonical"] = df["canonical"].str.upper()
    df.columns = ["VARIANT", "CANONICAL"]
    write_pandas(conn, df, table_name="NICKNAME_MAP", database=store.CONNECT_DB,
                 schema=store.CONNECT_SCHEMA, auto_create_table=True, overwrite=True,
                 quote_identifiers=False)
    return len(df)


# Multi-pass blocking — a record lands in SEVERAL blocks so a true match isn't lost when one
# blocking key disagrees. ZIP-only blocking caught just ~24% of findable matches (a person's
# LEIE address rarely equals their NPPES business ZIP); the name-only passes reclaim the rest.
# Each pass is (tag, block_key, validity); the tag prefix keeps passes from colliding.
def _passes(last_n: str, first_n: str, zip5: str) -> list[tuple[str, str, str]]:
    return [
        ("z", f"SOUNDEX({last_n}) || '~' || {zip5}", f"{zip5} <> ''"),                # surname-sound + same place
        ("i", f"SOUNDEX({last_n}) || '~' || LEFT({first_n}, 1)", f"{first_n} <> ''"),  # surname-sound + first initial, ANY place
        ("n", f"{last_n} || '~' || {first_n}", f"{first_n} <> ''"),                    # exact full name, ANY place (tiny, precise)
    ]


def _block_side(conn, pair_key: str, side: str, spec: dict, only_blocks_from: str | None) -> None:
    """Insert one side's blocked rows — ONE ROW PER PASS, so a record sits in several blocks and a
    moved/renamed true match is still co-blocked by a non-ZIP pass. The big (right) side is
    restricted to blocks the probe (left) side actually has, per pass (the tag prefix scopes it)."""
    last = quote_ident(spec["last"])
    zip5 = f"LEFT(REGEXP_REPLACE(TO_VARCHAR({quote_ident(spec['zip'])}), '[^0-9]', ''), 5)"
    id_n = normalize_sql("NPI", quote_ident(spec["id"]))
    last_n = f"UPPER(TRIM({last}))"
    first_n = f"UPPER(TRIM({quote_ident(spec['first'])}))"
    addr_n = normalize_sql("ADDRESS", quote_ident(spec["addr"]))   # USPS-standardized street line
    mid_i = f"UPPER(LEFT(TRIM({quote_ident(spec['mid'])}), 1))"    # middle INITIAL (move-stable disambiguator)
    # separators so 'AB'+'C' and 'A'+'BC' don't collide into one fallback REF
    ref = f"'{spec['table']}:' || COALESCE({id_n}, MD5({last_n} || '|' || {first_n} || '|' || {zip5}))"
    # individuals only: a blank surname is an ORG row (NPPES type-2 / LEIE entities) — ~2.28M
    # NPPES rows that would collapse into one SOUNDEX('') mega-block (JAROWINKLER('','') = 100).
    base = f"{last_n} <> ''"
    selects = []
    for tag, key, valid in _passes(last_n, first_n, zip5):
        block = f"'{tag}#' || ({key})"
        where = f"{base} AND {valid}"
        if only_blocks_from:
            where += (f" AND {block} IN (SELECT DISTINCT BLOCK FROM {SCRATCH_FQN} "
                      f"WHERE SIDE = '{only_blocks_from}')")
        selects.append(
            f"SELECT DISTINCT {ref}, '{spec['table']}', '{side}', {block}, "
            f"{last_n}, {first_n}, {zip5}, {id_n}, {addr_n}, {mid_i} "
            f"FROM {db.fqn(spec['table'])} WHERE {where}")
    db.rows(conn, f"INSERT INTO {SCRATCH_FQN} "
                  f"(REF, SRC, SIDE, BLOCK, LAST_N, FIRST_N, PLACE, ID_N, ADDR, MID) "
                  + " UNION ALL ".join(selects))


def _score_sql() -> str:
    """Self-join within block; nickname-expand first names; continuous 0-1 score."""
    return f"""
        WITH l AS (SELECT * FROM {SCRATCH_FQN} WHERE SIDE = 'L'),
             r AS (SELECT * FROM {SCRATCH_FQN} WHERE SIDE = 'R'),
             le AS (SELECT l.*, COALESCE(nk.CANONICAL, SPLIT_PART(l.FIRST_N, ' ', 1)) AS FX
                    FROM l LEFT JOIN {NICK_FQN} nk ON nk.VARIANT = SPLIT_PART(l.FIRST_N, ' ', 1)),
             re AS (SELECT r.*, COALESCE(nk.CANONICAL, SPLIT_PART(r.FIRST_N, ' ', 1)) AS FX
                    FROM r LEFT JOIN {NICK_FQN} nk ON nk.VARIANT = SPLIT_PART(r.FIRST_N, ' ', 1)),
        scored AS (
          SELECT le.REF AS LEFT_REF, re.REF AS RIGHT_REF, le.SRC AS LEFT_SRC, re.SRC AS RIGHT_SRC,
                 le.LAST_N AS L_LAST, re.LAST_N AS R_LAST, le.FX AS L_FIRST, re.FX AS R_FIRST,
                 le.PLACE AS PLACE,
                 (le.ID_N IS NOT NULL AND le.ID_N = re.ID_N) AS NPI_MATCH,
                 JAROWINKLER_SIMILARITY(le.LAST_N, re.LAST_N) AS JW_LAST,
                 JAROWINKLER_SIMILARITY(le.FX, re.FX) AS JW_FIRST,
                 ROUND(0.70 * JAROWINKLER_SIMILARITY(le.LAST_N, re.LAST_N) / 100.0
                     + 0.30 * JAROWINKLER_SIMILARITY(le.FX, re.FX) / 100.0, 3) AS SCORE
          FROM le JOIN re ON le.BLOCK = re.BLOCK AND le.REF <> re.REF
          WHERE EDITDISTANCE(le.LAST_N, re.LAST_N) <= {MAX_EDIT_LAST}
          -- a pair can share several blocks (multi-pass); keep it once
          QUALIFY ROW_NUMBER() OVER (PARTITION BY le.REF, re.REF ORDER BY le.BLOCK) = 1 )
        SELECT * FROM scored WHERE SCORE >= {MIN_SCORE}
    """


def _cap_blocks(conn) -> None:
    """Drop blocks whose L*R self-join would exceed PAIR_BUDGET — a common surname-sound + first
    initial is a quadratic mega-block. Logged, never silent (a silent cap reads as 'covered
    everything'). True matches with an exact name survive via the 'n' pass even when their dense
    'i'/'z' block is dropped, so the cap costs little recall."""
    over = db.dicts(conn, f"""
        SELECT BLOCK, COUNT_IF(SIDE='L') AS L_N, COUNT_IF(SIDE='R') AS R_N
        FROM {SCRATCH_FQN} GROUP BY BLOCK
        HAVING COUNT_IF(SIDE='L') * COUNT_IF(SIDE='R') > {PAIR_BUDGET}
        ORDER BY L_N * R_N DESC""")
    if not over:
        return
    dropped_pairs = sum(int(r["L_N"]) * int(r["R_N"]) for r in over)
    db.rows(conn, f"""DELETE FROM {SCRATCH_FQN} WHERE BLOCK IN (
        SELECT BLOCK FROM (
          SELECT BLOCK, COUNT_IF(SIDE='L') AS L_N, COUNT_IF(SIDE='R') AS R_N
          FROM {SCRATCH_FQN} GROUP BY BLOCK
        ) WHERE L_N * R_N > {PAIR_BUDGET})""")
    print(f"  block-size cap: dropped {len(over):,} dense block(s) (~{dropped_pairs:,} pairs over "
          f"budget {PAIR_BUDGET:,}); densest {over[0]['BLOCK'][:20]} "
          f"= {int(over[0]['L_N'])}x{int(over[0]['R_N'])}")


def _build_scratch(conn, pair: dict) -> None:
    db.rows(conn, f"CREATE OR REPLACE TEMPORARY TABLE {SCRATCH_FQN} "
                  f"(REF STRING, SRC STRING, SIDE STRING, BLOCK STRING, LAST_N STRING, "
                  f"FIRST_N STRING, PLACE STRING, ID_N STRING, ADDR STRING, MID STRING)")
    _block_side(conn, "", "L", pair["left"], only_blocks_from=None)
    _block_side(conn, "", "R", pair["right"], only_blocks_from="L")
    _cap_blocks(conn)


def run(pair: str = "leie_nppes", write: bool = False, top: int = 25,
        min_score: float = MIN_SCORE) -> dict:
    if pair not in PAIRS:
        raise SystemExit(f"unknown pair '{pair}'. known: {list(PAIRS)}")
    spec = PAIRS[pair]
    conn = db.connect()
    try:
        store.ensure_schema(conn)
        nk = _ensure_nickname_map(conn)
        print(f"resolve [{pair}]: {spec['desc']} (nickname map: {nk} variants)")
        _build_scratch(conn, spec)
        rows = db.dicts(conn, _score_sql())
        rows = [r for r in rows if float(r["SCORE"]) >= min_score]
        rows.sort(key=lambda r: -float(r["SCORE"]))
        auto = [r for r in rows if float(r["SCORE"]) >= HIGH]
        # ground-truth precision proxy: of AUTO-band links, how many share an NPI
        auto_npi = sum(1 for r in auto if r["NPI_MATCH"])
        print(f"  {len(rows):,} candidate links >= {min_score} "
              f"({len(auto):,} AUTO >= {HIGH}); "
              f"AUTO sharing NPI (ground-truth correct): "
              f"{auto_npi}/{len(auto)} = {(auto_npi / len(auto) * 100 if auto else 0):.0f}%")
        print(f"\n  top {min(top, len(rows))} candidates:")
        for r in rows[:top]:
            gt = "✓NPI" if r["NPI_MATCH"] else "  · "
            print(f"   [{r['SCORE']:.3f}] {gt}  {r['L_LAST']},{r['L_FIRST']}  ~  "
                  f"{r['R_LAST']},{r['R_FIRST']}  @ {r['PLACE']}")
        if write and rows:
            _write_links(conn, rows, spec)
            print(f"\n  wrote {len(rows):,} links -> {LINKS_FQN} (GATED: spine untouched)")
        return {"candidates": len(rows), "auto": len(auto), "auto_npi": auto_npi}
    finally:
        conn.close()


def _band(score: float) -> str:
    return "AUTO" if score >= HIGH else ("REVIEW" if score >= MIN_SCORE else "WEAK")


def _write_links(conn, rows, spec) -> None:
    import json
    db.rows(conn, LINKS_DDL)
    recs = [{
        "LEFT_REF": r["LEFT_REF"], "RIGHT_REF": r["RIGHT_REF"],
        "LEFT_SRC": r["LEFT_SRC"], "RIGHT_SRC": r["RIGHT_SRC"],
        "METHOD": "JW_PERSON_v1", "SCORE": float(r["SCORE"]), "BAND": _band(float(r["SCORE"])),
        "NPI_MATCH": bool(r["NPI_MATCH"]),
        "EVIDENCE": json.dumps({"jw_last": r["JW_LAST"], "jw_first": r["JW_FIRST"],
                                "place": r["PLACE"]}),
    } for r in rows]
    df = pd.DataFrame(recs)
    write_pandas(conn, df, table_name="ENTITY_LINKS_STAGE", database=store.CONNECT_DB,
                 schema=store.CONNECT_SCHEMA, auto_create_table=True, overwrite=True,
                 quote_identifiers=False)
    stage = store.cfqn("ENTITY_LINKS_STAGE")
    db.rows(conn, f"""
        INSERT INTO {LINKS_FQN} (LEFT_REF, RIGHT_REF, LEFT_SRC, RIGHT_SRC, METHOD, SCORE,
                                 BAND, NPI_MATCH, EVIDENCE)
        SELECT LEFT_REF, RIGHT_REF, LEFT_SRC, RIGHT_SRC, METHOD, SCORE, BAND, NPI_MATCH,
               PARSE_JSON(EVIDENCE) FROM {stage}""")
    db.rows(conn, f"DROP TABLE IF EXISTS {stage}")


if __name__ == "__main__":
    run()
