# THE PATTERN MAP — what the 1,030 leads actually are, zoomed out

**2026-07-21. Every number below was derived live tonight on the reader lane**
(`RIPPLE_READER` / `SERVE_WH`) by aggregating the queue mart's own SQL to pattern
grain, plus one payment-grain query (printed at the bottom, receipt discipline).
The 1,030 "leads" are not 1,030 stories. **They are four systemic patterns**, and
this file ranks them the way the mission ranks things: by who gets hurt and
whether the data shows it.

---

## THE MAP

| # | pattern (the systemic claim) | scale | receipt strength | what caps it today |
|---|---|---|---|---|
| 1 | **The drug/device industry keeps paying banned providers.** $914,102 across 2,244 payments went to **377 OIG-excluded providers ON/AFTER their exclusion date** (2022–2024 window) | 377 providers, $914k proven-after-ban, 206 still receiving in 2024 | HIGH — hard NPI key, 3-source name agreement on 735/773, payment-vs-exclusion dates both present | None. This one is fully measurable NOW |
| 2 | **Excluded providers still appear as Medicare Part D prescribers.** $63.5M in drug costs (incl. $2.24M opioids) attributed to 236 excluded prescribers; 68 of them six-figure; biggest single $7.5M | ~10× pattern 1's dollars | MEDIUM — hard NPI, 235/236 three-source, **but timeline-blind**: the landing table has no program-year column, so "billed WHILE excluded" cannot be claimed for any of the $63.5M | **One data gap**: land the year-split Part D files. That single land converts $63.5M of "co-occurrence" into a dated pattern |
| 3 | **Sanctioned vessels broadcasting** — 8 hulls, 20,232 AIS position reports | small | LOW as a pattern — the AIS archive is Jan 1–8 2024 and *predates* most of the sanctions listings (reverse causality) | Current AIS data. Until then this is a data-age artifact, not a finding |
| 4 | **Debarred companies still winning federal money** — 2 companies, $1.29M net obligations | **unknowable** | n/a — the SAM exclusions landing table is a 1,000-row capped sample with no dates | The detector is starving. 2 leads is a floor, not a measurement. Land the full SAM file to find out if this pattern is 2 or 2,000 |

*(The 11 `banned_but_operating` leads fold into the health region: their source
table was dropped from LANDING, evidence frozen — a remnant, not a pattern.)*

## PATTERN 1, ONE LEVEL DOWN — it's two mechanisms, not one

The payer-side aggregation (the compliance question: *who* pays banned providers?)
splits the pattern cleanly in two:

| mechanism | signature | top of the ranking (after-ban dollars) |
|---|---|---|
| **Big checks to banned providers** — consulting/royalty-scale engagements that any compliance screen should catch | few payments, huge dollars | **Medtronic: $621k in just 21 payments to 9 excluded providers — 68% of the entire pattern's dollars.** Then Skye Orthobiologics ($114k/1), ConvaTec ($45k/1) |
| **Mass unscreened small payments** — meals/travel flowing to excluded NPIs because nobody checks the LEIE at that grain | many payments, many providers, small dollars | **AbbVie: 223 payments to 71 excluded providers ($22k).** Abbott: 87 payments / 38 providers. ViiV: 101 payments / 5 providers |

By payment year: 2022 = $339k/132 providers · 2023 = $363k/177 · 2024 = $213k/206.
The provider count climbing (132→177→206) is partly mechanical — exclusions
accumulate inside a fixed 2022–24 payment window — so read it as "persistent,"
not proven-growing. Stated so it can't oversell.

## WHAT THE MAP ITSELF SAYS (meta-patterns)

- **98% of the light is on health** (1,009 of 1,030 leads). That is a statement
  about where OUR data is dense, not where harm is — the lamppost, not the city.
  The map's biggest known unknown is pattern 4: it's capped by a 1,000-row sample,
  so the procurement region of the map is effectively dark.
- **The dollars and the receipts live in different patterns.** Pattern 1 has the
  airtight timeline but small dollars ($914k). Pattern 2 has the dollars ($63.5M)
  but no timeline. The single highest-leverage move on this map is the one that
  fixes that: **year-split Part D data.**
- Receipt quality across the map is high: 970 of the 1,009 health leads are
  three-source fact-grade; only 3 leads sit in weak tiers.

## THEN DIG — the order the map suggests

1. **Pattern 1 is ready to be a finding now.** The systemic instrument (after-ban
   dollars by payer, by year) ran tonight and is reproducible below. The top-10
   case review is the *receipt-check step* for this pattern — ten pins to prove
   the map is real — not the deliverable itself.
2. **Land year-split Part D** → unlocks pattern 2's $63.5M timeline. (One source
   land; the biggest single upgrade available.)
3. **Land full SAM exclusions** → un-darkens the procurement region.
4. **Current-year AIS** (or drop the vessel patterns from the map until then).

Where the light points next is yours (RED) — this is the ranked menu, not a plan.

---

## RECEIPT — the pattern-1 instrument (reproducible, reader lane)

```sql
WITH npi_keys AS (
  SELECT DISTINCT left_key_value AS npi
  FROM LIBRARY_META."CONNECT".V_LEADS_PUBLISHED
  WHERE review_state IN ('pending','needs_work') AND rule_name = 'banned_but_paid'
),
leie AS (
  SELECT REGEXP_REPLACE(npi,'[^0-9]','') AS npi, UPPER(TRIM(lastname)) AS lname,
         TRY_TO_DATE(MIN(excldate),'YYYYMMDD') AS excl_date
  FROM LIBRARY_RAW.LANDING.FED_HHS_OIG_LEIE
  WHERE REGEXP_REPLACE(npi,'[^0-9]','') IN (SELECT npi FROM npi_keys)
  GROUP BY 1,2
),
after_ban AS (
  SELECT o.npi, o.payer, o.pay_date, o.amt
  FROM (
    SELECT REGEXP_REPLACE(npi,'[^0-9]','') AS npi,
           UPPER(TRIM(covered_recipient_last_name)) AS lname,
           TRY_TO_DATE(date_of_payment,'MM/DD/YYYY') AS pay_date,
           TRY_TO_DECIMAL(total_amount_of_payment_usdollars,18,2) AS amt,
           applicable_manufacturer_or_applicable_gpo_making_payment_name AS payer
    FROM LIBRARY_STAGING.DBT_CROGERS.INT_OPEN_PAYMENTS_ALL_YEARS
    WHERE REGEXP_REPLACE(npi,'[^0-9]','') IN (SELECT npi FROM npi_keys)
  ) o
  JOIN leie l ON l.npi = o.npi AND l.lname = o.lname
  WHERE o.pay_date >= l.excl_date
)
SELECT payer, COUNT(*) AS n_payments, ROUND(SUM(amt),2) AS usd,
       COUNT(DISTINCT npi) AS n_excluded_providers
FROM after_ban GROUP BY payer ORDER BY usd DESC;
```

Totals query: same CTEs, `SELECT COUNT(*), SUM(amt), COUNT(DISTINCT npi) FROM
after_ban` → **2,244 · $914,101.79 · 377** (first payment 2022-01-04, last
2024-12-31). Same LEIE⋈OP join discipline as the queue mart (NPI + surname,
explicit date formats per the known LEIE traps). The per-detector rollup numbers
above come from aggregating the mart's own SQL (`lead_queue.sql`, sources
hand-substituted, receipt columns NULLed) — the same hand-run proven against the
app earlier tonight in `outputs/HOUR_DOSSIER.md`.
