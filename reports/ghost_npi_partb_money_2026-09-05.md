# Part B — where the money landed, 2026-09-05

Follow-up on NPIs `1285673012` and `1871571406`. Queries through the Python door,
`connect/db.py`. Scripts: `scratchpad/hunt16.py`, `hunt17.py`.

**Headline: the payee is not in the data, and it is not obfuscation — CMS does
not publish it. No public CMS file in this warehouse carries a payee TIN, an EIN,
or a billing organization. Every one of these files is keyed on the rendering
individual.**

**What the Part B table does show is the number: $1,229,994.33 paid to Medicare
under Miranda's NPI, 90% of it for drugs he bought and billed. Aswad has no
Part B row at all.**

---

## 1. Who is the exact payee?

Answered directly: **there is no payee column.**

The full column list of
`FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER` is 83 columns. The
identity block is:

| Column | Holds |
|---|---|
| `RNDRNG_NPI` | the rendering individual's NPI |
| `RNDRNG_PRVDR_LAST_ORG_NAME` | last name, or org name if entity code is O |
| `RNDRNG_PRVDR_FIRST_NAME`, `_MI`, `_CRDNTLS` | person fields |
| `RNDRNG_PRVDR_ENT_CD` | **I** = individual, **O** = organization |
| `RNDRNG_PRVDR_ST1`, `_ST2`, `_CITY`, `_STATE_ABRVTN`, `_ZIP5` | practice address |
| `RNDRNG_PRVDR_TYPE` | specialty |
| `RNDRNG_PRVDR_MDCR_PRTCPTG_IND` | participating indicator |

The remaining 76 columns are service counts, dollar amounts, beneficiary
demographics and chronic-condition percentages. **No payee. No TIN. No EIN. No
group NPI. No billing entity.**

### The warehouse-wide check

Scanned every `FED_CMS_%` table in `LIBRARY_RAW.LANDING` for any column matching
`%PAYEE%`, `%TIN%`, `%EIN%`, `%BILLING%` or `%TAX%`.

| What the scan found | Reality |
|---|---|
| `FED_CMS_NPPES.EMPLOYER_IDENTIFICATION_NUMBER_EIN` | 100% empty, already proven |
| `FED_CMS_HCRIS.PAYROLL_TAXES_PAYABLE` | a hospital cost-report line item |
| `FED_CMS_HPT_MRF.BILLING_CODE` | a procedure code |
| Everything else | matched on `NATIND`, `RATING`, `TAXONOMY`, `ATTRIBUTES` |

**Not one real payee or tax identifier exists across every CMS table landed.**

### Why — the mechanism, not the label

CMS's public use files are built from claims and then de-identified at the
*payee* level, not the provider level. The rendering NPI is published because it
is already public in NPPES. The billing TIN is a taxpayer identifier and CMS
withholds it from every public release.

This is a **publication rule, not a corporate structure.** The information does
not exist in any public CMS file, so no query will surface it. Getting it
requires a FOIA to CMS, a court filing, or a state all-payer claims database.

---

## 2. The dollar amount

### Miranda, NPI 1285673012 — the only row

`FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER`, one row:

| Field | Value |
|---|---|
| `RNDRNG_PRVDR_ENT_CD` | **I** — individual |
| Name | Miranda, Eduardo |
| Address | 2344 Laguna Del Mar Ct, Laredo, TX |
| `RNDRNG_PRVDR_TYPE` | **Hematology-Oncology** |
| `RNDRNG_PRVDR_MDCR_PRTCPTG_IND` | **Y — participating** |
| `TOT_BENES` | 312 |
| `TOT_SRVCS` | 62,599 |
| `TOT_SBMTD_CHRG` | $2,863,850.12 |
| `TOT_MDCR_ALOWD_AMT` | $1,550,298.15 |
| **`TOT_MDCR_PYMT_AMT`** | **$1,229,994.33** |
| `DRUG_MDCR_PYMT_AMT` | **$1,102,884.56** |
| `MED_MDCR_PYMT_AMT` | $127,109.77 |

**Medicare paid $1,229,994.33 under this NPI. 89.7% of it was drugs.**

`ENT_CD` is `I`. The payment is recorded against an individual, not an
organization. If a company were the enrolled biller, this field would read `O`
and the name column would carry the company name.

### What the split means

`DRUG_MDCR_PYMT_AMT` versus `MED_MDCR_PYMT_AMT` separates drugs administered in
the office from professional services. A $1.10M drug figure against $127k of
medical services is the **buy-and-bill** pattern: the practice purchases infusion
drugs, administers them, and bills Medicare for the drug plus a markup.

62,599 services across 312 beneficiaries is **201 services per patient.** For an
infusion oncology practice that is high but not impossible — each drug unit
counts as a service.

### Miranda's money, all three streams

| Stream | Table | Amount | Paid to |
|---|---|---|---|
| Part B | `..._PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER` | **$1,229,994.33** | the biller behind this NPI |
| Part D | `FED_CMS_PARTD_PRESCRIBER_DRUG` | **$7,702,674** | pharmacies, not him |
| DME | `..._DURABLE_MEDICAL_EQUIPMENT_..._BY_REFER` | $46,385.19 | 6 suppliers, not him |

Only the Part B figure is money that flowed to whoever bills under his NPI. The
Part D and DME figures are money that flowed to third parties on his
authorization.

### The DME row, in full

| Field | Value |
|---|---|
| `RFRG_PRVDR_SPCLTY_DESC` | Hematology-Oncology |
| `RFRG_PRVDR_SPCLTY_SRCE` | Claim-Specialty |
| `TOT_SUPLRS` | 6 |
| `TOT_SUPLR_CLMS` | 24 |
| `TOT_SUPLR_SRVCS` | 1,343 |
| `SUPLR_SBMTD_CHRGS` | $135,265.61 |
| `SUPLR_MDCR_PYMT_AMT` | $46,385.19 |

Six named suppliers billed Medicare on his referrals. **The supplier names are
not in this table** — it is the referrer-side file. The companion
`..._BY_SUPPLIER` table at 440,670 rows has supplier identities but no referrer
link, so the six cannot be named from what is landed.

### Aswad, NPI 1871571406 — nothing

| Table | Row present? |
|---|---|
| Part B by provider | **no** |
| DME by referrer | **no** |
| FISS attending and rendering | **no** |
| Medicare enrollment | **no** |
| PECOS enrollment | **no** |

Aswad bills Medicare nothing. His entire footprint is Part D prescribing at
$2.55M plus seven small industry payments. **There is no payee to find because no
Part B money moved.**

### The FISS table is a name list, not a money table

`FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING`, 2,047,828
rows, has exactly **three real columns**: `NPI`, `LAST_NAME`, `FIRST_NAME`.

Miranda's row confirms he is on CMS's attending-and-rendering roster as of the
2026-08-05 load. It carries no dollars and no organization.

---

## 3. Tax ID, EIN, or organization NPI for the billing entity

**None available. Three separate reasons, each independently fatal:**

1. **Part B publishes no payee identifier.** Proven above by column scan.
2. **`ENT_CD` is `I`.** The enrolled biller for this NPI *is* the individual.
   There is no organization row to look up.
3. **NPPES redacts EIN.** The one column in the warehouse that would carry a
   provider's tax ID is 100% empty across all 9,606,683 rows.

`PECOS_ASCT_CNTL_ID` **8022034875** is the closest thing to a corporate key, and
it resolves to one member — Miranda himself.

---

## The vintage problem, stated up front

`FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER` has **no year
column**, and its registry row carries no `TEMPORAL_COVERAGE` and no source URL.

| Table | Vintage | How known |
|---|---|---|
| `FED_CMS_PARTD_PRESCRIBER_DRUG` | **DY2022** | filename in registry URL |
| Part B by provider | **unknown** | registry row is blank |
| DME by referrer | **unknown** | registry row is blank |
| `FED_CMS_ORDER_AND_REFERRING` | **unknown** | landed 2026-08-05 |

**The $1,229,994.33 has no year attached.** It is one annual figure from an
unknown year. Until the vintage is pinned, it cannot be placed before or after
the 2015 exclusion — which is the whole question.

This is the same trap that turned 554 ghost NPIs into 2. It has not been cleared
here; it has only been named.

---

## What the tables support, and what they do not

| Statement | Supported? |
|---|---|
| No CMS public file names a payee or billing TIN | **yes, scanned** |
| Part B recorded $1,229,994.33 under Miranda's NPI | **yes** |
| 89.7% of that was drug payments | **yes** |
| `ENT_CD` is `I`, so the biller is recorded as the individual | **yes** |
| Aswad has no Part B footprint | **yes** |
| That money was paid *during* the exclusion | **not shown — no year** |
| A hidden company received the money | **not shown, and unfindable here** |
| Ownership is being obfuscated | **not shown.** CMS withholds payee TINs from every provider equally |

The absence of a payee is not evidence about these two NPIs. It is the same
absence for all 1,296,739 rows in the table.

---

## Not checked

1. **The Part B vintage.** Highest priority. Everything else waits on it.
2. `FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVICE`,
   9.78M rows, which breaks the same money down by HCPCS code. That would name
   the drugs and procedures behind the $1.10M.
3. The six DME suppliers. Needs a referrer-to-supplier link not landed.
4. Whether Doctors Hospital of Laredo or Fort Duncan Medical Center, L.P. appear
   in `FED_USASPENDING_%` or SAM under a UEI.
5. `FED_CMS_MEDICARE_PROVIDER` and `FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE`,
   both of which list Miranda and were not opened.

## Cost

Two scripts, about 8 queries. Column scans are metadata. The largest data scan
was `..._PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER` at 1.30M rows, filtered to
two NPIs. No prior run of this pattern in the query log to price against.
