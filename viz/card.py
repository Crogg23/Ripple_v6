"""Chart cards: every question becomes a standalone, runnable, EDITABLE .py file.

The card is the hot loop and the learning ramp in one artifact:

    investigations/<slug>_<started>/q01_<name>.py     <- the code (commit this)
    investigations/<slug>_<started>/q01_<name>.html   <- the chart (gitignored)

Edit the SQL string or the plug kwargs, run the file, F5 the browser tab.
`ripple chart eject <card.py>` inlines the plug's actual Plotly source into the
card (inspect.getsource — the plug body IS the template, nothing to drift), so
hand-tuning raw px/go code is one command away.

Cards are written utf-8 with ASCII-only content, bootstrap their own sys.path
by walking up to the repo root (the dir holding ripple.py), and embed plotly.js
once per investigation folder (include_plotlyjs='directory') so a folder is a
self-contained offline artifact measured in KB, not MB.
"""

from __future__ import annotations

import inspect
import re
import textwrap
from datetime import date
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
INVESTIGATIONS = _REPO / "investigations"
_SLUG_RE = re.compile(r"[^a-z0-9_]+")

CARD_TEMPLATE = '''\
# Chart card - the whole loop is: edit the SQL or the plug kwargs below, then
#     python {fname}
# and refresh the browser tab (the .html next to this file is rewritten in place).
# Deeper: `ripple chart eject {fname}` inlines the plug's real Plotly code here.

import os
import sys
from pathlib import Path

# Find the repo root (the directory holding ripple.py) so `import viz` works
# from ANY current directory: RIPPLE_REPO env wins, then walking up from this
# file, then the repo this card was generated from.
_d = Path(os.environ.get("RIPPLE_REPO") or Path(__file__).resolve().parent)
while not (_d / "ripple.py").exists() and _d.parent != _d:
    _d = _d.parent
if not (_d / "ripple.py").exists():
    _d = Path({repo!r})  # where this card was generated
if str(_d) not in sys.path:
    sys.path.insert(0, str(_d))

from viz import plugs, safety, sqlrun, theme  # noqa: E402

if os.environ.get("RIPPLE_CARD_DRY"):
    print("[OK] card imports resolve (dry run)")
    raise SystemExit(0)

SQL = """\\
{sql}
"""

df, meta = sqlrun.run(SQL{run_args})
print("[OK] " + str(len(df)) + " rows in " + str(meta["elapsed_s"]) + "s on "
      + str(meta["warehouse"]) + " | " + str(meta["budget"]))

# --- plug call (ripple chart eject inlines this) ---
fig = plugs.{plug}(df{plug_args})
# --- end plug call ---
{badge_line}
OUT = Path(__file__).with_suffix(".html")
import webbrowser  # noqa: E402
fig.write_html(OUT, include_plotlyjs="directory", config=theme.PLOT_CONFIG)
print("[OK] wrote " + OUT.name)
if not os.environ.get("RIPPLE_NO_OPEN"):
    webbrowser.open(OUT.resolve().as_uri())
'''


def slugify(text: str) -> str:
    s = _SLUG_RE.sub("_", str(text).strip().lower()).strip("_")
    return (s or "question")[:40]


def render_body(fname: str, sql: str, plug: str, plug_kwargs: dict | None = None,
                classification: dict | None = None, unsafe_claims: bool = False,
                limit_rows: int | None = None) -> str:
    """The card body as text — the ONE place it is built (CLI, Workbench preview
    and save all call this, so what you see is always what gets saved)."""
    from viz import safety as _safety

    plug_args = ""
    for k, v in (plug_kwargs or {}).items():
        plug_args += f", {k}={v!r}"
    plug_args += ', as_of=meta["as_of"]'

    run_args = ""
    if limit_rows:
        run_args += f", limit_rows={int(limit_rows)}"
    if unsafe_claims:
        run_args += ", unsafe_claims=True"

    badge_line = ""
    if classification:
        ba = _safety.badge_args(classification)
        if ba:
            state, text = ba
            badge_line = f"fig = safety.badge(fig, {state!r}, {text!r})\n"

    # Escape for embedding in a (non-raw) triple-quoted literal: without this a
    # SPLIT_PART(x, '\t', 3) card silently sends a real TAB to Snowflake on
    # re-run, and '\x' or an embedded triple-quote corrupts the file outright.
    sql_lit = (sql.rstrip().rstrip(";")
               .replace("\\", "\\\\")
               .replace('"""', '\\"\\"\\"'))

    return CARD_TEMPLATE.format(
        fname=fname, sql=sql_lit, plug=plug, plug_args=plug_args,
        run_args=run_args, badge_line=badge_line, repo=str(_REPO),
    )


def new_card(slug: str, sql: str, plug: str = "table", plug_kwargs: dict | None = None,
             classification: dict | None = None, unsafe_claims: bool = False,
             limit_rows: int | None = None, name: str | None = None,
             new: bool = False, outdir: Path | None = None) -> Path:
    """Write a chart card; returns its path.

    Overwrite rule: an EXPLICITLY named card is overwritten on re-run (iterating
    one question shouldn't scatter 15 near-duplicates); an auto-named card (name
    defaulted from the plug) always forks — two different questions that both
    auto-suggest 'bar' must not clobber each other. Ejected (hand-tuned) cards
    are never overwritten. `new=True` always forks."""
    slug = slugify(slug)
    root = (outdir or INVESTIGATIONS)
    dirs = sorted(root.glob(f"{slug}_*"))
    card_dir = dirs[-1] if dirs else root / f"{slug}_{date.today().isoformat()}"
    card_dir.mkdir(parents=True, exist_ok=True)

    name_given = bool(name)
    name = slugify(name or plug)
    existing = sorted(card_dir.glob("q*.py"))
    same = [p for p in existing
            if not new and name_given and p.stem.split("_", 1)[-1] == name
            and "ejected from viz/plugs.py" not in p.read_text(encoding="utf-8")]
    if same:
        path = same[-1]
    else:
        nums = [int(m.group(1)) for p in existing
                if (m := re.match(r"q(\d+)_", p.name))]
        path = card_dir / f"q{max(nums, default=0) + 1:02d}_{name}.py"

    body = render_body(path.name, sql, plug, plug_kwargs, classification,
                       unsafe_claims, limit_rows)
    path.write_text(body, encoding="utf-8")
    return path


def latest_card(outdir: Path | None = None) -> Path | None:
    """The most recently modified card across all investigations."""
    root = outdir or INVESTIGATIONS
    cards = sorted(root.glob("*/q*.py"), key=lambda p: p.stat().st_mtime)
    return cards[-1] if cards else None


# --------------------------------------------------------------------------- #
# eject: inline the plug's REAL source into the card (zero template drift)
# --------------------------------------------------------------------------- #
def eject(card_path: str | Path) -> Path:
    """Rewrite a card with the plug body (and its helpers) inlined, so the card
    is self-sufficient raw Plotly code Chris can tune line by line."""
    from viz import plugs as _plugs

    path = Path(card_path)
    text = path.read_text(encoding="utf-8")
    m = re.search(r"fig = plugs\.(\w+)\(", text)
    if not m:
        raise ValueError(f"no plug call found in {path} (already ejected?)")
    plug_name = m.group(1)
    fn = _plugs.PLUGS[plug_name]

    consts = "\n".join(
        f"{n} = {getattr(_plugs, n)!r}"
        for n in ("META_COLS", "MAX_CATEGORIES", "MAX_TABLE_ROWS", "_US_STATES", "PARTY_COLORS")
    )
    helper_src = "\n\n".join(
        textwrap.dedent(inspect.getsource(h)) for h in _plugs.EJECT_HELPERS
    )
    plug_src = textwrap.dedent(inspect.getsource(fn))
    block = (
        "# --- ejected from viz/plugs.py: this is the plug's real code, tune freely ---\n"
        "import datetime as _dt  # noqa: E402\n"
        f"{consts}\n\n{helper_src}\n\n{plug_src}"
        "# --- end ejected code ---\n\n"
    )

    text = text.replace("# --- plug call (ripple chart eject inlines this) ---\n",
                        block + "# --- plug call (now local - the function above) ---\n", 1)
    text = text.replace(f"fig = plugs.{plug_name}(", f"fig = {plug_name}(", 1)
    path.write_text(text, encoding="utf-8")
    return path
