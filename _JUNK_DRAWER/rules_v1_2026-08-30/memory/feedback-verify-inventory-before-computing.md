---
name: feedback-verify-inventory-before-computing
description: "Before any warehouse-wide sweep or \"are these numbers reliable\" answer, verify the live inventory (databases/tables) and check for an existing audit first — don't trust a hardcoded list or jump straight to computing."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 14af180a-07d2-4cd6-9756-c925e06a3a46
  modified: 2026-08-27T01:03:56.874Z
---

Before running any full-warehouse sweep or answering "are these numbers
reliable," do two checks first, in this order:

1. **Confirm the live inventory, don't trust a remembered/hardcoded list.**
   On 2026-08-26 a warehouse sweep used an old hardcoded 5-database list
   (copied from an existing script) and silently missed 2 real databases
   that a prior audit had already found — reported "the whole warehouse"
   numbers that were actually a subset. The fix: run `SHOW DATABASES` (or
   equivalent live inventory query) before any full-warehouse claim, every
   time, even when reusing a known-good script.
2. **Check for an existing audit/report before building a new one.** The
   same session spent real effort building a fresh metadata sweep when a
   far more rigorous one ([[reports-the-audit-2026-08-24]] equivalent —
   see `reports/the_audit_2026-08-24/`) already existed, live-verified with
   real `SELECT COUNT(*)` and distinct+sample key checks, and had already
   answered the exact reliability question being asked. Chris had to
   explicitly redirect to it.

**Why:** Chris, 2026-08-26, after this exact pattern happened twice in one
session (missed databases, then duplicated an existing audit) — reaction
was direct anger at repeated oversights, not a one-off correction. This is
the breadth-first rule ([[feedback-breadth-first-surface-pass]]) applied to
tooling and prior-art, not just to question generation: "cover everything
before deepening anything" means verifying scope and checking for existing
work BEFORE computing, not after being asked whether the numbers are
trustworthy.

**How to apply:** Any time a task starts with "sweep/audit/measure the
whole X," first (a) pull a live inventory of X rather than reusing a
remembered list, and (b) search for existing reports/audits covering the
same ground before writing new measurement code. Both checks are cheap;
skipping either produces confidently-incomplete answers.
