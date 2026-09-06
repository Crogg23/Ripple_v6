# 85 — Device and pharma corporate PACs into leadership PACs

- **Checked:** Open Payments PY2024 payer names, case-folded and suffix-stripped, multi-word only → exact match on FINANCE__FED_FEC_COMMITTEES_DIM CONNECTED_ORG_NM (44,398 rows, 1 per CMTE_ID, 55% CYCLE null, 3,431 ambiguous) → COMMITTEE_TO_CANDIDATE 24K/24Z with MEMO_CD <> 'X', OTHER_ID = FED_FEC_LEADERSHIP_PAC committee (8,338 leadership PACs, 2024 file only).
- **First number:** 36 makers matched a corporate PAC; 31 of them gave $8.07M to 358 leadership PACs (2024: $4.62M, 2026: $3.44M). Abbott $1.17M to 141, Lilly $1.07M to 184, Gilead $844K to 180. Top recipient: Brett Guthrie (E&C chair) $242K from 24 makers.
- **Verified by eye:** Zimmer Biomet, Intuitive Surgical, Boston Scientific — all the real corporate PAC. 0 of 12 sampled were false positives.
- **Hit means:** the leg exists and the money is memo-clean; ranking by Open Payments total works (Boston Scientific $61M in doctor payments → $447K into leadership PACs).
- **Miss means:** exact-fold recall is low: BioNTech, AbbVie, Stryker, Medtronic, Arthrex (the top 5 payers, $690M) matched no DIM org name. Real total is bigger; the deep dive needs a contains-match with a by-eye pass.
- **Trap hit:** LEADERSHIP_PAC is one vintage (FEC_ELECTION_YR 2024 only); 10 of 36 matched PACs are IS_AMBIGUOUS. Did not touch the PAYMENT id column.

STATUS: lit
HEADLINE: 31 device/pharma corporate PACs put $8.07M into 358 leadership PACs in 2024–2026, Abbott first at $1.17M across 141 PACs, and the top five doctor-payers are still unmatched.
