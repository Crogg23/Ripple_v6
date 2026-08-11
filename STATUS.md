# RIPPLE STATUS — 2026-08-11 (evening) — the connection audit: is a match TRUE?

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE: one thing, and it is not from this session.** The roll-call vote
metadata is modeled into two tables that disagree (113,512 rows vs 3,364). The
code was repointed during the morning repair session but one table was never
rebuilt, and it CANNOT be rebuilt with dbt — a standing guard refuses because
that table mirrors a Python-built canonical one and dbt would overwrite
reconciled numbers. The offline test suite has been failing on this since the
repair session. The fix is re-running the Python builder; not forced past the
guard.

**What this session was:** the first measurement of the layer every story rides
on — when Ripple says two records are the same company, is that true? Full
detail: `reports/spine_connection_audit_2026-08-11.md`.

**Headlines:**

1. **One real wrong merge, found and fixed.** A placeholder tax ID of all nines
   had fused CVS Pharmacy, SK Telecom, Kingsway Financial, Enstar Group and a
   literal "TEST Company" into a single entity spanning 16 sources. The
   normalizer rejected all-zeros but not all-nines or keyboard walks. Fixed in
   both copies (engine + reading room), guards red-first.
2. **The banned-but-operating work was reading 5% of the banned list.** The
   spine and that lens still pointed at the 9,000-row capped debarment sample
   three weeks after — and four hours after — the full 167,928-row list landed
   under a new name. Repointed. Debarred firms holding federal contracts: **53
   before, 102 after.**
3. **Where joins fire, they are honest.** Debarred-firm-to-contract on the
   12-character federal entity ID: 99 of 102 have matching company names on both
   sides. Excluded-provider-to-pharma-payment on provider ID: 336 of 350 exact
   surname matches, and all 14 others are hyphen/spacing variants of the same
   person. 93.9% of 806M spine input rows carry a usable hard key.
4. **Fifty-four stale copies of the matching rule, found and regenerated.** The
   rule that cleans an ID before matching is copied into dozens of build files
   so the warehouse can run without Python. Those copies were nearly three weeks
   behind: they turned junk text into plausible-looking IDs that pointed at
   entities the who's-who had correctly refused to create — a join to nothing,
   silently. All regenerated, and one new test now checks every copy at once.
5. **Three dead sources removed from the who's-who** (a retired credit-union
   file, FCC licensing, NSF awards) — their ID columns were usable on zero rows.
6. **Recall gap found, deliberately NOT wired:** a fuller federal-contracts copy
   would raise debarred-with-awards from 102 to 343 — but that copy is itself
   truncated at a suspiciously round 20 million rows. Repointing to a known-short
   table trades one wrong number for another; it needs a clean re-pull first.

**Live/open items:**

- Disaster-aid reload still running, healthy (~21.5M of 25.9M). Post-landing
  chain unchanged.
- Every fix above is code-side. **None of it is in the warehouse until the
  who's-who build re-runs** — see YOUR MOVE.
- Chris's earlier one-liner list is still outstanding
  (`reports/repair_session_chris_gates_2026-08-11.md`).

**YOUR MOVE:**

1. **The one decision: re-run the who's-who build?** ~4.5 hours on the small
   warehouse, roughly **$10–15**. It is a full rebuild, not a catch-up: the
   placeholder fix changes how every ID is canonicalized, so a partial run would
   leave the bad merges in place. Until it runs, the 32M-entity map and the
   debarment lens keep serving the old, wrong-in-two-ways state. Say go and it
   starts; say wait and nothing breaks further.
2. Still open from this morning: the one-liner list, and go/no-go on the two
   priced FDA pulls.

**NEXT SESSION:**

1. Boot trust check; finish the disaster-aid chain if it landed.
2. If Chris said go: run the who's-who rebuild, then re-measure the same
   precision numbers against the rebuilt layer.
3. Otherwise: the roll-call mart rebuild via its Python builder, and the two
   recall gaps (uncapped contracts pull, IRS 990 e-file index).

**Tests:** offline suite 2,851 passing, none failing. The one live failure (the
roll-call mart above) is the pre-existing one from this morning.

**COST:** well under $1 of warehouse credit (sampling and metadata queries only,
small warehouse throughout). No agents. No spend without a price tag.
