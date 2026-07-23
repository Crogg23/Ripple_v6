# Ripple — Session Handoff (2026-07-23)

Plain-English rundown of what happened this session so anyone can pick it up cold.

---

## TL;DR (read this if nothing else)

- We set out to build "creative connections" across the data. Along the way we discovered the **real bottleneck isn't ideas — it's that most data sources were only *sampled* (a few rows peeked), not fully loaded.**
- We couldn't finish the loading fix because it needs a **write-capable Snowflake login + internet access**, and the saved login is read-only. That part is parked on Chris.
- Instead we proved the machine works by building **3 real, beyond-reasonable-doubt findings** on data that was *already* loaded clean — all live in a new `LIBRARY_MARTS.FINDINGS` schema.
- **Two things Chris must do:** (1) rotate the leaked credentials, (2) run the pour + typing sweep from an admin session to unblock the bigger stuff.

---

## How the session went (the arc)

1. **Full audit** of the repo + warehouse. Big picture: a genuinely deep, well-engineered platform (287M rows, a 12.9M-entity spine, a research-grade matching engine) sitting on a shaky, mostly-untyped-TEXT foundation, with a publishing layer that's fully built but has **never once published** (`decisions.total = 0`).
2. Chris pointed at **Boxes 1 & 2** of his mental model — "collect all the data" and "connect it" — and asked for a wide-net re-audit of just those.
3. We got into **"creative connections"** — the idea of making join keys where none exist (his old "encounter ID + sedation time" trick).
4. Chris set a hard rule: **matches must be beyond a reasonable doubt. Exact IDs only. No fuzzy name/date guessing.** (Saved to memory.)
5. We tried to build **hard-ID bridge chains** (company → hospital → doctor). **Dead end** — no shared exact ID exists in the loaded data to connect those worlds.
6. Every ambitious cross-domain play kept dying on the **same rock: the good sources are sample stubs** (FARA = 30 rows, NSF = 125 rows) or have empty ID columns (Foreign Aid = 4M rows, blank EIN).
7. Chris chose to **attack the loading bottleneck**. We mapped exactly how loading works and hit the credential wall (below).
8. Pivoted to delivering value on what's *already* loaded → built the **FINDINGS schema**.

---

## What we actually BUILT (all live, all reversible views)

New schema: **`LIBRARY_MARTS.FINDINGS`** — home for beyond-reasonable-doubt "finding candidates." Every object here is a **LEAD** (an exact-ID match), NOT a published claim. Human review required before anything goes public. Read access granted to `RIPPLE_READER` + `CLAUDE_MCP_READONLY`.

| View | What it flags | Count | Who gets hurt |
|---|---|---|---|
| `REVOKED_BUT_DEDUCTIBLE` | Charities the IRS auto-revoked, never reinstated, but STILL flagged tax-deductible in the master file | **22,512 orgs** (~$6.7B revenue, $15.5B assets) | Donors giving "deductible" money to orgs that lost their status |
| `REVOKED_BUT_DEDUCTIBLE_BY_STATE` | State-level map of the above | 59 states/terr | (the map layer) |
| `EXCLUDED_PROVIDER_PAID_AFTER_EXCLUSION` | OIG-banned providers who got industry money in a year *after* their ban | **287 providers** (~$512K) | Patients/taxpayers |
| `EXCLUDED_PROVIDER_AT_FACILITY` | Banned providers still tied to Medicare facilities | **28 facilities** (10 providers) | Patients at those facilities |
| `CATALOG` | Self-documenting index of every finding + harm + live count | 3 findings | (navigation) |

**How they were built:** each is a plain SQL view joining two already-loaded landing tables on an *exact* government ID (EIN or NPI), with the LEIE `NPI = 0000000000` "libel trap" excluded. No fuzzy matching anywhere.

### Important honesty note on Finding #1
The 22,512 splits into two flavors, and the view has a `review_bucket` column marking them:
- **Long tail** (small churches, scholarship funds, rescues, booster clubs) — the clean donor-harm story.
- **Whales** (revenue > $10M) — mostly hospital LLCs and universities revoked years ago; these are usually corporate *reorganizations*, not fraud, and must be reviewed one by one. Don't publish the whales as-is.

---

## What we FOUND (the important truths)

- **The loading bottleneck is the #1 constraint on everything.** Of ~2,840 catalog sources: only ~30 are fully modeled, ~171 landed, and ~2,300 were only scouted/sampled. The connect engine is a Ferrari being fed a thimble of gas.
- **Why sources are stuck:** when each source was onboarded, the auto-generated download code was told to grab only a small sample page. Nobody went back to pour the full barrel. There's no "sample vs full" toggle — you re-onboard in `chunked` mode to get everything.
- **The two IRS tables** (master exempt file 1.97M, revocation list 1.2M) are the *only* org tables with both real volume AND clean IDs — which is why the strongest finding came from them.
- **The cross-domain dream (money world ↔ health world) can't be built yet** — no loaded table shares an exact ID between them. Needs a new "keystone" source (e.g. a file carrying both a tax ID and a provider ID) to be poured.

---

## BLOCKED — needs Chris (can't be done by the agent)

1. **SECURITY — rotate credentials.** The `library-onboarding/.env` was shared into chat with a **live Anthropic API key and a live Snowflake PAT in plaintext**. Both should be revoked/rotated. (This matches the standing build-state "leaked PAT" blocker defect.) Chris said he'll rotate at the next phase — **do not forget.**
2. **The FARA pour** (fully load the foreign-agents source). Needs the onboarding pipeline, which reaches the internet and writes to the warehouse — the saved PAT is read-only so it can't. Run it yourself:
   ```
   cd c:\Code\Ripple_v6\library-onboarding
   # ensure .env has a WRITE-capable PAT + SNOWFLAKE_WAREHOUSE=DBT_WH
   $env:ONBOARD_SKIP_IF_UNCHANGED="0"
   python onboard.py --name FED_FARA --include-landed --skip-dbt --yes
   ```
3. **The typing sweep** (fix the ~80%-TEXT problem so joins work everywhere). The safe script is reserved for an ACCOUNTADMIN session:
   ```
   python scripts\thelibrary_typed_views.py          # preview (no writes)
   python scripts\thelibrary_typed_views.py --apply  # the real thing
   ```
   Rough cost: preview ~free; full apply ~5–12 credits (about one of your normal build days). All warehouses are X-Small (1 credit/hr, auto-suspend 60s), so spend is small.

---

## Credential situation (why the agent kept hitting walls)

- The Python scripts authenticate with the **PAT in `.env`, which is scoped to `RIPPLE_READER` (read-only)** — confirmed: Snowflake refused to let it act as ACCOUNTADMIN.
- The agent's *own* Snowflake connection (the in-IDE one) IS ACCOUNTADMIN — that's how the FINDINGS views got built. Chris authorized using it for this build phase, planning to rotate after.
- Net: the **safe, script-based** pour/typing needs a write-capable PAT; the agent's direct connection can do SQL writes but can't reach the internet (so it can't pour external sources).

---

## Decisions locked in this session (saved to project memory)

- **Matching standard:** beyond a reasonable doubt, exact IDs only, no fuzzy name/date matching. (Fuzzy = a possible future "mild signal" phase, never promoted to a finding.)
- **Fact vs. finding:** an exact-ID match is a *fact*; the story built on it is a *lead* that needs human sign-off. Nothing auto-publishes.
- Findings live in `LIBRARY_MARTS.FINDINGS` as reversible views.

---

## Suggested next steps (pick up here)

1. **Rotate the two credentials.** First. Always.
2. **Run the FARA pour + typing sweep** from an admin session → then ping the agent to verify (row counts jumped, types converted, and re-check whether a cross-domain finding now fires).
3. **Pressure-test the long-tail bucket** of `REVOKED_BUT_DEDUCTIBLE` (spot-check ~12, rule out reorg artifacts) to make it review-ready.
4. **Walk one finding through the review → publish path** — the pipeline's never fired once (`decisions.total = 0`). The revoked-charities long tail is the strongest candidate for a first Evidence.dev page.
5. **Optional cleanup:** convert the FINDINGS views into proper dbt models so they live in the pipeline instead of as standalone views (avoids drift).

---

*Everything above is also in project memory (`/memories/projects/Code-Ripple-v6/`): matching-standard, loading-and-creds, findings-delivered.*
