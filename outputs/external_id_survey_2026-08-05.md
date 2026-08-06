# External ID Standards Survey (2026-08-05)

**Why:** Ripple's join engine currently only recognizes 27 known ID types (`connect/keys.py`
KEY_TOKENS). This was a web survey — not a warehouse check — asking: what other identifier
standards exist across US public data that we're structurally blind to? Ranked by how much
the bridge matters for finding harm to people, per the mission test.

**Status: none of this is verified against our actual data yet.** Every candidate below needs
the same treatment NDC/EPA-case got in the 2026-08-05 coverage sweep: COUNT(DISTINCT) + value
sample, live in the warehouse, before it becomes a real key.

---

## Ranked candidates

### 1. RSSD ID — bank/holding-company identifier (STEEL)
Federal Reserve's permanent ID for every bank, branch, and holding company. Ties a bank's
enforcement history and ownership tree together — without it you can't trace a predatory
branch back to the parent company profiting from it. Free bulk source: Fed's NIC.

### 2. FDIC Certificate Number — insured-bank ID (STEEL)
Follows a bank through name changes and acquisitions. Tracks who inherits bad practices when
a failing bank gets bought instead of shut down. Free API via FDIC BankFind Suite.

### 3. DOT Number — trucking/carrier ID (STEEL)
FMCSA's ID for interstate commercial carriers. Direct line to crash history, safety
violations, and — via EIN/business registration — who really owns a fleet hiding a bad
safety record behind shell names. Public bulk via FMCSA SAFER/MCMIS.

### 4. NMLS ID — mortgage loan originator/broker ID (STEEL)
Catches a loan officer sanctioned in one state quietly resurfacing under a new company in
another. Direct mortgage-fraud/foreclosure-abuse bridge. Search is free; true bulk-download
status unconfirmed.

### 5. ORI — law enforcement agency ID (STEEL within FBI system)
Used in FBI UCR/NIBRS crime data. Without it, incident-level crime data can't be tied to a
*specific* department — department names collide across states. Foundational for any
police-accountability work. Public bulk via NIBRS CSV files.

### 6. NPDES Permit ID — water discharge permit ID (STRONG)
Distinct from FRS_ID (already have) — FRS_ID is the facility, this is the permit. One
facility can hold multiple permits; this ties specific pollution violations to a specific
legal authorization. Public bulk via EPA ECHO/ICIS-NPDES.

### 7. CLIA Number — clinical lab certification ID (STEEL)
Labs aren't always NPI-holding billing providers — this is the blind spot. Ties lab-fraud
patterns to a facility, joinable to CCN. Public, weekly-updated CMS registry.

### 8. NCT Number — clinical trial registry ID (STEEL)
Connects trial outcomes/adverse events to sponsor and downstream to FDA drug approvals.
Relevant for harm buried in trials on vulnerable populations. Public bulk via
ClinicalTrials.gov.

### 9. NDA / ANDA / BLA — FDA drug approval application numbers (STRONG)
Ties a drug's approval record to all its manufacturers and later recalls — the identity
spine for "which company is behind harm from this drug," especially for generics under one
ANDA. Only ANDA's 6-digit format was confirmed; NDA/BLA format unverified. Public via
Drugs@FDA.

### 10. CAGE Code — federal contractor facility ID (STRONG)
Facility-grain, not entity-grain like UEI (already have). Catches one bad worksite even when
the parent company rotates its UEI/name. Public via SAM.gov.

### 11. A-Number — immigration registration ID (STEEL in theory)
Highest potential harm-bridge on this list (detention, deportation-to-danger, labor
exploitation of noncitizens) — but almost certainly locked to FOIA/court records, not a bulk
public feed. **RED-lane: legal/ethical weight, flag for Chris before any pursuit,** not a
build item.

### 12. Aircraft IDs — N-Number (STRONG, gets reassigned) + ICAO24 hex (STEEL, permanent)
Private/corporate jet tracking tied to real owners — a known wealth/influence-mapping
pattern (who flies where behind an LLC). Public bulk via FAA registry CSV.

### 13. VIN — vehicle ID (STEEL)
Ties NHTSA recall/complaint/crash data to a specific vehicle. Lower mission priority —
consumer-safety grain, not the institutional-harm grain Ripple targets. Public via NHTSA.

### Lower priority / thinner evidence
- **Medicaid Provider ID** — real, distinct from NPI, but state-specific format variance weakens it as a clean key.
- **GLN/GS1** — no strong evidence of use in datasets Ripple would touch.
- **HIN (small-vessel hull ID)** — plausible for maritime labor abuse, not directly researched, bulk status unconfirmed.
- **State Secretary-of-State entity numbers** — useful for unmasking shell companies, but 50 different formats, no crosswalk, and some states paywall bulk data (Minnesota confirmed free-for-press only).

### Explicitly NOT a join key
- **HCPCS/CPT/ICD codes** — procedure/diagnosis classifications, same category as the already-banned NAICS/SIC. Descriptive attributes only, never join keys.

---

## Record-linkage methods beyond exact-ID matching

For entities that never share a clean ID and only appear as free text:

- **Fellegi-Sunter probabilistic linkage (1969)** — the standard framework: weighs how much each field match/mismatch (name, address, DOB) shifts the odds two records are the same entity, instead of requiring an exact match. Theoretical basis under most modern fuzzy-join tools.
- **Splink** — best-known open-source Python implementation of Fellegi-Sunter at scale (named for reference only, not a vendor pitch).
- **Phonetic matching (Soundex, Jaro-Winkler)** — catches spelling variants ("Smith"/"Smyth"), usually layered into probabilistic linkage as one signal among several.
- **Address standardization** — USPS-rule-based normalization so "123 Main St Apt 4" and "123 Main Street, Unit 4" register as the same place.
- **Blocking/indexing** — the scaling trick: bucket records (same ZIP, same name-first-letter) before comparing, instead of comparing every record to every other record.

These would sit **on top of** the existing NAME+ZIP corroboration — a formal confidence score
instead of today's binary "maybe" flag.

## Caveat (from the research pass itself)

None of this was checked against Ripple's live warehouse. Specifically unconfirmed: exact
NDA/BLA digit format, whether NMLS bulk data is truly downloadable vs. search-only, paywall
status of Secretary-of-State data outside Minnesota, CAGE/HIN bulk-file existence vs.
lookup-only. A-Number's legal availability was flagged, not vetted.

## Recommended next step

Green-lane: run the same live-data verification pass as yesterday's coverage sweep (COUNT,
COUNT DISTINCT, value sample) against RSSD/FDIC-CERT/DOT-Number/ORI/NPDES-Permit-ID/CLIA —
the top 7 — the moment the matching source data is identified as already-loaded or
easy-to-load. A-Number stays parked pending your call.
