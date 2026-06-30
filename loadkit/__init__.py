"""loadkit -- shared, offline-tested safety scaffolding for Ripple data loads.

Built during the US-politics load planning so a build session can be "let loose"
without troubleshooting or cleanup. Every risky load reuses these instead of
reinventing them:

  fec_parse    quote-aware, fail-loud parsing (no silent column-shift -> no wrong $)
  preflight    refuse to START a load that would die mid-stream (PAT/budget/key/deps)
  windowed     recursive window planning + a count referee for cursor-hostile APIs
  checkpoint   durable per-window resume
  atomic_load  land-to-staging + atomic swap (a crash leaves nothing to clean up)
  smoke        reconciliation referees (a load is not "done" until its numbers tie)

Each module exposes a PURE, importable core (no Snowflake, no network) that is unit
-tested offline; the thin live I/O wrappers are marked `# pragma: no cover`.

See outputs/POLITICS_BUILD_RUNBOOK.md for how these compose into the build, and the
GitHub issues (Phase 0-6) for the per-task specs.
"""

__all__ = ["fec_parse", "preflight", "windowed", "checkpoint", "atomic_load", "smoke"]
