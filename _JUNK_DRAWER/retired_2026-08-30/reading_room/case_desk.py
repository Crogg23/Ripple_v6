"""The Case Desk — person/entity-grouped review of the hard-ID detectors.

One unit = one person or entity; its case file shows EVERY reviewable lead
about them (the 2026-08-01 audit found 179 people split across up to 3
detector leads). Decisions stay PER-LEAD — each lead is a distinct claim
with its own receipt — so every member lead renders its own decision form,
keyed by lead_id (the stale-click guard: a queue shift orphans an old form's
submit and NO write happens).

Streamlit UI only: no SQL strings here (queries.py), no rendering logic
(render.py), no credential handling (connections.py), shared plumbing in
ui_common.py.
"""
from __future__ import annotations

import streamlit as st

import queries
import render
import ui_common


def _unit_label(by_id: dict):
    def label(uid: str) -> str:
        r = by_id[uid]
        flag = "🛠 " if (r.get("n_needs_work") or 0) > 0 else ""
        badge = f" · {r['n_leads']} leads" if (r.get("n_leads") or 0) > 1 else ""
        conflict = " · ⚠ name conflict" if (r.get("n_name_conflicts") or 0) > 0 else ""
        return (f"{flag}#{r['unit_rank']:>4} · "
                f"{r.get('unit_name') or r['entity_a_key_value']}"
                f"{badge}{conflict} · {(r.get('top_headline') or '')[:90]}")
    return label


def _render_source_records(case: dict):
    """The side-by-side raw-record panels for one lead (ported unchanged
    from the v1 single-desk app)."""
    st.subheader("Source records")
    if case.get("entity_a_key_type") == "NPI":
        left, right = st.columns(2)
        leie = ui_common.read("leie_records", queries.LEIE_SQL,
                              (case["entity_a_key_value"],))
        nppes = ui_common.read("nppes_record", queries.NPPES_SQL,
                               (case["entity_a_key_value"],))
        with left:
            st.markdown("**OIG-LEIE — the ban list** — the row OIG publishes, "
                        "translated (raw values kept in parentheses)  \n"
                        "(`LIBRARY_RAW.LANDING.FED_HHS_OIG_LEIE`)")
            panel = render.source_rows_to_panel(leie, "leie")
            for rec in panel["records"]:
                st.table(rec)
            for note in panel["notes"]:
                st.caption(f"ℹ️ {note}")
        with right:
            st.markdown("**NPPES — the federal provider registry** — the "
                        "independent third source corroborating the identity  \n"
                        "(`LIBRARY_RAW.LANDING.FED_CMS_NPPES`)")
            panel = render.source_rows_to_panel(nppes, "nppes")
            for rec in panel["records"]:
                st.table(rec)
            for note in panel["notes"]:
                st.caption(f"ℹ️ {note}")
        st.markdown(f"**The activity — the money** "
                    f"(`{case.get('entity_b_source')}`)")
        st.table({label: ("—" if case.get(k) is None else str(case.get(k)))
                  for k, label in (
                      ("entity_b_name", "Who paid / reported the activity"),
                      ("n_activity_records", "Payment records"),
                      ("activity_total_usd", "Total dollars"),
                      ("opioid_cost_usd", "Of which opioid drug cost"),
                      ("activity_min_date", "Earliest payment"),
                      ("activity_max_date", "Latest payment"))})
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


def _render_lead_body(case: dict, reviewer: str, can_decide: bool,
                      show_sources: bool):
    """One lead's full case-file body + its own decision form."""
    lead_id = case["lead_id"]

    st.header(case["headline"])
    meta_l, meta_r = st.columns(2)
    meta_l.markdown(f"**Lead** `{lead_id}` · **detector** "
                    f"`{case['detector']}` · **rank** #{case['priority_rank']} "
                    f"(score {case['priority_score']})")
    meta_r.markdown(f"**Tier** `{case['confidence_tier']}` · **timeline** "
                    f"`{case['receipt_verdict']}`")

    if case.get("latest_decision") == "needs_work":
        st.info(f"Flagged **needs work** by {case.get('latest_reviewer')} on "
                f"{case.get('latest_decided_at')} — note: "
                f"{case.get('latest_reason') or '(none)'}")

    if case.get("first_name_conflict"):
        st.warning("**⚠ Identity check needed:** "
                   + render.name_conflict_message(
                       case.get("leie_first_name"),
                       case.get("nppes_first_name")))

    if case.get("caveat"):
        st.warning(f"**Data caveat (travels with this lead):** {case['caveat']}")

    if show_sources:
        _render_source_records(case)

    ev = ui_common.read("evidence_payload", queries.EVIDENCE_SQL, (lead_id,))
    if ev:
        with st.expander(f"Frozen detector evidence "
                         f"({ev[0].get('evidence_count')} items recorded at "
                         f"detection)"):
            st.caption(f"Detector title at detection: {ev[0].get('title')}")
            st.json(ev[0].get("evidence_json") or "[]")

    st.subheader("Why these records are linked")
    for feat in render.linkage_features(case["detector"],
                                        case.get("entity_a_key_type") or "",
                                        case.get("entity_a_key_value") or "",
                                        case["confidence_tier"]):
        st.markdown(f"- {feat}")

    st.subheader("Receipt")
    st.markdown(f"**{case['receipt_verdict']}** — "
                f"{render.VERDICT_TEXT.get(case['receipt_verdict'], '')}")
    for src in render.three_sources(case):
        st.markdown(f"- `{src}`")

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

    # The decision form, keyed by THIS lead (stale-click safe).
    st.subheader(f"Decision — this claim only (`{case['detector']}`)")
    with st.form(key=f"decision_{lead_id}"):
        note = st.text_area("Note (optional — lands in the decision row)",
                            key=f"note_{lead_id}")
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
            params = queries.decision_params(lead_id, clicked, reviewer,
                                             note, case)
        except ValueError as exc:
            st.error(str(exc))
            return
        ui_common.write_decision(queries.INSERT_DECISION_SQL,
                                 queries.CONFIRM_DECISION_SQL,
                                 params, lead_id)


def render_desk(writer_state: str, reviewer: str):
    with st.sidebar:
        st.header("Case Desk filters")
        detector = st.selectbox("Detector", ["(all)"] + queries.DETECTORS)
        tier = st.selectbox("Confidence tier (best lead)",
                            ["(all)"] + queries.TIERS)
        detector = None if detector == "(all)" else detector
        tier = None if tier == "(all)" else tier

    units = ui_common.read(
        "case_queue", *queries.case_queue_sql(detector, tier, limit=20))
    if not units:
        st.success("Case Desk queue is empty for this filter — every "
                   "matching person has a decision on every claim. Change "
                   "the filter, or take the rest of the day.")
        return

    depth_n = units[0]["queue_depth"]
    st.subheader(f"People & entities — showing {len(units)} of {depth_n}")
    st.caption("One row per person/entity; a unit stays here while ANY of "
               "its claims is undecided. Decisions are per-claim inside the "
               "case file.")

    by_id = {r["unit_id"]: r for r in units}
    ui_common.sticky_radio_guard("case_radio", by_id)
    unit_id = st.radio("Pick a case file", list(by_id.keys()),
                       format_func=_unit_label(by_id), key="case_radio",
                       label_visibility="collapsed")
    if unit_id not in by_id:  # defensive: unreachable after the guard
        unit_id = next(iter(by_id))
    unit = by_id[unit_id]

    st.divider()

    # Person header
    st.title(unit.get("unit_name") or unit["entity_a_key_value"])
    st.markdown(f"**{unit['entity_a_key_type']}** "
                f"`{unit['entity_a_key_value']}` · "
                f"**{unit['n_leads']}** claim(s) · best tier "
                f"`{unit.get('best_tier') or '—'}`")
    if (unit.get("n_leads") or 0) > 1:
        st.info("This person/entity appears in **multiple detectors** — "
                "each claim below is decided on its own receipt. Confirming "
                "one does not confirm the others.")

    can_decide = ui_common.decision_gate(writer_state, reviewer)

    member_leads = ui_common.read(
        "person_leads", queries.PERSON_LEADS_SQL,
        (unit["entity_a_key_type"], unit["entity_a_key_value"]))
    if not member_leads:
        st.error(f"No leads found in LEAD_QUEUE for unit {unit_id} — the "
                 "mart may have been rebuilt; refresh the page.")
        return

    # Source records are per-person (same NPI), so pull them once with the
    # top lead; further leads collapse into expanders without re-pulling.
    for i, case in enumerate(member_leads):
        if i == 0:
            _render_lead_body(case, reviewer, can_decide, show_sources=True)
        else:
            st.divider()
            with st.expander(
                    f"Claim {i + 1} of {len(member_leads)} — "
                    f"{case['detector']}: {(case.get('headline') or '')[:110]}",
                    expanded=False):
                _render_lead_body(case, reviewer, can_decide,
                                  show_sources=False)
