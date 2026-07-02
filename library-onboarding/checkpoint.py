"""Checkpoint rendering + the foreman approval prompt.

Every checkpoint shares the same shape: a banner with the step name and a
``[i of N]`` position counter (in batch mode), a body, then the action prompt:

    -> go / edit [feedback] / skip / abort
"""

from __future__ import annotations

import sys
from typing import Optional, Tuple

from config import settings

# Force UTF-8 on stdout/stderr BEFORE any rich output. On Windows a redirected
# stdout defaults to cp1252, which can't encode the box/arrow/ellipsis glyphs and
# would crash the whole pour on the first checkpoint banner. errors='replace' makes
# it lossless-safe even if a stray glyph slips through.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:
        pass

try:
    from rich.console import Console
    from rich.syntax import Syntax
    from rich.table import Table

    _RICH = True
    # legacy_windows=False keeps rich off the cp1252 code path even under redirection.
    console = Console(legacy_windows=False)
except ImportError:  # pragma: no cover - degrade to plain print
    _RICH = False
    console = None  # type: ignore

# Action constants. FAILED = an unattended per-source give-up (auto-repair exhausted
# or an uncaught error): distinct from ABORT (a real human/Ctrl-C stop), so the batch
# can skip-and-continue on FAILED but halt on ABORT.
GO, EDIT, SKIP, ABORT, FAILED = "go", "edit", "skip", "abort", "failed"

_CHECKPOINTS = {
    1: "RECON",
    2: "SCRIPT",
    3: "LOAD",
    4: "DBT",
    5: "REGISTRY",
    6: "CONNECT",
}


# ---------------------------------------------------------------------------
# Output primitives
# ---------------------------------------------------------------------------
def _print(msg: str = "") -> None:
    if _RICH:
        console.print(msg)
    else:
        print(_strip_markup(msg))


def _strip_markup(msg: str) -> str:
    import re

    return re.sub(r"\[/?[a-z0-9 _#]+\]", "", msg)


def info(msg: str) -> None:
    _print(f"[cyan]{msg}[/cyan]")


def success(msg: str) -> None:
    _print(f"[bold green]OK[/bold green] {msg}")


def warn(msg: str) -> None:
    _print(f"[bold yellow]![/bold yellow] {msg}")


def error(msg: str) -> None:
    _print(f"[bold red]x[/bold red] {msg}")


def banner(num: int, position: Optional[Tuple[int, int]] = None) -> None:
    title = _CHECKPOINTS.get(num, "STEP")
    pos = f"   [{position[0]} of {position[1]}]" if position else ""
    line = "=" * 52
    _print()
    _print(f"[bold]{line}[/bold]")
    _print(f"[bold white]CHECKPOINT {num} - {title}[/bold white][dim]{pos}[/dim]")
    _print(f"[bold]{line}[/bold]")


# ---------------------------------------------------------------------------
# Per-checkpoint renderers
# ---------------------------------------------------------------------------
def _kv_table(rows) -> None:
    if not _RICH:
        for label, value in rows:
            print(f"{label:<14} {value}")
        return
    table = Table(show_header=False, box=None, pad_edge=False)
    table.add_column(justify="left", style="cyan", no_wrap=True)
    table.add_column(justify="left", style="white")
    for label, value in rows:
        table.add_row(label, str(value))
    console.print(table)


def render_recon(config: dict, position=None) -> None:
    banner(1, position)
    auth = config.get("auth", {})
    auth_str = auth.get("type", "none")
    if auth.get("notes"):
        auth_str += f" ({auth['notes']})"
    joins = config.get("joins_to", [])
    joins_str = (
        ", ".join(f"{j.get('source')} ({j.get('on')})" for j in joins) if joins else "—"
    )
    desc = config.get("description", "")
    source_line = f"{config['name']}" + (f" ({desc})" if desc else "")
    access = config.get("access_method", "")
    pattern = config.get("access_pattern", "")
    access_str = f"{access} [{pattern}]" if access and pattern else (access or pattern or "unknown")

    _kv_table(
        [
            ("Source:", source_line),
            ("SOURCE_ID:", config.get("source_id", "")),
            ("URL:", config["url"]),
            ("Jurisdiction:", config.get("jurisdiction", "")),
            ("Category:", config.get("category", "") + (f" / {config['subcategory']}" if config.get("subcategory") else "")),
            ("Publisher:", config.get("publisher", "") or "—"),
            ("Access:", access_str),
            ("Auth:", auth_str),
            ("Format:", config.get("format", "unknown")),
            ("Volume:", config.get("volume", "unknown")),
            ("Update:", config.get("update_cadence", "unknown")),
            ("Key IDs:", ", ".join(config.get("key_identifiers", [])) or "—"),
            ("Priority:", "tier " + str(config.get("priority_tier", "2"))),
            ("Landing:", f"{settings.raw_database}.{settings.raw_schema}.{config.get('landing_table','')}"),
            ("Staging:", config.get("staging_model", "")),
            ("Mart:", config.get("mart_model", "")),
            ("Joins to:", joins_str),
        ]
    )
    if config.get("accountability_relevance"):
        _print(f"\n[dim]Why it matters:[/dim] {config['accountability_relevance']}")
    fields = config.get("schema_fields", [])
    if fields:
        _print(f"\n[dim]Schema ({len(fields)} fields):[/dim]")
        for f in fields[:15]:
            _print(
                f"  [white]{f.get('name','?')}[/white] "
                f"[dim]{f.get('type','')}[/dim]  {f.get('description','')}"
            )
        if len(fields) > 15:
            _print(f"  [dim]... and {len(fields) - 15} more[/dim]")
    if config.get("fetch_error"):
        warn(f"Page fetch issue: {config['fetch_error']} (recon proceeded anyway)")


def render_script(config: dict, code: str, position=None) -> None:
    banner(2, position)
    info(f"Ingestion script for {config['name']} ({config.get('access_pattern')})")
    info(f"Target: {settings.raw_database}.{settings.raw_schema}.{config.get('landing_table','')}")
    _print()
    if _RICH:
        console.print(Syntax(code, "python", theme="ansi_dark", line_numbers=True))
    else:
        print(code)


def render_load(config: dict, result: dict, position=None) -> None:
    banner(3, position)
    sha = result.get("sha256", "")
    _kv_table(
        [
            ("Landing:", f"{settings.raw_database}.{settings.raw_schema}.{config.get('landing_table','')}"),
            ("Run ID:", result.get("run_id", "")),
            ("Content SHA-256:", (sha[:24] + "…") if len(sha) > 24 else sha),
            ("Source bytes:", f"{result.get('file_bytes', 0):,}"),
            ("Rows loaded:", f"{result.get('rows', 0):,}"),
            ("Columns:", result.get("columns", "")),
            ("Status:", result.get("status", "")),
        ]
    )
    sample = result.get("sample_rows", [])
    if sample:
        _print(f"\n[dim]Sample rows ({len(sample)}):[/dim]")
        if _RICH:
            tbl = Table(show_header=True, header_style="bold cyan", box=None)
            for col in sample[0].keys():
                tbl.add_column(str(col))
            for row in sample:
                tbl.add_row(*[str(v) for v in row.values()])
            console.print(tbl)
        else:
            for row in sample:
                print(row)


def render_dbt(config: dict, files: dict, position=None) -> None:
    banner(4, position)
    info("Generated dbt models:")
    for path in files.get("written", []):
        success(path)
    if files.get("note"):
        warn(files["note"])
    for label, key in (
        ("Staging", "staging_sql"),
        ("Intermediate", "intermediate_sql"),
        ("Mart", "mart_sql"),
        ("schema.yml", "schema_yml"),
    ):
        body = files.get(key)
        if not body or not str(body).strip():
            continue
        _print(f"\n[bold cyan]── {label} ──[/bold cyan]")
        if _RICH:
            lang = "yaml" if key == "schema_yml" else "sql"
            console.print(Syntax(body, lang, theme="ansi_dark"))
        else:
            print(body)


def render_registry(config: dict, result: dict, position=None) -> None:
    banner(5, position)
    _kv_table(
        [
            ("SOURCE_ID:", result.get("source_id", config.get("source_id", ""))),
            ("Registry:", result.get("fqn", "")),
            ("Join keys:", result.get("join_keys", "") or "—"),
            ("Status:", result.get("status", "")),
        ]
    )
    preview = result.get("preview")
    if preview:
        _print("[dim]Row preview:[/dim] " + ", ".join(f"{k}={v}" for k, v in preview.items()))


def render_connect(config: dict, result: dict, position=None) -> None:
    banner(6, position)
    result = result or {}
    detail = result.get("detail", {}) or {}
    rows = [
        ("Landing:", config.get("landing_table", "")),
        ("Mode:", result.get("mode") or detail.get("mode", "")),
    ]
    if "affected" in detail:
        rows.append(("Affected keys:", f"{detail.get('affected', 0):,}"))
    if "edges_kept" in detail:
        rows.append(("Edges kept:", detail.get("edges_kept")))
    rows.append(("Status:", result.get("status", "")))
    _kv_table(rows)
    if not result.get("ok", True):
        warn("CONNECT did not finish cleanly — `connect connect-changed` will retry it.")


# ---------------------------------------------------------------------------
# The approval prompt
# ---------------------------------------------------------------------------
def prompt_action(allow_skip: bool = True) -> Tuple[str, Optional[str]]:
    """Read a foreman decision. Returns (action, feedback_or_None)."""
    options = "go / edit [feedback]" + (" / skip" if allow_skip else "") + " / abort"

    if settings.auto_approve:
        _print(f"[dim]-> {options}[/dim]")
        _print("[dim](auto-approve: go)[/dim]")
        return GO, None

    while True:
        _print(f"\n[bold]-> {options}[/bold]")
        try:
            raw = input("  ").strip()
        except (EOFError, KeyboardInterrupt):
            _print()
            return ABORT, None

        if not raw:
            continue
        head, _, rest = raw.partition(" ")
        head = head.lower()

        if head in ("go", "g", "yes", "y"):
            return GO, None
        if head in ("edit", "e"):
            feedback = rest.strip()
            if not feedback:
                warn("edit needs feedback, e.g. `edit use the bulk CSV endpoint`")
                continue
            return EDIT, feedback
        if head in ("skip", "s") and allow_skip:
            return SKIP, None
        if head in ("abort", "a", "quit", "q"):
            return ABORT, None
        warn(f"Unrecognized: '{raw}'. Use: {options}")
