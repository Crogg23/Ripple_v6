"""review -- the batch review cockpit: drain the two stuck decision queues N-at-a-time.

Two 'what' targets:

  ripple review leads    the CONNECT leads queue (named-person accountability claims). Pending =
                         LEADS STATUS='active' minus anything the DECISIONS audit log already ruled
                         on. For each lead the agent PRE-FILLS a recommendation from the evidence
                         timeline, but a HUMAN must press a key for every named person -- we never
                         auto-confirm a claim about a real individual. c/r write via the safety
                         spine (connect.safety.record), so a verdict survives the next rebuild.

  ripple review domains  the catalog domaining queue: landed/modeled (or review-queue) sources with
                         DOMAIN_PRIMARY UNCLASSIFIED. The agent suggests a domain from a title/id
                         keyword guess against the 22-value FACET_VOCAB. Domain writes are catalog-
                         sensitive, so this DEFAULTS to STAGING: approvals collect into
                         outputs/_ripple_domain_approvals.json and we print the exact
                         scripts/propose_domain_retag.py-style --apply command. Only --apply writes
                         SOURCE_REGISTRY directly (one targeted UPDATE per row, DOMAIN_SOURCE='human').

ripple uses COMPUTE_WH (see common.py), so review never fights the live pour on RIPPLE_WH.

The PURE pieces (recommendation compute, decision->record arg mapping, queue-fetch SQL builders,
domain suggestion) are split out with no DB / no input() so tests/test_ripple_review.py can drive them.
"""
from __future__ import annotations

import json
import re
from datetime import date, datetime

from ripple import common as C

APPROVALS_PATH = C.REPO / "outputs" / "_ripple_domain_approvals.json"

# The 22 governed domains (FACET_VOCAB DOMAIN axis, minus the UNCLASSIFIED/open_data_portal buckets
# which are never a positive suggestion). Kept as a literal so `review domains` degrades without a DB.
FACET_DOMAINS = [
    "corporate_entities", "crime_security", "economy_labor_trade", "education",
    "elections_voting", "energy_environment", "geo_demographics", "government_power",
    "health_medicine", "history_culture", "housing_social", "immigration_migration",
    "justice_courts", "money_finance", "money_in_politics", "procurement_intl",
    "sanctions_enforcement", "science_research", "spending_budget",
    "targeted_investigation", "transport_movement",
]

# Ordered keyword -> domain table for the title/id guess. First hit wins, so more-specific patterns
# come first (e.g. 'campaign finance' -> money_in_politics before a bare 'finance' -> money_finance).
DOMAIN_KEYWORDS: list[tuple[str, str]] = [
    (r"campaign.?finance|\bfec\b|\bpac\b|lobby|donor|itcont|political contribution", "money_in_politics"),
    (r"sanction|ofac|sdn|debarred|excluded|denied.?part", "sanctions_enforcement"),
    (r"\belection|\bvoter|\bballot|precinct|polling", "elections_voting"),
    (r"medic(aid|are)|health|hospital|clinic|\bnpi\b|disease|mortality|cdc|drug|opioid|patient", "health_medicine"),
    (r"crime|police|homicide|firearm|\bgun\b|weapon|terror|ransomware|cyber|shooting|violence", "crime_security"),
    (r"court|prison|incarcerat|inmate|sentenc|judici|correction|parole|probation", "justice_courts"),
    (r"immigrat|refugee|asylum|border|visa|deport|migrat", "immigration_migration"),
    (r"emission|climate|\bco2\b|energy|environment|\bepa\b|pollut|storm|weather|noaa|fossil", "energy_environment"),
    (r"contract|procure|solicitation|\brfp\b|vendor|award", "procurement_intl"),
    (r"budget|appropriat|spending|expenditure|outlay|grant", "spending_budget"),
    (r"housing|\brent\b|eviction|mortgage|homeless|zoning|\bhpi\b", "housing_social"),
    (r"school|student|educat|teacher|\buniversit|college|enroll", "education"),
    (r"census|population|demograph|fertility|birth|\bage\b|life expectancy", "geo_demographics"),
    (r"transit|transport|vehicle|traffic|vessel|\bais\b|flight|aircraft|shipping|\bimo\b|\bmmsi\b", "transport_movement"),
    (r"company|corporat|business|\bein\b|\bcik\b|\bsec\b|filing|firm|llc", "corporate_entities"),
    (r"\bloan|\bdebt\b|bank|\bfinance|treasury|\bbond|securit|credit", "money_finance"),
    (r"research|science|\bai\b|technolog|patent|academ|scientif", "science_research"),
    (r"trade|labor|employ|\bwage|unemploy|\bgdp\b|inflation|econom|tariff", "economy_labor_trade"),
    (r"democracy|governance|corruption|freedom|\bunga\b|\bun\b vote|defense spend|military spend", "government_power"),
    (r"histor|culture|heritage|museum|archive|art\b", "history_culture"),
]

RULE_HELP = {
    "banned_but_paid": "OIG-excluded provider appears in payment records",
    "excluded_but_billing": "excluded provider still billing",
    "banned_but_operating": "banned entity still operating",
    "debarred_but_funded": "debarred entity still receiving funds",
    "sanctioned_vessel_broadcasting": "sanctioned vessel still broadcasting AIS",
    "sanctioned_vessel_broadcasting_v2": "sanctioned vessel still broadcasting AIS",
}


# =============================================================== argparse
def add_arguments(parser) -> None:
    parser.add_argument("what", choices=["leads", "domains"],
                        help="which queue to drain: leads (accountability) or domains (catalog)")
    parser.add_argument("--limit", type=int, default=20, help="how many to review this pass (default 20)")
    parser.add_argument("--rule", default=None, help="leads only: filter to one RULE_NAME")
    parser.add_argument("--by", default="", help="reviewer name recorded on each verdict")
    parser.add_argument("--auto-suggest", action="store_true",
                        help="leads only: print the recommendation table and WRITE NOTHING")
    parser.add_argument("--apply", action="store_true",
                        help="domains only: write SOURCE_REGISTRY directly (default stages to JSON)")


# =============================================================== PURE logic (unit-tested)
_DATE_RX = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
_YEAR_RX = re.compile(r"\b(19|20)\d{2}\b")


def exclusion_date_from_title(title: str) -> date | None:
    """Pull the exclusion/effective date a lead's TITLE carries (e.g. '... 2014-01-20 ...').

    That date is the pivot for the recommendation: activity AT OR AFTER it is a live violation;
    activity that predates it is a weaker, later-excluded story."""
    if not title:
        return None
    m = _DATE_RX.search(title)
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def _evidence_list(evidence) -> list[dict]:
    """EVIDENCE is a VARIANT (JSON) -- may arrive as a str or already-parsed list. Normalize to a list."""
    if evidence is None:
        return []
    if isinstance(evidence, str):
        try:
            evidence = json.loads(evidence)
        except Exception:
            return []
    if isinstance(evidence, dict):
        return [evidence]
    if isinstance(evidence, list):
        return [e for e in evidence if isinstance(e, dict)]
    return []


def evidence_years(evidence) -> list[int]:
    """Every 4-digit year appearing in the evidence rows (from 'year' fields or free text)."""
    years: list[int] = []
    for e in _evidence_list(evidence):
        for v in e.values():
            for m in _YEAR_RX.finditer(str(v)):
                years.append(int(m.group(0)))
    return years


def recommend(rule_name: str, title: str, evidence) -> tuple[str, str]:
    """PURE recommendation heuristic. Returns (verdict, one-line-why).

    verdict is one of 'confirm' / 'skip' / 'review' -- a SUGGESTION only; a human still decides.

      * vessel / archive rules  -> skip (archive, not a current-broadcast violation we can stand on)
      * evidence activity on/after the exclusion date -> confirm (timeline supports the violation)
      * evidence predates the exclusion date          -> skip (later-excluded, weaker story)
      * no date or no year to compare                 -> review (needs a human eyeball)
    """
    rn = (rule_name or "").lower()
    if "vessel" in rn or "archive" in rn or "broadcasting" in rn:
        return "skip", "archive/vessel rule -- not a current violation"
    excl = exclusion_date_from_title(title)
    years = evidence_years(evidence)
    if excl is None or not years:
        return "review", "no exclusion date or no dated evidence -- needs a look"
    excl_year = excl.year
    if max(years) >= excl_year:
        return "confirm", f"timeline supports violation (activity {max(years)} >= excluded {excl_year})"
    return "skip", f"later-excluded, weaker (all activity <= {max(years)} < excluded {excl_year})"


# The keystrokes the interactive loop accepts, mapped to the DECISIONS verb they record.
KEY_TO_DECISION = {"c": "confirmed", "r": "rejected"}
# Map the recommendation verb to the keystroke it pre-fills / suggests.
REC_TO_KEY = {"confirm": "c", "skip": "s", "review": ""}


def decision_record_args(lead_id: str, key: str, reviewer: str, reason: str) -> tuple | None:
    """PURE: map a keystroke to the positional args for connect.safety.record(conn, *args).

    Returns None for any key that is not a write (s/skip, q/quit, junk) so the caller writes nothing.
    Order matches record(kind, target_id, decision, reviewer, reason)."""
    decision = KEY_TO_DECISION.get((key or "").strip().lower())
    if decision is None:
        return None
    return ("lead", lead_id, decision, reviewer or "", reason or "")


def leads_fetch_sql(rule: str | None, limit: int) -> tuple[str, tuple]:
    """PURE SQL builder for the active-leads pull. We over-fetch (limit*4, capped) because the
    caller still has to anti-join the DECISIONS 'already ruled' set in Python, and some of the
    fetched rows will drop out there. Returns (sql, params)."""
    over = max(limit * 4, limit)
    over = min(over, 2000)
    where = ["STATUS = 'active'"]
    params: list = []
    if rule:
        where.append("RULE_NAME = %s")
        params.append(rule)
    sql = (
        'SELECT LEAD_ID, RULE_NAME, TITLE, EVIDENCE, EVIDENCE_COUNT, LEFT_KEY_VALUE, '
        'FIRST_SEEN, LAST_SEEN '
        'FROM LIBRARY_META."CONNECT".LEADS '
        f"WHERE {' AND '.join(where)} "
        "ORDER BY SCORE DESC NULLS LAST, EVIDENCE_COUNT DESC "
        f"LIMIT {int(over)}"
    )
    return sql, tuple(params)


def suggest_domain(source_id: str, name: str) -> tuple[str, str]:
    """PURE: guess a governed domain from the source id + human name by keyword. Returns
    (domain, why). Falls back to ('', 'no keyword match -- human call') so we never guess blindly
    into a wrong catalog domain."""
    hay = f"{source_id or ''} {name or ''}".lower()
    for rx, dom in DOMAIN_KEYWORDS:
        if re.search(rx, hay):
            return dom, f"matched /{rx.split('|')[0]}/"
    return "", "no keyword match -- human call"


def domains_fetch_sql(limit: int) -> str:
    """PURE SQL builder: landed/modeled sources still UNCLASSIFIED, the ones that hide the moat."""
    return (
        "SELECT source_id, "
        "COALESCE(name, source_id) AS name, "
        "domain_primary, lifecycle "
        "FROM LIBRARY_META.REGISTRY.CATALOG "
        "WHERE lifecycle IN ('landed','modeled') "
        "AND COALESCE(domain_primary,'UNCLASSIFIED') IN ('UNCLASSIFIED','') "
        "ORDER BY landed_row_count DESC NULLS LAST "
        f"LIMIT {int(limit)}"
    )


def render_evidence(evidence, max_rows: int = 4) -> str:
    """Compact one-line-per-row ASCII render of the EVIDENCE variant for the console."""
    rows = _evidence_list(evidence)
    if not rows:
        return "    (no structured evidence)"
    out = []
    for e in rows[:max_rows]:
        # keep it short + cp1252-safe; join the values we recognize, else dump the dict compactly.
        parts = []
        for k in ("year", "payer", "nature", "amount", "date"):
            if k in e and e[k] not in (None, ""):
                parts.append(f"{k}={e[k]}")
        if not parts:
            parts = [f"{k}={v}" for k, v in list(e.items())[:4]]
        out.append("    - " + ", ".join(str(p) for p in parts))
    if len(rows) > max_rows:
        out.append(f"    ... (+{len(rows) - max_rows} more)")
    return "\n".join(out)


def load_approvals() -> dict:
    try:
        return json.loads(APPROVALS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_approvals(d: dict) -> None:
    APPROVALS_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = APPROVALS_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(d, indent=2), encoding="utf-8")
    import os
    os.replace(tmp, APPROVALS_PATH)


def _clean_unicode(s: str) -> str:
    """The dash between name and status in some titles is a stray glyph; keep console cp1252-safe."""
    return (s or "").encode("ascii", "replace").decode("ascii")


# =============================================================== entry point
def run(args) -> int:
    print(C.header("RIPPLE REVIEW COCKPIT  (COMPUTE_WH -- never fights the pour)"))
    what = getattr(args, "what", None)
    if what == "leads":
        return _run_leads(args)
    if what == "domains":
        return _run_domains(args)
    print("usage: ripple review [leads|domains]")
    return 2


# --------------------------------------------------------------- leads
def _run_leads(args) -> int:
    limit = int(getattr(args, "limit", 20) or 20)
    rule = getattr(args, "rule", None)
    reviewer = getattr(args, "by", "") or ""
    auto = bool(getattr(args, "auto_suggest", False))

    try:
        conn = C.connect()
    except Exception as e:
        print(f"{C.BAD} can't reach Snowflake: {e}")
        print("      leads review needs the CONNECT.LEADS + DECISIONS tables -- try again when it's up.")
        return 1

    try:
        from connect import safety
    except Exception as e:
        print(f"{C.BAD} can't import the safety spine (connect.safety): {e}")
        return 1

    try:
        sql, params = leads_fetch_sql(rule, limit)
        pending_rows = C.dicts(conn, sql, params)
        already = safety.latest(conn, "lead")  # {lead_id: decision} -- anti-join set
        # True queue depth (active minus decided) — NOT the over-fetch buffer size, so this
        # count always agrees with `ripple status`'s "leads pending". One truth, two surfaces.
        total_active = C.scalar(conn, 'SELECT COUNT(*) FROM LIBRARY_META."CONNECT".LEADS '
                                "WHERE STATUS='active'" + (" AND RULE_NAME=%s" if rule else ""),
                                (rule,) if rule else ())
        total_pending = max(0, int(total_active or 0) - sum(1 for d in already.values()
                                                            if d not in (None, "")))
    except Exception as e:
        print(f"{C.BAD} query failed: {e}")
        return 1

    # Drop anything the audit log already ruled on, then take the requested slice.
    fresh = [r for r in pending_rows if r["LEAD_ID"] not in already]
    slice_ = fresh[:limit]

    if not slice_:
        print(f"\n{C.OK} nothing pending" + (f" for rule '{rule}'" if rule else "") + ". Queue is drained.")
        return 0

    print(f"\n{total_pending} lead(s) pending" + (f" (rule={rule})" if rule else "")
          + f"; showing {len(slice_)}.  reviewer: {reviewer or '(unset -- pass --by NAME)'}\n")

    # --auto-suggest: print the recommendation table, WRITE NOTHING.
    if auto:
        data = []
        for r in slice_:
            verdict, why = recommend(r["RULE_NAME"], r["TITLE"], r["EVIDENCE"])
            data.append([r["LEAD_ID"][:20], r["RULE_NAME"][:22],
                         verdict, _clean_unicode(r["TITLE"])[:44], why[:40]])
        print(C.table(["lead_id", "rule", "rec", "title", "why"], data))
        print(f"\n{C.DASH} --auto-suggest: nothing written. Drop the flag to decide interactively.")
        return 0

    # Interactive loop -- a human presses a key for every named person. Never auto-confirm.
    if C.pour_running():
        # DECISIONS lives in Snowflake, not the pour's log -- safe to write. Just flag it.
        print(f"{C.DASH} a pour is live; leads write to CONNECT.DECISIONS (not the pour log) -- ok.\n")

    written = 0
    for i, r in enumerate(slice_, 1):
        verdict, why = recommend(r["RULE_NAME"], r["TITLE"], r["EVIDENCE"])
        print(C.hr())
        print(f"[{i}/{len(slice_)}]  {r['RULE_NAME']}   ({RULE_HELP.get(r['RULE_NAME'], 'lead')})")
        print(f"  {_clean_unicode(r['TITLE'])}")
        print(render_evidence(r["EVIDENCE"]))
        print(f"  RECOMMENDATION: {verdict.upper()} -- {why}")
        suggested = REC_TO_KEY.get(verdict, "")
        prompt = f"  [c]onfirm / [r]eject / [s]kip / [q]uit  (suggest: {suggested or 'review'}) > "
        try:
            raw = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  (input closed) -- stopping.")
            break
        key = (raw[:1] or "").lower()
        reason = raw[1:].strip() if len(raw) > 1 else ""
        if key == "q":
            print("  quitting.")
            break
        rec_args = decision_record_args(r["LEAD_ID"], key, reviewer, reason)
        if rec_args is None:
            print("  skipped." if key in ("s", "") else f"  (unrecognized '{key}') -- skipped.")
            continue
        try:
            safety.record(conn, *rec_args)
            written += 1
            print(f"  {C.OK} recorded: {rec_args[2]}")
        except Exception as e:
            print(f"  {C.BAD} write failed: {e}")

    print(C.hr())
    print(f"{C.OK} done. {written} verdict(s) recorded to CONNECT.DECISIONS; "
          f"{len(fresh) - written} still pending.")
    return 0


# --------------------------------------------------------------- domains
def _run_domains(args) -> int:
    limit = int(getattr(args, "limit", 20) or 20)
    apply_now = bool(getattr(args, "apply", False))

    try:
        conn = C.connect()
    except Exception as e:
        print(f"{C.BAD} can't reach Snowflake: {e}")
        print("      domain review reads LIBRARY_META.REGISTRY.CATALOG -- try again when it's up.")
        return 1

    try:
        rows = C.dicts(conn, domains_fetch_sql(limit))
    except Exception as e:
        print(f"{C.BAD} query failed: {e}")
        return 1

    if not rows:
        print(f"\n{C.OK} no UNCLASSIFIED landed/modeled sources. Catalog domaining is clean.")
        return 0

    mode = "APPLY (writes SOURCE_REGISTRY)" if apply_now else "STAGING (collects to JSON)"
    print(f"\n{len(rows)} UNCLASSIFIED landed source(s); showing {len(rows)}.  mode: {mode}\n")
    if apply_now and C.pour_running():
        # Registry writes are catalog-sensitive; be loud but the pour doesn't lock the registry.
        print(f"{C.DASH} a pour is live. --apply writes one targeted UPDATE per row to SOURCE_REGISTRY.\n")

    approvals = load_approvals()
    staged = 0
    applied = 0
    for i, r in enumerate(rows, 1):
        sid, name = r["SOURCE_ID"], r.get("NAME") or r["SOURCE_ID"]
        dom, why = suggest_domain(sid, name)
        print(C.hr())
        print(f"[{i}/{len(rows)}]  {sid}")
        print(f"  name: {_clean_unicode(str(name))[:64]}   lifecycle: {r.get('LIFECYCLE','')}")
        print(f"  SUGGESTED: {dom or '(none)'}   ({why})")
        prompt = "  [a]pprove / [e]dit <domain> / [s]kip / [q]uit > "
        try:
            raw = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  (input closed) -- stopping.")
            break
        key = (raw[:1] or "").lower()
        if key == "q":
            print("  quitting.")
            break
        chosen = None
        if key == "a":
            chosen = dom
            if not chosen:
                print("  no suggestion to approve -- use [e]dit <domain>. skipped.")
                continue
        elif key == "e":
            typed = raw[1:].strip()
            if typed not in FACET_DOMAINS:
                print(f"  '{typed}' not a governed domain. skipped. (valid: {', '.join(FACET_DOMAINS[:6])} ...)")
                continue
            chosen = typed
        else:
            print("  skipped.")
            continue

        if apply_now:
            try:
                C.rows(conn,
                       "UPDATE LIBRARY_META.REGISTRY.SOURCE_REGISTRY "
                       "SET DOMAIN_PRIMARY=%s, DOMAIN_SOURCE='human', DOMAIN_CONFIDENCE='high', "
                       "NEEDS_TOPIC=FALSE WHERE SOURCE_ID=%s",
                       (chosen, sid))
                conn.commit()
                applied += 1
                print(f"  {C.OK} wrote {sid} -> {chosen}")
            except Exception as e:
                print(f"  {C.BAD} write failed: {e}")
        else:
            approvals[sid] = {"domain": chosen, "why": why, "at": C.now_iso()}
            staged += 1
            print(f"  {C.OK} staged {sid} -> {chosen}")

    print(C.hr())
    if apply_now:
        print(f"{C.OK} done. {applied} row(s) written to SOURCE_REGISTRY (DOMAIN_SOURCE='human').")
    else:
        save_approvals(approvals)
        print(f"{C.OK} staged {staged} approval(s) -> {APPROVALS_PATH}")
        print("  To apply the catalog-sensitive writes, run:")
        print("      python -m ripple review domains --apply")
        print("  (or hand the JSON to scripts/propose_domain_retag.py --apply)")
    return 0
