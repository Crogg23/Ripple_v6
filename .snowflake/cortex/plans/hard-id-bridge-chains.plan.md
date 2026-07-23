---
name: "hard id bridge chains"
created: "2026-07-23T05:17:14.030Z"
status: pending
---

# Plan: Hard-ID Bridge Chains

## The standard (this overrides everything below)

Matches must be **beyond a reasonable doubt**. Surrogate/derived keys are built from **EXACT components only** — hard government IDs, exact codes. **No fuzzy name matching. No approximate date windows.** Those are explicitly deferred to a future "mild-signal detection" phase and are out of scope here. Every bridge in this plan is an exact ID equality (`A.NPI = B.NPI`), so false-positive risk is structurally near-zero.

## Context

- **The bridge machinery exists but is starved.** [connect/bridge.py](<> "c:\Code\Ripple_v6\connect\bridge.py") builds `BRIDGE`-tier edges via `_build_crosswalk()` / `discover_bridged()`, gated by `HARD`/`CODE`/`SPINE` sets and `_valuable()` (requires both ends HARD). It currently produces only `CCN~NPI` (159 edges) and `CIK~EIN` (**1 edge**).
- **Smoking gun (read-only spike, done):** SEC sources (`FED_SEC_EDGAR`, `SEC_FILING_SUBMISSIONS`) carry `CIK + EIN` together in thousands of rows, yet only 1 `CIK~EIN` bridge exists. The raw material is present; the builder isn't consuming it. This is a plumbing bug to diagnose, not missing data.
- **Available exact bridges in the warehouse (spike results):** `NPI~CCN` (CMS facility affiliation, Open Payments), `EIN~CIK` (SEC EDGAR), `NPI~UEI` (`FED_SAM_EXCLUSIONS`). Two islands today: health `{NPI, CCN, UEI}` and corporate `{CIK, EIN}`, one `EIN`-link from fusing.
- **Spine is hard-ID-only by design** ([connect/spine.py](<> "c:\Code\Ripple_v6\connect\spine.py")) — exact-ID clustering, zero false merges. Bridge chains are the same nature: **facts**, not probabilistic leads.
- **Control-table philosophy holds:** durable pairs belong in a warehouse table (like `CONNECT_EDGES`, `SOURCE_REGISTRY`), regenerable by plain SQL, no runtime AI. Precedent derived-key models: [int\_sanctioned\_vessels.sql](<> "c:\Code\Ripple_v6\library-onboarding\ripple_dbt\models\intermediate\int_sanctioned_vessels.sql"), [politics\_\_member\_crosswalk.sql](<> "c:\Code\Ripple_v6\library-onboarding\ripple_dbt\models\marts\politics\politics__member_crosswalk.sql").

## The target chain

```mermaid
flowchart LR
    CIK["CIK (public co / SEC filer)"] -->|"EIN~CIK  SEC EDGAR"| EIN["EIN (org tax id)"]
    EIN -->|"KEYSTONE: EIN~UEI  USASpending?"| UEI["UEI (federal contractor)"]
    UEI -->|"NPI~UEI  SAM exclusions"| NPI["NPI (provider)"]
    NPI -->|"NPI~CCN  Open Payments / affiliation"| CCN["CCN (facility)"]
```

Every arrow is exact-ID equality. The dashed keystone (`EIN~UEI` or `EIN~CCN`) is the one link to confirm in the spike.

## Implementation steps

### 1. Feasibility spike — full crosswalk inventory + diagnose the bug (read-only)

- Extend the ID-co-occurrence scan across raw landing AND staging to enumerate every table carrying 2+ hard IDs, and **count distinct exact ID-pairs per table** (not just presence).
- Hunt the keystone: does any landed source carry `EIN + UEI` or `EIN + CCN` (USASpending recipient files, hospital cost reports — their EIN column may be named `TAX_ID`/`PRVDR_*`)? Confirm it exists and its pair-count.
- Diagnose why `CIK~EIN` = 1 edge: is the SEC source in the bridge builder's input set? Is `_valuable()` or the `HARD`/`CODE`/`SPINE` gating dropping it? Read [connect/bridge.py](<> "c:\Code\Ripple_v6\connect\bridge.py") against the live data.
- Exit gate: a concrete list of buildable exact bridges with real pair-counts, and a named root cause for the `CIK~EIN` gap.

### 2. Build a durable crosswalk table (`ENTITY_XWALK`)

- New dbt intermediate model(s) that extract exact `(id_type_a, id_value_a, id_type_b, id_value_b, source_table)` rows from every crosswalk-bearing source, normalized via [connect/keys.py](<> "c:\Code\Ripple_v6\connect\keys.py") (`normalize_sql`) so IDs match the engine's canonical form. Follow the `int_sanctioned_vessels` / `member_crosswalk` pattern (`view`, `source()` refs, header comment documenting each pair's provenance).
- One canonical, deduped table = the "Rosetta stone." Durable in the warehouse, rebuildable, no runtime AI.

### 3. Fix and extend the bridge builder to consume it

- Point [connect/bridge.py](<> "c:\Code\Ripple_v6\connect\bridge.py") at `ENTITY_XWALK` (or fix its existing input path) so it emits a `BRIDGE` edge for every exact pair — unblocking `CIK~EIN` from 1 to its true count.
- Verify `discover_bridged()` transitivity chains multi-hop (CIK->EIN->UEI->NPI->CCN) rather than only direct pairs; extend if it stops at one hop.
- Keep `_valuable()`'s "both ends HARD" rule — that IS the beyond-reasonable-doubt guardrail. Do not loosen it to admit fuzzy keys.

### 4. Register any new ID/bridge types

- If the keystone introduces a pair not yet known (e.g. `EIN~UEI`), add it through the intended triad: `KEY_TOKENS` ([portal\_recon/tag\_portal\_index.py](<> "c:\Code\Ripple_v6\portal_recon\tag_portal_index.py")), `NORM_RULES` ([connect/keys.py](<> "c:\Code\Ripple_v6\connect\keys.py")), `KEY_DOMAIN` ([connect/discover.py](<> "c:\Code\Ripple_v6\connect\discover.py")). `validate_key_config()` enforces the triad.

### 5. Prove ONE chain end-to-end

- Traverse `CIK -> EIN -> (UEI) -> NPI -> CCN` for a real starting entity and surface a cross-domain connection no single dataset held.
- Verify every hop is exact equality (bridge confidence = 1.0 / tier `BRIDGE`, no probabilistic rung). Spot-check 5-10 traversals by hand: is each hop genuinely the same real-world entity?

### 6. Hold the fact-vs-finding line

- The **chain is a fact** (exact identity) and can live in the graph/spine layer, no review needed.
- Any **finding built on a chain** (e.g. "this federal contractor is a subsidiary of a sanctioned parent") is still a **lead** -> must route through the existing confirm->publish firewall ([connect/safety.py](<> "c:\Code\Ripple_v6\connect\safety.py")). Nothing auto-publishes. Publishing stays Chris's call.

### 7. Deferred (explicitly out of scope now)

- Fuzzy `NAME`, `NAME@ZIP`, `NAME@YEAR`, address-as-entity, approximate date windows -> a separate future "mild-signal detection" phase, clearly labeled as below-the-bar and never auto-promoted to findings.

## Verification

- **Spike:** produces a concrete buildable-bridge list with pair-counts and a named `CIK~EIN` root cause; keystone `EIN~UEI`/`EIN~CCN` confirmed present or confirmed absent.
- **Crosswalk table:** `dbt build` succeeds; row counts per ID-pair are sane; IDs are normalized (no stray formatting mismatches).
- **Bridge rebuild:** `CIK~EIN` edge count jumps from 1 to its real magnitude; new pairs appear; every bridge edge has exact-match confidence (no probabilistic tier sneaks in).
- **Chain traversal:** one multi-hop chain returns a correct, hand-verifiable cross-domain result.
- **Regression:** existing `CONNECT_EDGES` / spine / receipt tests still pass; no existing edge counts silently change except the intended `CIK~EIN` fix.

## Critical Files

- [connect/bridge.py](<> "c:\Code\Ripple_v6\connect\bridge.py") - crosswalk + bridge building; the `CIK~EIN` diagnosis and the multi-hop extension live here
- [connect/discover.py](<> "c:\Code\Ripple_v6\connect\discover.py") - `KEY_DOMAIN`, `validate_key_config()`, edge persistence
- [connect/keys.py](<> "c:\Code\Ripple_v6\connect\keys.py") - `NORM_RULES` / `normalize_sql` for canonical ID normalization in the crosswalk
- [library-onboarding/ripple\_dbt/models/intermediate/int\_sanctioned\_vessels.sql](<> "c:\Code\Ripple_v6\library-onboarding\ripple_dbt\models\intermediate\int_sanctioned_vessels.sql") - template for the `ENTITY_XWALK` derived-key model
- [connect/safety.py](<> "c:\Code\Ripple_v6\connect\safety.py") - the firewall any chain-derived finding must route through
