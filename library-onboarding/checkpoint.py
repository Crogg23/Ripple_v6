"""Checkpoint rendering + the foreman approval prompt.

Every checkpoint shares the same shape: a banner with the step name and a
``[i of N]`` position counter (in batch mode), a body, then the action prompt:

    -> go / edit [feedback] / skip / abort
"""

from __future__ import annotations

from typing import Optional, Tuple

from config import settings

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.table import Table
    from rich.text import Text

    _RICH = True
    console = Console()
except ImportError:  # pragma: no cover - degrade to plain print
    _RICH = False
    console = None  # type: ignore

# Action constants
GO, EDIT, SKIP, ABORT = "go", "edit", "skip", "abort"

_CHECKPOINTS = {
    1: "RECON",
    2: "SCRIPT",
    3: "LOAD",
    4: "DBT",
    5: "CATALOG",
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
    line = "━" * 52
    _print()
    _print(f"[bold]{line}[/bold]")
    _print(f"[bold white]CHECKPOINT {num} — {title}[/bold white][dim]{pos}[/dim]")
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

    _kv_table(
        [
            ("Source:", source_line),
            ("URL:", config["url"]),
            ("Access:", config.get("access_pattern", "unknown")),
            ("Auth:", auth_str),
            ("Format:", config.get("format", "unknown")),
            ("Est. volume:", config.get("est_volume", "unknown")),
            ("Update:", config.get("update_frequency", "unknown")),
            ("Key IDs:", ", ".join(config.get("key_identifiers", [])) or "—"),
            ("Rate limits:", config.get("rate_limits", "unspecified")),
            ("Raw table:", config.get("raw_table", "")),
            ("Staging:", config.get("staging_model", "")),
            ("Mart:", config.get("mart_model", "")),
            ("Joins to:", joins_str),
        ]
    )
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
    info(f"Target: {config.get('raw_table')}")
    _print()
    if _RICH:
        console.print(Syntax(code, "python", theme="ansi_dark", line_numbers=True))
    else:
        print(code)


def render_load(config: dict, result: dict, position=None) -> None:
    banner(3, position)
    _kv_table(
        [
            ("Table:", config.get("raw_table", "")),
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
    for label, key in (("Staging", "staging_sql"), ("Mart", "mart_sql"), ("schema.yml", "schema_yml")):
        body = files.get(key)
        if not body:
            continue
        _print(f"\n[bold cyan]── {label} ──[/bold cyan]")
        if _RICH:
            lang = "yaml" if key == "schema_yml" else "sql"
            console.print(Syntax(body, lang, theme="ansi_dark"))
        else:
            print(body)


def render_catalog(config: dict, result: dict, position=None) -> None:
    banner(5, position)
    _kv_table(
        [
            ("Entity:", result.get("fqn", config.get("raw_table", ""))),
            ("OpenMetadata:", result.get("url", settings.openmetadata_host)),
            ("Columns:", result.get("column_count", "")),
            ("Status:", result.get("status", "")),
        ]
    )
    if result.get("identifiers"):
        _print(f"[dim]Key identifiers tagged:[/dim] {', '.join(result['identifiers'])}")


# ---------------------------------------------------------------------------
# The approval prompt
# ---------------------------------------------------------------------------
def prompt_action(allow_skip: bool = True) -> Tuple[str, Optional[str]]:
    """Read a foreman decision. Returns (action, feedback_or_None)."""
    options = "go / edit [feedback]" + (" / skip" if allow_skip else "") + " / abort"

    if settings.auto_approve:
        _print(f"[dim]→ {options}[/dim]")
        _print("[dim](auto-approve: go)[/dim]")
        return GO, None

    while True:
        _print(f"\n[bold]→ {options}[/bold]")
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
