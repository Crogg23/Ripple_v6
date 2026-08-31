"""Ripple — What Is This?

A plain-English explainer of what Ripple does, what data it holds, and why
it exists. Written so that anyone — investor, journalist, friend, stranger —
can read it cold and understand.
"""
import streamlit as st

st.set_page_config(page_title="Ripple — What Is This?", page_icon="📡", layout="wide")

st.markdown("""
# What Is This?

## The short version

Every year, the U.S. government publishes *enormous* amounts of data about
itself — who it pays, who it bans, who it licenses, who it fines. Thousands
of databases, all public, all free.

**The problem?** None of them talk to each other.

The database that tracks banned doctors doesn't know about the database that
tracks Medicare payments. The database that lists sanctioned ships doesn't
cross-reference port records. Each agency publishes its own silo and moves on.

**Ripple connects them.** We pour all of that public data into one place, then
build a machine that finds the *same person or company* across different
databases — and flags the contradictions.

---

## What kind of contradictions?

Here's a real example of what the system finds:

> A doctor gets excluded from federal healthcare programs (they're on an
> official "banned" list). But in a *different* government database, that same
> doctor is still receiving Medicare payments — sometimes for years after the ban.

That's not a hypothetical. The system currently flags **773 cases** like that.

Other things it finds:
- **Sanctioned vessels still broadcasting** — ships on a Treasury sanctions list
  that are still showing up in U.S. maritime tracking data
- **Debarred contractors still getting federal awards** — companies banned from
  government contracts that appear in the spending database anyway
- **Excluded providers still billing** — similar to the doctor example, but for
  facilities and other healthcare providers

---

## How does it actually work?

Think of it in three layers:

### Layer 1: The Library
We collect publicly available government datasets. Right now that's about
**1,942 tables** containing roughly **600 million rows** of data. These come
from agencies like:
- FDA (drug adverse events, recalls)
- SEC (financial filings, institutional holdings)
- CMS/HHS (Medicare payments, hospital data, banned providers)
- EPA (facility registries, enforcement)
- Treasury/OFAC (sanctions lists)
- DOJ (court records)
- And hundreds more

Every table is raw public data. We don't modify it, interpret it, or editorialize.
We just put it all in one room.

### Layer 2: The Connection Engine
This is the clever part. The engine looks at all those tables and asks:
*"Does this person/company/facility appear in more than one database?"*

It does this by matching on hard identifiers — things like:
- **NPI** (National Provider Identifier — every doctor/nurse has one)
- **EIN** (Employer Identification Number — every company has one)
- **LEI** (Legal Entity Identifier — international companies)
- **IMO** (ship identification numbers)
- **CIK** (SEC filing numbers)

When it finds the same identifier in two different databases, that's a
**connection** — proof that the same real-world entity appears in both places.

Right now: **16.2 million resolved entities** connected by **11,197 cross-database links**.

### Layer 3: The Detectors
Once you know a doctor appears in both the "banned" list and the "payments"
list, you can ask the obvious question: *should they?*

Detectors are simple rules:
- "Show me everyone on List A who also appears on List B, where being on
  both is a contradiction."

That's it. No AI interpretation. No opinion. Just: *here are the cases where
the government's own data contradicts itself.*

---

## What this is NOT

- **Not surveillance.** We only look at public government data about
  institutions and public figures acting in their official capacity.
  No private individuals. No scraped social media. No purchased data.
- **Not accusations.** A flag means "this looks like a contradiction in
  government records." It might be a data lag, a clerical error, or a real
  problem. Every flag gets human review before anyone says anything about it.
- **Not automated.** Nothing publishes without a human explicitly approving it.
  The machine finds patterns. Humans decide what they mean.

---

## Why does this matter?

Because right now, **nobody is doing this systematically.**

Journalists investigate one case at a time. Government auditors check one
program at a time. Nobody pours it all together and asks: *"across ALL of
this data, where are the contradictions?"*

That's the gap Ripple fills. Not by targeting anyone — by looking at
*everyone*, the same way, with the same lens. A census of contradictions,
not a subpoena.

---

## The numbers right now

| What | Count |
|------|-------|
| Government databases loaded | ~1,942 |
| Total data rows | ~600 million |
| Unique entities resolved | ~16.2 million |
| Cross-database connections | ~11,197 |
| Active red flags (leads) | ~1,040 |
| Detectors running | 7 |

---

*This page is part of Mission Control — the internal dashboard for the Ripple project.*
""")
