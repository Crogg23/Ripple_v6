---
name: spine-connection-audit-2026-08-11
description: First measurement of the entity spine/joins — placeholder-ID merge, spine reading pre-repair table copies, measured join precision ~97-100%
metadata:
  type: project
---

2026-08-11 (evening): first audit of the connection layer (the layer under every
story), companion to the same day's warehouse verification + repair.

What it found:
- **Placeholder IDs merge distinct companies.** EIN `999999999` fused CVS, SK
  Telecom, Kingsway Financial, Enstar and a literal "TEST Company" into one
  entity across 16 sources. `pad` normalization killed all-zeros only; it now
  also kills repeated digits and keyboard walks, in BOTH `connect/keys.py` and
  its `serve/serve_queries.py` mirror (the mirror has its own drift guard test).
- **The spine reads landing tables named in `connect/entity_index_specs.py`
  DISPLAY_SPECS — re-pulls that land under a NEW table name are invisible to it.**
  The dbt marts were repointed on 2026-08-11; the connection engine was not, so
  the debarment lens ran on a 9,000-row sample of a 167,928-row list. Whenever a
  source is re-pulled, check DISPLAY_SPECS and `connect/leads_specs.py` too.
- **Measured join precision (name corroboration, not vibes):** UEI
  debarment×contracts 99/102; NPI exclusions×open-payments 336/350 exact surname,
  the rest hyphen variants of the same person. 93.9% of 806M spine-input rows
  carry a usable hard key (`outputs/_spine_key_health_2026-08-11.json`).
- **Identity precision is structurally safe by design**: hard-ID-only clustering,
  no cross-ID-type fusion, fuzzy gated at REVIEW. The live risk is garbage INSIDE
  a hard ID — see [[bridge-fuel-reality]] and [[completeness-check-traps]].

Open: the fuller 20M USASpending contracts copy would take debarred-with-awards
from 102 to 343, but it is loader-capped at a round 20,000,000 — needs an
uncapped re-pull before repointing. Same shape for the IRS 990 e-file index.

A full who's-who rebuild (~4.5h / ~$10-15, see [[spine-full-rebuild-2026-08-08]])
is required for any of these fixes to reach the warehouse — the normalizer change
invalidates every key, so incremental catch-up will not do it.
