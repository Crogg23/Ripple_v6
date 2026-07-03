"""Pure SQL statement guard for the read lane. Stdlib only — fully offline-testable.

Honest scope (say what the belt is, not what we wish it were):
  * The LOAD-BEARING guarantees are server-side — the connector executes exactly
    ONE statement per cursor.execute() (never execute_string, never
    num_statements), and the session role's privileges bound what that statement
    can do. This guard is the fast, friendly early-reject in front of them.
  * The guard tokenizes: comments and string literals are stripped BEFORE any
    check, so `/* DROP */ SELECT 1` passes and `SELECT ';'` passes while
    `SELECT 1; DROP TABLE x` is rejected.
  * SELECT-embedded side effects (external functions, SYSTEM$..., TO_QUERY)
    are denied by token; anything we cannot see (a view hiding a claim table,
    an external function) is the role lane's job, not this regex's.
"""

from __future__ import annotations

import re

ALLOWED_FIRST = {"SELECT", "WITH", "SHOW", "DESCRIBE", "DESC", "EXPLAIN"}

# Word-boundary tokens denied anywhere in the statement skeleton. Statements
# (INSERT/CREATE/...) are already blocked by the first-keyword allowlist +
# single-statement execution; keeping them here is defense in depth against
# connector surprises. CALL and TO_QUERY are the real embedded risks.
DENY_TOKENS = {
    "CALL", "TO_QUERY", "EXECUTE", "INSERT", "UPDATE", "DELETE", "MERGE",
    "CREATE", "DROP", "ALTER", "TRUNCATE", "GRANT", "REVOKE", "UNDROP", "COPY",
    # IDENTIFIER('...') resolves a table name from a string literal AFTER the
    # skeleton blanks strings - it would smuggle claim tables past claim_refs().
    "IDENTIFIER",
}

# LIBRARY_META."CONNECT" claim tables: raw reads are unreviewed accusations about
# named people. sqlrun blocks these and points at V_LEADS_PUBLISHED instead.
CLAIM_TABLES = {"LEADS", "ENTITY_LINKS", "ENTITY_MAP", "ENTITY_GOLDEN", "MATCH_PAIRS"}

_IDENT_PART = re.compile(r"^[A-Z0-9_$]+$")
_QUOTED_PART = re.compile(r'^"[^"]+"$')


def strip_comments_and_strings(sql: str) -> str:
    """Statement 'skeleton': -- and /* */ comments removed, single-quoted string
    contents blanked (quotes kept). Double-quoted identifiers stay — they are
    inert as keywords but needed for "CONNECT" claim-table detection."""
    out = []
    i, n = 0, len(sql)
    while i < n:
        ch = sql[i]
        nxt = sql[i + 1] if i + 1 < n else ""
        if ch == "-" and nxt == "-":                    # -- line comment
            j = sql.find("\n", i)
            i = n if j == -1 else j
        elif ch == "/" and nxt == "*":                  # /* block comment */
            j = sql.find("*/", i + 2)
            i = n if j == -1 else j + 2
        elif ch == "'":                                 # 'string' ('' escapes)
            out.append("''")
            i += 1
            while i < n:
                if sql[i] == "'" and (i + 1 < n and sql[i + 1] == "'"):
                    i += 2
                elif sql[i] == "'":
                    i += 1
                    break
                else:
                    i += 1
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def first_keyword(skeleton: str) -> str:
    """First real keyword, tolerating leading whitespace and '(' wrappers."""
    m = re.match(r"[\s(]*([A-Za-z_]+)", skeleton)
    return m.group(1).upper() if m else ""


def check(sql: str) -> tuple[bool, str]:
    """(ok, reason). ok=False means reject with the reason; ok=True means the
    text guard is satisfied — the role lane + single-statement execution still
    stand behind it."""
    if not sql or not sql.strip():
        return False, "empty SQL"
    skeleton = strip_comments_and_strings(sql)
    kw = first_keyword(skeleton)
    if kw not in ALLOWED_FIRST:
        return False, (f"first keyword '{kw or '?'}' not allowed - the read lane runs "
                       f"{'/'.join(sorted(ALLOWED_FIRST))} only")
    body = skeleton.rstrip().rstrip(";")
    if ";" in body:
        return False, "multiple statements - run one at a time"
    for tok in DENY_TOKENS:
        if re.search(rf"\b{tok}\b", body, re.IGNORECASE):
            return False, f"'{tok}' is not allowed on the read lane"
    if re.search(r"SYSTEM\$", body, re.IGNORECASE):
        return False, "SYSTEM$ functions are not allowed on the read lane"
    return True, "ok"


def claim_refs(sql: str) -> set[str]:
    """Claim tables referenced via the CONNECT schema (quoted or not).
    V_LEADS_PUBLISHED deliberately does NOT match — that's the safe read."""
    refs = set()
    skeleton = strip_comments_and_strings(sql)
    for t in CLAIM_TABLES:
        if re.search(rf'"?CONNECT"?\s*\.\s*{t}\b', skeleton, re.IGNORECASE):
            refs.add(t)
    return refs


def validate_fqn(fqn: str) -> str:
    """Validate a 1-3 part identifier; returns the normalized FQN or raises.
    Unquoted parts are upper-cased and must match ^[A-Z0-9_$]+$; quoted parts
    ("CONNECT") pass through. Table names can't be bound as %s params — this
    is the only sanctioned interpolation path."""
    parts = [p.strip() for p in str(fqn).strip().split(".")]
    if not 1 <= len(parts) <= 3 or any(not p for p in parts):
        return _reject(fqn)
    out = []
    for p in parts:
        if _QUOTED_PART.match(p):
            out.append(p)
        elif _IDENT_PART.match(p.upper()):
            out.append(p.upper())
        else:
            return _reject(fqn)
    return ".".join(out)


def _reject(fqn):
    raise ValueError(f"invalid table identifier: {fqn!r}")


def quote_ident(name: str) -> str:
    """Quote one identifier (landing columns can be odd — spaces, lowercase)."""
    return '"' + str(name).replace('"', '""') + '"'
