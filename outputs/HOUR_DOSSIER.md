# THE HOUR DOSSIER — everything you need before the top-10 review

> **Altitude note (added after Chris's 07-21 correction):** this is the *manual for
> the plumbing*, deliberately granular — read it only when you sit down to click.
> The zoomed-out view comes first and lives in `outputs/PATTERN_MAP_2026-07-21.md`:
> the 1,030 leads are four systemic patterns, and the top-10 review is the
> receipt-check step for pattern #1 (industry payments to banned providers), not
> the deliverable. The case serves the map.

**Written 2026-07-21, verified against the actual code and the live warehouse that
evening.** Every command, query, and screen element below was either executed this
session or read directly from the committed code. Where something could not be run
(because it isn't provisioned yet), it says so in plain words.

---

## 0. WHERE THINGS STAND TONIGHT (read this first)

**The app is built and its reads work. The review itself can't start yet.** Two
things are missing, both yours, both in `CLOSE_THE_LOOP_checklist.md`:

1. **The decisions table doesn't exist.** `LIBRARY_META.REVIEW` (schema, DECISIONS
   table, writer role) is not in the warehouse — confirmed live tonight. That's
   checklist **Step 1** (run `scripts/provision_review_lane.sql` in Snowsight as
   ACCOUNTADMIN) plus **Step 2** (mint the `RIPPLE_REVIEW_PAT` and put it in
   `library-onboarding/.env`). Right now that PAT is **not** in `.env` — also
   confirmed tonight — so the app would open in read-only mode.
2. **The queue mart doesn't exist.** `LIBRARY_MARTS.DBT_CROGERS.LEAD_QUEUE` is not
   in the warehouse — confirmed live tonight. That's checklist **Steps 4–7** (build
   lane grants, then `dbt build --select marts.review`).

If you launch the app before those steps, you get a clean error page naming the
missing object, not a blank screen. Nothing breaks; it just can't show a queue that
hasn't been built.

**One bug was found and fixed tonight** (green-lane): the app clamps every session
with `USE SECONDARY ROLES NONE`, but Snowflake **refuses that command on
role-restricted PATs** — which is what all our PATs are. As committed, the app
could not open at all (live error: "Current session is restricted. USE ROLE not
allowed"), and verdict writes would have failed the same way mid-review. The fix in
`reading_room/connections.py` accepts the restricted session only after proving it
has zero secondary roles active (checked live: it does). All 15 offline tests pass,
and the app's own reader lane was connected live tonight as `RIPPLE_READER` on
`SERVE_WH`. Uncommitted in the working tree — commit when you're happy.

**The good news:** the leads are real and waiting. 1,030 pending leads sit in the
safe view tonight, and I ran the queue mart's exact SQL by hand on the reader lane
— the full case file for lead #1 is in section 4, precisely as it will appear.

---

## 1. HOW TO LAUNCH IT

```bash
cd /Users/chrisr./Documents/GitHub/Ripple_v6
./reading_room/run.sh
```

That's the whole thing. Notes, all verified tonight:

- **No install needed** — the dependencies (streamlit 1.50.0, the Snowflake
  connector) are already on this Mac's Python. If a fresh machine ever complains
  `command not found: streamlit`, run `pip install -r reading_room/requirements.txt`.
- **No `.env` swap needed.** The app ignores `SNOWFLAKE_PAT` entirely. Reads ride
  `SNOWFLAKE_SERVE_PAT` (in `.env` now, pinned to role `RIPPLE_READER`); verdict
  writes ride `RIPPLE_REVIEW_PAT` (the Step-2 mint) pinned to
  `RIPPLE_REVIEW_WRITER`, and the code raises rather than borrow any other
  credential. Even if `.env` is mid-checklist-swap to the build lane, the Reading
  Room is immune — that was proven executably on 2026-07-21 (receipts in
  `BETA_DECISIONS_2026-07-20.md`, Step 1 of the follow-up).
- The script serves **http://127.0.0.1:8890** — local only, nothing exposed. If
  your browser doesn't open by itself, open that address. (The control panel owns
  8899; they don't collide.)
- The terminal keeps running the server; leave it open. Ctrl-C stops the app.

## 2. WHAT YOU'RE LOOKING AT WHEN IT LOADS

*(This section describes the committed UI code, `reading_room/app.py` — the app
can't render a real queue until the mart is built, so this is code-verified, not
screenshot-verified.)*

- **Title bar:** "The Reading Room", with a one-line caption reminding you that
  headlines are fixed SQL templates and decisions are append-only database rows.
- **Yellow banner (only if something's off):** "Read-only mode…" means
  `RIPPLE_REVIEW_PAT` is missing — you can browse but not decide.
- **Left sidebar:** two dropdown filters (**Detector**, **Confidence tier**, both
  defaulting to "(all)") and a **Reviewer** text box. Type `chris` in that box —
  **the three decision buttons stay greyed out until a reviewer name is entered.**
- **Main area, top:** "Queue — showing 20 of 1,030" (top 20 by priority; the
  filters narrow it). Below that, a pick-list where each line is one lead:
  rank · detector · first ~110 characters of the headline. Click a line to open
  its case file below. A 🛠 prefix means someone already flagged it needs-work.
- **Main area, below the divider:** the full case file for whichever lead is
  selected (walkthrough in section 4), ending with the three buttons.

## 3. WHAT A LEAD IS

One row saying: **an entity that appears on a federal "flagged" list also appears
in a federal "activity" record, matched on a hard government ID** (NPI, UEI, IMO
hull number, or EIN — never name-matching). The lead is the co-occurrence plus the
frozen evidence for it. It is *not* an accusation; the review is where a human
decides if it's worth pursuing.

Tonight's queue, counted live from the safe view:

| detector | pending | in plain words |
|---|---|---|
| banned_but_paid | 773 | OIG-excluded provider still appears in drug/device-industry payment records (Open Payments) |
| excluded_but_billing | 236 | OIG-excluded provider appears in the Medicare Part D prescriber file |
| banned_but_operating | 11 | OIG-excluded provider was listed as affiliated with CMS facilities (source table since dropped — evidence frozen) |
| sanctioned_vessel_broadcasting_v2 | 6 | Sanctioned vessel (by IMO hull) appears in the Jan-2024 AIS coastal archive |
| sanctioned_vessel_broadcasting | 2 | Older version of the same rule — superseded, ranked near the bottom |
| debarred_but_funded | 2 | SAM-debarred company (by UEI) appears on federal contract transactions |

## 4. ONE REAL LEAD, TOP TO BOTTOM

This is the actual #1 lead in tonight's queue — produced by running the mart's own
SQL by hand on the live warehouse. When the mart is built, this is the top line
you'll see, rendered exactly like this:

**In the pick-list:**

> \#   1 · banned_but_paid · Mohammed Hadi, excluded from federal health programs 2024-10-20 (Conviction of a Medicare/…

**The case file below it:**

- **Headline (big):** "Mohammed Hadi, excluded from federal health programs
  2024-10-20 (Conviction of a Medicare/Medicaid program-related crime), appears in
  210 drug/device industry payment records totaling $4,779 — latest payment
  2024-12-10."
- **Meta line:** Lead `LEAD_0681071f13d241b7` · detector `banned_but_paid` ·
  rank #1 (score 6.5) — Tier `FACT_GRADE_3_SOURCE` · timeline
  `PAID_ON_OR_AFTER_EXCLUSION`
- **Source records**, side by side, every field shown, blanks as "—":
  - *Left:* the OIG-LEIE ban row for NPI **1275760100** — name, exclusion type
    `1128a1`, exclusion date, city/state (Old Westbury NY), specialty.
  - *Right:* the NPPES registry row for the same NPI — legal name **Mohammed
    Hadi** (it matches — that's what makes this three-source).
  - *Below:* the activity — payers "ABBVIE INC., Abbott Laboratories, Allergan,
    Inc.", **210 records, $4,779.27 total, spanning 2022-01-05 → 2024-12-10**,
    opioid cost $0.
- **Frozen detector evidence** (expander): the 48 evidence items the detector
  recorded at detection time, as raw JSON, plus its original title.
- **Why these records are linked:** exact match on NPI (unique, never reused) on
  BOTH lists, plus surname agreement across all 3 sources — "the corroboration a
  fat-fingered ID can't fake."
- **Receipt:** **PAID_ON_OR_AFTER_EXCLUSION** — "The latest recorded payment is ON
  or AFTER the exclusion date — activity while banned." With the three source
  tables listed.
- **Provenance** (expander): the tier definition and the frozen SQL that produced
  the lead. *Note: until the provision script re-points the safe view, this box
  shows a placeholder instead of the SQL — expected, says so on screen.*
- **Decision:** an optional note box and the three buttons.

## 5. WHERE THAT LEAD CAME FROM

- **The detector** is a fixed SQL rule named `banned_but_paid`, defined in
  `connect/leads_specs.py` and executed by the `connect` engine (`python -m
  connect leads --run`) on the build lane. No AI anywhere in the path — the rule
  is: join the OIG exclusion list (`FED_HHS_OIG_LEIE`) to the all-years CMS Open
  Payments union (43.3M rows, counted tonight) **on NPI**, require the surname to
  match too, one lead per hit, evidence frozen at detection.
- **This batch** was detected 2026-06-26→28 (the lead's own first/last-seen
  timestamps).
- **The queue mart** (`lead_queue.sql`, dbt) then re-computes every number you see
  **fresh from the source tables** — it never trusts the detector's capped
  evidence — and adds: the confidence tier (does NPPES corroborate the name?),
  the timeline verdict (latest payment vs. exclusion date), the fixed-template
  headline, and the priority score.
- **The priority score is arithmetic, not judgment:** tier weight (3-source = 3.0)
  + timeline weight (paid-after-ban = 2.0) + detector weight (1.0 here) + a small
  tiebreak. That's how #1 got 6.5, the maximum for this detector.

## 6. THE THREE BUTTONS

| button | writes verdict | what you're saying |
|---|---|---|
| ✅ Confirm | `confirmed` | "I checked the case file; the pattern is real in these records and worth keeping." **This is a private nomination — it does NOT publish.** |
| ❌ Reject | `rejected` | "This is junk / the data doesn't support it." The lead leaves the queue and the safe view stops serving it. |
| 🛠 Needs work | `needs_work` | "Can't call it yet — something needs checking." The lead **stays in the queue**, flagged 🛠 with your note attached. |

**What you are promising on Confirm — precisely:** a `confirmed` row in an
append-only audit table with your name on it. Nothing more. Publishing is a
separate, deliberate act (`python scripts/publish_lead.py <LEAD_ID> --by chris
--reason "…" --apply`), which refuses unless the latest verdict is `confirmed`.
One click cannot put anything on a public surface — that's the two-step gate you
ruled in on 07-20 (B1).

## 7. HOW TO JUDGE ONE — good vs. junk

Concrete checks, in the order the screen presents them:

1. **Do the names agree?** The tier tells you: `FACT_GRADE_3_SOURCE` = same
   surname on all three federal sources for that ID — strong. `NPPES_CONFLICT` =
   the registry shows a *different* surname — often a "Smith Md Pc" suffix
   artifact, sometimes a real identity problem. Look at the two name fields
   yourself before trusting either way.
2. **Does the timeline actually say "while banned"?** `PAID_ON_OR_AFTER_EXCLUSION`
   is the strong verdict. `PAYMENTS_PREDATE_EXCLUSION` means all the money came
   *before* the ban — much weaker as a pattern, usually a reject or needs-work.
3. **Read the caveat box — it can gut the lead.** Vessel leads: the AIS data is a
   Jan 1–8 2024 snapshot that *predates* most 2025-26 sanctions — an appearance is
   history, never "currently broadcasting." Debarment leads: SAM table is a
   1,000-row capped sample with no dates. These caveats travel with the lead
   because they change what the lead can honestly claim.
4. **Is the money what the headline implies?** Open Payments "payment records" are
   mostly industry meals, travel, and consulting fees. 210 records / $4,779 (lead
   #1) = a drug-rep-lunch pattern after exclusion — real, but the *size* is part
   of the judgment. Check `activity_total_usd` and, for Part D leads,
   `opioid_cost_usd`.
5. **`LEIE_ROW_MISSING` tier: check OIG's site first.** The exclusion row has
   vanished from the current monthly LEIE file — the ban may have been lifted
   (reinstatement). Confirming one of these without checking is the classic trap.
6. **When torn: Needs work with a note.** It's non-destructive, keeps the lead
   visible, and your note shows up flagged for next time.

**Junk signature:** predate-exclusion timeline + tiny dollars + name conflict +
a caveat that removes the claim. **Good signature:** three-source tier +
paid-after-ban timeline + activity that continues well past the exclusion date.

## 8. WHAT HAPPENS AFTER YOU CLICK

- One row is INSERTed into `LIBRARY_META.REVIEW.DECISIONS`: your verdict, your
  name, your note, a timestamp, and a snapshot of exactly what the screen showed
  you (so the decision stays interpretable after the queue rebuilds).
- The app reads the row back and shows a green confirmation naming verdict, lead,
  reviewer, time. The queue refreshes; confirmed/rejected leads drop out
  immediately, needs-work leads stay flagged.
- **Undo: write the right verdict on top.** The table is append-only — nothing is
  ever edited or deleted (the writer role physically holds no UPDATE/DELETE) —
  and **the latest verdict wins**. A misclicked Needs-work is easy: the lead is
  still in the queue, open it and decide again. A misclicked Confirm or Reject
  drops the lead out of the queue, so the app can't re-show it — the correction
  is one INSERT of the right verdict into `REVIEW.DECISIONS` (run it in Snowsight
  as the review role, or note the LEAD_ID and hand it to the next Claude session
  to write). Your misclick stays in the audit log forever — by design — but it
  stops *counting* the moment a newer row lands.
- **Double-click / stale click: harmless by construction.** A repeat click adds a
  duplicate row (same verdict, latest still wins). If the queue shifted between
  render and click, the buttons belong to the old form and the click lands
  nowhere — no write happens to the wrong lead.

## 9. HOW YOU KNOW YOU'RE DONE

Goal (from the checklist): **verdicts on the top 10 queue rows.** All-rejects
still counts — that's a finding about detector precision, not failure.

The official measure, runnable in Snowsight or any lane (verified live tonight —
currently returns 0):

```sql
SELECT METRIC, VALUE
FROM LIBRARY_META.REGISTRY.V_STATE
WHERE METRIC = 'decisions.total';
```

**VALUE ≥ 10 = done.** (Counts every decision row except the smoke test, so
duplicate clicks inflate it slightly. The exact ten-distinct-leads check, which
exists once Step 1 has run: `SELECT COUNT(*) FROM
LIBRARY_META.REVIEW.V_LATEST_DECISIONS;`)

Afterwards, per the checklist: export the decisions to git
(`python scripts/export_review_decisions.py`) so the verdicts are backed up
off-warehouse.

## 10. WHAT BREAKS, AND WHAT TO DO

| what you see | what it means | fix |
|---|---|---|
| Yellow "Read-only mode… mint a fresh PAT" banner | `RIPPLE_REVIEW_PAT` missing/expired in `.env` (it is missing tonight) | Checklist Step 2: mint PAT for `RIPPLE_REVIEW_WRITER` in Snowsight, add to `library-onboarding/.env`, restart the app |
| Red "Reader query 'queue' failed: … LEAD_QUEUE does not exist or not authorized" | The mart isn't built (tonight's state), or built but the reader grant wasn't re-run | Checklist Step 7 (`dbt build --select marts.review`), then re-run the **last line** of `provision_review_lane.sql` |
| Red "… 'queue' failed: … REVIEW … does not exist" | Step 1 never ran | Run `scripts/provision_review_lane.sql` in Snowsight as ACCOUNTADMIN |
| Buttons greyed out, blue hint about reviewer name | Reviewer box in the sidebar is empty | Type your name in the sidebar |
| Red "Write failed: … expired / auth" | Review PAT expired mid-session (normal weather) | Re-mint, update `.env`, restart — the app prints these exact steps |
| Clicked, nothing happened, no message | Queue shifted between render and click; the stale form was orphaned **on purpose** | Re-select the lead, decide again |
| "Insert reported success but the decision row is not readable back" | Ambiguous write | **Don't blind-retry.** Check `LIBRARY_META.REVIEW.DECISIONS` in Snowsight for the row first |
| "Port 8890 is already in use" | Another Streamlit still running | `READING_ROOM_PORT=8891 ./reading_room/run.sh`, or kill the old terminal |
| First query hangs ~10s then works | `SERVE_WH` waking up / idle-killed session | Nothing — the app reconnects once automatically |
| A decided lead is still listed, flagged 🛠 | That's needs_work — non-suppressing by design | Nothing; it drops out when it gets a confirm/reject |

---

## APPENDIX — what was verified how (honesty ledger)

- **Executed live tonight (reader lane, `RIPPLE_READER` on `SERVE_WH`):** the
  app's own `reader_connect()`; queue composition (1,030 pending by detector);
  the full mart SQL by hand → the #1–#5 leads and the complete #1 case-file row;
  `V_STATE` done-query (returns 0); absence of `LIBRARY_META.REVIEW.*` and
  `LEAD_QUEUE`; absence of `RIPPLE_REVIEW_PAT` in `.env`; presence of streamlit
  1.50.0 + connector; 15/15 offline tests after the clamp fix.
- **Read from committed code, not run:** the Streamlit screen layout (`app.py`,
  `render.py` — the UI cannot render a queue until the mart exists), the button →
  INSERT path (`queries.py`), `publish_lead.py`'s guards, the checklist steps.
- **Cannot be verified until provisioning:** the write path end-to-end (needs
  Steps 1–2), the mart build (Step 7), and whether the frozen `evidence_sql`
  reaches the provenance box after the view re-point (Step 1 + rebuild — if it
  still shows the placeholder after Step 7, flag it, don't debug mid-review).
