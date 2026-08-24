# THE_SCRIPT — Portfolio Copy Bank

Pull-from bullets for portfolio text. General-adult / hiring-manager reading level. No jargon, no internal codenames — just what the system does and why it's impressive.

---

## 1. Scale

- 558 government data sources unified into one queryable system.
- 1.23 billion records, spanning courts, safety inspections, federal spending, and corporate filings.
- A single dataset — FDA drug side-effect reports — contributes 62 million records on its own.
- Built and maintained solo, at a scale most small teams don't attempt.
- Not a snapshot: sources are re-pulled and re-verified on an ongoing basis, not loaded once and left.

## 2. Data Cleaning

- Maintains an active data-quality registry tracking 174 fields known to misrepresent themselves as complete.
- Caught and corrected a systemic bug where plain years (1998, 2005…) were silently erased across 29 tables — a defect that would look like nothing was wrong until someone checked.
- When a dataset fails quality checks, it gets fully rebuilt and verified record-by-record, not patched over.
- Runs a 4,800+ test suite against the data itself, not just the code that moves it.
- Distinguishes "loaded" from "trustworthy" as two separate, tracked states — nothing is assumed clean by default.

## 3. Organization

- Structured in three deliberate stages: raw as-published data, standardized/corrected data, and finished analysis-ready tables.
- 75 finished tables rebuilt in a single week — an actively maintained system, not a static archive.
- Designed so the system runs on plain, inspectable logic (SQL/dbt) rather than a black box.
- Every table's reliability is documented, not just its existence.

## 4. Connections

- Nearly 32 million people and organizations resolved into single identities across every source.
- The strongest identity matches (14 verified ID types, like tax IDs) link with 97–100% accuracy.
- Surfaces hidden relationships — the same company's lawsuits, contracts, and violations, tied together instead of scattered across a dozen disconnected government sites.
- Transparent about confidence: hard-ID matches vs. softer name/location matches are tracked separately, not blended into one false certainty.
- Built entity-resolution from scratch — no off-the-shelf identity-matching product underneath it.

## 5. Why It Exists

- Not a scraping exercise — built to make patterns of harm across public records visible, because no single source shows the whole picture.
- Looks at everyone the same way, with the same lens — a census of the public record, not a search for one target.
- Every finding requires human sign-off before anything is published — nothing here auto-publishes, on purpose.
- Built on the belief that a single anecdote only matters if the data behind it proves the pattern is real and repeated.

## 6. The Engineering Itself

- Runs on a cloud data warehouse (Snowflake) with a modern transformation framework (dbt) — the same stack used at real analytics companies, not custom scripts.
- Designed to run on plain SQL long-term — AI helped build it, but the finished system doesn't depend on AI to operate.
- Loaders are built to survive real-world failure — API throttling, dropped connections, partial pulls — with checkpointing so a multi-hour job can resume instead of restart.
- Handles messy, inconsistent government data formats (CSV dumps, paginated APIs, bulk extract files) and normalizes them into one consistent structure.

## 7. The Audit Discipline

- Runs recurring self-audits that hunt for exactly the kind of data corruption most projects never check for — and documents what it finds, including the failures.
- Treats "it looks complete" as a hypothesis to test, not a fact to trust — a mindset, not just a tool.
- Scores its own health on a standing 0–100 scale and tracks what moves the number, session to session — accountable to a metric, not a mood.
- Publicly tracks its own known-broken pieces alongside its verified ones, instead of hiding gaps.

## 8. Solo-Builder Scale

- One person, not a team, building and maintaining a system usually run by a data engineering team of several.
- Actively worked and expanded on an ongoing basis — not a one-time project that shipped and stopped.
- Every architectural and technical decision — what to load, how to clean it, how to connect it — made and owned end-to-end.

---

*Pull individual bullets into portfolio sections as needed — not meant to be used as one block of text.*
