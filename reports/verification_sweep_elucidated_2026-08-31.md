# The verification sweep, walked chain by chain

Written 2026-08-31 for Chris, in the methodology's own voice:
every finding shown as its chain — what was checked, what a match
means, what a miss means, what you could rerun yourself.
The chat version of this document is the canonical one-sitting read;
this file exists so it survives the scrollback.

Companion receipts: `reports/verification_audit_2026-08-30.md` progress log,
`reports/row1/*.json`, `scripts/row1_*.py`, `scripts/pass2_level2_namecheck_2026_08_31.py`,
`scripts/row15_pass1_spotcheck.py`, `scripts/drop_duplicate_families_2026_08_31.py`.

The content mirrors the chat walkthrough of 2026-08-31 exactly; see that
message for the full elucidated text. Sections: the question the audit asks;
counting what landed vs what publishers say; the zip extractor bug; the
registry's three lies; the clock layer that was already built; testing the
joins by name; what the test suite really said; the two guard holes; the
rebuild; the hash-checked drops; and the standing lesson — every failure
found this sweep was one simple thing nobody had looked at.
