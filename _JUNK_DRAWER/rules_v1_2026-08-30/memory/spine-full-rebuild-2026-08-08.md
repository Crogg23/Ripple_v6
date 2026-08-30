---
name: spine-full-rebuild-2026-08-08
description: Full spine rebuild 2026-08-08 — nursing-home NPI was phantom (source has no field); incremental catch-up exposed pre-existing drift; X-Small rebuild = ~4.5h wall / ~$10-15
metadata: 
  node_type: memory
  type: project
  originSessionId: 80d42741-cbef-49d6-b923-ed5ac2bb7643
  modified: 2026-08-08T18:24:04.167Z
---

2026-08-08 session facts:

- **Nursing-home NPI resolved**: CMS Provider Information dataset (provider-data API) has NO NPI field — verified live against all 100 source columns. The staging/mart column was phantom, removed everywhere. NPI↔CCN linking lives in the facility-affiliation mart. Another instance of [[bridge-fuel-reality]] (masked/phantom ID columns).
- **Incremental spine catch-up can EXPOSE old drift it can't fix**: running connect-changed on 3 stale CMS tables made the LEIE equivalence checks fail (~99 entities with stale pairs/membership predating the run) because the incremental path only merges the symmetric diff. The designed cure is the full rebuild backstop.
- **Full `connect all` cost reality on X-Small**: ~4.5 hours wall-clock (fingerprint phase alone ~3.5h over 1,269 tables), ~4-5 credits ≈ $10-15. My 30-60 min estimate was 4-5x low — quote hours next time. Result: 31.85M entities, 4,615 edges, all 6 validate checks pass, full suite 2,692 green.
- **DROP TABLE is classifier-blocked in Claude Code even with Chris's verbal approval** — warehouse drops must be run by Chris in Snowsight; put the exact one-liner in STATUS/checklist instead of retrying.
