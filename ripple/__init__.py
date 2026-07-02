"""ripple — the single front door to the Library.

One command instead of 54 scripts. Subcommands:
  status   the Morning Deck — your whole world on one screen (read-only)
  doctor   one GREEN/RED go/no-go health check (read-only)
  review   the batch review cockpit — drain the decision queues N at a time
  pour     plan / watch / run the onboarding pour, deterministic-first

Run:  python -m ripple <verb>   (or  python ripple.py <verb>)

Everything reads through COMPUTE_WH by default, so ripple never contends with a
live pour on RIPPLE_WH; anything that would write refuses while a pour is running.
"""
