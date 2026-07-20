---
title: SBA 7(a) — Loan Sizes Chase the Fee Cliff
---

> **BETA — INTERNAL PREVIEW. Not signed off, not published.** Ripple's publish gate is two-step: a human confirms the finding, then records a separate explicit publish verdict. Neither has happened. This page exists so the reviewer can see exactly what would ship.

**Grade: FACT** (the migrating-bunching pattern and its alignment to the rule calendar), carrying the attribution caveats in the caveats section below. Every number on this page was re-derived live against the source table on **2026-07-20** and matched the finding cell-for-cell before being frozen into the committed extracts this page reads. No database, no AI, and no credential sits behind this page at runtime.

## The mechanism, in one sentence

SBA's 7(a) rules put a cost cliff at a specific loan size — and moved it almost every year (zero-upfront-fee at ≤$350k in FY22, ≤$500k in FY23, ≤$1M in FY24–25, a fee step at $2M in FY24 only). Borrowers and lenders size loans to sit at or just under whichever line is active **that year** — so the pile-up in the data *migrates with the rule*: it appears when a cliff arrives at a line and collapses when it leaves.

```sql tiles
select
  (select sum(excess) from sba.excess_table)                                   as excess_loans,
  (select sum(observed)::float / sum(expected) from sba.excess_table)          as x_null,
  (select sum(n_total) from sba.master_grid where fy between 2022 and 2025)    as approvals,
  (select sum(excess)::float from sba.excess_table)
    / (select sum(n_total) from sba.master_grid where fy between 2022 and 2025) as share
```

<BigValue data={tiles} value=excess_loans title="Excess loans parked under active cliffs, FY22–25" fmt="#,##0" />
<BigValue data={tiles} value=share title="Share of all 7(a) approvals in those years" fmt="0.00%" />
<BigValue data={tiles} value=x_null title="Mass in treated windows vs. what no-rule years predict" fmt="0.00&quot;×&quot;" />
<BigValue data={tiles} value=approvals title="7(a) approvals, FY22–25 (the denominator)" fmt="#,##0" />

Back-of-envelope dollar scale (labeled estimate, not a query result): roughly **$3–5B** of loan volume sized to rule lines.

## The migration

The measure: loans in the $20k window at-or-under each round-number line, divided by loans in the $20k window just above it. A round-number magnet is era-stable. A **rule response moves when the rule moves** — which is exactly what happens:

```sql ratios
select
  fy,
  case line when '350k' then '$350k' when '500k' then '$500k'
            when '1m' then '$1M' else '$2M' end as threshold,
  ratio,
  cliff_active
from sba.ratio_grid
order by threshold, fy
```

<LineChart
    data={ratios}
    x=fy
    y=ratio
    series=threshold
    title="Below/above mass ratio at each dollar line, by fiscal year"
    subtitle="Elevated exactly in the years that line carries a cost cliff. FY26 is a partial year (through the 3/31/2026 snapshot)."
    yAxisTitle="below ÷ above (±$20k windows)"
    colorPalette={['#2a78d6','#008300','#e87ba4','#eda100']}
/>

The same numbers as a table — **bold-year map:** $350k carried a cliff in FY22 (zero-fee) and FY26 (underwriting cutoff returned); $500k in FY23–25; $1M in FY23–25; $2M in FY24 only:

<DataTable data={ratios} rows=all>
    <Column id=threshold />
    <Column id=fy />
    <Column id=ratio />
    <Column id=cliff_active title="cliff in force" />
</DataTable>

Read it line by line: **$2M spikes to 26.5 in FY24** — the only year a fee step ever sat there — and sits at 3.2–5.1 in every other year. **$1M jumps 2.8 → 12.6 → 24.3** when the zero-fee cutoff arrives, then collapses back to 2.8 in FY26 when it leaves. The $350k spike returns in FY26 exactly when the streamlined-underwriting cutoff moved back there (SOP 50 10 8, June 2025) — a prediction checked blind against the null design before the rule change was confirmed.

## What the pile-up looks like

FY2020 (no rule at $1M) versus FY2024 (zero-fee cutoff at $1M), loan counts in $10k bins around the line:

```sql hist
select cast(fy as varchar) as fiscal_year, bin_lo, n
from sba.hist_bins
where fy in (2020, 2024) and bin_lo between 900000 and 1090000
order by bin_lo, fiscal_year
```

<BarChart
    data={hist}
    x=bin_lo
    y=n
    series=fiscal_year
    type=grouped
    title="Loan counts in $10k bins around $1,000,000"
    subtitle="FY24: the whole plateau below the line lifts and the mass just above it hollows out — a level shift, not just a round-number spike."
    xFmt="$#,##0"
    colorPalette={['#c3c2b7','#2a78d6']}
/>

This is the shape that kills the "people just like round numbers" story: round-number affection doesn't read fee notices, and it can't lift the *entire* $920k–$1M plateau in exactly one fiscal year (median $10k-bin ratio below-vs-above: **2.65 in FY24 vs 1.26 in the FY20 control**, adjacent bins excluded).

## Why loans move: the notch, in dollars

Crossing $1,000,000 by one dollar in FY24 triggered the upfront guaranty fee on the whole loan:

```sql notch
select
  case bucket
    when '0_below'          then 'Just below ($980k–$1M)'
    when '1_exact_1M'       then 'Exactly $1,000,000'
    when '2_above_1M_1.1M'  then 'Just above ($1M–$1.1M]'
    when '3_above_1.1_1.2M' then 'Above ($1.1M–$1.2M]'
  end as loan_size,
  n as loans,
  med_fee as median_upfront_fee_usd
from sba.notch_1m_fy24
order by bucket
```

<DataTable data={notch} rows=all>
    <Column id=loan_size />
    <Column id=loans fmt="#,##0" />
    <Column id=median_upfront_fee_usd fmt="$#,##0" title="median upfront fee if above the line" />
</DataTable>

At exactly $1,000,000 the fee is $0; at $1,000,001 it's roughly $10,900 — about a 23% effective surcharge on the marginal $50k of borrowing. **485 loans sit at exactly $1,000,000 in FY24**, and the "hole" just above the line (381 loans in $1M–$1.1M vs 551 in $1.1M–$1.2M) is the corroborating scar.

## Did it survive the kill attempts?

The finding went through a seven-killer gauntlet plus three independent hostile re-derivations (full record in the repo's `SYSTEMIC_FINDING.md`). The short version:

- **Not the caps:** the SBA Express cap sat AT $350k in FY19–21 with baseline ratios; the spike lands only in FY22, the fee year. Excluding Express entirely, the $500k response still runs **1.57 → 4.09 → 9.43** (FY22→FY24):

```sql nonexpress
select fy, below_nonexp as below_non_express, above_nonexp as above_non_express,
       round(below_nonexp::float / above_nonexp, 2) as ratio
from sba.nonexpress_500k
order by fy
```

<DataTable data={nonexpress} rows=all />

- **Not the pipeline:** one source file, one load, one SHA-256, one as-of date — a load artifact cannot produce a *temporal migration* inside a single snapshot.
- **Not the base rate:** ten control centers that never carry a rule ($400k, $600k, $750k, $800k, $900k, $1.5M + an independent skeptic's set) stay flat across all eight years — treated ratio-of-ratios 2.91–6.94, controls max 1.52, **no overlap**.
- **Blind predictions held:** the $350k/FY22-only spike, the FY26 collapse at $500k/$1M, and the FY26 $350k re-spike were each stated before the confirming values were looked at.
- **Small tier steps don't bunch:** the FY26 $700k 3%→3.5% boundary shows ratio 1.30, inside its historical band. The mechanism is **zero-fee cliffs and large steps**, not any fee boundary whatsoever.

## The receipt (one case, selected by pre-registered rule)

Selection rule, logged before the gauntlet finished: the **median** loan of the FY24 just-below-$1M class — no cherry-picking. It resolves to:

```sql receipt
select
  borrname as borrower,
  borrcity || ', ' || borrstate as location,
  bankname as lender,
  approvaldate as approved,
  grossapproval as gross_approval_usd,
  sbaguaranteedapproval as sba_guaranteed_usd,
  processingmethod as processing,
  terminmonths as term_months,
  initialinterestrate as initial_rate_pct,
  jobssupported as jobs_supported,
  loanstatus as status
from sba.receipt_case
```

<DataTable data={receipt} rows=all />

A grocery business in suburban Chicago borrowed **exactly $1,000,000 — to the dollar — on October 1, 2023, the first day the zero-fee cutoff moved up to $1,000,000.** One dollar more would have owed ~$10,900 in fees. It is a standard PLP guaranty loan, statistically indistinguishable from the loans just above the line except for its size — and it is the *median* member of its 752-loan class, not an outlier. **Nothing about this loan is improper — that is the point.** The rule moved, and the market's loan sizes moved with it, roughly 6,300 times.

## What would falsify this, and what we could not verify

**Falsifiers:** a future fiscal year placing a zero-fee cliff at a new value with no migration to it; evidence that SBA's FOIA extract re-states approval amounts in a way correlated with fiscal year; proof that at-line loan products predate the incentive at the same share; any headline number failing to reproduce from the verbatim SQL below.

**Not verified, stated plainly:** whether the *borrower* or the *lender* moves the number (the data cannot distinguish; lender concentration analysis shows lenders amplify but don't create the pattern) · FY19–22 annual-service-fee tiers (upfront cutoffs, which carry the finding, were all verified against primary notices) · SBA's enforcement of the 90-day aggregation rule on split-pattern borrowers · FY26 completeness (partial year — all FY26 numbers provisional) · the receipt case's motive (consistent with fee-aware sizing; no document proves intent — the finding is about the class, not the case).

## Frozen receipts

**Source:** `LIBRARY_RAW.LANDING.FED_SBA_LOANS` — SBA 7(a)/504 FOIA file, 2,174,502 rows, single clean load, ASOFDATE 3/31/2026. Filters: `TRIM(PROGRAM)='7A'`, positive parsed `GROSSAPPROVAL`, `APPROVALFY` 2019–2026. **Re-derived live 2026-07-20; zero discrepancies against the committed finding (64 grid cells + totals, all control checks).** The master query, verbatim (Snowflake SQL — every chart above is this query's output, frozen):

<pre><code>WITH loans AS (SELECT APPROVALFY fy, TRY_TO_NUMBER(GROSSAPPROVAL,18,2) g
  FROM LIBRARY_RAW.LANDING.FED_SBA_LOANS
  WHERE TRIM(PROGRAM)='7A' AND TRY_TO_NUMBER(GROSSAPPROVAL,18,2) &gt; 0
    AND APPROVALFY BETWEEN '2019' AND '2026')
SELECT fy, COUNT(*) n_total,
 COUNT_IF(g&gt;330000 AND g&lt;=350000) b350, COUNT_IF(g&gt;350000 AND g&lt;=370000) a350, COUNT_IF(g=350000) at350,
 COUNT_IF(g&gt;480000 AND g&lt;=500000) b500, COUNT_IF(g&gt;500000 AND g&lt;=520000) a500, COUNT_IF(g=500000) at500,
 COUNT_IF(g&gt;980000 AND g&lt;=1000000) b1000, COUNT_IF(g&gt;1000000 AND g&lt;=1020000) a1000, COUNT_IF(g=1000000) at1000,
 COUNT_IF(g&gt;1980000 AND g&lt;=2000000) b2000, COUNT_IF(g&gt;2000000 AND g&lt;=2020000) a2000, COUNT_IF(g=2000000) at2000
FROM loans GROUP BY 1 ORDER BY 1;</code></pre>

**Primary sources:** [SBA 7(a) & 504 FOIA loan data](https://data.sba.gov/dataset/7-a-504-foia) · SBA Information Notices 5000-818641 (FY22 fees), the FY23 fee schedule, 5000-848801 (FY24), 5000-858936 (FY25), 5000-872051 (FY26) — all at [sba.gov/documents](https://www.sba.gov/documents) · [CRS report R41146](https://crsreports.congress.gov/product/pdf/R/R41146) (7(a) program overview) · SOP 50 10 (editions 7 and 8).

**Novelty:** bunching at SBA fee/guarantee thresholds is a known class in the economics literature (Bachas–Kim–Yannelis documented it at the historical $150k line). No published analysis was found (searched 2026-07-13) of the FY2022–26 waiver-cutoff **migration** at $350k/$500k/$1M/$2M. Known class, apparently-unpublished instance.

---

*Ripple beta · finding `sba-7a-cliff-migration` · verified 2026-07-13, re-derived 2026-07-20 · human sign-off: pending · publish verdict: none.*
