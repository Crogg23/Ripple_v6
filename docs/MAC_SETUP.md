# Getting the rules and hooks onto the Mac

Written 2026-08-31. The short version: almost everything travels with the repo.
Three things do not, and one of them is a genuine trap.

## What comes for free with `git clone`

All of this is tracked, so cloning the repo IS the install:

| Piece | Path |
|---|---|
| The constitution | `CLAUDE.md` |
| Corrections that fire every prompt | `.claude/corrections.md` |
| Data traps | `.claude/traps.md` |
| Output style | `.claude/output-styles/scannable.md` |
| Hook wiring | `.claude/settings.json` |
| Every hook | `.claude/hooks/*.sh`, `.claude/hooks/shape_check.py` |
| Slash words | `.claude/commands/*.md` |
| The skeptic | `.claude/agents/skeptic.md` |

Claude Code reads `.claude/settings.json` from the project root, so the hooks
arm themselves the moment the folder exists. No install step.

## What does NOT travel

### 1. Credentials

`library-onboarding/.env` is gitignored, and it holds the Snowflake token.
Without it, `connect/db.py` cannot open the warehouse.
Copy it across by hand. Never commit it.

`.snowflake/` is tracked but the key files under `.keys/` are not.

### 2. Auto-memory

Lives outside the repo, under the user's home directory:

    ~/.claude/projects/c--Code-Ripple-v6/memory/

Four trap notes and one methodology note live there today.
Copy that folder to the same path on the Mac.
The project slug is derived from the checkout path, so put the repo at a path
that produces the same slug, or rename the folder to match what the Mac makes.

### 3. Past transcripts

    ~/.claude/projects/c--Code-Ripple-v6/*.jsonl

217 files, 780 MB. CLAUDE.md says past transcripts are the record and should be
searched before asking Chris to re-explain. Without them that rule is dead on
the Mac. Copy them or accept the loss knowingly.

## The trap: `python` does not exist on macOS

Every hook shells out to an interpreter to read the hook payload JSON.
They were written on Windows, where `python` is on PATH.
A stock macOS ships `python3` and NO bare `python`.

Before 2026-08-31 that meant four hooks exited 127 on a Mac:

| Hook | What silently stopped |
|---|---|
| `block-dangerous-git.sh` | the git guard |
| `warehouse-gate.sh` | the spine and rebuild gates |
| `chris-words.sh` | corrections injection, greenlights, riff/build |
| `drawer-guard.sh` | the junk drawer sting |

Nothing announced it. The gates were simply gone.

**Fixed by `.claude/hooks/_py.sh`**, which every hook now sources. It:

- tries `python3`, then `python`, then `py`;
- makes each candidate PROVE it runs, because `python3` on Windows resolves to
  a Store stub that exits 127 without executing anything;
- fails CLOSED and loudly for the safety gates — no interpreter, no passage;
- fails OPEN and loudly for the conveniences;
- lets `hooks off` win over a missing interpreter, so a broken machine can
  still be worked on.

`tests/test_hooks_portable.py` runs every hook against a fake Mac PATH and
asserts each one still does its job. Nine tests.

## The other trap: the clone is 7 GB

`.git` holds a 6.95 GiB pack, 26,776 objects, no garbage. Multi-GB data files
were committed and later deleted; deleting a file does not remove it from
history. The five largest blobs are 2.7 GB, 2.1 GB, 1.5 GB, 463 MB, 460 MB.

Options, cheapest first:

1. `git clone --depth 1` — a shallow copy skips the history entirely. Fastest
   path to a working Mac. You lose `git log` depth on that clone.
2. Rewrite history to drop the blobs, then force-push. Destructive, needs a
   deliberate decision, and every other clone must be re-cloned after.
3. Copy the working tree by hand and `git init` fresh on the Mac. Loses history.

## Checklist for the Mac

1. Install python3 and confirm `python3 -c "pass"` runs.
2. `git clone --depth 1` the repo.
3. Copy `library-onboarding/.env` across.
4. Copy `~/.claude/projects/c--Code-Ripple-v6/memory/`.
5. Optionally copy the transcripts from the same folder.
6. Run `bash .claude/hooks/test-gate.sh` — expect ALL PASS.
7. Run `pytest tests/test_hooks_portable.py tests/test_shape_gate.py` — expect
   all green.
8. Say `hooks off` then `hooks on` once to confirm the kill switch answers.
