"""Ripple — The Reading Room. Streamlit UI ONLY: no SQL strings in this file
(queries.py owns SQL), no rendering logic (render.py owns it), no credential
handling (connections.py owns the two lanes).

Run:  ./reading_room/run.sh   (or: streamlit run reading_room/app.py)
Local only. Nothing here can publish; verdicts are nominations, and the
write role physically cannot update or delete rows.

Stale-click safety: the decision buttons live in a st.form whose key is the
lead_id being rendered — if the queue shifts between the render the reviewer
saw and their click (another decision landed, the mart rebuilt), the old
form's submit is orphaned by its key and NO write happens. A verdict can
only ever land on the lead whose case file produced the button.
"""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))

import connections  # noqa: E402
import queries  # noqa: E402
import render  # noqa: E402

st.set_page_config(page_title="Ripple — The Reading Room", page_icon="🗂️",
                   layout="wide")


def _friendly_error(e: Exception) -> str:
    """A plain-English one-liner for a reviewer, with the raw exception tucked
    into an expander for anyone who needs to debug it. Was: raw Snowflake/
    driver exception text shown directly as the primary error."""
    s = str(e).lower()
    if any(t in s for t in ("closed", "expired", "no longer exists", "reset by peer",
                            "could not connect", "operationalerror")):
        return "Can't reach the warehouse right now — it may have gone idle. Try again in a moment."
    if "not authorized" in s or "insufficient privileges" in s:
        return "This role doesn't have access to that data."
    if "compilation error" in s or "syntax error" in s:
        return "That query isn't valid SQL — this is a bug, not something you did."
    return "Something went wrong talking to the warehouse."


def _show_error(banner, e: Exception, label: str = "details"):
    banner(_friendly_error(e))
    with st.expander(label, expanded=False):
        st.code(str(e))


# ── lanes (cached per process; cleared + retried once if Snowflake killed
#    an idle session, so one expired connection never bricks the app) ────────
@st.cache_resource
def _reader():
    return connections.reader_connect()


@st.cache_resource
def _writer():
    return connections.writer_connect()


def _read(name: str, sql: str, params: tuple = ()):  # -> list[dict]
    """Reader-lane query with the mandated failure UX: errors carry the
    query NAME, never a blank page. Retries exactly once on a dead cached
    connection (idle-killed sessions are normal weather)."""
    for attempt in (1, 2):
        try:
            cur = _reader().cursor()
            cur.execute(sql, params or None)
            cols = [d[0].lower() for d in cur.description]
            return [dict(zip(cols, r)) for r in cur.fetchall()]
        except Exception as exc:
            if attempt == 1:
                _reader.clear()  # drop the dead connection, reconnect once
                continue
            _show_error(st.error, exc, label=f"query '{name}' — details")
            st.stop()


# ── header + lane banners ───────────────────────────────────────────────────
st.title("The Reading Room")
st.caption("lead review surface · every headline is a fixed SQL template · "
           "decisions are append-only rows, enforced by the database, not "
           "this app")

# Success flash from the previous run (st.rerun() wipes inline messages).
if st.session_state.get("flash"):
    st.success(st.session_state.pop("flash"))

writer_state, writer_msg = connections.writer_status()
if writer_state != "ready":
    st.warning(f"**Read-only mode.** {writer_msg}")

# ── sidebar: filters + reviewer ─────────────────────────────────────────────
with st.sidebar:
    st.header("Queue filters")
    detector = st.selectbox("Detector", ["(all)"] + queries.DETECTORS)
    tier = st.selectbox("Confidence tier", ["(all)"] + queries.TIERS)
    detector = None if detector == "(all)" else detector
    tier = None if tier == "(all)" else tier
    st.divider()
    reviewer = st.text_input("Reviewer (required to decide)",
                             value=st.session_state.get("reviewer", ""))
    st.session_state["reviewer"] = reviewer

# ── queue screen ────────────────────────────────────────────────────────────
queue = _read("queue", *queries.queue_sql(detector, tier, limit=20))

if not queue:
    st.success("Queue is empty for this filter — every matching lead has a "
               "decision. Change the filter, or take the rest of the day.")
    st.stop()

depth_n = queue[0]["queue_depth"]  # same query, same snapshot as the rows below
st.subheader(f"Queue — showing {len(queue)} of {depth_n}")

# Radio identity: OPTIONS ARE LEAD IDS (stable), labels are cosmetic via
# format_func — so a queue reorder can't silently remap the selection.
by_id = {r["lead_id"]: r for r in queue}


def _label(lid: str) -> str:
    r = by_id[lid]
    flag = "🛠 " if r.get("latest_decision") == "needs_work" else ""
    return (f"{flag}#{r['priority_rank']:>4} · {r['detector']} · "
            f"{(r['headline'] or '')[:110]}")


if st.session_state.get("queue_radio") not in by_id:
    # Sticky widget value from a prior render (e.g. the just-decided lead
    # dropped out of the queue on rerun) — clear it before st.radio
    # reconciles session_state against the new options, which otherwise
    # raises instead of falling back to a default.
    st.session_state.pop("queue_radio", None)

lead_id = st.radio("Pick a case file", list(by_id.keys()),
                   format_func=_label, key="queue_radio",
                   label_visibility="collapsed")
if lead_id not in by_id:  # defensive: should be unreachable after the pop above
    lead_id = next(iter(by_id))

# ── case file ───────────────────────────────────────────────────────────────
case_rows = _read("case_file", queries.CASE_SQL, (lead_id,))
if not case_rows:
    st.error(f"Lead {lead_id} not found in LEAD_QUEUE — the mart may have "
             "been rebuilt; refresh the page.")
    st.stop()
case = case_rows[0]

st.divider()

# 1 — the headline, big and first
st.header(case["headline"])
meta_l, meta_r = st.columns(2)
meta_l.markdown(f"**Lead** `{case['lead_id']}` · **detector** "
                f"`{case['detector']}` · **rank** #{case['priority_rank']} "
                f"(score {case['priority_score']})")
meta_r.markdown(f"**Tier** `{case['confidence_tier']}` · **timeline** "
                f"`{case['receipt_verdict']}`")

if case.get("latest_decision") == "needs_work":
    st.info(f"Flagged **needs work** by {case.get('latest_reviewer')} on "
            f"{case.get('latest_decided_at')} — note: "
            f"{case.get('latest_reason') or '(none)'}")

if case.get("caveat"):
    st.warning(f"**Data caveat (travels with this lead):** {case['caveat']}")

# 2 — side-by-side source records, every field: flag side vs activity side
st.subheader("Source records")
if case.get("entity_a_key_type") == "NPI":
    left, right = st.columns(2)
    leie = _read("leie_records", queries.LEIE_SQL,
                 (case["entity_a_key_value"],))
    nppes = _read("nppes_record", queries.NPPES_SQL,
                  (case["entity_a_key_value"],))
    with left:
        st.markdown("**OIG-LEIE — the ban** "
                    "(`LIBRARY_RAW.LANDING.FED_HHS_OIG_LEIE`)")
        for rec in render.source_rows_to_panel(leie, "leie")["records"]:
            st.table(rec)
    with right:
        st.markdown("**NPPES — the registry** "
                    "(`LIBRARY_RAW.LANDING.FED_CMS_NPPES`)")
        for rec in render.source_rows_to_panel(nppes, "nppes")["records"]:
            st.table(rec)
    st.markdown(f"**The activity — the money** "
                f"(`{case.get('entity_b_source')}`)")
    st.table({k: ("—" if case.get(k) is None else str(case.get(k)))
              for k in ("entity_b_name", "n_activity_records",
                        "activity_total_usd", "opioid_cost_usd",
                        "activity_min_date", "activity_max_date")})
else:
    a, b = st.columns(2)
    a.markdown(f"**Flagged entity** — `{case.get('entity_a_source')}`")
    a.table({k: ("—" if case.get(k) is None else str(case.get(k)))
             for k in ("entity_a_name", "entity_a_key_type",
                       "entity_a_key_value", "entity_a_location")})
    b.markdown(f"**Activity side** — `{case.get('entity_b_source')}`")
    b.table({k: ("—" if case.get(k) is None else str(case.get(k)))
             for k in ("entity_b_name", "n_activity_records",
                       "activity_total_usd", "activity_min_date",
                       "activity_max_date")})

ev = _read("evidence_payload", queries.EVIDENCE_SQL, (lead_id,))
if ev:
    with st.expander(f"Frozen detector evidence "
                     f"({ev[0].get('evidence_count')} items recorded at "
                     f"detection)"):
        st.caption(f"Detector title at detection: {ev[0].get('title')}")
        st.json(ev[0].get("evidence_json") or "[]")

# 3 — linkage features, plain English
st.subheader("Why these records are linked")
for feat in render.linkage_features(case["detector"],
                                    case.get("entity_a_key_type") or "",
                                    case.get("entity_a_key_value") or "",
                                    case["confidence_tier"]):
    st.markdown(f"- {feat}")

# 4 — receipt verdict + its sources
st.subheader("Receipt")
st.markdown(f"**{case['receipt_verdict']}** — "
            f"{render.VERDICT_TEXT.get(case['receipt_verdict'], '')}")
for src in render.three_sources(case):
    st.markdown(f"- `{src}`")

# 5 — provenance footer: the full chain, zero black boxes
with st.expander("Provenance — the full chain from raw record to headline"):
    st.markdown(f"**Confidence tier definition** — "
                f"{render.TIER_DEFS.get(case['confidence_tier'], '')}")
    st.markdown("**The exact frozen query that produced this lead** "
                f"(SHA-256 `{case.get('sql_sha256') or '—'}`, as of "
                f"{case.get('lead_as_of_date') or '—'}):")
    st.code(case.get("evidence_sql") or
            "(receipt columns reach the safe view once "
            "scripts/provision_review_lane.sql is applied)", language="sql")
    st.caption("Priority formula and template text: "
               "models/marts/review/_review__models.yml — deterministic, "
               "documented, versioned.")

# 6 — the three buttons, inside a form KEYED BY THIS LEAD (stale-click safe)
st.divider()
st.subheader("Decision")

if writer_state == "ready" and not (reviewer or "").strip():
    st.info("Enter your reviewer name in the sidebar to enable the buttons.")
can_decide = writer_state == "ready" and bool((reviewer or "").strip())

with st.form(key=f"decision_{lead_id}"):
    note = st.text_area("Note (optional — lands in the decision row)")
    c1, c2, c3 = st.columns(3)
    submitted = {
        "confirm": c1.form_submit_button("✅ Confirm",
                                         disabled=not can_decide,
                                         use_container_width=True),
        "reject": c2.form_submit_button("❌ Reject",
                                        disabled=not can_decide,
                                        use_container_width=True),
        "needs_work": c3.form_submit_button("🛠 Needs work",
                                            disabled=not can_decide,
                                            use_container_width=True),
    }
clicked = next((k for k, v in submitted.items() if v), None)

if clicked:
    try:
        params = queries.decision_params(lead_id, clicked, reviewer, note,
                                         case)
        try:
            wcur = _writer().cursor()
            wcur.execute(queries.INSERT_DECISION_SQL, params)
        except Exception:
            _writer.clear()  # dead cached connection — reconnect once
            wcur = _writer().cursor()
            wcur.execute(queries.INSERT_DECISION_SQL, params)
        verdict, reviewer_clean = params[1], params[3]
        wcur.execute(queries.CONFIRM_DECISION_SQL, (lead_id, reviewer_clean))
        landed = wcur.fetchone()
        if not landed:
            st.error("Insert reported success but the decision row is not "
                     "readable back — do NOT retry blindly; check "
                     "LIBRARY_META.REVIEW.DECISIONS.")
        elif landed[0] != verdict:
            # A newer row from this same reviewer already landed (e.g. a
            # double-submit from two tabs) between our write and this
            # read-back — the row we just wrote is real, but it is not the
            # latest one anymore. Say so instead of flashing the wrong verdict.
            st.warning(
                f"Your **{verdict}** on `{lead_id}` was written, but a newer "
                f"decision (**{landed[0]}** by {landed[1]} at {landed[2]}) "
                f"has since landed for this reviewer on this lead — that one "
                f"wins. Append-only: nothing was lost, but check the row.")
            st.rerun()
        else:
            st.session_state["flash"] = (
                f"Recorded **{landed[0]}** on `{lead_id}` by {landed[1]} at "
                f"{landed[2]} — append-only, latest verdict wins. (A repeat "
                f"click would add a harmless duplicate row, never corrupt.)")
            st.rerun()  # refetch the queue — the decided lead drops out NOW
    except Exception as exc:
        _show_error(st.error, exc, label="write failure details")
        if "expired" in str(exc).lower() or "auth" in str(exc).lower():
            st.info(connections.WRITER_REMEDIATION)
