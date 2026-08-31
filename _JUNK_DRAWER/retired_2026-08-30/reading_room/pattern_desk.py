"""The Pattern Desk — cohort-grain review of the statistical detector.

The unit of review is the PATTERN: one peer cohort (NAICS-4 x employer size
band) with all its outlier establishments as receipts. One verdict covers
every member lead that has no individual decision; individual lead decisions
always win (specific beats general — enforced by
LIBRARY_META.REVIEW.V_EFFECTIVE_LEAD_DECISIONS, not by this app). Nothing
here can publish: the verdict vocabulary is confirm/reject/needs_work, and
'published' remains a separate per-lead act behind its own gate.

Streamlit UI only: no SQL strings here (queries.py), no rendering logic
(render.py), shared plumbing in ui_common.py. The decision form is keyed by
cohort_id — the same stale-click guard as lead forms.
"""
from __future__ import annotations

import streamlit as st

import queries
import render
import ui_common


def _cohort_label(by_id: dict):
    def label(cid: str) -> str:
        r = by_id[cid]
        flag = "🛠 " if r.get("latest_decision") == "needs_work" else ""
        industry = r.get("industry") or f"NAICS-{r.get('naics')}"
        return (f"{flag}#{r['priority_rank']:>3} · {industry} · "
                f"{r.get('size_band')} employees · "
                f"{r.get('n_outliers')} outliers · worst "
                f"{r.get('worst_fold_plausible') or r.get('worst_fold')}x"
                + (" · ☠" if (r.get('n_deaths_total') or 0) > 0 else ""))
    return label


def render_desk(writer_state: str, reviewer: str):
    with st.sidebar:
        st.header("Pattern Desk")
        st.caption("Workplace-injury outlier cohorts (2024 OSHA Form 300A). "
                   "You are reviewing PATTERNS — one verdict per cohort; "
                   "member establishments are the receipts.")

    cohorts = ui_common.read("cohort_queue", *queries.cohort_queue_sql(limit=20))
    if not cohorts:
        st.success("Pattern Desk queue is empty — every cohort has a "
                   "decision. Take the rest of the day.")
        return

    depth_n = cohorts[0]["queue_depth"]
    st.subheader(f"Cohorts — showing {len(cohorts)} of {depth_n}")

    by_id = {r["cohort_id"]: r for r in cohorts}
    ui_common.sticky_radio_guard("cohort_radio", by_id)
    cohort_id = st.radio("Pick a cohort", list(by_id.keys()),
                         format_func=_cohort_label(by_id), key="cohort_radio",
                         label_visibility="collapsed")
    if cohort_id not in by_id:  # defensive: unreachable after the guard
        cohort_id = next(iter(by_id))

    rows = ui_common.read("cohort_case", queries.COHORT_CASE_SQL, (cohort_id,))
    if not rows:
        st.error(f"Cohort {cohort_id} not found in COHORT_QUEUE — the mart "
                 "may have been rebuilt; refresh the page.")
        return
    cohort = rows[0]

    st.divider()

    # 1 — the pattern headline
    st.header(cohort["headline"])
    meta_l, meta_r = st.columns(2)
    meta_l.markdown(f"**Cohort** `{cohort['cohort_id']}` · **rank** "
                    f"#{cohort['priority_rank']} "
                    f"(score {cohort['priority_score']})")
    meta_r.markdown(f"**Detector** `osha_cohort_outlier_2024` · grain "
                    f"`cohort` (pattern, not person)")

    if cohort.get("latest_decision") == "needs_work":
        st.info(f"Flagged **needs work** by {cohort.get('latest_reviewer')} "
                f"on {cohort.get('latest_decided_at')} — note: "
                f"{cohort.get('latest_reason') or '(none)'}")

    if cohort.get("caveat"):
        st.warning(f"**Data caveat (travels with this cohort):** "
                   f"{cohort['caveat']}")

    # 2 — the cohort stats, every number the verdict rests on
    st.subheader("The pattern in numbers")
    st.table({
        "Peer cohort size (establishments)": str(cohort.get("cohort_n") or "—"),
        "Cohort pooled DART rate": str(cohort.get("cohort_pooled_dart") or "—"),
        "Outliers flagged (member leads)": str(cohort.get("n_outliers") or "—"),
        "Worst fold vs cohort (plausible)": str(cohort.get("worst_fold_plausible") or "—"),
        "Median fold among outliers": str(cohort.get("median_fold") or "—"),
        "Deaths reported by members": str(cohort.get("n_deaths_total") or "0"),
        "Implausible rates (DART > 50)": str(cohort.get("n_implausible") or "0"),
        "States represented": str(cohort.get("states") or "—"),
        "Member keys failing EIN rejoin": str(cohort.get("n_rejoin_failures") or "0"),
    })

    # 3 — receipts: the worst plausible members, drill-down per receipt
    st.subheader("Receipts — the establishments that prove the pattern")
    receipts = render.parse_receipts(cohort.get("receipts_sample"))
    if receipts:
        st.table(render.receipts_table(receipts))
        for r in receipts:
            lid = r.get("lead_id")
            if not lid:
                continue
            with st.expander(f"Full case file — {r.get('title') or lid}",
                             expanded=False):
                case_rows = ui_common.read("receipt_case", queries.CASE_SQL,
                                           (lid,))
                if case_rows:
                    c = case_rows[0]
                    st.markdown(c.get("headline") or "")
                    if c.get("caveat"):
                        st.caption(f"Caveat: {c['caveat']}")
                    st.markdown(f"Lead `{lid}` · rank #{c.get('priority_rank')}"
                                f" · effective decision: "
                                f"`{c.get('latest_decision') or 'pending'}`"
                                f" ({c.get('latest_decision_level') or '—'})")
                else:
                    st.caption(f"Lead `{lid}` is no longer in the queue "
                               "(decided or expired).")
    else:
        st.caption("No plausible-rate receipts to sample — every member of "
                   "this cohort reports an implausible rate. Review the "
                   "member list below.")

    with st.expander("All member establishments (first 100, worst first)"):
        members = ui_common.read("cohort_members", queries.COHORT_MEMBERS_SQL,
                                 (cohort_id, 100))
        for m in members:
            decided = m.get("latest_decision")
            mark = f" · `{decided}` ({m.get('latest_decision_level')})" if decided else ""
            st.markdown(f"- `{m['lead_id']}` "
                        f"{(m.get('headline') or '')[:120]}{mark}")

    # 4 — why this is a pattern, plain English
    st.subheader("Why this is flagged as a pattern")
    for feat in render.cohort_features(cohort):
        st.markdown(f"- {feat}")

    with st.expander("Provenance — formula and grain"):
        st.markdown("**Cohort priority formula** (weights DRAFT v1, "
                    "Checkpoint-1 approval pending) and the cohort rollup "
                    "definition: `models/marts/review/_review__models.yml` "
                    "(model `cohort_queue`). Member-lead receipts carry "
                    "their own frozen SQL in the per-lead case files.")

    # 5 — the cohort decision, blast radius stated plainly
    st.divider()
    st.subheader("Decision — this PATTERN")
    n = cohort.get("n_outliers") or 0
    st.caption(f"This verdict covers **all {n} member leads that have no "
               f"individual decision**. Individual lead decisions always "
               f"win. Confirm = nominate the pattern (nothing publishes); "
               f"Reject = suppress the undecided members; Needs work = keep "
               f"everything visible, flagged.")

    can_decide = ui_common.decision_gate(writer_state, reviewer)

    with st.form(key=f"cohort_decision_{cohort_id}"):
        note = st.text_area("Note (optional — lands in the decision row)")
        c1, c2, c3 = st.columns(3)
        submitted = {
            "confirm": c1.form_submit_button("✅ Confirm pattern",
                                             disabled=not can_decide,
                                             use_container_width=True),
            "reject": c2.form_submit_button("❌ Reject pattern",
                                            disabled=not can_decide,
                                            use_container_width=True),
            "needs_work": c3.form_submit_button("🛠 Needs work",
                                                disabled=not can_decide,
                                                use_container_width=True),
        }
    clicked = next((k for k, v in submitted.items() if v), None)
    if clicked:
        try:
            params = queries.cohort_decision_params(cohort_id, clicked,
                                                    reviewer, note, cohort)
        except ValueError as exc:
            st.error(str(exc))
            return
        ui_common.write_decision(
            queries.INSERT_COHORT_DECISION_SQL,
            queries.CONFIRM_COHORT_DECISION_SQL,
            params, cohort_id,
            flash_suffix=(f" Covers {n} member leads without individual "
                          f"decisions."))
