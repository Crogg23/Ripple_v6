# Frank thread 2: the hospice and the home health agency

Opened 2026-09-05. NPI `1164450573`, Alexander Frank, excluded 2025-08-20.
All queries through the Python door, `connect/db.py`. Chat plug-in still 401.

---

## The two facilities, named

Source: `FED_CMS_FACILITY_AFFILIATION`, ingested 2026-07-11.
Frank has exactly three rows in that file.

| Type | CCN | Legal name | Doing business as |
|---|---|---|---|
| Nursing home | 375414 | HASKELL CARE CENTER | — |
| Hospice | 371701 | NEIGHBORHOOD HOSPICE, LLC | COMPLETE HOSPICE CARE OF SOUTHERN OKLAHOMA |
| Home health | 377668 | UNIVERSAL REHAB SERVICES | UNIVERSAL HOME HEALTH / UNIVERSAL HEALTHCARE |

Note the name drift. The hospice's Care Compare name and its PECOS legal name are
different strings. The home health agency has three names across three files:
`UNIVERSAL REHAB SERVICES` in enrollments, `UNIVERSAL HOME HEALTH` as the DBA,
`UNIVERSAL HEALTHCARE` in Care Compare. Name-only matching would have missed both.
The CCN is what held.

### Geography

| Entity | City | County |
|---|---|---|
| Frank, NPPES practice address | Oklahoma City | Oklahoma |
| Haskell Care Center | Haskell | Muskogee |
| Complete Hospice Care of S. OK | Lawton | Comanche |
| Universal Healthcare | Oklahoma City | Oklahoma |

Haskell is roughly 130 road miles east of Oklahoma City. Lawton is roughly 90 miles
southwest. His three facilities sit at three corners of the state.

**This is context, not a finding.** The warehouse holds no travel or visit-date
data. A physician can direct a hospice plan of care by phone and fax. The distance
is worth knowing and proves nothing on its own.

---

## What the warehouse actually holds on these two

| Facility | Table | What is in it |
|---|---|---|
| Hospice 371701 | `FED_CMS_HOSPICE` | 15 columns: name, address, ownership, cert date |
| Hospice 371701 | `FED_CMS_HOSPICE_ENROLLMENTS` | org NPI, PECOS associate ID, LLC, for-profit |
| HHA 377668 | `FED_CMS_HOME_HEALTH` | 99 columns of quality and spend |
| HHA 377668 | `FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS` | org NPI, associate ID, LLC, proprietary |

**There is no hospice utilization or payment file in the warehouse.** Searched
`LIBRARY_RAW.LANDING` for every table name matching `%HOSPICE%`. Two hits, both
above, both directories. No patient counts, no days, no dollars, no live-discharge
rate. The single strongest hospice-fraud measure in public data — the live
discharge rate — is not landed.

**The home health agency does have quality data.**

| Measure | Value | Read |
|---|---|---|
| Quality of patient care star rating | **1.5 of 5** | bottom 9.4% of 7,961 rated agencies |
| Discharge to community | **Worse than national rate** | patients less often go home |
| Potentially preventable readmission | Same as national | — |
| Potentially preventable hospitalization | Same as national | — |
| Falls with major injury | 4.04% | — |
| Medicare spend per episode vs national | 0.98 | 54th pct, see the caveat below |
| Episodes used in the spend calc | 1,196 | — |

Star distribution across all rated agencies: 156 at 1.0, 593 at 1.5. The agency
sits in the bottom 749 of 7,961.

**The star rating is the weakest thing in that table.** The functional-improvement
measures are far more extreme, and they are the ones that speak to long stays.

| Do patients get better at... | This agency | National median | Agencies worse | Percentile |
|---|---|---|---|---|
| bathing | **41.14%** | 90.07% | 192 of 8,041 | **2.4th** |
| breathing | **37.94%** | 90.46% | 281 of 7,805 | **3.6th** |
| getting in and out of bed | **45.00%** | 88.47% | 295 of 7,986 | **3.7th** |
| walking or moving around | **49.71%** | 87.47% | 341 of 8,029 | **4.2nd** |
| taking medications by mouth | **46.74%** | 86.30% | 480 of 7,937 | **6.0th** |

Patients at this agency do not improve, at the 2nd to 6th percentile nationally.
The 1.5-star rating is a summary of that.

**The 0.98 spend ratio cannot serve as a counterweight, and an earlier draft used
it as one.** The measure is Medicare spend *per episode*. Adding more episodes to
the same patient does not move it. It is blind by construction to the exact
behaviour the re-certification ratio below alleges. The national median is 0.97,
so 0.98 sits at roughly the 54th percentile, not "at the average."

---

## The finding: Frank's recertification ratio

Source: `FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI`.
Registry says DY2023. COVID codes prove only 2021 or later. **Vintage is
unproven and the number below is only as good as that.**

Two codes carry home health certification.

| Code | Meaning |
|---|---|
| G0180 | initial certification for a home health plan of care |
| G0179 | re-certification, one per additional 60-day episode |

Frank's lines:

| Code | Beneficiaries | Services | Services per beneficiary |
|---|---|---|---|
| G0180 certification | 30 | 31 | 1.03 |
| G0179 re-certification | 59 | 201 | **3.41** |

His ratio of re-certifications to certifications is **6.48**.

### What that number means, plainly

Home health runs in 60-day episodes. The first episode needs a certification. Every
episode after it needs a re-certification. So the ratio is a direct measure of how
long patients stay on home health before they are discharged.

A ratio near 1 means new starts and continuations roughly balance.
A ratio of 6.48 means continuations dominate by six and a half to one.

Do not read the ratio as a per-patient episode count. That would need a
steady-state assumption this file cannot support. The per-patient number the file
does support is **3.41 re-certifications per re-certified patient**, which is
roughly seven months of continued home health on top of the first episode.

### The comparison

| Population | Value |
|---|---|
| National totals in this file | 396,309 re-certs vs 695,422 certs, ratio **0.57** |
| Practitioners billing both codes | 5,136 |
| Median ratio among them | **1.04** |
| 99th percentile | 6.56 |
| **Frank** | **6.48** |
| Practitioners above him | **53** |
| His rank | **54 of 5,136**, 98.97th percentile |

Nationally, certifications outnumber re-certifications. Frank re-certifies six and
a half times for every new patient he starts.

Two disclosures the rank needs.

**The denominator is not everyone.** A ratio only exists where both codes appear.
19,653 practitioners bill either code. 13,462 bill certifications only. **1,055
bill re-certifications with no certification row at all** — an infinite ratio by
this measure — and the filter deletes every one of them. Their cert row is missing
because it fell under the suppression floor, which is itself the long-stay shape.
The exclusion runs one direction.

| Denominator | Frank's rank | Percentile |
|---|---|---|
| Both codes present, the measure used here | 54 of 5,136 | 98.97 |
| Every G0179 biller | 1,109 of 6,191 | 82.1 |
| Every biller of either code | 1,109 of 19,653 | 94.4 |

**The 5,136 are not all physicians.** 896 are nurse practitioners and 95 are
physician assistants, about 19% of the set. Read it as practitioners.

### Walking the chain

- **What was checked.** G0179 and G0180 service counts per NPI in the Part B
  service file, Frank against every other doctor who bills both.
- **What a hit means.** Patients kept on home health across many consecutive
  60-day episodes rather than discharged when they recover.
- **What a miss means.** A ratio near the 1.04 median, where new starts and
  continuations roughly balance.

---

## The check that mattered most: is it the agency or the man?

If Universal Healthcare pushes long stays, every doctor on its panel would show a
high ratio. Pulled all 15 distinct practitioners listed at the hospice and the
home health agency and ran the same measure. Frank is listed at both, so he holds
two of the sixteen rows.

| Facility | Doctor | Re-certs | Certs | Ratio |
|---|---|---|---|---|
| Home health | **FRANK** | 201 | 31 | **6.48** |
| Home health | COX | 82 | 20 | 4.10 |
| Hospice | JAMES | 74 | 31 | 2.39 |
| Home health | DEPPEN | 295 | 131 | 2.25 |
| Home health | FINCH | 69 | 40 | 1.73 |
| Home health | MENZ | 86 | 51 | 1.69 |
| Home health | BROWN | 167 | 102 | 1.64 |
| Home health | ALTSTATT | 85 | 55 | 1.55 |
| Home health | KRABLIN | 211 | 143 | 1.48 |
| Home health | MORTON, DWUMA, HENSON, FORD | — | — | no cert row above the floor |
| Hospice | SINGH, VICE | — | — | no cert row above the floor |

**All six of those are in the Part B file.** Ford has 20 rows, Morton 15, Dwuma 8,
Vice 7, Singh 7, Henson 7. What they lack is a G0179 or G0180 line clearing the
11-beneficiary suppression floor. That is a different thing from absence, and an
earlier draft of this report got it wrong.

Frank tops his own panel at 6.48, and the next practitioner sits at 4.10.

**But the panel does cluster high, and the national median is the wrong yardstick.**
The panel's own median is **1.706**, which is the **76th percentile nationally**.
All eight sit above the national median of 1.04. The lowest of them, 1.475, is
still inside the national top 30%.

The honest baseline is geographic.

| Peer set | Practitioners | Median ratio | Frank's rank |
|---|---|---|---|
| National, both codes | 5,136 | 1.04 | 54, 98.9th pct |
| Family practice only | 1,582 | 1.20 | 15, 99.1st pct |
| **Oklahoma only** | **237** | **1.79** | **3rd** |

Oklahoma's median is 1.79. **Frank's panel is ordinary for Oklahoma. Frank is
third in the state.**

- **Hit means** the long-stay pattern is Frank's, not his co-panel's.
- **Miss means** his panel-mates would sit near him and the agency would be the story.

Against the Oklahoma baseline the panel is unremarkable and Frank is not.

**One limit on this whole section.** G0179 and G0180 name no agency. A practitioner
on this panel may certify mostly for other agencies. The codes cannot fully
separate the man from the agency, and this test is weaker than its heading implies.

---

## The hospice produced nothing

Two Part B codes cover physician oversight outside a visit.

| Code | Meaning | Frank |
|---|---|---|
| G0181 | home health care plan oversight | **no row above the floor** |
| G0182 | hospice care plan oversight | **no row above the floor** |

Nationally only 211 providers bill G0182 at all, for 23,077 services. It is a rare
code. Frank's absence from it is not unusual.

**This is an absence, not a zero, and the difference matters.** The file deletes
any line under 11 beneficiaries. Frank could bill both codes on up to ten patients
each and still read as blank. His own rows prove the floor is live in his data: he
has a 99348 residence-visit line sitting at exactly 11 beneficiaries.

So the honest statement is that **his hospice affiliation shows no Part B billing
above the suppression floor.** Whether it generates any at all is not testable
here. The hospice money, if any, would be in the hospice's own claims, which the
warehouse does not hold.

---

## The practice shape is not rare

The handoff called the nursing-home-plus-hospice-plus-home-health shape a known
fraud pattern worth checking. Measured it.

| Cut | Physicians |
|---|---|
| Any facility affiliation in the file | 940,350 |
| Any hospice | 30,511 |
| Any home health agency | 122,538 |
| **Hospice and home health and nursing home, all three** | **7,127** |
| All three, and exactly one of each | **950** |
| All three, exactly one of each, and nothing else | **46** |

**7,127 physicians have Frank's practice shape.** That is not rare and it does not
single him out.

The 46 figure is the narrowest cut, and it is a cut chosen after seeing Frank. It
should not be reported as though the shape selected him. It did not.

### The exclusion rate in that group is not usable

| Group | Physicians | With an LEIE NPI match |
|---|---|---|
| All affiliated | 940,350 | 15 |
| All three types | 7,127 | 1 |
| The 46 | 46 | **1, Frank** |

15 exclusions across 940,350 affiliated doctors is impossibly low. Three reasons,
all known traps:

1. `FED_HHS_OIG_LEIE` carries an NPI on only 10.5% of rows.
2. OIG deletes people on reinstatement, so the list is current, not historical.
3. Excluded doctors drop out of Medicare, so they leave the affiliation file.

A single hit in a group of 46 is one person, not a rate. **No base-rate claim can
be made from these numbers.**

---

## Loose ends found along the way

**Frank is absent from PECOS.** `FED_CMS_PECOS_PROVIDER_ENROLLMENT` holds 2,978,925
rows including 129,509 family practice enrollments. Neither his NPI nor his
associate ID `4587624473` appears. Both of his facilities' org enrollments do
appear. Either the file is a vintage that postdates his exclusion, or the load is
partial. Unresolved.

**He is still in the affiliation file.** That file was ingested 2026-07-11, almost
eleven months after his 2025-08-20 exclusion. This is the ingest date, not the
file's own vintage, so it is a flag to chase and not yet a claim.

**No owner identity exists.** Ownership *type* is landed — the hospice reads
For-Profit, the agency reads PROPRIETARY. No owner name or ID is. Searched for
owner, PECOS and change-of-ownership tables. `FED_CMS_PECOS_PROVIDER_ENROLLMENT` is an enrollment roster with no owner
column. The CMS all-owners files for home health and hospice are not landed.
**Nothing in the warehouse shows who owns either facility.** Frank's link to both
is a listed clinical affiliation and nothing more.

**LEIE name search on the org names returned three false hits** — a Houston home
health outfit, a Philadelphia rehab, a second Houston rehab, all different states
and different decades. This is the single-word name collision trap. None are ours.

---

## What is claimed, and what is not

| Claim | Supported |
|---|---|
| Frank's two other facilities are a Lawton hospice and an OKC home health agency | **yes** |
| The home health agency rates 1.5 of 5 stars, bottom 9.4% | **yes** |
| Its patients improve at the 2nd to 6th percentile nationally | **yes, five measures** |
| The 0.98 spend ratio argues against a billing mill | **no. It cannot see episode count** |
| The agency's discharge-to-community is worse than national | **yes** |
| Frank's re-cert to cert ratio is 6.48, rank 54 of 5,136 | **yes** |
| He tops his own agency's panel on that measure | **yes, 9 of 15 had data** |
| His panel is unremarkable against the national median | **no. Panel median 1.706 is the 76th pct** |
| His panel is unremarkable against Oklahoma | **yes. Oklahoma median is 1.79** |
| His hospice affiliation produces zero Part B billing | **not testable. No row above the floor** |
| The three-facility practice shape is rare | **no. 7,127 doctors have it** |
| The shape predicts exclusion | **no. LEIE cannot support any rate** |
| Frank owns either facility | **not shown. No owner identity is landed** |
| The long stays are medically unjustified | **not shown, and not showable here** |
| The hospice billed anything improper | **not shown. No hospice claims data exists** |

---

## The load-bearing unknown, again

The re-certification ratio measures how long patients stay on home health. It does
not say why.

A physician running a genuinely frail, homebound, chronically ill panel — exactly
what a nursing home practice produces — will legitimately re-certify more than a
clinic doctor whose patients recover. Frank's own Part B is 1,099 nursing facility
visits and 762 residence visits. His panel really is that population.

**The ratio is a flag, not a verdict.** What separates a long stay that is
appropriate from one that is not is the patient's clinical course, and that lives
in records the warehouse will never hold.

### The censoring is not random, and it cuts both ways

Everything above is computed on a file that deletes every line under 11
beneficiaries. That deletion is correlated with the thing being measured.

| Effect | Direction |
|---|---|
| Low-volume practitioners vanish from the peer set | median reads **higher** than truth, flattering Frank |
| A low-cert high-recert doctor loses the cert row and drops out | rank reads **better** than truth, damning Frank |

The two do not cancel and neither can be sized from this file. **The measure cannot
see the population most likely to be more extreme than Frank** — the 1,055
practitioners with re-certifications and no certification row.

---

## Where to go next

1. **Land the CMS hospice utilization file.** Live discharge rate is the measure
   that would make the hospice half of this thread answerable. It is public.
2. **Land the CMS all-owners files** for home health and hospice. They would settle
   whether Frank owns anything or only signs orders.
3. **Resolve the PECOS absence.** It is either a vintage artifact or a partial
   load, and it changes how much weight the enrollment files can carry.
4. **Thread 3, untouched:** the 23 DME suppliers on Frank's referrals, 36,017
   services for 64 beneficiaries.
