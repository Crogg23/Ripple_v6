# Fable Audit — 2026-07-02

**What this is:** the durable record of the comprehensive platform audit run by Claude Fable 5 on
2026-07-02 (54 agents, ~3.5M tokens: 8 subsystem readers incl. live read-only Snowflake → 6 critics →
adversarial verification of every negative finding: **18 CONFIRMED, 22 PARTIAL (directionally right,
corrected), 0 REFUTED**). The remediation session is `outputs/INSTRUMENT_HARDENING_PLAN_2026-07-02.md`.

## Live ground truth at audit time (queried, not quoted)
819 landing tables / 243.3M rows / 9.06 GB · CATALOG 1,724 vs registry 1,647 (77 orphans) ·
154 taps (129 landed + 25 modeled) · spine 9.79M entities · LEADS 1,030 across 6 rules ·
DECISIONS 0 · CONFIRMED match rung 0.876 precision @ 0.46 recall · THE_LIBRARY 160 views (exact) ·
median landed source 4 days fresh · budget 32.8/300 credits · June 1,054 ingest runs vs July 44.

## THE PATTERN
Claims backed by a count-gate, acceptance query, or persisted measurement verified EXACTLY
(160 views, 1,645-row backup, 338,520 portal index, MATCH_RUNGS). Claims living only in prose rotted
(124 taps → 154; 353 leads → 1,030; 24.3M rows → 243.3M; 20,696 edges persisted nowhere queryable).
Fix: derive headline numbers (V_STATE), never hand-transcribe.

## Verified BAD findings (condensed; all evidence file:line-cited in the session transcript)
1. **Product loop never closed** — 1,030 leads, 0 human verdicts ever; publishing layer absent by design.
2. **Safety gate is a library, not a chokepoint** — leads.published() had zero consumers;
   dashboard_server/build_dashboard read LEADS raw; RIPPLE_FOR_EVERYONE.md line 9 committed the exact
   time-ordered overclaim the engine refuses in titles; vessel titles implied present tense over a
   years-stale AIS archive.
3. **99.03% lead concentration** — 1,020/1,030 ride LEIE×NPI; EIN detector existed only as a stub.
4. **Pour bleeding** — 51% failure (35/68), ~15 key-class failures through a wrong AUTH_REQUIRED filter;
   'empty' loads retired as complete; recon-minted duplicate source_ids (fed_us_sec_edgar /
   fed_us_usaspending_api) exactly as pour-readiness finding 18 predicted before being deferred.
5. **Landing↔mart drift invisible** — NPPES landing wiped to 700K by an interrupted reload (mart 9.6M);
   AIS landing 58.1M vs mart 7.3M; freshness ledger designed but NOT deployed; measures landing only.
6. **dbt = mirror, not engine** — one full build ever (06-20); CI parse-only; FAKE_LLM fixture committed
   at HEAD broke parse; politics canon Python-built with the dbt mirror already missing 2 marts.
7. **CI red 14 runs** on hallucinated rapidfuzz==9.0.0; PRs #30/#31/#45 merged on red.
8. **Zero scheduling on the actual (Windows) machine** — heartbeat/launchd macOS-only; do-nothing = freeze.
9. **DR guard never ran** — export_control_plane never executed (DR_STAGE absent); control-plane content
   (registry, run log, verdicts) unrecoverable on a DROP; predecessor DB already lost once.
10. **Security nominal** — unattended exec() of LLM code with full os.environ (both secrets);
    ACCOUNTADMIN everywhere; CLAUDE_MCP_READONLY holds CREATE TABLE.
11. **~7 loader generations, contradictory invariants** — empty-registration policies conflict;
    non-atomic chunked writes on live tables; fec_itcont --max-rows smoke would swap a truncated table
    over the live 84M rows; loadkit checkpoint/windowed had zero consumers.
12. **Credential cliff** — PAT 2026-09-20 + SAM key ~09-22 (2 days apart), tracked only in prose;
    five docs still screamed about the already-resolved 07-05 rotation.
13. **Truth drift** — CLAUDE.md self-contradicting scale (~900 vs ~1,647, both wrong live), 5-vs-6
    checkpoints, --queue undocumented; build-state 'latest' stale within a day; no invalidation protocol.
14. **CONFIRMED rung overclaims** — 0.876 precision (1-in-8 wrong), single population, thresholds picked
    on the eval split; safe only because auto-merge/publish are off.

## Instrument COULD-BEs (adopted into the hardening plan)
V_STATE derived state view · persisted CONNECT_EDGES · date-gate capability in the leads engine ·
EIN detector (FED_SEC_EDGAR_FINANCIALS × FED_IRS_BMF) · politics keys (BIOGUIDE/ICPSR/CAND_ID/CMTE_ID)
into the spine · keep-alive tier on Windows (scheduler + heartbeat port + key ledger + DR export) ·
snapshot archiving for temporal deltas (future) · portal-index spine-overlap ranking · receipts-page
generator off published() (future) · LDA lobbying load (loadkit.windowed's intended consumer).

## Deferred (post-pour session)
Full connect rebuild (fingerprint/discover/spine/entity-index) + CONNECT_EDGES population + leads re-run
over the complete poured landing zone; regrade_empty_loads --apply (sampling race vs live pour);
mart schema normalization out of DBT_CROGERS (breaks THE_LIBRARY view FQNs until regenerated);
itcont donor-ER calibration; LDA load execution; git history rewrite (pack size); story/publishing work.
