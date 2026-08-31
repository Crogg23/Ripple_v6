# Handoff: Make Chris able to explain Ripple, cold, to anyone

**Repo:** c:\Code\Ripple_v6 (git, branch `main`)
**Read first:** `CLAUDE.md` at repo root (the operating constitution) — this handoff
follows its Beer Rule on purpose; that rule *is* the tone spec for this task.

**How to use this doc:** paste this whole file as your opening message in a new
session. Tell the agent to run it as a live conversation with you, not a solo
writing task. Budget 30–45 minutes of back-and-forth. This is not a "go build a
thing" task — if the agent starts writing files in the first five minutes
without talking to you first, that's it doing the wrong task.

---

## Why this exists

Chris can build Ripple. Chris cannot yet *explain* Ripple — not because he
doesn't understand it, but because nobody has made him say it out loud, in his
own words, in front of a skeptical question. Two good written artifacts already
exist (`docs/ripple_pitch_deck.md`, `docs/RIPPLE_FOR_EVERYONE.md`) and don't
need a rewrite — they need (1) a numbers refresh against live reality, and (2)
a companion session that gets the explanation INTO Chris, not just onto a page.

The test for whether this session worked: Chris can be asked "so what does your
thing actually do?" by a stranger at a party, with zero notes, and give a
90-second answer that's accurate, jargon-free, and sounds like *him* — not like
he's reciting something an AI wrote.

## What NOT to do

- Don't write a new pitch doc from a blank page. The two existing docs are
  genuinely good — open both first (`docs/ripple_pitch_deck.md`,
  `docs/RIPPLE_FOR_EVERYONE.md`) and treat them as the draft, not the target.
- Don't lecture. If you catch yourself writing three paragraphs explaining a
  concept before Chris has said anything, stop — ask him what HE thinks it
  does first, then correct only what's wrong.
- Don't invent or reuse stale numbers. Pull current ones live (see "Ground it
  in reality" below) — the pitch deck's "500 million rows" and "773 banned
  providers" are both out of date as of this session.
- Don't produce a finished doc as the *first* output. The conversation comes
  first. The refreshed doc is what falls out of it afterward.

## Tone (this is not optional — it's the whole point)

Curiosity-driven, not instructional. Every explanation should feel like a
discovery Chris is making WITH the agent, not a fact being delivered TO him.
Concretely:

- Start every new concept with a real example or a question, never a
  definition. ("Here's a doctor who's on two lists that shouldn't overlap —
  why do you think that matters?" not "Ripple performs entity resolution
  across heterogeneous public datasets.")
- No jargon without earning it. If a term like "entity resolution" or "fact
  vs. lead" needs to be used, it gets introduced through the example first,
  named second. Never the reverse.
- Plain words, full truth — per CLAUDE.md's Beer Rule. Simplify the language,
  never the substance. If a part of Ripple is genuinely unfinished or shaky
  (see "Known soft spots" below), say so plainly; don't paper over it with
  confident-sounding language.
- Short exchanges. Ask one thing, wait, react to the actual answer. This is a
  conversation, not a monologue with pauses.

## Ground it in reality first (do this before talking to Chris)

Pull a handful of CURRENT, real numbers so nothing in the conversation is
stale or invented. Suggested pulls (read-only, use `scripts/_snowflake_conn.py`
same as prior sessions in this repo):

- Total landed rows and table count (`LIBRARY_META.REGISTRY` or equivalent —
  check `build-state.md`'s "DATA STATE" section for the live query).
- Current `lead_queue` row count and its breakdown by detector (`rule_name` /
  `detector` column) — this replaces the pitch deck's stale "773" number with
  today's real one.
- One live example lead from `lead_queue` — a real name, a real dollar figure,
  a real date range — to use as the opening hook, the same way the pitch deck
  already opens with the banned-doctor story. A different real one is fine and
  arguably better (proves this isn't a one-off).
- The current fact/lead/unverified split from `honesty/mart_grades.json`
  (391 marts: 389 fact, 1 lead, 1 unverified as of 2026-07-30 — reconfirm live).

## Session structure (rough shape, adapt to how Chris responds)

1. **Open with the live example**, not a definition. Show Chris the one real
   lead you pulled. Ask him to explain in his own words why it's interesting
   before offering any framing.
2. **Build the mechanism WITH him**, piece by piece, each time starting from
   "what do you think happens next" rather than telling him. Use the existing
   four-verb framing (scout / collect / connect / explore) from
   `docs/RIPPLE_FOR_EVERYONE.md` as scaffolding, but verify it still matches
   the current architecture before reusing it — check `OVERVIEW.md`.
3. **Introduce the fact-vs-lead distinction** (the "honesty engine") as the
   moment the story turns from "cool trick" to "trustworthy tool" — this is
   the single most portfolio-differentiating idea in the whole project
   (`honesty/README.md` explains why); it deserves real weight, not a
   footnote.
4. **Teach-back checkpoint.** At least twice during the session, stop and ask
   Chris to explain the piece you just covered back to you, unprompted, as if
   you were a stranger. Correct gently, only what's actually wrong. This step
   is the actual point of the exercise — don't skip it to save time.
5. **Stress-test him.** Ask 2–3 skeptical-stranger questions a real person
   would ask ("isn't this just doxxing people?" / "how is this different from
   a search engine?" / "why should I trust a computer's idea of a pattern?").
   Let Chris attempt an answer first; only help if he's genuinely stuck.
6. **Close by refreshing the artifact**, not writing a new one: update the
   live numbers and the opening example in `docs/ripple_pitch_deck.md` and/or
   `docs/RIPPLE_FOR_EVERYONE.md` (small, surgical edits, not a rewrite), and
   write a short (under 150 words) "the 90-second answer" cheat-sheet in
   Chris's own words from the conversation — capture HIS phrasing, not a
   polished AI paraphrase of it.

## Known soft spots to be honest about, not hide

If these come up (they might, especially in the stress-test step), don't spin
them — Chris explicitly does not want to sound like he's overselling:

- Ripple has flagged real leads but none are yet human-confirmed/published —
  it finds candidates for a journalist to check, it doesn't publish findings
  itself (`CLAUDE.md`: "human sign-off required on every finding, no
  exceptions").
- A meaningful slice of the newer data sources (roughly a third of the
  platform, added in a recent onboarding wave) don't have automatic
  data-quality checks yet — real, being worked on, not hidden.
- There's one open security item (an overly-powerful access credential being
  used day-to-day) that Chris owns and hasn't rotated yet — don't bring this
  up unprompted in a portfolio context, but if directly asked "is this
  production-grade," the honest answer is "not yet, here's what's left."

## Done looks like

- Chris has said the 90-second explanation out loud, unprompted, at least
  once, and it held up under a skeptical follow-up question.
- A short written cheat-sheet exists in Chris's own words (not this session's
  prose) that he could glance at before an interview or a demo.
- `docs/ripple_pitch_deck.md` and/or `docs/RIPPLE_FOR_EVERYONE.md` have
  current numbers, not stale ones.
