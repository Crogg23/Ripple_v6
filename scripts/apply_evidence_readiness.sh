#!/usr/bin/env bash
# apply_evidence_readiness.sh — run the full evidence.dev-readiness sequence in one pull.
#
# Built 2026-07-07. Every step is a preview-tested --apply script that snapshots a rollback
# to outputs/ before it mutates. This runner just chains them in the ONE correct order and
# STOPS on the first failure so nothing runs against a half-applied state.
#
#   bash scripts/apply_evidence_readiness.sh          # asks once, then runs
#   bash scripts/apply_evidence_readiness.sh --yes    # unattended
#
# NOT included (do these yourself — see notes at the end):
#   * revoke_straggler_pats.py  — irreversible token drops; confirm nothing authenticates via
#     the 5 targets first, then: python3 scripts/revoke_straggler_pats.py --apply
#   * Snowsight serving-PAT mint — a session can't mint its own PAT (err 099413).
set -u
cd "$(dirname "$0")/.."                 # repo root
PY=python3

step() {                                # step "label" cmd...
  local label="$1"; shift
  echo ""
  echo "══════════════════════════════════════════════════════════════════════"
  echo "▶ $label"
  echo "══════════════════════════════════════════════════════════════════════"
  if ! "$@"; then
    echo ""
    echo "✖ STEP FAILED: $label"
    echo "  Nothing after this ran. Check the error, roll back via the outputs/ snapshot"
    echo "  if needed, fix, and re-run — every step is idempotent."
    exit 1
  fi
}

echo "This applies 8 warehouse/file steps to make the Library evidence.dev-ready:"
echo "  1 reconcile OP2022 (13.25M rows live)      5 giant pre-agg marts (14)"
echo "  2 V_CONNECTIONS_CORE view                  6 reconcile + TYPE the reading room"
echo "  3 retire the IRS_EO_BMF 2x dup             7 measure join keys (82 sources)"
echo "  4 rebuild 7 frozen marts (926k rows)       8 generate evidence pages"
echo "Each snapshots a rollback to outputs/ first. Runs as your Snowflake PAT (ACCOUNTADMIN)."
if [ "${1:-}" != "--yes" ]; then
  printf "\nType YES to proceed: "; read -r ok
  [ "$ok" = "YES" ] || { echo "aborted."; exit 0; }
fi

# 1-2 · free fires (independent, reversible)
step "1/8 · reconcile OP2022 -> 13.25M rows live"        $PY scripts/reconcile_op2022.py --apply
step "2/8 · V_CONNECTIONS_CORE (4,308 trustworthy edges)" $PY scripts/build_v_connections_core.py --apply

# 3-5 · data fixes + marts (must precede the reconcile in step 6)
step "3/8 · retire IRS_EO_BMF exact 2x dup"              $PY scripts/dedup_irs_eo_bmf.py --apply --prune-edges
step "4/8 · rebuild 7 frozen marts (~926k rows)"         $PY scripts/rebuild_frozen_marts.py --apply
step "5/8 · 14 giant pre-agg marts (+ FRIENDLY_LAYER_EXTRAS)" $PY scripts/build_giant_aggs.py --apply

# 6 · the atomic reconcile + type (prunes the retired irs_eo_bmf view, keeps agg views, types 123)
step "6a/8 · reading-room inventory"                     $PY scripts/thelibrary_inventory.py
step "6b/8 · reconcile + TYPE reading room (~8.5 min)"   $PY scripts/thelibrary_build.py --apply --typed

# 7 · catalog join keys
step "7/8 · measure JOIN_KEYS_STD (82 sources)"          $PY scripts/backfill_join_keys_std.py --apply

# 8 · evidence pages (needs typed views + agg marts from steps 5-6)
step "8/8 · generate evidence.dev pages"                 $PY scripts/gen_evidence_pages.py --apply

echo ""
echo "══════════════════════════════════════════════════════════════════════"
echo "✅ ALL 8 STEPS DONE — the Library is evidence.dev-ready."
echo "   Left for you (can't be scripted):"
echo "   • Mint the serving PAT in Snowsight (RIPPLE_READER, 90d), then swap evidence off"
echo "     ACCOUNTADMIN:  cp evidence/sources/library/connection.yaml.serve \\"
echo "                       evidence/sources/library/connection.yaml"
echo "     and put the token (base64) in connection.options.yaml + .env SNOWFLAKE_SERVE_PAT."
echo "   • Optional security hygiene (irreversible): python3 scripts/revoke_straggler_pats.py --apply"
echo "   • Rebuild the site:  npm --prefix evidence run sources && npm --prefix evidence run build"
echo "══════════════════════════════════════════════════════════════════════"
