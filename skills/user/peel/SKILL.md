---
name: peel
description: >
  Investigative instrument. Takes any input — a news story, a headline, or just a hunch — runs it through four moves and points at where to dig, using public, legal, ethically-sourced data only. Trigger on "/peel" AND on any natural signal that Chris wants the layer under a story: "what's really going on here," "dig into this," "peel this," "is this systemic," "where's the data on this," "follow the money," "this smells off," or any time he drops a link or headline and wants the mechanism underneath. The four moves are reaction → mechanism → residue → class, then the zoom test (one case → one actor → one system), then a "where to dig next" list of named public datasets and join keys. Enforce the discipline rule every time: a connection only counts as a FINDING if public data can hold it — otherwise it's a HYPOTHESIS.
---

# Peel

Take the story apart layer by layer until the public data underneath shows. The visible event sits on top; the system sits at the bottom. Peel down.

## When this fires

- He types `/peel`
- OR any natural signal: "what's really going on here," "dig into this," "peel this," "is this systemic," "where's the data," "follow the money," "this smells off," or he drops a headline or link and wants the layer under it

Input can be anything — a polished story, a one-line headline, or a half-formed hunch. You don't need a clean question to start.

## Two rules that govern everything

**Sourcing.** Public, legal, ethically-sourced data only. No leaks, no scraping behind logins, no private records.

**Discipline — enforce every time.** A connection only counts if public data can hold it: a shared **key, dollar, address, or timestamp.**
- Data can hold it → **FINDING.**
- It only lives as a feeling → **HYPOTHESIS** — chase it, don't publish it.

Never dress a hypothesis as a finding. No exceptions.

## The four moves

Run all four, in order, every time.

1. **The reaction** — the visible event, one line. What can we see happened?
2. **The mechanism** — why did it behave that way? The rule, loophole, or incentive underneath. Not *what* happened — *what made it* happen.
3. **The residue** — if that mechanism is real, it HAD to leave a trail. Name the specific public dataset(s) that would hold the proof and the **join key** that reaches it (FIPS, EIN, CIK, UEI, LEI, NPI, NDC, lat/lon, country ISO, …). Check the registry first — `LIBRARY_META.REGISTRY.SOURCE_REGISTRY` — before naming something we'd have to onboard.
4. **The class** — the mechanism is rarely a one-off. Describe the whole class of cases with the same shape, and where that class's trail lives at scale.

## The zoom test (the fractal check)

Restate the story at three zoom levels:

```
one case   →   one actor   →   one system
```

- Shape holds at all three → tag **SYSTEMIC**
- Shape breaks somewhere → tag **ONE-OFF**

## Output

Always this shape, scannable:

1. **The four moves** — reaction, mechanism, residue, class. One tight beat each.
2. **Zoom-test tag** — SYSTEMIC or ONE-OFF, plus one line on why.
3. **Where to dig next** — named public dataset(s) + join key(s), and whether each is already in the Library or needs onboarding.

The point is to aim the next move, not to write the article. Keep it tight.
