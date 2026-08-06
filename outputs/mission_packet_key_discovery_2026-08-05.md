# Mission Packet: Key & Join Discovery Sweep

**For:** Fable session
**Follows:** `absence_sweep_findings_2026-08-05.md`
**Trigger:** that sweep only ever touched the *already-connected* part of the warehouse
(2,694 verified edges). It explicitly did not touch:
- **~793 unfingerprinted landing tables** — no key identified, no list of them anywhere,
  just a raw count in `hunch_lattice.json`'s `blind_spots.unfingerprinted_landing`.
- **285 pairs that share a key but have no verified edge** — enumerated, never opened.
- Anything about tables/keys/joins that **should exist but haven't been noticed at all** —
  this sweep only ever reasoned over what the lattice already knows about itself.

We do not get to assume the 895-blind-spot number is close to complete. **We don't know
what we don't know. Don't be lazy about that — go find it, don't just re-read what's
already been read.**

---

## The job

Not another absence sweep. This is a **coverage sweep**: find what keys/joins are missing
from the map, and where the map itself might be blind.

### Track 1 — Inventory the 793 unknowns
No list of these tables exists yet. Build one.
- Diff the full warehouse table list against `hunch_lattice.json`'s known/fingerprinted
  set — produce the actual 793 (or whatever the real number is; the 895/102/793 math in
  the last sweep was never independently checked, verify it first).
- For each: table name, row count, domain guess (from name/schema), and — critically —
  **scan actual column names/samples for anything that looks like an ID**: NPI, EIN, CCN,
  DUNS, UEI, FRS_ID, docket numbers, case IDs, license numbers, any *_ID / *_NO / *_NUM
  column, even if it doesn't match a key already in the spine. New key *types* are as
  valuable as new tables on existing keys.
- Flag tables that are candidates for existing STEEL/STRONG keys vs. tables that might
  need an entirely new key type added to the spine (a key family that doesn't exist yet
  is itself a finding — report it, don't discard it because it doesn't fit the current taxonomy).

### Track 2 — Open the 285 unverified pairs
These share a key on paper but nobody confirmed the join actually works.
- For each: pull a real sample from both sides, check actual value overlap (not just
  "column exists"), and classify: verified / format-mismatch-fixable / false-positive
  (key name matches but semantics don't) / needs-normalization (padding, casing, prefix
  stripping — cf. the HCRIS CCN mismatch already caught in A-4).
- Do not skip the boring ones. The last sweep skipped all 285 on the assumption none would
  outrank the verified pool — that assumption itself was never tested. Test it.

### Track 3 — Adversarial gap-hunt on the existing spine
Assume the current key list (CCN, NPI, EIN, FRS_ID, MINE_ID, CIK, PWSID, DOCKET, BIOGUIDE,
NAME@ZIP) is incomplete even for tables we already have.
- For every domain cluster (HEALTH, FINANCE, ENVIRONMENT, LABOR, etc.), ask: what
  identifier *should* exist to connect this domain to the others, and do we have a table
  that carries it under a different column name than we're matching on? (e.g. a table
  with `provider_id` that's actually an NPI in disguise, a `permit_no` that's actually a
  PWSID.)
- Check whether known trap columns (masked/sentinel-blank IDs — cf. NPPES EIN, NOAA_AIS
  imo_number, LEIE NPI at 10.4%) have siblings nobody's checked yet. Any column that LOOKS
  like a key but hasn't been COUNT(DISTINCT)'d + value-sampled is unverified, not just low.

### Track 4 — Outside the warehouse entirely
Separate from Tracks 1-3 (which are internal-only): name candidate **public datasets we
don't have at all** that would plug an obvious hole once the domain clusters from Track 1
are visible — e.g. if Track 1 surfaces a rich but disconnected environmental cluster with
no FRS bridge, say so, don't silently drop it. This track is a list of gaps + suggested
external sources, not a build.

---

## Method rules (same discipline as the absence sweep)

- Read every source file in full before reasoning over it — no partial reads.
- Every "verified" claim needs an actual sample pulled, not a column-name match.
- No fresh warehouse SQL if SERVE_MON/SERVE_WH is still down — say so and work from
  metadata/schemas instead; don't fake a verified edge from unavailable data.
- Rank output by how many currently-isolated tables/domains a new key would unlock, not
  by table size alone — a small table that bridges two disconnected clusters beats a huge
  table that just adds another row count to an already-connected one.
- Flag every assumption you're carrying forward from the last sweep (the 895/102/793 split,
  "285 doesn't outrank the verified pool," the STEEL/STRONG tiering) and say whether you
  independently confirmed it or are just repeating it.

## Deliverable

Same shape as `absence_sweep_findings_2026-08-05.md`: ranked findings list, explicit
caveats section, explicit "what this run did NOT do" honesty section. Lead with a count:
how many of the ~793 got inventoried, how many of the 285 got opened, how many net-new
keys/domains surfaced. If full coverage isn't possible in one pass, say exactly what
fraction was covered and what's left — no silent truncation.
