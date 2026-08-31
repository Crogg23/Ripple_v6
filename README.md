# Ripple

Ripple pours the public record — government datasets on doctors, companies,
ships, contracts, sanctions — into one Snowflake warehouse, draws only the
connections that can't be faked (shared government IDs, never name guesses),
and points at the ones that shouldn't exist: banned but still paid, debarred
but still funded, sanctioned but still broadcasting. Nothing is ever published
without an explicit human decision; auto-publish is structurally blocked.

## Read this first

**[`STARTING_ROSTER.md`](STARTING_ROSTER.md)** — the line between live and
dead work. If a folder isn't on the roster, it's retired; retired work lives
in `_JUNK_DRAWER/` with a LEDGER.md row.

**[`docs/RIPPLE.md`](docs/RIPPLE.md)** — the whole thing in one document:
the plain-English story, a decoder for every jargon word, a room-by-room map
of this repo, how to turn it on, and the deep tour of how it works.

Then, as needed:

- [`build-state.md`](build-state.md) — the instrument panel. Machine-generated
  live numbers; the **only** numbers to trust. Prose numbers anywhere else are
  stale by definition.
- [`CHRIS_DECISIONS.md`](CHRIS_DECISIONS.md) — the owner's decision ledger.
- [`CLAUDE.md`](CLAUDE.md) — the operating constitution. Wins every argument.
- [`docs/ripple_pitch_deck.md`](docs/ripple_pitch_deck.md) — the outward-facing
  overview. [`docs/RIPPLE_DESIGN_BRIEF.md`](docs/RIPPLE_DESIGN_BRIEF.md) — for
  whoever builds the visual layer.

## Quick start

macOS setup lives in [`docs/MAC_SETUP.md`](docs/MAC_SETUP.md). The old
Windows `.bat` launchers and the Reading Room app are retired to the drawer.

From a terminal, after `pip install -r requirements.txt` into a venv and
dropping your Snowflake token into `library-onboarding/.env` (template beside
it):

```bash
python -m connect all                    # rebuild the connection map + leads
python library-onboarding/onboard.py     # walk a new source into the Library
python ripple.py chart                   # make a chart from warehouse data
```

Dev/test extras: `pip install -r requirements-dev.txt`.

> **dbt note:** dbt runs the 1,378 cleanup models in
> `library-onboarding/ripple_dbt` but is **deliberately not in
> `requirements.txt`** — `dbt-snowflake` needs `snowflake-connector-python~=3.0`,
> which conflicts with this repo's `==4.4.0` pin. Give it its own venv:
>
> ```bash
> python -m venv .dbt-venv && .dbt-venv/Scripts/pip install -r requirements-dbt.txt
> ```
>
> And never run a bare `dbt build` — see `docs/RIPPLE.md` §7.
