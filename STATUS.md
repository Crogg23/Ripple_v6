# RIPPLE STATUS — 2026-08-11 (night) — CourtListener bulk load

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE: same one thing as last session, untouched.** The roll-call vote mart
still disagrees with its Python-built twin (113,512 vs 3,364 rows). Needs the
Python builder re-run; not forced past the standing guard. Not from this
session.

**What this session was:** loading the rest of the free court-records
publisher's data — everything Ripple didn't already have except the citation
network (upload failed, safe retry) and the giant full-text file (skipped on
purpose).

**Headlines:**

1. **Corrected a claim from last session.** Attorneys/parties for court cases
   are NOT available as a bulk file, despite what I said in chat earlier. Would
   need a separate API-key job later.
2. **21 new tables landed and modeled, all passing.** Judges' gifts, debts,
   outside income, agreements, reimbursements, spousal income, and outside
   positions; their schooling and political affiliation; the court list; 10.1M
   decision summaries; 18.1M reporter citations; 973k lower-court links; a
   federal-case-outcomes copy carrying CourtListener's own case ids. All built
   clean in the warehouse (37/37 checks passed).
3. **One piece failed and was left alone rather than retried into a mess:** the
   citation network (which case cites which) hit a cloud-upload error mid-file.
   Nothing was corrupted; it just isn't loaded yet. Safe one-command retry.
4. **The 54.6 GB full opinion text was skipped on purpose.** It's for reading
   one ruling, not for finding patterns — the decision-summary and citation
   layers that DID load carry the signal. Chris agreed after seeing the
   time/disk cost (would've been an overnight job with the disk this machine
   has free).
5. **No new links added to the entity map.** Everything new here connects to
   itself (a decision belongs to a docket, a citation belongs to a decision) by
   CourtListener's own internal ids — real relationships, but not a shared
   national ID, so nothing was added to the identity-matching rules. Judges
   still don't carry a national registry ID either; that's a real gap, not an
   oversight.

**Where this leaves the "fun stuff":** the new data is landed, modeled, and
already sitting in the warehouse tonight — it's queryable right now from either
machine once you pull. It has NOT been added to the entity map (no new
cross-source matching), so it won't show up automatically in Findings/Explore
yet; it's reachable via direct lookup/SQL against the justice-domain court
tables. Wiring judges and courts into map connections is future work, not
started.

**Live/open items:**

- Disaster-aid reload from the prior session should be checked on next boot.
- Citation-network load failed partway — retry with the same loader script,
  same file, nothing else needs to change.
- Full opinion text intentionally not loaded.
- Chris's earlier one-liner cleanup list is still outstanding.

**YOUR MOVE:**

1. Same one as last session: run the full who's-who (identity map) rebuild?
   ~4.5 hrs, ~$10-15. Nothing from tonight touched identity matching, so this
   decision is unchanged and still waiting.
2. Say the word if you want the citation-network retry or the full-text load
   queued for an overnight run later.

**NEXT SESSION:**

1. Boot trust check against this file and git log.
2. Retry the citation-network file if wanted.
3. If Chris said go on the map rebuild: run it, then re-measure connection
   precision.
4. Roll-call mart rebuild via its Python builder (still pending, unrelated to
   tonight).

**Tests:** offline suite 3,034 passing, 2 skipped, 1 pre-existing failure (the
roll-call mart, same as last session — nothing new broke).

**COST:** free-tier downloads, warehouse compute for six PUT/COPY loads plus a
21-model dbt build — small warehouse, low single-digit dollars. No agents spun
up. Full price tag for a future citation-map retry or full-text load: same as
quoted before, $10-30 one-off, ~$1-2/month.
