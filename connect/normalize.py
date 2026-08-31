"""One definition of the canonical name/address SQL expressions, shared.

Lifted verbatim from the retired spine module on 2026-08-30 so the live
rebuild path (incremental.py) and the entity index stop importing from
retired code. Behavior is unchanged — same expressions, same callers.
"""

from __future__ import annotations

from .keys import quote_ident


def _name_expr(spec: dict) -> str:
    """Canonical-name expression: prefer org/facility name, else 'LAST, FIRST'."""
    parts = []
    if spec.get("org"):
        # 2026-08-24: the portal crawls were written through pandas, so a missing
        # name lands as the literal string 'nan' (7/83 rows on the DC NPDES tables,
        # 19/1,392 on a Utah clinic table). Treat it as no name, never as a name.
        parts.append(f"NULLIF(NULLIF(TRIM({quote_ident(spec['org'])}), ''), 'nan')")
    if spec.get("person"):
        last, first = spec["person"]
        parts.append(f"NULLIF(TRIM({quote_ident(last)}) || ', ' || TRIM({quote_ident(first)}), ', ')")
    if not parts:
        return "CAST(NULL AS STRING)"
    return parts[0] if len(parts) == 1 else f"COALESCE({', '.join(parts)})"


def _addr_expr(spec: dict) -> str:
    bits = [f"TRIM(COALESCE({quote_ident(spec[k])}, ''))" for k in ("city", "state", "zip") if spec.get(k)]
    if not bits:
        return "CAST(NULL AS STRING)"
    joined = " || ' ' || ".join(bits)
    return f"NULLIF(TRIM({joined}), '')"
