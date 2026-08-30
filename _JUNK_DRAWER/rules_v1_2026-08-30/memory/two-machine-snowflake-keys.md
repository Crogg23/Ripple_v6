---
name: two-machine-snowflake-keys
description: 2026-08-20 - Ripple is now a TWO-machine setup (Windows box + Mac laptop); both Snowflake key slots are live and rotating without --slot clobbers the other machine
metadata: 
  node_type: memory
  type: project
  originSessionId: b7d61832-8c75-40e6-a228-a1702062f80b
  modified: 2026-08-20T15:26:45.498Z
---

Chris works from **two machines**: the Windows box (`c:\Code\Ripple_v6`) and a Mac
laptop. Both authenticate to Snowflake as CROGG23 by key pair, and **both of the
user's two RSA key slots are now occupied**:

- **RSA_PUBLIC_KEY (slot 1)** — the Windows box. Set 2026-08-20.
- **RSA_PUBLIC_KEY_2 (slot 2)** — the Mac laptop. Set 2026-08-19 ~23:46 PT.

Snowflake accepts a JWT signed by either private half, so the machines work
independently and neither needs the other's key.

**Why:** on 2026-08-20 every warehouse connection from the Windows box failed with
"JWT token is invalid" — including dbt's own connection test. Cause: the Mac had
rotated slot 2 the previous night, replacing the July-29 public key that the
Windows box's private key matched. Nothing was compromised; a second machine simply
took the slot. Diagnosed by reading `DESC USER CROGG23` output — the
`RSA_PUBLIC_KEY_2_LAST_SET_TIME` timestamp is what gave it away, and 06:46 in the
account's UTC clock is 23:46 Pacific.

**How to apply:**
- **`scripts/rotate_dbt_keypair.py` defaults to `--slot 2`, which is the Mac's.**
  Always pass `--slot` explicitly: `--slot 1` on the Windows box, `--slot 2` on the
  Mac. A default rotation from either machine silently locks the other one out.
- When any warehouse connection fails with "JWT token is invalid," check
  `RSA_PUBLIC_KEY*_LAST_SET_TIME` on the user **before** assuming a broken key file
  or clock skew — the other machine having rotated is now the likeliest cause.
- The script never executes SQL and never prints the private key; it prints an
  `ALTER USER` statement for Chris to paste into a Snowflake worksheet.
- `--force` is blocked by Chris's own git-guardrail hook, which pattern-matches the
  flag anywhere, not just on git commands. Work around it by renaming the existing
  key file first (which also preserves it) rather than overwriting.
- The dbt profile header carried a stale note claiming slot 1's private half was
  lost. That was true 2026-07-29 → 2026-08-20 and is now corrected in the file.

Related: [[snowflake-pat-role-reality]] (PATs can't use ACCOUNTADMIN, which is why
key-pair auth is the only workable non-interactive path on this account).
