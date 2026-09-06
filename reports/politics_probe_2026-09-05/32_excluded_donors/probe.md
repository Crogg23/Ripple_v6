# 32 — Excluded-entity donor overlap

**Checked:** 3,187 multi-word LEIE org names (HEALTH__FED_HHS_OIG_LEIE, 1979–2026) against FEC indiv (84.2M rows, SUB_ID is a real key, 2023–26 money) three ways: donor EMPLOYER, org DONOR_NAME, and committee name / connected org in the COMMITTEES_DIM. Plus the 8 banned DME suppliers and Almaz by name.
**First number:** 40 LEIE names hit as an employer, 3,418 gifts, $647K — but only 11 of those 3,418 gifts came from the LEIE entity's own state (all 11 = RIGHT AT HOME, a national franchise). Org-donor leg: 0. Committee leg: 0. The nine DME names: 1 hit, $308, from Oregon, for an Alabama exclusion.
**Eyeballed 3 of 3, all false:** HEALTH PARTNERS (excluded: Evansville IN, 2000) = HealthPartners physicians in Minneapolis; UNITED MEDICAL (MD/OH) = donors elsewhere; MAGNOLIA HEALTH (Dallas, 2026) = 0 same-state gifts. False-positive rate seen: 3 of 3, and same-state share 0.3% says the rest are the same.
**A hit would mean:** an excluded provider's owners or staff still writing checks to federal campaigns. **A miss means:** LEIE org names are too generic (HEALTH PARTNERS, FAMILY HEALTH CENTER, CORNER DRUG) to carry identity without an address, and LEIE holds no NPI on the 3 top rows to bridge on.
**Trap hit:** the generic-institutional-name collision (traps 2026-09-03) — multi-word did not save it here; LEIE orgs are small local shops with names shared by hundreds of unrelated businesses. Also FEC indiv has no MEMO_CD; earmark double-count lives in TRANSACTION_TYPE 15E, not filtered here (moot at $0 real).
STATUS: dead
HEADLINE: 40 name hits, $647K, 0 of 3 verified real, 11 of 3,418 gifts same-state — LEIE org names do not reach FEC donors without an address bridge.
